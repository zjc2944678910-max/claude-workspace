# Telegram Dual Relay — Project Card

| Field | Value |
|---|---|
| **Repository** | `/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/infrastructure/telegram-dual-relay` |
| **Summary** | Telegram message relay service for dual-bot forwarding |
| **Live host** | `—` |

## Key Surfaces

- `src/`: relay service source code
- `scripts/`: operational scripts
- `systemd/`: service unit files
- `tests/`: test suite
- `docs/`: documentation
- `examples/`: example configs

## Working Guidance

- Service logic changes → `src/`.
- Deployment or systemd setup → `systemd/` and `scripts/`.

## Safety Boundary

- Relay changes can affect message delivery for connected bots.
- Test locally before deploying to production host.