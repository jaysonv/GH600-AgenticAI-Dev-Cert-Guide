# GH-600 cheat sheet

Items marked (v) were checked against docs.github.com or Microsoft Learn on 15 Oct 2026. Unmarked items come from background knowledge: confirm them in the docs before relying on them.

## Files and locations

| Thing | Location |
|---|---|
| Repo-wide custom instructions | `.github/copilot-instructions.md` |
| Path-specific instructions | `.github/instructions/*.instructions.md` with `applyTo` frontmatter |
| Agent-readable instructions (cross-tool) | `AGENTS.md` |
| Custom agents (repo) | `.github/agents/*.agent.md` |
| Org/enterprise custom agents | `github-private` repo (see "Prepare for custom agents" docs) |
| Cloud agent environment setup | `.github/workflows/copilot-setup-steps.yml`, job named `copilot-setup-steps` (v) |
| Repo MCP config | Repo **Settings > Copilot > MCP servers**, JSON with top-level `mcpServers` (v) |
| MCP secrets/variables | **Agents** secrets/variables, names must start `COPILOT_MCP_` (v) |

## MCP config keys (v)

- Required: `tools` (list of tool names, or `["*"]`), `type` (`local`, `stdio`, `http`, `sse`)
- Local: `command`, `args`, optional `env`
- Remote: `url`, optional `headers`
- Variable substitution: `$VAR`, `${VAR}`, `${VAR:-default}` (names must start `COPILOT_MCP_`)
- Only MCP **tools** are supported (not resources or prompts). Remote servers needing **OAuth** are not supported.
- GitHub MCP and Playwright MCP are on by default. Default GitHub token: **read-only, current repo only**.
- Remote GitHub MCP: `https://api.githubcopilot.com/mcp/` and the read-only variant `/mcp/readonly`. Header `X-MCP-Toolsets` selects toolsets.
- Once configured, tools are used **autonomously, without asking approval**: allowlist specific read-only tools.
- Code review only uses tools whose `annotations.readOnlyHint` is `true`.
- Validate: assign an issue to Copilot > View session > **Start MCP Servers** step lists tools.

## Cloud agent guardrails (v)

- Only users with **write access** can trigger it. Comments from others are never shown to it.
- Pushes to **one branch**: a new `copilot/` branch, or the PR branch when you `@copilot` on an existing PR. Branch protections and required checks still apply.
- Cannot run arbitrary git, cannot mark "Ready for review", cannot approve or merge.
- Workflows do **not** run until a user with write access clicks **Approve and run workflows** (can be relaxed).
- The person who requested the PR **cannot approve it**. PRs under the agent's own identity need **one extra approval** (if approvals are already required).
- Internet access restricted by a **firewall** (customizable allowlist).
- Hidden characters are filtered from input (an HTML comment in an issue is not passed to the agent).
- Commits: authored by Copilot, requester as co-author, **signed (Verified)**, message links to the **session log**. Admins get session logs and **audit log events**.
- Built-in validation: **CodeQL**, **Advisory Database** checks on new dependencies, **secret scanning**, **Copilot code review**. No GHAS license required.

## Copilot Memory (v, public preview)

- Stores **repository-level facts** and **user-level preferences**.
- Facts carry **citations**, validated against the **current branch** before use.
- Unused entries auto-deleted after **28 days**.
- Created from activity by users with **write access** and Memory enabled. Repo owners can review and delete repo facts. Users can delete their own preferences.
- Used by cloud agent, code review, Copilot CLI and agentic autofix. Code review uses repo-level facts only.
- Enabled **per user**. In org/enterprise plans an admin enables the policy first.

## Autonomy ladder (study aid, not a GitHub term)

| Level | Behavior | Example |
|---|---|---|
| L0 | Suggest only | Chat answers |
| L1 | Acts after approving each step | Plan approval gate |
| L2 | Acts in sandbox; human reviews the PR | Cloud agent default |
| L3 | Acts and merges low-risk change when checks pass | Doc typo fix |
| L4 | Fully autonomous | Rarely justified |

## Error-handling reflexes

| Symptom | Reflex |
|---|---|
| Transient failure (timeout, 503) | Bounded retry with backoff, then escalate |
| Deterministic failure (denied, bad config) | Do not retry. Fix cause or escalate |
| Partial progress | Resume from checkpoint idempotently, or roll back |
| Bad change pre-merge | Close draft PR / revert on `copilot/` branch |
| Stalled agent | Timeout, cancel, roll back partial work, re-queue or escalate |
| Repeated degraded behavior | Circuit breaker: stop routing, fall back to human |

## Failure classification

| Class | Clues | Typical fix |
|---|---|---|
| Reasoning | Wrong plan, misread requirement, scope creep | Clearer acceptance criteria, plan validation, smaller task |
| Tool misuse | Wrong arguments, denied call, MCP not started | Fix tool config/allowlist, tighten instructions for the tool |
| Context/environment | Missing dependency, firewall block, stale memory | Setup steps, firewall allowlist, prune stale context |
