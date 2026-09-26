# GetThatJob

<p align="center">
  <img src="plugins/get-that-job/assets/brand/get-that-job-logo.png" alt="GetThatJob logo: blue GTJ flowchart mark on a dark square" width="160">
</p>

GetThatJob is a Codex plugin for setting up a private job-search workspace, checking applicant documents, finding and assessing roles, preparing applications, building a reusable application profile, and recording verified outcomes. It carries the **workflow**, not an applicant's personal information or document design.

## How GetThatJob works

Read the four numbered panels from left to right. Each box has the same size; the paths inside the panels show the key decisions.

```mermaid
flowchart LR
    subgraph setup["01  SET UP"]
        direction TB
        A("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>Ask GetThatJob for help</div>") --> B("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>First use here?</div>")
        B --> C("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>Yes: SetupSkill adds missing files and saves choices</div>")
        B --> D("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>SetupChecker checks sources</div>")
        C --> D
    end
    subgraph search["02  SOURCES & SEARCH"]
        direction TB
        E("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>CV and priorities ready?</div>")
        E --> F("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>No: add documents or answer questions</div>")
        F --> G("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>ProfileIntake verifies facts and CV style</div>")
        E --> H("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>JobFinder checks roles and eligibility</div>")
        G --> H
    end
    subgraph prepare["03  PREPARE & CHECK"]
        direction TB
        I("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>Tailor CV, letter and packet</div>") --> J("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>Fill and check portal draft</div>")
        J --> P("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>ProfileBuilder saves verified answers</div>")
        P --> K("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>Follow your saved submission choice</div>")
    end
    subgraph outcome["04  SUBMIT & TRACK"]
        direction TB
        L("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>You click Apply or Codex submits when authorized</div>") --> M("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>EmailConfirmationChecker checks receipt</div>")
        M --> N("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>Tracker and packet record outcome</div>")
        N --> O("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>ApplicationFollowUp checks later status</div>")
    end
    setup --> search --> prepare --> outcome
    classDef step fill:#00182f,stroke:#355675,color:#d9e8f6,stroke-width:2px;
    classDef decision fill:#111111,stroke:#5c9fde,color:#5c9fde,stroke-width:2px,stroke-dasharray:5 4;
    class A,C,D,F,G,H,I,J,P,K,L,M,N,O step;
    class B,E decision;
    style setup fill:transparent,stroke:#355675,color:#5c9fde
    style search fill:transparent,stroke:#355675,color:#5c9fde
    style prepare fill:transparent,stroke:#355675,color:#5c9fde
    style outcome fill:transparent,stroke:#355675,color:#5c9fde
    linkStyle 0,1,2,3,4,5,6,7,8,9,10,11,12,13 stroke:#6f95b5,stroke-width:2px;
    linkStyle 14,15,16 stroke:transparent,fill:transparent;
```

## Install in Codex

Install the plugin from this repository:

```text
codex plugin marketplace add https://github.com/YazanMahaini/GetThatJob
codex plugin add get-that-job@get-that-job
```

Start a new Codex task after installation so the skills are available. Open the task in your job-search workspace, or give its full folder path in your prompt. Type `@GetThatJob` and select the installed plugin from Codex's suggestions. Codex may display the selected mention as `[@GetThatJob](plugin://get-that-job@get-that-job)`.

**Recommended model:** GetThatJob works best with **GPT-6 Sol** at **Extra High** reasoning (`xhigh`). Select these settings in Codex for results closest to the workflow documented here.

The setup helper uses Python 3 when available. The skills also describe a file-tool fallback for systems without Python.

### Use an existing workspace

Point GetThatJob to the existing job-search folder. It previews additions with `setup_workspace.py --workspace <path> --dry-run`, then creates only missing scaffold files and a per-workspace setup marker. Existing files are opened in create-only mode and never replaced, truncated, or removed; an existing but malformed tracker or Markdown file is reported for review rather than reset. Subsequent runs see the marker and make no setup changes. Normal job-search work can still update the applicant's tracker and notes as new verified information arrives.

## Start with one prompt

In your applicant workspace, select the `@GetThatJob` plugin mention and send:

```text
Use @GetThatJob and find me jobs.
```

That request starts or resumes the pipeline. GetThatJob handles these tasks in sequence:

1. **Set up and check the workspace.** On first use in that workspace, it creates only missing folders and blank records. It preserves existing files, checks available CVs and credentials, asks once for your email plugin and submission preference, and identifies any missing search priorities.
2. **Find and assess jobs.** It searches LinkedIn Jobs and employer sites, checks live requirements, eligibility, and duplicates, and records why a role fits or fails. If LinkedIn needs sign-in, it asks you to use LinkedIn's official flow while it continues employer-site research.
3. **Prepare strong applications.** For a strong eligible role, it follows your approved CV's style, creates a tailored CV, cover letter, and application packet, and fills and checks a portal draft when accessible.
4. **Build your reusable profile.** After each filled and checked draft, ProfileBuilder saves newly verified reusable answers in your private `APPLICATION_PROFILE.md`. Later applications check that file before asking you the same question again.
5. **Follow your saved submission choice.** By default, Codex gives you the checked draft and stops so you can click Apply yourself or tell it to submit that application. If you chose automatic submission, it rechecks and submits a complete application without asking again, unless a required fact, signature, or other blocker needs you.

### When Codex needs you

Codex may ask you to add an approved CV or relevant credential, confirm a search preference or unsupported application answer, sign in to a site, or review a completed draft. It should name the exact missing item and continue independent work where possible. You can reply in the same task; you do not need to restart the pipeline.

At first setup, GetThatJob asks: **“Which email plugin should I use to check application confirmations? Please select it with `@`, such as `@Outlook Email` or `@Gmail`.”** It saves that plugin selection in your private `OPERATIONS.md` and reuses it when you resume; it does not ask again. If the selected plugin is not installed or connected, job search and draft preparation can continue, but Codex will report that it cannot verify an email receipt until access is available. It does not switch to another mailbox without your direction.

It also asks whether to **stop after filling and checking each application** or **submit complete applications automatically without asking each time**. The default is to stop and let you click Apply. In that mode, you can instead tell Codex to submit a specific checked application. Your choice is saved privately and applies to future applications until you explicitly change it. Automatic submission never includes signing an application, paying a fee, or guessing a required answer; those still stop for your input.

After reviewing a checked draft in the default mode, tell Codex any revisions you want. If you want it to submit that application, say: `Use @GetThatJob to submit my reviewed application for [employer and role].` It rechecks the application before submission. An e-signature or signing declaration requires a separate, explicit instruction for that specific application.

If you click Apply yourself, continue in the same GetThatJob task with either prompt:

```text
I applied, check email.
Submitted. Check email and confirm.
```

GetThatJob routes these to EmailConfirmationChecker. It identifies the application from your recent tracker and packet when there is one clear match; if several are plausible, it asks which employer and role you mean. It uses your selected email plugin to look for a matching receipt and records only what the evidence confirms. You can ask for a later status check when you want one.

## Add your own sources

Place at least one current, approved CV in `CVs/`. Add official credentials to `Qualifications&Certificates/` as relevant, and optionally put an approved letter example in `CoverLetters/Template/`. ProfileIntake records the applicant's facts, preferred roles, eligibility and source documents in that workspace. After each checked application draft, ProfileBuilder merges newly verified reusable form answers into the private `APPLICATION_PROFILE.md`, preserving earlier entries and their source and reuse scope. It can also capture verified answers from an application filled outside JobFinder when that application is reviewed. Later forms check the accumulated profile before asking the applicant again. The applicant's CV controls tailored CV styling; this repository contains no CV or cover-letter style template.

## Application flow

JobFinder searches LinkedIn Jobs and employer sites, verifies the live posting, checks duplicates and essential requirements, creates a tailored CV and cover letter, and fills a checked draft when accessible. ProfileBuilder then captures newly verified reusable answers. The saved submission mode determines whether JobFinder stops for the applicant or passes a complete checked draft to ApplicationFinalize for automatic submission. Application signing always requires explicit authorization for that specific application. EmailConfirmationChecker verifies a matching receipt, and ApplicationFollowUp records later stages when asked.

LinkedIn access is checked at use time. If the available LinkedIn app has no job-search tool, the skill uses a signed-in LinkedIn browser session. If signed out, it asks the applicant to sign in through LinkedIn's official flow and continues employer-site research while waiting. Email checking uses the plugin selected for that workspace; it only reads matching messages and never sends or changes them.

Every applicant has different qualifications, preferences, accounts and live opportunities. The plugin provides the same workflow and safeguards; job matches and application outcomes depend on those inputs and external sites.

## Privacy

Only generic templates, skills and helper scripts are distributed. Keep real CVs, credentials, the populated `APPLICATION_PROFILE.md`, application packets and access details in a separate applicant workspace. The repository's `.gitignore` blocks common accidental additions at the repository root. Review every commit before publishing.

## Development checks

Validate `plugins/get-that-job/` with Codex's plugin validator and each `skills/*/SKILL.md` with the skill validator. Test setup and checking in a synthetic temporary workspace. Review the source for private information and run `git status` before pushing. No real application needs to be submitted to test this repository.
