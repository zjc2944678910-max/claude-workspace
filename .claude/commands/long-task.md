---
description: Initialize or resume a long-task run directory for multi-slice work
---

Determine whether the current task needs a long-task run directory.

## Escalation triggers (any one → use long-task)

- Multiple implementation slices identified
- Cross-module or cross-repo scope
- More than 2 continuation or recovery turns expected
- Worker returned "needs_fix" and repair loop started
- Verification failure requiring structured tracking

## If starting new

1. Run: `bash tools/long-task-init.sh --project <slug> --task "<goal>"`
2. Fill `00-request.md`: exact goal, constraints, route evidence
3. Fill `01-context.md`: risk level, route lock, confirmed facts
4. Break work into slices in `02-plan.md`
5. Begin first slice, update `03-ledger.md`

## If resuming

1. Find the existing run directory under `scratch/runs/`
2. Read `03-ledger.md` for current state
3. Read `04-decisions.md` for binding constraints
4. Check git status for uncommitted changes
5. Continue from the last non-terminal slice

## Reference

- Template details: `context/templates/long-task-run.md`
- Risk levels: `.claude/rules/15-risk-levels.md`
- Agent roles: `context/agent-roles.md`
