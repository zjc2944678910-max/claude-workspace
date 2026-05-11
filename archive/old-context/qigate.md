# QiGate Project Note

## Identity

- Project name: QiGate
- Repository: `/Users/zhangjincheng/Documents/GitHub/codex-workspace/projects/products/qigate`
- Summary: multi-tenant property access SaaS workspace

## Main Surfaces

- `apps/web`: brand site and property console
- `apps/api`: NestJS API and event simulation
- `apps/miniapp`: Taro WeChat miniapp
- `services/gateway`: Go device gateway skeleton
- `packages/domain`: shared domain logic
- `packages/ui`: shared UI components

## Quick Start

- `corepack prepare pnpm@10.11.0 --activate`
- `pnpm install`
- `pnpm dev`

## Working Guidance

- Frontend changes usually start in `apps/web`.
- Backend behavior usually starts in `apps/api`.
- Cross-surface domain changes often touch `packages/domain`.
