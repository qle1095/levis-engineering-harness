---
name: k-explain
description: Explain concepts and model outputs through clear writing, diagrams, interactive HTML, or bespoke explainer videos. Use when the user invokes k-explain or wants a visual, interactive, or animated explanation to make a concept easier to understand. Focus on teaching rather than general website or promotional video production.
---

# k-explain

Turn a concept into something the user can understand, inspect, and reason about. Base the approach on the Karpathy passage supplied by the user: controlled language, diagrams and images, interactive webpages, and bespoke explainer videos.

Keep this skill self-contained and independent of other explanation skills. The choices below translate the passage into practical defaults.

## Choose the medium for understanding

As models do more work autonomously, the user needs to understand their outputs and oversee their decisions. Spend the model's effort on making the idea visible: what happens, why it happens, and what the user needs to judge.

Honor the requested format and length. Otherwise, infer the learning need from the question and context, then choose and build the explanation. Ask only when missing information materially changes what to teach. Do not make the user select a format every time.

| What the user needs to grasp | Useful format |
| --- | --- |
| A definition, distinction, or short causal explanation | Clear writing |
| Parts, relationships, structure, or a process at a glance | Diagram or image |
| How changing an input affects an outcome; comparisons and exploration | Interactive HTML |
| An idea that becomes clear through a guided sequence, motion, and narration | Bespoke explainer video |

Actively consider the richer formats. A short question can deserve a substantial custom artifact if that makes the answer click. The formats are options, not a required production sequence, and video is not automatically better for every topic.

Custom software can be useful even if it is used once and discarded. Do not reject a helpful simulator, animation, or explainer because it would once have been too expensive to build. Optimize for the user's understanding, not the artifact's lifespan or decorative complexity.

## Writing: about 80% of the way to ASD-STE100

ASD-STE100 originated in aerospace maintenance documentation. Use a relaxed, ASD-STE100-inspired style by default. This is a practical writing preference, not a measured compliance level.

- Use familiar, concrete words and short sentences. Give each sentence one main idea.
- Name the actor and action. Prefer active voice and direct verbs.
- Use the same term for the same thing. Define a necessary technical term before relying on it.
- Make references explicit when words such as "it" or "this" could mean several things.
- Separate instructions from explanations. Present steps in the order the reader needs them.
- Preserve the mechanism, important distinctions, and uncertainty while simplifying the language.

Keep enough natural phrasing for the explanation to be pleasant to read. Apply this style to prose, diagram labels, interface text, captions, and narration.

For a request for strict ASD-STE100, consult the actual writing rules and controlled dictionary. Do not present these relaxed guidelines, or the model's familiarity with STE, as proof of compliance. The [official ASD-STE100 FAQ](https://www.asd-ste100.org/STE_faq.html) describes the standard's writing rules and controlled vocabulary.

## Diagrams and images: make relationships visible

Use a visual when it lets the user see something they would otherwise have to reconstruct from paragraphs.

Choose a form that matches the idea: a flow for a process, a sequence for exchanges, a map for relationships, or a before-and-after image for a change. Keep labels close to what they describe, use consistent visual meanings, and reveal complex structures in useful stages.

Use a precise diagram for exact relationships and an illustration when appearance or spatial intuition carries the lesson. Include a short explanation of what to notice. Check that arrows, labels, and grouping tell the same story as the text; beauty cannot repair a misleading model.

## Interactive HTML: let the user try the idea

Build and present a usable webpage when the user can learn by changing something and observing the result. Prefer a self-contained HTML artifact when practical.

Use controls tied to the concept: a slider for a variable, a toggle for a comparison, or a step button for a process. Show the cause and effect together. Choose an initial example that teaches immediately and make it easy to reset or replay.

Use visual polish and animation to direct attention and reveal behavior. Avoid interactions that merely decorate a paragraph. Explain the model's important assumptions so the user can distinguish a teaching simplification from real system behavior.

Open or render the page and exercise the teaching controls. Check that the displayed results agree with the explanation. Deliver the working artifact, not just its source code or a proposal to build it.

## Explainer videos: guide attention through time

Treat bespoke video as a real teaching option. Build a visual argument that unfolds: introduce the question, make the mechanism visible, work through a concrete example, and connect the result back to the question. Adapt the sequence to the topic rather than imposing a fixed duration or scene count.

For a "3b1b-style" explanation, use the useful teaching qualities of 3Blue1Brown: visual intuition, progressive construction, clear mathematical relationships, and motion that explains a transformation. Create an original explanation suited to the user's topic.

Plan narration and visuals together. Synchronize the spoken point with the object or change on screen. Allow time to absorb the important steps; include captions or a transcript for replay and review.

For narration, use ElevenLabs when the user requests or authorizes it and credentials are available through a supported secret mechanism. Keep keys out of generated artifacts. Otherwise, research currently available free options that use local compute and choose one suited to the machine, setup effort, and voice quality. Do not assume an old tool recommendation is still suitable.

Render and inspect the result, including narration timing and readability. Deliver a playable video when that is the requested output. If tooling prevents completion, state what is missing and accurately label any animation, storyboard, or script delivered as a partial result.

## Check whether the explanation works

Use a concrete example when it helps expose the mechanism. Verify that the prose, visuals, controls, and narration agree. For explanations of model outputs, make key assumptions and the basis for consequential conclusions inspectable.

If the user remains confused, reconsider the representation: a relationship may need a diagram, a changing system may need a control, or a transformation may need motion. Be willing to build a new, disposable explanation instead of merely expanding the original prose.

Deliver the explanation and only the orientation needed to use it. The result should let the user explain what happens, predict a relevant change, or assess the output they came to understand.
