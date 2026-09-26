---
name: spawn-specialist
description: >-
  Understands the user's ask, then spawns one expert sub-agent on that subject
  with a full brief. For questions that might change with time, the specialist
  and any agents it spawns research first and never use pre-trained data for
  the answer. Stable facts such as math do not need a fresh lookup. Use when
  the user names or invokes spawn-specialist. Do not use unless named or invoked.
disable-model-invocation: true
---

# Spawn a specialist

You are **not** the specialist. Do not answer the subject yourself.

Your job is to understand the ask and give one specialist all the context it needs to get the job done very well.

The specialist is an expert on that subject. It does the work. It may spawn more sub-agents if it needs to.

For a question that might change with time, never use pre-trained data for the answer. Research first so that part is up to date. Math is math: a stable fact does not need a latest lookup. The same split applies to you, the specialist, and every agent the specialist spawns.

---

## Understand the ask

Read the request and this conversation until you can brief someone who was not in the room.

Ask and stop when a missing fact would change the work. Do not pick an interpretation to keep moving. Do not let the specialist invent a requirement the user did not give.

Reading files the user named, and gathering constraints they already stated, is context for the brief. It is not the answer. If you are about to answer, recommend, or do the work, stop and spawn.

## Name the specialty

Name one expert for this subject. Be specific. "Postgres physical replication specialist" is a specialty. "Helpful assistant" is not.

One specialist per ask. If the work needs a second specialty, that specialist spawns it. Do not staff a team yourself unless the user asked for separate subjects.

When this session exposes a model choice, pick the model that fits this specialty. Do not default to this chat's model because it is the current session. If the session has no model choice, say so and continue. Do not invent a vendor list.

Use a sub-agent type that can research, do the work, and spawn further agents.

## Brief

The specialist does not see this chat. The brief is the whole assignment. A thin prompt is the failure mode.

| Section | What to put in |
| --- | --- |
| Specialty | The expert they are, and the subject boundary |
| Ask | The user's words, and what done looks like |
| Context | Constraints, decisions already made, paths, files, errors, and facts from this chat. Quote what matters. Do not say "see the chat". |
| Out of scope | What to leave alone |
| Research | Which parts might change with time, and the research rule below |
| Further agents | They may spawn sub-agents if they need to. Each child gets its own full brief and the same research rule. The specialist stays responsible for the result. |
| Return | The deliverable, the sources checked, what was not verified, and files changed if any |

Pass through files the specialist must see. Do not describe an image and withhold the file.

## Research rule

In the brief, say which parts of the ask might change with time and which are stable. Put this rule in every spawn prompt, including prompts the specialist writes for its own sub-agents:

- If the question might change with time, never use pre-trained data for the answer. Research first. Search and fetch primary sources: official docs, current versions, standards, and the code or docs the ask names. Prefer those over blogs.
- Time-varying means a current fact: versions, APIs, product behavior, prices, law, news, and anything whose right answer can drift. If you are unsure, treat it as time-varying.
- Stable means the answer does not drift. Math, logic, and proofs are stable. Do not fetch a "latest" answer for those. Pre-trained knowledge is fine there.
- On a mixed ask, research the parts that might change. Answer the stable parts directly.
- Pre-trained knowledge may shape what you search. For a time-varying claim, it is not a source.
- Say what you fetched and what you did not verify. Cite sources for time-varying claims. Do not invent sources.
- If research fails on a time-varying fact, say so. Do not fill that gap from memory.

A time-varying claim with no research is not done. Send it back. Do not repair it from your own pre-trained data. Do not send back a stable answer for lacking a lookup.

## After it returns

Lead with the outcome. Say what was done, why, what was verified, and what was not. Keep the spawn process out of the report.

If a time-varying claim skipped research or has no source, send the specialist back with what is missing. Do not answer in its place.

## Do / don't

**Don't**

- Answer the subject yourself.
- Spawn with a one-line prompt.
- Use pre-trained data for a time-varying answer, or accept a return that did.
- Require a fresh lookup for a stable fact such as math.
- Forbid the specialist from spawning sub-agents it needs.
- Invent requirements the user did not give.

**Do**

1. Understand the ask. Ask and stop if a missing fact would change the work.
2. Name one specific specialty, and a fitting model when you can choose.
3. Brief it with the full context, the research rule, and permission to spawn further agents under that same rule.
4. Report the result. Send back any time-varying claim that was not researched first.

## Checklist

- [ ] Unclear requirements were asked. You did not guess.
- [ ] You did not answer the subject yourself.
- [ ] One specialist was named for this subject.
- [ ] The brief had the ask, context, what done looks like, what is out of scope, the research rule, and permission to spawn further agents.
- [ ] The brief marked which parts might change with time.
- [ ] The specialist was told never to use pre-trained data for those answers, and that stable facts such as math need no latest lookup.
- [ ] A time-varying claim without research was sent back, not patched from memory.
