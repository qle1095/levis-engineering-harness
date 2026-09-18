# levis-engineering-harness

**Levi's engineering harness** is docs and Agent Skills only, **not an application**. It guides coding agents. Open this working space in **Cursor or Codex**.

## How it is used

The **orchestrator** follows [AGENTS.md](AGENTS.md). It is not the implementer.

When spawned, the **implementer** and **reviewer** load their skills and follow [STANDARDS.md](STANDARDS.md).

To orient later coding agents on another tree, name a target directory and use [`research-project-agents`](.agents/skills/research-project-agents/SKILL.md). That skill analyzes the named directory and writes that directory’s `AGENTS.md` (structure and purpose).

## Docs

- [AGENTS.md](AGENTS.md) — Orchestrator rules: allowed models, orchestrator is not the implementer, default pipeline, improvement loop, and report-back.
- [STANDARDS.md](STANDARDS.md) — Elegance, clear code, secrets, errors/logs/audit, changelog/docs, tests, and review gates.
- [CHANGELOG.md](CHANGELOG.md) — Project changelog.

## Skills

Skills live under `.agents/skills/`. Cursor, Codex, and other Agent Skills–compatible harnesses load them from this path.

All three are pipeline-only (`disable-model-invocation: true` — the agent/pipeline loads them; the user does **not** slash-invoke them):

- [`implementer`](.agents/skills/implementer/SKILL.md) — Used when spawned as the implementer in the AGENTS.md pipeline. Executes the plan; follows STANDARDS.md.
- [`reviewer`](.agents/skills/reviewer/SKILL.md) — Used when spawned as the reviewer in the AGENTS.md pipeline. Reviews against STANDARDS.md.
- [`research-project-agents`](.agents/skills/research-project-agents/SKILL.md) — Analyzes a user-named directory and writes that directory’s AGENTS.md so later coding agents can understand structure and purpose without reading the tree. **Name a target directory**; do not default to this harness.
