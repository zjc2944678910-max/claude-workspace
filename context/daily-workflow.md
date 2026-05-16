# Daily Workflow Decision Tree

Policy source: `CLAUDE.md`. Risk levels: `.claude/rules/15-risk-levels.md`. Agent roles: `context/agent-roles.md`.

---

## Task Classification → Execution Path

```
User request arrives
    │
    ├─ Simple question / lightweight check / typo?
    │   └─ L0 Tiny Fast Path
    │
    ├─ Target project + files + tests explicit, no risky surface?
    │   └─ Small Known-Scope Path
    │
    ├─ Multi-file / unclear routing / cross-module / API route?
    │   └─ Standard Task Path
    │
    └─ Multiple slices / repair loops / cross-repo?
        └─ Long Task Path (use run-directory)
```

---

## L0 Tiny Fast Path

**Use for**: simple questions, single-file edits, typos, lightweight checks, known-answer lookups.

1. Stay at workspace-index level unless user names a specific project
2. Classify in one line (`L0 tiny: <rationale>`), then answer directly
3. Skip: delegation, route lock, workspace-health, structured closeout
4. Verify with smallest relevant check (if any needed)

---

## Small Known-Scope Path

**Use when**: target project, files, tests, and acceptance are explicit; no live/deploy/auth/secrets surface.

1. Read only relevant files (README, target module)
2. Classify: `L0/L1: <rationale>`
3. Implement the scoped change directly
4. Run focused verification (tests, type check, or manual review)
5. Close out concisely: what changed, verification status, residual risk

---

## Standard Task Path

**Use when**: above paths don't fit — multi-file, unclear routing, API routes, deploy/auth surfaces.

1. **Route**: resolve target from `PROJECTS.md` / `registry/project-registry.json`
2. **Classify**: state risk level + rationale before first action
3. **Plan**: brief plan or state approach
4. **Execute**: direct (L0/small L1) or delegate via worker-delegate MCP (broader L1)
5. **Verify**: run tests, type check, or read-only audit (L2)
6. **Close out**: confirmed facts, changes, verification status, risks, next steps

---

## Long Task Path

**Use when**: multiple implementation slices, cross-repo, 2+ continuation turns, worker repair loops.

1. Initialize run directory: `bash tools/long-task-init.sh --project <slug> --task "<goal>"`
2. Fill `00-request.md` and `01-context.md`
3. Break into slices in `02-plan.md`
4. Track progress in `03-ledger.md`
5. Store reusable decisions in `04-decisions.md`
6. Close with `05-summary.md`

See `context/templates/long-task-run.md` for details.

---

## Delegation Decision Matrix

| Situation | Default owner |
|-----------|--------------|
| L0 tiny question or isolated fix | Claude direct |
| Small known-scope L0/L1 | Claude direct |
| L1 with unknown call chain or cross-module risk | worker-delegate (implementer role) |
| Pre-change risk review needed | Agent subagent (reviewer role) |
| Unfamiliar codebase exploration | Agent subagent (mapper role) |
| L2 read-only audit — data collection | worker-delegate (mapper role) |
| L2 read-only audit — diagnosis/conclusion | Claude direct (never delegate) |
| L3 state-changing repair | Claude direct (never delegate) |
| Architecture or safety judgment | Claude direct (never delegate) |

---

## Escalation Triggers

From **L0 tiny** → **L1**:
- Touches multiple modules or shared core logic
- Involves API routes, build/CI, or dependency changes
- Unclear project routing
- Any live/production/deploy/auth/secrets surface

From **Standard** → **Long Task**:
- Multiple implementation slices identified
- Cross-repo or cross-module scope
- 2+ continuation or recovery turns
- Worker returns "needs_fix" and repair loop starts
- Verification failure requiring structured tracking

---

## Token Awareness

- **Simple tasks**: brief answers, no overhead
- **Standard tasks**: keep command output bounded; use `--stat` before full diffs
- **L2 audits**: invest in thorough evidence gathering; store long logs in scratch/
- Evidence pointers (path + line + finding) over pasted content
- Reuse confirmed decisions from DECISIONS.md before re-exploring
