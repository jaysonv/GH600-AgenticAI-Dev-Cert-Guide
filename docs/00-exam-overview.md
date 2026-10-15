# GH-600 exam overview

**Certification:** GitHub Certified: Agentic AI Developer  **Exam:** GH-600, *Developing in Agentic AI Systems*

The exam is delivered through Microsoft and Pearson VUE, but GitHub owns the certification and its syllabus.

## Verified facts (Microsoft Learn, checked 15 Oct 2026)

| Item | Value |
|---|---|
| Duration | 120 minutes |
| Passing score | 700 or greater (scaled, not a simple percentage) |
| Language | English |
| Proctoring | Proctored; may include interactive components |
| Prerequisites | None formal. SDLC, GitHub workflows/controls, code quality, security and review practices, plus hands-on use of Copilot, MCP servers and agent customization are expected |
| Validity | 2 years (GitHub is moving to Microsoft's recertification process) |
| Retake | 24 hours after the first attempt; longer waits after that (see Microsoft's retake policy) |
| Preview features | Most questions cover GA features, but commonly used Preview features may appear |
| Sandbox | https://ghcertdemo.starttest.com/ (try every question type before exam day) |

Third-party sites quote about 60 questions and a $99 USD fee. Microsoft publishes neither on the pages I checked, so treat them as unconfirmed and look at the price shown when you schedule.

## Domains and weights

| # | Domain | Weight |
|---|---|---|
| 1 | Prepare agent architecture and SDLC processes | 15-20% |
| 2 | Implement tool use and environment interaction | 20-25% |
| 3 | Manage memory, state, and execution | 10-15% |
| 4 | Perform evaluation, error analysis, and tuning | 15-20% |
| 5 | Orchestrate multi-agent coordination | 15-20% |
| 6 | Implement guardrails and accountability | 10-15% |

Domain 2 is the largest. Domains 4 and 5 together carry roughly a third of the exam, so do not skimp on them.

## What the exam is really testing

Scenario judgment, not definitions. Expect "a team has problem X, which configuration or process change is best?" Good answers are almost always:

- **least privilege** (narrowest tool list, read-only first, scoped tokens)
- **plan before act** for risky work, with a gate between them
- **inspectable artifacts** (draft PRs, session logs, commits, checklists)
- **risk-proportional humans in the loop**: not zero, not on every step
- **change one thing, re-measure** when tuning
- **technical enforcement** over "please behave" instructions

## Terminology note

GitHub's docs now say **Copilot cloud agent**. Older docs, blog posts and some exam prep sites say **Copilot coding agent**. They are the same feature. Treat both names as equivalent on exam day.

## Exam-day strategy

- About 2 minutes per question on average. Flag and move on after 90 seconds.
- Read the last sentence first (what is being asked), then the scenario.
- Eliminate answers that grant broad access, skip human review for irreversible actions, or add approvals that reduce no risk.
- For interactive/ordering items, rehearse them in the official sandbox.
- Register with a personal Microsoft account, not a work or school one, so your records survive a job change.
