# Explain

Help someone looking at a codebase for the first time understand it. The explanation is for Levi. Synthesize with [`explain-to-levi`](../explain-to-levi/SKILL.md) — read that skill and follow it. Do not skip it.

Cover, in an order a first reader can use:

1. What this repo is
2. What it is trying to accomplish
3. Overall architecture
4. Current state: what is good, what is bad

The goal is understanding. Not a status dashboard, not a file tour, not a score.

## Target

The user must name the target directory, or clearly mean the workspace they have open ("this repo").

- If they mean the open workspace and that workspace is this harness, ask which project — do not explain this harness unless they asked about the harness.
- If the target is missing and not clearly the open workspace, ask and stop.
- Do not default to this harness.

The path may be anywhere readable. Confirm it exists and is a directory.

## Procedure

1. **Find** `AGENTS.md` files in the target. The filename is `AGENTS.md`.
2. **If any exist**, run the software-factory [`crawl`](crawl.md) command first so those files match the code, then read them (root and the nested ones the architecture requires). Do not explain from stale factory docs.
3. **If none exist**, still run `crawl` before explaining. A first-time explanation with no layer docs would be a cold skim; the goal is an expert read. Say that you are crawling because there is no `AGENTS.md` yet.
4. **After crawl**, read the `AGENTS.md` files. Read code only where a claim is missing or the docs disagree. Do not re-crawl by hand in this session.
5. **Synthesize** with explain-to-levi. Read `.agents/skills/explain-to-levi/SKILL.md` (when this skill runs inside the harness, that path; when explaining another repo, the skill still applies — read it from the harness that loaded software-factory).

## How the explanation lands

This must match explain-to-levi, not replace it:

- **First sentence:** what this repo does for a person using it, or what problem it exists to solve. Plain English.
- **Then** what it is trying to accomplish.
- **Then** the architecture as a path a change would take — where work enters, who owns it, what must stay true. One concrete example from the tree ("if you changed X, you would start at Y").
- **Then** current state: what is in good shape, what is weak or risky, tied to evidence (a path, a missing contract, a footgun already in `AGENTS.md`). Good and bad are judgments a newcomer needs, not a style nit list.
- If you do not know, say so. Do not invent purpose the code and docs do not support.

## Do not

- Skip explain-to-levi.
- Dump a tree listing or a table of every package as the explanation.
- Implement changes in this command.
- Default the target to this harness.
- Use Windows paths or dates.
- Point at STANDARDS.md.
