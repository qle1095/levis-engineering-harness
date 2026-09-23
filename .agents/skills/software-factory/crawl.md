# Crawl

Spawn sub-agents to crawl a target codebase at every real layer. Synthesize their reports and write `AGENTS.md` at each layer so a later coding agent reaches the right solution faster, with fewer wrong turns.

Always `AGENTS.md`. Never `agents.md`.

Richer than [`research-project-agents`](../research-project-agents/SKILL.md): that skill writes one short file for one named directory. Crawl covers every real layer. Do not invoke research-project-agents. Do not use its short Structure / Purpose / Where to look template. Use [`agents-md-template.md`](agents-md-template.md).

## Target

The user must name the target directory. Ask and stop if it is missing, not a directory, or does not exist. Do not default to this harness. The path may be anywhere readable.

## Who writes

| Role | Does | Does not |
| --- | --- | --- |
| **Crawler** sub-agents | Explore a bounded subtree. Return an evidence report. | Write or edit `AGENTS.md`. Invent requirements, product intent, or behavior the code does not show. |
| **This session** | Synthesize reports. Cross-check. Write every `AGENTS.md`. | Let crawlers write the files. |

Mark inferences as inferences. Prefer a model fit for crawling vs synthesis when the session exposes a choice. Do not invent a vendor list.

## Procedure

1. **Map the tree.** Skip vendored deps, generated output, lockfiles, binaries, and VCS metadata. Do not skip source, tests, infra, scripts, configs, ADRs, or existing agent rules.
2. **Name the layers.** A layer is a directory a coding agent would otherwise rediscover: service, package, module, app, library, pipeline, infra stack, or a folder with non-obvious behavior. Cover every layer, including nested ones. Skip empty folders, fixture dumps, and vendored trees. When a directory has real code or a real boundary, it is in scope.
3. **Spawn crawlers in parallel.** One per area a single pass cannot cover well. Bound each crawler to a subtree. Each report must include, from evidence:

| Report field | Evidence for |
| --- | --- |
| Purpose | What this area does |
| Entry points | How work enters |
| Public contracts | Interfaces, APIs, exports |
| Data shapes | Types, schemas, payloads |
| Invariants | What must stay true |
| Call direction | Who calls whom |
| Run / test / build | Commands if evidenced |
| Errors / failure | How it fails |
| Concurrency / state | Shared state, races, locks |
| Config / env | Knobs that matter |
| Footguns | Wrong turns that look right |
| Patterns to copy | How change is done here |
| Out of scope | What does not belong |

Quote paths. No file dump. No invented requirements.

4. **Synthesize.** Prefer merge over wipe when an `AGENTS.md` already exists: keep guidance that still matches the tree; replace guidance the code contradicts. Cross-check crawler reports against each other before writing. Resolve contradictions by reading the code, not by voting.
5. **Write** `AGENTS.md` at each layer using [`agents-md-template.md`](agents-md-template.md). Root file points at nested `AGENTS.md` files so an agent can descend. Nested files state the parent boundary in one line.
6. **Stop** when a coding agent could land a change in that layer without re-learning the footguns, contracts, and ownership the reports already found.

## Expertly done

Do not leave out details that would help a later coding agent reach the right solution. If a section would not change a coding agent's decision, cut it. If cutting it would let them ship the wrong fix, it stays.

## Do / don't

**Don't**

- Default the target to this harness.
- Invent requirements or product intent.
- Let crawlers write `AGENTS.md`.
- Use the research-project-agents short template.
- Skip real layers, nested boundaries, tests, infra, or existing agent rules.
- Write `AGENTS.md` in every empty folder, fixture dump, or vendored tree.
- Use Windows paths.
- Add dates.
- Point at STANDARDS.md.

**Do**

1. Confirm the user-named target exists and is a directory.
2. Map layers; spawn bounded crawlers in parallel.
3. Synthesize here; write every `AGENTS.md` yourself.
4. Merge existing guidance that still matches; fix what the code contradicts.
5. Link nested files from the root; state parent boundary in nested files.
