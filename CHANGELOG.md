# Changelog

## 2026-09-19

The planner / implementer / reviewer loop is a user-invoked `orchestrator` skill. `AGENTS.md` is the pointer. `run-record` still owns the look. The orchestrator skill owns when/where.

Orchestrator keeps one run record per implementation request at `docs/runs/YYYY-MM-DD-short-name.md`.

File is created as header + Intent + Turn 1 on first role return. Later returns append. Prior turns are not rewritten.

Orchestrator writes it; sub-agents do not.

Chat report-back stays.

`docs/runs/` is gitignored. Run records stay local.

Run records are tables (one idea per row). New pipeline skill `run-record` owns that scan format. Orchestrator reads it before writing.

## 2026-09-18

Renamed to Levi's engineering harness (`levis-engineering-harness`).

New docs and Agent Skills harness — not an application.

Pipeline skills: `implementer`, `reviewer`, `research-project-agents`.

`research-project-agents` analyzes a user-named directory and writes that directory’s `AGENTS.md` (structure and purpose). No domain walk-up.

`architecture-brainstorm` is a user-invoked skill for software engineering architecture brainstorming (first principles and current research). Not a pipeline role.

`tests/` is gone. Tests are allowed when they earn their keep; they are not required. Tester is optional. Planner, implementer, and reviewer stay required.

Orchestrator picks a model per spawned job from the current chat session; cloning this chat onto every role is the failure mode.
