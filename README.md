# levis-engineering-harness

**Levi's engineering harness** is docs and Agent Skills only, **not an application**. It guides coding agents. Open this working space in **Cursor or Codex**.

## How it is used

Name or invoke [`orchestrator-e2e`](.agents/skills/orchestrator-e2e/SKILL.md) for a planner / implementer / reviewer pipeline that runs through. Name or invoke [`orchestrator-learning`](.agents/skills/orchestrator-learning/SKILL.md) for the same pipeline when it should stop after each phase, explain it with explain-to-levi, and wait. Both are user-invoked, not every chat. When either runs, this session is not the implementer. orchestrator-e2e writes one run record using the `run-record` skill. orchestrator-learning writes one when that phase tables cleanly. Sub-agents do not.

When spawned, the **implementer** and **reviewer** load their skills and follow [STANDARDS.md](STANDARDS.md).

To orient later coding agents on another tree, name a target directory and use [`research-project-agents`](.agents/skills/research-project-agents/SKILL.md). That skill analyzes the named directory and writes that directory’s `AGENTS.md` (structure and purpose).

To brainstorm software engineering architecture, name or invoke [`architecture-brainstorm`](.agents/skills/architecture-brainstorm/SKILL.md). That is a conversation with an expert engineer, not a pipeline role and not a build.

When explaining anything to Levi, follow [`explain-to-levi`](.agents/skills/explain-to-levi/SKILL.md). That skill loads for explanation, not only when he names it.

## Docs

- [AGENTS.md](AGENTS.md) — Docs/skills harness; name or invoke orchestrator-e2e or orchestrator-learning.
- [STANDARDS.md](STANDARDS.md) — Elegance, surgical changes, clear code, secrets, errors/logs/audit, changelog/docs, when to test, and review gates.
- [CHANGELOG.md](CHANGELOG.md) — Project changelog.

## Skills

Skills live under `.agents/skills/`. Cursor, Codex, and other Agent Skills–compatible harnesses load them from this path.

**Pipeline-only** (`disable-model-invocation: true` — the agent/pipeline loads them; the user does **not** slash-invoke them):

- [`implementer`](.agents/skills/implementer/SKILL.md) — Used when spawned as the implementer in the orchestrator-e2e or orchestrator-learning pipeline. Executes the plan; follows STANDARDS.md.
- [`reviewer`](.agents/skills/reviewer/SKILL.md) — Used when spawned as the reviewer in the orchestrator-e2e or orchestrator-learning pipeline. Reviews against STANDARDS.md.
- [`run-record`](.agents/skills/run-record/SKILL.md) — Used when orchestrator-e2e or orchestrator-learning writes a run record. Owns the scan format (tables, short cells, one idea per row). Keeps human-readability and ease to scan through it a priority.
- [`research-project-agents`](.agents/skills/research-project-agents/SKILL.md) — Analyzes a user-named directory and writes that directory’s AGENTS.md so later coding agents can understand structure and purpose without reading the tree. **Name a target directory**; do not default to this harness.

**Every chat** (no `disable-model-invocation` — loads when explaining anything to Levi):

- [`explain-to-levi`](.agents/skills/explain-to-levi/SKILL.md) — How to explain so it clicks. When it does not, think from first principles about what would help Levi understand this, instead of matching a list of past misses.

**User-invoked** (`disable-model-invocation: true` — same flag, different loader: Levi names or invokes; it does not auto-load):

- [`orchestrator-e2e`](.agents/skills/orchestrator-e2e/SKILL.md) — on-demand pipeline (planner / implementer / reviewer) that runs through. Not every chat.
- [`orchestrator-learning`](.agents/skills/orchestrator-learning/SKILL.md) — same pipeline, but stops after each phase, explains it with explain-to-levi, writes a run record when that phase tables cleanly, and waits. Not every chat.
- [`architecture-brainstorm`](.agents/skills/architecture-brainstorm/SKILL.md) — software engineering architecture brainstorming: expert engineer in the room, first principles, current research, pushback, tradeoffs. Not a build.
