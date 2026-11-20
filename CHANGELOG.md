# Changelog

## 2026-11-19

`software-factory` now proves its checks before anyone builds. The verifier writes red checks, `checks/red-*.sh`: probes that must fail on the code as it is today and pass after the build. A new command, `factory.py red <id>`, runs them and writes `red.md`. The script refuses the first build until every red check has failed, or the verification plan says under `## Red first` why nothing can fail first. A check that passes before the work cannot tell broken from fixed.

Every question to Levi now carries a recommended answer, worded so "yes" accepts it. The rules are in one place, **Asking Levi** in the skill.

The reviewer lists, under `## For next time`, each mistake a script or a one-line rule could catch before it reaches a reviewer again. The report offers it to Levi as its own ticket.

STANDARDS name two more tests that prove nothing: one that works out its expected value the way the code does, and one that tests the code's insides instead of its behavior. The implementer now writes one test at a time.

Added `GLOSSARY.md` to the skill: one name for each thing on the line, with the words to avoid. "Vague task" is a research task; "specialist" is the verifier.

These ideas come from Matt Pocock's skills, `mattpocock/skills` (MIT): proof that a check goes red first, questions with a recommended answer, the retro, and the glossary format.

## 2026-11-18

`software-factory` is rebuilt. It no longer writes `AGENTS.md` files; init, crawl, improve, and explain are gone. A pasted task now runs through a line: intake, research, verification design, an implementer / gate / reviewer loop, and a TLDR report. The main chat is the orchestrator and spawns Opus sub-agents for all the work.

Intake sorts the task. A standard task has a clear done and an existing pattern. A research task has a clear goal but no known best solution: a researcher looks it up instead of answering from training data, ranks the solutions, and Levi chooses. The researcher then writes the plan.

A verifier decides the checks before any build, and writes `checks.sh` to run them. The implementer builds to them. A script, the gate, runs them: a failing build goes straight back to the implementer and no reviewer is spawned. The gate refuses to run if the plan or the checks changed after the build started. The reviewer judges what a script cannot.

Sub-agents hand off through files in the ticket folder, not through the orchestrator. Each role has one instruction file under `roles/` and writes one file, which starts with a verdict line and a short summary. Levi's answers are saved in his words. A new chat can resume a ticket from its folder.

`board/factory.py` is the only thing that changes a ticket's stage, and it refuses a move the line does not allow: no build before the verification plan, no review before the gate passes, no done before the reviewer accepts, and no fifth round without Levi. It has a test file, `board/test_factory.py`.

Added a live board on `http://127.0.0.1:4747`. It shows each ticket's stage, state, round results, and files, and its cost, tokens, time, and model with one row per sub-agent. Cost is read from Claude Code's sub-agent transcripts, matched by the ticket folder line that starts every brief, and priced from `board/prices.json`. It is the API list price of the sub-agents; the orchestrator chat is not counted. Tickets live in `~/.software-factory/tickets/`, one folder each.

The board is a list of tickets, most urgent first, with each ticket's stage drawn as a pipeline in its row, and a side pane with activity, files, and sub-agents. It is keyboard driven. Its look is set by `board/DESIGN.md`: greyscale, colour only for state, no cards or badges.

## 2026-11-10

STANDARDS now require building a feature into the architecture, not bolting it on. If there is no natural way to build it and a refactor would be the clean path, stop before building and say so. The reviewer checks this under Maintainability.

## 2026-10-02

Updated `k-explain` to require a custom visual teaching artifact by default. Includes a bundled teaching-sheet reference for consistent presentation across conversations. Supplied examples define the teaching structure and visual style; short prompts no longer route to prose alone. Requires rendering, visual inspection, and interaction checks before delivering the usable result. Diagram arrows must follow actual data inputs; video verification must inspect encoded scene changes and narration timing. Explicit user format requests still take precedence.

Added `k-explain`: an independent skill that chooses clear writing, diagrams, interactive HTML, or bespoke narrated video to make concepts and model outputs easier to understand. Includes relaxed ASD-STE100 writing and ElevenLabs or local narration options.

## 2026-10-01

Added `bible`: chooses specialists for the user's ask, gives each a folder of concise project memory, and tracks delivery through `/goal` with verified completion criteria.

## 2026-09-26

Removed `orchestrator-learning`. The pipeline is `orchestrator-e2e` only. Each role's conversation is a run-record artifact, so the pipeline runs through without stopping after a phase to explain and wait.

`spawn-specialist` is a user-invoked skill. This session understands the ask and briefs one expert. It does not answer the subject. For questions that might change with time, the specialist researches first and never uses pre-trained data for the answer. Stable facts such as math do not need a fresh lookup. It may spawn more sub-agents if it needs to; those agents follow the same split.

## 2026-09-23

`software-factory` is a user-invoked skill. init interviews and writes layer AGENTS.md; crawl writes AGENTS.md from the tree; improve researches with type-specific experts; explain crawls then explains with explain-to-levi. It does not implement the product.

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
