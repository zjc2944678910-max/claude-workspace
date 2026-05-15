# Workspace Model

## Role Split

- `claude-workspace`: Claude Code coordination root for context, planning, audits, and handoffs
- `~/.claude`: global Claude Code state for settings, hooks, plugins, commands, tools, and historical sessions
- `codex-workspace`: Codex-oriented workspace index and broader operator surface
- Real project repositories: where implementation changes actually happen
- Codex delegation from Claude Code: optional implementation handoff only when the user explicitly asks for Codex

## Boundaries

- Workspace notes and project routing belong in `claude-workspace`.
- User-wide Claude behavior belongs in `~/.claude`; changes there affect new Claude Code desktop and CLI sessions.
- Product code belongs in the real project repository selected from `PROJECTS.md` or `registry/projects.md`.
- Scratch output, raw imports, and generated evidence are not durable memory until summarized into `context/`, `DECISIONS.md`, or an intentional handoff.

## Daily Flow

1. Start in `claude-workspace`.
2. Read `CLAUDE.md`.
3. Resolve the real target path from `PROJECTS.md` or `registry/projects.md`.
4. Switch into the actual repository or ops surface for the task.
5. Promote durable outcomes back into `context/`, `DECISIONS.md`, or `handoffs/`.
6. Run a closeout pass for longer sessions: update durable notes, create handoffs only when useful, and use a cleanup manifest before deleting or archiving temporary material.

## Maintenance Checks

- `bash tools/workspace-health.sh`: confirms registered project routing is consistent.
- `bash tools/workspace-inventory.sh`: reports workspace size, git state, scratch/inbox contents, and `~/.claude/projects` volume without modifying files.
