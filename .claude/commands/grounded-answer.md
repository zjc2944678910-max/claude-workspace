---
description: Answer with evidence first, separate confirmed facts from inference, and avoid hallucination
disable-model-invocation: true
---

Use a verification-first answer.

Checklist:

1. Do not guess missing facts.
2. Verify from one or more of:
   - local files
   - command output
   - logs
   - official docs
3. Separate the answer into:
   - confirmed facts
   - unconfirmed or inferred items
   - next verification step
4. If the question involves paths, runtime state, internal behavior, root cause, or permissions, say `不确定` when evidence is missing.
5. If earlier assistant text may be wrong, correct it directly instead of building on it.
6. If environment reachability matters, state whether you mean:
   - Cowork shell / VM
   - host macOS
   - connected workspace
