# Lesson 5: Orchestrate multi-agent coordination (15-20%)

**Objectives:** operate multi-agent workflows; configure observability for them; detect and respond to failures; manage agent lifecycles.

## 1. Operating multi-agent workflows

### Orchestration patterns

| Pattern | Shape | Use when | GitHub-flavored example |
|---|---|---|---|
| **Orchestrator-worker** (hub-and-spoke) | One coordinator splits work, delegates, aggregates | Task decomposes into independent parts | Coordinator opens sub-issues, assigns each to an agent, collects PRs |
| **Sequential pipeline** | A > B > C | Each stage needs the previous output | planner > implementer > tester > reviewer > human merge |
| **Parallel fan-out / fan-in** | Many agents at once, then merge | Independent modules or variants | Several cloud agent sessions on separate issues |
| **Generator-critic** (evaluator-optimizer) | One produces, another critiques, loop | Quality-sensitive output | Implementer agent + code review agent |
| **Event-driven** | Agents react to GitHub events | Triage, routing | Label or issue-opened triggers an agent |

Pick the simplest pattern that fits. More agents means more coordination cost.

### Isolation for parallel execution

Parallel agents must not trample each other.

- **Separate branches** (each cloud agent session gets its own `copilot/` branch), **separate working copies/worktrees**, separate environments.
- **Disjoint ownership:** assign file/module ownership per agent up front.
- Do not share uncommitted state. Share through commits, PRs and artifacts.
- Copilot CLI has parallel task execution (*fleet*) and the SDK has fleet mode; the principle is the same.

### Conflicts and how to handle them

| Conflict | Detect | Resolve |
|---|---|---|
| **Overlapping code changes** | Merge conflicts, overlapping file lists in PRs, ownership map | Serialize, rebase, re-partition ownership, or have an integrator agent/human merge |
| **Duplicated effort** | Two PRs for one need | Claim work before starting (assignment, label, sub-issue), check for existing claims |
| **Contradictory outputs** | Different designs or behaviors from different agents | Escalate to an arbiter (human or designated reviewer agent), record the decision in one place |

## 2. Observability for multi-agent behavior

- **Artifacts suitable for review and audit:** one PR per agent task, linked issues, session logs, scan results.
- **Document key decisions, hand-offs and outcomes:** a hand-off record says *who* passed *what* (inputs, outputs, assumptions) to *whom*, and what was decided and why. A single coordination issue or `DECISIONS.md` works well.
- **Post-hoc analysis:** reconstruct a timeline from session logs, commit co-author trails and audit log events, then look for stalls, rework loops and contradictions.

## 3. Failures and degraded behavior

| Situation | Signals | Response |
|---|---|---|
| **Failed** | Error, no PR | Classify (Lesson 4), bounded retry if transient, else escalate |
| **Partial** | Some subtasks done | Resume from checkpoint idempotently or roll back; do not restart blindly |
| **Stalled** | No progress past a timeout, waiting forever | Timeout/heartbeat detection, cancel, roll back partial work, re-queue or escalate |
| **Degraded** | Rising failure rate, low-quality output, contradictions | Pause routing (circuit breaker), fall back to human or alternative agent, investigate |

**Recovery patterns:** retry with limits, **rollback** (revert or close the branch), **human-in-the-loop** escalation, **circuit breaker**, fallback agent, idempotent operations so replays are safe.

## 4. Lifecycle of agents in multi-agent workflows

| Action | Safe practice |
|---|---|
| **Add** an agent | Define its role, tools, inputs/outputs (hand-off contract). Review its definition by PR. Pilot on low-risk tasks |
| **Update / reconfigure / replace** | Version the agent definition in the repo. Roll out gradually. Let in-flight tasks finish (drain) or hand them off cleanly. Keep hand-off contracts backward compatible |
| **Retire** | Stop routing new work. Finish or reassign in-flight work. **Preserve** logs, PRs and decision records for audit. Document why and who replaced it |

Because custom agents are files in a repo, changes to them get normal PR review, history and rollback. That is the governance story.

## Exam traps

- Parallel agents on the same files, with no ownership plan, will conflict.
- "Restart everything" is rarely the best recovery. Prefer checkpoint resume or targeted rollback.
- Deleting a retired agent's history hurts auditability.
- More agents is not better. Orchestration cost is real.

## Self-check

1. Which pattern fits "coordinator splits a feature into three independent modules"?
2. How do you prevent duplicated effort?
3. What evidence would you use for post-hoc analysis?
4. How do you retire an agent without losing auditability?

Next: [Lab 8](../labs/lab-08-multi-agent/README.md).
