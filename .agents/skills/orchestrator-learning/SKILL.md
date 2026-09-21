---
name: orchestrator-learning
description: Runs the same planner / implementer / reviewer pipeline as orchestrator-e2e, but stops after each phase. Explains that phase with explain-to-levi, writes a run record when the return tables cleanly, and waits for Levi before the next phase. Use when Levi names or invokes orchestrator-learning. Do not use unless named/invoked.
disable-model-invocation: true
---

# Orchestrator learning

You are **not** the implementer. Read and follow [`orchestrator-e2e`](../orchestrator-e2e/SKILL.md) for ask-first, roles, models, standards, and the end report.

This skill changes the cadence, the explanation, and when a run record is written.

## One phase, then stop

After each spawned role returns:

1. Explain this phase by reading and following [`explain-to-levi`](../explain-to-levi/SKILL.md). Do not copy that skill here. Say what this phase found or changed, why, and what the next phase would do.
2. If that return can be scanned as run-record tables — short cells, one idea per row — read [`run-record`](../run-record/SKILL.md) and append the turn as orchestrator-e2e requires. If it cannot, do not force a table. The explanation is the stop.
3. End the turn. Do not spawn the next role until Levi says go.

A reviewer or tester reject stops the same way. Explain the reject with explain-to-levi. Write the run-record turn when the reject tables cleanly. Do not send it back until he says to.

A bare go is permission to spawn the next role. It is not a run-record turn. If he changes the plan, write that as a User lock on the next turn when it tables, then spawn the role that must absorb the change, then stop again after it returns.

When a run record exists, put its path in the explanation. Do not paste the file. The table is the scan. The explanation is how it clicks.

The short end report from orchestrator-e2e still happens once he has let the loop finish.

Example, after the planner returns:

> The app already ends a session in `auth/session.ts` by clearing the cookie. The plan is to call that from a new button in `Header.tsx`.
> Next, the implementer would add that button. Say go.

That return tables (Found, Plan, Why), so it is also a run-record turn.

## Do not

- Do not run the next phase in the same turn as the explanation.
- Do not treat "repeat until the reviewer accepts" in orchestrator-e2e as permission to keep spawning without a go.
- Do not explain with a table. explain-to-levi is the explanation. The run record is only the scan, and only when it tables cleanly.
- Do not infer this skill. He names orchestrator-learning.
