# Lesson 2: Implement tool use and environment interaction (20-25%)

The largest domain. Four objective groups: select and configure tools, configure MCP servers, integrate agents with development environments, and run agents with safe execution paths.

## 1. Selecting and configuring tools

1. **Identify required tools** from the task. Read code? search? edit? run tests? call an external system? Start from the task, not from "what is available".
2. **Configure** them: built-in tools, custom agent `tools` lists, MCP servers.
3. **Permissions**: least privilege. Read-only first. Add write tools only when the task needs them. A narrow tool list is the strongest guardrail you have because the agent *cannot* call what it does not have.

## 2. MCP (Model Context Protocol) servers

MCP is a standard way for agents (clients) to use external tools and data (servers). Servers can run **locally** (a process the agent starts) or be **remote** (HTTP/SSE).

### Repository-level configuration for cloud agent (verified)

Location: repo **Settings > Copilot > MCP servers**. Paste JSON with a top-level `mcpServers` object.

```json
{
  "mcpServers": {
    "sentry": {
      "type": "local",
      "command": "npx",
      "args": ["@sentry/mcp-server@latest", "--host=$SENTRY_HOST"],
      "env": {
        "SENTRY_HOST": "https://contoso.sentry.io",
        "SENTRY_ACCESS_TOKEN": "$COPILOT_MCP_SENTRY_ACCESS_TOKEN"
      },
      "tools": ["get_issue_details"]
    }
  }
}
```

Keys:

| Key | Notes |
|---|---|
| `type` (required) | `local`, `stdio`, `http` or `sse` |
| `tools` (required) | Names of enabled tools, or `["*"]`. **Allowlist specific read-only tools**: the agent uses them autonomously and does not ask approval |
| `command`, `args`, `env` | Local servers |
| `url`, `headers` | Remote servers |

Secrets and variables: add **Agents** secrets/variables whose names start with **`COPILOT_MCP_`**. Only those are visible to the MCP config. Substitution: `$VAR`, `${VAR}`, `${VAR:-default}`.

Limits to remember: cloud agent and code review support MCP **tools only** (not resources or prompts) and do **not** support remote servers that use **OAuth**. Code review only uses tools that set `annotations.readOnlyHint: true`.

Defaults: the **GitHub MCP server** and **Playwright MCP server** are enabled by default. The default GitHub token is **read-only and limited to the current repository**. To reach other repos, configure a fine-grained PAT (read-only, specific repos) or a GitHub App, and keep `tools` narrow.

### The remote GitHub MCP server

- `https://api.githubcopilot.com/mcp/` (full) and `https://api.githubcopilot.com/mcp/readonly` (read-only).
- Header `X-MCP-Toolsets` selects toolsets (for example `repos,issues,pull_requests`). Use the `tools` field to pick individual tools.
- If the firewall warns about `api.github.com`, add it to the custom allowlist.

### Registries and allow lists (governance)

Organizations and enterprises can control which MCP servers are usable: an **allowlist** of permitted servers, and an **MCP registry** (public or private) that is the source of discoverable servers, optionally with enforcement so only registry servers are allowed. Org/enterprise admins can also define MCP servers inside **custom agent** frontmatter. **Verify** the current policy names in *Configure enterprise allowlist*, *Configure MCP registry* and *Restrict based on registry*.

### Validating MCP configuration (verified)

Assign an issue to Copilot, open the session via **View session**, open the log's **Start MCP Servers** step: started servers list their tools. If a server needs `uv`, `pipx` or other tools missing from the runner, install them in `copilot-setup-steps.yml`.

## 3. Integrating agents within development environments

**Execution context.** Cloud agent runs in an ephemeral, GitHub Actions-powered environment. Evaluate: what is installed, what network is reachable, what secrets exist, which repo and branch.

**Environment setup.** `.github/workflows/copilot-setup-steps.yml` with a single job named `copilot-setup-steps` installs dependencies and logs in to services before the agent starts. Secrets for it live in the `copilot` environment / Agents secrets.

**Firewall.** Internet access is restricted by default. Add specific hosts to the custom allowlist rather than disabling the firewall.

**Scope to a repository.** Cloud agent works in the repository where the task starts. Repo-level MCP config, instructions and permissions bound what it can see. The default GitHub token only reaches the current repo.

**Branch-based scope (verified).** The agent can push to **a single branch**: a new `copilot/` branch, or the PR's branch when you mention `@copilot` on an existing PR. Branch protection and required checks still apply.

**Autonomous actions (verified).** It can create branches and **draft** PRs. It cannot approve or merge, cannot mark "Ready for review", and cannot run arbitrary git commands. By default workflows on its PRs do not run until a user with write access clicks **Approve and run workflows**.

**Invoked from CI.** Agents can be run from workflows (for example Copilot CLI in GitHub Actions, or agentic workflows). Give the workflow minimal `permissions:`, pin actions, and treat issue/PR text as untrusted input.

**Environment-specific constraints.** Runner type (hosted, larger, self-hosted), network egress, required tooling, secrets, org policy. Handle them in setup steps and allowlists, not by loosening everything.

## 4. Safe execution paths and error handling

| Concern | Pattern |
|---|---|
| Error handling | Classify errors: transient vs deterministic; surface a clear message |
| Retries | **Bounded** retries with backoff for transient errors. Never retry deterministic failures (denied permission, invalid config). Make operations idempotent |
| Rollbacks | Work on an isolated branch: close the draft PR or revert commits. `main` is untouched. Copilot CLI also supports cancel and roll back |
| Escalation paths | After retry limit or on ambiguity: comment, assign a human, add a label, open an issue. Define who and where beforehand |
| Traceability | Commits authored by Copilot with the requester as co-author, **signed** (Verified), messages link to the **session log**. Admins get session logs and **audit log events** |

## Exam traps

- "Retry until it works" is wrong. Bounded retries, then escalate.
- Turning off the firewall to fix one blocked host is wrong. Allowlist the host.
- Secrets in MCP config must be `COPILOT_MCP_`-prefixed Agents secrets, never literals committed to the repo.
- `tools: ["*"]` on a write-capable server is the lazy answer. Prefer a named list.
- The agent opening a PR does not mean CI ran. Someone with write access must approve workflow runs (default).

## Self-check

1. Where do you put MCP JSON, and which secret prefix is required?
2. Which two things does cloud agent MCP not support?
3. Name three controls that make an agent's push safe.
4. A tool call fails with "permission denied". Retry or escalate? Why?

Next: Labs [3](../labs/lab-03-environment-and-firewall/README.md), [4](../labs/lab-04-mcp-servers/README.md), [5](../labs/lab-05-safe-execution-paths/README.md).
