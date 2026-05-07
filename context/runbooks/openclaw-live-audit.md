# OpenClaw Live Audit Runbook

## Trigger

Use this runbook for OpenClaw, NAS, live, production, timeout, slow-reply, or performance-investigation tasks.

## Default Mode

- Read-only audit
- No repairs, restarts, or config edits without explicit approval

## Procedure

1. Confirm the target surface:
   - mainline repo
   - migration reference
   - ops surface
   - live host `oc-nas`
2. Gather read-only evidence from the relevant surfaces.
3. Separate findings into:
   - confirmed facts
   - hypotheses
   - risks
   - next checks
4. If repair is requested later, create a repair plan before changing anything.
