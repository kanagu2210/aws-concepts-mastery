# {{PROJECT_NAME}} — Concept Expander
## Stage 3 of 6 — Spine to Full Concept
### expand_prompt.md

---

# PURPOSE

You receive one concept spine from Stage 1 (Outline) and expand it
into one full teaching concept.

The spine was planned in Stage 1 (Outline) and curated in Stage 2 (Curate).
The id, slug, title, layer, phase_name, concept_type, exams, interviews, domain,
{{ENTITY_FIELD}}, concept_tier, cognitive_role, and core_idea are already locked.

If the spine contains an `approved: false` field — stop. Do not expand it.
This spine has been held back during curation. Return nothing.

Your job is to fill in all remaining fields with rich, accurate
teaching content that Stage 4 (Narrate) will turn into a spoken
teaching script.

Do not change any spine field.
Do not include the approved field in your output.
Do not invent a different concept.
Do not add a meta block.
Do not output anything except the single concept YAML.

---

# YOUR ROLE

{{EXPERT_ROLE}}

Your output is teaching material — not documentation,
not fact summaries, but content that builds genuine understanding.

---

# DEPTH LADDER

The spine's `milestones` field and `layer` field together determine depth.
Never require knowledge beyond what the deepest exam in the spine's
exam list needs. Never undershoot.

Exam depth mapping:
{{MILESTONE_DEPTH_MAP}}

| Stage | Learner capability | Applies to |
|-------|--------------------|------------|
| D1 | Can explain and define the concept clearly | Foundation level |
| D2 | Can distinguish it from adjacent concepts | Core level |
| D3 | Can reason about when to apply it vs alternatives | Intermediate exams |
| D4 | Can design systems using it under constraints | Advanced exams |
| D5 | Can evaluate trade-offs and prescribe solutions at scale | Expert level |

D5 is the ceiling. Never require implementation, configuration,
CLI syntax, or troubleshooting steps.

---

# SPINE_TYPE RULES — HOW TYPE SHAPES THE EXPANSION

The spine's `concept_type` field determines the emphasis and structure
of the expanded concept. Read it before writing a single field.

**mental_model**
The concept is a framework with multiple interrelated parts.
`boundary.includes` must cover each part of the framework in sequence.
`real_world_analogy` must map to the whole framework, not one part.

**concept**
A single service or mechanism. The most common type.
`boundary.includes` covers what it is, how it works, key behaviours,
and cost/scale characteristics.

**contrast**
The spine distinguishes between two or more things.
Both things must be named in the title.
`boundary.includes` must be ordered: all includes for side A first,
then all includes for side B, then the decision rule.

**pattern**
A reusable architectural pattern combining multiple services.
`boundary.includes` must be ordered by data flow through the system.

**bridge**
Maps existing understanding to exam or interview performance.
Does NOT introduce new concepts.

---

# COGNITIVE ROLE — WHERE THE EXPANSION LINGERS

| cognitive_role | Expansion emphasis |
|----------------|--------------------|
| definition | Real-world analogy is the centrepiece. |
| contrast | The contrast is the centrepiece. |
| model | The framework structure is the centrepiece. |
| application | The decision scenario is the centrepiece. |

---

# REAL WORLD ANALOGY RULES

- Must be from everyday non-technical life
- Must explain WHY the concept exists, not just WHAT it does
- Must be immediately recognisable to a non-technical person
- One or two sentences maximum
- Must survive the "three-month memory test"

---

# CONFUSION BUSTER RULES

One paragraph. Structure it exactly like this:
1. Name the most commonly confused adjacent concept first
2. State ONE concrete, memorable contrast
3. Give a rule the learner can apply
4. Second person, no hedging

---

# INCLUDES — WHAT TO TEACH

Includes are the raw teaching material Stage 4 (Narrate) builds
the spoken script from. Each include must be a complete, standalone
teaching statement.

Typical range: 4–8 includes. Never fewer than 3.
Pattern spines and mental_model spines often need 8–12.

Every include makes a claim. Statements that merely name a topic
are not includes.

---

# EXCLUDES

The `excludes` list tells Stage 4 (Narrate) what NOT to teach.
Every exclude must name a specific topic that is genuinely adjacent
and give a brief reason why it is out of scope.

Aim for 2–4 concept-specific excludes.

---

# UNDERSTANDING FIELDS — QUALITY STANDARDS

## real_world_scenarios
Each scenario must be specific enough that Narrate can build a
genuine [Check:] question from it. Needs a named company type,
a specific load or constraint, and a specific decision point.

## common_misunderstandings
A misunderstanding is a wrong internal model — a belief the learner
forms about how something works. State the wrong model explicitly.

## why_it_exists
One sentence. Names a specific consequence — not a vague difficulty.

---

# REQUIRED YAML SCHEMA (STRICT)

Return ONLY a single concept as a YAML list item.
No meta block. No fences. No commentary.
Start directly with `- id:`.

Do not add, remove, or rename any field.
Copy ALL spine fields exactly as received — do not change them.

```yaml
- id: <from spine — do not change>
  global_sequence: <same as id>
  slug: <from spine — do not change>

  phase: <from spine — do not change>
  phase_name: <from spine — do not change>
  concept_type: <from spine — do not change>
  milestones: <from spine — do not change>
  applied: <from spine — do not change>

  area: <from spine — do not change>
  {{ENTITY_FIELD}}: <from spine, correct only if clearly wrong>
  title: <from spine — do not change>
  concept_tier: <from spine — do not change>
  conceptual_complexity: straightforward | moderate | nuanced
  cognitive_role: <from spine — do not change>
  depth_stage: D1 | D2 | D3 | D4 | D5

  core_idea: "<from spine — copy exactly>"

  real_world_analogy: "<one or two sentences — everyday non-technical
    analogy — explains WHY it exists, not just WHAT it does>"

  confusion_buster: "<one paragraph — names the confused concept
    first — one concrete contrast — a rule the learner can apply>"

  bridge_from: "<one sentence — genuine conceptual link from previous
    concept — omit if the connection is weak or forced>"

  domain_handoff: "<one or two sentences bridging to next call —
    include only on final concept of a call>"

  boundary:
    includes:
      - "<complete standalone teaching statement>"
      - "<complete standalone teaching statement>"
    excludes:
      - "<specific adjacent topic> — <reason it is out of scope>"

  links:
    depends_on:
      - slug: <slug>
        reason: "<what this concept needs from that one>"
    next_best: []
    often_confused_with: []
    contrast_with: []

  understanding:
    concept_tier: <same as concept_tier above>
    real_world_scenarios:
      - "<company type + specific load/constraint + decision point>"
    common_misunderstandings:
      - "<the wrong internal model the learner forms>"
    why_it_exists: "<one sentence — specific consequence>"

  notes: |
    Layer: <layer number and name>
    Exams: <exam list>
    <all exam task statements this spine satisfies>
```

---

The schema above is the complete output. Generate it now.
