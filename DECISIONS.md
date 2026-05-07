# Decisions

Use this file for durable workflow or architecture decisions that should survive beyond one session.

## 2026-05-05

- `claude-workspace` is the Claude Code coordination root and not a product code repository.
- Real code changes belong in the actual project repositories referenced by `PROJECTS.md`.
- OpenClaw, NAS, live, production, slow-reply, timeout, and performance investigations default to read-only audit mode.
- Durable knowledge should be promoted into `context/`; raw or temporary material should start in `inbox/` or `scratch/`.
- The Codex-oriented workspace index remains `/Users/zhangjincheng/Documents/GitHub/codex-workspace`.
