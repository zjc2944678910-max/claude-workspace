#!/usr/bin/env bash
# session-audit.sh — Automated workspace health audit for session closeout.
# Checks memory promotion, context freshness, and scratch hygiene.
# Output: HEALTHY / STALE / INCOMPLETE per category.

set -euo pipefail

WORKSPACE_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TODAY=$(date +%Y-%m-%d)
ISSUES=0

echo "=== Session Audit ($TODAY) ==="
echo ""

# ── 1. DAILY.md freshness ───────────────────────────────────────────────────

echo "── DAILY.md"
DAILY="$WORKSPACE_ROOT/DAILY.md"
if [ ! -f "$DAILY" ]; then
    echo "  INCOMPLETE: DAILY.md does not exist"
    ISSUES=$((ISSUES + 1))
elif grep -q "$TODAY" "$DAILY" 2>/dev/null; then
    echo "  HEALTHY: has today's date ($TODAY)"
else
    echo "  STALE: no entry for today"
    ISSUES=$((ISSUES + 1))
fi

# ── 2. DECISIONS.md freshness ───────────────────────────────────────────────

echo ""
echo "── DECISIONS.md"
DECISIONS="$WORKSPACE_ROOT/DECISIONS.md"
if [ ! -f "$DECISIONS" ]; then
    echo "  INCOMPLETE: DECISIONS.md does not exist"
    ISSUES=$((ISSUES + 1))
else
    LAST_DATE=$(grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' "$DECISIONS" | tail -1)
    if [ -z "$LAST_DATE" ]; then
        echo "  STALE: no dated entries found"
        ISSUES=$((ISSUES + 1))
    else
        DAYS_AGO=$(( ($(date -j -f "%Y-%m-%d" "$TODAY" +%s 2>/dev/null || date -d "$TODAY" +%s) - $(date -j -f "%Y-%m-%d" "$LAST_DATE" +%s 2>/dev/null || date -d "$LAST_DATE" +%s)) / 86400 ))
        if [ "$DAYS_AGO" -gt 7 ]; then
            echo "  STALE: last entry is $LAST_DATE ($DAYS_AGO days ago)"
            ISSUES=$((ISSUES + 1))
        else
            echo "  HEALTHY: last entry $LAST_DATE ($DAYS_AGO days ago)"
        fi
    fi
fi

# ── 3. Project notes completeness ──────────────────────────────────────────

echo ""
echo "── Project Notes"
REGISTRY="$WORKSPACE_ROOT/registry/project-registry.json"
if [ -f "$REGISTRY" ]; then
    SLUGS=$(python3 -c "
import json
with open('$REGISTRY') as f:
    data = json.load(f)
for p in data.get('projects', []):
    print(p['slug'])
" 2>/dev/null || true)

    for slug in $SLUGS; do
        NOTE="$WORKSPACE_ROOT/context/projects/$slug.md"
        if [ ! -f "$NOTE" ]; then
            echo "  INCOMPLETE: missing context/projects/$slug.md"
            ISSUES=$((ISSUES + 1))
        elif grep -qi "fill in\|TODO\|placeholder" "$NOTE" 2>/dev/null; then
            echo "  INCOMPLETE: $slug.md still has placeholder content"
            ISSUES=$((ISSUES + 1))
        else
            echo "  HEALTHY: $slug.md"
        fi
    done
else
    echo "  SKIP: registry/project-registry.json not found"
fi

# ── 4. Scratch hygiene ──────────────────────────────────────────────────────

echo ""
echo "── Scratch Hygiene"
SCRATCH="$WORKSPACE_ROOT/scratch"
if [ -d "$SCRATCH" ]; then
    OLD_FILES=$(find "$SCRATCH" -maxdepth 2 -type f -mtime +7 ! -path "*/delegation-log.jsonl" ! -path "*/.gitkeep" 2>/dev/null | head -10)
    OLD_COUNT=$(echo "$OLD_FILES" | grep -c . 2>/dev/null || echo 0)
    if [ "$OLD_COUNT" -gt 0 ]; then
        echo "  STALE: $OLD_COUNT files older than 7 days:"
        echo "$OLD_FILES" | while read -r f; do
            echo "    - ${f#$WORKSPACE_ROOT/}"
        done
        ISSUES=$((ISSUES + 1))
    else
        echo "  HEALTHY: no old files"
    fi
else
    echo "  HEALTHY: scratch/ does not exist"
fi

# ── 5. Unfinished long-task runs ────────────────────────────────────────────

echo ""
echo "── Long-Task Runs"
RUNS_DIR="$SCRATCH/runs"
if [ -d "$RUNS_DIR" ]; then
    UNFINISHED=0
    for ledger in "$RUNS_DIR"/*/03-ledger.md; do
        [ -f "$ledger" ] || continue
        if grep -qiE "pending|implementing|in.progress" "$ledger" 2>/dev/null; then
            RUN_DIR=$(dirname "$ledger")
            echo "  INCOMPLETE: ${RUN_DIR#$WORKSPACE_ROOT/} has unfinished slices"
            UNFINISHED=$((UNFINISHED + 1))
        fi
    done
    if [ "$UNFINISHED" -eq 0 ]; then
        echo "  HEALTHY: no unfinished runs"
    else
        ISSUES=$((ISSUES + UNFINISHED))
    fi
else
    echo "  HEALTHY: no runs directory"
fi

# ── Summary ─────────────────────────────────────────────────────────────────

echo ""
echo "=== Summary ==="
if [ "$ISSUES" -eq 0 ]; then
    echo "All checks HEALTHY."
else
    echo "$ISSUES issue(s) found. Address before closing session."
fi

exit "$( [ "$ISSUES" -eq 0 ] && echo 0 || echo 1 )"
