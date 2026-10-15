# Lab 1: Instructions and agent boundaries (Domain 1)

**Goal:** see how task definition and repo instructions change cloud agent output.

## Steps

1. Copy `labs/sandbox-app/` into a new private repo.
2. Create issue #4 **"Make pricing better"** exactly as written. Assign to Copilot. Note what it does: scope, tests, PR description. Close the PR without merging.
3. Create issue #1 using `assets/issue-template.md` (acceptance criteria, scope, constraints). Assign to Copilot. Compare with step 2.
4. Add `.github/copilot-instructions.md` from `assets/copilot-instructions.md` and the path-specific file `assets/python.instructions.md` to `.github/instructions/`.
5. Re-run issue #2 and check whether the agent now runs the documented test command and follows the conventions.

## Verify

- [ ] Vague issue produced a wider or less predictable diff than the templated one
- [ ] The agent's PR cites or follows your instructions
- [ ] You can name each anti-pattern you saw (vague task, no done criteria, scope creep)

## Break it

Add a contradictory line to the instructions ("always add type hints" and "never add type hints"). Re-run a task. Observe inconsistent behavior, then fix by deleting the contradiction.

## Exam link

Anti-patterns, inputs/outputs/success criteria, repo instructions. Docs: *Add repository instructions*, *Get the best results* (cloud agent tutorials).
