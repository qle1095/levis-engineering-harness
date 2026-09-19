---
name: run-record
description: Owns the scan format for pipeline run records at docs/runs/: tables, short cells, one idea per row. Keeps human-readability and ease to scan through it a priority. Use when the orchestrator writes or appends a run record after a spawned role returns. Do not use when implementing product work or when spawned as implementer or reviewer.
disable-model-invocation: true
---

# Run record

Keeps human-readability and ease to scan through it a priority.

## Look

- Tables. Short cells. One idea per row.
- Repeat the field when one label has several ideas.
- Long **Changed** is not one paragraph. The same path may appear on more than one row.
- Packed **Must change** → one row per fix, not `(1) (2) (3)` in one cell.
- Easy wording. Condense dumps. No transcripts, raw diffs, play-by-play, secrets/PII.
- Unlabeled two-column tables (`| | |` / `|---|---|`) with **bold** field names.
- No mermaid. No `## Roles`, `## Loop`, `## Not done`, mutating Status.

## File shape

**Header** (once):

```markdown
# <short title>

| | |
|---|---|
| **Request** | one line of user intent |
| **Record** | `docs/runs/YYYY-MM-DD-short-name.md` |
```

**Intent** — table, not bullets. Repeat **Asked** / **Locked** per idea. Omit **Locked** if none.

```markdown
## Intent

| | |
|---|---|
| **Asked** | what was asked |
| **Locked** | one constraint |
```

Each turn is a heading plus a two-column table (`## Turn N — <Role>`; reviewer/tester put the verdict in the heading).

Planner — omit **Not doing** if none; one rejected path per **Not doing** row:

```markdown
## Turn 1 — Planner

| | |
|---|---|
| **Found** | … |
| **Plan** | … |
| **Why** | … |
| **Not doing** | … |
```

Implementer — no **Changed** paragraph; repeat the path per idea:

```markdown
## Turn 2 — Implementer

| | |
|---|---|
| `AGENTS.md` | one idea |
| `AGENTS.md` | another idea |
| `CHANGELOG.md` | what changed there |
| **Why** | … |
```

Reviewer / tester — Accept:

```markdown
## Turn 5 — Reviewer — Accept

| | |
|---|---|
| **Verdict** | Accept |
| **Why** | … |
```

Reviewer / tester — Reject — one **Must change** row per fix:

```markdown
## Turn 3 — Reviewer — Reject

| | |
|---|---|
| **Verdict** | Reject |
| **Why** | … |
| **Must change** | one required fix |
| **Who next** | Implementer |
```

Extra role: **Found** or path rows, **Why**, **Verdict** if they judged.

User lock: `## Turn N — User lock`, rows of **Locked**.

## Bad

```
## Turn 4 — Implementer
**Changed:** `AGENTS.md` Run record now states rules once: “still applies”; When-and-where is one statement each; no-rewrite lives only in the scan rules; Accept does not erase Reject (no Loop qualifier). Report back lead-in says “chat **Status**.” CHANGELOG left as-is.
**Why:** Reviewer asked for rules, not edit history, and one statement of each constraint.
```

## Good

```markdown
## Turn 4 — Implementer

| | |
|---|---|
| `AGENTS.md` | Run record states rules once: “still applies” |
| `AGENTS.md` | When-and-where is one statement each |
| `AGENTS.md` | no-rewrite only in the scan rules |
| `AGENTS.md` | Accept does not erase Reject |
| `AGENTS.md` | Report back lead-in says “chat **Status**” |
| `CHANGELOG.md` | left as-is |
| **Why** | Reviewer asked for rules, not edit history, and one statement of each constraint |
```

Orchestrator skill owns when/where/who-writes/append-only/spawn-return. Do not copy those process rules here. Look templates stay.
