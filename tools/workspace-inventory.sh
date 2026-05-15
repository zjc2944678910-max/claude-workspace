#!/usr/bin/env bash
# workspace-inventory.sh - read-only inventory for claude-workspace and global Claude state.
# Usage: bash tools/workspace-inventory.sh

set -euo pipefail
cd "$(dirname "$0")/.."

ROOT="$(pwd)"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"

section() {
  echo ""
  echo "-- $1 --"
}

print_size() {
  local path="$1"
  if [ -e "$path" ]; then
    du -sh "$path" 2>/dev/null || true
  else
    echo "(missing) $path"
  fi
}

count_files() {
  local path="$1"
  if [ -d "$path" ]; then
    find "$path" -type f 2>/dev/null | wc -l | tr -d ' '
  else
    echo "0"
  fi
}

echo "========================================"
echo " claude-workspace inventory (read-only)"
echo "========================================"
echo "Workspace: $ROOT"
echo "Claude home: $CLAUDE_HOME"

section "SIZE"
print_size "$ROOT"
print_size "$ROOT/.claude"
print_size "$ROOT/context"
print_size "$ROOT/scratch"
print_size "$ROOT/inbox"
print_size "$ROOT/handoffs"
print_size "$ROOT/archive"
print_size "$CLAUDE_HOME"
print_size "$CLAUDE_HOME/projects"

section "GIT STATUS"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  status="$(git status --short)"
  if [ -n "$status" ]; then
    printf "%s\n" "$status"
  else
    echo "(clean)"
  fi
else
  echo "(not a git worktree)"
fi

section "TRACKED FILES"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git ls-files | wc -l | tr -d ' '
  echo " tracked files"
else
  echo "(not available)"
fi

section "UNTRACKED FILES"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  untracked="$(git ls-files --others --exclude-standard)"
  if [ -n "$untracked" ]; then
    printf "%s\n" "$untracked" | sed -n '1,80p'
  else
    echo "(none)"
  fi
else
  echo "(not available)"
fi

section "IGNORED FILES"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  ignored="$(git status --short --ignored)"
  ignored="$(printf "%s\n" "$ignored" | sed -n 's/^!! //p')"
  if [ -n "$ignored" ]; then
    printf "%s\n" "$ignored" | sed -n '1,80p'
  else
    echo "(none)"
  fi
else
  echo "(not available)"
fi

section "SCRATCH"
echo "$(count_files "$ROOT/scratch") files"
if [ -d "$ROOT/scratch" ]; then
  find "$ROOT/scratch" -maxdepth 3 -type f 2>/dev/null | sort | sed -n '1,80p'
fi

section "INBOX"
echo "$(count_files "$ROOT/inbox") files"
if [ -d "$ROOT/inbox" ]; then
  find "$ROOT/inbox" -maxdepth 3 -type f 2>/dev/null | sort | sed -n '1,80p'
fi

section "HANDOFFS"
echo "$(count_files "$ROOT/handoffs") files"
if [ -d "$ROOT/handoffs" ]; then
  find "$ROOT/handoffs" -maxdepth 3 -type f 2>/dev/null | sort | sed -n '1,80p'
fi

section "GLOBAL CLAUDE PROJECT HISTORY"
if [ -d "$CLAUDE_HOME/projects" ]; then
  echo "$(find "$CLAUDE_HOME/projects" -type f -name '*.jsonl' 2>/dev/null | wc -l | tr -d ' ') jsonl session files"
  du -sh "$CLAUDE_HOME/projects"/* 2>/dev/null | sort -hr | sed -n '1,20p'
else
  echo "(missing)"
fi

section "NOTES"
echo "- This script is read-only."
echo "- Use context/templates/cleanup-manifest.md before deleting or archiving material."
echo "- Prefer ask over delete-candidate when ownership or durability is unclear."
