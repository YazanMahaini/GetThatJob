---
name: profile-intake
description: Index a job seeker's CVs and credentials, capture confirmed search preferences, and identify evidence gaps while preserving their document style.
---

# ProfileIntake

If `.getthatjob/setup.json` is absent in the selected workspace, use [SetupSkill](../setup-skill/SKILL.md) first.
If the marker says `intake_gate: awaiting-documents`, follow SetupChecker's first-use handoff and wait for the applicant's explicit continue or skip before reading CVs.

Use after setup or whenever the user supplies or updates a CV, credential, letter example, or durable profile fact. Read **every** supplied approved CV, including role-specific variants, and check `APPLICATION_PROFILE.md` for already confirmed form answers. Index the supported information from each CV in `CV_INDEX.md` and the appropriate private profile files so a variant is not ignored. Update `QUALIFICATIONS_INDEX.md`, `MEMORY.md`, `APPLICATION_PROFILE.md`, and `TARGET_ROLES.md` with only facts the sources support, citing the file or user statement and date where useful. Do not treat a CV as official proof of an award or license when a credential document conflicts. Mark conflicts and missing status clearly; do not silently merge competing claims.

Ask for the few preferences that determine search quality: role priorities, acceptable locations or remote scope, compensation and employment types, and exclusions. Read the standing submission mode from `OPERATIONS.md`; SetupSkill asks for it only on first setup, so do not ask again during intake or resumption. Update it only when the applicant explicitly changes it. Record nationality, residence, work authorization, availability, contact information, and referees only from the user or authorized sources and only when relevant. Keep application-specific answers in packets.

Identify which CV the applicant considers the original or master factual source and which are approved role-specific variants. Preserve each source file. Separately compare their visual designs: inspect page structure, typography, spacing, section order, and visual hierarchy. With one CV, use its design; with several sharing a design, record one representative. If several designs differ, ask the applicant to choose **one of their own CVs** as the design reference and save its filename under `Visual design reference` in `CV_INDEX.md`. Keep an existing choice unless the applicant changes it. Follow that design where practical without imposing a plugin CV template or redesigning it. The design choice does not restrict factual sources: use supported information across all approved CVs, subject to official evidence and conflict checks. Output format follows the applicant's request and employer requirements; Word is not a universal requirement. The generic DOCX in `CoverLetters/Template/` is the default **letter** design only. If the applicant supplies their own approved letter and wants its design, record its filename in `CoverLetters/README.md` and use it instead. Never treat the bundled template's placeholder text as an applicant fact.

When intake is complete, run [SetupChecker](../setup-checker/SKILL.md) again to confirm the indexes and remaining gaps. Continue with the user's original search request when enough information exists to make progress.
