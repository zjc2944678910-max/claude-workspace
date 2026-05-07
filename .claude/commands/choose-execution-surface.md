---
description: Decide whether a task belongs to the Cowork shell, the host Mac, or the connected workspace before acting
disable-model-invocation: true
---

Choose the execution surface before proposing commands or file actions.

Checklist:

1. Identify the target surface:
   - Cowork shell / VM
   - host macOS
   - connected workspace
2. Do not assume host-only paths are reachable from the Cowork shell.
3. If the task depends on GUI apps, Finder state, browser state, macOS temp paths, or the real Terminal, treat it as host-side unless verified otherwise.
4. If the task is file-centric and the file can be moved, prefer moving it into the connected workspace.
5. State the chosen surface explicitly before giving commands.
