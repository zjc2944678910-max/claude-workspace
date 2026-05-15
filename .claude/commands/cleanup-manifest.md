---
description: Create a conservative cleanup manifest without deleting or moving files
disable-model-invocation: true
---

Create a cleanup manifest from `context/templates/cleanup-manifest.md`.

Rules:

1. Inspect candidate files and directories before classifying them.
2. Use four buckets: keep, archive, delete-candidate, ask.
3. Prefer `ask` when ownership, durability, or safety is unclear.
4. Do not delete, move, or rewrite files while creating the manifest.
5. Put generated manifests in `scratch/plans/` unless the user requests another location.

Recommended evidence:

- `git status --short`
- `bash tools/workspace-inventory.sh`
- `find scratch inbox handoffs -maxdepth 3 -type f`
