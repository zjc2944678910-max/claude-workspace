# Context Notes

Store durable context here when it should outlive a single Claude session.

## Good Uses

- project identity, paths, and scope boundaries
- architecture notes and execution-surface maps
- operator runbooks and repeated debugging findings
- naming conventions and domain glossaries
- stable conclusions that Claude should not relearn every time

## Avoid

- large raw logs
- temporary scratch output
- copied screenshots without summarizing them
- secrets, credentials, or tokens
- anything that belongs in the real product repository

## Writing Standard

- keep notes compact and task-reusable
- separate confirmed facts from working assumptions
- prefer absolute local paths
- update existing notes instead of creating near-duplicates
- move stale notes into `archive/` when a newer source replaces them

## Project Notes

Active project notes live in `context/projects/`. Each must use the **project-card** shape defined in `context/templates/project-note.md`.

Active project set: **OpenClaw**, **NAS Platform**, **Telegram Dual Relay**, **MathorCup-D**.

Retired project notes go to `archive/old-context/`. Do not keep stale project notes in `context/projects/`.
