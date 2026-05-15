---
description: Produce a concise handoff summary for Claude or Codex
disable-model-invocation: true
---

Create a handoff summary with:

- user goal
- confirmed facts
- files or repositories touched
- verification status
- residual risks
- next recommended action

Store durable handoffs under `handoffs/` only when another Claude, Codex, or future session needs the summary.
Do not use handoffs as a substitute for durable project facts; promote stable knowledge into `context/` or `DECISIONS.md`.
