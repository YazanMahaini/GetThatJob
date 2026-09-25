---
name: application-finalize
description: Recheck and complete a specific reviewed job application only when the user has authorized its final submission, then record reliable submission evidence.
---

# ApplicationFinalize

If `.getthatjob/setup.json` is absent in the selected workspace, use [SetupSkill](../setup-skill/SKILL.md) first, preserving any existing application records.

Use when the user explicitly directs final submission of a specific prepared application. Read workspace `AGENTS.md` and `OPERATIONS.md`, its tracker row and packet, the live posting, and the current portal draft. Verify the employer and destination, requisition, eligibility, deadline, fees, duplicate status, answers, and final document versions. Ask only about an unresolved required fact or commitment that cannot be sourced.

The instruction to submit authorizes the final Apply/Submit control for that application. It does **not** authorize entering the user's name in an e-signature or certification-signature field, checking a signature-equivalent affirmation, or signing a binding declaration. Obtain explicit instruction to sign that particular application when such a field blocks submission. Preserve the user's standing review preference unless their current instruction supersedes it. Do not pay fees or accept employment terms as part of routine submission.

After a permitted final action, inspect the confirmation page or application history. Record the observed timestamp, exact employer status, and evidence in the packet and `APPLICATIONS.csv`; mark `submitted` only when the evidence establishes it. If the result is unclear, record an unresolved attempt rather than claiming success. Then use [EmailConfirmationChecker](../email-confirmation-checker/SKILL.md) when email access is available or the user asks for receipt verification.
