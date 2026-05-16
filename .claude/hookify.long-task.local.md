---
name: long-task-suggestion
trigger: prompt
description: Suggest long-task run directory for multi-step work
disabled: true
---

# Long Task Suggestion

When a task has these signals, suggest initializing a long-task run directory:

- Multiple implementation slices identified
- Cross-repo or cross-module scope
- 2+ continuation or recovery turns expected
- Worker returns needs_fix and repair loop starts

Command:
```bash
bash tools/long-task-init.sh --project <slug> --task "<goal>"
```

Creates structured tracking in `scratch/runs/<slug>-<date>/` with plan, ledger, decisions, and summary files.

Template reference: `context/templates/long-task-run.md`
