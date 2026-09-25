---
name: run-record
description: Owns the scan format for pipeline run records at docs/runs/: tables, short cells, one idea per row. Keeps human-readability and ease to scan through it a priority. Use when orchestrator-e2e or orchestrator-learning writes or appends a run record after a spawned role returns. Do not use when implementing product work or when spawned as implementer or reviewer.
disable-model-invocation: true
---

# Run record

Keeps human-readability and ease to scan through it a priority.

## Look

- Tables. Short cells. One idea per row.
- Planner turns are four columns. One issue per row. Read across: what was found, what will be done, why that choice, any caveat.
- Implementer turns are four columns. One change per row. Read across: where, the code before, the code after, what that change does.
- Reviewer rejects are four columns. One finding per row. Read across: where, the code and what it does, the required fix, why that fix.
- Other turns stay unlabeled two-column tables (`| | |` / `|---|---|`) with **bold** field names.
- Repeat the field when one label has several ideas, except on a planner, implementer, or reviewer-reject turn.
- Long **Changed** is not one paragraph. The same path may appear on more than one row.
- Packed **Must change** → one row per fix, not `(1) (2) (3)` in one cell.
- Easy wording. Condense dumps. The scan table has no transcripts, raw diffs, or play-by-play. Secrets and PII stay out of both the scan and the conversation files.
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

Each turn is a heading plus a table (`## Turn N — <Role>`; reviewer/tester put the verdict in the heading). Under the heading, one line: `Artifact: docs/runs/<same-name>/turn-N-<role>.md`.

## Conversation artifacts

The scan table is not the conversation. After a role returns, write the sub-agent transcript to `docs/runs/YYYY-MM-DD-short-name/turn-N-role.md`, same name as the scan file, no `.md` on the folder.

Include the prompt, what the agent said, and each tool call (name and input). Skip tool results that are a whole file dump. Do not paste this file into the scan table. Sub-agents do not write it.

Planner — four columns. One issue per row. **Found** cites `file:line`, then enough of the surrounding code that the snippet shows what it is doing without opening the file. Do not quote only the one token that is wrong. Put each snippet line after `<br>` so it stays inside the cell. Then say what happens: the input and the result. **Plan** is the change for that finding. **Why** is why that change, not a reason for the whole plan. **Note** is a caveat for that row; leave the cell empty when there is none. Do not use a **Not doing** column.

```markdown
## Turn 1 — Planner

| Found | Plan | Why | Note |
|---|---|---|---|
| `config.go:47-49`<br>`b, err := os.ReadFile(path)`<br>`if err != nil {`<br>`    panic(err)`<br>`}`<br>If the path is missing, `ReadFile` fails and `panic` stops the program. The caller never gets an error it can handle | Return the read error | A missing file must be an error | Wrap with `%w` so `os.ErrNotExist` still matches |
```

Implementer — four columns. One change per row. **File** is `path:line`. **Before** and **After** quote enough code to see the change without opening the file. Use `<br>` between snippet lines. If the code is new, **Before** says there was none. If it was removed, **After** says it is gone. **Summary** is what the change does.

```markdown
## Turn 2 — Implementer

| File | Before | After | Summary |
|---|---|---|---|
| `config.go:47-49` | `b, err := os.ReadFile(path)`<br>`if err != nil {`<br>`    panic(err)`<br>`}` | `b, err := os.ReadFile(path)`<br>`if err != nil {`<br>`    return nil, fmt.Errorf("read config: %w", err)`<br>`}` | A missing file returns an error. The program does not stop |
```

Reviewer / tester — Accept. The heading carries the verdict. One row is enough when there is nothing to fix.

```markdown
## Turn 5 — Reviewer — Accept

| File | Found | Must change | Why |
|---|---|---|---|
| | Nothing left that fails the plan | | |
```

Reviewer / tester — Reject. The heading carries the verdict. Four columns, one finding per row. **Found** quotes enough code to see the problem, then says what happens. **Must change** is the fix for that row. **Why** is why that fix. Put who does the next edit in one line under the table, not as a repeated row.

```markdown
## Turn 3 — Reviewer — Reject

| File | Found | Must change | Why |
|---|---|---|---|
| `config.go:157-164` | `i := strings.LastIndex(s, ":")`<br>`portStr = s[i+1:]`<br>`a:b:8080` loads. The host `a:b` is ignored because only the text after the last colon is checked | Reject a host that contains `:`, and a port that is not plain digits | `host:port` means one host and one port |

Who next: Implementer
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

| File | Before | After | Summary |
|---|---|---|---|
| `AGENTS.md:12` | `still applies to the report` | `still applies` | The run-record rule is stated once |
```

`orchestrator-e2e` owns when/where/who-writes/append-only/spawn-return. Do not copy those process rules here. Look templates stay.
