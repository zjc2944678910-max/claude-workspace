---
description: Prepare a bounded delegation brief for worker-delegate or Agent tool
---

Build a delegation brief from the current task context.

## Pre-delegation checklist

- [ ] Risk level is L0 or L1 (never delegate L2/L3)
- [ ] Target project and scope are explicitly identified
- [ ] Acceptance criteria are concrete and testable
- [ ] No live/deploy/auth/secrets surface involved

## Brief structure

1. **Task**: one-sentence bounded goal
2. **Role**: mapper | reviewer | implementer | verifier | docs-checker (see `context/agent-roles.md`)
3. **CWD**: absolute path to the working directory
4. **Scope hint**: owned files/directories, plus forbidden surfaces
5. **Acceptance criteria**: concrete pass conditions
6. **Constraints**: forbidden actions, max file count, risk level, route lock if applicable
7. **Output format**: summary, changed_files, tests_run, risks, followups

## After delegation

- Verify the result against acceptance criteria
- Check changed files for correctness and safety
- If worker returns "blocked" or "needs_fix", diagnose before re-delegating
- Do not accept unverified worker output as final
