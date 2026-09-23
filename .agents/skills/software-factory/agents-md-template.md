# AGENTS.md for a layer

Required shape of a layer `AGENTS.md`. Filename always `AGENTS.md`. Never `agents.md`.

Not a README clone. Not a file listing. Write only what a coding agent needs to land the right change faster.

## Expertly done bar

If a section would not change a coding agent's decision, cut it. If cutting it would let them ship the wrong fix, it stays. Do not emit empty sections.

## Required sections (order)

### 1. Title and one-line purpose

```markdown
# <layer name>

<One line: what this layer is for.>
```

Nested files: after the one-liner, state the parent boundary in one line (e.g. parent of `services/api` is the repo root / `services`).

### 2. Owns

```markdown
## Owns

- What belongs here.
```

### 3. Does not own

```markdown
## Does not own

- What must not be done here.
```

### 4. Contracts

```markdown
## Contracts

- Public interfaces, data shapes, invariants.
```

Only what exists — or, during init bootstrap, what the architect locked. No invented requirements.

### 5. How to change

```markdown
## How to change

- Patterns to copy, entry points, commands, tests, migration notes.
```

From evidence only.

### 6. Footguns

```markdown
## Footguns

- Mistakes that produce the wrong solution.
```

### 7. Where to look

```markdown
## Where to look

- Paths that matter.
- Nested `AGENTS.md` links (root and parents point down).
```

## Optional (only when evidenced)

Emit only if the report has real content. Do not stub.

| Section | When |
| --- | --- |
| `## Runtime` | How it runs in production or local, if evidenced |
| `## Scale` | Limits, sharding, throughput notes that change design |
| `## Failure` | Failure modes, retries, degradation that change the fix |

## Do not

- Clone README into `AGENTS.md`.
- Dump every file path.
- Invent requirements or product intent.
- Emit empty optional sections.
- Use Windows paths.
- Add dates.
- Point at STANDARDS.md.
- Use the short Structure / Purpose / Where to look-only shape from research-project-agents.
