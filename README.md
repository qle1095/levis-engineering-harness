# levis-engineering-harness

**Levi's engineering harness** is docs and Agent Skills only, **not an application**. It guides coding agents. Open this working space in **Cursor or Codex**.

## How it is used

Name or invoke [`orchestrator-e2e`](.agents/skills/orchestrator-e2e/SKILL.md) for a planner / implementer / reviewer pipeline that runs through. It is user-invoked, not every chat. When it runs, this session is not the implementer. It writes one run record using the `run-record` skill, and a conversation artifact for each role. Sub-agents do not.

When spawned, the **implementer** and **reviewer** load their skills and follow [STANDARDS.md](STANDARDS.md).

To orient later coding agents on another tree, name a target directory and use [`research-project-agents`](.agents/skills/research-project-agents/SKILL.md). That skill analyzes the named directory and writes that directory’s `AGENTS.md` (structure and purpose).

To brainstorm software engineering architecture, name or invoke [`architecture-brainstorm`](.agents/skills/architecture-brainstorm/SKILL.md). That is a conversation with an expert engineer, not a pipeline role and not a build.

Name or invoke [`software-factory`](.agents/skills/software-factory/SKILL.md) to build or refresh a factory of `AGENTS.md` files on a named target. Not this harness unless they asked about the harness. Not a product build; implementation is orchestrator-e2e when they say yes.

Name or invoke [`spawn-specialist`](.agents/skills/spawn-specialist/SKILL.md) to hand the ask to one expert on that subject. This session briefs; it does not answer. For questions that might change with time, the specialist researches first and does not use pre-trained data for the answer. Stable facts such as math do not need a fresh lookup. It may spawn more sub-agents if it needs to. Those agents follow the same split.

When explaining anything to Levi, follow [`explain-to-levi`](.agents/skills/explain-to-levi/SKILL.md). That skill loads for explanation, not only when he names it.

## Docs

- [AGENTS.md](AGENTS.md) — Docs/skills harness; name or invoke orchestrator-e2e.
- [STANDARDS.md](STANDARDS.md) — Elegance, surgical changes, clear code, secrets, errors/logs/audit, changelog/docs, when to test, and review gates.
- [CHANGELOG.md](CHANGELOG.md) — Project changelog.

## Skills

Skills live under `.agents/skills/`. Cursor, Codex, and other Agent Skills–compatible harnesses load them from this path.

- [`bible`](.agents/skills/bible/SKILL.md) — creates the specialists needed for the ask, gives each concise project memory in its own folder, and uses `/goal` to deliver and verify the result.

**Pipeline-only** (`disable-model-invocation: true` — the agent/pipeline loads them; the user does **not** slash-invoke them):

- [`implementer`](.agents/skills/implementer/SKILL.md) — Used when spawned as the implementer in the orchestrator-e2e pipeline. Executes the plan; follows STANDARDS.md.
- [`reviewer`](.agents/skills/reviewer/SKILL.md) — Used when spawned as the reviewer in the orchestrator-e2e pipeline. Reviews against STANDARDS.md.
- [`run-record`](.agents/skills/run-record/SKILL.md) — Used when orchestrator-e2e writes a run record. Owns the scan format (tables, short cells, one idea per row) and the conversation artifact beside each turn. Keeps human-readability and ease to scan through it a priority.
- [`research-project-agents`](.agents/skills/research-project-agents/SKILL.md) — Analyzes a user-named directory and writes that directory’s AGENTS.md so later coding agents can understand structure and purpose without reading the tree. **Name a target directory**; do not default to this harness.

**Every chat** (no `disable-model-invocation` — loads when explaining anything to Levi):

- [`explain-to-levi`](.agents/skills/explain-to-levi/SKILL.md) — How to explain so it clicks. When it does not, think from first principles about what would help Levi understand this, instead of matching a list of past misses.

**User-invoked** (`disable-model-invocation: true` — same flag, different loader: Levi names or invokes; it does not auto-load):

- [`orchestrator-e2e`](.agents/skills/orchestrator-e2e/SKILL.md) — on-demand pipeline (planner / implementer / reviewer) that runs through. Each role's conversation is a run-record artifact. Not every chat.
- [`architecture-brainstorm`](.agents/skills/architecture-brainstorm/SKILL.md) — software engineering architecture brainstorming: expert engineer in the room, first principles, current research, pushback, tradeoffs. Not a build.
- [`software-factory`](.agents/skills/software-factory/SKILL.md) — builds a factory of AGENTS.md files so later coding agents can read them, build, and improve. Not a product build. Commands: init, crawl, improve, explain.
- [`spawn-specialist`](.agents/skills/spawn-specialist/SKILL.md) — understands the ask, then spawns one expert on that subject with a full brief. For questions that might change with time, the specialist researches first and never uses pre-trained data for the answer. Stable facts such as math do not need a fresh lookup. It may spawn more sub-agents if it needs to.
