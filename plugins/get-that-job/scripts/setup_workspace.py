#!/usr/bin/env python3
"""Create or safely repair a GetThatJob workspace without replacing applicant files."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = PLUGIN_ROOT / "assets" / "workspace"
MARKER = Path(".getthatjob") / "setup.json"


def acknowledge_documents(workspace: Path) -> dict[str, object]:
    """Release the first-use handoff only after the applicant explicitly resumes."""
    workspace = workspace.expanduser().resolve()
    marker_path = workspace / MARKER
    if marker_path.is_symlink() or marker_path.parent.is_symlink() or not marker_path.is_file():
        raise ValueError("A regular setup marker is required before resuming intake.")
    marker = json.loads(marker_path.read_text(encoding="utf-8"))
    if marker.get("intake_gate") != "awaiting-documents":
        return {"status": "no-pending-handoff", "workspace": str(workspace)}
    marker["intake_gate"] = "released"
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=marker_path.parent,
                                         prefix="setup-", suffix=".tmp", delete=False) as stream:
            temporary = stream.name
            stream.write(json.dumps(marker, indent=2) + "\n")
        os.replace(temporary, marker_path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)
    return {"status": "documents-acknowledged", "workspace": str(workspace)}


def setup(workspace: Path, *, repair: bool = False, dry_run: bool = False) -> dict[str, object]:
    workspace = workspace.expanduser().resolve()
    if workspace == PLUGIN_ROOT or PLUGIN_ROOT in workspace.parents:
        raise ValueError("Choose an applicant workspace outside the plugin source.")
    marker_path = workspace / MARKER
    if marker_path.is_symlink() or marker_path.parent.is_symlink():
        raise ValueError("Setup marker path must not be a symbolic link.")
    if marker_path.exists() and not marker_path.is_file():
        raise ValueError("Setup marker path must be a file.")
    marker_exists = marker_path.exists()
    if marker_exists and not repair:
        return {"status": "already-initialized", "workspace": str(workspace), "created": []}

    created: list[str] = []
    for source in sorted(TEMPLATE_ROOT.rglob("*")):
        relative = source.relative_to(TEMPLATE_ROOT)
        destination = workspace / relative
        if any((workspace / Path(*relative.parts[:index])).is_symlink()
               for index in range(1, len(relative.parts) + 1)):
            raise ValueError(f"Refusing symbolic-link destination: {destination}")
        if source.is_dir():
            if destination.exists() and not destination.is_dir():
                raise ValueError(f"Expected a folder: {destination}")
            if not destination.exists():
                if not dry_run:
                    destination.mkdir(parents=True, exist_ok=True)
                created.append(relative.as_posix() + "/")
        elif source.is_file():
            if destination.exists():
                if not destination.is_file():
                    raise ValueError(f"Expected a file: {destination}")
                continue
            if not dry_run:
                destination.parent.mkdir(parents=True, exist_ok=True)
                try:
                    with source.open("rb") as template, destination.open("xb") as applicant_file:
                        shutil.copyfileobj(template, applicant_file)
                except FileExistsError:
                    if not destination.is_file():
                        raise ValueError(f"Expected a file: {destination}") from None
                    continue
            created.append(relative.as_posix())

    if dry_run:
        if not marker_exists:
            created.append(MARKER.as_posix())
        return {"status": "preview-repair" if marker_exists else "preview-initialize",
                "workspace": str(workspace), "would_create": created}

    if marker_exists:
        return {"status": "repaired", "workspace": str(workspace), "created": created}

    marker_path.parent.mkdir(parents=True, exist_ok=True)
    marker = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "workspace": str(workspace),
        "intake_gate": "awaiting-documents",
    }
    try:
        with marker_path.open("x", encoding="utf-8") as marker_file:
            marker_file.write(json.dumps(marker, indent=2) + "\n")
    except FileExistsError:
        return {"status": "already-initialized", "workspace": str(workspace), "created": created}
    return {"status": "initialized", "workspace": str(workspace), "created": created}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--repair", action="store_true", help="Restore missing template files without changing an existing setup marker")
    parser.add_argument("--dry-run", action="store_true", help="List additions without changing the workspace")
    parser.add_argument("--documents-ready", action="store_true",
                        help="Release the first-use document handoff after the applicant says to continue")
    args = parser.parse_args()
    if args.documents_ready and (args.repair or args.dry_run):
        parser.error("--documents-ready cannot be combined with --repair or --dry-run")
    result = (acknowledge_documents(args.workspace) if args.documents_ready
              else setup(args.workspace, repair=args.repair, dry_run=args.dry_run))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
