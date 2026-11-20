# Software factory glossary

The words of the line. Each word means one thing. Use these words, and only these, in notes, briefs, files, and reports. When someone uses a word under _Avoid_, answer with the word in bold.

Only words special to the factory are here. This file says what each thing is. How to use it is in [SKILL.md](SKILL.md) and [commands.md](commands.md).

## The work

**Request**:
What Levi pasted, in his words. Saved as `request.md`.
_Avoid_: prompt, ask, task description

**Ticket**:
One request on the line, from intake to done. It has an id, a ticket folder, and a row on the board.
_Avoid_: job, issue, run, task (a task is what the request asks for; the ticket carries it)

**Solution ticket**:
A ticket opened under a research ticket to build one of its solutions, so several can be measured side by side.
_Avoid_: child ticket, sub-ticket, variant

**Target**:
The codebase the ticket changes.
_Avoid_: repo, project, workspace

**Kind**:
What sort of task the request is. There are two: standard task and research task. Intake decides it.
_Avoid_: type, category, size

**Standard task**:
A task where done is clear and a good pattern for it already exists in the target. It skips research.
_Avoid_: simple task, small task, easy task

**Research task**:
A task where the goal is clear but the right solution is not. It needs an architectural decision, or has more than one real way to do it.
_Avoid_: vague task, complex task, big task

## The line

**Line**:
The fixed order of stages a ticket passes through.
_Avoid_: workflow, process, flow

**Stage**:
Where a ticket is on the line: intake, research, verification, build, review, or done.
_Avoid_: step, phase, status

**State**:
Whether the work is moving: working, waiting, stopped, or done. Waiting means the orchestrator asked Levi and the line continues when he answers. Stopped means the line cannot continue and Levi was told why. The board shows a working ticket as quiet after twenty minutes with no update.
_Avoid_: status, blocked, paused

**Move**:
A change of stage. Only the script makes one, and it refuses a move the line does not allow.
_Avoid_: transition, advance, promote

**Round**:
One pass of build, gate, and review. A ticket gets four rounds before the line stops and asks Levi.
_Avoid_: iteration, attempt, turn, cycle, loop

**Update**:
One or two plain sentences on the board: what just happened and what happens next.
_Avoid_: log, comment, status

**Board**:
The live page that shows every ticket, its stage, its state, and its cost.
_Avoid_: dashboard, UI, monitor

**Pipeline**:
The board's drawing of the line in a ticket's row: one node per stage. A word for the picture only, not for the line.

## Who does what

**Orchestrator**:
The main chat. It sorts the request, spawns sub-agents, runs the script, keeps the board true, and reports. It does none of the work.
_Avoid_: main agent, coordinator, manager

**Sub-agent**:
An Opus agent the orchestrator spawns for one role on one ticket.
_Avoid_: worker, specialist, agent (alone)

**Role**:
The one job a sub-agent has. There are five, each with a file under `roles/`.

- **Scout**: reads the target and reports what is there. _Avoid_: explorer
- **Researcher**: finds and ranks the solutions for a research task, then writes the plan. _Avoid_: architect, analyst
- **Verifier**: decides the checks before any build. _Avoid_: specialist, tester, QA
- **Implementer**: builds the ticket in the target. _Avoid_: builder, developer, coder
- **Reviewer**: judges what a script cannot. It did not build. _Avoid_: critic, auditor

## The hand-off

**Ticket folder**:
The folder that holds everything about one ticket. Sub-agents hand off through its files. It sits outside the target.
_Avoid_: workspace, run folder, scratch

**Brief**:
The few lines that start a sub-agent: the ticket folder, the role, the target, the round, the task. It names paths and carries no content.
_Avoid_: prompt, instructions, context

**Verdict line**:
The first line of a file a sub-agent or the script writes, such as `REVIEW: ACCEPT`. It tells the orchestrator the next move.
_Avoid_: status line, header, result

**Summary**:
The three to five bullets under the verdict line of a file.
_Avoid_: overview, abstract (and never for what Levi gets at the end; that is the report)

**Levi's words**:
His answers and decisions, saved as he typed them in `levi.md`.
_Avoid_: requirements, feedback, notes

**Report**:
What the orchestrator tells Levi when the ticket is done.
_Avoid_: summary, write-up, recap

## The proof

**Plan**:
`plan.md`: how the solution Levi chose will be built. Research tasks only.
_Avoid_: spec, design, proposal

**Verification plan**:
`verification-plan.md`: the checks that prove the work, decided before any build. Always say "verification plan", never "plan" alone.
_Avoid_: test plan, spec, acceptance criteria

**Check**:
One way to prove the work, named in the verification plan. The gate runs it, or the reviewer does it by hand.
_Avoid_: validation, assertion, test (a test is one kind of check)

**Red check**:
A check script, `checks/red-*.sh`, that must fail on the code as it is before the build and pass after it. It proves the check can tell broken from fixed.
_Avoid_: failing test, repro, smoke test

**Red first**:
The rule that every red check is run, and fails, before the first build.
_Avoid_: TDD, red-green

**Gate**:
The script run that decides whether a build passes its checks. Not an agent.
_Avoid_: CI, test run, validation

**Lock**:
From the first build on, the verification plan and the checks change only through the verifier. The gate refuses to run if anything else changed them.
_Avoid_: freeze, protect

**Review**:
The reviewer's verdict on one round: accept or reject, with findings.
_Avoid_: audit, critique, QA

**Finding**:
One thing the reviewer says must change before it accepts.
_Avoid_: issue, comment, nit

## Settled

- **"Vague task"** was the first name for a research task. The goal of a research task is clear; only the solution is open. Use **research task**.
- **"Specialist"** was the first name for the verifier. Use **verifier**.
- **"Plan"** names two files. Say **plan** for `plan.md` and **verification plan** for `verification-plan.md`.
- **"Summary"** is the bullets in a file. What Levi reads at the end is the **report**.
- **"Pass"** is what a gate does. One trip through build, gate, and review is a **round**.
