# GetThatJob plugin development

This folder is the reusable plugin source. It must never contain a job seeker's CV, contact details, credentials, application packets, or style template. Each user's workspace holds those items.

Keep `get-that-job` as the manifest name and preserve the plugin's skill entry points. Changes to first-use behavior must remain safe for existing workspaces: setup never overwrites user files and runs once per workspace; later checks and profile intake update workspace records.

Validate every skill and the plugin manifest after changes. Test setup and checking in a temporary workspace rather than in a real applicant's project. Do not change a real applicant workspace while developing this generic plugin.
