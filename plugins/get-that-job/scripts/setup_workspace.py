#!/usr/bin/env python3
"""Create or safely repair a GetThatJob workspace without replacing applicant files."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = PLUGIN_ROOT / "assets" / "workspace"
MARKER = Path(".getthatjob") / "setup.json"


def setup(workspace: Path, *, repair: bool = False) -> dict[str, object]:
    workspace = workspace.expanduser().resolve()
    if workspace == PLUGIN_ROOT or PLUGIN_ROOT in workspace.parents:
        raise ValueError("Choose an applicant workspace outside the plugin source.")
    marker_path = workspace / MARKER
    marker_exists = marker_path.exists()
    if marker_exists and not repair:
        return {"status": "already-initialized", "workspace": str(workspace), "created": []}

    workspace.mkdir(parents=True, exist_ok=True)
    created: list[str] = []
    for source in sorted(TEMPLATE_ROOT.rglob("*")):
        relative = source.relative_to(TEMPLATE_ROOT)
        destination = workspace / relative
        if source.is_dir():
            if destination.exists() and not destination.is_dir():
                raise ValueError(f"Expected a folder: {destination}")
            if not destination.exists():
                destination.mkdir(parents=True)
                created.append(relative.as_posix() + "/")
        elif source.is_file():
            if destination.exists():
                if not destination.is_file():
                    raise ValueError(f"Expected a file: {destination}")
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            created.append(relative.as_posix())

    if marker_exists:
        return {"status": "repaired", "workspace": str(workspace), "created": created}

    marker_path.parent.mkdir(parents=True, exist_ok=True)
    marker = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "workspace": str(workspace),
    }
    temporary = marker_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(marker, indent=2) + "\n", encoding="utf-8")
    temporary.replace(marker_path)
    return {"status": "initialized", "workspace": str(workspace), "created": created}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--repair", action="store_true", help="Restore missing template files without changing an existing setup marker")
    args = parser.parse_args()
    result = setup(args.workspace, repair=args.repair)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
