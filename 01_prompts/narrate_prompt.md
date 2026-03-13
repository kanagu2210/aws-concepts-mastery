# AWS Concept Mastery — Teaching Script Generator
## Stage 4 of 6 — Concept to Spoken Script
### narrate_prompt.md

---

# PURPOSE

You are generating a teaching script from a single concept entry
produced by Stage 3 (Expand).

This script will be spoken aloud by a teacher to a live classroom.
It is the exact words the teacher speaks — written out in full,
in the order they are spoken, exactly as they would sound in a
real classroom.

The script is saved to `output/02_narrated/<id>_<slug>.md` by
`run.py`. Stage 5 (Render) reads it from that file.
You do not need to think about storage — just generate the script.

---

# INPUT — CONCEPT ENTRY

You will be given one concept entry from the expanded concepts file.
The entry contains these fields.

```yaml
id, global_sequence, slug
layer, layer_name         # which layer this concept belongs to
spine_type                # mental_model | concept | contrast | pattern | bridge
exams                     # which exams this concept covers
interviews                # true if commonly asked in interviews

domain, aws_service
title, concept_tier
conceptual_complexity, cognitive_role
depth_stage               # D1 | D2 | D3 | D4 | D5

concept_spine
real_world_analogy
confusion_buster
bridge_from
domain_handoff            # bridges to the next call — do not teach from this field

boundary:
  includes
  excludes

links:
  depends_on
  next_best               # informational only — do not reference in script
  often_confused_with
  contrast_with

understanding:
  real_world_scenarios
  common_misunderstandings
  why_it_exists

notes
```

The fields are the content boundary — never go beyond them.
The `excludes` list is a hard wall — if a topic appears there,
do not teach it, and if a student would ask about it, the script
has a deflection line ready.

---

# THREE COMMITMENTS BEFORE READING FURTHER

Before reading any other section, read the concept entry and
commit to these three values. They determine everything.

**1. spine_type** — What is the structural shape of this script?
- `mental_model` → framework walkthrough, part by part
- `concept` → standard treatment, shaped by cognitive_role
- `contrast` → both sides introduced early, decision rule repeated
- `pattern` → design walkthrough, services in data flow order
- `bridge` → coaching only, no new concepts, exam/interview focus

**2. layer** — What does the room already know?
- L1 → nothing assumed, analogy carries the weight
- L2 → big ideas known, going under the hood
- L3 → mechanisms known, adding services to the toolbox
- L4 → services known, now making choices
- L5 → service choices known, now composing systems
- L6 → knowledge complete, translating to exam/interview performance

**3. depth_stage** — How deep does this go, and how long?
- D1 → define and ground, 400–600 words
- D2 → define plus one contrast, 500–700 words
- D3 → brief definition, decision reasoning dominates, 650–900 words
- D4 → design constraints and trade-offs dominate, 800–1100 words
- D5 → scale and prescriptive recommendations dominate, 1000–1500 words

Write these three values down internally before continuing.
Every section below applies differently depending on them.

---

A teaching script is not an article. It is not a lesson plan.
It is not slide notes.

It is the exact words a teacher speaks to students — written out
in full, in the order they are spoken, exactly as they would sound
in a real classroom.

The teacher who picks up this script should be able to walk into
a room, start reading from line one, and have a natural, engaging
teaching session without preparing anything else.

That means:
- Every sentence is written to be spoken, not read silently
- The rhythm is conversational — short punchy sentences mix with
  longer ones that carry a full idea
- Pauses, emphasis, and student interactions are scripted explicitly
- The script never sounds like it was printed from a textbook

---

# SCRIPT FORMAT — THREE ELEMENTS ONLY

**Speech paragraphs.** The words the teacher speaks, written as
plain flowing text. No `TEACHER:` label. No `[PAUSE]` markers.
Paragraph breaks carry the rhythm — a new paragraph is a natural
breath. A single sentence on its own line is not a mistake — it
is often the right choice. Short single-sentence paragraphs land
hard. Use them when a point needs to sit.

**[Board: ...]** Something the teacher writes or draws on the board
at this moment. One line. Keep it minimal — only things that
genuinely help if visible while being explained.

**[Check: ...]** A question directed at the room. Written as the
exact words the teacher says. Must require a real answer — not
"does everyone understand?" but something the student has to
actually think about. See CHECK QUALITY RULES below.

---

# EXAMPLE — WHAT SPOKEN TEACHING LOOKS AND SOUNDS LIKE

This is what a teaching passage should feel like. Read it before
writing a word. Notice the rhythm, the fragments, the direct
address, the thinking out loud.

---

Who here has seen a website go down?

Most of you. Good. Because that's the problem we're solving today.

`[Board: One thing fails → everything goes down]`

When one thing fails and takes the whole system with it — that's a
single point of failure. High availability says: we're not building
systems like that anymore.

Now — you might already be thinking, isn't that the same as fault
tolerance? That's a smart thing to wonder. Here's the difference.

Fault tolerance means the system keeps running even when something
breaks. Zero downtime. Zero impact. You don't even know it happened.

High availability means something different. It means the system
recovers fast — fast enough that most users don't notice. Not zero
downtime. Minimal downtime.

`[Board: Fault tolerance = keeps running | High availability = recovers fast]`

[Check: Your company's SLA says 99.9% uptime. You're designing the
database layer. Does that SLA require fault tolerance or high
availability — and what's the difference in what you'd build?]

The answer matters. Fault tolerance is expensive. High availability
is a design choice. You need to know which one the business is
actually asking for.

---

Notice:
- Fragments used deliberately. "Most of you. Good."
- The teacher thinks out loud before answering. "Here's the difference."
- A hard pivot lands on its own line. "The answer matters."
- The [Check:] requires applying the distinction to a real situation.
- No "Today we will cover..." No "It is important to note..."
- The confusion is named and resolved — not avoided.

---

# FIELD MAPPING — HOW EACH FIELD SHAPES THE SCRIPT

| Field | How it is used in the script |
|-------|------------------------------|
| `title` | Script title header only — never spoken as an announcement |
| `layer` | Sets the register (see LAYER REGISTER section) |
| `spine_type` | Determines the script's structural shape (see SPINE_TYPE section) |
| `exams` | Sets the ceiling on technical depth |
| `interviews` | If true, the script ends with one interview framing line |
| `concept_spine` | The central idea — the teacher returns to this throughout |
| `real_world_analogy` | Introduced early, extended throughout — the mental model the room carries |
| `bridge_from` | Opening lines if strong — use only when it creates real momentum |
| `confusion_buster` | Surfaced early as a brief flag, then fully resolved in the middle |
| `boundary.includes` | The teaching content — every include gets spoken and grounded |
| `boundary.excludes` | Hard wall — if a student asks about these, the script has a deflection line |
| `understanding.why_it_exists` | The "why does this matter" moment — grounded in real consequences |
| `understanding.real_world_scenarios` | Used in [Check:] moments and worked examples |
| `understanding.common_misunderstandings` | Surface as student voice — "someone always thinks this" — state the wrong model, then correct it |
| `links.often_confused_with` | Named briefly early — not fully resolved, just flagged |
| `links.contrast_with` | Board comparison moment |
| `depth_stage` | D1–D2 = define and ground; D3 = contrast and apply; D4–D5 = design reasoning |
| `cognitive_role` | Shapes what the script lingers on (see COGNITIVE ROLE section) |
| `concept_tier` | foundation = slower pace; core = full treatment; extension = move faster |

---

# LAYER REGISTER — HOW LAYER CHANGES THE SCRIPT

The `layer` field sets the register and assumed knowledge of the room.

| Layer | Register |
|-------|----------|
| L1 — Foundations | The room knows nothing yet. No AWS assumed. Every idea is introduced from scratch. The analogy carries most of the weight. |
| L2 — Core Mechanisms | The room knows the big ideas. Now we go under the hood. "You know what IAM is — today we look at how it actually makes a decision." |
| L3 — Service Mastery | The room understands the mechanisms. Now we add tools to the toolbox. Service purpose, boundaries, and cost are the focus. |
| L4 — Decision Patterns | The room knows the services. Now we make choices. "You've got SQS and SNS in front of you — which one do you pick and why?" |
| L5 — Architectural Patterns | The room can choose services. Now we compose them into systems. Worked design scenarios dominate. |
| L6 — Exam and Interview Bridges | The room has the knowledge. Now we translate it to performance. Exam traps, distractor patterns, interview framing. |

Never teach below the layer's register. A L4 script that explains
what SQS is from scratch is wrong — the room already knows.
A L2 script that assumes SAP-level architecture knowledge is also wrong.

---

# SPINE_TYPE — HOW TYPE SHAPES THE SCRIPT STRUCTURE

The `spine_type` field determines the fundamental shape of the script.
This overrides default structure. Read it before making any decisions.

**mental_model**
The script walks through a framework part by part.
Each part gets its own moment — introduced, grounded in the analogy,
connected to the next part.
The teacher reveals the framework progressively — not all at once.
The [Board:] moment shows the framework's structure.
The landing line shows how the parts form a whole.
Good entry points: lead with the problem the framework solves,
or lead with the confusion it resolves.

**concept**
Standard treatment. Entry point, analogy, mechanics, confusion,
scenario, landing line. Shape determined by cognitive_role.
The most common type — no special structural constraint.

**contrast**
The comparison is the spine of the entire script.
Both things are introduced early — never just one then the other late.
The [Board:] moment shows them side by side.
The decision rule is stated clearly and repeated.
At least one [Check:] asks the room to apply the decision rule
to a scenario before the teacher gives the answer.
The landing line is the decision rule, compressed.
Good entry points: lead with the confusion, or lead with a scenario
where the wrong choice has consequences.

**pattern**
The script is a design walkthrough.
A real business scenario is established first — name the company,
the load, the failure mode being designed around.
Then the services are introduced one by one in the order data flows
through the system.
Each service's role is explained in the context of the scenario —
not in the abstract.
[Check:] moments ask "what happens if this service fails?" or
"why this service and not that one?"
The landing line names the pattern and what problem it solves.

**bridge**
The script is coaching, not teaching.
The teacher is preparing the room to perform — not introducing concepts.
No new concepts are introduced. Everything references what the room
already knows from L1–L5.
Structure: here's the question type → here's the trap → here's the
reasoning path that avoids it → here's what the correct answer looks like.
[Check:] moments present a real exam/interview scenario and ask the
room to identify the trap or choose the answer before the teacher reveals it.

---

# COGNITIVE ROLE — WHERE THE SCRIPT LINGERS

| cognitive_role | Script emphasis |
|----------------|-----------------|
| `definition` | The teacher spends time on plain-English explanation and the analogy. Student questions are about what it is and why it exists. |
| `contrast` | The comparison moment is the heart of the script. The board gets a side-by-side. Students are asked to identify which concept applies to a scenario. |
| `model` | The teacher walks through each part of the framework in sequence, showing how the parts relate. The board has a simple diagram. |
| `application` | The worked scenario carries the most time. Students are asked to reason through a real situation before the teacher gives the answer. |

---

# DEPTH STAGE — PACING, CEILING, AND LENGTH

| depth_stage | Pacing and ceiling | Approximate length |
|-------------|--------------------|--------------------|
| D1 | Slowest. Maximum analogy time. Define before any mechanism. No comparison to adjacent services required. | 400–600 words |
| D2 | Steady. Full definition plus one contrast. The confusion_buster gets its own moment. | 500–700 words |
| D3 | Balanced. Definition is brief — the room knows what it is. Decision reasoning and scenario application get the most time. | 650–900 words |
| D4 | Faster on definitions. Design constraints and trade-offs dominate. Scenarios involve multiple services interacting. | 800–1100 words |
| D5 | Fastest on basics. Scale, organisational complexity, and prescriptive recommendations dominate. Scenarios have multiple valid answers with different trade-offs. | 1000–1500 words |

These are guides, not hard limits. A D1 script that needs 700 words
is fine. A D3 script at 1400 words is too long — tighten it.

---

# CONCEPT TIER — PACING

| concept_tier | Pacing |
|--------------|--------|
| `foundation` | Slower. More space between ideas. More [Check:] moments. The analogy gets extra time. |
| `core` | Balanced. Full treatment. One or two student interaction moments. |
| `extension` | Faster. The teacher assumes foundations are solid and moves to the nuance. Less time on definition, more on distinction and decision. |

---

# THREE DECISIONS BEFORE WRITING

Before writing a single word, make these three decisions.

## Decision 1 — What is the entry point?

Read `cognitive_role`, `spine_type`, `concept_spine`, and
`understanding.why_it_exists`. Then choose one entry point.

**Lead with the problem.**
Use when `why_it_exists` describes a painful situation students
can picture. Start with that pain before naming the concept.

**Lead with the confusion.**
Use when `links.often_confused_with` is populated and the
confusion is genuine. Name it in the first minute.

**Lead with the story.**
Use when `real_world_analogy` is vivid and immediately picturable.
Drop the class into the story before any AWS context.

**Lead with the scenario.**
Use when `real_world_scenarios` describes a situation students
have personally experienced or can easily imagine.

**Lead with the bridge.**
Use only when `bridge_from` is present AND it creates genuine
momentum — not just a mechanical transition. If bridge_from is
weak or forced, choose a different entry point and fold the
connection in naturally later.

**Lead with the design problem.** (L5 pattern spines only)
Name the business scenario and the failure mode before naming
any service. "You're running a payment processor. Black Friday.
500k transactions per minute. Your database is the bottleneck."

## Decision 2 — Where does the confusion get resolved?

If `links.often_confused_with` is populated — never save it for
the end. Flag it briefly early, resolve it fully in the middle.

If you led with the confusion — resolve it after the mechanics
are built. The opening names it, the middle resolves it fully.

## Decision 3 — What is the landing line?

One sentence. Chosen before you write the script.
Write toward it. It compresses the whole session into a form
the student can repeat back three months later without rereading.

The test: could a student repeat this sentence back accurately
after three months? If it is a summary, it fails — summaries
require memory. If it is the concept_spine in a form that sticks,
it passes.

FAIL: "So in summary — Lambda is serverless, event-driven, and
automatically scales based on incoming requests."
(A list. Requires remembering three things. Will not survive.)

PASS: "Lambda means you write the function — AWS worries about
the server. You're billed for the hundred milliseconds it runs,
not the hours it waits."
(One idea, two sentences, concrete. Survives three months.)

For contrast spines: the landing line is the decision rule.
For pattern spines: the landing line names the pattern and its purpose.
For bridge spines: the landing line is the exam/interview insight.
For mental_model spines: the landing line shows how the parts form a whole.

---

# WHAT MUST APPEAR IN EVERY SCRIPT

These ingredients must all be present. Their order and weight
is yours to decide based on the three decisions above.

**The concept in plain words.**
The `concept_spine` spoken naturally. Said once clearly early.
Not read out — spoken as the teacher's own words.

**The real world picture.**
The `real_world_analogy` introduced early, returned to at least
once more when mechanics need grounding. Never replaced with
a second analogy.

**The content from `boundary.includes`.**
Every include must be covered somewhere. Spoken as connected
explanation — not as a list, not necessarily in YAML order
for concept/bridge spines. For contrast, pattern, and
mental_model spines, the YAML order is the teaching sequence —
follow it.

Ground each include in the analogy or a scenario before moving on.

**The reason it exists.**
`understanding.why_it_exists` — the real consequence that makes
this concept matter. Grounded in a specific picture.

**At least one real scenario.**
From `understanding.real_world_scenarios`. Specific — name the
company type, name the problem, name what happens.
Followed by a [Check:].

**The confusion resolved.**
From `confusion_buster` — named early, resolved fully before the end.
If `links.contrast_with` is populated, the board gets a side-by-side.
If `links.often_confused_with` is populated — flag briefly early,
do not fully resolve.

**At least two [Check:] moments.**
Real questions requiring real thought.
Not "does that make sense?" — something the student has to answer.
See CHECK QUALITY RULES below.

**At least one [Board:] moment.**
Only if there's a structure, contrast, or relationship that
genuinely helps when visible. Not forced.

**Interview framing line (if interviews: true).**
One line near the end — not a new paragraph, just a natural
moment — framing how this concept appears in interviews.
"In an interview, if they ask you to design a system that needs
to process jobs without losing them, this is what you reach for."

**The landing line.**
Last. One sentence. Repeatable three months later.

---

# CHECK QUALITY RULES

A [Check:] is a question spoken to the room that requires applying
knowledge, not recalling a definition.

FAIL: "Does that make sense?"
(No wrong answer. Requires nothing.)

FAIL: "Can anyone tell me what SNS stands for?"
(Recall, not application.)

FAIL: "What are the main use cases for Lambda?"
(Open-ended. No stake. No right or wrong direction to reason toward.)

PASS: "You've got a system where one event needs to trigger billing,
a notification email, and an audit log entry — all at the same time.
SQS or SNS — which one and why?"
(Specific scenario. Forces the decision rule. Has a correct answer.)

PASS: "Your RDS instance just went down. You're in a Multi-AZ
deployment. What happens in the next 60 seconds — walk me through it."
(Requires knowing the mechanism. Has a specific correct sequence.)

The [Check:] moment should come after the content needed to answer
it has been taught — not before. Use it to confirm landing, not
to introduce.

---

# WHAT MUST NEVER APPEAR

- Fixed section labels: Opening, Analogy, Mechanics, Close, Summary
- Timing labels: [~2 minutes], [~90 seconds]
- Any sequence that every script follows regardless of concept
- New concepts not present in the concept entry
- Content from `boundary.excludes`
- L1-register explanation in an L4/L5 script ("First, let me
  explain what Lambda is..." in a script about event-driven patterns)

---

# VOICE RULES

The teacher speaks like someone who knows the material well but
uses plain, simple words. Not academic. Not corporate. Not a
presenter. A person in a room who cares whether the room follows.

## Simple words

Not "implement" — "build" or "set up".
Not "utilise" — "use".
Not "subsequently" — "then".
Not "regarding" — "about".
Not "functionality" — "how it works".
Not "conceptually" — just say the thing.
Not "in the context of" — just say where.

## Spoken rhythm

Real speech uses structures that written prose does not.
Use all of these — they are not errors, they are technique.

**Fragments.** A full sentence is not always needed.
"Not always. Not even most of the time."
"Two services. One job each."

**Mid-sentence pivots.**
"You'd think the answer is yes — it isn't."
"The obvious move here is Lambda — except it's not."

**Trailing emphasis.** The point lands after the dash.
"The backup isn't waiting. It's running."
"That's the whole thing. That's it."

**The restart.** Signals a gear change.
"Now — wait. Think about that for a second."
"Right. So. Here's where it gets interesting."

**Direct address.** Occasional, not constant.
"You, running a startup — this is the decision you'll face."
"Think about the last time you waited for a page to load."

## Short paragraphs land hard

A paragraph break is a breath. A single sentence on its own line
is not a stylistic choice — it is weight. Use it when a point
needs to land before the next one arrives.

"The backup is always running.

Not waiting. Running.

That distinction is everything."

## Thinking out loud

A real teacher does not just deliver content. They model the
thinking process. They say the things the room is quietly thinking.

"Now I'm going to say something that sounds backwards. Stay with me."
"Here's the question you should be asking right now."
"You probably just thought of an exception. Good. Let's get to it."
"The reason I'm spending time on this is — it trips up everyone."

This is not padding. It creates the feeling of being in a room
with someone who is thinking, not reading.

## Acknowledging difficulty

A real teacher flags hard moments before and after — not with
formal language but with human acknowledgment.

WRONG: "It is important to note that this concept is complex."
RIGHT: "This next bit is the part that catches people. Slow down."

WRONG: "That was a key point worth remembering."
RIGHT: "Let me say that one more time differently, because it matters."

Never signal importance with formal flags. Signal it with pace
and repetition.

## Teacher personality

The teacher has mild opinions about the content. Not enthusiasm.
Not cheerleading. A dry, genuine perspective.

"AWS called this 'Simple' Storage Service. You'll decide for
yourself whether that name holds up after you've worked with it."

"There are four answers on the exam. Three of them are SQS.
Learn to read the question."

"This is one of those services that sounds complicated until
you realise it does one thing and does it well."

Not a comedian. Not performatively humble. Just a person with
a point of view who has taught this before.

## Contractions are mandatory

"It is" → "It's". "You are" → "You're". "Do not" → "Don't".
"They are" → "They're". "We will" → "We'll".
No exceptions. Uncontracted speech sounds written.

## Repetition is a tool

Don't assume a hard point landed the first time. Say it again
in different words. The second version is not redundant — it is
the one that lands for the person who missed the first.

"So the read replica handles read traffic. The primary handles
writes. They are not interchangeable. One reads, one writes."

## Good transitions sound spoken

WRONG: "Having established the definition of high availability,
we will now examine its relationship to fault tolerance."

RIGHT: "Right. So that's what it is. Now — why does any of this
matter when you're designing something?"

RIGHT: "Good. Hold that. Because now we need to talk about what
happens when it breaks."

Transitions are short, directional, and often start mid-thought.

## Banned phrases — written language tells

Never say these. They signal that the text was written, not spoken.

**Formal written language:**
- "As we can see…"
- "It is important to note that…"
- "This is a key concept…"
- "Let's explore…"
- "In summary…"
- "To recap what we've covered…"
- "Having established…"
- "It is worth noting that…"

**Spoken AI tells — phrases that try to sound human but don't:**
- "Think of it this way…" (just give the analogy)
- "What this means in practice is…" (just explain it)
- "The key insight here is…" (just state the insight)
- "Let me break this down…" (just break it down)
- "At the end of the day…" (filler)
- "That's a great question" (no student asked anything)
- "So, to summarise what we've just seen…" (just end)
- "This is actually quite simple once you understand…"
  (condescending and untrue)

---

# SCRIPT ANTI-PATTERNS — NEVER DO THESE

**The Lecture Voice.** Long unbroken blocks of speech with no
[Check:], no [Board:], no paragraph breaks. A real teacher breathes.
Break up long explanations. No paragraph should exceed six sentences.

**The Announcement Opening.**
"Today we are going to cover high availability, which is an
important concept in the Cloud Concepts domain." Never.
Start with a question, a problem, or a scenario.

**The List Dump.**
"High availability has three characteristics: first... second...
third..." Real teaching builds one idea at a time. It does not
start with the structure.

**The False Check.**
"Does that make sense?" after a hard concept. Ask something that
requires a real answer.

**The Textbook Transition.**
"Having established the definition of high availability, we will
now explore its relationship to fault tolerance." No real teacher
speaks like this.

**The Metadata Opening.**
Never start with the domain, task number, concept tier, depth stage,
layer, or exam list. Those are yours to use internally.

**The Generic Bridge Pattern.**
A bridge (L6) script that teaches the concept instead of coaching
exam performance. Bridge scripts coach — they never teach new material.

**The Uniform Paragraph.** Every paragraph the same length, the
same rhythm, the same structure. Real speech varies. Short. Then
longer. Then a fragment. Then a full idea. Mix it.

---

# BEFORE YOU WRITE — SILENT GATE

Run this before writing the first spoken word. Do not reveal it.
If any item fails, revise your plan before generating.

**Three commitments confirmed:**
- [ ] spine_type identified — structural shape chosen
- [ ] layer identified — assumed knowledge of room locked
- [ ] depth_stage identified — pacing and length target set

**Three decisions made:**
- [ ] Entry point chosen (problem / confusion / story / scenario /
      bridge / design problem) — not a default announcement
- [ ] Confusion resolution placement decided (early flag, middle resolve)
- [ ] Landing line drafted — one sentence, repeatable in three months

**Content planned:**
- [ ] Every boundary.includes item will be covered
- [ ] No boundary.excludes item will appear
- [ ] At least two [Check:] moments planned — each requires applying knowledge
- [ ] Interview framing line planned if interviews: true

**Voice committed:**
- [ ] Contractions throughout — no exceptions
- [ ] At least one fragment, one mid-sentence pivot, one thinking-out-loud moment
- [ ] No banned written-language phrases
- [ ] No spoken AI tells
- [ ] No paragraph will exceed six sentences

Now write the script.

---

# OUTPUT FORMAT

The script uses only:
- Plain speech paragraphs — no labels, no markers, no `TEACHER:`
- `[Board: what is written or drawn]` on its own line
- `[Check: the exact words spoken to the room]` on its own line
- `##` section headings as navigation markers for the teacher

## File header (mandatory)

Every script must begin with this YAML front matter block.
`run.py` uses it to store and index the file correctly.

```
---
id: <from concept entry>
slug: <from concept entry>
title: <from concept entry>
layer: <from concept entry>
layer_name: <from concept entry>
exams: <from concept entry>
interviews: <from concept entry>
---
```

The front matter is followed by a blank line, then the script begins.
Do not add any other metadata. Do not add a title heading after the
front matter — the script opens directly with the first spoken line.

Section headings must reflect the actual content of that section —
not fixed labels. Every script should have different headings.

Good heading examples:
- `## The Plane That Keeps Flying`
- `## Why Two Seconds Is Sometimes Too Long`
- `## Standby vs Always On`
- `## The Decision Nobody Wants to Make`
- `## What the Interviewer Is Really Asking`

Bad heading examples — never use these:
- `## Opening`
- `## The Analogy`
- `## The Mechanics`
- `## Conclusion`
- `## Close`
- `## Summary`
- `## [~90 seconds]`

No timing estimates anywhere in the output.

---

# HOW TO USE THIS PROMPT

Paste this prompt into a conversation, then paste a single concept
entry from the expanded concepts file beneath it.

The generator produces one complete teaching script for that concept.

The script is designed to be used directly — the teacher reads
through it once before delivering it. No other preparation needed.

Generate the complete teaching script now.