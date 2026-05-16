---
name: runbook-reference
trigger: prompt
description: Surface relevant runbook when live/audit/deploy keywords detected
disabled: true
---

# Runbook Reference

When task involves these keywords, read the matching runbook before acting:

| Keywords | Runbook |
|----------|---------|
| openclaw, live audit, oc-nas, 线上检查 | `context/runbooks/openclaw-live-audit.md` |
| deploy, 部署, release, 发版 | `context/runbooks/deployment-checklist.md` |
| slow reply, timeout, 超时, 响应慢, performance | `context/runbooks/slow-reply-triage.md` |

Read the runbook first. Follow its checklist. Don't reinvent the diagnostic steps.
