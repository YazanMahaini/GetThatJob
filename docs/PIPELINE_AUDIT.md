# Pipeline audit

This checklist maps the reusable plugin to the reference job-search workflow. Applicant-specific facts, location order, document design, portal notes, and application history remain in each applicant workspace.

| Stage | Release behavior |
| --- | --- |
| First use | Create the four source/application folders, an optional letter-reference folder, the profile and evidence indexes, operations notes, search log, tracker, packet guide, and a per-workspace setup marker. Ask for the email plugin and submission mode; save `stop-and-wait` by default and preserve existing files and choices. |
| Document intake | Require one approved readable CV; index supplied CVs and credentials; identify unsupported claims and missing preferences. Use the applicant's source style. |
| Job sources | Check available LinkedIn app tools; use a job-search tool if exposed, otherwise use signed-in LinkedIn Jobs in a browser. Prompt for official sign-in when needed. Search employer and suitable job sites while access is pending. |
| Screening | Verify the live employer post, deadline and time zone, pay conditions, location, nationality, work authorization, essential criteria, requested files, and route. Reject stale, fee-charging, duplicate, unverifiable, and mandatory-ineligible roles. |
| Duplicate control | Check the 24-column application tracker, search log, and accessible portal history by employer and requisition before tailoring. Do not infer submission from a portal's updated timestamp. |
| Application materials | Prepare both tailored CV and cover letter for each strong eligible role, plus required extras. Keep originals unchanged. Pair new Word files with same-stem PDFs; inspect layout, text, properties, and comments. Use applicant-provided styling only. |
| Portal draft | Fill all supported fields from verified sources, save, reopen or inspect persistence, and record questions and blockers. A search request authorizes reversible draft preparation. |
| Reusable profile | After each checked draft, promote newly verified non-CV form answers to the private `APPLICATION_PROFILE.md` with source, confirmation date, and reuse scope. Read it before the next form and recheck context-specific answers. |
| Review and submission | In `stop-and-wait` mode, hand off the checked draft for the applicant to click Apply or direct a specific submission. In `automatic-submit` mode, use the saved standing authorization for a complete checked application without case-by-case approval. A signature or equivalent declaration requires separate authorization for that specific application in either mode. |
| Confirmation | On first setup, ask once for the applicant's email plugin `@` mention and save that plugin selection privately. A short manual-submission report such as "I applied, check email" invokes EmailConfirmationChecker; disambiguate only when several applications could match. Use the selected plugin for a narrow, read-only receipt search; capture sender, subject, timestamp, link, and evidence. Update the packet and tracker only when the evidence supports the stage. |
| Later status | On request, check recruiter and portal updates, record interviews or deadlines, and preserve original submission evidence. |

## Release checks

- Validate the Codex plugin manifest and all skill entry points.
- Test first setup, repeat setup without overwrite, preservation of saved email and submission choices during repair, empty input, valid source files, invalid document detection, and compatibility with the reference tracker schema in a synthetic workspace.
- Verify marketplace discovery and installation from the repository layout.
- Review tracked files for applicant identifiers, contact details, application files, and accidental runtime caches before publication.

These checks verify packaging and prescribed behavior. External job sites, sign-in state, individual portal controls, document rendering, and confirmation emails vary by user and time; a real application cannot be used as a release test without that applicant's instruction.
