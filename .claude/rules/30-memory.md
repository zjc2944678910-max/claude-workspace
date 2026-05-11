# Memory Rules

- `context/` stores durable project knowledge.
- `DAILY.md` stores current-session or current-day notes.
- `DECISIONS.md` stores lasting workflow decisions.
- `inbox/` is for unprocessed imports.
- `scratch/` is for disposable output, not durable memory.
- Generated indexes, inventories, bulk audits, and one-off cleanup scripts should stay in `scratch/` unless they are promoted into a concise durable note.
- Project-index edits (adding/removing projects) must be synchronized across `PROJECTS.md`, `registry/projects.md`, and `context/projects/`. Run `tools/workspace-health.sh` to verify consistency after any project-index change.
