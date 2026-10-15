# Lab 4: MCP servers (Domain 2)

**Goal:** configure, validate and constrain MCP servers using least privilege.

## Steps

1. In repo Settings > Copilot > MCP servers, paste `assets/mcp-readonly-github.json` (remote GitHub MCP, read-only, narrow toolsets). Create a **fine-grained PAT** with read-only access to your sandbox repo only. Store it as Agents secret `COPILOT_MCP_GITHUB_PERSONAL_ACCESS_TOKEN`.
2. Assign an issue to Copilot: *"List open issues and summarize them in a comment."* Open **View session**, then the **Start MCP Servers** step. Confirm the tools.
3. Add a second server from `assets/mcp-local-example.json` (adapt to any server you have). Use a named `tools` list. Add its secret with the `COPILOT_MCP_` prefix.
4. Confirm the agent can only call listed tools.

## Verify

- [ ] Secrets are `COPILOT_MCP_` prefixed Agents secrets
- [ ] `tools` is a named read-only list, not `*`
- [ ] You can find the MCP startup step in the session log
- [ ] You can state the two cloud-agent MCP limitations

## Break it

1. Misspell the secret name: observe the failure and where it shows up.
2. Use a remote server that requires OAuth: observe that it is unsupported.
3. Remove `/readonly` and widen `tools` to `*`: write down what new risk you introduced.

## Exam link

Add MCP as a tool, GitHub remote MCP server, registries, allow lists. The admin-level registry and allowlist features need an org/enterprise: read *Configure enterprise allowlist*, *Configure MCP registry* and *Restrict based on registry*, then summarize each in three lines.
