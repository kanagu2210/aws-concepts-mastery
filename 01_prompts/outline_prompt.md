# {{PROJECT_NAME}} — Outline Generator
## Stage 1 of 6 — Spine Planning
### outline_prompt.md

---

# PURPOSE

Generate concept spines for a mastery curriculum on {{SUBJECT}}.

A spine is a minimal planning record — not a full concept. It contains
only the fields needed to plan and sequence the full concept set.
Stage 3 (expand) will turn each spine into a full teaching concept.
Stage 2 (curate) validates the spine list before any expansion begins.
Nothing gets fully generated until the spine list is curated and approved.

This is NOT an exam cram tool. It is organised by how {{SUBJECT_SHORT}}
actually works. Exam domains are metadata — not the organising principle.

---

# YOUR ROLE

{{EXPERT_ROLE}}

Your job is to produce concept spines that build genuine understanding —
deep enough that exam questions and interview scenarios become easy
as a byproduct. Organised by layer, not by exam domain.

---

# THE LAYER ARCHITECTURE

The curriculum is organised into layers. Each layer has a distinct
cognitive purpose. Read these carefully — they determine what you
generate and how deep you go.

{{PHASE_DESCRIPTIONS}}

---

# COMPLETE SPINE SCHEMA

Every spine must have exactly these fields — no more, no less:

```yaml
- id: 47
  slug: example-spine-slug
  title: How Something Actually Works

  phase: 2
  phase_name: <must match the layer name from the layer architecture above>

  concept_type: mental_model
  # Allowed values: {{ALLOWED_TYPES}}

  milestones: [{{ALLOWED_MILESTONES}}]
  # Which exams/certifications this spine covers. Every spine must have at least one.

  applied: true
  # true if this concept is commonly asked in interviews
  # false otherwise

  area: <one of the allowed domains below>
  # Allowed values:
{{ALLOWED_AREAS}}

  {{ENTITY_FIELD}}: General
  # "General" or an official in-scope service/component name

  concept_tier: foundation
  # Allowed values: {{ALLOWED_TIERS}}

  cognitive_role: model
  # Allowed values: {{ALLOWED_ROLES}}
  # "map" is banned.

  core_idea: "One sentence. One idea. Written as a confident
    human teaching statement."
  # No "and" joining two ideas.

  notes: "Exam task references this spine satisfies"

  # approved is NOT set by the generator. It is set manually during curation.
  # Do not include this field in generated output.
```

---

# GENERATION PLAN

You will be asked to generate spines for ONE call at a time.
Each call specifies: CALL_NAME, START_ID, and TARGET.

Hard limit: exactly the TARGET number of spines per call.
Never exceed the target. Never pad to inflate.

---

# EXAM COVERAGE MAP (MANDATORY)

Every task statement below must be satisfied by at least one spine.
Use this as your checklist. Do not skip any item.
Tag every spine with the task statements it satisfies in the `notes` field.

{{COVERAGE_MAP}}

---

# LAYER RULES — WHAT BELONGS WHERE

These rules are hard. Do not mix purposes across layers.

Each layer in the architecture above specifies which concept_types are
allowed or required. Follow those constraints exactly.

---

# ANTI-DUPLICATION RULES

The spine list grows call by call. Each call receives the already-
generated slug list as context. Check every slug before generating.

## Rule 1 — No same concept at different layers
Layer determines angle. If the angle is the same, it's a duplicate.

## Rule 2 — No same service, same angle
Two spines covering the same service from the same teaching angle
must be merged.

## Rule 3 — Shared concepts are tagged, not duplicated
If a concept appears in multiple exams, one spine covers it with
multiple exam tags. Never generate two spines for the same concept
targeting different exams.

## Rule 4 — Slug collision check
Before outputting, scan every slug in the ALREADY GENERATED list.
Any slug collision must be resolved by renaming with a layer prefix.

---

# SPINE_TYPE RULES

concept_type determines how Stage 3 (expand) treats the concept
and how Stage 4 (narrate) scripts it.

**mental_model** — A framework with multiple parts.
Expands into a structured explanation of each part and how they relate.

**concept** — A single service or idea. The most common type.
Expands into definition, mechanics, scenarios.

**contrast** — Distinguishes between two or more things.
Must name both things in the title.
Expands into a side-by-side comparison with decision rules.

**pattern** — A reusable architectural pattern.
Expands into a scenario walkthrough naming the services involved.

**bridge** — Maps understanding to exam/interview format.
Expands into question types, distractor patterns, scenario frameworks.

---

# CONCEPT_SPINE RULES

The core_idea is one sentence. One idea.

Written as a confident human teaching statement — not a definition
label, not a fact, not a feature list.

No "and" joining two ideas.

The test: could a teacher speak this sentence to a class and have
it land as a genuine insight? If yes — good. If it sounds like
a documentation summary — rewrite it.

---

# CONCEPT TIER RULES

**foundation** — The concept everything else in this layer builds on.
Max 15% of any call. Used sparingly.

**core** — The main body of the call. ~60% of spines.

**extension** — Nuance, specificity, important distinctions.
Minimum 20% of any call. Never skip extension spines.

---

# SEQUENCING RULES

Within each call, order spines as a learning arc:
1. Foundation concepts first, in dependency order
2. Core concepts next, each following what it builds on
3. Extension concepts last

IDs are globally sequential across all calls.
Never reset between calls. Each call receives START_ID.

---

# SLUG RULES

Globally unique kebab-case.
Use layer + domain-context prefixes where collision risk exists.

Do not use generic slugs.

---

# SERVICE CONTROL

{{ENTITY_FIELD}} must be either "General" or an official in-scope
service/component name relevant to the exams listed in the spine.

Never use deprecated names. If uncertain, use "General".

---

# OUTPUT FORMAT

Return ONLY valid YAML. No markdown fences. No commentary.
No explanation before or after the YAML.

Start directly with `- id:` for the first spine.

After outputting all spines for the call, append a single summary line:
# Call: <call name> | Count: <n> | IDs: <start>–<end>

---

# PLANNING PHASE (SILENT — DO NOT OUTPUT)

Before generating any YAML, complete this silently:

## Step 1 — Scope check
Read the call name carefully. What services, mechanisms, or patterns
are in scope?

## Step 2 — Layer integrity check
For every planned spine, ask: does this belong in this layer?

## Step 3 — Exam coverage check
Verify every relevant task from the Exam Coverage Map is covered.

## Step 4 — Dedup check
Check every planned spine against the ALREADY GENERATED SLUGS list.

## Step 5 — concept_type check
Verify spine types match the layer rules.

## Step 6 — Count check
Verify your planned count exactly matches the call TARGET.

## Step 7 — Sequence check
Verify spines run foundation → core → extension within the call.

Only after completing all seven steps, output the YAML.

---

# ALREADY GENERATED SLUGS

The following slugs already exist. Do not duplicate them.
{existing_slugs}

---

# THIS CALL

CALL_NAME: {domain_call}
START_ID:  {start_id}
TARGET:    {target_count}
DOMAIN:    {domain_value}

Generate exactly {target_count} spines starting at id {start_id}.
