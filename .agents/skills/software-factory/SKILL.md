---
name: software-factory
description: >-
  Builds a software factory of AGENTS.md files so later coding agents can read
  them, build the software, and improve it. Commands: init (interview, design,
  write layer AGENTS.md), crawl (crawl every layer and write AGENTS.md),
  improve (type-specific experts research how to make the code better),
  explain (crawl, then explain the repo with explain-to-levi). Use when the
  user names software-factory, or asks to init, crawl, improve, or explain a
  codebase as a software factory.
disable-model-invocation: true
---

# Software factory — coordinator, not implementer

You are **not** the implementer. This skill builds or refreshes a factory of `AGENTS.md` files so later coding agents can read them, build the software, and improve it. It does not implement the product.

Your job is to pick the command, read its file, and follow it. Spawn the sub-agents that command names. Do not collapse roles into one agent. Choose a model that fits each job when the session exposes a choice.

## Pick a command

If the user did not name a command, ask which one and stop. Do not guess.

| Command | Read and follow |
| --- | --- |
| **init** | [init.md](init.md) |
| **crawl** | [crawl.md](crawl.md) |
| **improve** | [improve.md](improve.md) |
| **explain** | [explain.md](explain.md) |

The user names one command. Read that file and follow it. When that command tells you to run crawl, follow [crawl.md](crawl.md) as well. Do not invent a fifth command.

Layer file shape for **init** and **crawl**: [agents-md-template.md](agents-md-template.md).

## Rules that apply to every command

- **Target.** A directory the user names. Ask and stop if missing or invalid. Do not default to this harness. [explain.md](explain.md) has the extra rule for "this repo".
- **Filename.** Always `AGENTS.md`. Never `agents.md`.
- **Roles.** Spawn the sub-agents the command names. Do not collapse roles. Prefer a model fit for each job when the session exposes a choice. If it does not, say so and continue.
- **No product build.** This skill does not implement product code. **init** and **improve** hand off to [`orchestrator-e2e`](../orchestrator-e2e/SKILL.md) only after the user says yes.
- **explain.** Read [`explain-to-levi`](../explain-to-levi/SKILL.md) and follow it.

Do not point at `STANDARDS.md`. Do not use Windows paths or dates.
