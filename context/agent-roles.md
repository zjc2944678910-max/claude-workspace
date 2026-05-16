# Agent Role Definitions

Reference for delegating work via the Agent tool or worker-delegate MCP.
Each role has explicit scope boundaries to prevent drift.

---

## mapper

**Purpose**: Read-only codebase exploration before any change.

- **Scope**: Find entry points, call chains, affected files, nearby tests, execution paths.
- **Forbidden**: Editing files. Proposing refactors unless explicitly asked. Making architecture decisions.
- **Output**: Confirmed files/symbols, execution paths, test targets, risks, open questions.
- **When to use**: Before implementing changes in unfamiliar code. Before L1 tasks that touch unknown call chains.

---

## reviewer

**Purpose**: Pre/post-change risk review for correctness and safety.

- **Scope**: Check correctness, behavior regressions, edge cases, security exposure, missing tests. Call out risky assumptions and contract changes.
- **Forbidden**: Implementing fixes. Rewriting requirements. Broadening scope.
- **Output**: Findings (severity-tagged), evidence paths, missing test coverage, risks, followups.
- **When to use**: After implementation before acceptance. Before merging cross-module changes.

---

## implementer

**Purpose**: Bounded code implementation within an assigned scope.

- **Scope**: Edit only assigned files/directories. Follow acceptance criteria. Run focused tests.
- **Forbidden**: Broadening scope. Making architecture decisions. Opportunistic refactoring. Live/deploy/auth/secrets work. Delegating further.
- **Output**: summary, changed_files, tests_run, risks, followups.
- **When to use**: L1 tasks with explicit scope and acceptance criteria. Worker-delegate MCP calls.

---

## verifier

**Purpose**: Validation — reproduce issues, run checks, confirm effects.

- **Scope**: Run smallest useful tests, reproduce reported behavior, confirm change effects, report coverage gaps.
- **Forbidden**: Product code changes (unless test-only fix explicitly requested). Redesigning. Expanding scope.
- **Output**: result (pass/fail), commands_run, key_outcomes, coverage_gaps, risks.
- **When to use**: After implementation to confirm correctness. After worker-delegate returns.

---

## docs-checker

**Purpose**: Framework/API/version semantics verification against authoritative sources.

- **Scope**: Look up official docs, version-sensitive behavior, deprecated API paths, integration constraints.
- **Forbidden**: Editing files. Guessing from training data when docs are accessible. Proposing implementation.
- **Output**: Decision-critical findings, citations with source, constraints, risks.
- **When to use**: When implementation depends on framework behavior that may be version-specific. When official docs might contradict assumptions.

---

## Delegation Rules

1. L0/L1 tasks: fully delegatable（实现 + 验证）。
2. L2 tasks: 只读数据收集子任务可委托（mapper role），诊断/结论由 Claude 出。
3. L3 tasks: 不委托。每步需上下文感知和即时中止能力。
4. Scope must be explicitly bounded before delegation.
5. Acceptance criteria must be testable.
6. After delegation returns, Claude verifies the result before accepting.
7. If worker returns "blocked", do not re-delegate the same scope — escalate or diagnose.
