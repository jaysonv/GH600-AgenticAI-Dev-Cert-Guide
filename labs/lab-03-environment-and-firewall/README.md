# Lab 3: Environment setup and firewall (Domain 2)

**Goal:** prepare the agent's environment with `copilot-setup-steps.yml` and handle a blocked network call correctly.

## Steps

1. Add `assets/copilot-setup-steps.yml` as `.github/workflows/copilot-setup-steps.yml`. Run it manually (`workflow_dispatch`) once to prove it works.
2. Add a dev-only dependency to the sandbox app (for example create `requirements-dev.txt` with `ruff`). Update setup steps to install it.
3. Create a task: *"Run ruff on the project and fix findings."* Assign to Copilot. Confirm in the session log that the setup steps ran first.
4. Create a task that needs an external host (for example fetch a schema from a URL). Observe the firewall warning.
5. Add the **single** host to the custom allowlist (see *Customize the firewall*). Re-run.

## Verify

- [ ] Job name is exactly `copilot-setup-steps`
- [ ] Session log shows setup steps before agent work
- [ ] Only the required host was allowlisted

## Break it

Rename the job to `setup`. Re-run and note the behavior. Fix it. Then remove the dependency install and re-run to see an environment failure (classify it for Lab 7).

## Exam link

Execution context, environment-specific constraints, firewall allowlist vs disabling.
