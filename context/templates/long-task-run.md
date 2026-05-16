# Long Task Run Template

## When to Use

Escalate to a long-task run directory when:
- Task spans multiple implementation slices
- More than 2 continuation or recovery turns needed
- Worker repair loop starts (needs_fix cycle)
- Cross-module or cross-repo scope
- Verification failure requiring structured tracking

## Initialization

```bash
bash tools/long-task-init.sh --project <slug> --task "<goal>"
```

Creates `scratch/runs/<slug>-<date>/` with 6 state files.

## Run Directory Structure

| File | Purpose | When to fill |
|------|---------|--------------|
| `00-request.md` | Exact goal, user constraints, route evidence | Before starting |
| `01-context.md` | Risk level, route lock, confirmed facts vs hypotheses | Before starting |
| `02-plan.md` | Strategy, ordered slices, owned scope per slice | After initial exploration |
| `03-ledger.md` | Slice IDs, statuses, brief results | Updated per slice |
| `04-decisions.md` | Confirmed facts future slices must honor | Accumulated during work |
| `05-summary.md` | Final outcome, changed files, verification, risks | At completion |

## Ledger State Machine

```
pending → implementing → verifying → done
                      ↘ needs_fix → implementing (max 3 loops → blocked)
```

Terminal states: `done`, `blocked`, `deferred`

## Rules

- Max 3 repair loops per slice before marking `blocked`
- Route Lock fields must be filled before implementation starts
- New evidence pointing outside Route Lock → stop as blocked, don't switch silently
- Decisions in `04-decisions.md` are binding for subsequent slices
- After interruption/compaction: reconstruct state from `03-ledger.md` + `04-decisions.md` + git status

## Closing Out

When all slices reach terminal state:
1. Fill `05-summary.md` with changed files, verification, residual risks
2. Promote any durable decisions into `context/` or `DECISIONS.md`
3. Run `bash tools/workspace-health.sh` if project routing changed
