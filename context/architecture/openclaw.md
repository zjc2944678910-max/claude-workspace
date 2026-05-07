# OpenClaw Architecture Note

## Surfaces

- Mainline code repository: application source and normal feature work
- Migration reference: historical comparison and recovery context
- Ops surface: deployment ledger, manifests, mirrors, evidence, rollback bundles
- Sidecar state: project-specific local state outside source control

## Route Selection

- Feature work or app bug fix: mainline repository
- Production audit or deployment-history question: ops surface
- Historical diff or migration validation: migration reference
- Local state inspection: sidecar state
