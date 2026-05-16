# Risk Level Classification

## Levels

| Level | Meaning | Required Behavior |
|-------|---------|-------------------|
| **L0 tiny** | Simple questions, single-file small edits, typos, lightweight checks | Answer directly, skip overhead (no route lock, no delegation, no health checks) |
| **L0/L1** | Local code edits, known scope, workflow/tooling changes | Plan → implement → verify; state level before acting |
| **L2** | Read-only audit: live/production/NAS/OpenClaw/VPS/timeout/performance | Do NOT modify, restart, deploy, patch, or repair. Gather evidence only |
| **L3** | State-changing repair: config writes, service restarts, deploys, runtime changes | Blocked until user explicitly says "进入修复阶段" |

## Decision Tree

- Simple question or lightweight check → **L0 tiny**
- Local code edit, scope is explicit and bounded → **L0/L1**
- Touches OpenClaw, NAS, live, production, VPS, timeout, performance → **L2 read-only**
- Involves service restart, deploy, config write, rollback, runtime patch → **L3 blocked**

## Escalation Rules

- If uncertain between two levels, raise by one.
- L0 tiny fast path NEVER overrides L2 or L3 gates.
- Substantive tasks: state level + rationale before first action.
- L0 tiny → L1 escalation triggers: touches multiple modules, shared core logic, API routes, dependency/build/CI behavior, unclear project routing, or any live/production/deploy/auth/secrets surface.

## Repair Authorization

- L3 tasks require the explicit phrase "进入修复阶段" from the user.
- Authorization expires after 30 minutes or at session end.
- Even with authorization, keep changes minimal and reversible.
- Document what was changed and why in the closeout.

## Cross-References

- Live audit behavior: `20-live-audit.md`
- Project risk profiles: `registry/project-registry.json`
- Daily workflow paths: `context/daily-workflow.md`
