# GetThatJob repository instructions

This repository is a public Codex plugin marketplace. The reusable plugin lives in `plugins/get-that-job/`. Never add an applicant's CV, contact information, credential scans, cover letters, application packets, session logs, or authentication data. The files in `plugins/get-that-job/assets/workspace/` must remain blank, generic templates without a visual CV or letter style.

Keep the marketplace entry, plugin manifest, skill links, setup/check scripts, README, and workflow diagram consistent. Setup runs once per applicant workspace and preserves existing files. Validate the plugin and every skill after edits. Use synthetic temporary workspaces for tests, and remove them after checking their resolved path. Do not submit a real job application as a release test.
