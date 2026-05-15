# claude-workspace

This directory is a Claude Code-only workspace tree.

Use it as a front desk for planning, context, audits, handoffs, and lightweight project routing. Real code changes should happen in the actual repositories registered here, not in this directory.

This workspace is separate from global Claude Code state in `~/.claude`.
Use this repository for project routing and durable workspace notes; use
`~/.claude` for user-wide Claude Code settings, plugins, hooks, and session
history.

## Quick Start

1. Open `/Users/zhangjincheng/Documents/GitHub/claude-workspace` as the Claude Code working folder.
2. Ask Claude to read `CLAUDE.md`.
3. Let Claude locate the real target repository from `PROJECTS.md` or `registry/projects.md`.
4. When a session produces durable knowledge, promote it into `context/` or `DECISIONS.md`.
5. For any question about paths, storage locations, runtime state, root causes, skills, connectors, or Claude internals, require Claude to verify first and mark unconfirmed items explicitly.
6. For any command, file access, or GUI step, decide first whether it belongs to the Cowork shell, the host Mac, or a connected workspace.
7. Before ending a substantial session, run a lightweight closeout: promote stable facts, write a handoff only when useful, and inspect `scratch/` or `inbox/` for follow-up cleanup.

## Core Files

- `CLAUDE.md`: root instructions Claude should load first
- `PROJECTS.md`: short project index and routing hints
- `DAILY.md`: current working notes
- `DECISIONS.md`: long-lived workflow and architecture decisions
- `.claude/rules/05-grounding.md`: anti-hallucination and verification-first rules for paths, state, causes, and internal behavior
- `tools/workspace-health.sh`: read-only project-index consistency check
- `tools/workspace-inventory.sh`: read-only workspace and global Claude state inventory
- `CLAUDE.md` and `.claude/rules/05-grounding.md`: also define when to use the Cowork shell, when to use host-side computer interaction, and when to move files into the workspace first

## Main Areas

- `.claude/`: Claude-local rules, local settings, and reusable slash commands
- `registry/`: canonical paths, hosts, and tool cheat sheets
- `context/`: project notes, runbooks, architecture notes, and templates
- `inbox/`: imported screenshots, notes, and log snippets waiting to be processed
- `scratch/`: disposable work products, drafts, experiments, and plans
- `handoffs/`: summaries passed between Claude and Codex
- `archive/`: retired notes and old context

## Useful Commands

- `grounded-answer`: force evidence-first answers with confirmed facts, unconfirmed items, and next verification steps
- `choose-execution-surface`: decide whether a task belongs to the Cowork shell, the host Mac, or the connected workspace before proposing commands
- `workspace-health`: verify registered project routing consistency
- `session-closeout`: end a session with memory promotion, handoff, and conservative cleanup checks
- `update-memory`: promote stable facts into the right durable notes
- `handoff-summary`: write a compact transfer summary only when another session or tool needs it
- `cleanup-manifest`: classify cleanup candidates without deleting or moving files

## Maintenance Loop

Run these checks before larger workspace edits, after project-index changes, or
when Claude Code behavior feels stale:

1. `bash tools/workspace-health.sh`
2. `bash tools/workspace-inventory.sh`
3. Review `DAILY.md`, `context/`, `scratch/`, and `inbox/`.
4. If cleanup is needed, create a conservative manifest from `context/templates/cleanup-manifest.md`; do not delete files from the manifest without a separate confirmation.

## Boundaries

- Do not store product source code here.
- Do not store secrets here.
- Do not treat `scratch/` or `inbox/` as durable memory.
- Do not keep generated indexes, temporary audit reports, or one-off cleanup scripts in the workspace root.
- Keep this workspace separate from `/Users/zhangjincheng/Documents/GitHub/codex-workspace`, which remains the Codex-oriented workspace index.
- Keep this workspace separate from `~/.claude`, which controls global Claude Code behavior for new desktop and CLI sessions.
- Codex is optional from Claude Code. Claude should call Codex delegation only when the user explicitly asks for Codex.
