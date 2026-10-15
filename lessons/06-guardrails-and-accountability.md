# Lesson 6: Implement guardrails and accountability (10-15%)

**Objectives:** define autonomy levels; implement guardrails and human-in-the-loop workflows.

## 1. Autonomy levels

Classify each kind of agent action by **operational**, **security** and **compliance** risk, then assign the lowest level of human involvement that is still safe. The goal: **maximize delivery speed while staying compliant** with organizational security and Responsible AI standards.

### Risk classification (study example)

| Action | Typical risk | Reversible? | Suggested control |
|---|---|---|---|
| Read code, search, list issues | Low | n/a | Allow (read-only tools) |
| Create a branch, open a draft PR | Low | Yes | Allow, human reviews the PR |
| Run tests in the sandbox | Low-medium | Yes | Allow in isolated environment |
| Run CI workflows on agent code | Medium | Mostly | Approve and run workflows (default) |
| Change dependencies, workflow files, auth code | High | Mostly | Required reviewers via CODEOWNERS/rulesets, security scans |
| Touch secrets, permissions, org settings | Very high | Hard | Block, or explicit human authorization |
| Deploy to production, delete data, publish releases | Very high | **No** | Explicit authorization through a controlled path (protected environment, required reviewers) |

### Autonomy ladder (study aid)

L0 suggest only > L1 act with approval per step > L2 act in sandbox, human reviews PR > L3 act and merge low-risk changes when checks pass > L4 fully autonomous. Most teams should live at L1-L2 for code and move specific, well-understood task types up as evidence accumulates.

## 2. Guardrails and human-in-the-loop

### Identify what needs human judgment

Humans add value where there is ambiguity, business or ethical trade-offs, security sensitivity or irreversibility. They add little to rote, verifiable, reversible steps. Spend approvals where they reduce risk.

### Block actions that violate policy

Use **technical enforcement**, not just instructions.

- Tool allowlists and read-only tool sets
- **Firewall** and network allowlists
- Branch protection, **rulesets**, required status checks, required reviews, CODEOWNERS
- Secret scanning and push protection, code scanning as required checks
- Content exclusion for sensitive files
- Org/enterprise policies for Copilot features and MCP servers
- Hooks that can deny a tool call (see the *Hooks* docs; **verify** current behavior)

Instructions ("never touch secrets") help but are advisory. A model can ignore them. Controls the agent cannot bypass are the real guardrail.

### Least privilege

- Narrowest tool list; read-only MCP endpoints and tools
- Fine-grained PATs or GitHub Apps limited to specific repos and read-only where possible
- Secrets scoped to where they are needed (`COPILOT_MCP_` Agents secrets for MCP, the `copilot` environment for setup steps)
- Minimal `permissions:` in workflows

### Explicit authorization for irreversible or compliance-sensitive changes

Use controlled paths: protected environments with required reviewers for deploys, protected branches, two-person rules, signed commits, change tickets where compliance demands it.

### Preserve velocity

Do not add approvals that do not reduce risk. Approve at PR level, not per tool call. Use async review. Auto-allow read-only actions. Reserve blocking approvals for high-risk classes.

## 3. What GitHub's cloud agent already enforces (verified)

| Risk | Built-in mitigation |
|---|---|
| Unvalidated code | CodeQL, dependency advisory check, secret scanning, code review pass |
| Pushing code | Only users with **write access** can trigger it. One branch (`copilot/` or the PR branch). Cannot run arbitrary git. Draft PRs need human review/merge; it cannot mark ready, approve or merge. Workflows wait for **Approve and run workflows**. The requester **cannot approve** the PR. **Extra approval** needed for PRs under its own identity (if approvals required) |
| Sensitive data exposure | Restricted internet access via **firewall** |
| Prompt injection | **Hidden characters filtered**, for example HTML comments are not passed to the agent. Comments from users without write access are never shown |
| Loss of oversight | Commits authored by Copilot with requester as co-author, **signed**, linking to **session logs**. Session logs and **audit log events** for admins |
| Automations (no human starting each task) | Work attributed to the creator (who therefore cannot approve it), you choose exactly which tools an automation can use, events from untrusted users are ignored by default, workflows still need human approval |

The study guide links the *Build guardrails* tutorial and the *Risks and mitigations* page. Read both.

## 4. Responsible AI and accountability

- A human is accountable for what merges. "The agent did it" is not a control.
- Make actions attributable and reviewable (co-authorship, logs).
- Review AI-generated code for security, licensing and quality like any contribution.
- Be transparent: label agent-authored PRs, keep audit trails.
- Check the *Responsible use: Agents* documentation.

## Exam traps

- Instructions are not enforcement.
- Approving every tool call is not safe, only slow.
- Irreversible actions (production deploys) need explicit authorization or a controlled path, no matter how good the agent is.
- Least privilege wins ties: narrow tools, read-only first, scoped tokens.
- The person who triggers the agent should not be the sole approver of its output.

## Self-check

1. Classify five agent actions by risk and assign a control.
2. Why are instructions weaker than a ruleset?
3. Name four built-in cloud agent protections.
4. How do you keep guardrails from destroying velocity?

Next: [Lab 9](../labs/lab-09-guardrails-and-autonomy/README.md).
