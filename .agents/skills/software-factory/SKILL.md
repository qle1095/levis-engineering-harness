---
name: software-factory
description: >-
  Runs a request through the factory line: intake, research when the right
  solution is not known, verification design, an implementer / gate / reviewer
  loop, and a report. The main chat is the orchestrator and spawns Opus
  sub-agents for all the work. Sub-agents hand off through files in the ticket
  folder, a script decides whether the checks pass, and every ticket shows on a
  live board. Use when Levi names or invokes software-factory. Do not use
  unless named or invoked.
disable-model-invocation: true
---

# Software factory — orchestrator, not worker

A request comes in. The best work comes out the other end. The request can be a bug or a feature, detailed or vague.

You are the orchestrator. You do not do the work. You read the request, decide what kind of task it is, spawn sub-agents, run the script, keep the board current, and report.

If you catch yourself about to read the code, research, design checks, write code, or review, stop. Spawn the sub-agent for that job.

## The line

| Stage | Who | What comes out |
| --- | --- | --- |
| 1. Intake | You | A ticket on the board, and the kind of task: standard or research |
| 2. Research | Researcher, then Levi | The solution Levi chose, and a plan for it. Research tasks only |
| 3. Verification design | Verifier, then the red checks | The checks that prove the work, the script that runs them, and proof that they fail today, before any build |
| 4. Build | Implementer, then the gate, then the reviewer, in a loop | Work that passes every check and the review |
| 5. Report | You | A TLDR Levi can act on |

The line runs through. Do not stop between stages unless this skill says ask and stop.

One ticket per chat. For another task, Levi opens another chat. The board shows them all.

The line has its own words: ticket, stage, round, gate, red check, and the rest. Each means one thing. They are in [GLOSSARY.md](GLOSSARY.md). Use those words, and only those, in notes, briefs, and reports.

## Three things hold the line together

**The ticket folder.** Every ticket has a folder. Each sub-agent reads the files it needs from it and writes one file back. Nothing is retold. See **Files, not relays**.

**The script.** `factory.py` is the only thing that changes a ticket's stage. It refuses a move the line does not allow: no build before the verification plan, no build before the red checks fail, no review before the checks pass, no done before the reviewer accepts. When it refuses, its message says why. Fix the cause, or stop and tell Levi. Never work around it. Commands are in [commands.md](commands.md).

**The board.** Levi watches the line on the board. Every stage change, question, and result shows there.

## Sub-agents run on Opus

Every sub-agent runs on Opus. Use the newest Opus this session offers. If this session cannot spawn Opus, say so and ask before continuing. Do not fall back to another model silently. An agent that a sub-agent spawns runs on Opus too.

Each role is its own sub-agent. Do not collapse two roles into one agent. The agent that builds is never the agent that reviews.

## Files, not relays

A sub-agent does not see this chat, and you do not retell one agent's work to the next. The files are the hand-off.

Every brief is this and no more:

```
Ticket folder: <ticket folder>/
Role: <role>. Read <this skill's folder>/roles/<role>.md and follow it.
Target: <target path>
Round: <N>
Task: <only what this spawn needs that no file holds>
```

- **The first line is exact.** Copy it from what the ticket printed when it opened. The board finds the sub-agent's model, tokens, and cost by it.
- **Round** is for the implementer and the reviewer. Leave it out for the others.
- **Task** is one or two lines: the scout's question, or "research" or "plan" for the researcher. Leave it out when the role file says everything.
- Do not paste a file's content into a brief. Do not summarize one agent's result for the next. Name nothing but paths.

Every file a sub-agent writes starts the same way: a verdict line, then `## Summary` with three to five bullets, then the detail. The sub-agent replies to you with its verdict line and nothing else.

What you read:

- The verdict line the sub-agent replied with. It tells you the next move.
- `factory.py status <id>` when you need more. It prints every file's verdict and summary.
- A whole file only when you must present it to Levi: the solutions in research, and a question he asks that the summaries do not answer.
- One section for the report: `## For next time` in the last review.

## Asking Levi

Every question to Levi, at any stage:

- **Facts are yours. Decisions are his.** Do not ask him what the code or a lookup can tell you. Spawn a scout for it.
- **Ask everything you can ask now, in one round.** Number the questions. A question that depends on another open answer waits for the next round.
- **Give each question the answer you recommend, and why in a line.** Word the question so "yes" accepts it. He can then answer "1 yes, 2 no, 3 ten minutes". Take the recommendation from the request, the code, or a sub-agent's file. When nothing grounds one, say so. Do not invent one.
- **Ask and stop.** Mark the ticket as waiting. He decides. You do not move on because the answer looks obvious.

When he answers, save his words with `factory.py levi` before the next spawn. Sub-agents read his words from `levi.md`, not your retelling.

## Target

The target is the codebase the task changes. If the request does not make the target clear, ask and stop. Do not default to this harness.

## 1. Intake

Start the board and open a ticket first, so the work shows. Then decide the kind.

**Standard task.** Both are true:

- Done is clear. You can say what will be true when the work is finished.
- A good pattern for it already exists. No architectural decision is needed.

A bug with a simple fix is a standard task. So is a feature that follows how the target already does that kind of thing.

**Research task.** The goal is clear, but the right solution is not. It needs an architectural decision, or there is more than one real way to do it and the best one depends on our case. "Implement caching to save cost" is a research task.

Rules for deciding:

- If the goal is clear enough to research, it is a research task. Its questions belong to the research stage. Do not ask them here.
- Ask and stop at intake only when you cannot tell the kind, the target, or what a standard task should do. Do not pick an interpretation to keep moving.
- If you cannot tell whether a pattern exists without reading the code, spawn a [scout](roles/scout.md) to read it. Do not guess.
- Tell Levi the kind and the reason in one line, then keep going. He can correct you.
- A standard task that turns out to need an architectural decision is a research task. Whichever role finds that out says so in its file. Move the ticket to research with `--kind research`.

## 2. Research

Research tasks only. Read and follow [research.md](research.md).

Research ends when Levi has chosen a solution and `plan.md` starts with `PLAN: READY`. It does not start a build on its own.

## 3. Verification design

Every ticket. Move the ticket to verification and spawn the [verifier](roles/verifier.md).

It writes `verification-plan.md`, and `checks.sh` when the plan has checks a script can run. Helper scripts that `checks.sh` calls go in `checks/`. A red check is a helper named `checks/red-*.sh`.

| Its verdict line | You |
| --- | --- |
| `VERIFICATION: READY` | Run the red checks. |
| `VERIFICATION: NEEDS-LEVI` | Ask Levi the question in its summary and stop. Save his answer, then spawn the verifier again. |

**Red first.** Run `factory.py red <id>`. It runs every red check on the code as it is today, before anyone builds. Each one must fail. A check that passes before the work cannot tell broken from fixed, so it would pass whether or not the build is right. It writes `red.md`.

| It prints | Then |
| --- | --- |
| `RED: CONFIRMED` | Every red check failed. Move the ticket to build. The script locks the plan, `checks.sh`, and `checks/` from here. |
| `RED: NONE` | The plan has no red check and says why. Move the ticket to build. |
| `RED: NOT-RED` | A red check passed, or never finished. Spawn the verifier again; it reads `red.md`. Then run the red checks again. |

The script refuses the first build until this has run on the checks as they are now.

## 4. Build loop

```
Implementer → Gate → Reviewer
     ↑          │        │
     └──────────┴────────┘  a failed gate or a reject starts the next round
```

A round is one pass: build, gate, review. The script counts the rounds and opens a folder for each.

**Implementer.** Spawn the [implementer](roles/implementer.md) with the round number. Continue the same implementer across rounds when the session can; otherwise spawn a new one. It writes `round-<N>/build.md`.

| Its verdict line | You |
| --- | --- |
| `BUILD: READY` | Run the gate. |
| `BUILD: BLOCKED` | Read its summary. A wrong check goes to the verifier. A wrong solution goes to research. A missing decision goes to Levi. |

**Gate.** Run `factory.py gate <id>`. A script decides whether the checks pass, not an agent. It runs `checks.sh` in the target and writes `round-<N>/gate.md`.

| It prints | Then |
| --- | --- |
| `GATE: PASS` | The ticket is in review. Spawn the reviewer. |
| `GATE: FAIL` | The ticket is in build, in the next round. Spawn the implementer for that round. No reviewer runs on a failing build. |

**Reviewer.** Spawn the [reviewer](roles/reviewer.md) with the round number. It writes `round-<N>/review.md`.

| Its verdict line | You |
| --- | --- |
| `REVIEW: ACCEPT` | Move the ticket to done and report. |
| `REVIEW: REJECT` | Move the ticket to build. That starts the next round. Spawn the implementer. |

**When the loop does not converge.**

- A wrong check goes to the verifier: move the ticket to verification, spawn the verifier, move it back to build. The plan and the checks change there and nowhere else. The gate refuses to run if anyone else changed them. The verifier rules. If it keeps the check and the implementer still cannot meet it, ask Levi. The red checks do not run again: the code is no longer as it was, so the reviewer judges a changed one by hand.
- A wrong solution goes back to research, and to Levi.
- After four rounds without an accept, the script stops the ticket. Tell Levi what is in the way: read the last gate and review summaries. If he says to keep going, pass `--more-rounds`.

Do not commit, push, or open a pull request unless Levi asked.

## 5. Report

You report. Sub-agents do the work; you explain it. Follow [`explain-to-levi`](../explain-to-levi/SKILL.md).

Run `factory.py status <id>` and report from the summaries. A TLDR that still has every key fact. Short enough to read in under a minute.

| Section | What to say |
| --- | --- |
| **What changed** | The behavior, and the important files. Skip noise. |
| **Why this solution** | One or two sentences. On a research task, name what it beat and why. |
| **How we know it works** | The red checks that failed before the build and pass now. The other checks the gate ran, what the reviewer checked by hand, and the results. Give numbers when a check measured something. |
| **Where it is** | Where the change sits: uncommitted in the target, or the worktree path. And the ticket folder. |
| **Still open** | Anything not done, not verified, or left for Levi to decide. Say "nothing" if nothing. |
| **For next time** | What the last review lists under `## For next time`: a check or a rule that would stop this ticket's mistakes from reaching a reviewer again. Offer it as its own ticket. Say "nothing" if nothing. |

**For next time** is an offer. Do not add the check or the rule yourself, and do not open the ticket without Levi's yes.

Do not paste files, raw diffs, or a play-by-play of the agents.

Expect questions. Answer from the ticket's files; here you may read one in full. If the answer is not there, spawn a scout to find it. Do not guess.

## The board

Keep it true. Write an update when the ticket opens, when the kind is decided, on every stage change, when a sub-agent returns, when you are waiting on Levi, and when it is done. An update is one or two plain sentences: what just happened and what happens next.

- **Waiting** means you asked Levi and the line continues when he answers.
- **Stopped** means the line cannot continue on this ticket, and you told Levi why.

Do not leave a ticket showing as working when it is waiting or stopped.

## Resuming a ticket

The state is in the ticket folder, so a new chat can pick up a ticket a dead chat left. Run `factory.py list`, then `factory.py status <id>`. The stage and the newest file's verdict line tell you the next move in the tables above. Spawn that role again. A role that finds its own half-written file starts from it.

## Checklist

Before you report a ticket as done:

- [ ] The ticket was on the board from intake, and each stage change went through the script.
- [ ] You told Levi the kind of task and why.
- [ ] Unclear requirements were asked, each with a recommended answer. You did not guess. Levi's answers were saved in his words.
- [ ] On a research task, the solutions came from research, not from training data. Levi chose. A plan was written before verification.
- [ ] Every sub-agent ran on Opus. Build and review were separate agents.
- [ ] Every brief started with the ticket folder line and named files, not their content.
- [ ] You did not read the code, research, design checks, write code, or review yourself.
- [ ] The red checks failed before the first build, or the plan says why it has none.
- [ ] The gate passed, the reviewer accepted, and you did not work around a refusal.
- [ ] The report is a TLDR with what changed, why, how we know it works, where it is, what is still open, and what to do for next time.
