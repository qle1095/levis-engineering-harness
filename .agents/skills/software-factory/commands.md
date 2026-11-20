# The factory script

`factory.py` is in the `board` folder beside this file. It needs Python 3 and nothing else. The commands below use `<board>` for that folder's path.

It does five jobs: it keeps each ticket's state, it refuses a move the line does not allow, it runs the red checks, it runs the gate, and it serves the live board.

## Start the board

Once per session, before the first ticket. Run it in the background:

```bash
python3 <board>/factory.py serve
```

It prints the address, `http://127.0.0.1:4747`. Give Levi the address once. If the board is already running, the command says so and exits. That is fine.

## Open a ticket

At intake, before anything else:

```bash
python3 <board>/factory.py new --title "Cache product lookups" --target /path/to/codebase --request - <<'REQUEST'
the request, in Levi's words
REQUEST
```

`--title` is a few words that name the request. `--request -` reads the request from the lines that follow, so a long pasted prompt needs no quoting. The request is saved as `request.md` in the ticket folder, and sub-agents read it from there.

It prints the ticket id, the ticket folder, and the line that starts every brief. Keep all three.

`--parent <id>` opens a ticket that builds one solution of a research ticket. It takes no `--request`. See [research.md](research.md).

## Write an update, or move the ticket

```bash
python3 <board>/factory.py update <id> --note "what just happened and what happens next"
```

| Flag | Values | When |
| --- | --- | --- |
| `--kind` | `standard`, `research` | When you decide the kind, or when a standard task turns out to be a research task |
| `--stage` | `research`, `verification`, `build`, `done` | When the ticket moves to that stage |
| `--state` | `waiting`, `stopped` | `waiting` when you asked Levi and the line continues when he answers. `stopped` when the line cannot continue on this ticket |
| `--target` | a path | When the target was not known at intake |
| `--title` | a few words | When the first title turned out wrong |
| `--more-rounds` | | When the ticket hit the round limit and Levi said to keep going |

- `--note` is required. One or two plain sentences Levi can read without the chat. "Reviewer rejected: the retry test passes even with retries off. Back to the implementer." Not "Turn 4 complete."
- An update without `--state` shows the ticket as working. So after Levi answers, the next update clears `waiting` on its own.
- A ticket that shows as working with no update for twenty minutes turns quiet on the board. Write an update when a long sub-agent returns.
- A sub-agent may post its own progress on a long job, with `--note` only. Stage, state, and kind are yours.
- No secrets, tokens, or personal data in a title, request, or note. If the request holds a secret, leave it out of the ticket.

## The moves the script allows

| From | To | The script requires |
| --- | --- | --- |
| intake | research | `--kind research` |
| intake | verification | `--kind standard` |
| research | verification | `plan.md` starts with `PLAN: READY` |
| research | done | The ticket has solution tickets, and each one is done |
| verification | build | `verification-plan.md` starts with `VERIFICATION: READY`. Before the first build, `red` has run on the checks as they are now and did not print `NOT-RED`. The plan, `checks.sh`, and `checks/` are locked from here |
| build | review | Only the gate does this. `--stage review` is refused |
| review | build | This round's `review.md` starts with `REVIEW: REJECT`. Starts the next round |
| review | done | This round's `review.md` starts with `REVIEW: ACCEPT` |
| build or review | verification | Nothing. For a wrong check |
| verification, build, or review | research | `--kind research`. For a wrong solution, or a standard task that needs a decision |

Anything else is refused, and the message says why. Fix the cause. Do not work around it, and do not edit `ticket.json` by hand.

Each time a ticket enters build, a new round starts and the script makes its folder. After four rounds without an accept the script refuses another and the ticket stops.

## Save what Levi said

```bash
python3 <board>/factory.py levi <id> --about "Which solution" - <<'LEVI'
his words, as he typed them
LEVI
```

It appends to `levi.md` in the ticket folder. Every role reads that file. Save his words before the next spawn, and do not tidy them.

## Run the red checks

When the verifier replies `VERIFICATION: READY`, before the first build:

```bash
python3 <board>/factory.py red <id>
```

It runs each `checks/red-*.sh` with `bash`, from the root of the ticket's target, on the code as it is today. Each one must fail.

- **`RED: CONFIRMED`**: every red check failed. The move to build is now allowed.
- **`RED: NONE`**: the plan has no red check and gives the reason under `## Red first`. The move to build is allowed.
- **`RED: NOT-RED`**: a red check passed, or never finished. The move to build stays refused. Only the verifier fixes a check.
- It writes `red.md` with one row per red check and the last lines of output, and `red.log` with all of it.
- It refuses a red check that `checks.sh` does not call, and a plan with no red check and no reason.
- If the plan or the checks change afterwards, run it again. The script refuses the build until it has.
- It runs only before the first build. Once a build has started the code is no longer broken, so there is nothing to try a red check against.
- A red check that runs longer than thirty minutes is stopped and counts as not red. `--timeout <seconds>` changes that.

## Run the gate

When the implementer replies `BUILD: READY`:

```bash
python3 <board>/factory.py gate <id>
```

It runs the ticket's `checks.sh` with `bash`, from the root of the ticket's target, and prints `GATE: PASS` or `GATE: FAIL`.

- **PASS** moves the ticket to review.
- **FAIL** keeps the ticket in build and starts the next round.
- Either way it writes `round-<N>/gate.md` with the result and the last lines of output, and `round-<N>/gate.log` with all of it.
- A plan with no automated checks has no `checks.sh`. The gate passes with nothing run, and the reviewer does the plan's checks by hand.
- It refuses to run when `verification-plan.md`, `checks.sh`, or anything in `checks/` changed after the build started. Only the verifier changes them: move the ticket to verification, spawn the verifier, move it back to build.
- Checks that run longer than thirty minutes are stopped and fail. `--timeout <seconds>` changes that. Run a slow gate in the background.

## See where a ticket is

```bash
python3 <board>/factory.py status <id>
```

It prints the kind, stage, state, and round, then every file in the ticket folder with its verdict line and its summary bullets. Use it in place of opening the files: to decide the next move, to resume a ticket, and to write the report.

```bash
python3 <board>/factory.py list
```

## The ticket folder

Each ticket has its own folder, `~/.software-factory/tickets/<id>/`, outside the target. Nothing in it is committed with the work.

| File | Written by | What |
| --- | --- | --- |
| `ticket.json` | the script | The ticket's state. The board reads it |
| `request.md` | the script, at `new` | The request in Levi's words |
| `levi.md` | the script, at `levi` | Levi's answers and decisions, in his words |
| `scout-<topic>.md` | scout | What the code shows |
| `solution.md` | researcher | The ranked solutions. Research tasks only |
| `plan.md` | researcher | The plan for the solution Levi chose. Research tasks only |
| `verification-plan.md` | verifier | The checks. Locked when the build starts |
| `checks.sh` | verifier | The script the gate runs. Locked when the build starts |
| `checks/*` | verifier | Helper scripts `checks.sh` calls: a probe, a measuring script. Locked when the build starts |
| `checks/red-*.sh` | verifier | The red checks: probes that must fail before the build and pass at the gate |
| `red.md`, `red.log` | the script, at `red` | What each red check did before the build |
| `round-<N>/build.md` | implementer | What was built in round N |
| `round-<N>/gate.md`, `gate.log` | the script, at `gate` | The checks' result and output |
| `round-<N>/review.md` | reviewer | The verdict and the findings |

You write none of these yourself. The script writes its own, and each sub-agent writes one.

## Cost, tokens, and model

The board shows what each ticket has cost so far, the tokens used, the time on the line, and the model. Open a ticket to see one row per sub-agent.

You do nothing to record it. Claude Code writes each sub-agent's model and token counts to its transcript. The board finds the transcripts whose brief starts with the ticket folder line and prices them from `prices.json` beside `factory.py`.

Know what the number is:

- It is the API list price of the sub-agents. On a subscription it shows relative spend, not a bill.
- The orchestrator chat is not counted.
- It needs Claude Code. In a harness that does not write those transcripts, the board shows no cost.
- A model missing from `prices.json` shows as having no price. Add it there.
- When a ticket is marked done, its totals are saved in the ticket, because Claude Code deletes old transcripts.

## Tests

The script has tests. Run them from the `board` folder after changing it:

```bash
python3 -m unittest test_factory
```
