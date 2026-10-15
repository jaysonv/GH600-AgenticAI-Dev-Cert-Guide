# Lesson 3: Manage memory, state, and execution (10-15%)

**Objectives:** implement memory strategies; persist state and manage context drift; keep memory and state consistent across tools and environments.

## 1. Memory strategies

| Type | What it is | GitHub examples | Lifetime |
|---|---|---|---|
| **Short-term** | What is in the current context window / session | The running session, chat turns | One session |
| **Long-term** | Knowledge persisted for future sessions | Copilot Memory, custom instructions | Days to indefinitely |
| **External** | State kept outside the model in systems of record | Issues, PR descriptions, progress files in the repo, databases, MCP servers | As long as the system keeps it |

Choosing: put **stable conventions** in instructions (reviewed, versioned). Let **learned repo facts** live in Copilot Memory. Put **task progress and decisions** in external, durable artifacts. Keep **scratch reasoning** short-term.

### Copilot Memory (verified, public preview at time of writing)

- Stores **repository-level facts** (conventions, architecture decisions, build commands) and **user-level preferences**.
- Repo facts are stored **with citations** to supporting code. Before use, Copilot checks citations against the **current branch**; only validated facts are used.
- Created only from activity by users with **write access** and Memory enabled. Repo facts are usable only in operations on the **same repository**.
- Repo owners can **review and delete** repo facts. Users can view/delete their own preferences. Admins can export/delete user preferences on Business/Enterprise plans.
- **Expiration:** unused entries are deleted automatically after **28 days**. Successful validation and use can reset the timer.
- Used by cloud agent, code review, Copilot CLI and agentic autofix. Code review uses repo-level facts only.
- Enabled **per user**. Org/enterprise admins enable the policy first, then users can opt out.

### Scoping memory to the task

- Use **path-specific instructions** (`applyTo`) so Python rules do not clutter a docs task.
- Keep instructions short and specific. A bloated context buries the important lines.
- Pull in only linked context the task needs, not the whole wiki.

### Expiration, pruning and reset rules

Decide, for each memory source: *who may write it, how it is validated, when it expires, who can delete it, how to reset it.* Copilot Memory already gives you validation against the branch, a 28-day unused expiry and delete controls. For your own external state (progress files, notes), add equivalents: dated entries, an owner, a "last verified" marker, and a cleanup step on task completion.

## 2. Persisting state and managing context drift

**State as durable artifacts.** Capture progress and decisions where humans and the next session can read them:

- a checklist in the PR description (done / next / blocked)
- a `PROGRESS.md` or decision log on the working branch
- issue comments for hand-offs and rationale
- commit messages that explain *why*

**Resuming without repeating or diverging.**

1. Start every resumed session by **reading** the artifacts and the git diff.
2. **Verify** recorded state against reality (is step 3 really done? do tests pass now?).
3. Make steps **idempotent** so re-running one is harmless.
4. Continue from the first unverified step and **honor recorded decisions** unless you explicitly supersede them (with a note).

**Drift** is gradual divergence from the original intent during long runs: forgotten constraints, scope creep, contradicting earlier decisions.

- **Detect:** at checkpoints compare current work with the acceptance criteria and plan; diff size vs scope; tests unrelated to the task changing; instructions being violated.
- **Correct:** re-anchor by re-stating goal and constraints, revert off-scope changes, split the task, start a fresh session seeded from the artifacts.

## 3. Continuity across tools and environments

Agents may work in the IDE, CLI, cloud agent and code review. State must survive hand-offs.

- **Share state** through the repository and GitHub objects, not chat history. Copilot Memory is shared across features (a fact learned by cloud agent can be used by code review).
- **Prevent conflicting context:** one source of truth per fact (for example conventions live in one instructions file, not three). When two sources disagree, resolve by deleting or fixing one, not by hoping.
- **Prevent stale context:** validate against current code (as Memory does with citations), expire, and re-verify before acting on remembered facts.

## Exam traps

- Memory is not a place for secrets or one-off task notes.
- "Longer context" does not fix drift. Re-anchoring and smaller tasks do.
- Memory facts are validated against the **current branch**: a fact about code that no longer exists will not be used.
- Chat history is not durable shared state.

## Self-check

1. Which memory type holds a PR checklist, and why is it preferable for resuming work?
2. After how long are unused Copilot Memory entries removed?
3. What three actions come first when resuming an interrupted agent task?
4. How do you stop two tools from acting on contradictory conventions?

Next: [Lab 6](../labs/lab-06-memory-and-state/README.md).
