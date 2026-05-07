---
name: default-workspace
description: User's default workspace directory — always use this as the primary working folder
type: feedback
---

用户偏好固定使用 `/Users/zhangjincheng/Documents/GitHub/claude-workspace` 作为工作目录，不想每次都手动选择。

**Why:** 用户觉得每次都要选择目录很麻烦。
**How to apply:** 每次开始工作时，如果用户没有指定其他目录，就使用这个路径。如果 Cowork 需要通过 `request_cowork_directory` 挂载目录，直接传入这个路径。
