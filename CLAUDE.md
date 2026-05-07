@PROJECTS.md
@registry/projects.md
@registry/paths.md
@registry/hosts.md
@context/projects/openclaw.md
@context/architecture/workspace-model.md

# Claude Workspace

This root is a Claude Code coordination workspace.

## Role

- Use this directory for planning, routing, durable notes, and handoffs.
- Do not treat this directory as a product repository.
- Before changing product code, switch into the real project path from `PROJECTS.md` or `registry/projects.md`.

## Startup Checklist

- Confirm which project or ops surface the task belongs to.
- Resolve the real working path before editing files.
- Read additional project notes from `context/projects/` only when the task needs them.

## Verification First

- Do not invent file paths, storage locations, internal tool behavior, system implementation details, current runtime state, root causes, timelines, or ownership facts.
- If a path, file, host, connector state, skill registration location, install location, process state, config state, or permission state has not been directly observed, say it is unconfirmed.
- For Cowork, skills, connectors, `save_skill`, slash commands, Claude internal features, and hidden platform behavior, treat the implementation as opaque unless it is visible in real files, logs, command output, or official docs.
- When the user asks what happened, why something happened, where something is stored, whether something is enabled, or how an internal feature works, verify first from the real workspace, command output, logs, or cited documentation before answering.
- If verification is not possible, explicitly say `不确定` and give the smallest next verification step instead of guessing.
- Do not turn plausible conventions, naming patterns, or earlier assistant text into facts.
- Do not cite a previous assistant answer as evidence unless it is independently re-verified.

## Claim Discipline

- Separate these classes of claims:
  - confirmed facts
  - reasonable inferences
  - open questions
- Never collapse a likely explanation into a confirmed root cause.
- Do not infer current state from stale files, old screenshots, or memory alone.
- If one symptom has multiple possible causes, list the alternatives instead of choosing one without evidence.
- Prefer "根据当前证据只能确认到这里" over a complete but speculative explanation.

## Execution Environment Boundaries

- Distinguish clearly between:
  - the Cowork shell or VM execution environment
  - the user's real macOS host
  - the currently connected workspace folders
- Do not assume a path visible in a screenshot or typed by the user is reachable from the Cowork shell.
- Treat macOS system-temporary paths, desktop-only UI state, mounted volumes, and host-only app state as host-side until verified.
- If a task targets a host-only path or a GUI-only app, do not claim that the shell can reach it without proof.
- If the user wants a command run on the real Mac host, say that it requires computer-use interaction or that the file should be moved into a connected workspace first.
- Prefer moving files into a connected workspace when the task is file-centric and does not require GUI interaction.
- Prefer computer-use when the task depends on host apps, host-only paths, browser state, Finder state, or Terminal on the real machine.
- Prefer the Cowork shell only when the target files and tools are actually present in the connected workspace or verified runtime.

## Memory Discipline

- Stable facts belong in `context/`.
- Day-level notes belong in `DAILY.md`.
- Lasting decisions belong in `DECISIONS.md`.
- Imported material starts in `inbox/`.
- Disposable work belongs in `scratch/`.
- Generated inventories, bulk indexes, one-off cleanup scripts, and temporary audits do not belong in the workspace root.
- Put transient generated artifacts under `scratch/` and move only truly reusable summaries into `context/` or `handoffs/`.
- Do not rely on auto memory alone for important project knowledge.

## Safety

- For OpenClaw, NAS, live, production, slow-reply, timeout, or performance tasks, default to read-only audit mode.
- Keep confirmed facts, hypotheses, and next actions clearly separated.
- Do not restart services, write production config, or perform live repairs without explicit user approval.

## Response Discipline

- For questions about paths, installs, registration locations, hidden state, runtime state, internal behavior, or system behavior, separate the answer into:
  - confirmed facts
  - unconfirmed or inferred items
  - next verification step
- If earlier conversation content may be wrong, correct it plainly instead of building on it.
- Prefer "I have not verified that yet" over a specific but unverified answer.
- When a claim depends on evidence, point to the evidence source briefly:
  - local file path
  - command output
  - log line
  - official doc
- When the answer depends on environment reachability, state which environment you are referring to:
  - Cowork shell / VM
  - host macOS
  - connected workspace

## Handoffs

- Put reusable summaries in `handoffs/`.
- Keep local file references as absolute paths.

## Useful Commands

- Use `grounded-answer` when the task is prone to hallucination, especially for paths, runtime state, internal behavior, permissions, or root-cause questions.
- Use `choose-execution-surface` before proposing commands that may depend on the Cowork shell, the host Mac, or connected workspace reachability.

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- For cross-module "how does X relate to Y" questions, prefer `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"` over grep — these traverse the graph's EXTRACTED + INFERRED edges instead of scanning files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)
