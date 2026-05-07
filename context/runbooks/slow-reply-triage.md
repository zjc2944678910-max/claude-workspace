# Slow Reply Triage

## Goal

Create a consistent first pass for slow-reply, timeout, or degraded-responsiveness reports.

## Checklist

1. Confirm which surface is slow:
   - client UI
   - API
   - background worker
   - live host or infra
2. Capture the time window and symptoms.
3. Collect read-only evidence:
   - local repository clues
   - ops notes or evidence bundles
   - live health or logs when authorized for read-only access
4. Separate:
   - confirmed bottlenecks
   - suspected causes
   - missing evidence
5. Recommend the smallest next check before any repair action.
