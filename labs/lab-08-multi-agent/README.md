# Lab 8: Multi-agent coordination (Domain 5)

**Goal:** run agents in parallel, trigger and resolve a conflict, keep a hand-off record and rehearse recovery.

## Steps

1. Create a coordination issue from `assets/coordination-issue.md`. It owns the plan, the ownership table and the decision log.
2. **Orchestrator-worker:** split work into three sub-issues: #3 `format_price`, #5 `clamp_discount`, #6 docstrings. Fill the ownership table.
3. Assign all three to Copilot at once. Note each session gets its own `copilot/` branch.
4. **Conflict drill:** two of the tasks both edit `shop.py`. Merge one, then see what happens to the second PR. Resolve it (ask the agent to update/rebase on the PR, or re-partition) and record the decision in the log.
5. **Duplicate drill:** deliberately assign two agents the same issue. Detect and close the duplicate. Add a "claim" step to your process (assignee/label).
6. **Hand-off record:** after each agent finishes, log what was handed to the next stage (tests agent or reviewer).
7. **Stall drill:** cancel a session halfway. Roll back or resume from PROGRESS.md.

## Verify

- [ ] Each agent had its own branch and PR
- [ ] Conflict detected and resolved with a recorded decision
- [ ] Duplicate prevented by a claim mechanism
- [ ] Coordination issue lets an outsider reconstruct who did what

## Break it

Remove the ownership table and repeat step 3. Count conflicts. Restore it.

## Exam link

Orchestration patterns, isolation, conflict types, hand-off documentation, failure recovery. Also read the docs on custom agents and (optionally) Copilot CLI fleet/parallel tasks to see the same ideas implemented locally.
