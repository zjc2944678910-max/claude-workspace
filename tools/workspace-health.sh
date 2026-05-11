#!/usr/bin/env bash
# workspace-health.sh — read-only health check for claude-workspace project index consistency.
# Checks: active project paths exist, project set is consistent across docs, stale references absent.
# Usage: bash tools/workspace-health.sh

set -euo pipefail
cd "$(dirname "$0")/.."

CONFIRMED=()
DRIFT=()
MISSING=()
STALE=()

# ── 1. Canonical active project set ──────────────────────────────────────────
ACTIVE_PROJECTS=(OpenClaw "NAS Platform" "Telegram Dual Relay" "MathorCup-D")
ACTIVE_SLUGS=(openclaw nas-platform telegram-dual-relay mathorcup-d)

# ── 2. Check project paths exist ─────────────────────────────────────────────
check_path() {
  local label="$1" path="$2"
  if [ -e "$path" ]; then
    CONFIRMED+=("path exists: $label -> $path")
  else
    MISSING+=("path missing: $label -> $path")
  fi
}

check_path "OpenClaw"    "/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/products/openclaw/nas-openclaw-v22"
check_path "NAS Platform" "/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/infrastructure/nas-platform"
check_path "Telegram Dual Relay" "/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/infrastructure/telegram-dual-relay"
check_path "MathorCup-D" "/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/products/MathorCup_D_repo"

# ── 3. Check PROJECTS.md lists all active projects ───────────────────────────
for proj in "${ACTIVE_PROJECTS[@]}"; do
  if rg -q "$proj" PROJECTS.md 2>/dev/null; then
    CONFIRMED+=("PROJECTS.md contains: $proj")
  else
    DRIFT+=("PROJECTS.md missing: $proj")
  fi
done

# ── 4. Check registry/projects.md lists all active projects ──────────────────
for proj in "${ACTIVE_PROJECTS[@]}"; do
  if rg -q "$proj" registry/projects.md 2>/dev/null; then
    CONFIRMED+=("registry/projects.md contains: $proj")
  else
    DRIFT+=("registry/projects.md missing: $proj")
  fi
done

# ── 5. Check context/projects/*.md cards exist for each active project ───────
for slug in "${ACTIVE_SLUGS[@]}"; do
  if [ -f "context/projects/${slug}.md" ]; then
    CONFIRMED+=("context/projects/${slug}.md exists")
  else
    MISSING+=("context/projects/${slug}.md missing")
  fi
done

# ── 6. Check for stale retired-project references in active entrypoint docs ──
ACTIVE_DOCS=(README.md PROJECTS.md CLAUDE.md registry/projects.md registry/tools.md registry/paths.md context/README.md)
for doc in "${ACTIVE_DOCS[@]}"; do
  if [ -f "$doc" ]; then
    matches=$(rg -ic 'qigate|QiGate' "$doc" 2>/dev/null || true)
    if [ "$matches" -gt 0 ] 2>/dev/null; then
      STALE+=("stale retired-project reference in $doc ($matches occurrence(s))")
    fi
  fi
done

# Also check active project notes
for slug in "${ACTIVE_SLUGS[@]}"; do
  f="context/projects/${slug}.md"
  if [ -f "$f" ]; then
    matches=$(rg -ic 'qigate|QiGate' "$f" 2>/dev/null || true)
    if [ "$matches" -gt 0 ] 2>/dev/null; then
      STALE+=("stale retired-project reference in $f ($matches occurrence(s))")
    fi
  fi
done

# ── Output ───────────────────────────────────────────────────────────────────
echo "========================================"
echo " claude-workspace health check"
echo "========================================"
echo ""

echo "── CONFIRMED (${#CONFIRMED[@]}) ──"
if [ ${#CONFIRMED[@]} -gt 0 ]; then
  for item in "${CONFIRMED[@]}"; do echo "  ✓ $item"; done
else
  echo "  (none)"
fi
echo ""

echo "── DRIFT (${#DRIFT[@]}) ──"
if [ ${#DRIFT[@]} -gt 0 ]; then
  for item in "${DRIFT[@]}"; do echo "  ✗ $item"; done
else
  echo "  (none)"
fi
echo ""

echo "── MISSING (${#MISSING[@]}) ──"
if [ ${#MISSING[@]} -gt 0 ]; then
  for item in "${MISSING[@]}"; do echo "  ✗ $item"; done
else
  echo "  (none)"
fi
echo ""

echo "── STALE REFERENCES (${#STALE[@]}) ──"
if [ ${#STALE[@]} -gt 0 ]; then
  for item in "${STALE[@]}"; do echo "  ✗ $item"; done
else
  echo "  (none)"
fi
echo ""

# Exit code: non-zero if any drift, missing, or stale
if [ ${#DRIFT[@]} -eq 0 ] && [ ${#MISSING[@]} -eq 0 ] && [ ${#STALE[@]} -eq 0 ]; then
  echo "Result: ALL CHECKS PASSED"
  exit 0
else
  echo "Result: ISSUES FOUND"
  exit 1
fi
