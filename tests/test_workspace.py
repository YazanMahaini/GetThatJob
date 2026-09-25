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
from setup_workspace import setup  # noqa: E402


class WorkspaceTests(unittest.TestCase):
    def test_existing_applicant_files_survive_first_and_repeat_setup(self) -> None:
        with tempfile.TemporaryDirectory(prefix="getthatjob-test-") as directory:
            workspace = Path(directory)
            instructions = workspace / "AGENTS.md"
            instructions.write_text("Applicant-owned instructions\n", encoding="utf-8")
            first = setup(workspace)
            second = setup(workspace)
            self.assertEqual(first["status"], "initialized")
            self.assertEqual(second["status"], "already-initialized")
            self.assertEqual(instructions.read_text(encoding="utf-8"), "Applicant-owned instructions\n")
            self.assertTrue((workspace / ".getthatjob" / "setup.json").is_file())
            self.assertTrue((workspace / "APPLICATION_PROFILE.md").is_file())
            marker_before = (workspace / ".getthatjob" / "setup.json").read_text(encoding="utf-8")
            (workspace / "APPLICATION_PROFILE.md").unlink()
            repaired = setup(workspace, repair=True)
            self.assertEqual(repaired["status"], "repaired")
            self.assertTrue((workspace / "APPLICATION_PROFILE.md").is_file())
            self.assertEqual((workspace / ".getthatjob" / "setup.json").read_text(encoding="utf-8"), marker_before)
            self.assertEqual(instructions.read_text(encoding="utf-8"), "Applicant-owned instructions\n")

    def test_document_readiness_and_invalid_word_file(self) -> None:
        with tempfile.TemporaryDirectory(prefix="getthatjob-test-") as directory:
            workspace = Path(directory)
            setup(workspace)
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
            self.assertEqual(check(workspace)["status"], "ready")

            (workspace / "CVs" / "Broken.docx").write_text("not a Word document", encoding="utf-8")
            damaged = check(workspace)
            self.assertEqual(damaged["status"], "repair-needed")
            self.assertTrue(any("Broken.docx" in item for item in damaged["repair"]))

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
