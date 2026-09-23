# Init

Build a software factory for a named target by writing `AGENTS.md` files that later coding agents read, build from, and improve.

Filename is always `AGENTS.md`. Never `agents.md`.

This command does **not** implement the product. It interviews, designs, and writes layer harness files only.

---

## Target

The user must name the target directory (the software to build or bootstrap). Ask and stop if it is missing, not a directory, or does not exist. Do not default to this harness. The path may be anywhere readable.

Creating the target directory is allowed only when the user explicitly wants a new project path and confirms it.

Do not use Windows paths.

---

## Roles

Do not collapse these roles. The session running this command is the **coordinator**. It asks the user. It does not design the system and does not write `AGENTS.md` files.

| Role | Who | Job |
| --- | --- | --- |
| **Program manager** | This session | Talks to the user. Holds the interview. Locks the product description **in the conversation**. Does not write files. Not a sub-agent — sub-agents cannot hold the interview. |
| **Engineering solution architect** | Spawned sub-agent | Designs the solution from locked requirements. Does not write `AGENTS.md`. Does not implement code. |
| **Agent harness architect** | Spawned sub-agent | **Only** writer of `AGENTS.md` files (root and every layer). Does not implement the software. |

When spawning, choose the model that fits **that job** from models available in this chat.

- Do not default every role to the parent model.
- If the session exposes no model choice, say so and continue. Do not invent a vendor list.

---

## Workflow

### 1. Check root AGENTS.md

Look for `AGENTS.md` at the target root.

### 2. Existing product description

If it already contains a real description of the software the user wants: read it, restate it, and ask what is still wrong or missing. Do not redesign from scratch without that check.

### 3. Interview (Program manager)

If the root file is missing, or it does not describe the software: the Program manager helps the user build that description.

Ask, then wait. Do not assume. Do not let a sub-agent invent a missing requirement.

Learn at least:

| Need | What to get |
| --- | --- |
| **What** | What software they are trying to build |
| **Why / whom** | Problems it solves, and for whom |
| **Use cases** | Concrete scenarios |
| **Scale** | Users, data volume, request rate, latency, regions, tenancy, growth — whichever change the design. Understand the scale size of the problem. |
| **Environment** | Language, runtime, deploy target, team, constraints they already have |
| **Other** | Anything else that would change the solution (compliance, offline, budget, deadline, what must not change) |

Ask only what you need. Keep questions short and specific. Batch them. If an answer is still ambiguous in a way that would change the design, ask again and stop. Do not pick an interpretation to keep moving.

### 4. Lock requirements (conversation only)

After the user has answered, lock the product description **in the conversation**. Show that locked text and proceed only after they have answered. The Program manager does not write files.

A later fork the user did not decide stops the command. Ask and wait.

### 5. Engineering solution architect

Pass the locked requirements to the Engineering solution architect. That agent solutions the engineering problems and designs how to solve them from those criteria. Scale, use cases, and environment drive the design.

Offer the best solution for **this** problem, not a default stack from memory.

Before recommending current practice: name the systems in play and search official docs / current vendor guidance (same bar as [`architecture-brainstorm`](../architecture-brainstorm/SKILL.md)). Say what was verified.

If a missing constraint would change the design, return that question; the coordinator asks the user and waits.

**Must return:**

| Section | Content |
| --- | --- |
| Problem framing | What is being solved |
| Chosen design | How it is solved |
| Why it fits | Scale and use cases |
| Tradeoffs | What you accept |
| Rejected options | Real alternatives not chosen |
| Layer map | Directories and what each owns |

Does not write `AGENTS.md`. Does not implement code.

### 6. Agent harness architect

Pass the locked product description + design to the Agent harness architect. That agent is the **only** writer of `AGENTS.md` files. It places the locked product description in the root `AGENTS.md`, plus the architecture map and pointers to nested files, and writes each layer file.

Read `.agents/skills/software-factory/agents-md-template.md` if it exists. If it does not exist yet, follow this bar anyway:

Each file tells a future coding agent:

- What this layer is for
- What it owns
- What it must not do
- Contracts
- Invariants
- How to extend it
- Footguns

Create a directory only when a designed layer needs a home for its `AGENTS.md`. Prefer merge over wipe if files already exist.

Do not invent requirements beyond what the Program manager locked and the architect designed.

**Do not** implement application code, configs, or scaffolds beyond those layer directories and `AGENTS.md` files.

### 7. Implement or wait

When the harness architect returns, ask the user whether they want to implement now.

| Answer | Action |
| --- | --- |
| Yes | Stop this command. Invoke [`orchestrator-e2e`](../orchestrator-e2e/SKILL.md) for the build. This session does not become the implementer. |
| No | Say: tell me when. Do not start building. |

---

## Do / don't

**Don't**

- Implement the product in init.
- Skip the interview when the root file does not describe the software.
- Default the target to this harness.
- Let the Program manager write `AGENTS.md` (or any files).
- Let a sub-agent hold the interview or invent requirements.
- Collapse roles into one agent that designs and writes everything.
- Let two actors write the same `AGENTS.md`.
- Wipe existing `AGENTS.md` files; prefer merge.
- Use Windows paths.
- Add dates or version-sensitive instructions.
- Point this command at `STANDARDS.md`.
- Bake explain-to-levi into init.

**Do**

1. Require a named target; ask and stop if invalid.
2. Check existing root `AGENTS.md` before redesigning.
3. Interview as Program manager; lock the product description in chat after answers; do not write files.
4. Spawn Engineering solution architect with a model fit for design; research before recommending current practice.
5. Spawn Agent harness architect with a model fit for harness writing; that agent alone writes root and layer `AGENTS.md`.
6. Ask about implement; hand off to `orchestrator-e2e` or wait.
