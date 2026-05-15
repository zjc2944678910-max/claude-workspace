---
description: End a substantial Claude session with memory, handoff, and cleanup checks
disable-model-invocation: true
---

Run a lightweight session closeout.

Checklist:

1. Review the user goal and current verification state.
2. Update `DAILY.md` for current-day context only.
3. Promote stable facts into `context/` or lasting decisions into `DECISIONS.md`.
4. Create a handoff under `handoffs/` only if another session or tool needs it.
5. Inspect `scratch/` and `inbox/` for leftover raw or temporary material.
6. If cleanup is useful, create a conservative manifest using `context/templates/cleanup-manifest.md`.
7. Do not delete or move material during closeout unless the user explicitly approves that separate action.

Useful checks:

- `bash tools/workspace-health.sh`
- `bash tools/workspace-inventory.sh`
