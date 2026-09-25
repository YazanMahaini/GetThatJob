---
name: email-confirmation-checker
description: Check a specific recently submitted job application's confirmation email and record matched receipt evidence without changing mailbox messages.
---

# EmailConfirmationChecker

If `.getthatjob/setup.json` is absent in the selected workspace, use [SetupSkill](../setup-skill/SKILL.md) first, preserving any existing application records.

Use after the applicant says a prepared application was submitted, after an authorized final submission, or when they ask for its confirmation. Read `AGENTS.md`, `OPERATIONS.md`, that application's `APPLICATIONS.csv` row, and its packet first. Use the applicant's configured mailbox connector (Outlook in a workspace that specifies Outlook), or a signed-in email UI, for a **read-only** search of that application, not general inbox triage. If access requires sign-in, prompt the user to connect or sign in through the provider's official flow and resume when available; do not request credentials in chat. Do not send, reply, delete, move, or alter messages.

Search narrowly by employer, role or requisition, and submission window; widen only as needed. Match employer, role/requisition, recipient when visible, and timing. Distinguish an explicit application-received acknowledgement from account creation, a saved draft, marketing mail, or later status updates. Fetch message details only when the preview is insufficient.

Record sender, exact subject, received time and zone, stable message link if available, and the short evidence establishing receipt. Compare portal evidence when available. Update the matching tracker row and packet, preserving history and keeping the employer's exact portal or email status separate from the internal stage. Mark `submitted` only when evidence establishes submission. Do not infer a new submission from a portal's last-updated time after merely viewing or editing a record. If no connected mailbox or matching receipt exists, report that precise limit and retain the last verified stage. Do not copy private email contents beyond what the packet needs. Update `MEMORY.md` only for a durable profile change, not routine application status. Tell the applicant which application was checked, whether a receipt matched, when it arrived, the recorded status, and any discrepancy.
