#!/usr/bin/env bash
# long-task-init.sh — Initialize a long-task run directory under scratch/runs/.
#
# Usage: bash tools/long-task-init.sh --project <slug> --task "<goal>"
#
# Creates: scratch/runs/<slug>-<YYYY-MM-DD>/
#   00-request.md       goal, constraints, route evidence
#   01-context.md       risk level, route lock, confirmed facts
#   02-plan.md          strategy, ordered slices
#   03-ledger.md        slice IDs and statuses
#   04-decisions.md     reusable decisions for this task
#   05-summary.md       final outcome (filled at end)

set -euo pipefail
cd "$(dirname "$0")/.."

# ── Parse arguments ──────────────────────────────────────────────────────────
PROJECT=""
TASK=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2 ;;
    --task) TASK="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [ -z "$PROJECT" ] || [ -z "$TASK" ]; then
  echo "Usage: bash tools/long-task-init.sh --project <slug> --task \"<goal>\""
  exit 1
fi

# ── Create run directory ─────────────────────────────────────────────────────
DATE=$(date +%Y-%m-%d)
RUN_DIR="scratch/runs/${PROJECT}-${DATE}"

if [ -d "$RUN_DIR" ]; then
  # Append counter if same project+date already exists
  COUNTER=2
  while [ -d "${RUN_DIR}-${COUNTER}" ]; do
    COUNTER=$((COUNTER + 1))
  done
  RUN_DIR="${RUN_DIR}-${COUNTER}"
fi

mkdir -p "$RUN_DIR"

# ── Generate state files ─────────────────────────────────────────────────────

cat > "$RUN_DIR/00-request.md" << EOF
# Request

- **Project**: ${PROJECT}
- **Task**: ${TASK}
- **Created**: ${DATE}

## Constraints

(fill in)

## Route Evidence

(fill in: how was this project identified)
EOF

cat > "$RUN_DIR/01-context.md" << EOF
# Context

## Risk Level

(L0/L1/L2/L3 + rationale)

## Route Lock

- target_project: ${PROJECT}
- target_surface: (fill in)
- project_root: (fill in)
- forbidden_surfaces: (fill in)

## Confirmed Facts

(fill in as you learn)

## Hypotheses

(fill in — separate from confirmed facts)
EOF

cat > "$RUN_DIR/02-plan.md" << EOF
# Plan

## Strategy

(brief approach)

## Slices

| ID | Description | Owner | Status |
|----|-------------|-------|--------|
| T01 | | | pending |
EOF

cat > "$RUN_DIR/03-ledger.md" << EOF
# Ledger

Track slice progress. Statuses: pending → implementing → verifying → done | needs_fix | blocked

| Slice | Status | Result | Notes |
|-------|--------|--------|-------|
| T01 | pending | | |
EOF

cat > "$RUN_DIR/04-decisions.md" << EOF
# Decisions

Reusable facts and decisions for this task. Future slices must honor these.

(fill in as confirmed facts accumulate)
EOF

cat > "$RUN_DIR/05-summary.md" << EOF
# Summary

(fill in at task completion)

## Changed Files

## Verification

## Residual Risks

## Next Steps
EOF

echo "Long-task run directory created: ${RUN_DIR}"
echo "Files: 00-request.md through 05-summary.md"
echo "Next: fill in 00-request.md and 01-context.md before starting work."
