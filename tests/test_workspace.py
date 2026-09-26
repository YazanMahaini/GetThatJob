"""Behavior checks for the portable GetThatJob workspace helpers."""

from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "get-that-job"
sys.path.insert(0, str(PLUGIN / "scripts"))

from check_workspace import TRACKER_FIELDS, check  # noqa: E402
from setup_workspace import acknowledge_documents, setup  # noqa: E402


class WorkspaceTests(unittest.TestCase):
    def test_existing_applicant_files_survive_first_and_repeat_setup(self) -> None:
        with tempfile.TemporaryDirectory(prefix="getthatjob-test-") as directory:
            workspace = Path(directory)
            instructions = workspace / "AGENTS.md"
            instructions.write_text("Applicant-owned instructions\n", encoding="utf-8")
            tracker = workspace / "APPLICATIONS.csv"
            tracker.write_bytes(b"Applicant-owned tracker\r\n")
            operations = workspace / "OPERATIONS.md"
            operations.write_text(
                "Applicant-owned workflow\nEmail confirmation uses Outlook.\n"
                "Submission mode: automatic-submit\n",
                encoding="utf-8",
            )
            (workspace / "CVs").mkdir()
            cv = workspace / "CVs" / "Approved CV.docx"
            cv.write_bytes(b"Applicant-owned CV")
            existing = {file.relative_to(workspace): file.read_bytes()
                        for file in workspace.rglob("*") if file.is_file()}
            preview = setup(workspace, dry_run=True)
            self.assertEqual(preview["status"], "preview-initialize")
            self.assertFalse((workspace / ".getthatjob").exists())
            self.assertFalse((workspace / "APPLICATION_PROFILE.md").exists())
            self.assertEqual({file.relative_to(workspace): file.read_bytes()
                              for file in workspace.rglob("*") if file.is_file()}, existing)
            first = setup(workspace)
            second = setup(workspace)
            self.assertEqual(first["status"], "initialized")
            self.assertEqual(second["status"], "already-initialized")
            for relative, content in existing.items():
                self.assertEqual((workspace / relative).read_bytes(), content)
            self.assertEqual(instructions.read_text(encoding="utf-8"), "Applicant-owned instructions\n")
            self.assertEqual(
                operations.read_text(encoding="utf-8"),
                "Applicant-owned workflow\nEmail confirmation uses Outlook.\n"
                "Submission mode: automatic-submit\n",
            )
            self.assertTrue((workspace / ".getthatjob" / "setup.json").is_file())
            self.assertTrue((workspace / "APPLICATION_PROFILE.md").is_file())
            marker_before = (workspace / ".getthatjob" / "setup.json").read_text(encoding="utf-8")
            profile = workspace / "APPLICATION_PROFILE.md"
            profile.write_text(
                profile.read_text(encoding="utf-8")
                + "\n| Preferred contact time | Morning | Applicant, 2026-01-01 | General | 2026-01-02 |\n",
                encoding="utf-8",
            )
            saved_profile = profile.read_text(encoding="utf-8")
            setup(workspace, repair=True)
            self.assertEqual(profile.read_text(encoding="utf-8"), saved_profile)
            profile.unlink()
            repaired = setup(workspace, repair=True)
            self.assertEqual(repaired["status"], "repaired")
            self.assertTrue((workspace / "APPLICATION_PROFILE.md").is_file())
            self.assertEqual((workspace / ".getthatjob" / "setup.json").read_text(encoding="utf-8"), marker_before)
            self.assertEqual(instructions.read_text(encoding="utf-8"), "Applicant-owned instructions\n")

    def test_document_readiness_and_invalid_word_file(self) -> None:
        with tempfile.TemporaryDirectory(prefix="getthatjob-test-") as directory:
            workspace = Path(directory)
            setup(workspace)
            self.assertEqual(check(workspace)["status"], "awaiting-documents")
            acknowledge_documents(workspace)
            empty = check(workspace)
            self.assertEqual(empty["status"], "needs-input")
            self.assertEqual(empty["repair"], [])

            cv = workspace / "CVs" / "Example CV.txt"
            cv.write_text("Synthetic Applicant\nProject coordination\n", encoding="utf-8")
            with (workspace / "CV_INDEX.md").open("a", encoding="utf-8") as stream:
                stream.write("\n| Example CV.txt | Yes | TXT | Approved source |\n")
            memory = workspace / "MEMORY.md"
            memory.write_text(
                memory.read_text(encoding="utf-8").replace(
                    "[Add from user or approved CV]", "Synthetic Applicant (Example CV.txt)"
                ),
                encoding="utf-8",
            )
            with (workspace / "TARGET_ROLES.md").open("a", encoding="utf-8") as stream:
                stream.write("\n| 1 | Project Coordinator | Local | Paid | Example CV.txt |\n")
            missing_choices = check(workspace)
            self.assertEqual(missing_choices["status"], "needs-input")
            self.assertTrue(any("stipend" in item for item in missing_choices["input_needed"]))
            targets = workspace / "TARGET_ROLES.md"
            answers = {
                "Pay rule": "Paid only; available stipends count as paid",
                "Employment types": "Full-time, part-time, internships, and contracts",
                "Current country of residence": "Exampleland (applicant statement)",
                "Search geography and order": "Exampleland first, then remote roles based there",
                "Mobility and authorization limits": "No relocation; verify each posting",
                "Minimum compensation": "No minimum",
            }
            lines = targets.read_text(encoding="utf-8").splitlines()
            updated = []
            for line in lines:
                if line.startswith("- ") and ":" in line:
                    label = line[2:].split(":", 1)[0]
                    if label in answers:
                        line = f"- {label}: {answers[label]}"
                updated.append(line)
            targets.write_text("\n".join(updated) + "\n", encoding="utf-8")
            self.assertEqual(check(workspace)["status"], "ready")

            (workspace / "CVs" / "Broken.docx").write_text("not a Word document", encoding="utf-8")
            damaged = check(workspace)
            self.assertEqual(damaged["status"], "repair-needed")
            self.assertTrue(any("Broken.docx" in item for item in damaged["repair"]))

    def test_first_use_handoff_persists_until_explicit_release(self) -> None:
        with tempfile.TemporaryDirectory(prefix="getthatjob-test-") as directory:
            workspace = Path(directory)
            setup(workspace)
            marker = workspace / ".getthatjob" / "setup.json"
            cv = workspace / "CVs" / "Approved CV.txt"
            cv.write_text("Synthetic applicant", encoding="utf-8")
            self.assertEqual(json.loads(marker.read_text(encoding="utf-8"))["intake_gate"], "awaiting-documents")
            pending = check(workspace)
            self.assertEqual(pending["status"], "awaiting-documents")
            self.assertNotIn("cv_count", pending)
            self.assertEqual(setup(workspace)["status"], "already-initialized")
            self.assertEqual(check(workspace)["status"], "awaiting-documents")
            self.assertEqual(acknowledge_documents(workspace)["status"], "documents-acknowledged")
            self.assertEqual(json.loads(marker.read_text(encoding="utf-8"))["intake_gate"], "released")
            self.assertEqual(check(workspace)["cv_count"], 1)
            self.assertEqual(acknowledge_documents(workspace)["status"], "no-pending-handoff")
            default = workspace / "CoverLetters" / "Template" / "GetThatJob_Default_Cover_Letter_Style.docx"
            self.assertTrue(default.is_file())
            self.assertTrue(check(workspace)["default_cover_letter_template"])
            self.assertEqual(check(workspace)["cover_letter_source_count"], 0)

    def test_workspace_choices_survive_repeat_setup_and_repair(self) -> None:
        with tempfile.TemporaryDirectory(prefix="getthatjob-test-") as directory:
            workspace = Path(directory)
            setup(workspace)
            operations = workspace / "OPERATIONS.md"
            cv_index = workspace / "CV_INDEX.md"
            self.assertIn("Chosen CV design reference (filename in `CVs/`): Not selected", cv_index.read_text(encoding="utf-8"))
            template = operations.read_text(encoding="utf-8")
            self.assertIn("## Confirmation email plugin", template)
            self.assertIn("Selected Codex email plugin:", template)
            self.assertIn("## Submission preference", template)
            self.assertIn("Submission mode: `stop-and-wait`", template)

            chosen = (
                "# Applicant operations\n\n"
                "## Confirmation email plugin\n\n"
                "- Selected Codex email plugin: gmail@openai-curated-remote\n"
                "\n## Submission preference\n\n"
                "- Submission mode: `automatic-submit`\n"
            )
            operations.write_text(chosen, encoding="utf-8")
            chosen_design = cv_index.read_text(encoding="utf-8").replace(
                "Chosen CV design reference (filename in `CVs/`): Not selected",
                "Chosen CV design reference (filename in `CVs/`): Synthetic CV B.docx",
            )
            cv_index.write_text(chosen_design, encoding="utf-8")
            self.assertEqual(setup(workspace)["status"], "already-initialized")
            setup(workspace, repair=True)
            self.assertEqual(operations.read_text(encoding="utf-8"), chosen)
            self.assertEqual(cv_index.read_text(encoding="utf-8"), chosen_design)

    def test_older_marker_does_not_start_a_new_document_handoff(self) -> None:
        with tempfile.TemporaryDirectory(prefix="getthatjob-test-") as directory:
            workspace = Path(directory)
            setup(workspace)
            marker_path = workspace / ".getthatjob" / "setup.json"
            marker = json.loads(marker_path.read_text(encoding="utf-8"))
            marker.pop("intake_gate")
            marker_path.write_text(json.dumps(marker), encoding="utf-8")
            self.assertNotEqual(check(workspace)["status"], "awaiting-documents")

    def test_tracker_matches_marketplace_and_reference_schema(self) -> None:
        with tempfile.TemporaryDirectory(prefix="getthatjob-test-") as directory:
            workspace = Path(directory)
            setup(workspace)
            with (workspace / "APPLICATIONS.csv").open(encoding="utf-8", newline="") as stream:
                self.assertEqual(tuple(csv.DictReader(stream).fieldnames or ()), TRACKER_FIELDS)

        marketplace = json.loads((ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
        entry = next(item for item in marketplace["plugins"] if item["name"] == "get-that-job")
        self.assertEqual(marketplace["name"], "get-that-job")
        self.assertEqual(entry["source"]["path"], "./plugins/get-that-job")
        manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], entry["name"])


if __name__ == "__main__":
    unittest.main()
