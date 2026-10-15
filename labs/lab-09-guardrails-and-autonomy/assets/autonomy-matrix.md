# Autonomy matrix

| Action | Operational risk | Security risk | Compliance risk | Reversible? | Level (L0-L4) | Control (technical) |
|---|---|---|---|---|---|---|
| Read repository | Low | Low | Low | n/a | L3 | Read-only tools |
| Create branch + draft PR | Low | Low | Low | Yes | L2 | Single branch, PR review |
| Run tests | | | | | | |
| Modify workflow files | High | High | Medium | Mostly | L1 | CODEOWNERS + ruleset |
| Add dependency | | | | | | |
| Change secrets/permissions | | | | | | |
| Deploy to production | Very high | Very high | High | No | L0/L1 | Protected environment, required reviewers |
