@PROJECTS.md
@registry/paths.md
@registry/hosts.md

# Claude Workspace

Coordination root. Not a product repo. Real code lives in paths from `PROJECTS.md`.

## Core Rules

- Resolve project path from `PROJECTS.md` or `registry/project-registry.json` before editing product code.
- Read `context/projects/<slug>.md` only when the task needs that project's context.
- Verify before claiming: paths, runtime state, root causes, internal behavior. Say `不确定` if unverified.
- Separate confirmed facts / inferences / open questions. Never present guesses as facts.
- Risk levels enforced by `tools/workspace-guard.py` hook. See `.claude/rules/15-risk-levels.md`.
- Codex delegation only when user explicitly asks. Otherwise Claude implements directly.

## Environment Boundaries

- Distinguish: Cowork shell / host macOS / connected workspace.
- Host-only paths (macOS temp, GUI state, Finder) unreachable from shell unless verified.
- File-centric tasks → move into workspace. GUI tasks → computer-use.

## Memory & Closeout

- Durable facts → `context/`. Daily notes → `DAILY.md`. Decisions → `DECISIONS.md`.
- Disposable → `scratch/`. Imports → `inbox/`.
- Session closeout: promote durable notes, create handoff if needed, cleanup manifest before deleting.

## Worker Delegation

- Use `worker-delegate` MCP for bounded implementation and file reading/summarization.
- Tiers: light → default → strong → complex → hardest (gpt-5.5).
- Use `read_and_summarize` to offload large file reads to worker (saves Claude context).
- See `context/agent-roles.md` for role definitions, `context/daily-workflow.md` for decision tree.

## Commands

`grounded-answer` · `choose-execution-surface` · `workspace-health` · `session-closeout` · `workspace-inventory` · `cleanup-manifest` · `delegate-task` · `long-task`

## graphify

Knowledge graph at `graphify-out/`. Use `graphify query/path/explain` for cross-module questions before grep. Run `graphify update .` after code changes.
