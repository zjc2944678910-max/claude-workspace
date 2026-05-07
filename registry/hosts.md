# Host Registry

## oc-nas

- Alias: `oc-nas`
- Role: current live OpenClaw SSH target for audits and repairs
- Default mode: read-only audit
- Use when:
  - checking live health
  - collecting read-only evidence
  - verifying runtime state during an incident
- Do not use for state-changing work unless the user explicitly authorizes it.
