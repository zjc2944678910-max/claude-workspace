---
description: Promote stable facts from the current session into the right workspace notes
disable-model-invocation: true
---

Review the current session and decide what should be preserved.

Move items as follows:

- stable project facts -> `context/projects/`
- reusable procedures -> `context/runbooks/`
- workflow or architecture decisions -> `DECISIONS.md`
- day-specific notes -> `DAILY.md`
- cross-tool transfer summaries -> `handoffs/` only when another session or tool needs them

Do not copy raw logs or large temporary output into durable notes.
If raw material remains in `inbox/` or disposable output remains in `scratch/`, leave it there or create a cleanup manifest; do not delete it as part of memory promotion.
