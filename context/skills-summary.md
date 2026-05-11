# Claude Code Skills 汇总

最后更新: 2026-05-08

---

## 一、已安装的插件（4 个）

### 1. Caveman — Token 压缩
- **作用**: 压缩输出文字，省 ~65% output token
- **命令**:
  - `/caveman lite` — 轻度压缩，保留完整语法
  - `/caveman full` — 默认模式，省冠词、用短词
  - `/caveman ultra` — 最大压缩，电报风格
  - `/caveman wenyan` — 文言文模式
  - `/caveman stats` — 查看省了多少 token
  - `stop caveman` — 关闭，恢复正常输出
- **使用场景**: 日常对话默认开启。写正式文档或代码注释时关闭
- **状态**: 自动激活，每次会话启动时加载

### 2. Security-guidance — 安全检查
- **作用**: 编辑文件时自动检测安全问题（命令注入、XSS、不安全模式）
- **触发方式**: 自动，在 Edit/Write/MultiEdit 操作前运行检查
- **使用场景**: 编辑 OpenClaw、Telegram Dual Relay 等活跃项目代码时自动生效
- **不需要手动操作**，发现安全问题会自动弹出警告

### 3. Hookify — 事件驱动规则
- **作用**: 用 markdown 文件创建自定义 hook 规则，比传统 rules 更省 token
- **命令**:
  - `/hookify` — 分析对话，自动创建规则
  - `/hookify 别用 rm -rf` — 根据指令创建规则
  - `/hookify:list` — 查看已有规则
  - `/hookify:configure` — 交互式开关规则
  - `/hookify:help` — 帮助文档
- **规则文件**: `.claude/hookify.{名称}.local.md`
- **使用场景**:
  - 阻止危险命令: `/hookify 拦截 rm -rf 操作`
  - 代码质量提醒: `/hookify 编辑 Python 文件时提醒不要用 print 调试`
  - 工作流提醒: `/hookify 停止工作前检查是否跑了测试`

### 4. Commit-commands — Git 工作流
- **作用**: 自动化 git commit/push/PR 流程
- **命令**:
  - `/commit-commands:commit` — 分析 diff，自动提交
  - `/commit-commands:commit-push-pr` — 一键 commit + push + 创建 PR
- **使用场景**: 在 git 仓库目录中（OpenClaw、Telegram Dual Relay、MathorCup-D、NAS platform）使用
- **注意**: 需要在有 `.git` 的目录中使用

---

## 二、内置 Skills（系统自带）

| Skill | 用途 | 使用时机 |
|-------|------|----------|
| `review` | 代码审查 | 提交 PR 前 |
| `security-review` | 安全审查 | 涉及认证、用户输入、API 时 |
| `simplify` | 代码简化 | 重构时检查冗余 |
| `init` | 初始化 CLAUDE.md | 新项目 |
| `claude-api` | Claude API 开发 | 写 Anthropic SDK 代码时 |
| `loop` | 定时循环任务 | 监控、轮询 |
| `update-config` | 修改配置 | 改 settings.json |
| `fewer-permission-prompts` | 减少权限弹窗 | 配置 allowlist |

---

## 三、Anthropic Skills 插件（25 个）

### 开发流程
| Skill | 用途 |
|-------|------|
| `tdd-workflow` | TDD 红绿重构工作流 |
| `e2e-testing` | Playwright E2E 测试 |
| `python-testing` | pytest 测试策略 |
| `codebase-onboarding` | 新项目上手指南 |

### 语言/框架模式
| Skill | 用途 |
|-------|------|
| `frontend-patterns` | React/Next.js 模式 |
| `python-patterns` | Python 惯用写法 |
| `coding-standards` | 通用编码规范 |
| `api-design` | REST API 设计 |
| `database-migrations` | 数据库迁移 |
| `postgres-patterns` | PostgreSQL 优化 |
| `docker-patterns` | Docker 最佳实践 |

### 安全/架构
| Skill | 用途 |
|-------|------|
| `security-review` | 安全审查清单 |
| `architecture-decision-records` | ADR 架构决策记录 |
| `git-workflow` | Git 工作流模式 |

### 效率工具
| Skill | 用途 |
|-------|------|
| `karpathy-guidelines` | 防 LLM 常见错误 |
| `skill-stocktake` | 审计已安装 skills 质量 |
| `consolidate-memory` | 整理 memory 文件 |
| `kanban-board` | 看板 UI 设计 |
| `html-ppt` | HTML 演示文稿 |
| `meeting-notes` | 会议记录模板 |
| `weekly-update` | 周报模板 |
| `schedule` | 定时任务管理 |

---

## 四、Graphify — 代码库知识图谱

- **作用**: 把代码库转成可视化知识图谱，支持 28+ 语言
- **命令**:
  - `graphify build .` — 生成知识图谱
  - `graphify query "问题"` — 自然语言查询
  - `graphify path "A" "B"` — 查找两个概念间的路径
  - `graphify explain "概念"` — 解释某个概念
- **输出**: `graphify-out/` 目录下的 HTML 图、Markdown 报告
- **使用场景**: 理解 OpenClaw、Telegram Dual Relay、MathorCup-D 等活跃代码库结构时
- **特点**: 代码本地解析，不发 API；修改代码后运行 `graphify update .` 保持图谱最新

---

## 五、自定义 Commands（6 个）

| 命令 | 用途 |
|------|------|
| `/audit-openclaw` | OpenClaw 只读审计 |
| `/choose-execution-surface` | 判断用哪个执行环境 |
| `/grounded-answer` | 验证优先的回答格式 |
| `/handoff-summary` | 生成交接摘要 |
| `/inspect-project` | 检查注册项目 |
| `/update-memory` | 更新 workspace 记忆 |

---

## 六、常用组合工作流

### 日常开发
1. Caveman full 模式默认开启
2. 切到项目目录
3. `/commit-commands:commit` 提交变更

### 新项目上手
1. `graphify build .` 生成知识图谱
2. `codebase-onboarding` 生成上手指南
3. `/inspect-project` 注册到 workspace

### 代码审查
1. `review` 审查代码质量
2. `security-review` 安全检查
3. `hookify` 设置防犯规则

### 安全审计
1. `/audit-openclaw` OpenClaw 只读审计
2. Security-guidance 自动检查编辑中的安全问题
3. `security-review` 全面安全审查
