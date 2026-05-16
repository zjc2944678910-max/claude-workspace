# Live Audit Rules

These rules implement the L2 read-only gate from `15-risk-levels.md`.

- OpenClaw, NAS, live, production, timeout, and performance tasks default to **L2 read-only audit mode**.
- Use repo docs, ops surfaces, and read-only host inspection to gather evidence.
- Do not restart services, edit production files, patch runtimes, or change config without explicit approval.
- State-changing repair requires **L3 authorization** — user must say "进入修复阶段".
- Summaries should separate confirmed evidence, hypotheses, risks, and next checks.
- See `15-risk-levels.md` for full risk classification and escalation rules.
