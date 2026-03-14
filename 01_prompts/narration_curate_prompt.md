# AWS Concept Mastery — Narration Seam Repair
## Stage 4c — Curate
### curate_prompt.md

---

# PURPOSE

You receive a teaching script that was generated in multiple sections.
Each `##` heading marks a section boundary. Your job is to repair the
seams between sections so the script reads as one continuous piece of
spoken teaching — not a collection of separate episodes.

This is surgical editing. You are not rewriting the script.
You are welding the joints.

---

# INPUT

TITLE: {{TITLE}}

SCRIPT:
{{SCRIPT}}

---

# THE ONE PROBLEM YOU ARE SOLVING

Each section was generated independently. The result is that sections
end abruptly and begin cold. The reader can feel the joins.

A section ending abruptly sounds like:
> "...and that's how the route table works."
> `## The Next Section`
> "Security groups operate at the instance level."

The reader loses the thread. There is no bridge. No reason to keep reading.

A cold section opening sounds like:
> "Security groups are stateful firewalls that..."

The reader has no sense of why this comes next, or what connects it
to what they just read.

Your job is to warm these joins.

---

# WHAT YOU MAY CHANGE

Only the seam zones — defined as:
- The **last 1–3 sentences** before a `##` heading
- The **first 1–3 sentences** after a `##` heading

Outside these zones: zero changes. Not a word.

Within these zones you may:
- Add a short bridge sentence (max one sentence) at the end of a section
  that creates forward momentum into the next topic
- Rework the opening sentence of a section to acknowledge what just
  came before, or to frame why this topic follows naturally
- Tighten or slightly reword a closing sentence that ends too flatly
- Trim an opening sentence that re-introduces something already established

You may NOT:
- Change any `[Think: ...]` marker — not the text, not the position
- Change the YAML front matter
- Change the landing line (the final sentence of the script)
- Move content from one section to another
- Add new facts, examples, numbers, or concepts
- Change any sentence outside the seam zones
- Rewrite entire paragraphs — even in the seam zones
- Remove `##` headings
- Change the order of sections

---

# THE BUDGET

Count the words in the input script body (excluding front matter).
Your total changes — words added plus words removed — must not exceed
**15% of the original word count**.

Use the budget wisely. Spend it on the worst seams first.
A script with two jarring joins and six smooth ones should have
its budget concentrated on those two.

If the script already flows reasonably between sections, make only
minimal repairs and return most of the budget unused.

---

# WHAT A GOOD SEAM SOUNDS LIKE

**Before (abrupt ending + cold opening):**
> The route table finds no match and drops the packet. The peering
> connection is just the tunnel. You must add explicit routes.
>
> `## Why the Street Addresses Matter`
>
> Before you can peer two VPCs, they need non-overlapping CIDR blocks.

**After (repaired):**
> The route table finds no match and drops the packet. The peering
> connection is just the tunnel — and a tunnel with no directions
> is useless. That brings us to the first thing you need before
> you can even build the tunnel.
>
> `## Why the Street Addresses Matter`
>
> The prerequisite is simple but non-negotiable: the two VPCs cannot
> share any IP address space. Non-overlapping CIDR blocks.

Notice:
- The ending now has forward momentum — "that brings us to..."
- The opening now frames the section as a prerequisite, connecting it
  to the previous section's problem
- No facts were changed. One sentence was added at the end.
  The opening was lightly reworked — not rewritten.

---

# SELF-DEFEATING REPAIRS TO AVOID

**The Announcement Bridge** — adding "Now let's look at X" or
"Next, we'll explore Y." These are the most common AI tells.
They tell the reader what is coming instead of creating momentum.
A good bridge makes the reader want to keep reading. An announcement
just labels the next section.

WRONG: "Now let's explore why CIDR blocks matter."
RIGHT: "And that starts with a constraint you cannot negotiate around."

**The Summary Close** — ending a section with "So in summary..."
or "In other words..." before the next heading. Teaching scripts
do not summarise mid-lesson. The reader is still in the room.

**The Restart Open** — beginning a new section by re-explaining
something already established. "Remember that VPCs are isolated..."
when the entire previous section was about VPC isolation. Trust the
reader's memory. They just read it.

**The Hollow Connector** — generic phrases that gesture at connection
without creating it. "This is connected to what we just discussed."
"Building on the previous section." These add words without adding
flow.

---

# OUTPUT FORMAT

Return the complete script exactly as it was, with only the seam
repairs applied.

The output must:
- Begin with the YAML front matter block, unchanged
- Preserve every `##` heading, unchanged, in the same order
- Preserve every `[Think: ...]` marker, unchanged, in the same position
- Preserve every sentence outside the seam zones, word for word
- End with the same landing line as the input

Append this block at the very end of the output, after the script:

```
---
CURATE_REPORT:
  seams_repaired: N
  words_before: N
  words_after: N
  word_delta_pct: N.N%
  budget_used: N.N% of 15%
  changes:
    - section: "## Section Heading"
      type: "closing bridge added / opening reworked / both"
      note: "one sentence describing what changed and why"
```

This report is for logging only — the pipeline strips it before
saving the file.

---

# OUTPUT RULE

Return the complete repaired script followed by the CURATE_REPORT block.
No markdown fences. No preamble. No explanation outside the report block.
Start with `---` (the YAML front matter opening).