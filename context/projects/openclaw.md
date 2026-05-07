# OpenClaw Project Note

## Identity

- Project name: OpenClaw
- Mainline repository: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/products/openclaw/nas-openclaw-v22`
- Migration reference: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/migrations/openclaw-mac-migration`
- Operator surface: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/ops/projects/openclaw`
- Sidecar state: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/state/project-data/openclaw`
- Live host alias: `oc-nas`

## Working Modes

- Product code changes: use the mainline repository
- Migration comparison or historical reconstruction: use the migration reference
- Operator docs, deployment history, evidence, rollback bundles: use the ops surface
- Non-source project data: use the sidecar state path

## Default Safety Boundary

- Treat NAS, live, production, slow-reply, timeout, and performance-incident requests as read-only by default.
- Keep confirmed evidence, hypotheses, and recommendations separate.
- Do not perform repair actions unless the user explicitly authorizes a repair stage.

## Common Route Choice

- Feature or bug fix in the application: mainline repository
- Live audit, deployment ledger, mirrors, rollback review: ops surface
- Comparing old and new layouts or recovering lost context: migration reference
- Reviewing project-specific local state: sidecar state
