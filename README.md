# levis-engineering-harness

**Levi's engineering harness** is docs and Agent Skills only, **not an application**. It guides coding agents. Open this working space in **Cursor or Codex**.

## How it is used

Name or invoke [`orchestrator`](.agents/skills/orchestrator/SKILL.md) for the planner / implementer / reviewer pipeline. It is user-invoked, not every chat. When it runs, this session is not the implementer. After pipeline work the orchestrator writes one run record using the `run-record` skill; sub-agents do not.

When spawned, the **implementer** and **reviewer** load their skills and follow [STANDARDS.md](STANDARDS.md).

To orient later coding agents on another tree, name a target directory and use [`research-project-agents`](.agents/skills/research-project-agents/SKILL.md). That skill analyzes the named directory and writes that directory’s `AGENTS.md` (structure and purpose).

To brainstorm software engineering architecture, name or invoke [`architecture-brainstorm`](.agents/skills/architecture-brainstorm/SKILL.md). That is a conversation with an expert engineer, not a pipeline role and not a build.

## Docs

- [AGENTS.md](AGENTS.md) — Docs/skills harness; name or invoke orchestrator.
- [STANDARDS.md](STANDARDS.md) — Elegance, surgical changes, clear code, secrets, errors/logs/audit, changelog/docs, when to test, and review gates.
- [CHANGELOG.md](CHANGELOG.md) — Project changelog.

## Skills

Skills live under `.agents/skills/`. Cursor, Codex, and other Agent Skills–compatible harnesses load them from this path.

**Pipeline-only** (`disable-model-invocation: true` — the agent/pipeline loads them; the user does **not** slash-invoke them):

- [`implementer`](.agents/skills/implementer/SKILL.md) — Used when spawned as the implementer in the orchestrator pipeline. Executes the plan; follows STANDARDS.md.
- [`reviewer`](.agents/skills/reviewer/SKILL.md) — Used when spawned as the reviewer in the orchestrator pipeline. Reviews against STANDARDS.md.
- [`run-record`](.agents/skills/run-record/SKILL.md) — Used when the orchestrator writes a run record. Owns the scan format (tables, short cells, one idea per row). Keeps human-readability and ease to scan through it a priority.
- [`research-project-agents`](.agents/skills/research-project-agents/SKILL.md) — Analyzes a user-named directory and writes that directory’s AGENTS.md so later coding agents can understand structure and purpose without reading the tree. **Name a target directory**; do not default to this harness.

**User-invoked** (`disable-model-invocation: true` — same flag, different loader: Levi names or invokes; it does not auto-load):

- [`orchestrator`](.agents/skills/orchestrator/SKILL.md) — on-demand pipeline (planner / implementer / reviewer). Not every chat.
- [`architecture-brainstorm`](.agents/skills/architecture-brainstorm/SKILL.md) — software engineering architecture brainstorming: expert engineer in the room, first principles, current research, pushback, tradeoffs. Not a build.
