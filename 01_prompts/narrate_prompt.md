# {{PROJECT_NAME}} — Teaching Script Generator
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
phase, phase_name         # which layer this concept belongs to
concept_type                # mental_model | concept | contrast | pattern | bridge
milestones                     # which exams this concept covers
applied                # true if commonly asked in interviews

area, {{ENTITY_FIELD}}
title, concept_tier
conceptual_complexity, cognitive_role
depth_stage               # D1 | D2 | D3 | D4 | D5

core_idea
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

**1. concept_type** — What is the structural shape of this script?
- `mental_model` → framework walkthrough, part by part
- `concept` → standard treatment, shaped by cognitive_role
- `contrast` → both sides introduced early, decision rule repeated
- `pattern` → design walkthrough, services in data flow order
- `bridge` → coaching only, no new concepts, exam/interview focus

**2. layer** — What does the room already know?
Read the phase_name to understand the assumed knowledge level.
Lower layers assume less. Higher layers assume prior layers are mastered.

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

**Landing line in multipart scripts:**

Only the FINAL part ends with the landing line.
All other parts end at a natural breath point — a moment of
resolution on the current block of includes — but do not close
the concept. The room knows there is more coming.

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
Paragraph breaks carry the rhythm.

**[Pause: ...]** A moment where the teacher stops and gives the reader
time to think. Written as a short prompt — one sentence naming what
to sit with. Not a quiz. Not a question to answer out loud.

---

# EXAMPLE — WHAT SPOKEN TEACHING LOOKS AND SOUNDS LIKE

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

# FIELD MAPPING — HOW EACH FIELD SHAPES THE SCRIPT

| Field | How it is used in the script |
|-------|------------------------------|
| `title` | Script title header only — never spoken as an announcement |
| `phase` | Sets the register |
| `concept_type` | Determines the script's structural shape |
| `milestones` | Sets the ceiling on technical depth |
| `applied` | Not used in narration — informational only |
| `core_idea` | The central idea — the teacher returns to this throughout |
| `real_world_analogy` | Read this field to understand what KIND of scenario fits the concept. Then replace it with the closest matching scenario from the approved analogy sources below. |
| `bridge_from` | Opening lines if strong — use only when it creates real momentum |
| `confusion_buster` | Surfaced early as a brief flag, then fully resolved in the middle |
| `boundary.includes` | The teaching content — every include gets spoken and grounded |
| `boundary.excludes` | Hard wall — if a student asks about these, the script has a deflection line |
| `understanding.why_it_exists` | The "why does this matter" moment |
| `understanding.real_world_scenarios` | Used in [Pause:] moments and worked examples |
| `understanding.common_misunderstandings` | Surface as student voice — "someone always thinks this" |
| `links.often_confused_with` | Named briefly early — not fully resolved |
| `links.contrast_with` | Named and contrasted in the prose |
| `depth_stage` | D1–D2 = define and ground; D3 = contrast and apply; D4–D5 = design reasoning |
| `cognitive_role` | Shapes what the script lingers on |
| `concept_tier` | foundation = slower pace; core = full treatment; extension = move faster |

---

# LAYER REGISTER — HOW LAYER CHANGES THE SCRIPT

The `phase` field sets the register and assumed knowledge of the room.
Lower-numbered layers assume the room knows nothing yet.
Higher-numbered layers assume all prior layers are mastered.

Never teach below the layer's register. A higher-layer script that
explains basics from scratch is wrong — the room already knows.
A lower-layer script that assumes expert knowledge is also wrong.

---

# SPINE_TYPE — HOW TYPE SHAPES THE SCRIPT STRUCTURE

The `concept_type` field determines the fundamental shape of the script.

**mental_model** — Walk through a framework part by part.
**concept** — Standard treatment, shaped by cognitive_role.
**contrast** — Both sides introduced early, decision rule repeated.
**pattern** — Design walkthrough, services in data flow order.
**bridge** — Coaching, not teaching. No new concepts.

---

# DEPTH STAGE — PACING, CEILING, AND LENGTH

| depth_stage | Pacing and ceiling | Target length |
|-------------|--------------------|--------------------|
| D1 | Slowest. Maximum analogy time. | 600–900 words |
| D2 | Steady. Full definition plus one contrast. | 800–1100 words |
| D3 | Balanced. Decision reasoning dominates. | 1100–1500 words |
| D4 | Faster on definitions. Design constraints dominate. | 1500–2000 words |
| D5 | Fastest on basics. Scale and prescriptive recommendations. | 2000–2800 words |

**Target the upper third of the range as your minimum.**

---

# THREE DECISIONS BEFORE WRITING

## Decision 1 — What is the entry point?

Choose one: Lead with the problem / the confusion / the story /
the scenario / the bridge / the design problem.

## Decision 2 — Where does the confusion get resolved?

Flag it briefly early, resolve it fully in the middle.

## Decision 3 — What is the landing line?

One sentence. Chosen before you write the script.
Write toward it. It compresses the whole session into a form
the student can repeat back three months later without rereading.

---

# WHAT MUST APPEAR IN EVERY SCRIPT

- An opening that frames the session
- The concept in plain words
- The real world picture (using approved analogy sources)
- The content from `boundary.includes` — every include covered
- The reason it exists
- At least one real scenario with a [Pause:]
- The confusion resolved
- At least two [Pause:] moments
- A closing summary of key learnings (2-4 sentences)
- The landing line

---

# PAUSE QUALITY RULES

A [Pause:] names something specific to think about. It does not ask
for a spoken answer. It creates the experience of reasoning through
a problem rather than passively receiving the answer.

---

# WHAT MUST NEVER APPEAR

- Fixed section labels: Opening, Analogy, Mechanics, Close, Summary
- Timing labels: [~2 minutes], [~90 seconds]
- New concepts not present in the concept entry
- Content from `boundary.excludes`
- Lower-register explanation in a higher-layer script

---

# ANALOGY SOURCES — USE ONLY THESE

All real-world scenarios and analogies must be grounded in one
of these approved sources. Choose the one that fits the concept
most naturally and stick with it throughout the script.

{{ANALOGY_SOURCES}}

## Rules

- Pick ONE source per script. Do not mix sources.
- Introduce naturally the first time, then use it directly.
- The source provides the scenario. The concept solves its problem.
- Do not invent new companies, use generic business types, or use
  sources outside this list.

---

# VOICE RULES

The teacher speaks like someone who knows the material well but
uses plain, simple words. Not academic. Not corporate.

## Simple words

Not "implement" — "build" or "set up".
Not "utilise" — "use".
Not "subsequently" — "then".

## Spoken rhythm

**Fragments.** "Not always. Not even most of the time."
**Mid-sentence pivots.** "You'd think the answer is yes — it isn't."
**Trailing emphasis.** "That's the whole thing. That's it."
**Direct address.** Occasional, not constant.

## Contractions are mandatory

"It is" → "It's". "You are" → "You're". "Do not" → "Don't".

## Banned phrases

Never say: "As we can see…", "It is important to note that…",
"Let's explore…", "In summary…", "Think of it this way…",
"The key insight here is…", "Let me break this down…"

---

# TEACHING STYLE NOTES

{{TEACHING_NOTES}}

---

# OUTPUT FORMAT

The script uses only:
- Plain speech paragraphs
- `[Pause: one sentence naming what to think about]` on its own line
- `##` section headings as navigation markers for the teacher

## File header (mandatory)

```
---
id: <from concept entry>
slug: <from concept entry>
title: <from concept entry>
phase: <from concept entry>
phase_name: <from concept entry>
milestones: <from concept entry>
applied: <from concept entry>
---
```

Section headings (`##`) are navigation markers — not topic
announcements. They should be evocative, not descriptive.

Maximum 4 headings per script.

---

Generate the complete teaching script now.
