# Changelog

## 2026-09-23

STANDARDS now require three checks. A test that would still pass if every function it calls returned no result observes nothing: rewrite it or delete it. When a feature path exists, run it before accept, and the reviewer reads the diff. When two actors might write the same file, key, or record, give each its own unless one shared writer is required.

One more branch in an existing chain, or a second flag that must stay in sync with the first, is a reason to pause for elegance.

When two fixes fail on the same assumption, `orchestrator-e2e` writes that assumption down before a third fix.

## 2026-09-21

The pipeline is two skills. `orchestrator-e2e` runs planner, implementer, and reviewer through to the end. `orchestrator-learning` stops after each phase, explains it, and waits before the next. `orchestrator-e2e` still owns the shared pipeline rules.

`explain-to-levi` is now a skill in this harness (`.agents/skills/explain-to-levi/`). It is the same skill as the home copy: how to explain so it clicks, and how to update itself when it does not.

`orchestrator-learning` explains each phase with `explain-to-levi`. It writes a run record only when that phase tables cleanly.

`explain-to-levi` no longer keeps a list of past misses. When an explanation does not click, the agent reasons from first principles about what would help Levi understand this, or what he is looking for, then explains again. A new sentence is added to the skill only when that reasoning produces a principle that would apply to any topic.

STANDARDS now require surgical edits: change only what the request needs, remove only orphans this change created, and mention pre-existing dead code instead of deleting it.

Reviewer rejects drive-by formatting, drive-by refactors, and unrelated deletes.

Error handling is for failures that can happen, not invented cases. An overbuilt patch gets rewritten smaller. Implementer stops and names a fork instead of picking silently.

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
