# GetThatJob

<p align="center">
  <img src="plugins/get-that-job/assets/brand/get-that-job-logo-compact.svg" alt="Get That Job! inside a blue flowchart box on a dark square" width="160">
</p>

GetThatJob is a Codex plugin for setting up a private job-search workspace, checking applicant documents, finding and assessing roles, preparing applications, building a reusable application profile, and recording verified outcomes. It carries the **workflow** and a generic cover-letter design, never an applicant's personal information or CV design.

## How GetThatJob works

Read the four numbered panels from left to right. Each box has the same size; the paths inside the panels show the key decisions.

```mermaid
flowchart LR
    subgraph setup["01  SET UP"]
        direction TB
        A("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>Ask GetThatJob for help</div>") --> B("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>First use here?</div>")
        B --> C("<div style='width:210px;height:66px;display:flex;align-items:center;justify-content:center;text-align:center'>Yes: create folders, then pause for your documents</div>")
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

## Install in ChatGPT Work or Codex

**Required for a new setup:** Create a new, clean, empty folder for your job-search project. Make that folder the project's working directory, then open the project and start your GetThatJob chat **inside that project**. GetThatJob will create its folders and records there. Do not start the setup from the plugin repository, a general chat, or another project's directory. If you are returning to an existing GetThatJob workspace, reopen that project instead; see [Resume an existing workspace](#resume-an-existing-workspace).

### ChatGPT Work (recommended)

This is the recommended setup used to test GetThatJob:

1. Create a new, empty folder for the job-search project.
2. Create a new ChatGPT Work project using that folder as its project directory. Open the new project and confirm you are chatting **inside it**.
3. In that project's chat, send this prompt. ChatGPT Work handles the installation and guides you through any access step your account requires.

> Install the following plugin: [https://github.com/YazanMahaini/GetThatJob](https://github.com/YazanMahaini/GetThatJob)

### Codex

Create a new, empty folder for the job-search project and open that folder as the active Codex project directory. Confirm the new project is selected before installing the plugin from this repository:

```text
codex plugin marketplace add https://github.com/YazanMahaini/GetThatJob
codex plugin add get-that-job@get-that-job
```

Start a new Codex task **inside that same project** after installation so the skills are available and GetThatJob creates its workspace files in the empty folder you chose. Type `@GetThatJob` and select the installed plugin from Codex's suggestions. Codex may display the selected mention as `[@GetThatJob](plugin://get-that-job@get-that-job)`.

The setup helper uses Python 3 when available. The skills also describe a file-tool fallback for systems without Python.

## Start with one prompt

In your applicant workspace, select the `@GetThatJob` plugin mention and send:

```text
Use @GetThatJob and find me jobs.
```

That request starts or resumes the pipeline. GetThatJob handles these tasks in sequence:

1. **Set up and check the workspace.** On first use in that workspace, it asks once for your email plugin and submission preference, then creates only missing folders and blank records. It **pauses so you can add your CVs and other documents**. When you say to continue, it checks the available sources and identifies missing search priorities. If your CVs have different designs, it asks which of your own CVs should set the style. Existing workspaces keep their files and resume without a new first-use pause.
2. **Find and assess jobs.** It searches LinkedIn Jobs and employer sites, checks live requirements, eligibility, and duplicates, and records why a role fits or fails. If LinkedIn needs sign-in, it asks you to use LinkedIn's official flow while it continues employer-site research.
3. **Prepare strong applications.** For a strong eligible role, it uses verified information from your approved CVs and follows your chosen CV design, creates a tailored CV, cover letter, and application packet, and fills and checks a portal draft when accessible. The letter uses the bundled generic design unless you choose your own approved letter as its reference.
4. **Build your reusable profile.** After each filled and checked draft, ProfileBuilder saves newly verified reusable answers in your private `APPLICATION_PROFILE.md`. Later applications check that file before asking you the same question again.
5. **Follow your saved submission choice.** By default, Codex gives you the checked draft and stops so you can click Apply yourself or tell it to submit that application. If you chose automatic submission, it rechecks and submits a complete application without asking again, unless a required fact, signature, or other blocker needs you.

### Resume an existing workspace

The empty-folder requirement is for a **new** setup. To continue a job search already managed by GetThatJob, reopen its existing project and start the task inside that project. GetThatJob uses the existing job-search folder. It previews any needed additions with `setup_workspace.py --workspace <path> --dry-run`, then creates only missing scaffold files and a per-workspace setup marker. Existing files are opened in create-only mode and never replaced, truncated, or removed; an existing but malformed tracker or Markdown file is reported for review rather than reset. Subsequent runs see the marker and make no setup changes. Normal job-search work can still update the applicant's tracker and notes as new verified information arrives.

## Add your own sources

On first setup, GetThatJob creates the folders and **waits** while you add your files. Put at least one current, approved CV in `CVs/` and relevant official credentials in `Qualifications&Certificates/`. A generic cover-letter design is already in `CoverLetters/Template/`. If you prefer the look of your own letter, add an approved reference there and tell GetThatJob to use it. Then reply in the same chat: `I've added my documents. Continue.` You can also explicitly ask it to continue without adding files; it will report what is missing. This handoff is remembered if you leave and return later.

ProfileIntake records the applicant's facts, preferred roles, eligibility and source documents in that workspace. After each checked application draft, ProfileBuilder merges newly verified reusable form answers into the private `APPLICATION_PROFILE.md`, preserving earlier entries and their source and reuse scope. It can also capture verified answers from an application filled outside JobFinder when that application is reviewed. Later forms check the accumulated profile before asking the applicant again. A CV from this applicant controls tailored CV styling; the bundled letter design contains only placeholders.

## When Codex needs you

You can start with one request and let GetThatJob do the work. It will pause and tell you exactly what it needs when only you can provide it. That might be a CV, proof of a qualification, your preferred kinds of jobs, an answer missing from your documents, a website sign-in, or your review of a completed application. Reply in the same conversation; it will pick up where it stopped and keep doing any other available work meanwhile.

On first setup, it asks which email plugin you use. Select its `@` mention, such as `@Outlook Email` or `@Gmail`. GetThatJob remembers your choice for this private workspace, so you do not have to repeat it later. If the plugin is not connected yet, the job search can continue; email confirmation checks will wait until it is connected.

It also asks whether to **stop after filling and checking each application** or **submit complete applications automatically**. The default is to stop and let you click Apply yourself. You can instead tell Codex to submit a particular checked application. GetThatJob remembers this choice until you tell it to change it. Even with automatic submission, it will ask you before signing anything, paying a fee, or answering a question it cannot verify.

If you add several CVs with different designs, GetThatJob asks you to pick one of **your CVs** as the design to follow. This controls how tailored CVs look. It still reads all your approved CVs for information, so choosing a design does not discard experience or skills recorded in another version. If you have one CV, or your CVs share the same design, no choice is needed.

After reviewing a checked draft in the default mode, tell Codex any revisions you want. If you want it to submit that application, say: `Use @GetThatJob to submit my reviewed application for [employer and role].` It rechecks the application before submission. An e-signature or signing declaration requires a separate, explicit instruction for that specific application.

If you click Apply yourself, continue in the same GetThatJob task with either prompt:

```text
I applied, check email.
```

```text
Submitted. Check email and confirm.
```

GetThatJob routes these to EmailConfirmationChecker. It identifies the application from your recent tracker and packet when there is one clear match; if several are plausible, it asks which employer and role you mean. It uses your selected email plugin to look for a matching receipt and records only what the evidence confirms. You can ask for a later status check when you want one.

## Tips

- Put a comprehensive **master CV** containing all your experience in `CVs/`, or add **all your approved CV versions** there. GetThatJob reads every version for supported information. If the CVs have different **design styles**, it asks you which of **your CVs** should set the look of tailored CVs rather than guessing. If factual details conflict, it flags those separately for you to resolve.
- **Recommended model:** GetThatJob works best with **GPT-6 Sol** at **Extra High** reasoning (`xhigh`). Select these settings in Codex for results closest to the workflow documented here.

## Application flow

JobFinder searches LinkedIn Jobs and employer sites, verifies the live posting, checks duplicates and essential requirements, creates a tailored CV and cover letter, and fills a checked draft when accessible. ProfileBuilder then captures newly verified reusable answers. The saved submission mode determines whether JobFinder stops for the applicant or passes a complete checked draft to ApplicationFinalize for automatic submission. Application signing always requires explicit authorization for that specific application. EmailConfirmationChecker verifies a matching receipt, and ApplicationFollowUp records later stages when asked.

LinkedIn access is checked at use time. If the available LinkedIn app has no job-search tool, the skill uses a signed-in LinkedIn browser session. If signed out, it asks the applicant to sign in through LinkedIn's official flow and continues employer-site research while waiting. Email checking uses the plugin selected for that workspace; it only reads matching messages and never sends or changes them.

Every applicant has different qualifications, preferences, accounts and live opportunities. The plugin provides the same workflow and safeguards; job matches and application outcomes depend on those inputs and external sites.

## Privacy

Only generic templates, including the optional default cover-letter design, skills and helper scripts are distributed. Keep real CVs, credentials, the populated `APPLICATION_PROFILE.md`, application packets and access details in a separate applicant workspace. The repository's `.gitignore` blocks common accidental additions at the repository root. Review every commit before publishing.

## Development checks

Validate `plugins/get-that-job/` with Codex's plugin validator and each `skills/*/SKILL.md` with the skill validator. Test setup and checking in a synthetic temporary workspace. Review the source for private information and run `git status` before pushing. No real application needs to be submitted to test this repository.
