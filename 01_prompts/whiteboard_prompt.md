# {{PROJECT_NAME}} — Whiteboard
## Stage 4b — Narration to Progressive SVG Whiteboard
### whiteboard_prompt.md

---

# PURPOSE

You receive a teaching script. You produce one complete, self-contained
HTML page — a scrollable whiteboard showing the board being built up
progressively as the lesson unfolds.

You decide how many panels to draw and what each panel shows.
There are no [Board:] markers in the script. The script is pure
narration. You read it, understand the teaching arc, and decide
where the natural visual moments are.

No navigation. No buttons. No JavaScript. Pure static HTML.

---

# INPUT

TITLE: {{TITLE}}
LAYER: {{PHASE}}
EXAMS: {{MILESTONES}}

SCRIPT:
{{SCRIPT}}

---

# STEP 1 — READ THE SCRIPT COMPLETELY

Read the entire script before drawing anything.

Identify:
- The central concept and its key relationships
- The teaching arc: what the room learns in sequence
- The natural visual moments: where a diagram would genuinely
  help a learner understand what is being explained
- The final insight: the one sentence that captures the whole lesson

Do not draw every paragraph. Draw the moments where a visual
genuinely adds something the words alone cannot.

---

# STEP 2 — DECIDE HOW MANY PANELS

A panel is warranted when the narration introduces or reveals:
- A structural relationship between components (architecture spine)
- A decision rule or threshold (rule pill)
- A before/after state change (failure map, scaling event)
- A process that has meaningful steps in sequence (step chain)
- A comparison between two things (comparison table)
- A quantity or proportion that benefits from being seen (bars)
- The final insight that closes the lesson (insight line)

A panel is NOT warranted for:
- A paragraph that explains something already drawn
- A pause moment (these are for thinking, not drawing)
- A transition sentence
- Repetition of a concept already on the board

**Panel count guidance:**
- D1–D2 scripts (600–1100 words): 2–3 panels
- D3 scripts (1100–1500 words): 3–4 panels
- D4 scripts (1500–2000 words): 4–5 panels
- D5 scripts (2000–2800 words): 5–7 panels

Stay at the lower end unless the content genuinely needs more.
A focused board with 3 excellent panels beats a cluttered board
with 7 mediocre ones.

---

# STEP 3 — PLAN THE SPATIAL LAYOUT

The board is 680 x 480. Plan all zones before drawing panel 1.

Every zone is reserved from panel 1 onward — even if empty —
so later panels fill in correctly without crowding.

Typical zone layout:

  TOP STRIP    (y: 20-70):   Crisis banner — the problem / stakes
  UPPER BAND   (y: 70-200):  Architecture spine — core components + arrows
  MID-LEFT     (y: 200-320): Process zones — step chains, sequences
  MID-RIGHT    (y: 200-320): Rules + thresholds
  LOWER BAND   (y: 320-400): Comparison table or failure scenario
  BOTTOM STRIP (y: 400-450): Proportion bars, cost model
  INSIGHT LINE (y: 462):     The closing sentence of the lesson

Use only the zones the content needs. Not every script needs
every zone. A D2 script might only need the top strip, upper band,
and insight line.

---

# THE CORE MODEL — CUMULATIVE BOARD

Each panel shows the COMPLETE STATE of the board at that moment.
Not just what was just added — everything drawn so far.

Panel 1: the first visual moment — usually crisis + spine.
Panel N: all prior zones plus one new zone.
Final panel: the complete finished board, everything at full opacity.

New elements in THIS panel:    stroke-width="2"  opacity="1.0"
Elements from PRIOR panels:    stroke-width="1"  opacity="0.72"

In the FINAL panel: ALL elements at opacity="1.0" stroke-width="2".
No prior/new distinction — the finished record.

## CRITICAL — KEEP PRIOR ELEMENTS COMPACT

SVG output grows large fast. To stay within output limits:

Prior elements (opacity="0.72") must be drawn as MINIMAL PLACEHOLDERS:
- Boxes: keep the rect and a single label text only. Drop internal
  detail lines — the reader already saw them in the previous panel.
- Arrows: keep the path and a short label (3 words max). Drop
  secondary annotation text on prior arrows.
- Text blocks: reduce to one summary line. Not all original lines.
- Zone backgrounds: keep as-is (they are just a rect, already compact).

New elements (opacity="1.0") get FULL DETAIL — every property,
every label, every annotation line. This is what the reader is
looking at right now.

The final panel is the exception — all elements get full detail
since it is the finished record the student keeps.

This approach keeps each panel roughly the same size regardless
of how many prior zones exist. A panel-8 SVG should be no larger
than a panel-2 SVG.

---

# VISUAL FORMS — HOW NARRATION BECOMES BOARD CONTENT

## Form 1 — CRISIS BANNER
Use for: the problem being solved, the stakes, the nightmare scenario.
Full-width rectangle at the top. Compressed facts only — numbers,
conditions, consequences. No sentences.

## Form 2 — ARCHITECTURE SPINE
Use for: core components and their relationships.
Nodes connected by labelled arrows. The permanent map.
Every node labelled. Every arrow labelled. No exceptions.

## Form 3 — CALLOUT ANNOTATION
Use for: what a component does, its key constraints.
Small rectangle connected by a short line to its target node.
Compressed facts — one per line. Not sentences.

## Form 4 — RULE PILL
Use for: thresholds, policies, conditions, timing rules.
Compact rounded rectangle: condition -> outcome
Stack multiple pills vertically. Actual values from the script only.

## Form 5 — STEP CHAIN
Use for: processes, sequences, what happens in order.
Boxes connected left-to-right by arrows.
Timing annotation below each box. Key insight callout below the chain.

## Form 6 — COMPARISON TABLE
Use for: two things compared across multiple dimensions.
Two-column table with ALL CAPS headers. One row per dimension.
Actual values in every cell. No empty cells.

## Form 7 — FAILURE SCENARIO MAP
Use for: what breaks and what recovers.
BEFORE state, break event, AFTER state.
Red tint for the failed component. Green for recovery path.

## Form 8 — PROPORTION BARS
Use for: quantities, before/after comparisons, relative scale.
Horizontal bars proportional to values. Actual numbers beside each bar.

## Form 9 — INSIGHT LINE
The closing moment. Final panel only.
Position: y=462, full width, text-anchor="middle", x=340.
Font size 14px, font-weight 600.
The one sentence from the script that the student carries out.

---

# SVG TECHNICAL RULES

Every panel: viewBox="0 0 680 480"
All content within x=20 to x=660, y=20 to y=465.

Arrow marker — define in every SVG's defs block:
  <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5"
    markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>

- dominant-baseline="central" on every text element
- fill="none" on every path used as a connector
- No rotated text. No drop shadows. No gradients.
- Minimum font size 11px. Detail annotations may be 10px.
- Arrows stop at box edges — never overlap a box
- Table cells: use rect + text pairs

---

# COLOUR PALETTE

Board background: #ffffff

  Primary components:   fill #f0fdf4   stroke #15803d   text #166534
  Control plane:        fill #fdf3e3   stroke #d97706   text #92400e
  Traffic / clients:    fill #eff6ff   stroke #1d4ed8   text #1e40af
  Failure / problem:    fill #fee2e2   stroke #dc2626   text #b91c1c
  Neutral / tables:     fill #f8fafc   stroke #94a3b8   text #475569
  Annotations:          fill #fffbeb   stroke #fcd34d   text #92400e
  New arrows:           stroke #1e293b
  Prior arrows:         stroke #94a3b8   opacity="0.6"

---

# HTML DOCUMENT STRUCTURE

<!doctype html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Nunito', sans-serif; background: #f5f3ef; color: #2c2a26; }
.wb-shell { max-width: 860px; margin: 0 auto; padding: 1.5rem 1rem 4rem; }
.wb-topbar { display: flex; align-items: center; gap: 1rem;
  padding: 0.75rem 0 1.25rem; border-bottom: 1.5px solid #e0dbd2;
  margin-bottom: 2rem; flex-wrap: wrap; }
.wb-concept-title { font-size: 15px; font-weight: 700; flex: 1; }
.wb-tags { display: flex; gap: 6px; }
.exam-tag { padding: 2px 10px; border-radius: 10px; font-size: 11px;
  font-weight: 700; color: #fff; }
{{MILESTONE_TAG_CSS}}
.wb-panel { margin-bottom: 3rem; }
.wb-panel-label { font-size: 11px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 0.08em; color: #9c9690; margin-bottom: 0.6rem; }
.wb-board { background: #fff; border: 1px solid #e8e3da;
  border-radius: 8px; overflow: hidden; }
.wb-board svg { display: block; width: 100%; height: auto; }
.wb-caption { margin-top: 0.5rem; font-size: 12px; color: #9c9690;
  font-style: italic; line-height: 1.5; }
</style>
</head>
<body>
<div class="wb-shell">
  <div class="wb-topbar">
    <div class="wb-concept-title">{{TITLE}}</div>
    <div class="wb-tags"><!-- one .exam-tag per exam --></div>
  </div>

  <!-- one .wb-panel per visual moment you identified -->
  <div class="wb-panel">
    <div class="wb-panel-label">Board — Step 1 of N</div>
    <div class="wb-board">
      <svg viewBox="0 0 680 480" xmlns="http://www.w3.org/2000/svg"
        font-family="'Nunito', sans-serif">
        <defs>
          <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke"
              stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </marker>
        </defs>
        <rect width="680" height="480" fill="#ffffff"/>
        <g opacity="0.72">
          <!-- prior elements, stroke-width="1" -->
        </g>
        <g opacity="1.0">
          <!-- new elements this panel, stroke-width="2" -->
        </g>
      </svg>
    </div>
    <div class="wb-caption">Brief description of what this panel shows</div>
  </div>

</div>
</body>
</html>

---

# CONTENT LOCK

Every label, number, rule, and value on the board comes directly
from the script. No invented content.
No prose sentences appear inside any SVG — only compressed facts,
labels, values, and visual forms.
The wb-caption is a brief description in your own words of what
the panel is showing — not a quote from the script.

---

# SELF-CHECK — VERIFY BEFORE OUTPUTTING

1.  Output is a complete HTML document starting with <!doctype html>.
2.  Output ends with </html> — if you are near your output limit,
    stop adding new panels rather than truncating mid-panel.
3.  Panel count reflects the actual visual moments in the script —
    not forced to match any fixed number.
4.  Panel label reads "Board — Step N of TOTAL" with correct numbers.
    TOTAL matches the actual number of panels produced.
5.  Each SVG contains all prior zones (as minimal placeholders) plus
    the new zone at full detail.
6.  Prior zones: wrapped in <g opacity="0.72">, stroke-width="1",
    reduced to one label per box, one label per arrow.
7.  New zones: wrapped in <g opacity="1.0">, stroke-width="2",
    with full detail — all properties, all labels.
8.  Final panel: ALL elements at opacity="1.0" stroke-width="2",
    full detail on every element.
9.  Every arrow is labelled. New-zone nodes have key properties inside.
10. All values and numbers from the script appear somewhere on the board.
11. No prose sentences inside any SVG.
12. Insight line at y=462 in the final panel only.
13. viewBox="0 0 680 480" on every SVG.
14. No JavaScript anywhere in the output.
15. Google Fonts CDN is the only external resource.

---

# OUTPUT RULE

Return ONLY raw HTML.
No markdown. No code fences. No preamble. No explanation.
Must begin with <!doctype html> and be a complete valid document.