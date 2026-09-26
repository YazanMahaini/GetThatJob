# Job search and application operations

## Workspace lifecycle

Setup runs once for this workspace and writes `.getthatjob/setup.json`. Run SetupChecker after the user adds or changes source documents, and use ProfileIntake to index verified information. Read `APPLICATION_PROFILE.md` before asking for recurring form answers. Missing inputs are questions to resolve, not permission to invent facts.

## Confirmation email plugin

- Selected Codex email plugin: [Ask once during first setup for its @ mention; record the selected plugin name or ID, never credentials]

Use the selected plugin for read-only searches for application receipts and later employer messages. Check its connection when needed. If the plugin is unavailable, report that email verification is unavailable; preserve the last verified application stage. A resumed workspace keeps its recorded choice unless the applicant explicitly changes it.

## Submission preference

- Submission mode: `stop-and-wait`

Ask during first setup whether the applicant prefers `automatic-submit`; keep `stop-and-wait` when they do not explicitly choose automatic submission. In `stop-and-wait` mode, fill and check the application, then stop before final Apply/Submit so the applicant can click it or instruct Codex to submit that specific application. In `automatic-submit` mode, a completed, checked application may go directly to ApplicationFinalize without another approval. Never infer signing permission from either mode. Keep the saved mode across future runs until the applicant explicitly changes it.

## Opportunity pipeline

For LinkedIn Jobs, use a job-search connector tool when one is available or a signed-in browser. A LinkedIn people-search result is not a job listing. If LinkedIn is signed out, ask the applicant to sign in through the official LinkedIn page or connector flow and continue employer-site searching while access is pending. Record any unsearched source as a coverage gap.

1. Search the user's targets and open the live employer posting. Log source, requisition, date checked, deadline, location, pay, eligibility, and route.
2. Check `APPLICATIONS.csv`, `SEARCH_LOG.md`, and any accessible application history for duplicates. Compare essential requirements against approved CVs and credential evidence. Mark each as met, unclear, or unmet.
3. For a strong, eligible role, create `applications/<ID>/README.md`, a tailored CV and a cover letter, plus any requested extras. Use supported facts from all approved CVs and the chosen CV design reference recorded separately in `CV_INDEX.md`. Preserve originals. Follow the requested output format. Pair every new Word document with a same-stem PDF in the packet, and use the PDF for review and upload unless the employer requires another format. Check text, layout, metadata, and comments.
4. Fill an accessible portal draft using verified answers when the user's request authorizes preparation. Check what persisted. Leave unknown required answers for the user. After each checked draft or material draft update, use ProfileBuilder to add newly verified, reusable answers to `APPLICATION_PROFILE.md`, preserving source and scope. Follow the saved submission mode: `stop-and-wait` means hand off the draft before Apply/Submit; `automatic-submit` means invoke ApplicationFinalize when all checks pass. Never sign without explicit instruction for that application.
5. After authorized submission or user-reported submission, use the selected email plugin to verify a matching receipt when connected, and compare portal confirmation. Record exact status and evidence; follow later changes in the same packet. Do not treat a portal's last-updated timestamp as proof of a new submission without independent evidence.
6. On request, check later portal or recruiter updates, interviews, deadlines, and outcomes. Preserve original submission evidence and record each change with its source and observation time. Do not respond, withdraw, or accept an offer without the user's applicable instruction.

## Tracker

`APPLICATIONS.csv` is the single index, one row per distinct requisition. Use stable IDs and internal stages such as `discovered`, `shortlisted`, `preparing`, `needs-input`, `ready-for-review`, `submitted`, `interview`, `offer`, `rejected`, `withdrawn`, and `closed`. Keep the employer's wording separately in `portal_status`. Never mark `submitted` from a button click without confirmation.

## Document and privacy checks

Do not invent claims or disclose private credential files when unrequested. If a portal uses a plain-text letter field, adapt the letter to readable paragraphs and its character limit. Inspect rendered deliverables and remove stale source-document metadata or unrelated comments. Store application-specific answers and evidence in the packet, not the durable profile.
