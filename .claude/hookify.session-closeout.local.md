---
name: session-closeout-reminder
trigger: stop
description: Remind to run session closeout after substantial work
---

# Session Closeout Reminder

When a session involved substantial work (multiple file edits, L1+ tasks, or diagnostic work):

1. Run `/session-closeout` before ending
2. Update `DAILY.md` with today's session notes
3. Promote stable facts to `context/` or `DECISIONS.md`
4. If another session/tool needs context, create handoff in `handoffs/claude-to-codex/` or `handoffs/codex-to-claude/`
5. Check `scratch/` for material worth promoting or cleaning

Skip for L0 tiny tasks (single questions, typo fixes).
