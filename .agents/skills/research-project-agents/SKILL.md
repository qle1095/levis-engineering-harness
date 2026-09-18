---
name: research-project-agents
description: analyze files under a user-specified directory; write/update that directory’s AGENTS.md so later coding agents can understand structure and purpose without reading the tree. Requires a named target; does not default to this harness.
disable-model-invocation: true
---

# Write AGENTS.md for a target directory

## Target

The user must name the target directory. Ask and stop if it is missing, not a directory, or does not exist. Do not default to this harness. The path may be anywhere readable.

## Workflow

1. **Research** the tree (see Research).
2. **Write or update** AGENTS.md in that same directory (see Write AGENTS.md).

Two steps only.

## Research

Analyze files under the target: structure (parts and boundaries) and purpose. Not a file dump.

Read as they exist:

- Layout and boundaries
- Entry points
- README — claimed intent vs the tree
- Existing AGENTS.md, `.cursor/rules`, skills, and similar agent files
- ADRs / decision records
- Pipelines

Skip vendored, generated, and lockfile noise.

If the tree is large, spawn sub-agents to explore and analyze in parallel. Synthesize before writing. Sub-agents must not invent requirements or write AGENTS.md.

Stop when the output template can be filled from evidence.

## Write AGENTS.md

Write or update AGENTS.md at the user-named directory. If a nested AGENTS.md exists, mention it under Where to look; do not update the nested file instead.

Prefer merge over wipe: keep guidance that still matches the tree.

Drop leftover `## Domain` and `## Self-Improvement Loop for each project` headings if present.

Not a README clone. Do not copy this harness’s orchestrator AGENTS.md unless that directory actually uses this pipeline.

## Output template

Required order:

1. `# <name>` plus one-line intent
2. `## Structure`
3. `## Purpose`
4. `## Where to look`

Optional: `## Commands`, `## Constraints` if evidenced.

Do not emit `## Domain` or `## Self-Improvement Loop for each project`.

Do not require old Intent / Architecture / Design decisions headings.

## Do not

- Do not default to this harness.
- Do not clone README into AGENTS.md.
- Do not use Windows paths.
- Do not add time-sensitive dates.
- Do not search ancestor directories for another AGENTS.md to follow.
- Do not invent requirements.
- Do not let a sub-agent write AGENTS.md.
- Do not point this skill at STANDARDS.md.
