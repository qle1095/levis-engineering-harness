## Demand elegance (balanced)

Elegance is part of the bar, but do not over-engineer.

- **Non-trivial changes:** Pause (planner and reviewer) and ask: *is there a more elegant way?* Prefer the design that matches existing architecture with less special-casing, fewer branches, and a clearer name.
- **Hacky fixes:** If a patch works but feels like a workaround, send it back to the implementer with: *knowing everything we know now, implement the elegant solution.* Do not ship the hack.
- **Simple, obvious fixes:** Skip this. A one-line correction, a typo, or a clear follow-the-pattern change does not need an elegance debate.

Elegant means the straightforward solution that belongs in this codebase — not a new abstraction, extra layer, or speculative flexibility.

## Write clear code

- **Comments:** Concise and meaningful. Explain context and *why* — what the surrounding code does not. A reader should follow intent from the comments. Do not narrate what the code already says; do not require a comment on every line.
- **Names:** Functions and variables say what they are. Match surrounding style.
- **Nesting:** Prefer early returns, extraction, and composition over deep nested `if`/`for`. Not a ban — do not force worse code to flatten a short, clear nest.
- **Entry point:** Every program has a clear entry point (`main()` or the language equivalent). This repo is language-agnostic.

## No secrets

- **Secrets:** No secrets, tokens, certs, or credentials in code, diffs, docs, logs, or error payloads.
- **Config:** Put secrets in config or environment variables. Never commit them.
- **Identity:** Log **stable identifiers** (user id, subject id, resource id), not secrets or **PII**.

## Log and handle errors

- **Errors:** Handle failures explicitly (nulls, empty input, timeouts, retries, partial failure where relevant). Do not swallow errors. Do not leak secrets or PII in error payloads (see No secrets).
- **Logs:** Meaningful, useful, not noisy. Use a **structured** log (key/value fields).
- **Audit fields:** Every audit record includes:
  - **What** type of event occurred
  - **When** it occurred — timestamp from internal clocks, UTC or a stated offset from UTC (e.g. UTC-7)
  - **Where** it occurred
  - **Source** of the event
  - **Outcome** of the event
  - **Identity** of associated individuals, subjects, or objects/entities — **stable identifiers only** (see No secrets).

## Changelog and docs

- **Changelog:** When behavior, API, or ops change, update the project's changelog. If none exists, add a short one.
- **Docs:** Create or update docs (including comments/README when behavior or setup changed). Keep them short, precise, human-readable, and easy to scan — the same bar as this file.

## Test when it earns its keep

- Write tests only when they earn their keep. Do not force them. Do not ban them.
- **When:** Real logic or behavior that can regress, or a testable procedure. Then cover the described behavior and the edges that matter.
- **Skip:** Docs-only, policy, obvious one-liners, or a test that would just restate the change. A missing test is not a defect in those cases.
- **If warranted:** Happy path and relevant edges. Compiling / green CI is not enough.
- **Existing tests:** Update ones that still earn their keep. Do not delete them only to make CI green. Do not add tests that do not earn their keep.
- **Fit:** Use the project's existing layout and runner when you do write tests. This repo does not prescribe a framework. This harness has no test suite.

## Review gates

Implementer and reviewer use these checklists.

### Correctness

- **Happy path:** Behaves as described.
- **Edge cases:** Error paths handled (nulls, empty input, timeouts, retries, partial failure).
- **Concurrency:** Races and double-submit considered where relevant.
- **Tests:** Only when they earn their keep (see Test when it earns its keep). If warranted: cover happy path and relevant edges; update existing tests, do not delete them to make CI green. If not warranted: do not reject for missing tests; do not require a tester ritual.

### Security

- **Secrets:** No secrets, tokens, certs, or credentials in the diff.
- **Auth:** AuthN / AuthZ enforced for new or changed endpoints and UI actions.
- **Input:** User input validated; queries parameterized; no injection / XSS / path traversal.
- **Sensitive data:** Not logged or returned in error payloads (see No secrets).

### Operability

- **Defaults:** Config and feature flags have safe defaults.
- **Observability:** Logs / metrics useful and not noisy; no PII.
- **Migrations:** Data backfills reversible, or explicitly one-way with a rollback note.
- **Resources:** CPU, memory, DB, and network usage reasonable for the hot path.

### Maintainability

- **Fit:** Names and structure match the surrounding code.
- **Cleanup:** No leftover debug code, TODOs without a ticket, or dead code.
- **Docs:** Docs, README, or comments updated when behavior or setup changed.
