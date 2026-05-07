# Workspace Model

## Role Split

- `claude-workspace`: Claude Code coordination root for context, planning, audits, and handoffs
- `codex-workspace`: Codex-oriented workspace index and broader operator surface
- Real project repositories: where implementation changes actually happen

## Daily Flow

1. Start in `claude-workspace`.
2. Read `CLAUDE.md`.
3. Resolve the real target path from `PROJECTS.md` or `registry/projects.md`.
4. Switch into the actual repository or ops surface for the task.
5. Promote durable outcomes back into `context/`, `DECISIONS.md`, or `handoffs/`.
