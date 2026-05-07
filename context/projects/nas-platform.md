# NAS Platform Project Note

## Identity

- Project name: NAS Platform
- Repository: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/infrastructure/nas-platform`
- Summary: NAS and VPS infrastructure repo for app stacks, infra services, generated env files, and deployment scripts

## Main Surfaces

- `apps-*`: application compose stacks
- `infra-*`: platform service compose stacks
- `generated/`: generated env files
- `scripts/`: push and sync scripts
- `vps-nginx/`: VPS nginx configs
- `vps-ssh/`: SSH config fragments

## Working Guidance

- Infra changes often start in the matching `apps-*` or `infra-*` directory.
- Deployment behavior usually involves `scripts/`.
- Public routing and TLS behavior usually lives in `vps-nginx/`.
