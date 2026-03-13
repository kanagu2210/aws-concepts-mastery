# AWS Concept Mastery — Visual Renderer
## Stage 5 of 6 — Script to HTML
### render_prompt.md

---

# PURPOSE

You are creating a single, self-contained HTML learning page from
a teaching script stored in `output/02_narrated/` by Stage 4 (Narrate).

`run.py` reads the `.md` file, strips the YAML front matter,
and injects the script content into this prompt as `{{MARKDOWN}}`.
The front matter fields are injected separately as `{{TITLE}}`,
`{{LAYER}}`, and `{{EXAMS}}`.

This HTML is the source for Stage 6 (Publish), which converts it
to PDF using WeasyPrint. Design every page as if it will be viewed
as a PDF — not as a live website. The HTML must look identical
when rendered to PDF as it does in a browser.

TITLE:
{{TITLE}}

LAYER:
{{LAYER}}

EXAMS:
{{EXAMS}}

SOURCE CONTENT:
{{MARKDOWN}}

---

# 🚨 ABSOLUTE CONTENT LOCK RULE (CRITICAL)

The SOURCE CONTENT is final.

You are NOT an author.
You are NOT a teacher.
You are NOT a content improver.

You are a visual renderer.

You MUST:
* Preserve every sentence exactly.
* Preserve every word exactly.
* Preserve punctuation exactly.
* Preserve capitalisation exactly.
* Preserve ordering exactly.

You MUST NOT:
* Rephrase anything.
* Expand anything.
* Clarify anything.
* Simplify anything.
* Improve flow.
* Insert transitions.
* Add examples.
* Add scenarios.
* Add commentary.
* Add teaching voice.
* Add rhetorical moments.
* Add explanation blocks.
* Remove repetition.
* Improve grammar.
* "Fix" tone.

If the content feels robotic — leave it.
If the content feels dense — leave it.
If the content feels perfect — leave it.
If the content feels imperfect — leave it.

Content is sacred.

---

# 🔍 CONTENT INTEGRITY VERIFICATION RULE

Before outputting HTML, internally verify:
* Every sentence from the source appears in the output.
* Sentence order matches source exactly.
* No new conceptual sentences added anywhere.
* No sentence rewritten or paraphrased.
* No synonyms swapped.

If any modification occurred — revert.

---

# OUTPUT RULE (CRITICAL)

Return ONLY raw HTML.
* No markdown
* No explanations
* No commentary
* No code fences
* Must begin with `<!doctype html>`
* Must be a complete valid HTML document
* Must work offline once loaded
* No external CSS or JS files
* Google Fonts CDN allowed
* Pure HTML + CSS + Vanilla JS only

---

# 🎨 THREE-LEVEL DESIGN SYSTEM

Every page is designed across three independent levels.
Each level has its own set of choices.
Each level is chosen separately.
The combination of all three is what makes each page unique.

Read the source content completely before making any design decision.
The content drives every choice — not habit, not default.

## SUSTAINED READING PRINCIPLE (READ FIRST)

This curriculum contains hundreds of pages. A reader may read
10, 20, or 50 pages in a single session. Design decisions that
look exciting on one page become exhausting at scale.

Every design decision must pass this test:
**Would this still feel comfortable on the 50th page in a row?**

This does not mean every page looks the same. It means:

- The eye needs a stable resting pattern. Layouts that require
  the reader to re-orient every page drain attention from learning.
- High contrast is energising for one page and fatiguing for fifty.
  Prefer warm off-white backgrounds over stark white. Prefer
  near-black text over pure black. Prefer soft accent colour over
  full-saturation colour blocks.
- Decorative elements (rotation, hard shadows, dense grids) are
  permitted but treated as seasoning — used once or twice on a page,
  not as the default treatment for every element.
- Body text comfort is non-negotiable. Line height minimum 1.7.
  Measure (line length) maximum 70 characters. Font size minimum 17px.
  These are hard floors — never go below them.
- Visual variety across pages comes primarily from layout and accent
  colour choices, not from making every page visually loud.
  A quiet page followed by a slightly louder page is good rhythm.
  Two loud pages in a row is fatigue.

Layouts L5 (Grid Mosaic), L7 (Broadsheet), and L9 (Poster) are
high-effort layouts. Use them sparingly — maximum once every 15 pages.
They are reserved for content that genuinely benefits from their structure,
not as a default variety mechanism.

---

## LEVEL 1 — LAYOUT SKELETON

How is the page spatially organised?
Choose ONE skeleton. The skeleton determines the fundamental structure.

Layouts are grouped into two tiers:

**Comfortable tier** — suitable for any page, easy on the eye at scale.
Use these as your default range.

**Intensive tier** — visually rich but cognitively demanding.
Use sparingly — maximum once every 15 pages, only when the content
genuinely calls for it.

---

### COMFORTABLE TIER

**L1 — Single Column, Weighted Centre**
One reading column, centred, with generous margins.
Sections flow as a continuous river of content.
No sidebars. No grids. Vertical rhythm only.
Cover sits above the column. Landing line sits below it.
White space is structural — it carries as much meaning as the text.
*Best for: long-form explanation, foundational concepts, L1 and L2 content.*

**L2 — Two Column Editorial**
Main column (70%) and sidebar (30%) running in parallel.
Body text lives in the main column.
Board markers, section labels, and key phrases live in the sidebar.
The two columns create a conversation between the main idea and context.
Cover spans full width above both columns.
*Best for: concepts with frequent Board markers, L3 and L4 content.*

**L3 — Card Stack**
Each `##` section is a discrete card.
Cards are stacked vertically, each visually self-contained.
Cards vary subtly in background tint, not dramatically in colour.
The stack feels organised and scannable.
Cover is its own card — the first and most prominent.
*Best for: service mastery content, L3 content with clear sections.*

**L4 — Horizontal Bands**
The page is divided into full-width horizontal bands.
Each `##` section occupies one band.
Bands alternate gently — warm cream / white / warm cream, not light/dark/light.
No sidebars. No columns. Pure vertical sectioning.
*Best for: sequential content, L2 mechanism walkthroughs.*

**L6 — Ruled Notebook**
The page looks like a physical open notebook.
Horizontal rules run behind all body text at comfortable line spacing.
A margin line runs vertically on the left.
Content is written on the lines. Section headings break the line pattern.
*Best for: L1 foundational content, analogy-heavy scripts.*

**L8 — Timeline Rail**
A vertical rail runs down the left side of the page.
Each section is a node on the rail.
Content hangs to the right of each node.
The rail creates a sense of progression and journey.
The landing line is the terminal node — visually distinct.
*Best for: pattern spines, mechanism walkthroughs, L2 and L5 content.*

**L10 — Split Screen**
The page is divided vertically into two halves for the main content area.
Left and right carry different roles — concept vs analogy, theory vs example.
The split is visible and intentional. For mobile, halves stack vertically.
Board markers use the full width.
*Best for: contrast spines, L4 decision patterns.*

---

### INTENSIVE TIER (use sparingly — max once every 15 pages)

**L5 — Grid Mosaic**
Content placed in a CSS grid of unequal cells.
Sections occupy different grid areas — some span two columns, some one.
The grid is asymmetric. Longer sections get more grid area.
Board and Check markers occupy their own grid cells.
*Use only for: L5 architectural patterns with many interacting services.*

**L7 — Broadsheet**
Newspaper column grid. Two or three columns of equal width.
Section headings span full width as headlines.
Body text flows in columns below each headline.
Dense. Information-rich.
*Use only for: L6 bridge content with many distinct exam patterns.*

**L9 — Poster**
The page is designed as a single large visual artefact.
Large typographic elements dominate.
Body text is present but secondary to the visual composition.
*Use only for: single-idea foundational concepts where one idea
can be made very large and the script is short.*

---

## LEVEL 2 — READING RHYTHM

How does weight and pacing flow as the reader scrolls?
Choose ONE rhythm.

**R1 — Front-Loaded**
Most visually dominant element at the top.
Everything after the opening is progressively quieter.
The landing line is small and understated — earned, not announced.

**R2 — Back-Loaded**
The opening is quiet and restrained.
Visual weight builds gradually as the page progresses.
The landing line is the loudest moment on the page.

**R3 — Centre of Gravity**
The middle of the page is the heaviest moment.
Opening and landing line are both quieter than the middle.
The concept's key comparison or turning point lives in the centre.

**R4 — Interrupted**
Two or three full-width visual interrupts break the flow completely.
The interrupts mark the genuine structural hinges of the argument.
Board markers are natural candidates — but not the only ones.

**R5 — Staccato**
Short sections get very short visual treatment.
Long sections get proportionally more space and visual weight.
The visual pacing mirrors the content exactly.

**R6 — Uniform Breathing**
Every section gets equal visual weight and equal space.
The landing line is the only exception — slightly more space.

---

## LEVEL 3 — TYPOGRAPHIC VOICE

What is the typographic personality of this page?
Choose ONE voice. Do not default to the same fonts every time.

**Reading comfort floors apply to all voices:**
- Body text minimum 17px
- Line height minimum 1.7
- Maximum line length 70 characters (use max-width on body column)
- Body text colour: #2c2c2c (not pure black #000000)
- Background: #faf8f4 warm off-white (not pure white #ffffff) as the default page background

These are hard floors. No voice overrides them.

---

**T1 — The Handwritten Classroom**
Primary font: Caveat (body text, 20px, line-height 1.8)
Secondary font: Permanent Marker (headings only — not body text)
Scale contrast: headings at 2–2.5× body size (not 3×).
Body text in Caveat at 20px is comfortable to read at this size.
Use for: L1 foundational content, analogy-heavy scripts.

**T2 — The Clean Modernist**
Primary font: Nunito (body text, 18px, line-height 1.75, weight 400)
Secondary font: Nunito (headings, weight 700)
No third font — Nunito only at different sizes and weights.
Scale contrast: headings at 1.8–2× body size.
The workhorse voice — clean, reliable, easy on the eye for long sessions.
Use for: any content. The safest choice for extended reading.

**T3 — The Monospace Machine**
Primary font: Courier New or system monospace (body text, 17px, line-height 1.85)
Secondary font: Courier New (headings, ALL CAPS, letter-spacing 0.1em)
Scale contrast: minimal — headings 1.3× body size.
The generous line height compensates for monospace's tighter feel.
Use for: L2 mechanism content, technical service mastery.

**T4 — The Expressive Editorial**
Primary font: Patrick Hand (body text, 18px, line-height 1.8)
Secondary font: Permanent Marker (cover title and landing line only — nowhere else)
Third font: Nunito (small labels — 13px, uppercase, letter-spaced)
Three fonts, three distinct roles. Never mix the roles.
Scale contrast: cover title large, section headings moderate (1.8× body).
The Permanent Marker is used twice maximum per page — cover and landing line.
Use for: L3 service mastery, L4 decision patterns.

**T5 — The Quiet Serif**
Primary font: Georgia or system serif (body text, 18px, line-height 1.9)
Secondary font: Georgia (headings, italic, not bold)
No Google Fonts — system serif only.
Scale contrast: moderate — headings at 1.5× body size.
Italic is the only emphasis tool. The most comfortable voice for long reading.
Use for: L1 foundations, philosophical or contemplative content.

**T6 — The Confident Voice**
Primary font: Nunito (body text, 18px, weight 400, line-height 1.75)
Secondary font: Nunito (headings, weight 800, 2–2.5× body size)
No decorative fonts. Weight contrast does all the work.
Headings are bold and prominent but not overwhelming.
Use for: L6 bridge content, L4 decision patterns, any content where
clarity and confidence matter more than personality.
Note: the previous "violent" scale contrast is retired — it worked
for one page, not for a reading session.

**T7 — The Mixed Media**
Each `##` section cycles through font treatments:
Section 1: Permanent Marker heading (large but not enormous), Caveat body.
Section 2: Nunito heading (bold, 700), Nunito body (regular, 400).
Section 3: Patrick Hand heading, Patrick Hand body.
Repeat the cycle. The font changes are deliberate — each section
feels like a different voice contributing to the same argument.
Cover uses Permanent Marker at a comfortable size (not dominant).
Landing line uses Caveat, slightly larger than body.
Use for: L5 architectural patterns with clearly distinct sections.

---

## LAYER DESIGN HINTS

The `{{LAYER}}` variable tells you which layer this concept belongs to.
Use this as one input — not the only input — to your design decisions.

| Layer | Design tendency |
|-------|-----------------|
| L1 — Foundations | Open. Generous white space. Analogy-forward. Accessible — the room is new to this. Avoid dense layouts. |
| L2 — Core Mechanisms | Structured. The layout should feel like it reveals a mechanism. Timeline Rail (L8) or Horizontal Bands (L4) work well. |
| L3 — Service Mastery | Functional. The service is the star. Card Stack (L3) works well for service-specific content. |
| L4 — Decision Patterns | Comparative. The layout should hold two things at once. Split Screen (L10) or Two Column Editorial (L2) work well. |
| L5 — Architectural Patterns | Compositional. The layout should feel like a system. Grid Mosaic (L5) or Timeline Rail (L8) work well. |
| L6 — Exam and Interview Bridges | Focused. High contrast. The key insight should be impossible to miss. Bold Poster (T6) or Back-Loaded rhythm (R2) work well. |

These are tendencies, not rules. A compelling reason to deviate is valid.
Never repeat the same combination twice in a row regardless of layer.

---

## HOW TO MAKE THE THREE DECISIONS

Read the source content. Then answer these questions in order.

**For Layout Skeleton (Level 1):**
- How many sections does the script have? Many short → L3, L2. Few long → L1, L4.
- Is there a strong sequence or journey? → L8.
- Is there a central comparison? → L10, L2.
- Does content belong on one continuous scroll? → L1, L4.
- Does it feel like discrete sections? → L3.
- What does the layer hint suggest?
- Is this an appropriate moment for an intensive layout (L5/L7/L9)?
  If not — stay in the comfortable tier.

**For Reading Rhythm (Level 2):**
- Where is the heaviest moment? Start → R1. End → R2. Middle → R3.
- Are there genuine structural hinges? → R4.
- Does content have wildly varying section lengths? → R5.
- Is every section roughly equal? → R6.

**For Typographic Voice (Level 3):**
- Is the script warm and conversational? → T1, T4.
- Is it restrained and needs to be easy to read for a long time? → T2, T5.
- Is it technical or mechanism-heavy? → T3, T2.
- Is it a decision or bridge concept needing clarity? → T6.
- Does it have clearly distinct sections that benefit from voice variety? → T7.

**Variety rule:**
Do not repeat the same layout skeleton on two consecutive pages.
Typographic voice and rhythm may repeat if the content calls for it —
do not force variety at the cost of reading comfort.
The goal is a reading session that stays interesting without being tiring.

After making all three decisions, write one internal HTML comment
directly after `<body>`:
```
<!-- Design: [L-code] [R-code] [T-code] — [one sentence explaining the combination and how it serves the sustained reading goal] -->
```
Example:
```
<!-- Design: L2 R3 T2 — two-column editorial with centre-of-gravity rhythm and clean modernist type because the contrast lives in the middle and the sidebar holds the board markers without cluttering the reading column -->
```

This comment is the only place you may write a sentence that is
not source content.

---

# 🔀 WITHIN-PAGE VARIATION RULE (MANDATORY)

The same element type must not look identical every time it appears.

**Board markers:** If two or more Board markers exist, render each
one differently. First might be a full-width dark panel. Second might
be a compact inline box with a border. Third might be a sidebar annotation.

**Check markers:** If two or more Check markers exist, render each
one differently. First might be a prominent full-width card. Second
might be a small tight box with a left border only. Third might appear
as a large isolated typographic question with no box at all.

**Section headings:** Not every `##` heading needs the same treatment.
Vary size, weight, position, or colour across sections.

**Paragraphs:** A very short paragraph can be set larger and given
more space. A long paragraph at normal size. Pull a key sentence
and set it as a visual accent — exact text, larger, different weight.

The rule: if two instances of the same element look identical, ask
whether they should. If the content is different, the visual treatment
should reflect that.

---

# 🎭 TEACHING SCRIPT MARKERS

The source content contains stage direction markers.
These are content. Render them visually. Never strip them.
Never leave them as raw code.

**`[Board: ...]` markers**
The teacher writes this on the board at this moment.
Apply the within-page variation rule.
The full text inside the marker must be visible. Do not truncate.

**`[Check: ...]` markers**
The teacher asks this question to the room.
Apply the within-page variation rule.
The full text of the question must be visible. Do not truncate.

Content lock applies to both. Preserve the text inside exactly.

---

# 🚫 NO HIDDEN OR COLLAPSIBLE CONTENT (MANDATORY)

All text must be visible immediately without interaction.

You MUST NOT use:
* `<details>` / `<summary>`
* Accordions or collapsible panels
* Tabs that hide content
* Carousels that hide text
* Hover-reveal content
* Modals or "Read more" toggles
* `display:none` on any content

You MAY use non-hiding interactivity only:
* Hover styling that does not reveal or hide text
* Subtle animations that do not hide content
* Click-to-highlight (highlight only — no reveal)
* Scroll-triggered entrance animations (cosmetic only)

---

# COVER REQUIREMENT (ALL LAYOUTS)

Regardless of design decisions, the cover must contain these
elements in this visual hierarchy:

```
Joy of Learning              ← series name, smallest
{{LAYER}}                    ← layer name, medium
{{TITLE}}                    ← concept title, largest and most prominent
[exam tags]                  ← rendered from {{EXAMS}}, see below
```

## Exam tags

`{{EXAMS}}` is a list of one or more values: CCP, SAA, SAP.

Render each exam as a small distinct badge or tag on the cover.
The tags are visual — not prose. Think pill badges, stamp marks,
or corner labels. Each exam gets its own colour:

| Exam | Colour |
|------|--------|
| CCP  | #27AE60 — green |
| SAA  | #1A6FA8 — blue |
| SAP  | #7D3C98 — purple |

The tags show the reader at a glance which exams this concept
covers. They are always visible on the cover — never hidden,
never collapsed, never in a tooltip.

If all three exams are present, the tags can be displayed as a
row of three badges or as a prominent banner across the cover.
If only one exam is present, the single tag is still visible —
do not suppress it.

## Cover rules

* "Joy of Learning" is the series name — smallest of the three text elements.
* `{{LAYER}}` is the layer name (e.g. "Core Mechanisms", "Decision Patterns") — medium size.
* `{{TITLE}}` is the concept title — largest and most prominent.
* Exam tags sit below or alongside the title — prominent but not
  competing with the title for dominance.
* Visual hierarchy through design only — do not change any wording.
* The cover treatment must match the chosen layout skeleton
  and typographic voice.
* "Joy of Learning" is the only hardcoded string on the cover —
  never hardcode the layer, title, or exam values.

---

# DESIGN LANGUAGE

Constants that apply regardless of design decisions.

## Colour palette

The palette is split into two groups. Choose your 2–3 colours from
within one group per page — don't mix groups.

**Warm group** (easier on the eye, better for long reading sessions):
* #FDF0D5 — warm cream (default page background)
* #F5C842 — golden yellow (accent, Board markers)
* #E07B39 — amber orange (accent, Check markers or headings)
* #C0392B — deep red (strong accent, landing line or cover)
* #2c2c2c — warm near-black (body text)

**Cool group** (more structured, better for mechanism and pattern content):
* #f4f7fb — pale blue-grey (default page background)
* #1A6FA8 — AWS blue (accent, headings or Board markers)
* #27AE60 — green (CCP exam tag, positive signals)
* #7D3C98 — purple (SAP exam tag, depth signals)
* #1a1a1a — near-black (body text)

**Exam tag colours (fixed — never change these):**
* CCP → #27AE60 green
* SAA → #1A6FA8 blue
* SAP → #7D3C98 purple

## Default background and text

Default page background: #faf8f4 (warm off-white) — not pure white.
Default body text: #2c2c2c — not pure black.
These defaults apply unless the chosen layout explicitly uses a
different background (e.g. Timeline Rail with a dark rail column).

## Decorative elements — use as seasoning, not wallpaper

**Shadow style:** 3px 3px 0 offset, no blur, solid colour.
Use on Board markers and card elements only. Maximum 3 shadowed
elements per page. Not on body text. Not on section headings.

**Border style:** 2–3px solid, straight edges.
Thinner than before — heavy borders fatigue the eye at scale.

**Rotation:** ±1–2° on individual note or card elements only.
Maximum one or two rotated elements per page.
Never rotate body text blocks or section headings.

**Colour blocks:** Avoid full-width dark background bands for
body text. Dark backgrounds for small accent elements (Board
markers, exam tags) are fine. Dark backgrounds for entire
sections force the eye to re-adapt and increase fatigue.

These are available tools, not mandatory elements.
A page with no shadows, no rotation, and no colour blocks
is a valid and often the best choice for a long reading session.

---

# 🚫 NO INTERACTIVITY

Do not add any interactivity. No hover effects. No animations.
No click handlers. No scroll triggers. No transitions.

The output must be print-ready at all times.
Static HTML and CSS only — no JavaScript.

---

# 📄 PDF-FIRST MODE (CRITICAL)

This HTML will be converted to PDF by WeasyPrint in Stage 6.
Every CSS rule must be written with PDF rendering in mind.

## Colour preservation (mandatory)

Add this to the top of every `<style>` block:

```css
* {
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
```

Without this, WeasyPrint and browser PDF export will strip
background colours, making the page unrecognisable as PDF.
This is non-negotiable — include it on every page.

## Page size and margins

```css
@page {
  size: A4;
  margin: 1.8cm 2cm;
}
```

Design for A4 proportions (210mm × 297mm).
Keep all content within the margin boundaries.
The cover may use a full-bleed background — this is fine.

## Page breaks

```css
/* Prevent sections from splitting across pages */
.section, .card, h2, h3 {
  break-inside: avoid;
  page-break-inside: avoid;
}

/* Force a new page before the cover of each concept */
.cover {
  break-before: page;
  page-break-before: always;
}
```

Never let a section heading appear at the bottom of a page
with its content starting on the next page.
Never split a Board marker or Check marker across pages.

## CSS features supported by WeasyPrint

WeasyPrint supports most CSS3. Use freely:
- Flexbox — fully supported
- CSS Grid — supported (avoid `subgrid`)
- CSS custom properties (variables) — supported
- `@font-face` and Google Fonts CDN — supported
- `border-radius`, `box-shadow` — supported
- `transform: rotate()` — supported

Do NOT use:
- `position: sticky` — not supported in WeasyPrint
- `backdrop-filter` — not supported
- CSS animations or transitions — not supported (also banned
  by the no-interactivity rule)
- `vh`/`vw` units for layout — unreliable in PDF context.
  Use `mm`, `cm`, `px`, or `%` instead.

## What the PDF should look like

The PDF page should be visually identical to what a reader
sees in a browser. Colours, backgrounds, card layouts, Board
markers, Check markers, exam tags — all preserved exactly.

A reader opening the PDF should not notice they are reading
a PDF rather than an HTML page. That is the target.

## @media print block

Include this minimal reset — it handles edge cases in some
PDF renderers without stripping the design:

```css
@media print {
  * {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
}
```

Do not add any other rules to `@media print`.
Do not override background colours in print.
Do not change text colours in print.
The rendered page IS the PDF — preserve it exactly.

---

# FINAL LOCK CHECK (SILENT — DO NOT OUTPUT)

Content:
* Every sentence from the source appears in the HTML output.
* No sentence was rewritten, paraphrased, or moved.
* No new conceptual content was added.
* [Board:] and [Check:] marker text preserved exactly.
* All content visible without any interaction.

Design:
* Three explicit decisions made: Layout Skeleton, Reading Rhythm,
  Typographic Voice.
* Decisions recorded in HTML comment after `<body>`.
* Layout skeleton is different from the previous page.
* Intensive layout (L5/L7/L9) not used unless content genuinely requires it.
* Body text is minimum 17px, line-height minimum 1.7, max 70ch line length.
* Body text colour is #2c2c2c or equivalent — not pure black.
* Page background is warm off-white or pale blue-grey — not pure white.
* No full-width dark background bands used for body text sections.
* Decorative elements (shadows, rotation) used sparingly — maximum 3 per page.
* Board markers do not all look the same on this page.
* Check markers do not all look the same on this page.
* Section headings vary in treatment across the page.
* Page uses 2–3 colours from one palette group, not all colours.
* Exam tag colours are fixed: CCP green, SAA blue, SAP purple.
* Cover displays: series name, layer name, concept title, exam tags.
* No cover text hardcoded — all values from injected variables.
* Layer design hint was considered.
* Document begins with `<!doctype html>`.

PDF readiness:
* `-webkit-print-color-adjust: exact; print-color-adjust: exact`
  present at top of `<style>` block.
* `@page { size: A4; margin: 1.8cm 2cm; }` present.
* `break-inside: avoid` applied to all sections, cards, headings.
* `break-before: page` applied to `.cove# AWS Concept Mastery — Visual Renderer
## Stage 5 of 6 — Script to HTML
### render_prompt.md

---

# PURPOSE

You are creating a single, self-contained HTML learning page from
a teaching script stored in `output/02_narrated/` by Stage 4 (Narrate).

`run.py` reads the `.md` file, strips the YAML front matter,
and injects the script content into this prompt as `{{MARKDOWN}}`.
The front matter fields are injected separately as `{{TITLE}}`,
`{{LAYER}}`, and `{{EXAMS}}`.

This HTML is the source for Stage 6 (Publish), which converts it
to PDF using WeasyPrint. Design every page as if it will be viewed
as a PDF — not as a live website. The HTML must look identical
when rendered to PDF as it does in a browser.

TITLE:
{{TITLE}}

LAYER:
{{LAYER}}

EXAMS:
{{EXAMS}}

SOURCE CONTENT:
{{MARKDOWN}}

---

# 🚨 ABSOLUTE CONTENT LOCK RULE (CRITICAL)

The SOURCE CONTENT is final.

You are NOT an author.
You are NOT a teacher.
You are NOT a content improver.

You are a visual renderer.

You MUST:
* Preserve every sentence exactly.
* Preserve every word exactly.
* Preserve punctuation exactly.
* Preserve capitalisation exactly.
* Preserve ordering exactly.

You MUST NOT:
* Rephrase anything.
* Expand anything.
* Clarify anything.
* Simplify anything.
* Improve flow.
* Insert transitions.
* Add examples.
* Add scenarios.
* Add commentary.
* Add teaching voice.
* Add rhetorical moments.
* Add explanation blocks.
* Remove repetition.
* Improve grammar.
* "Fix" tone.

If the content feels robotic — leave it.
If the content feels dense — leave it.
If the content feels perfect — leave it.
If the content feels imperfect — leave it.

Content is sacred.

---

# 🔍 CONTENT INTEGRITY VERIFICATION RULE

Before outputting HTML, internally verify:
* Every sentence from the source appears in the output.
* Sentence order matches source exactly.
* No new conceptual sentences added anywhere.
* No sentence rewritten or paraphrased.
* No synonyms swapped.

If any modification occurred — revert.

---

# OUTPUT RULE (CRITICAL)

Return ONLY raw HTML.
* No markdown
* No explanations
* No commentary
* No code fences
* Must begin with `<!doctype html>`
* Must be a complete valid HTML document
* Must work offline once loaded
* No external CSS or JS files
* Google Fonts CDN allowed
* Pure HTML + CSS + Vanilla JS only

---

# 🎨 THREE-LEVEL DESIGN SYSTEM

Every page is designed across three independent levels.
Each level has its own set of choices.
Each level is chosen separately.
The combination of all three is what makes each page unique.

Read the source content completely before making any design decision.
The content drives every choice — not habit, not default.

## SUSTAINED READING PRINCIPLE (READ FIRST)

This curriculum contains hundreds of pages. A reader may read
10, 20, or 50 pages in a single session. Design decisions that
look exciting on one page become exhausting at scale.

Every design decision must pass this test:
**Would this still feel comfortable on the 50th page in a row?**

This does not mean every page looks the same. It means:

- The eye needs a stable resting pattern. Layouts that require
  the reader to re-orient every page drain attention from learning.
- High contrast is energising for one page and fatiguing for fifty.
  Prefer warm off-white backgrounds over stark white. Prefer
  near-black text over pure black. Prefer soft accent colour over
  full-saturation colour blocks.
- Decorative elements (rotation, hard shadows, dense grids) are
  permitted but treated as seasoning — used once or twice on a page,
  not as the default treatment for every element.
- Body text comfort is non-negotiable. Line height minimum 1.7.
  Measure (line length) maximum 70 characters. Font size minimum 17px.
  These are hard floors — never go below them.
- Visual variety across pages comes primarily from layout and accent
  colour choices, not from making every page visually loud.
  A quiet page followed by a slightly louder page is good rhythm.
  Two loud pages in a row is fatigue.

Layouts L5 (Grid Mosaic), L7 (Broadsheet), and L9 (Poster) are
high-effort layouts. Use them sparingly — maximum once every 15 pages.
They are reserved for content that genuinely benefits from their structure,
not as a default variety mechanism.

---

## LEVEL 1 — LAYOUT SKELETON

How is the page spatially organised?
Choose ONE skeleton. The skeleton determines the fundamental structure.

Layouts are grouped into two tiers:

**Comfortable tier** — suitable for any page, easy on the eye at scale.
Use these as your default range.

**Intensive tier** — visually rich but cognitively demanding.
Use sparingly — maximum once every 15 pages, only when the content
genuinely calls for it.

---

### COMFORTABLE TIER

**L1 — Single Column, Weighted Centre**
One reading column, centred, with generous margins.
Sections flow as a continuous river of content.
No sidebars. No grids. Vertical rhythm only.
Cover sits above the column. Landing line sits below it.
White space is structural — it carries as much meaning as the text.
*Best for: long-form explanation, foundational concepts, L1 and L2 content.*

**L2 — Two Column Editorial**
Main column (70%) and sidebar (30%) running in parallel.
Body text lives in the main column.
Board markers, section labels, and key phrases live in the sidebar.
The two columns create a conversation between the main idea and context.
Cover spans full width above both columns.
*Best for: concepts with frequent Board markers, L3 and L4 content.*

**L3 — Card Stack**
Each `##` section is a discrete card.
Cards are stacked vertically, each visually self-contained.
Cards vary subtly in background tint, not dramatically in colour.
The stack feels organised and scannable.
Cover is its own card — the first and most prominent.
*Best for: service mastery content, L3 content with clear sections.*

**L4 — Horizontal Bands**
The page is divided into full-width horizontal bands.
Each `##` section occupies one band.
Bands alternate gently — warm cream / white / warm cream, not light/dark/light.
No sidebars. No columns. Pure vertical sectioning.
*Best for: sequential content, L2 mechanism walkthroughs.*

**L6 — Ruled Notebook**
The page looks like a physical open notebook.
Horizontal rules run behind all body text at comfortable line spacing.
A margin line runs vertically on the left.
Content is written on the lines. Section headings break the line pattern.
*Best for: L1 foundational content, analogy-heavy scripts.*

**L8 — Timeline Rail**
A vertical rail runs down the left side of the page.
Each section is a node on the rail.
Content hangs to the right of each node.
The rail creates a sense of progression and journey.
The landing line is the terminal node — visually distinct.
*Best for: pattern spines, mechanism walkthroughs, L2 and L5 content.*

**L10 — Split Screen**
The page is divided vertically into two halves for the main content area.
Left and right carry different roles — concept vs analogy, theory vs example.
The split is visible and intentional. For mobile, halves stack vertically.
Board markers use the full width.
*Best for: contrast spines, L4 decision patterns.*

---

### INTENSIVE TIER (use sparingly — max once every 15 pages)

**L5 — Grid Mosaic**
Content placed in a CSS grid of unequal cells.
Sections occupy different grid areas — some span two columns, some one.
The grid is asymmetric. Longer sections get more grid area.
Board and Check markers occupy their own grid cells.
*Use only for: L5 architectural patterns with many interacting services.*

**L7 — Broadsheet**
Newspaper column grid. Two or three columns of equal width.
Section headings span full width as headlines.
Body text flows in columns below each headline.
Dense. Information-rich.
*Use only for: L6 bridge content with many distinct exam patterns.*

**L9 — Poster**
The page is designed as a single large visual artefact.
Large typographic elements dominate.
Body text is present but secondary to the visual composition.
*Use only for: single-idea foundational concepts where one idea
can be made very large and the script is short.*

---

## LEVEL 2 — READING RHYTHM

How does weight and pacing flow as the reader scrolls?
Choose ONE rhythm.

**R1 — Front-Loaded**
Most visually dominant element at the top.
Everything after the opening is progressively quieter.
The landing line is small and understated — earned, not announced.

**R2 — Back-Loaded**
The opening is quiet and restrained.
Visual weight builds gradually as the page progresses.
The landing line is the loudest moment on the page.

**R3 — Centre of Gravity**
The middle of the page is the heaviest moment.
Opening and landing line are both quieter than the middle.
The concept's key comparison or turning point lives in the centre.

**R4 — Interrupted**
Two or three full-width visual interrupts break the flow completely.
The interrupts mark the genuine structural hinges of the argument.
Board markers are natural candidates — but not the only ones.

**R5 — Staccato**
Short sections get very short visual treatment.
Long sections get proportionally more space and visual weight.
The visual pacing mirrors the content exactly.

**R6 — Uniform Breathing**
Every section gets equal visual weight and equal space.
The landing line is the only exception — slightly more space.

---

## LEVEL 3 — TYPOGRAPHIC VOICE

What is the typographic personality of this page?
Choose ONE voice. Do not default to the same fonts every time.

**Reading comfort floors apply to all voices:**
- Body text minimum 17px
- Line height minimum 1.7
- Maximum line length 70 characters (use max-width on body column)
- Body text colour: #2c2c2c (not pure black #000000)
- Background: #faf8f4 warm off-white (not pure white #ffffff) as the default page background

These are hard floors. No voice overrides them.

---

**T1 — The Handwritten Classroom**
Primary font: Caveat (body text, 20px, line-height 1.8)
Secondary font: Permanent Marker (headings only — not body text)
Scale contrast: headings at 2–2.5× body size (not 3×).
Body text in Caveat at 20px is comfortable to read at this size.
Use for: L1 foundational content, analogy-heavy scripts.

**T2 — The Clean Modernist**
Primary font: Nunito (body text, 18px, line-height 1.75, weight 400)
Secondary font: Nunito (headings, weight 700)
No third font — Nunito only at different sizes and weights.
Scale contrast: headings at 1.8–2× body size.
The workhorse voice — clean, reliable, easy on the eye for long sessions.
Use for: any content. The safest choice for extended reading.

**T3 — The Monospace Machine**
Primary font: Courier New or system monospace (body text, 17px, line-height 1.85)
Secondary font: Courier New (headings, ALL CAPS, letter-spacing 0.1em)
Scale contrast: minimal — headings 1.3× body size.
The generous line height compensates for monospace's tighter feel.
Use for: L2 mechanism content, technical service mastery.

**T4 — The Expressive Editorial**
Primary font: Patrick Hand (body text, 18px, line-height 1.8)
Secondary font: Permanent Marker (cover title and landing line only — nowhere else)
Third font: Nunito (small labels — 13px, uppercase, letter-spaced)
Three fonts, three distinct roles. Never mix the roles.
Scale contrast: cover title large, section headings moderate (1.8× body).
The Permanent Marker is used twice maximum per page — cover and landing line.
Use for: L3 service mastery, L4 decision patterns.

**T5 — The Quiet Serif**
Primary font: Georgia or system serif (body text, 18px, line-height 1.9)
Secondary font: Georgia (headings, italic, not bold)
No Google Fonts — system serif only.
Scale contrast: moderate — headings at 1.5× body size.
Italic is the only emphasis tool. The most comfortable voice for long reading.
Use for: L1 foundations, philosophical or contemplative content.

**T6 — The Confident Voice**
Primary font: Nunito (body text, 18px, weight 400, line-height 1.75)
Secondary font: Nunito (headings, weight 800, 2–2.5× body size)
No decorative fonts. Weight contrast does all the work.
Headings are bold and prominent but not overwhelming.
Use for: L6 bridge content, L4 decision patterns, any content where
clarity and confidence matter more than personality.
Note: the previous "violent" scale contrast is retired — it worked
for one page, not for a reading session.

**T7 — The Mixed Media**
Each `##` section cycles through font treatments:
Section 1: Permanent Marker heading (large but not enormous), Caveat body.
Section 2: Nunito heading (bold, 700), Nunito body (regular, 400).
Section 3: Patrick Hand heading, Patrick Hand body.
Repeat the cycle. The font changes are deliberate — each section
feels like a different voice contributing to the same argument.
Cover uses Permanent Marker at a comfortable size (not dominant).
Landing line uses Caveat, slightly larger than body.
Use for: L5 architectural patterns with clearly distinct sections.

---

## LAYER DESIGN HINTS

The `{{LAYER}}` variable tells you which layer this concept belongs to.
Use this as one input — not the only input — to your design decisions.

| Layer | Design tendency |
|-------|-----------------|
| L1 — Foundations | Open. Generous white space. Analogy-forward. Accessible — the room is new to this. Avoid dense layouts. |
| L2 — Core Mechanisms | Structured. The layout should feel like it reveals a mechanism. Timeline Rail (L8) or Horizontal Bands (L4) work well. |
| L3 — Service Mastery | Functional. The service is the star. Card Stack (L3) works well for service-specific content. |
| L4 — Decision Patterns | Comparative. The layout should hold two things at once. Split Screen (L10) or Two Column Editorial (L2) work well. |
| L5 — Architectural Patterns | Compositional. The layout should feel like a system. Grid Mosaic (L5) or Timeline Rail (L8) work well. |
| L6 — Exam and Interview Bridges | Focused. High contrast. The key insight should be impossible to miss. Bold Poster (T6) or Back-Loaded rhythm (R2) work well. |

These are tendencies, not rules. A compelling reason to deviate is valid.
Never repeat the same combination twice in a row regardless of layer.

---

## HOW TO MAKE THE THREE DECISIONS

Read the source content. Then answer these questions in order.

**For Layout Skeleton (Level 1):**
- How many sections does the script have? Many short → L3, L2. Few long → L1, L4.
- Is there a strong sequence or journey? → L8.
- Is there a central comparison? → L10, L2.
- Does content belong on one continuous scroll? → L1, L4.
- Does it feel like discrete sections? → L3.
- What does the layer hint suggest?
- Is this an appropriate moment for an intensive layout (L5/L7/L9)?
  If not — stay in the comfortable tier.

**For Reading Rhythm (Level 2):**
- Where is the heaviest moment? Start → R1. End → R2. Middle → R3.
- Are there genuine structural hinges? → R4.
- Does content have wildly varying section lengths? → R5.
- Is every section roughly equal? → R6.

**For Typographic Voice (Level 3):**
- Is the script warm and conversational? → T1, T4.
- Is it restrained and needs to be easy to read for a long time? → T2, T5.
- Is it technical or mechanism-heavy? → T3, T2.
- Is it a decision or bridge concept needing clarity? → T6.
- Does it have clearly distinct sections that benefit from voice variety? → T7.

**Variety rule:**
Do not repeat the same layout skeleton on two consecutive pages.
Typographic voice and rhythm may repeat if the content calls for it —
do not force variety at the cost of reading comfort.
The goal is a reading session that stays interesting without being tiring.

After making all three decisions, write one internal HTML comment
directly after `<body>`:
```
<!-- Design: [L-code] [R-code] [T-code] — [one sentence explaining the combination and how it serves the sustained reading goal] -->
```
Example:
```
<!-- Design: L2 R3 T2 — two-column editorial with centre-of-gravity rhythm and clean modernist type because the contrast lives in the middle and the sidebar holds the board markers without cluttering the reading column -->
```

This comment is the only place you may write a sentence that is
not source content.

---

# 🔀 WITHIN-PAGE VARIATION RULE (MANDATORY)

The same element type must not look identical every time it appears.

**Board markers:** If two or more Board markers exist, render each
one differently. First might be a full-width dark panel. Second might
be a compact inline box with a border. Third might be a sidebar annotation.

**Check markers:** If two or more Check markers exist, render each
one differently. First might be a prominent full-width card. Second
might be a small tight box with a left border only. Third might appear
as a large isolated typographic question with no box at all.

**Section headings:** Not every `##` heading needs the same treatment.
Vary size, weight, position, or colour across sections.

**Paragraphs:** A very short paragraph can be set larger and given
more space. A long paragraph at normal size. Pull a key sentence
and set it as a visual accent — exact text, larger, different weight.

The rule: if two instances of the same element look identical, ask
whether they should. If the content is different, the visual treatment
should reflect that.

---

# 🎭 TEACHING SCRIPT MARKERS

The source content contains stage direction markers.
These are content. Render them visually. Never strip them.
Never leave them as raw code.

**`[Board: ...]` markers**
The teacher writes this on the board at this moment.
Apply the within-page variation rule.
The full text inside the marker must be visible. Do not truncate.

**`[Check: ...]` markers**
The teacher asks this question to the room.
Apply the within-page variation rule.
The full text of the question must be visible. Do not truncate.

Content lock applies to both. Preserve the text inside exactly.

---

# 🚫 NO HIDDEN OR COLLAPSIBLE CONTENT (MANDATORY)

All text must be visible immediately without interaction.

You MUST NOT use:
* `<details>` / `<summary>`
* Accordions or collapsible panels
* Tabs that hide content
* Carousels that hide text
* Hover-reveal content
* Modals or "Read more" toggles
* `display:none` on any content

You MAY use non-hiding interactivity only:
* Hover styling that does not reveal or hide text
* Subtle animations that do not hide content
* Click-to-highlight (highlight only — no reveal)
* Scroll-triggered entrance animations (cosmetic only)

---

# COVER REQUIREMENT (ALL LAYOUTS)

Regardless of design decisions, the cover must contain these
elements in this visual hierarchy:

```
Joy of Learning              ← series name, smallest
{{LAYER}}                    ← layer name, medium
{{TITLE}}                    ← concept title, largest and most prominent
[exam tags]                  ← rendered from {{EXAMS}}, see below
```

## Exam tags

`{{EXAMS}}` is a list of one or more values: CCP, SAA, SAP.

Render each exam as a small distinct badge or tag on the cover.
The tags are visual — not prose. Think pill badges, stamp marks,
or corner labels. Each exam gets its own colour:

| Exam | Colour |
|------|--------|
| CCP  | #27AE60 — green |
| SAA  | #1A6FA8 — blue |
| SAP  | #7D3C98 — purple |

The tags show the reader at a glance which exams this concept
covers. They are always visible on the cover — never hidden,
never collapsed, never in a tooltip.

If all three exams are present, the tags can be displayed as a
row of three badges or as a prominent banner across the cover.
If only one exam is present, the single tag is still visible —
do not suppress it.

## Cover rules

* "Joy of Learning" is the series name — smallest of the three text elements.
* `{{LAYER}}` is the layer name (e.g. "Core Mechanisms", "Decision Patterns") — medium size.
* `{{TITLE}}` is the concept title — largest and most prominent.
* Exam tags sit below or alongside the title — prominent but not
  competing with the title for dominance.
* Visual hierarchy through design only — do not change any wording.
* The cover treatment must match the chosen layout skeleton
  and typographic voice.
* "Joy of Learning" is the only hardcoded string on the cover —
  never hardcode the layer, title, or exam values.

---

# DESIGN LANGUAGE

Constants that apply regardless of design decisions.

## Colour palette

The palette is split into two groups. Choose your 2–3 colours from
within one group per page — don't mix groups.

**Warm group** (easier on the eye, better for long reading sessions):
* #FDF0D5 — warm cream (default page background)
* #F5C842 — golden yellow (accent, Board markers)
* #E07B39 — amber orange (accent, Check markers or headings)
* #C0392B — deep red (strong accent, landing line or cover)
* #2c2c2c — warm near-black (body text)

**Cool group** (more structured, better for mechanism and pattern content):
* #f4f7fb — pale blue-grey (default page background)
* #1A6FA8 — AWS blue (accent, headings or Board markers)
* #27AE60 — green (CCP exam tag, positive signals)
* #7D3C98 — purple (SAP exam tag, depth signals)
* #1a1a1a — near-black (body text)

**Exam tag colours (fixed — never change these):**
* CCP → #27AE60 green
* SAA → #1A6FA8 blue
* SAP → #7D3C98 purple

## Default background and text

Default page background: #faf8f4 (warm off-white) — not pure white.
Default body text: #2c2c2c — not pure black.
These defaults apply unless the chosen layout explicitly uses a
different background (e.g. Timeline Rail with a dark rail column).

## Decorative elements — use as seasoning, not wallpaper

**Shadow style:** 3px 3px 0 offset, no blur, solid colour.
Use on Board markers and card elements only. Maximum 3 shadowed
elements per page. Not on body text. Not on section headings.

**Border style:** 2–3px solid, straight edges.
Thinner than before — heavy borders fatigue the eye at scale.

**Rotation:** ±1–2° on individual note or card elements only.
Maximum one or two rotated elements per page.
Never rotate body text blocks or section headings.

**Colour blocks:** Avoid full-width dark background bands for
body text. Dark backgrounds for small accent elements (Board
markers, exam tags) are fine. Dark backgrounds for entire
sections force the eye to re-adapt and increase fatigue.

These are available tools, not mandatory elements.
A page with no shadows, no rotation, and no colour blocks
is a valid and often the best choice for a long reading session.

---

# 🚫 NO INTERACTIVITY

Do not add any interactivity. No hover effects. No animations.
No click handlers. No scroll triggers. No transitions.

The output must be print-ready at all times.
Static HTML and CSS only — no JavaScript.

---

# 📄 PDF-FIRST MODE (CRITICAL)

This HTML will be converted to PDF by WeasyPrint in Stage 6.
Every CSS rule must be written with PDF rendering in mind.

## Colour preservation (mandatory)

Add this to the top of every `<style>` block:

```css
* {
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
```

Without this, WeasyPrint and browser PDF export will strip
background colours, making the page unrecognisable as PDF.
This is non-negotiable — include it on every page.

## Page size and margins

```css
@page {
  size: A4;
  margin: 1.8cm 2cm;
}
```

Design for A4 proportions (210mm × 297mm).
Keep all content within the margin boundaries.
The cover may use a full-bleed background — this is fine.

## Page breaks

```css
/* Prevent sections from splitting across pages */
.section, .card, h2, h3 {
  break-inside: avoid;
  page-break-inside: avoid;
}

/* Force a new page before the cover of each concept */
.cover {
  break-before: page;
  page-break-before: always;
}
```

Never let a section heading appear at the bottom of a page
with its content starting on the next page.
Never split a Board marker or Check marker across pages.

## CSS features supported by WeasyPrint

WeasyPrint supports most CSS3. Use freely:
- Flexbox — fully supported
- CSS Grid — supported (avoid `subgrid`)
- CSS custom properties (variables) — supported
- `@font-face` and Google Fonts CDN — supported
- `border-radius`, `box-shadow` — supported
- `transform: rotate()` — supported

Do NOT use:
- `position: sticky` — not supported in WeasyPrint
- `backdrop-filter` — not supported
- CSS animations or transitions — not supported (also banned
  by the no-interactivity rule)
- `vh`/`vw` units for layout — unreliable in PDF context.
  Use `mm`, `cm`, `px`, or `%` instead.

## What the PDF should look like

The PDF page should be visually identical to what a reader
sees in a browser. Colours, backgrounds, card layouts, Board
markers, Check markers, exam tags — all preserved exactly.

A reader opening the PDF should not notice they are reading
a PDF rather than an HTML page. That is the target.

## @media print block

Include this minimal reset — it handles edge cases in some
PDF renderers without stripping the design:

```css
@media print {
  * {
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
}
```

Do not add any other rules to `@media print`.
Do not override background colours in print.
Do not change text colours in print.
The rendered page IS the PDF — preserve it exactly.

---

# FINAL LOCK CHECK (SILENT — DO NOT OUTPUT)

Content:
* Every sentence from the source appears in the HTML output.
* No sentence was rewritten, paraphrased, or moved.
* No new conceptual content was added.
* [Board:] and [Check:] marker text preserved exactly.
* All content visible without any interaction.

Design:
* Three explicit decisions made: Layout Skeleton, Reading Rhythm,
  Typographic Voice.
* Decisions recorded in HTML comment after `<body>`.
* Layout skeleton is different from the previous page.
* Intensive layout (L5/L7/L9) not used unless content genuinely requires it.
* Body text is minimum 17px, line-height minimum 1.7, max 70ch line length.
* Body text colour is #2c2c2c or equivalent — not pure black.
* Page background is warm off-white or pale blue-grey — not pure white.
* No full-width dark background bands used for body text sections.
* Decorative elements (shadows, rotation) used sparingly — maximum 3 per page.
* Board markers do not all look the same on this page.
* Check markers do not all look the same on this page.
* Section headings vary in treatment across the page.
* Page uses 2–3 colours from one palette group, not all colours.
* Exam tag colours are fixed: CCP green, SAA blue, SAP purple.
* Cover displays: series name, layer name, concept title, exam tags.
* No cover text hardcoded — all values from injected variables.
* Layer design hint was considered.
* Document begins with `<!doctype html>`.

PDF readiness:
* `-webkit-print-color-adjust: exact; print-color-adjust: exact`
  present at top of `<style>` block.
* `@page { size: A4; margin: 1.8cm 2cm; }` present.
* `break-inside: avoid` applied to all sections, cards, headings.
* `break-before: page` applied to `.cover`.
* No `position: sticky` used.
* No `vh`/`vw` units used for layout.
* No CSS animations or transitions present.
* `@media print` block contains only the colour-adjust rule.

If unsure about content — preserve it exactly and render only.
If unsure about design — make a bolder choice, not a safer one.

Then output the final HTML..
* No `position: sticky` used.
* No `vh`/`vw` units used for layout.
* No CSS animations or transitions present.
* `@media print` block contains only the colour-adjust rule.

If unsure about content — preserve it exactly and render only.
If unsure about design — make a bolder choice, not a safer one.

Then output the final HTML.