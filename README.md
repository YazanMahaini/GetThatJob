# GetThatJob

<p align="center">
  <img src="plugins/get-that-job/assets/brand/get-that-job-logo.png" alt="GetThatJob logo: blue GTJ flowchart mark on a dark square" width="160">
</p>

GetThatJob is a Codex plugin for setting up a private job-search workspace, checking applicant documents, finding and assessing roles, preparing applications, building a reusable application profile, and recording verified outcomes. It carries the **workflow**, not an applicant's personal information or document design.

## How GetThatJob works

Read the top row from left to right, then the bottom row from right to left.

```mermaid
%%{init: {"flowchart": {"rankSpacing": 10, "nodeSpacing": 20}}}%%
flowchart TB
    subgraph first[" "]
        direction LR
        A("01 SET UP<br/>Create files<br/>Check sources<br/>Keep existing") --> B("02 SOURCES<br/>Add CVs<br/>Add records<br/>Verify facts") --> C("03 FIND JOBS<br/>Find roles<br/>Check fit<br/>Check criteria") --> D("04 PREPARE<br/>Tailor CV<br/>Fill draft<br/>Save answers")
    end
    subgraph second[" "]
        direction RL
        E("05 REVIEW<br/>Review draft<br/>Request edits<br/>Choose action") --> F("06 CONFIRM<br/>Check email<br/>Check portal<br/>Verify receipt") --> G("07 TRACK<br/>Track outcome<br/>Save evidence<br/>Follow up") --> H("08 REUSE<br/>Use profile<br/>Recheck facts<br/>Find next role")
    end
    first ~~~ second
    classDef step fill:#00182f,stroke:#355675,color:#5c9fde,stroke-width:2px,font-size:16px;
    class A,B,C,D,E,F,G,H step;
    style first fill:transparent,stroke:transparent
    style second fill:transparent,stroke:transparent
    linkStyle 0,1,2,3,4,5 stroke:#6f95b5,stroke-width:2px;
```

The [detailed interactive workflow](WORKFLOW.md) shows the main decisions and stages, with notes on alternate routes and repeat steps. It also offers full-resolution [horizontal](docs/workflow-detailed-horizontal.png) and [vertical](docs/workflow-detailed-vertical.png) PNGs.

## Install in Codex

From this public repository, copy its GitHub URL and run:

```text
codex plugin marketplace add <repository-url>
codex plugin add get-that-job@get-that-job
```

Start a new Codex task after installation so the skills are available. Ask: “Use GetThatJob to set up my job-search workspace.” The first use in each workspace creates folders and blank records without overwriting existing files. Later uses check the setup marker and continue from the saved state.

The setup helper uses Python 3 when available. The skills also describe a file-tool fallback for systems without Python.

### Use an existing workspace

Point GetThatJob to the existing job-search folder. It previews additions with `setup_workspace.py --workspace <path> --dry-run`, then creates only missing scaffold files and a per-workspace setup marker. Existing files are opened in create-only mode and never replaced, truncated, or removed; an existing but malformed tracker or Markdown file is reported for review rather than reset. Subsequent runs see the marker and make no setup changes. Normal job-search work can still update the applicant's tracker and notes as new verified information arrives.

## Add your own sources

Place at least one current, approved CV in `CVs/`. Add official credentials to `Qualifications&Certificates/` as relevant, and optionally put an approved letter example in `CoverLetters/Template/`. ProfileIntake records the applicant's facts, preferred roles, eligibility and source documents in that workspace. After each checked application draft, ProfileBuilder merges newly verified reusable form answers into the private `APPLICATION_PROFILE.md`, preserving earlier entries and their source and reuse scope. It can also capture verified answers from an application filled outside JobFinder when that application is reviewed. Later forms check the accumulated profile before asking the applicant again. The applicant's CV controls tailored CV styling; this repository contains no CV or cover-letter style template.

## Application flow

JobFinder searches LinkedIn Jobs and employer sites, verifies the live posting, checks duplicates and essential requirements, creates a tailored CV and cover letter, and fills a checked draft when accessible. ProfileBuilder then captures newly verified reusable answers. JobFinder stops for applicant review before final submission. ApplicationFinalize handles a separately authorized submission; application signing always requires explicit authorization for that specific application. EmailConfirmationChecker verifies a matching receipt, and ApplicationFollowUp records later stages when asked.

LinkedIn access is checked at use time. If the available LinkedIn app has no job-search tool, the skill uses a signed-in LinkedIn browser session. If signed out, it asks the applicant to sign in through LinkedIn's official flow and continues employer-site research while waiting. Email checking similarly uses the applicant's connected mailbox; it never sends or changes messages.

Every applicant has different qualifications, preferences, accounts and live opportunities. The plugin provides the same workflow and safeguards; job matches and application outcomes depend on those inputs and external sites.

## Privacy

Only generic templates, skills and helper scripts are distributed. Keep real CVs, credentials, the populated `APPLICATION_PROFILE.md`, application packets and access details in a separate applicant workspace. The repository's `.gitignore` blocks common accidental additions at the repository root. Review every commit before publishing.

## Development checks

Validate `plugins/get-that-job/` with Codex's plugin validator and each `skills/*/SKILL.md` with the skill validator. Test setup and checking in a synthetic temporary workspace. Review the source for private information and run `git status` before pushing. No real application needs to be submitted to test this repository.
