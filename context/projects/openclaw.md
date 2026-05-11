# OpenClaw — Project Card

| Field | Value |
|---|---|
| **Repository** | `/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/products/openclaw/nas-openclaw-v22` |
| **Summary** | OpenClaw NAS application (mainline product) |
| **Live host** | `oc-nas` |

## Key Surfaces

- **Mainline repo**: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/products/openclaw/nas-openclaw-v22` — product code changes
- **Migration reference**: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/migrations/openclaw-mac-migration` — legacy comparison, recovery
- **Ops surface**: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/ops/projects/openclaw` — deployment history, rollback bundles, audit evidence
- **Sidecar state**: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/state/project-data/openclaw` — non-source project data

## Working Guidance

- Feature or bug fix → mainline repo.
- Live audit or deployment ledger → ops surface.
- Old/new layout comparison → migration reference.
- Project-specific local state → sidecar state.

## Safety Boundary

- NAS, live, production, slow-reply, timeout, and performance tasks are **read-only by default**.
- Keep confirmed evidence, hypotheses, and recommendations separate.
- No repair actions without explicit user approval.
