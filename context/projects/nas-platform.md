# NAS Platform — Project Card

| Field | Value |
|---|---|
| **Repository** | `/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/infrastructure/nas-platform` |
| **Summary** | NAS and VPS infrastructure: app stacks, infra services, env files, deployment scripts |
| **Live host** | `oc-nas` (NAS) / VPS via `vps-ssh/` |

## Key Surfaces

- `apps-*`: application compose stacks
- `infra-*`: platform service compose stacks
- `generated/`: generated env files
- `scripts/`: push and sync scripts
- `vps-nginx/`: VPS nginx configs
- `vps-ssh/`: SSH config fragments

## Working Guidance

- Infra changes → matching `apps-*` or `infra-*` directory.
- Deployment → `scripts/`.
- Public routing and TLS → `vps-nginx/`.

## Safety Boundary

- Infrastructure changes can affect all hosted services.
- Confirm scope before editing compose stacks or nginx configs.
