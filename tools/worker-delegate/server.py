"""
Worker Delegate MCP Server

Delegates bounded implementation tasks to cheaper models via VPS relay APIs.
Claude (Opus) stays as architect/reviewer; worker models do implementation.

Relay endpoints (OpenAI-compatible):
  - new-api  (:3000) → MiMo, DeepSeek
  - sub2api  (:8080) → GPT series
"""

import json
import os
from pathlib import Path

import httpx
from fastmcp import FastMCP

mcp = FastMCP(
    "worker-delegate",
    instructions=(
        "Use this server to delegate bounded implementation tasks to worker models. "
        "Claude handles architecture, design, review, and acceptance. "
        "Worker models handle code implementation within a defined scope."
    ),
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CONFIG_PATH = Path(__file__).parent / "config.json"

def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)


def get_relay(relay_name: str, cfg: dict) -> dict:
    relay = cfg["relays"][relay_name]
    key_env = relay["api_key_env"]
    return {
        "base_url": relay["base_url"],
        "api_key": os.environ.get(key_env, ""),
    }


# ---------------------------------------------------------------------------
# Worker system prompt
# ---------------------------------------------------------------------------

WORKER_SYSTEM_PROMPT = """\
You are a code implementation worker. Your role is strictly bounded execution.

Rules:
- Implement exactly what the task describes. No more, no less.
- Stay within the specified scope. Do not touch files outside scope.
- Follow all constraints. If a constraint conflicts with the task, say so and stop.
- Return clean, working code in fenced code blocks with file paths as headers.
- Do not make architectural decisions, expand scope, or add unrequested features.
- Do not add unnecessary comments, docstrings, or error handling beyond what's needed.
- If the task is unclear, state what's unclear rather than guessing.

Output format:
1. **Understanding**: 1-2 sentences confirming what you'll implement.
2. **Implementation**: Code blocks with `filepath` headers for each changed file.
3. **Verification**: How to verify this works (command or test).
4. **Risks**: Anything the reviewer should double-check (or "None").
"""

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
async def delegate_task(
    task: str,
    context: str = "",
    tier: str = "default",
    model: str = "",
    scope: str = "",
    constraints: str = "",
    max_tokens: int = 16384,
) -> str:
    """Delegate a bounded implementation task to a worker model.

    Args:
        task: What to implement. Be specific: files, functions, acceptance criteria.
        context: Relevant code snippets, file contents, or background. Keep bounded.
        tier: Model tier selection. Options: default, strong, complex, code, light.
             default=mimo-v2.5, strong=mimo-v2.5-pro, complex=gpt-5.4,
             code=gpt-5.3-codex, light=gpt-5.4-mini.
        model: Override tier with a specific model ID (e.g. "deepseek-v4-flash").
        scope: Files or directories the worker may edit. Empty = inferred from task.
        constraints: What the worker must NOT do. Forbidden actions, files, patterns.
        max_tokens: Max response tokens. Default 16384 (MiMo reasoning models need extra room).

    Returns:
        Worker model's implementation response including code and verification steps.
    """
    cfg = load_config()

    # Resolve model
    if not model:
        model = cfg["tiers"].get(tier, cfg["tiers"]["default"])

    # Find relay for this model
    relay_name = cfg["model_routing"].get(model)
    if not relay_name:
        return f"Error: model '{model}' not found in routing config. Available: {list(cfg['model_routing'].keys())}"

    relay = get_relay(relay_name, cfg)
    if not relay["api_key"]:
        return f"Error: API key not set for relay '{relay_name}'. Set env var: {cfg['relays'][relay_name]['api_key_env']}"

    # Build user message
    parts = [f"## Task\n{task}"]
    if scope:
        parts.append(f"## Scope\n{scope}")
    if constraints:
        parts.append(f"## Constraints\n{constraints}")
    if context:
        parts.append(f"## Context\n{context}")
    user_message = "\n\n".join(parts)

    # Call relay API
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            resp = await client.post(
                f"{relay['base_url']}/chat/completions",
                headers={
                    "Authorization": f"Bearer {relay['api_key']}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": WORKER_SYSTEM_PROMPT},
                        {"role": "user", "content": user_message},
                    ],
                    "max_tokens": max_tokens,
                    "temperature": 0.3,
                },
            )
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            return f"Error: relay returned {e.response.status_code}: {e.response.text[:500]}"
        except httpx.ConnectError:
            return f"Error: cannot connect to relay '{relay_name}' at {relay['base_url']}"
        except httpx.ReadTimeout:
            return f"Error: relay '{relay_name}' timed out after 120s"

    data = resp.json()
    message = data["choices"][0]["message"]
    content = message.get("content", "") or ""
    reasoning = message.get("reasoning_content", "")

    # Build result with metadata
    usage = data.get("usage", {})
    reasoning_tokens = usage.get("completion_tokens_details", {}).get("reasoning_tokens", 0)
    meta_lines = [
        f"**Model**: {model} (via {relay_name})",
    ]
    if usage:
        token_info = f"**Tokens**: {usage.get('prompt_tokens', '?')} in / {usage.get('completion_tokens', '?')} out"
        if reasoning_tokens:
            token_info += f" ({reasoning_tokens} reasoning)"
        meta_lines.append(token_info)

    result = "\n".join(meta_lines) + "\n\n---\n\n"
    if reasoning:
        result += f"<details><summary>Reasoning ({reasoning_tokens} tokens)</summary>\n\n{reasoning}\n\n</details>\n\n"
    result += content

    return result


@mcp.tool()
async def list_worker_models() -> str:
    """List available worker models, their tiers, and relay sources."""
    cfg = load_config()

    lines = ["## Tier Defaults\n"]
    for tier, model_id in cfg["tiers"].items():
        lines.append(f"- **{tier}**: `{model_id}`")

    lines.append("\n## All Available Models\n")
    lines.append("| Model | Relay | Notes |")
    lines.append("|-------|-------|-------|")
    for model_id, relay_name in cfg["model_routing"].items():
        notes = cfg.get("model_notes", {}).get(model_id, "")
        lines.append(f"| `{model_id}` | {relay_name} | {notes} |")

    return "\n".join(lines)


@mcp.tool()
async def quick_ask(
    question: str,
    model: str = "",
    tier: str = "default",
    max_tokens: int = 2048,
) -> str:
    """Ask a worker model a quick question without full task framing.

    Good for: code explanations, API lookups, format conversions, quick checks.
    Not for: implementation tasks (use delegate_task instead).

    Args:
        question: The question to ask.
        model: Specific model ID. Empty = use tier default.
        tier: Model tier if model not specified.
        max_tokens: Max response tokens.
    """
    cfg = load_config()

    if not model:
        model = cfg["tiers"].get(tier, cfg["tiers"]["default"])

    relay_name = cfg["model_routing"].get(model)
    if not relay_name:
        return f"Error: model '{model}' not found in routing."

    relay = get_relay(relay_name, cfg)
    if not relay["api_key"]:
        return f"Error: API key not set for relay '{relay_name}'."

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            resp = await client.post(
                f"{relay['base_url']}/chat/completions",
                headers={
                    "Authorization": f"Bearer {relay['api_key']}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": question}],
                    "max_tokens": max_tokens,
                    "temperature": 0.3,
                },
            )
            resp.raise_for_status()
        except (httpx.HTTPStatusError, httpx.ConnectError, httpx.ReadTimeout) as e:
            return f"Error: {e}"

    data = resp.json()
    message = data["choices"][0]["message"]
    content = message.get("content", "") or ""
    reasoning = message.get("reasoning_content", "")
    usage = data.get("usage", {})
    reasoning_tokens = usage.get("completion_tokens_details", {}).get("reasoning_tokens", 0)

    meta = f"**Model**: {model} | **Tokens**: {usage.get('prompt_tokens', '?')} in / {usage.get('completion_tokens', '?')} out"
    if reasoning_tokens:
        meta += f" ({reasoning_tokens} reasoning)"

    result = meta + "\n\n---\n\n"
    if reasoning:
        result += f"<details><summary>Reasoning</summary>\n\n{reasoning}\n\n</details>\n\n"
    result += content

    return result


if __name__ == "__main__":
    mcp.run()
