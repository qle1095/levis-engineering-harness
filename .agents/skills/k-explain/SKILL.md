---
name: k-explain
description: Build custom visual teaching artifacts for concepts and model outputs using annotated teaching sheets, interactive HTML, or bespoke explainer videos. Use when the user invokes k-explain or wants a visual, interactive, or animated explanation. Focus on teaching rather than general website or promotional video production.
---

# k-explain

Turn a concept into something the user can understand, inspect, and reason about. Base the approach on the [Karpathy passage](https://x.com/karpathy/status/2105819303471976479): controlled language, diagrams and images, interactive webpages, and bespoke explainer videos.

Keep this skill self-contained and independent of other explanation skills. The choices below translate the passage into practical defaults.

## Required output: a custom visual teaching artifact

Every invocation must produce and present a custom visual teaching artifact, unless the user explicitly requests prose only or another format. A short topic or a simple distinction does not waive this requirement. Clear writing supports the artifact; it is not the default deliverable. A prose answer with a small Mermaid flowchart does not satisfy this skill.

Before building a visual artifact, inspect the [bundled teaching-sheet reference](assets/teaching-sheet-reference.png). It preserves the default presentation across conversations: a light engineering sheet with square sections, restrained color, close annotations, and useful visual density. Match its teaching quality and visual discipline; adapt the number of sections and the subject-specific diagrams rather than copying its content. An explicit user format or a new supplied example takes precedence.

Use a supplied example as the output contract: inspect it and match its teaching structure, level of detail, and visual style while adapting the content to the new topic. Read supplied source links before attributing claims to them; use an accessible mirror when the original is blocked, and disclose that substitution. Do not claim to have read an inaccessible source.

Without a supplied format, build an annotated teaching sheet: a coherent visual explanation with labeled sections, diagrams of the mechanism, a worked example, and comparisons or limits that help the user reason about the topic. Use disciplined spacing, readable type, and labels next to the objects they explain. Each section must teach something; adapt the arrangement and number of sections to the subject. Do not substitute a dashboard, decorative cards, or a generic chain of boxes for the explanation.

Honor the user's requested format and length. Infer the learning need and build the artifact without making the user select a medium. Ask only when missing information materially changes what to teach.

| What the user needs to grasp | Required artifact |
| --- | --- |
| A definition, distinction, relationship, or structure | Annotated diagram or teaching sheet with a concrete example |
| A process, changing state, or the effect of changing an input | Interactive HTML with a visual explanation and controls that expose the mechanism |
| An idea best taught through a guided sequence, motion, and narration | Bespoke explainer video |

For interactive HTML, retain enough of the visual explanation to understand the topic at a glance. Let the user inspect a process with steps or change a meaningful input and see its effect. Put the cause and effect together; do not replace the teaching sheet with text inside a webpage. Video is an option, not a mandatory escalation from HTML.

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

Make the required artifact show what happens and why. Use the worked example to connect the diagram to a result the user can predict or inspect.

Choose a form that matches the idea: a flow for a process, a sequence for exchanges, a map for relationships, or a before-and-after image for a change. Keep labels close to what they describe, use consistent visual meanings, and reveal complex structures in useful stages.

Use a precise diagram for exact relationships and an illustration when appearance or spatial intuition carries the lesson. Include a short explanation of what to notice. For each arrow, identify what flows and verify that the destination actually consumes it. Separate operations with different inputs; do not route data through an unrelated computation for layout convenience. Check that labels and grouping agree with these routes; beauty cannot repair a misleading model.

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

Render the video and inspect the encoded media itself at multiple scene times. Verify that its frames change as planned, the narration matches the visible explanation, captions remain readable, and playback reaches the end. Source-animation screenshots, successful encoding, and valid media metadata do not prove the finished video teaches the sequence. Deliver a playable video when that is the requested output. If tooling prevents completion, state what is missing and accurately label any animation, storyboard, or script delivered as a partial result.

## Check whether the explanation works

Before delivery, render and inspect the artifact. Check readable labels, spacing, arrows, and grouping against the mechanism and worked example. Exercise implemented teaching controls and verify their displayed outcomes. For explanations of model outputs, make key assumptions and the basis for consequential conclusions inspectable.

If the user remains confused, reconsider the representation: a relationship may need a diagram, a changing system may need a control, or a transformation may need motion. Be willing to build a new, disposable explanation instead of merely expanding the original prose.

Deliver the rendered artifact with only the orientation needed to use it. Show an image preview for a teaching sheet and provide the usable interactive page or playable video when built. Source code, a plan, a textual substitute, or an unrendered diagram is not completion. If a tool fails, try an available alternative; if completion remains blocked, preserve the work and clearly label the missing deliverable. Do not silently fall back to a normal chat explanation. The result must let the user explain what happens, predict a relevant change, or assess the output they came to understand.
