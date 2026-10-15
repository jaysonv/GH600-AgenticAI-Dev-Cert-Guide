# Lab 2: Plan, validate, gate, execute (Domain 1)

**Goal:** build a two-stage workflow where a read-only planner must be approved before an executor can act.

## Steps

1. Add `assets/planner.agent.md` and `assets/executor.agent.md` to `.github/agents/` in your sandbox repo. **Verify** the frontmatter keys and tool aliases in the *Custom agents configuration* reference, then adjust.
2. Create issue #5 (`clamp_discount`). Run the **planner** agent on it (cloud agent session or IDE chat). It should post a structured plan and make **no** file changes.
3. Validate the plan using `assets/plan-checklist.md` (files exist, scope respected, tests listed, rollback noted).
4. Approve by commenting `APPROVED PLAN` on the issue (or adding an `approved-plan` label).
5. Run the **executor** agent with the approved plan pasted or linked. Review the draft PR against the plan.

## Verify

- [ ] Planner produced no commits
- [ ] Plan was structured and checkable
- [ ] Executor diff matches the plan (deviations are explained)
- [ ] You can state what technically prevented the planner from editing

## Break it

Give the planner a write tool and ask for a plan again. Does it start editing? Remove the tool again. This is why "tools" beats "instructions" as an enforcement mechanism.

## Exam link

Plan vs execution, structured plan, plan validation, blocking action until approved.
