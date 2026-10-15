# Sources

## Official (start here)

- Certification page: https://learn.microsoft.com/en-us/credentials/certifications/agentic-ai-developer/
- **Study guide (skills measured):** https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-600
- Exam sandbox: https://ghcertdemo.starttest.com/
- Microsoft Learn modules named in the study guide:
  - Foundations of Agentic AI in GitHub: https://learn.microsoft.com/en-us/training/modules/foundations-agentic-ai/
  - Designing Agent Architecture and SDLC Integration: https://learn.microsoft.com/en-us/training/modules/design-agent-architecture-integration/
  - Tooling, MCP, and Agent Execution Environments: https://learn.microsoft.com/en-us/training/modules/agent-tooling-mcp-execution-environments/
- Instructor-led course: Microsoft GH-600T00, *Developing in Agentic AI Systems*

## GitHub Docs (domain by domain)

| Domain | Pages |
|---|---|
| 1 Architecture and SDLC | Prepare for custom agents (admin), Customization library: Implementation planner, Research/plan/iterate, Use plan mode (IDE), Review Copilot output |
| 2 Tools and environment | Configure MCP servers, MCP and cloud agent, Customize the agent environment (copilot-setup-steps), Customize the firewall, Custom agents configuration (reference), Configure enterprise allowlist, Configure MCP registry, Restrict based on registry, Configure secrets and variables, Copilot CLI in Actions |
| 3 Memory and state | About Copilot Memory, Manage Copilot Memory (yourself / administrator), CLI context management, Session persistence (SDK) |
| 4 Evaluation | Manage agent sessions, Troubleshoot cloud agent, Review AI-generated code, Customization library: custom agents |
| 5 Multi-agent | Custom agents (SDK feature), Fleet mode / parallel task execution (CLI), Monitor agentic activity, Agentic audit log events |
| 6 Guardrails | Risks and mitigations (cloud agent), Build guardrails (tutorial), Hooks, About automations, Rationale/confidence/approvals, Responsible use: Agents |

All under https://docs.github.com/en/copilot (search the title). The study guide itself links the "Build guardrails" tutorial and the risks-and-mitigations page.

## How this repo was built

Domain lists, weights and exam logistics come from the Microsoft study guide. Facts marked (v) were read directly in GitHub Docs. Lessons also use general agent-engineering practice (planning gates, orchestration patterns, evaluation), which is what the exam scenarios test.

## Caution on third-party material

Some "GH-600 prep" pages describe a different exam (Azure AI Foundry, Semantic Kernel, AutoGen). That is **not** this exam. "Exam dumps" sites also violate Microsoft's exam policies and are often wrong. Use official docs plus original practice questions.
