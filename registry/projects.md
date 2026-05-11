# Project Registry

This file is the detailed registry of real repositories and working surfaces that Claude sessions may need.

Active project set: **OpenClaw**, **NAS Platform**, **Telegram Dual Relay**, **MathorCup-D**.

## OpenClaw

- Mainline repository: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/products/openclaw/nas-openclaw-v22`
- Migration reference: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/migrations/openclaw-mac-migration`
- Ops surface: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/ops/projects/openclaw`
- Sidecar state: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/state/project-data/openclaw`
- Live host alias: `oc-nas`
- Typical route:
  - product fix -> mainline repo
  - live audit or deployment history -> ops surface
  - legacy comparison -> migration reference

## NAS Platform

- Repository: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/infrastructure/nas-platform`
- Summary: NAS and VPS infrastructure repo with app stacks, infra stacks, generated env files, and deployment scripts
- Primary surfaces:
  - `apps-*`
  - `infra-*`
  - `generated/`
  - `scripts/`
  - `vps-nginx/`
  - `vps-ssh/`

## Telegram Dual Relay

- Repository: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/infrastructure/telegram-dual-relay`
- Summary: Telegram message relay service for dual-bot forwarding
- Primary surfaces:
  - `src/`
  - `scripts/`
  - `systemd/`
  - `tests/`
  - `docs/`

## MathorCup-D

- Product-style archive repo: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/products/MathorCup_D_repo`
- Research workspace: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/research/mathorcup_D`
- Summary: MathorCup competition Problem D — data analysis and modeling
