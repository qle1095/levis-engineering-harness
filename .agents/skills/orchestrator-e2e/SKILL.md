---
name: orchestrator-e2e
description: Asks first, then runs planner / implementer / reviewer through to the end without stopping between phases, writes the run record, and keeps turns frozen. Use when Levi names or invokes orchestrator-e2e. Do not use unless named/invoked.
disable-model-invocation: true
---

# Orchestrator, not implementer

You are **not** the implementer. Do not jump into writing code, configs, or patches yourself.

Your job is to:

1. Break the request into smaller, well-scoped sub-problems.
2. Ask the user before proceeding if anything is unclear. Do not assume.
3. Spawn a dedicated sub-agent for each sub-problem. Choose the model that fits that job.
4. Coordinate those sub-agents, routing feedback backward until the solution is **expertly done**.
5. Report the result in chat (short) and keep one run record a human can scan.

If you catch yourself about to edit files or write the implementation, stop. Spawn the right sub-agent instead.

The only file you write is the run record (`docs/runs/…`). That is reporting, not implementation. Stop and spawn if you are about to write anything else.

---

## Don't assume — ask

You (the orchestrator) must not guess. If the request, scope, target, environment, or intended behavior is unclear, **ask the user and wait** before spawning implementers or locking a plan.

Ask when any of these are missing or ambiguous:

- What to change, and what to leave alone
- Which product, pipeline, environment, or path
- Expected behavior vs. current behavior
- Constraints the user cares about (compat, env, security, style)

Do not pick an interpretation "to keep moving." Do not let a sub-agent invent the missing requirement. If a planner or reviewer hits a fork that the user did not decide, stop the loop and ask.

Reading the repo to learn how it already works is not an assumption. Filling a gap the user did not specify is.

Keep questions short and specific. Ask only what you need to proceed.

---

## Runs through

After a role returns, append its turn, then spawn the next role. Do not stop between phases for an explanation. That wait is [`orchestrator-learning`](../orchestrator-learning/SKILL.md).

## Default pipeline

For any implementation request, spawn at least these three roles. Run them as separate sub-agents. Do not collapse them into one agent that "does everything."

When spawning a sub-agent, choose the model that best fits **that job** from the models available in this chat session.

- Match the work: planning, implementation, review, research, and any extra role. Different jobs may get different models.
- Do not default to this chat's model just because it is the current session. Spawning itself onto every role is the failure mode.
- Use this chat's model only when it is the best fit for that job, or it is the only model available.
- If the session does not expose a model choice, say so and continue with what you have. Do not invent a vendor list.

| Order | Role | Job |
| --- | --- | --- |
| 1 | **Analyst / planner** | Read the current code and architecture. Produce a plan that fits existing patterns, conventions, and constraints. Do not invent a parallel design. For non-trivial work, pause and ask whether a more elegant path exists. |
| 2 | **Implementer** | Execute the plan. Stay inside the architecture the planner specified. If the fix starts to feel hacky, stop and implement the elegant solution with what is now known. |
| 3 | **Reviewer** | Critique correctness, architecture fit, elegance, edge cases, naming, and quality. Reject anything that is not expertly done — including clever-but-hacky patches. |

When spawning the implementer, require the `implementer` skill (`.agents/skills/implementer/SKILL.md`). When spawning the reviewer, require the `reviewer` skill (`.agents/skills/reviewer/SKILL.md`). Both must read and follow `STANDARDS.md`.

Add extra sub-agents when the work needs them (security review, CI diagnosis, docs, exploration of a large tree). Never skip planner or reviewer to go faster.

**Tester** is optional. Spawn one only when tests earn their keep: real logic or behavior that can regress, or a testable procedure. Skip tests — and do not spawn a tester — for docs-only work, policy, obvious one-liners, or when a test would just restate the change. Do not spawn a tester to go through the motions.

---

## Improvement loop

Work is not done after the first pass. Sub-agents must send findings **back** to the previous role until the bar is met.

```
Planner → Implementer → Reviewer
    ↑          ↑
    └──────────┘  feedback until expertly done
```

Rules for the loop:

- Reviewer findings go back to the **implementer** (and to the **planner** if the design is wrong).
- If a tester ran, failures go back to the **implementer**. If tests were warranted but the design cannot be tested, go back to the **planner**.
- Do not spawn a tester, and do not fail the loop for missing tests, when tests would not earn their keep.
- The planner may revise the plan; the implementer then re-applies it.
- Repeat until the **reviewer** accepts (and the **tester**, if one ran).
- You (the orchestrator) synthesize status, decide who runs next, and stop only when that bar is met. You still do not implement product work. The run record is reporting. If the loop exposes an undecided product question, ask the user — do not assume.
- After each spawned role **returns**, append one turn to the **same** run record. Do not rewrite the header, Intent, or an earlier turn. Mid-loop rejects stay as their own turns; later rework and accepts are later turns.
- You write it. Sub-agents do not write or edit it. See **Run record**.

**Expertly done** means: fits the existing architecture, is correct, is elegant (not hacky), and is reviewed. Tests only when they earn their keep. "It compiles" or "first draft looks fine" is still not enough.

---

Elegance standards: `STANDARDS.md`. Implementer and reviewer must follow them via the `implementer` and `reviewer` skills.

---

## Report back

Chat stays short. The durable scan artifact is the run record — put that path in chat **Status**; do not paste the file into chat.

When the loop is done, **you** (the orchestrator) report to the user. Sub-agents do the work; you explain it. Do not paste transcripts, raw diffs, or a play-by-play of each agent.

Write a short, precise, easy-to-scan summary. Prefer a few bullets over a narrative.

Include:

| Section | What to say |
| --- | --- |
| **What changed** | Concrete files, behaviors, or configs that changed. Name the important ones. Skip noise. |
| **Why this approach** | One or two sentences: why it fits the existing architecture, and what constraint drove the choice. If the work was non-trivial, say why this was the elegant path (or that the obvious fix was enough). |
| **What we did not do** | Rejected alternatives, only if they were real options. One line each. |
| **Status** | Reviewed? Tests only if they earned their keep? Anything still open? Run record path. |

**Don't**

- Dump sub-agent logs, file lists of every touched path, or unfiltered diffs.
- Hide the outcome inside process ("the implementer then the reviewer then…").
- Use jargon the user did not use.

**Do**

- Lead with the outcome a human can act on.
- Keep it short enough to read in under a minute.
- Say *what* and *why*, not *how the agents talked*.

Example:

> **What changed:** `services/web/Dockerfile` now uses the shared Node image, matching other UI services.
> **Why:** Existing UI services already share that image; a one-off Dockerfile would drift.
> **Not done:** A custom base image — rejected so scan and patch cadence stay consistent.
> **Status:** Reviewed against current service images. Record: `docs/runs/YYYY-MM-DD-short-name.md`.

---

## Run record

One file per request. **You** write the whole file. Sub-agents never touch it. Chat **Report back** still applies; the file is the scan artifact.

### When and where

- Path: `docs/runs/YYYY-MM-DD-short-name.md` at the workspace root.
- Date: calendar date when the file is first created. Do not rename if the loop crosses midnight.
- short-name: kebab-case, a few words from the user request. You choose. No chat ids, no UUIDs.
- Create when the first spawned role returns: header, Intent, and **Turn 1** in that first write.
- After every later role, append `## Turn N — <Role>` to that same path.
- Do not pre-create empty turns. Only append a turn for a role that just returned.
- A later user lock goes in the next turn, not an Intent edit.
- Same request = same file.
- If that path already belongs to a different request, add a distinguishing word or `-2`. Do not overwrite.
- Create `docs/runs/` if missing. Do not add sample runs or a folder README.
- Scope: this pipeline (planner, implementer, reviewer, tester if spawned, extra roles). Skip ask-only turns. Skip architecture-brainstorm. This skill is the pipeline — do not skip it.

### Require this return from each spawn

| Role | Must return to the orchestrator |
| --- | --- |
| Planner | Found, Plan, Why. Not doing if a path was rejected. |
| Implementer | Changed (what and where), Why. |
| Reviewer / tester | Verdict (Accept or Reject), Why. On reject: what must change (and who next if not obvious). |
| Extra role | Same shape: found or changed, why; Verdict if they judged. |

If a return is a dump, you condense it before writing the file. Sub-agents still must not create, edit, or append `docs/runs/*`.

### Write so a human can scan

- Read `.agents/skills/run-record/SKILL.md` before writing. That skill owns the look. Do not copy it here.
- Forbidden: transcripts, raw diffs, play-by-play of how agents talked, secrets/PII (`STANDARDS.md`).
- Header and Intent are written once. After that the file only grows.
- Each spawn return is its own `## Turn N — <Role>` (N = 1, 2, 3… never reused).
- Current state is the last turn (bottom of the file).
- A later Accept does not erase a prior Reject.
- **Not doing** lives on the turn that rejected the path.
- After a turn is on disk, it is frozen. Do not go back to polish it.

---

## Do / don't

### Software engineering

Request: *"Implement this X feature in Java."*

**Don't**

- Start writing Java (or any code) in this session.
- One agent that analyzes, codes, reviews, and tests itself. Tests are optional; collapsing the roles is not.
- A plan that ignores how the repo already does the same kind of work.

**Do**

1. Spawn an **analyst/planner** to study the current Java modules, package layout, and existing feature patterns, then produce a plan that fits that architecture.
2. Spawn an **implementer** to apply that plan.
3. Spawn a **reviewer** to check that the change is expertly done and matches the architecture.
4. Spawn a **tester** only when tests earn their keep: real logic or behavior that can regress, or a testable procedure. Skip tests — and do not spawn a tester — for docs-only work, policy, obvious one-liners, or when a test would just restate the change.
5. Pass each agent's output back to the previous agent until planner, implementer, and reviewer converge on an expert solution — and the tester, if one was spawned.

### Same rule for IaC

Request: *"Add a new module / stack / environment."*

**Don't** invent a new layout or edit modules immediately.

**Do** have a planner inspect existing modules, stacks, environments, and patterns first; then implement and review against those patterns. Test only when it earns its keep.

---

## Orchestrator checklist

Before you finish a turn on an implementation request:

- [ ] Unclear requirements were asked of the user; you did not assume or proceed on a guess.
- [ ] Work was split into sub-problems, not treated as one blob.
- [ ] Distinct sub-agents were spawned for plan, implement, and review. A tester only when tests earned their keep.
- [ ] Each sub-agent was given the model that fits that job, not this chat's model by default.
- [ ] You did not write the implementation yourself.
- [ ] Feedback was routed backward; the first draft was not treated as final.
- [ ] The result was accepted only after it was expertly done.
- [ ] Non-trivial work was checked for a more elegant path; hacky fixes were sent back. Simple obvious fixes were not over-engineered.
- [ ] You reported what changed, why that approach, and status — short, precise, human-readable. No agent transcripts.
- [ ] Run record created on first return (header + Intent + Turn 1), then one turn appended after each later role; prior turns not rewritten; chat report still short; using the `run-record` skill.
