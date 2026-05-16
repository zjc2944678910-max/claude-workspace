---
description: Summarize worker delegation metrics from the log
disable-model-invocation: true
---

Read `scratch/delegation-log.jsonl` and produce a summary:

1. **Total delegations** — count of entries
2. **By tool** — delegate_task vs quick_ask vs read_and_summarize
3. **By status** — ok vs error vs incomplete
4. **By model** — if model field is present, group by model
5. **Token usage** — total tokens_in / tokens_out if available
6. **Recent errors** — last 5 error entries with task_prefix

If the log file doesn't exist or is empty, say so.

Keep output concise — table format preferred.
