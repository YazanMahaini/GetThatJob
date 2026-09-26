#!/usr/bin/env python3
"""Check workspace structure and the applicant documents needed to begin."""

from __future__ import annotations

import argparse
import csv
import json
import zipfile
from pathlib import Path


REQUIRED_DIRS = ("applications", "CoverLetters", "CoverLetters/Template", "CVs", "Qualifications&Certificates")
REQUIRED_FILES = (
    "AGENTS.md", "MEMORY.md", "APPLICATION_PROFILE.md", "CV_INDEX.md", "QUALIFICATIONS_INDEX.md",
    "TARGET_ROLES.md", "OPERATIONS.md", "SEARCH_LOG.md", "APPLICATIONS.csv",
    "applications/README.md", "CoverLetters/README.md", "CoverLetters/Template/README.md",
    "CoverLetters/Template/GetThatJob_Default_Cover_Letter_Style.docx", "CVs/README.md",
    "Qualifications&Certificates/README.md", ".getthatjob/setup.json",
)
TRACKER_FIELDS = (
    "id", "employer", "role", "location", "work_arrangement", "source",
    "posting_url", "portal_url", "requisition_id", "date_found", "deadline",
    "status", "portal_status", "nationality_eligibility", "work_authorization",
    "paid_status", "compensation", "fit_summary", "cv_file", "packet_path",
    "date_submitted", "confirmation", "follow_up", "notes",
)
DOCUMENT_SUFFIXES = {".docx", ".doc", ".pdf", ".odt", ".rtf", ".txt", ".md"}
DEFAULT_LETTER = "GetThatJob_Default_Cover_Letter_Style.docx"


def source_documents(folder: Path) -> list[Path]:
    if not folder.is_dir():
        return []
    return sorted(
        file for file in folder.rglob("*")
        if file.is_file() and file.name.lower() != "readme.md"
        and not file.name.startswith(("~$", "."))
    )


def check_document(file: Path) -> str | None:
    if file.stat().st_size == 0:
        return "is empty"
    if file.suffix.lower() not in DOCUMENT_SUFFIXES:
        return "has an unrecognized document format; review manually"
    if file.suffix.lower() == ".docx":
        try:
            with zipfile.ZipFile(file) as archive:
                if archive.testzip() is not None or "word/document.xml" not in archive.namelist():
                    return "is not a readable Word document"
        except (OSError, zipfile.BadZipFile):
            return "is not a readable Word document"
    if file.suffix.lower() == ".pdf":
        with file.open("rb") as stream:
            if stream.read(5) != b"%PDF-":
                return "does not have a PDF header"
    return None


def check(workspace: Path) -> dict[str, object]:
    workspace = workspace.expanduser().resolve()
    marker_path = workspace / ".getthatjob" / "setup.json"
    if marker_path.is_file():
        try:
            marker = json.loads(marker_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            marker = {}
        if marker.get("intake_gate") == "awaiting-documents":
            return {
                "status": "awaiting-documents", "workspace": str(workspace),
                "message": "Pause before checking CVs. Invite the applicant to add files, then wait for an explicit continue or skip.",
                "folders": ["CVs/", "Qualifications&Certificates/", "CoverLetters/Template/"],
            }
    repair: list[str] = []
    input_needed: list[str] = []
    notes: list[str] = []
    for item in REQUIRED_DIRS:
        if not (workspace / item).is_dir():
            repair.append(f"Missing folder: {item}/")
    for item in REQUIRED_FILES:
        if not (workspace / item).is_file():
            repair.append(f"Missing file: {item}")

    tracker = workspace / "APPLICATIONS.csv"
    if tracker.is_file():
        try:
            with tracker.open(encoding="utf-8-sig", newline="") as stream:
                fields = csv.DictReader(stream).fieldnames or []
            missing = [field for field in TRACKER_FIELDS if field not in fields]
            if missing:
                repair.append("APPLICATIONS.csv is missing columns: " + ", ".join(missing))
        except (OSError, UnicodeError, csv.Error):
            repair.append("APPLICATIONS.csv could not be read")

    cv_files = source_documents(workspace / "CVs")
    valid_cvs: list[Path] = []
    for file in cv_files:
        problem = check_document(file)
        if problem:
            repair.append(f"CVs/{file.relative_to(workspace / 'CVs').as_posix()} {problem}")
        else:
            valid_cvs.append(file)
    if not valid_cvs:
        input_needed.append("Add at least one current, user-approved CV to CVs/.")

    cv_index = workspace / "CV_INDEX.md"
    if cv_index.is_file():
        index_text = cv_index.read_text(encoding="utf-8", errors="replace")
        for file in valid_cvs:
            if file.name not in index_text:
                input_needed.append(f"Index CVs/{file.name} in CV_INDEX.md, including approval and use notes.")

    credential_files = source_documents(workspace / "Qualifications&Certificates")
    qualification_index = workspace / "QUALIFICATIONS_INDEX.md"
    if qualification_index.is_file():
        index_text = qualification_index.read_text(encoding="utf-8", errors="replace")
        for file in credential_files:
            problem = check_document(file)
            if problem:
                repair.append(f"Qualifications&Certificates/{file.relative_to(workspace / 'Qualifications&Certificates').as_posix()} {problem}")
            elif file.name not in index_text:
                input_needed.append(f"Index Qualifications&Certificates/{file.name} in QUALIFICATIONS_INDEX.md.")
    if not credential_files:
        notes.append("No credential evidence added; verify qualification claims before using them.")

    target_roles = workspace / "TARGET_ROLES.md"
    if target_roles.is_file():
        content = target_roles.read_text(encoding="utf-8", errors="replace")
        if not any(line.startswith("| ") and "[Ask" not in line and "---" not in line
                   and "Priority" not in line for line in content.splitlines()):
            input_needed.append("Record at least one confirmed target role in TARGET_ROLES.md.")
    memory = workspace / "MEMORY.md"
    if memory.is_file():
        content = memory.read_text(encoding="utf-8", errors="replace")
        if "[Add from user or approved CV]" in content:
            input_needed.append("Record the applicant's preferred name and source in MEMORY.md.")

    cover_files = source_documents(workspace / "CoverLetters")
    custom_cover_files = [file for file in cover_files
                          if file.relative_to(workspace / "CoverLetters").as_posix()
                          != f"Template/{DEFAULT_LETTER}"]
    if not custom_cover_files:
        notes.append("Use the bundled generic cover-letter design unless the applicant chooses their own letter reference.")
    for file in cover_files:
        problem = check_document(file)
        if problem:
            repair.append(f"CoverLetters/{file.relative_to(workspace / 'CoverLetters').as_posix()} {problem}")

    status = "repair-needed" if repair else "needs-input" if input_needed else "ready"
    return {
        "status": status,
        "workspace": str(workspace),
        "cv_count": len(valid_cvs),
        "credential_count": len(credential_files),
        "cover_letter_source_count": len(custom_cover_files),
        "default_cover_letter_template": (workspace / "CoverLetters" / "Template" / DEFAULT_LETTER).is_file(),
        "repair": repair,
        "input_needed": input_needed,
        "notes": notes,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()
    result = check(args.workspace)
    print(json.dumps(result, indent=2))
    raise SystemExit({"ready": 0, "repair-needed": 1, "needs-input": 2,
                      "awaiting-documents": 2}[str(result["status"])])


if __name__ == "__main__":
    main()
