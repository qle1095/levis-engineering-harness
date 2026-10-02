---
name: bible
description: >-
  Deliver the user's ask with the specialists it needs, concise persistent
  memory for each role, and goal tracking through completion. Use when the
  user names bible or asks for a specialist team with durable project memory
  and goal tracking.
---

# Bible

Given the user's ask, create the roles needed to deliver it. Think like someone
hiring specialists: choose the expertise the work actually needs, give each
person enough context to act, and stay responsible for the combined result.

Give each specialist a brain: its own folder containing precise, distilled
project memory. Use `/goal` to carry the work through to a verified deliverable.

## Establish the goal

Turn the ask into a concrete outcome, its constraints, and observable completion
criteria. Preserve the user's scope. Clarify missing information when it changes
what must be delivered; continue work that does not depend on that answer.

Use the environment's native `/goal` capability. When goal tools are exposed,
read the current goal with `get_goal` and create the requested goal with
`create_goal` if none is unfinished. Reuse an existing goal when this ask belongs
to it; do not replace an unrelated unfinished goal. Ask the user to resolve that
conflict before starting a new one. Set a token budget only if the user explicitly
requested one. The coordinating agent owns goal updates; specialists work on
their assigned portions of that goal.

If native goal tracking is unavailable, say so and keep the outcome and completion
criteria in the working brief. Continue the authorized work without claiming
that `/goal` is active.

## Staff the work

Choose the smallest team that covers the needed expertise. Define each role by
its specialty, responsibility, deliverable, and how that deliverable will be
checked. Do not force every ask through a fixed planner / implementer / reviewer
pipeline.

Spawn specialists with the available sub-agent tools. Give each a self-contained
brief containing the user's ask, goal and completion criteria, relevant context,
constraints, source files, its responsibility, dependencies, memory path, and
expected return. Tell it which files it owns. Separate parallel writers' files;
schedule dependent work after its inputs are ready.

Each specialist acts as the expert assigned to it, researches claims that may
have changed using current primary sources, and returns its deliverable with
verification evidence, unresolved issues, and updated memory. Request further
specialties when the work reveals a real need; the coordinator assigns their
folders and ownership. Reuse suitable roles rather than spawning duplicates.

If sub-agent tools are unavailable, perform the needed roles sequentially and
state that limitation. Keep each role's responsibility and memory distinct.

## Give each role project memory

Use the project this ask concerns. Store each role's memory in
`.agents/bible/<role-name>/MEMORY.md` beneath that project's root, using short,
stable role names. Reuse an existing project memory location if one is already
established. If the ask has no project, use a task workspace. Do not put another
project's memory in this harness merely because the skill lives here.

Create each folder when its role is needed. Before work, have the specialist
read its memory and check relevant facts against current project sources.
The assigned specialist is the sole writer to its memory during the assignment.
Memory is context, not authority to change the user's request.

Keep only information that helps the next assignment:

- The role's responsibility and project constraints relevant to it.
- Confirmed facts and decisions, with a short reason and a source path or link.
- Useful findings, known pitfalls, and unresolved questions that still matter.
- Where the current deliverable lives and what was verified.

Update memory at meaningful handoffs and completion. Replace stale or superseded
facts, distinguish uncertainty from confirmed knowledge, and merge repetition.
Link to authoritative project documents rather than copying them. Exclude
transcripts, activity logs, generic advice, secrets, and unrelated information.
Keep it concise enough for the next specialist to read in full.

## Deliver at goal level

Collect the specialists' outputs, resolve conflicts, and assemble the actual
deliverable. Check it against the goal's completion criteria using evidence
appropriate to the task. A specialist's claim of success alone is insufficient.
Send concrete gaps back to the responsible role and continue through correction
and verification without stopping between routine handoffs.

Mark the native goal complete with `update_goal` only when the requested outcome
is achieved and no required work remains. Follow the goal tools' rules for
pausing, blocking, and budget limits; do not call partial work complete. If a
required user decision or external blocker prevents delivery, state precisely
what remains and keep the goal status accurate.

Report what was delivered, where it is, what was verified, and any remaining
limitation. Include final token usage when the completed goal was budgeted.
