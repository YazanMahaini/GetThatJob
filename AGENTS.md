# GetThatJob repository instructions

This repository is a public Codex plugin marketplace. The reusable plugin lives in `plugins/get-that-job/`. Never add an applicant's CV, contact information, credential scans, completed cover letters, application packets, session logs, or authentication data. Workspace scaffolding must stay generic. A generic cover-letter DOCX may provide the default letter design, with placeholders only; no applicant's content or CV visual style belongs in the plugin.

Keep the marketplace entry, plugin manifest, skill links, setup/check scripts, README, and workflow diagram consistent. Setup runs once per applicant workspace and preserves existing files. Validate the plugin and every skill after edits. Use synthetic temporary workspaces for tests, and remove them after checking their resolved path. Do not submit a real job application as a release test.
