---
name: setup-skill
description: Initialize a GetThatJob applicant workspace once on its first use, creating private folders and blank workflow records without overwriting existing files.
---

# SetupSkill

Use only when the selected applicant workspace lacks `.getthatjob/setup.json`. First use is **per workspace**, not once per plugin installation; otherwise one person's setup would prevent another person's workspace from being created. Do not run against the plugin source.

Choose the workspace by the explicit user path when provided. Otherwise use an empty or clearly designated job-search current workspace; if the current directory is an unrelated project, create a `GetThatJob` sibling. Tell the user the path. Resolve `../../scripts/setup_workspace.py` relative to this SKILL.md and run it with an available Python 3 interpreter and `--workspace <path>`. If Python is unavailable, create the same files from `../../assets/workspace/` with local file tools, copying only absent files, then write `.getthatjob/setup.json` with a creation time. The script creates `applications/`, `CoverLetters/Template/`, `CVs/`, `Qualifications&Certificates/`, workflow Markdown files, `APPLICATIONS.csv`, and the one-time marker. It preserves existing applicant files.

Then run [SetupChecker](../setup-checker/SKILL.md). Report the specific documents and profile inputs the user should add. An empty cover-letter template or credential folder does not prevent setup. Never copy the creator's CVs, letter design, identity, country, or role preferences into the new workspace.
