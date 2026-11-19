# Research stage

For research tasks. The right solution is not known yet. Do not guess it. Do not answer it from training data. Training data rots, and it does not know our case.

Move the ticket to research with `--kind research`. Every step below hands off through files in the ticket folder. See **Files, not relays** in [SKILL.md](SKILL.md).

## 1. Ask Levi first

Ask the questions whose answers change the solution: the goal and its number, the constraints, what is off limits. Ask as many as the problem needs. Short and specific.

Ask only what the code cannot tell you. If a question is about the code — where the cost is, how a path works today — spawn a [scout](roles/scout.md) with that question. Then ask Levi the rest.

Ask and stop. Mark the ticket as waiting.

When he answers, save his words with `factory.py levi` before anything else.

## 2. Spawn the researcher

One lead [researcher](roles/researcher.md), with Task `research`. When the problem splits into separate subjects, the lead spawns its own researchers and stays responsible for one answer.

Use a sub-agent that can search the web, read the code, and spawn further agents.

It writes `solution.md`.

| Its verdict line | You |
| --- | --- |
| `RESEARCH: READY` | Go to step 3. |
| `RESEARCH: NEEDS-LEVI` | Ask Levi the questions in its summary and stop. Save his answers, then spawn the researcher again. |

A claim about current practice with no source is not done. Send the researcher back. Do not repair it from memory.

## 3. Present to Levi

Read `solution.md` in full. This is one of the few files you read whole, because Levi has to choose from it.

The ranking and the recommendation are the researcher's. You present them. Do not re-rank from your own knowledge.

Follow [`explain-to-levi`](../explain-to-levi/SKILL.md). Lead with the recommendation and the reason. Then one table, one row per solution, easy wording, so he can read across and compare.

Then one of these, as the researcher's file says:

- **The best cannot be known without building.** Say why. Ask which solutions he wants built so they can be compared.
- **The best can be chosen on paper.** Explain the decision in the table. Let Levi decide the next step.

Ask and stop. Mark the ticket as waiting. He decides. You do not start a build because the answer looks obvious.

Save his choice with `factory.py levi --about "Which solution"`.

## 4. After Levi chooses

### One solution

Spawn the researcher again, with Task `plan`. Continue the same researcher when the session can. It writes `plan.md`: the plan the implementer will execute.

| Its verdict line | You |
| --- | --- |
| `PLAN: READY` | Move the ticket to verification. |
| `PLAN: NEEDS-LEVI` | Ask Levi the question in its summary and stop. Save his answer, then spawn the researcher again. |

### Several solutions to compare

Build each one and measure.

1. Open one ticket for each solution with `factory.py new --parent <this ticket> --title "<request>: <solution>"`. Give each its own git worktree of the target as `--target`. Two implementers never share a working tree. A solution ticket starts in research with this ticket's request, Levi's words, and `solution.md`.
2. For each solution ticket, spawn the researcher with Task `plan`. The Task names which solution that ticket builds.
3. Spawn one verifier for all of them. Its Task lists every solution ticket's folder. It writes the same `verification-plan.md` and `checks.sh` into each. The plan includes the measure that decides the winner, and the baseline taken before any build.
4. Run each solution ticket through the build loop, with its own implementer and its own reviewer. Leave each worktree uncommitted.
5. This ticket stays in research and waits. Say on the board which tickets it waits for.

When every solution ticket is done, read each one's last `gate.md` and `review.md` summaries. Present the results in one table with the measured numbers. Levi picks the winner. Save his words.

The winner's worktree is the result. Report it. Leave the other worktrees in place and list their paths under **Still open**. Then move this ticket to done.
