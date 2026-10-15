# Practice labs

Nine labs, one or more per domain. Do them on **your own throwaway repository**, never a production one.

## Prerequisites

- A GitHub account with a Copilot plan that includes **Copilot cloud agent** (and, for org-level labs, an org where you are admin). Check your plan and enable the feature in repo/org settings.
- Agent runs consume Copilot usage. Check your plan's billing and usage pages before running many sessions.
- Copy `labs/sandbox-app/` into a new private repo (for example `gh600-sandbox`). It is a tiny Python app with tests and seeded tasks in `ISSUES.md`.
- GitHub UI labels change often. If a menu has moved, follow the linked doc.

> Frontmatter keys and some UI paths in these labs come from my reading of the docs. Where a lab says **verify**, open the linked reference before trusting it, since the exam can test the current behavior.

| Lab | Domain | Skill |
|---|---|---|
| 01 Instructions and agent boundaries | 1 | Task templates, repo and path instructions |
| 02 Plan then execute | 1 | Read-only planner, approval gate, executor |
| 03 Environment setup and firewall | 2 | copilot-setup-steps, allowlist |
| 04 MCP servers | 2 | MCP config, least-privilege tools, secrets |
| 05 Safe execution paths | 2, 6 | Branch/ruleset scope, retries, rollback, escalation |
| 06 Memory and state | 3 | Progress artifacts, Copilot Memory, drift drill |
| 07 Evaluate and tune | 4 | Signals, failure classification, one-variable tuning |
| 08 Multi-agent coordination | 5 | Isolation, conflicts, hand-offs, recovery |
| 09 Guardrails and autonomy | 6 | Autonomy matrix, enforcement, injection test |

Each lab ends with a **Break it** drill. The exam rewards knowing how things fail, so do not skip it.
