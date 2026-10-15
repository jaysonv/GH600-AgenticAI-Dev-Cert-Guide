# Lesson 1: Prepare agent architecture and SDLC processes (15-20%)

**Objectives:** integrate agents into the SDLC; separate planning, reasoning and action; configure observability and control for autonomous agents.

## 1. What an agent is, for this exam

An agent is a model running in a loop with **instructions**, **tools**, **memory/state** and a **goal**. It decides its next step, calls a tool, observes the result and repeats. That loop is why agents need *boundaries*: each iteration can change real state (files, branches, issues).

Chat assistance proposes. A coding agent **acts**: it creates branches, edits files, runs commands and opens pull requests. GitHub is the **control plane and system of record**: issues carry the task, branches isolate the work, PRs carry the review, Actions and rulesets enforce policy, session logs carry the evidence.

## 2. Choosing steps for agents (SDLC integration)

| Good candidates | Poor candidates |
|---|---|
| Well-scoped, verifiable, reversible | Ambiguous requirements |
| Tests for existing code with CI in place | Cross-service architecture redesign |
| Bug fixes with a reproducible failing test | Security-critical changes without review |
| Docs, dependency bumps, mechanical refactors | Irreversible or production-affecting operations |
| Triage, summarising, first-pass review | Decisions needing business judgment |

Rule of thumb: delegate when **success can be checked automatically** and **failure is cheap to undo**.

### Common anti-patterns (and the mitigation)

| Anti-pattern | Mitigation |
|---|---|
| Vague task, no definition of done | Task template with acceptance criteria |
| Mega-task that spans many concerns | Split into small, independently verifiable tasks |
| Agent can write anywhere, merge its own work | Branch scope, required human review, rulesets |
| No observability | Draft PRs, session logs, checklists in the PR |
| Over-broad tool access | Allowlist the minimum, read-only first |
| One agent plans, codes, reviews and deploys | Separate roles and separation of duties |
| No verification loop | Tests, CodeQL and review as part of "done" |
| Instruction bloat or contradiction | Short, specific, path-scoped instructions |
| Trusting agent output | Treat it like a junior contributor's PR |

## 3. Inputs, outputs and success criteria

Define these **before** delegating.

- **Inputs:** goal, scope (files/areas), constraints (don't touch X), context links, environment needs.
- **Outputs:** a **draft PR** with a clear description, tests, and a link to the session log.
- **Success criteria:** objective and checkable, for example "regression test added and passing, existing suite green, no new CodeQL alerts, no files outside `src/billing/` changed".

Weak: *"Fix the invoice bug."* Strong: *"Invoices with a 0% tax rate show NaN. Add a failing test in `tests/test_invoice.py`, fix `invoice.py`, keep public API unchanged, all tests and CodeQL pass."*

## 4. Boundaries between planning, reasoning and action

Separating *thinking* from *doing* is the central design idea of this domain.

- **Planning/reasoning** is read-only: inspect the repo, produce a plan.
- **Action** mutates state: edit, commit, push, call write tools.

How to implement the separation:

1. A **planner** (custom agent or plan mode) with **read/search tools only**. Restricting tools is real enforcement, since a planner that cannot edit cannot "accidentally" implement.
2. The planner outputs a **structured plan**: numbered steps, files touched, tests to add, risks, rollback note. Structure makes it *validatable*.
3. **Validate the plan**: reviewer or reviewer-agent checks that referenced files exist, scope matches the task, and the plan meets criteria.
4. **Gate**: nothing executes until approved (label, comment approval, environment approval, or a human re-assigning the issue).
5. An **executor** agent (write tools) follows the approved plan and opens a draft PR.

GitHub gives you building blocks: plan mode in the IDE, custom agents (for example the *implementation planner* example in the docs' customization library), research/plan/iterate flows for cloud agent, and draft PRs as the natural checkpoint.

## 5. Observability and control for autonomous agents

**Degree of autonomy.** Decide it per task type from the risk of the action (Lesson 6 covers levels in detail). Higher autonomy requires stronger guardrails and better evidence.

**Inspectable artifacts in standard tooling.** Prefer artifacts reviewers already use:

- draft pull request with description and checklist
- commits (co-authored, signed, linking to the session log)
- session logs (what the agent ran and saw)
- issue/PR comments for decisions and hand-offs
- Actions run logs and uploaded artifacts, scan results

**Human intervention without slowing delivery.**

- Review at the **PR boundary**, not every tool call.
- Use **CODEOWNERS / rulesets** to pull humans in only for sensitive paths.
- Let humans **steer asynchronously** (PR comments) instead of blocking synchronously.
- Auto-allow low-risk, read-only operations.

## 6. Preparing the repository and organization

- Repo instructions (`.github/copilot-instructions.md`, path-specific `.instructions.md`, `AGENTS.md`): build/test commands, conventions, do/don't.
- Environment preparation (`copilot-setup-steps.yml`, Lesson 2).
- Org/enterprise preparation for custom agents (shared agents repo, policies, MCP governance).
- Branch protection/rulesets and CODEOWNERS so agent PRs meet the same bar as human PRs.

## Exam traps

- "Approve every action" sounds safe but is an anti-pattern: it ruins velocity without reducing risk.
- A plan that is not validated and gated is only a suggestion.
- Success criteria such as "make it work" are not criteria.
- Observability means artifacts people can inspect in **existing tools**, not a bespoke dashboard.

## Self-check

1. Name three properties of a task that make it a good first candidate for an agent.
2. How would you *technically* stop a planner from changing code?
3. What must a plan be before you can validate it automatically?
4. Which artifacts let an auditor reconstruct what a cloud agent did?

Next: [Lab 1](../labs/lab-01-instructions-and-agent-boundaries/README.md) and [Lab 2](../labs/lab-02-plan-then-execute/README.md).
