#!/usr/bin/env python3
"""
workspace-guard.py — Claude Code hook for workspace policy enforcement.

Adapted from codex-workspace workspace_guard.py for Claude Code's hook system.
Handles: PreToolUse (command classification), UserPromptSubmit (route hints), Stop (closeout).

Usage in .claude/settings.json hooks:
  command: "/usr/bin/python3 tools/workspace-guard.py <event>"
  where <event> is: pre-tool-use | user-prompt-submit | stop
"""

import json
import os
import re
import sys
import time
from pathlib import Path

# ── Configuration ────────────────────────────────────────────────────────────

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = WORKSPACE_ROOT / "registry" / "project-registry.json"
STATE_DIR = Path.home() / ".claude" / "state"
STATE_FILE = STATE_DIR / "claude-workspace-hooks.json"

REPAIR_PHRASE = "进入修复阶段"
REPAIR_TTL_SECONDS = 1800  # 30 minutes

DELEGATION_LOG = WORKSPACE_ROOT / "scratch" / "delegation-log.jsonl"

# ── Long-task signal phrases ────────────────────────────────────────────────

LONG_TASK_SIGNALS = [
    "multiple files", "cross-module", "cross-repo", "repair loop",
    "needs_fix", "phase 2", "phase 3", "continuation", "多个文件",
    "跨模块", "跨仓库", "修复循环", "多步", "multi-step", "multi-slice",
]

# ── Runbook keyword mapping ─────────────────────────────────────────────────

RUNBOOK_MAP = {
    "context/runbooks/openclaw-live-audit.md": [
        "openclaw", "live audit", "oc-nas", "线上检查",
    ],
    "context/runbooks/deployment-checklist.md": [
        "deploy", "部署", "release", "发版",
    ],
    "context/runbooks/slow-reply-triage.md": [
        "slow reply", "timeout", "超时", "响应慢", "performance",
    ],
}

# ── Hard block patterns (immediate deny, never allowed) ──────────────────────

HARD_BLOCK_PATTERNS = [
    r"\brm\s+(-[a-zA-Z]*r[a-zA-Z]*f|--recursive\s+--force|-[a-zA-Z]*f[a-zA-Z]*r)\b",
    r"\brm\s+-rf\b",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+clean\s+-[a-zA-Z]*f\b",
    r"\bgit\s+checkout\s+--\s+\.",
    r"\bfind\b.*\b-delete\b",
    r"\bmkfs\b",
    r"\bdd\s+if=",
    r"\b(curl|wget)\b.*\|\s*(ba)?sh\b",
]

# ── L3 block patterns (need repair authorization) ────────────────────────────

L3_BLOCK_PATTERNS = [
    r"\bsystemctl\s+(restart|stop|start|enable|disable)\b",
    r"\bservice\s+\S+\s+(restart|stop|start)\b",
    r"\bdocker\s+compose\s+(down|rm|stop)\b",
    r"\bdocker\s+(rm|stop|kill)\b",
    r"\bkubectl\s+(apply|delete|rollout|scale)\b",
    r"\bhelm\s+(install|upgrade|uninstall|rollback)\b",
    r"\bterraform\s+(apply|destroy)\b",
    r"\bansible-playbook\b",
    r"\bscp\b.*\boc-nas\b",
    r"\bssh\b.*\boc-nas\b.*\b(rm|mv|cp|systemctl|docker|service)\b",
]

# ── Live/production terms (emit L2 notice) ───────────────────────────────────

LIVE_TERMS = [
    "oc-nas", "openclaw", "production", "prod", "live",
    "deploy", "rollback", "nas-platform",
]

# ── Inspection commands (always pass, never block) ───────────────────────────

INSPECTION_PREFIXES = [
    "cat ", "less ", "head ", "tail ", "grep ", "rg ", "ag ", "ack ",
    "find ", "fd ", "ls ", "tree ", "wc ", "file ", "stat ",
    "git log", "git status", "git diff", "git show", "git branch",
    "git remote", "git stash list", "git blame",
    "echo ", "printf ", "date", "whoami", "hostname", "uname",
    "python3 -c", "node -e", "jq ", "yq ",
    "curl -s", "wget -q",
    "bash tools/workspace-health.sh", "bash tools/workspace-inventory.sh",
    "bash tools/session-audit.sh",
]


# ── State management ─────────────────────────────────────────────────────────

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_state(state):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def is_repair_authorized():
    state = load_state()
    ts = state.get("repair_authorized_at", 0)
    return (time.time() - ts) < REPAIR_TTL_SECONDS


def authorize_repair():
    state = load_state()
    state["repair_authorized_at"] = time.time()
    save_state(state)


def mark_substantive_work():
    state = load_state()
    state["substantive_work"] = True
    save_state(state)


def mark_delegation_used():
    state = load_state()
    state["delegation_used"] = True
    save_state(state)


def get_session_flags():
    state = load_state()
    return state.get("substantive_work", False), state.get("delegation_used", False)


# ── Registry loading ─────────────────────────────────────────────────────────

def load_registry():
    if REGISTRY_PATH.exists():
        try:
            return json.loads(REGISTRY_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {"projects": []}


# ── Command classification ───────────────────────────────────────────────────

def is_inspection_command(cmd):
    cmd_stripped = cmd.strip()
    for prefix in INSPECTION_PREFIXES:
        if cmd_stripped.startswith(prefix):
            return True
    return False


def classify_command(cmd):
    """Returns: ('pass', None) | ('hard_block', reason) | ('l3_block', reason) | ('live_notice', msg)"""
    if is_inspection_command(cmd):
        return ("pass", None)

    for pattern in HARD_BLOCK_PATTERNS:
        if re.search(pattern, cmd):
            return ("hard_block", f"Destructive command blocked: matches pattern `{pattern}`")

    for pattern in L3_BLOCK_PATTERNS:
        if re.search(pattern, cmd):
            if is_repair_authorized():
                return ("pass", None)
            return ("l3_block", f"L3 state-changing command. User must say \"{REPAIR_PHRASE}\" to authorize.")

    for term in LIVE_TERMS:
        if term in cmd.lower():
            return ("live_notice", f"L2 notice: command references live term '{term}'. Ensure read-only intent.")

    return ("pass", None)


# ── Hook handlers ────────────────────────────────────────────────────────────

def handle_pre_tool_use():
    """PreToolUse handler for Bash commands."""
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return

    tool_input = payload.get("tool_input", payload)
    cmd = tool_input.get("command", "")
    if not cmd:
        return

    classification, message = classify_command(cmd)

    if classification == "hard_block":
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "reason": message
            }
        }
        print(json.dumps(output))

    elif classification == "l3_block":
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "reason": message
            }
        }
        print(json.dumps(output))

    elif classification == "live_notice":
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": message
            }
        }
        print(json.dumps(output))

    else:
        if not is_inspection_command(cmd):
            mark_substantive_work()


def handle_user_prompt_submit():
    """UserPromptSubmit handler — emit route hints and detect repair phrase."""
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return

    user_message = payload.get("user_message", payload.get("content", ""))
    if not user_message:
        return

    # Check for repair authorization phrase
    if REPAIR_PHRASE in user_message:
        authorize_repair()
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": f"L3 repair authorized for {REPAIR_TTL_SECONDS // 60} minutes."
            }
        }
        print(json.dumps(output))
        return

    # Route hints from registry
    registry = load_registry()
    hints = []
    msg_lower = user_message.lower()

    for project in registry.get("projects", []):
        keywords = project.get("routing_keywords", [])
        for kw in keywords:
            if kw in msg_lower:
                risk = project.get("risk_profile", "unknown")
                hints.append(f"Route hint: {project['name']} ({risk})")
                break

    # Long-task signal detection (migrated from hookify.long-task.local.md)
    matched_signals = [s for s in LONG_TASK_SIGNALS if s in msg_lower]
    if matched_signals:
        hints.append(
            f"Long-task signals: {', '.join(matched_signals)}. "
            "If not in a run directory, consider: bash tools/long-task-init.sh --project <slug> --task \"<goal>\""
        )

    # Runbook matching (migrated from hookify.runbooks.local.md)
    for runbook_path, keywords in RUNBOOK_MAP.items():
        for kw in keywords:
            if kw in msg_lower:
                hints.append(f"Runbook available: {runbook_path} — read before acting.")
                break

    if hints:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": " | ".join(hints)
            }
        }
        print(json.dumps(output))


def handle_post_tool_use():
    """PostToolUse handler — validate delegation output and log metrics."""
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return

    tool_name = payload.get("tool_name", "")
    tool_output = payload.get("tool_output", payload.get("response", ""))

    delegation_tools = {"delegate_task", "quick_ask", "read_and_summarize"}
    if tool_name not in delegation_tools:
        return

    mark_delegation_used()

    warnings = []
    output_str = str(tool_output)

    if tool_name == "delegate_task":
        expected_sections = ["Understanding", "Implementation", "Verification", "Risk"]
        missing = [s for s in expected_sections if s.lower() not in output_str.lower()]
        if missing:
            warnings.append(f"Worker output may be incomplete — missing sections: {', '.join(missing)}")

    error_indicators = ["Error: relay", "Error: cannot connect", "Error: model", "Connection refused"]
    for indicator in error_indicators:
        if indicator.lower() in output_str.lower():
            warnings.append(f"Worker output contains error: '{indicator}'")
            break

    # Log to delegation-log.jsonl
    log_entry = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "tool": tool_name,
        "status": "error" if warnings else "ok",
        "task_prefix": output_str[:120].replace("\n", " "),
    }

    # Extract model info if present (worker-delegate includes **Model**: ... header)
    model_match = re.search(r"\*\*Model\*\*:\s*(\S+)", output_str)
    if model_match:
        log_entry["model"] = model_match.group(1)

    tokens_match = re.search(r"\*\*Tokens\*\*:\s*(\d+)\s*/\s*(\d+)", output_str)
    if tokens_match:
        log_entry["tokens_in"] = int(tokens_match.group(1))
        log_entry["tokens_out"] = int(tokens_match.group(2))

    try:
        DELEGATION_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(DELEGATION_LOG, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except OSError:
        pass

    if warnings:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": "Delegation review needed: " + " | ".join(warnings)
                    + ". Verify worker output against acceptance criteria before using."
            }
        }
        print(json.dumps(output))


def handle_stop():
    """Stop handler — context-aware closeout reminders."""
    substantive, delegation = get_session_flags()

    parts = []

    if delegation:
        parts.append(
            "This session used worker delegation. "
            "Verify worker output was checked against acceptance criteria."
        )

    if substantive:
        parts.append(
            "Substantive work detected. Before closing: "
            "(1) Does DECISIONS.md need a new entry? Run /capture-decision. "
            "(2) Should context/projects/ be updated?"
        )

    if not parts:
        parts.append(
            "Lightweight session. No special closeout needed."
        )

    output = {
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "additionalContext": " | ".join(parts)
        }
    }
    print(json.dumps(output))


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: workspace-guard.py <event>", file=sys.stderr)
        sys.exit(1)

    event = sys.argv[1]

    if event == "pre-tool-use":
        handle_pre_tool_use()
    elif event == "user-prompt-submit":
        handle_user_prompt_submit()
    elif event == "post-tool-use":
        handle_post_tool_use()
    elif event == "stop":
        handle_stop()
    else:
        print(f"Unknown event: {event}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
