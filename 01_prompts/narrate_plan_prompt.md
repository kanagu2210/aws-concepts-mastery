# AWS Concept Mastery — Narration Planner
## Stage 4a of 6 — Part Planning for Multipart Narration
### narrate_plan_prompt.md

---

# PURPOSE

You are planning how to split a teaching concept into narration parts.

Each part will become a separate API call that generates one section of
the full teaching script. The parts are then combined into one file.

Your output is a JSON plan. Nothing else. No commentary.

---

# INPUT

You will be given one expanded concept entry. It contains a
`boundary.includes` array — a list of teaching statements ordered
as the intended teaching sequence.

Your job is to group those includes into parts. Each part will be
narrated as a self-contained teaching block that flows into the next.

---

# PARTITIONING RULES

## How many parts

Count the includes in `boundary.includes`.

- 1–4 includes  → 1 part  (no split needed)
- 5–7 includes  → 2 parts
- 8–10 includes → 3 parts
- 11–14 includes → 4 parts
- 15+ includes  → 5 parts maximum

Never create a part with fewer than 2 includes.
Never create a part with more than 5 includes.
Split as evenly as possible. If uneven, front-load — earlier parts
get the extra include, not later ones.

## What each part covers

Parts divide the `boundary.includes` array sequentially.
Part 1 covers includes 0 to N. Part 2 covers N+1 to M. And so on.
The order within each part is always the YAML order — never rearrange.

Includes are referenced by their 0-based index in the array.

## Part focus

Each part needs a short focus label — 3 to 6 words — that describes
what that block of includes is teaching. This is used internally
by the narration prompt to orient the teacher for that block.

Examples of good focus labels:
- "What it is and why it exists"
- "How the mechanism works under the hood"
- "Decision rules and trade-off scenarios"
- "Common misunderstandings corrected"
- "Exam and interview application"

## Handoff sentence

For every part boundary (between part N and part N+1), write one
handoff sentence. This sentence will be injected into the narration
prompt for part N+1 as the planned continuation point.

The handoff must:
- Describe what concept or idea part N will have just finished explaining
- Give part N+1 a natural starting point — not a summary, a momentum line
- Be written as if the teacher just said it — first person, spoken register
- Be one sentence only

Good handoff examples:
- "We've just established how IAM evaluates a request step by step —
   now we need to look at what actually happens when that evaluation hits
   an explicit deny versus finding no matching allow."
- "So that's how the queue holds messages — next I want to show you what
   happens to those messages when the consumer is slow, or crashes
   entirely, and why that changes which service you reach for."

Bad handoff examples:
- "Part 1 is complete. Part 2 will cover the following topics."
  (Not spoken. Structural, not substantive.)
- "Now let's move on to the next section."
  (No content. Gives part 2 nothing to build on.)

---

# OUTPUT FORMAT

Return ONLY valid JSON. No markdown fences. No commentary before or after.
Start directly with `{`.

```
{
  "total_parts": <integer>,
  "parts": [
    {
      "part": 1,
      "include_indexes": [0, 1, 2],
      "focus": "What it is and why it exists",
      "handoff_to_next": "<handoff sentence — omit this field on the final part>"
    },
    {
      "part": 2,
      "include_indexes": [3, 4, 5],
      "focus": "How the mechanism works",
      "handoff_to_next": "<handoff sentence — omit on final part>"
    },
    {
      "part": 3,
      "include_indexes": [6, 7],
      "focus": "Decision rules and exam application"
    }
  ]
}
```

Rules:
- `include_indexes` must be 0-based, sequential, non-overlapping, and cover all includes
- `handoff_to_next` is present on every part except the last
- `focus` is 3–6 words, plain English, no quotes inside the string
- `total_parts` must equal the length of the `parts` array

---

# CONCEPT INPUT