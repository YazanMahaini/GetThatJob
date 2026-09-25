---
name: profile-builder
description: After a checked job-application draft, save newly verified reusable form answers in the applicant's private APPLICATION_PROFILE.md so later applications do not ask for them again.
---

# ProfileBuilder

Invoke after **each filled and checked application draft**, including a material update to a saved draft. If setup has not run in this workspace, use [SetupSkill](../setup-skill/SKILL.md) first. Read the approved CV index, `MEMORY.md`, `APPLICATION_PROFILE.md`, the just-filled application packet, and the verified portal answers. The applicant's active instruction takes precedence if they do not want a particular fact retained.

Identify answers that will help with future forms and are not already clear in the approved CV: for example date or place of birth, nationality, residence, contact preferences, language proficiency, availability, or a user-confirmed form convention. Record each fact's exact value, original source, confirmation date, and reuse scope in `APPLICATION_PROFILE.md`. A value entered into a portal is not proof by itself; trace it to a direct user statement, official document, or other approved source. Note in the packet which facts were promoted to the reusable profile.

Use the general-facts table only for stable applicant facts. Put work-authorization answers, application-specific eligibility, salary expectations, referee-contact permission, disclosures, consents, and portal date conventions in the scoped table with the exact question or context and a recheck rule. Never reuse a country-specific or employer-specific answer as a universal answer. Do not save passwords, one-time codes, payment details, or irrelevant private document contents. Preserve corrections and flag conflicts; do not silently replace an older fact with a stronger claim.

Before asking a question in the next application, read `APPLICATION_PROFILE.md` and reuse a still-valid answer whose scope covers the new field. Ask again only if the value is missing, conflicting, stale, requires a new commitment, or the new question changes its meaning. Keep this file inside the applicant workspace and never upload it as an application attachment.
