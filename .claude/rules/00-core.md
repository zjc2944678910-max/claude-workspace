# Core Workspace Rules

- 验证优先、事实与推断分离、环境可达性判断——遵循 workspace CLAUDE.md 中的完整规则。
- 本目录是协调面，不是产品仓库；编辑代码前先从 `PROJECTS.md` 解析真实项目路径。
- 稳定知识写入 `context/`，不要只依赖 auto memory。
- **Project-index sync rule**: when adding, removing, or renaming a project, update all of `PROJECTS.md`, `registry/projects.md`, `registry/project-registry.json`, and `context/projects/*.md` in the same change, then verify with `tools/workspace-health.sh`.
