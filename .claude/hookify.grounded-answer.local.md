---
name: grounded-answer-pattern
trigger: prompt
description: Use verification-first pattern for diagnostic and root-cause questions
---

# Grounded Answer Pattern

When question is diagnostic (why, root cause, 为什么, 根因, 怎么回事, what caused):

1. Do not guess — verify from files, command output, logs, or docs first
2. Structure answer as:
   - 已确认事实
   - 未确认/推测
   - 下一步验证
3. Say `不确定` when evidence is missing
4. If earlier assistant text may be wrong, correct directly

Reference command: `/grounded-answer`
