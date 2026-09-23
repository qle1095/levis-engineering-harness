# Improve

Spawn a team of experts to analyze the target codebase, then research how to make the current code better. "Better" depends on the software type — staff experts who know what better means for *that* type. Also cover the standard lenses that apply.

This command **researches and recommends**. It does **not** implement. Implementation, if the user wants it, is [`orchestrator-e2e`](../orchestrator-e2e/SKILL.md). After the brief, ask. If they say no, tell them to say when.

## Target

The user must name the target directory. Ask and stop if it is missing, not a directory, or does not exist. Do not default to this harness. The path may be anywhere readable.

## Prerequisite

| State | Action |
| --- | --- |
| No `AGENTS.md` anywhere under the target | Run the `crawl` command first ([`crawl.md`](crawl.md)). Do not staff experts on a cold skim. |
| `AGENTS.md` files exist | Read root and nested files before staffing. |

Do not skip the code. `AGENTS.md` can be stale. Experts read the code for every claim they make.

## Who does what

The session running improve is the **coordinator**. It does not implement. It does not pretend to be every expert.

| Role | Does | Does not |
| --- | --- | --- |
| **Expert** sub-agents | Answer a bounded question for this software type. Research current practice. Return findings with evidence. | Edit product code, configs, or `AGENTS.md`. Invent requirements. |
| **This session** | Name the type from evidence. Staff the team. Spawn experts. Synthesize one improvement brief. Ask about implementing. | Implement. Collapse into one generic "make it clean" pass. |

Prefer a model fit for each expert when the session exposes a choice. Do not invent a vendor list. Do not default every expert to this chat's model when a better fit is available. If the session has no model choice, say so and continue.

## Procedure

1. **Confirm the target.** Ask and stop if missing or not a directory.
2. **Prerequisite.** Crawl if needed. Otherwise read existing `AGENTS.md` files.
3. **Name the software type** from root `AGENTS.md`, nested `AGENTS.md`, and enough code to back the label. Do not invent a type.
4. **Staff the team** from that type. Name each expert for what "better" means here (examples only — not a fixed roster): game systems designer, compiler IR specialist, trading latency engineer, CRUD domain modeler, pipeline reliability engineer, mobile client performance engineer, and so on. Always add the standard lenses that apply:

| Lens | When |
| --- | --- |
| Security | Attacker surface, trust boundaries, secrets, authn/z |
| Resiliency | Failure modes, retries, degradation, recovery |
| Scalability | Load, growth, bottlenecks, capacity |
| Performance | Latency, throughput, resource cost |
| Output quality | User-visible or downstream output the software produces |

Skip a standard lens only when it cannot apply, and say why in one line (example: a pure offline batch with no attacker surface — note that; do not invent a threat model).

5. **Spawn experts in parallel.** Each gets: the bounded question, the software type, scale and use cases from `AGENTS.md`, and the paths to read. Each must research current practice:

- Name the systems in play from the target. Do not invent systems the code does not use.
- Search and fetch official docs, RFCs, and vendor current guidance. Prefer those over blogs.
- Do not recommend from memory alone.
- Say what was verified and what was not. If search/fetch fails, say so. Do not invent sources.

6. **Collect findings.** Experts return only. No edits.
7. **Route disagreement.** If two experts conflict on a **fact**, read the code or re-research before recommending. If they conflict on a **goal** the user did not set, ask the user and stop.
8. **Synthesize one improvement brief** (coordinator writes it in chat):

| Section | Content |
| --- | --- |
| What "better" means | In the user's terms, for this software type |
| Prioritized changes | What, why, which evidence, tradeoff, what gets worse if we do it |
| Standard lenses | Security, resiliency, scalability, performance, output quality — where each applies |
| What not to change | Leave alone, and why |
| Open questions | What would change the recommendation — ask; do not assume |

9. **Ask** whether to implement now via `orchestrator-e2e`. If yes, stop and invoke that skill — this session does not become the implementer. If no, say tell me when.

## Do / don't

**Don't**

- Implement in this command.
- Use one generic "make it clean" pass.
- Spawn a fixed roster that ignores the software type.
- Default the target to this harness.
- Invent requirements or a software type the evidence does not support.
- Recommend current practice from memory alone, or invent sources.
- Use Windows paths or dates.
- Point at STANDARDS.md.
- Bake explain-to-levi into improve.

**Do**

1. Confirm the user-named target; crawl if `AGENTS.md` is missing.
2. Name the type from evidence; staff type-specific experts plus applicable standard lenses.
3. Spawn in parallel with bounded questions and research duty.
4. Synthesize one prioritized brief; ask before any implementation.
5. Hand off to `orchestrator-e2e` only when the user says yes.
