---
name: profile-intake
description: Index a job seeker's CVs and credentials, capture confirmed search preferences, and identify evidence gaps while preserving their document style.
---

# ProfileIntake

If `.getthatjob/setup.json` is absent in the selected workspace, use [SetupSkill](../setup-skill/SKILL.md) first.

Use after setup or whenever the user supplies or updates a CV, credential, letter example, or durable profile fact. Read the supplied source itself. Update `CV_INDEX.md`, `QUALIFICATIONS_INDEX.md`, `MEMORY.md`, and `TARGET_ROLES.md` with only facts the sources support, citing the file or user statement and date where useful. Do not treat a CV as official proof of an award or license when a credential document conflicts. Mark conflicts and missing status clearly.

Ask for the few preferences that determine search quality: role priorities, acceptable locations or remote scope, compensation and employment types, exclusions, and submission preference. Record nationality, residence, work authorization, availability, contact information, and referees only from the user or authorized sources and only when relevant. Keep application-specific answers in packets.

Identify which CV the user considers the original or master source and which are approved role-specific variants. Preserve each source file. The user's selected CV controls the tailored CV's style, even when it differs from the creator's: inspect page structure, typography, spacing, section order, and visual hierarchy, then match it where practical. Do not impose a plugin template or automatically redesign it. Output format follows the user's source, explicit request, and employer requirements; Word is not a universal requirement. A cover-letter reference is optional and must come from this applicant or a direct user choice.

When intake is complete, run [SetupChecker](../setup-checker/SKILL.md) again to confirm the indexes and remaining gaps. Continue with the user's original search request when enough information exists to make progress.
