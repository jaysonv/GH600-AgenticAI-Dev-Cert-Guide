# Lesson 4: Perform evaluation, error analysis, and tuning (15-20%)

**Objectives:** define success criteria and evaluation signals; analyze failures and find root causes; tune agent behavior from evidence.

## 1. Success criteria and evaluation signals

**Specify expected outcomes and operational constraints.** Outcomes: what must be true (behavior, tests, docs). Constraints: what must *not* happen (files off limits, no new dependencies, performance or security budgets).

**Signals** are measurements that tell you whether the criteria were met.

| Quantitative | Qualitative |
|---|---|
| CI pass/fail, test pass rate | Reviewer judgment of correctness and clarity |
| Coverage change, test count change | Adherence to team conventions |
| Static analysis / lint findings | Quality of PR description and explanation |
| CodeQL alerts, secret scanning hits, vulnerable dependencies | Did it solve the *intent*, not just the letter |
| Diff size vs expected scope | Reviewer trust / willingness to merge |
| Review iterations, time to merge, revert rate | |
| Cost per task (usage consumed) | |

**Align criteria with development intent.** Green checks are necessary, not sufficient. An agent can make a failing test pass by deleting it, or "fix" a bug by catching and hiding the exception. Pair automated signals with criteria such as "test count must not decrease" and with human review of the *why*.

**Automated scanning generates signals.** Cloud agent by default validates its work with **CodeQL**, checks new dependencies against the **GitHub Advisory Database** (malware advisories and High/Critical CVSS), and runs **secret scanning**, and also gets a second opinion from **Copilot code review** (verified; no GHAS license required for this built-in validation). You can add your own linters, test suites, dependency review and code scanning workflows as further signals.

## 2. Analyzing failures and finding root causes

**Evidence sources:** session logs, the plan, traces of tool calls, outputs, workflow artifacts, the PR timeline, CI logs.

**Method:**

1. Reproduce or locate the first point where behavior diverged from expectation.
2. Compare *plan* vs *actions* vs *result*.
3. Classify the root cause.
4. Fix the cause, not the symptom.

### Root-cause classes

| Class | What it looks like | Examples | Typical fix |
|---|---|---|---|
| **Reasoning error** | Wrong plan or interpretation | Misread requirement, scope creep, wrong algorithm, ignored a constraint | Sharper acceptance criteria, plan validation, smaller task, example in the issue |
| **Tool misuse** | Right idea, wrong tool use | Bad arguments, wrong tool chosen, repeated failing call, denied call, MCP server did not start | Fix tool config and allowlist, describe tool usage in instructions, remove unnecessary tools |
| **Context / environment issue** | Agent was set up to fail | Missing dependency, firewall block, stale or missing instruction, contradictory memory, flaky test | Setup steps, allowlist, prune or fix context, stabilize tests |

Quick triage questions:

- Did the agent *understand* the task? (If not: reasoning or missing context.)
- Did it *call the right tools correctly*? (If not: tool misuse.)
- Did the *environment let it succeed*? (If not: context/environment.)

## 3. Tuning agent behavior

Tune **from evidence**, one change at a time, and re-measure.

| Lever | Examples |
|---|---|
| **Instructions** | Make rules specific and testable, remove contradictions, add a verification step ("run tests before finishing"), add a worked example |
| **Workflows** | Add a planning stage, split large tasks, add a review stage, add a required scan |
| **Constraints** | Narrow scope, add "do not touch" paths, require approval for sensitive actions |
| **Memory** | Delete wrong or stale entries, scope instructions with `applyTo`, add durable progress artifacts |
| **Tools** | Add a missing tool, remove an unused or risky one, narrow an allowlist, fix configuration |

**Tuning loop:** define an evaluation set (5-10 representative tasks) > run baseline > classify failures > change **one** lever > re-run the *same* set > compare signals > keep or revert.

Avoid: tuning on a single anecdote, changing five things at once, "fixing" by loosening permissions, or adding more instructions when the real fault is the environment.

## Exam traps

- A failing check is not automatically a model problem. Check environment and tools first.
- "Add more instructions" is often the wrong fix for tool or environment faults.
- Success signals must tie back to intent. Passing CI by weakening tests is a failure.
- When a question lists several fixes, prefer the one that addresses the *classified* root cause with the smallest, most reversible change.

## Self-check

1. Give three quantitative and two qualitative signals.
2. Classify: "agent retried the same invalid `gh` flag five times." Why?
3. Classify: "build fails because the package registry was blocked."
4. Why change only one variable per tuning iteration?

Next: [Lab 7](../labs/lab-07-evaluate-and-tune/README.md).
