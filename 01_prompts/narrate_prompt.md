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
- D1 → define and ground, 600–900 words
- D2 → define plus one contrast, 800–1100 words
- D3 → brief definition, decision reasoning dominates, 1100–1500 words
- D4 → design constraints and trade-offs dominate, 1500–2000 words
- D5 → scale and prescriptive recommendations dominate, 2000–2800 words

Write these three values down internally before continuing.
Every section below applies differently depending on them.

---

# CONTINUATION CONTEXT — MULTIPART NARRATION

This section is only relevant when the script is being generated
as one part of a multipart narration. If no continuation context
is provided below, ignore this section entirely.

When continuation context IS provided, it means:
- This is part N of a larger script for the same concept
- Part N-1 has already been generated and delivered to the room
- The room has just heard the handoff line — they are mid-session

**What this means for your output:**

Do NOT open with an entry point. The entry point was part 1.
Do NOT introduce the concept. The room already knows what it is.
Do NOT use the real_world_analogy as an opener — it was used in part 1.
  You may return to it briefly if it helps ground a new include,
  but do not re-introduce it.

DO open mid-flow, as if continuing a sentence the teacher just finished.
DO pick up from exactly where the handoff line left off.
DO treat the last paragraph of the previous part as the live landing
  point — your first sentence should feel like the next breath after it.

The handoff line and last paragraph of the previous part will be
injected below as:

HANDOFF LINE: <one sentence — the planned momentum point>
PREVIOUS PART ENDING:
<last paragraph of the previous part's actual output>

Your opening must feel like a direct continuation of that ending —
not a new beginning, not a transition announcement, not "as we
discussed." Just the next thing the teacher says.

**Landing line in multipart scripts:**

Only the FINAL part ends with the landing line.
All other parts end at a natural breath point — a moment of
resolution on the current block of includes — but do not close
the concept. The room knows there is more coming.

A mid-script ending sounds like:
"So that's the queue. Now — what happens when the consumer
on the other end can't keep up? That's where things get interesting."

Not like:
"In summary, SQS is a managed message queue service that..."

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
- Pauses and student interactions are scripted explicitly
- The script never sounds like it was printed from a textbook

---

# SCRIPT FORMAT — TWO ELEMENTS ONLY

**Speech paragraphs.** The words the teacher speaks, written as
plain flowing text. No `TEACHER:` label. No `[PAUSE]` markers.
Paragraph breaks carry the rhythm — a new paragraph is a natural
breath. A single sentence on its own line is not a mistake — it
is often the right choice. Short single-sentence paragraphs land
hard. Use them when a point needs to sit.

**[Pause: ...]** A moment where the teacher stops and gives the reader
time to think. Written as a short prompt — one sentence naming what
to sit with. Not a quiz. Not a question to answer out loud.
A beat of deliberate reflection before the teaching continues.
See PAUSE QUALITY RULES below.

---

# EXAMPLE — WHAT SPOKEN TEACHING LOOKS AND SOUNDS LIKE

This is what a teaching passage should feel like. Read it before
writing a word. Notice the rhythm, the fragments, the direct
address, the thinking out loud.

---

Who here has seen a website go down?

Most of you. Good. Because that's the problem we're solving today.

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

[Pause: Your company's SLA says 99.9% uptime. You're designing the
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
- The [Pause:] gives the reader a beat to absorb the distinction before moving on.
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
| `interviews` | Not used in narration — informational only |
| `concept_spine` | The central idea — the teacher returns to this throughout |
| `real_world_analogy` | Read this field to understand what KIND of scenario fits the concept — scale, failure, cost, fan-out, etc. Then replace whatever specific analogy is written there with the closest matching scenario from the approved company list (see ANALOGY COMPANIES below). Do not use the field's analogy verbatim if it names a company or scenario outside the approved list. |
| `bridge_from` | Opening lines if strong — use only when it creates real momentum |
| `confusion_buster` | Surfaced early as a brief flag, then fully resolved in the middle |
| `boundary.includes` | The teaching content — every include gets spoken and grounded |
| `boundary.excludes` | Hard wall — if a student asks about these, the script has a deflection line |
| `understanding.why_it_exists` | The "why does this matter" moment — grounded in real consequences |
| `understanding.real_world_scenarios` | Used in [Pause:] moments and worked examples |
| `understanding.common_misunderstandings` | Surface as student voice — "someone always thinks this" — state the wrong model, then correct it |
| `links.often_confused_with` | Named briefly early — not fully resolved, just flagged |
| `links.contrast_with` | Named and contrasted in the prose — differences stated clearly |
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
| L6 — Exam and Interview Bridges | The room has the knowledge. Now we translate it to performance. Focus on precise distinctions and common confusions. |

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
The decision rule is stated clearly and repeated.
At least one [Pause:] gives the reader a moment to apply the
decision rule to a scenario before the teacher works through it.
The landing line is the decision rule, compressed.
Good entry points: lead with the confusion, or lead with a scenario
where the wrong choice has consequences.

**pattern**
The script is a design walkthrough.
A real business scenario is established first — name the company,
the load, the failure mode being designed around.

Before introducing any individual service, give the room the whole
picture in one paragraph: what the full system does end-to-end,
what a request experiences from arrival to completion, and what
each major piece's job is in that journey. One paragraph — not a
list of components, a narrative of flow. Every service introduced
later gets anchored to this picture, not introduced as a new topic.

Then the services are introduced one by one in the order data flows
through the system.
Each service's role is explained in the context of the scenario —
not in the abstract.
[Pause:] moments ask "what happens if this service fails?" or
"why this service and not that one?" — giving the reader a beat
to think through the answer before the teacher explains it.
The landing line names the pattern and what problem it solves.

**Symmetry rule for pattern scripts:** Every mechanism described
in one direction must be described with equal depth in the other
direction. If scale-out gets a step-by-step timeline, scale-in
gets a step-by-step timeline. If AZ failure during high load is
explained, AZ recovery is addressed. The reader should never feel
that one half of a mechanism was explained and the other half
was only referenced. Reference is not explanation.

**bridge**
The script is coaching, not teaching.
The teacher is preparing the room to perform — not introducing concepts.
No new concepts are introduced. Everything references what the room
already knows from L1–L5.
Structure: here's the question type → here's the trap → here's the
reasoning path that avoids it → here's what the correct answer looks like.
[Pause:] moments present a real exam/interview scenario and give the
reader time to identify the trap or reason toward the answer before
the teacher reveals it.

---

# COGNITIVE ROLE — WHERE THE SCRIPT LINGERS

| cognitive_role | Script emphasis |
|----------------|-----------------|
| `definition` | The teacher spends time on plain-English explanation and the analogy. Student questions are about what it is and why it exists. |
| `contrast` | The comparison moment is the heart of the script. Students are asked to identify which concept applies to a scenario. |
| `model` | The teacher walks through each part of the framework in sequence, showing how the parts relate. |
| `application` | The worked scenario carries the most time. Students are asked to reason through a real situation before the teacher gives the answer. |

---

# DEPTH STAGE — PACING, CEILING, AND LENGTH

| depth_stage | Pacing and ceiling | Target length |
|-------------|--------------------|--------------------|
| D1 | Slowest. Maximum analogy time. Define before any mechanism. No comparison to adjacent services required. | 600–900 words |
| D2 | Steady. Full definition plus one contrast. The confusion_buster gets its own moment. | 800–1100 words |
| D3 | Balanced. Definition is brief — the room knows what it is. Decision reasoning and scenario application get the most time. | 1100–1500 words |
| D4 | Faster on definitions. Design constraints and trade-offs dominate. Scenarios involve multiple services interacting. | 1500–2000 words |
| D5 | Fastest on basics. Scale, organisational complexity, and prescriptive recommendations dominate. Scenarios have multiple valid answers with different trade-offs. | 2000–2800 words |

**Target the upper third of the range as your minimum.**
The lower bound is a floor — do not treat it as a target.
A D3 script at 1100 words has been cut short. A D3 script at
1400 words is doing its job. Earn every word — but spend them.

A script is too short when:
- An include is stated but not grounded in an analogy or scenario
- A [Pause:] moment exists but the setup is only one sentence
- The confusion_buster is named but resolved in one line
- The landing line arrives before the room has had time to absorb it

These are signs to expand, not trim.

---

# CONCEPT TIER — PACING

| concept_tier | Pacing |
|--------------|--------|
| `foundation` | Slower. More space between ideas. More [Pause:] moments. The analogy gets extra time. |
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

Do not pivot to the solution immediately after naming the problem.
Spend at least two sentences letting the consequence land — what
is actually breaking, what the business is losing, why this specific
failure mode matters. The reader needs to feel the problem before
they're ready to understand why the pattern solves it.

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
The landing line must be specific to this pattern — not a generic
statement about AWS or cloud design. A landing line that could apply
to any pattern has failed.

FAIL: "Auto Scaling means you pay for what you use when you use it."
(True of any auto-scaling service. Doesn't name what this specific
pattern solves or what the operator's role is.)

PASS: "Define the floor, the ceiling, and the signal — Auto Scaling
handles everything in between, including the failures you didn't plan for."
(Names the operator's role, the system's role, and the resilience
property in one sentence. Specific to this pattern.)

**Accuracy rule — AZ failure mechanics:** When teaching what happens
when an Availability Zone fails, describe the mechanism accurately.
Auto Scaling does not detect AZ impairment and consciously route
around it. The actual sequence: failed instances fail their health
checks, Auto Scaling terminates them and launches replacements, and
the rebalancing algorithm places new instances in zones with fewer
running instances — which naturally avoids the impaired zone.
The mechanism is reactive, not predictive. Scripts that say Auto
Scaling "detects AZ impairment" describe a capability it does not have.

For bridge spines: the landing line is the key insight that sharpens understanding.
For mental_model spines: the landing line shows how the parts form a whole.

---

# WHAT MUST APPEAR IN EVERY SCRIPT

These ingredients must all be present. Their order and weight
is yours to decide based on the three decisions above.

**An opening that frames the session.**
The first paragraph tells the room what they are going to understand
by the end — not as a list of topics, but as a promise. One or two
sentences that make the reader want to keep going.
"By the end of this, you'll know exactly when to reach for X and why
it exists — and you'll have a picture in your head that sticks."
Not a formal agenda. A reason to pay attention.

**The concept in plain words.**
The `concept_spine` spoken naturally. Said once clearly early.
Not read out — spoken as the teacher's own words.

**The real world picture.**
The `real_world_analogy` introduced early, returned to at least
once more when mechanics need grounding. Never replaced with
a second analogy. The scenario must use one of the approved
company contexts (see ANALOGY COMPANIES below) — not a generic
"imagine a company" or an arbitrary business type.

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
Followed by a [Pause:] that gives the reader a beat to reason
through what they'd do before the teacher continues.

**The confusion resolved.**
From `confusion_buster` — named early, resolved fully before the end.
If `links.contrast_with` is populated, the prose states the differences
clearly and concisely.
If `links.often_confused_with` is populated — flag briefly early,
do not fully resolve.

**At least two [Pause:] moments.**
Each one gives the reader a genuine beat to think — a specific
scenario or mechanism to reason through before the teaching continues.
Not "does that make sense?" — something with content and direction.

**A closing summary of key learnings.**
Two to four sentences before the landing line that pull together
what the room now knows. Not a list. Not "in summary". A brief
spoken recap in the teacher's voice — the kind of thing a teacher
says while slowly capping the marker.
"So here's where we've landed. You know what X is and why it exists.
You know the one situation where you'd choose it over Y.
And you know the catch that trips everyone up."
This must be genuinely specific to this concept — not generic.

**The landing line.**
Last. One sentence. Repeatable three months later.

---

# PAUSE QUALITY RULES

A [Pause:] is a beat of deliberate reflection — not a quiz, not a
question to answer out loud. It gives the reader a moment to sit
with a scenario or mechanism before the teacher continues.

The pause names something specific to think about. It does not ask
for a spoken answer. It does not test recall. It creates the
experience of reasoning through a problem rather than passively
receiving the answer.

WRONG — vague non-pause:
"[Pause: Think about what you've just learned.]"
(Nothing to think about. No direction.)

WRONG — quiz disguised as a pause:
"[Pause: What are the three scaling policy types?]"
(This is a recall test. The reader either knows it or doesn't.
No thinking happens.)

RIGHT — scenario pause:
"[Pause: Picture your 3 instances at 95% CPU. New capacity is
3 minutes away. What's happening to your users right now?]"
(Specific. The reader can reason through it. The teaching that
follows will land harder because the reader just felt the problem.)

RIGHT — mechanism pause:
"[Pause: Two health checks running simultaneously — one at the
load balancer, one at the EC2 layer. Think about which one would
catch a crashed application process first, and why.]"
(Directed. The reader applies what was just taught. The answer
follows naturally in the next paragraph.)

**Placement rule:** A [Pause:] must come after the content needed
to reason through it has been taught — never before. The reader
must have the building blocks. The pause confirms landing; it does
not introduce.

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

# ANALOGY COMPANIES — USE ONLY THESE

All real-world scenarios and analogies must be grounded in one
of these four companies. Choose the one that fits the concept
most naturally and stick with it throughout the script.

**Amazon (e-commerce + logistics)**
Use for: scale, traffic spikes, inventory, ordering pipelines,
Black Friday load, warehouse fulfilment, delivery routing.
Best fit: auto scaling, CDN, queuing, caching, databases, cost.

**Netflix (streaming + content delivery)**
Use for: global content distribution, recommendation engines,
regional failover, high read traffic, video transcoding pipelines.
Best fit: CDN, S3, Lambda, read replicas, multi-region, resilience.

**Twitter / X (social feed + real-time events)**
Use for: fan-out writes, timeline generation, viral traffic spikes,
event streams, pub/sub, rate limiting.
Best fit: SNS, SQS, Kinesis, caching, horizontal scaling.

**LinkedIn (professional network + jobs)**
Use for: profile reads, search indexing, connection graphs,
notification delivery, B2B data pipelines.
Best fit: search, graph databases, batch processing, IAM, VPC.

## Rules

- Pick ONE company per script. Do not mix companies.
- Introduce the company naturally the first time, then use it directly.
  First use: "Take Netflix, for example — ..." or "Consider Amazon's situation: ..."
  Subsequent uses: "Netflix's approach...", "Amazon's pipeline...", "Twitter's feed..."
  Not "Think Netflix" or "imagine a large e-commerce company."
- The company provides the scenario. The AWS concept solves its problem.
- If the concept_entry's real_world_analogy already names one of these
  companies, use that one. If it names something else, map it to the
  closest match from the four above.
- Do not invent new companies, use generic business types ("a startup",
  "an enterprise"), or use companies outside this list.

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
[Pause:], no paragraph breaks. A real teacher breathes.
Break up long explanations. No paragraph should exceed six sentences.

**The Announcement Opening.**
"Today we are going to cover high availability, which is an
important concept in the Cloud Concepts domain." Never.
Start with a question, a problem, or a scenario.

**The List Dump.**
"High availability has three characteristics: first... second...
third..." Real teaching builds one idea at a time. It does not
start with the structure.

**The Empty Pause.**
"[Pause: Think about what you've just learned.]" after a hard concept.
A pause needs a specific scenario or mechanism to sit with —
not a vague invitation to reflect.

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
- [ ] For pattern spines: whole-picture paragraph planned — one
      narrative of end-to-end flow before any service is introduced
- [ ] At least two [Pause:] moments planned — each gives the reader
      a specific scenario or mechanism to reason through
- [ ] Every [Pause:] comes after the content needed to reason through it
- [ ] Analogy company chosen from approved list (Amazon / Netflix / Twitter / LinkedIn) — not a generic business
- [ ] Same company used throughout — no switching mid-script

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
- `[Pause: one sentence naming what to think about]` on its own line
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

Section headings (`##`) are navigation markers for the teacher —
not topic announcements for the learner. They signal where a new
teaching block begins, nothing more.

Rules for section headings:
- Maximum 4 headings per script
- A heading must never announce what is about to be taught
- A heading should be evocative, not descriptive — a phrase that
  creates curiosity or names a moment, not a component or a concept
- The prose itself must carry all transitions between ideas
  A heading is never a substitute for a transition sentence

The transition between teaching blocks must always appear in the
last sentence of one block or the first sentence of the next —
never delegated to a heading.

WRONG heading: "## The Auto Scaling Group Manages the Fleet"
RIGHT heading: "## When the Load Hits"

WRONG heading: "## CloudWatch Metrics Drive Scaling Decisions"
RIGHT heading: "## What the System Is Watching"

Good heading examples:
- `## The Plane That Keeps Flying`
- `## Why Two Seconds Is Sometimes Too Long`
- `## Standby vs Always On`
- `## The Decision Nobody Wants to Make`

Bad heading examples — never use these:
- `## Opening`
- `## The Analogy`
- `## The Mechanics`
- `## Conclusion`
- `## Close`
- `## Summary`
- `## [~90 seconds]`
- Any heading that names a service, component, or AWS concept

No timing estimates anywhere in the output.

---

# HOW TO USE THIS PROMPT

Paste this prompt into a conversation, then paste a single concept
entry from the expanded concepts file beneath it.

The generator produces one complete teaching script for that concept.

The script is designed to be used directly — the teacher reads
through it once before delivering it. No other preparation needed.

Generate the complete teaching script now.