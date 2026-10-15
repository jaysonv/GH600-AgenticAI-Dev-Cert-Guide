# Lab 6: Memory and state (Domain 3)

**Goal:** make progress durable, observe Copilot Memory, and run a drift drill.

## Steps

1. **Memory settings.** Find your Copilot Memory settings (personal settings, or admin settings if you manage an org). Read what is stored for you and for your sandbox repo. Note which items have citations. *Memory is a public-preview feature: availability varies by plan.*
2. **Progress artifact.** Create a long task: *"Add `format_price`, `clamp_discount`, docstrings for all functions."* Tell the agent to maintain `PROGRESS.md` on its branch (see `assets/PROGRESS-template.md`) with done/next/decisions.
3. **Interrupt and resume.** Stop the session midway (or start a new session on the same branch). Ask the agent to resume. Check that it reads PROGRESS.md, verifies state and does not redo finished steps.
4. **Drift drill.** Add the constraint "do not change `parse_price`" at the start. Add a later instruction that tempts the agent to touch it. See if it holds the constraint. Use a checkpoint review to detect drift.
5. **Stale fact drill.** Change a convention in the repo (for example switch the test command in your instructions). Check that agents follow the new convention and discuss how stale facts would age out.

## Verify

- [ ] PROGRESS.md reflects reality after each step
- [ ] Resumed session skipped completed work
- [ ] You can name three ways to correct drift
- [ ] You know where to view and delete stored memories

## Break it

Edit PROGRESS.md to claim a step is done when it is not. Does the agent verify or trust it? This is why "verify recorded state against reality" matters.

## Exam link

Short vs long-term vs external memory, pruning/expiration, durable artifacts, resuming, drift, sharing state, stale and conflicting context.
