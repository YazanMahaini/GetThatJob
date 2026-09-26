---
name: application-finalize
description: Recheck and submit a specific checked job application under the applicant's standing automatic-submit choice or a direct submission instruction, then record reliable evidence.
---

# ApplicationFinalize

If `.getthatjob/setup.json` is absent in the selected workspace, use [SetupSkill](../setup-skill/SKILL.md) first, preserving any existing application records.

Use when the user explicitly directs final submission of a specific prepared application, or when a complete checked draft is handed off under `automatic-submit` in `OPERATIONS.md`. A missing mode means `stop-and-wait`. Read workspace `AGENTS.md`, `OPERATIONS.md`, and `APPLICATION_PROFILE.md`, its tracker row and packet, the live posting, and the current portal draft. Verify the employer and destination, requisition, eligibility, deadline, fees, duplicate status, answers, and final document versions. Ask only about an unresolved required fact or commitment that cannot be sourced.

The applicant's direct instruction or saved `automatic-submit` mode authorizes the final Apply/Submit control for a fully checked, eligible application without another approval. Neither authorizes entering the user's name in an e-signature or certification-signature field, checking a signature-equivalent affirmation, or signing a binding declaration. Obtain explicit instruction to sign that particular application when such a field blocks submission. Preserve the standing mode unless the applicant explicitly changes it; a one-off submission instruction changes only that application. Do not pay fees or accept employment terms as part of routine submission.

After a permitted final action, inspect the confirmation page or application history. Record the observed timestamp, exact employer status, and evidence in the packet and `APPLICATIONS.csv`; mark `submitted` only when the evidence establishes it. If the result is unclear, record an unresolved attempt rather than claiming success. If final corrections introduced newly verified reusable answers, invoke [ProfileBuilder](../profile-builder/SKILL.md). Then use [EmailConfirmationChecker](../email-confirmation-checker/SKILL.md) to check the selected email plugin and record a matching receipt or the precise access limitation.
