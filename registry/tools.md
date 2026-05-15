# Tool Registry

## Local CLI Basics

- `rg`: fast file and text search
- `git status`: inspect repository state before editing
- `ssh oc-nas`: OpenClaw live host entry for read-only audits

## Claude Workspace Shortcuts

- `CLAUDE.md`: root instructions
- `PROJECTS.md`: short project index
- `.claude/commands/audit-openclaw.md`: reusable OpenClaw audit command
- `.claude/commands/inspect-project.md`: project routing command
- `.claude/commands/update-memory.md`: note-promotion command
- `.claude/commands/handoff-summary.md`: summary command
- `.claude/commands/session-closeout.md`: end-of-session memory, handoff, and cleanup checklist
- `.claude/commands/cleanup-manifest.md`: conservative cleanup planning command
- `tools/workspace-health.sh`: read-only project-index consistency check
- `tools/workspace-inventory.sh`: read-only inventory for workspace and global Claude state

## Note

This file is a cheat sheet, not a rule file. Keep behavior rules in `CLAUDE.md` or `.claude/rules/`.
