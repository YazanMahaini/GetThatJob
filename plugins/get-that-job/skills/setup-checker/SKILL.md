---
name: setup-checker
description: Check a GetThatJob workspace after setup or document uploads for required folders, a usable CV, source indexes, and missing applicant inputs.
---

# SetupChecker

If `.getthatjob/setup.json` is absent in the selected workspace, use [SetupSkill](../setup-skill/SKILL.md) first. Do not bypass first-use setup when this skill is invoked directly.

Resolve `../../scripts/check_workspace.py` relative to this SKILL.md and run it with an available Python 3 interpreter and `--workspace <path>`. If scaffold files are missing in a workspace with a setup marker, preview `../../scripts/setup_workspace.py --workspace <path> --repair --dry-run`, then run it with `--repair` and recheck; repair copies only missing generic templates and preserves the marker and all applicant files. An existing but malformed file is reported for review, never replaced with a blank template. If Python is unavailable, inspect and restore missing template files directly from `../../assets/workspace/`, using create-only operations. Exit 2 means the structure exists but user input is still needed; it is not a tool failure. Read the JSON result and inspect the actual new documents when a format or claim is uncertain. The script checks presence and basic file integrity; it cannot certify that a CV is current, a credential claim is true, or a document's visual layout is sound.

The minimum source document for tailoring is one readable, user-approved CV. A previous cover letter is optional. Credential evidence is required only when the particular claim or application requires proof; record an absent proof as unresolved. Check that `APPLICATION_PROFILE.md` exists, that every supplied CV and credential file is indexed, that role targets are user-confirmed, and that names and application answers come from the person's sources. Give a concise list of missing or unusable files and the exact folder for each. Do not substitute plugin samples, another applicant's files, or invented facts.

If a user has just added files, continue with [ProfileIntake](../profile-intake/SKILL.md) to interpret and index them. Do not rerun one-time setup when the marker exists.

Read the confirmation email plugin choice from `OPERATIONS.md` when reporting setup status. On a resumed workspace, do not ask for its `@` mention again. If a choice is absent, report that email receipt checking is not configured; continue other work and accept a plugin only when the applicant explicitly supplies or changes one. Existing workspace instructions that already name an email provider count as a recorded choice even if they predate the template's structured field.
