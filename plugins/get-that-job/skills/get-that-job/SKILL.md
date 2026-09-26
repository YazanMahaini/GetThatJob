---
name: get-that-job
description: Route GetThatJob requests through first-use setup, document intake, job search, the saved submission choice, and confirmation tracking.
---

# GetThatJob

Use this as the plugin's entry point. Resolve the applicant workspace from the user's explicit path, then an existing workspace in the current project, or a new `GetThatJob` folder beside an unrelated current project. Do not place applicant documents in the plugin source. Explain the selected location.

Before other plugin work, inspect `.getthatjob/setup.json` in that workspace. If absent, use [SetupSkill](../setup-skill/SKILL.md) once. For an established applicant workspace, preview additions first and preserve every existing folder, Markdown file, tracker row, document, and application packet. The marker is per workspace: a different applicant or new workspace needs its own first setup. If present, never rerun setup merely because a source file is missing; use [SetupChecker](../setup-checker/SKILL.md) to find gaps and repair only the affected workspace files as appropriate.

SetupSkill asks for the applicant's confirmation email plugin `@` mention during first setup and records the selected plugin in that workspace's `OPERATIONS.md`. On resumption, read that choice and do not ask again. Use the selected plugin for later read-only confirmation checks; if unavailable, report that limitation without changing plugins silently.

SetupSkill also asks once whether to stop at a checked draft or submit complete applications automatically. Read the standing `Submission mode` in `OPERATIONS.md` on every run; a missing mode in an older workspace means `stop-and-wait`. Do not ask again on resumption. Update the mode only when the applicant explicitly changes it. The active instruction for a specific application can override the standing mode for that application.

Route the active request:

- New or changed CVs, cover letters, certificates, or profile facts: [SetupChecker](../setup-checker/SKILL.md), then [ProfileIntake](../profile-intake/SKILL.md).
- A filled or materially updated application draft, including one filled outside JobFinder: [ProfileBuilder](../profile-builder/SKILL.md) after verifying its answers.
- Search, screen, or prepare a role: [JobFinder](../job-finder/SKILL.md). Continue useful searching while unresolved profile inputs are identified.
- A checked application under `automatic-submit`, or a specific application the user directs Codex to submit: [ApplicationFinalize](../application-finalize/SKILL.md).
- A submitted application's receipt, including a short report such as "I applied, check email" or "Submitted. Check email and confirm": [EmailConfirmationChecker](../email-confirmation-checker/SKILL.md).
- A later employer update, recruiter message, interview, or outcome: [ApplicationFollowUp](../application-follow-up/SKILL.md).

The workspace files, rather than this plugin, hold the applicant's facts, priorities, CV style, permissions, and opportunity history. Follow the user's active instruction when it supersedes a workspace preference. Never infer signing permission from permission to search, draft, or submit.
