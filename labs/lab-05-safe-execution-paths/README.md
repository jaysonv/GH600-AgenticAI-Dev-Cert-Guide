# Lab 5: Safe execution paths (Domains 2 and 6)

**Goal:** set the repository controls that bound an agent, then rehearse retry, rollback and escalation.

## Steps

1. Create a branch ruleset (or branch protection) for `main`: require a PR, require 1 approval, require status checks (a simple workflow running `python -m unittest`).
2. Add `assets/CODEOWNERS` (replace the handle with yours).
3. Assign issue #1 to Copilot. Record: branch name, PR draft status, whether workflows ran, who can approve.
4. Click **Approve and run workflows** and watch CI.
5. Try to approve the PR as the user who requested it. Note what GitHub allows.
6. **Rollback drill:** close the draft PR without merging. Confirm `main` is unchanged and delete the `copilot/` branch.
7. **Escalation drill:** write an issue comment template (`assets/escalation-template.md`) and use it when an agent run needs a human.

## Verify

- [ ] Agent worked on a single `copilot/` branch
- [ ] Workflows waited for approval
- [ ] Requester could not satisfy the required approval on their own request
- [ ] Rollback left `main` untouched

## Break it

Remove "required checks" from the ruleset and reason about what a bad agent PR could now do. Restore the rule.

## Exam link

Branch-based scope, autonomous branch/PR actions, retries, rollbacks, escalation, traceability. Verify behaviors in *Risks and mitigations*.
