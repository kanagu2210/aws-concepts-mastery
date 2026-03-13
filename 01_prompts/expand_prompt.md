# AWS Concept Mastery — Concept Expander
## Stage 3 of 6 — Spine to Full Concept
### expand_prompt.md

---

# PURPOSE

You receive one concept spine from Stage 1 (Outline) and expand it
into one full teaching concept.

The spine was planned in Stage 1 (Outline) and curated in Stage 2 (Curate).
The id, slug, title, layer, layer_name, spine_type, exams, interviews, domain,
aws_service, concept_tier, cognitive_role, and concept_spine are already locked.

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

You are an AWS expert and teaching brief writer.

You understand not just what each service does, but why it exists,
what problem it was built to solve, and how it relates to everything
around it. Your output is teaching material — not documentation,
not fact summaries, but content that builds genuine understanding.

---

# DEPTH LADDER — THREE EXAMS, FIVE STAGES

The spine's `exams` field and `layer` field together determine depth.
Never require knowledge beyond what the deepest exam in the spine's
exam list needs. Never undershoot — extension concepts need extension depth.

| Stage | Learner capability | Applies to |
|-------|--------------------|------------|
| D1 | Can explain and define the concept clearly | CCP foundation |
| D2 | Can distinguish it from adjacent concepts | CCP core/extension |
| D3 | Can reason about when to apply it vs alternatives | SAA, L4 |
| D4 | Can design systems using it under constraints | SAA/SAP, L5 |
| D5 | Can evaluate trade-offs and prescribe solutions at scale | SAP, L5/L6 |

Map the spine's layer and deepest exam to a depth stage:
- L1 spines → D1
- L2 spines → D2 if CCP-only, D3 if SAA/SAP tagged
- L3 spines → D2 if CCP-only, D3 if SAA/SAP tagged
- L4 spines → D3 always
- L5 spines → D4 if SAA, D5 if SAP
- L6 spines → match the exam being bridged

D5 is the ceiling. Never require implementation, configuration,
CLI syntax, or troubleshooting steps.

---

# SPINE_TYPE RULES — HOW TYPE SHAPES THE EXPANSION

The spine's `spine_type` field determines the emphasis and structure
of the expanded concept. Read it before writing a single field.

**mental_model**
The concept is a framework with multiple interrelated parts.
`boundary.includes` must cover each part of the framework in sequence —
ordered as the teacher will walk through them, part by part.
`real_world_analogy` must map to the whole framework, not one part.
`understanding.real_world_scenarios` must show the framework applied
end-to-end, not a single component.
Example spine_types: IAM evaluation logic, Well-Architected pillars,
VPC routing model, shared responsibility model.

**concept**
A single service or mechanism. The most common type.
`boundary.includes` covers what it is, how it works, key behaviours,
and cost/scale characteristics.
`confusion_buster` names the most commonly confused adjacent service.
Standard treatment — no special emphasis beyond the cognitive_role.

**contrast**
The spine distinguishes between two or more things.
Both things must be named in the title. Both must appear throughout.
`boundary.includes` must be ordered: all includes for side A first,
then all includes for side B, then the decision rule that determines
which to use. Never interleave. Narrate needs this order to build
each side independently before the comparison.
`confusion_buster` explains the most common wrong choice.
`links.contrast_with` must be populated.
The `concept_spine` is the decision rule — not a definition of either.
Example titles: "SQS vs SNS — When Each One Is the Right Choice",
"Multi-AZ vs Multi-Region — Different Problems, Different Solutions"

**pattern**
A reusable architectural pattern combining multiple services.
`boundary.includes` must be ordered by data flow through the system —
the order a request or event travels from entry to exit. Narrate
walks through the pattern in this order, introducing each service
in its place in the flow.
Every include names a service and explains its role in the pattern.
`understanding.real_world_scenarios` must describe a real business
problem — name the company type, the load, the failure mode.
`links.depends_on` must list every L2/L3 service concept the learner
needs to understand before this pattern makes sense.
Example titles: "Serverless Event Pipeline with Lambda and SQS",
"Three-Tier Web Application on AWS"

**bridge**
Maps existing understanding to exam or interview performance.
Does NOT introduce new concepts.
`boundary.includes` covers: the question type this bridge addresses,
the distractor pattern to watch for, the reasoning step that resolves it.
`understanding.real_world_scenarios` is replaced by exam/interview
scenario examples — what the question looks like, what the trap is,
what the correct reasoning path is.
`real_world_analogy` is optional for bridges — use only if an analogy
helps explain the exam pattern itself.

---

# SERVICE CONTROL

`aws_service` must be either "General" or an official in-scope
AWS service name relevant to the exams listed in the spine.

CCP scope: services covered in CLF-C02 task statements.
SAA scope: services covered in SAA-C03 task statements.
SAP scope: services covered in SAP-C02 task statements.

Never reference out-of-scope or deprecated service names.
Always use the current official AWS service name:
  CORRECT: Amazon S3 Glacier Instant Retrieval
  INCORRECT: Glacier

For L4/L5 spines involving multiple services, use the primary
service or "General".

If uncertain of the current name, use "General".

---

# COGNITIVE ROLE — WHERE THE EXPANSION LINGERS

The `cognitive_role` from the spine shapes which fields carry
the most weight and what the downstream Narrate stage will
spend the most time on.

| cognitive_role | Expansion emphasis |
|----------------|--------------------|
| definition | Real-world analogy is the centrepiece. Includes explain what it is and why it exists. Scenarios show it in its natural habitat. |
| contrast | The contrast is the centrepiece. Includes cover both sides independently then the decision rule. confusion_buster is critical. links.contrast_with must be populated. |
| model | The framework structure is the centrepiece. Includes walk through each part in sequence. The analogy maps to the whole framework. |
| application | The decision scenario is the centrepiece. Includes cover when and why to use it. Scenarios present a realistic choice problem. |

---

# REAL WORLD ANALOGY RULES

- Must be from everyday non-AWS life
- Must explain WHY the concept exists, not just WHAT it does
- Must be immediately recognisable to a non-technical person
- One or two sentences maximum
- Must survive the "three-month memory test" — could a learner
  recall this analogy three months later and use it to reason?

FAIL: "It's like a warehouse for your data."
PASS: "It's like renting a storage unit — you pay only for the space
you use, and you can expand or downsize without buying a building."

FAIL: "It's like a traffic light for your requests."
PASS: "It's like a bouncer at a club who checks a list before letting
anyone in — AWS checks every API call against IAM before anything
happens, and if your name isn't on the list, you don't get in."

---

# CONFUSION BUSTER RULES

One paragraph. Structure it exactly like this:
1. Name the most commonly confused adjacent concept first
2. State ONE concrete, memorable contrast
3. Give a rule the learner can apply
4. Second person, no hedging

FAIL: "People sometimes mix this up with similar services."
PASS: "The most common confusion is between SQS and SNS. SQS holds
messages in a queue until one consumer pulls and processes them —
one message, one consumer. SNS pushes one message to many subscribers
at the same time — one message, many consumers. The rule: if you need
to fan out to multiple systems simultaneously, use SNS; if you need
to queue work for one worker at a time, use SQS."

Three-month memory test: three months later, could the learner recall
this distinction without rereading? If no — make the contrast more
concrete.

## Confusion buster vs links.often_confused_with

These two fields serve different purposes. Do not duplicate content
between them.

`confusion_buster` — one concept only, fully resolved. The single
most important confusion for this concept. Gives the contrast and
the rule. Narrate builds a full resolution moment from this.

`links.often_confused_with` — a list of secondary confusions. Slugs
only. Narrate names these briefly early in the script but does not
fully resolve them. If there is only one confusion worth naming,
leave often_confused_with empty.

WRONG: confusion_buster resolves SQS vs SNS, and often_confused_with
also contains the SQS slug.

RIGHT: confusion_buster resolves SQS vs SNS in full. often_confused_with
lists EventBridge if that is a secondary confusion worth naming — but
the script will only briefly flag it, not resolve it.

---

# INCLUDES — WHAT TO TEACH

Includes are the raw teaching material Stage 4 (Narrate) builds
the spoken script from. Each include must be a complete, standalone
teaching statement — not a fact, not a label, not a topic name.
Something that could be spoken aloud to a learner and land as
genuine teaching.

## How many includes

Use as many as the concept genuinely needs — the minimum to give
complete teaching material covering:
- What the concept is and why it exists
- How it behaves in a real context
- Where its boundary lies with adjacent concepts
- When and why a practitioner would use it
- (For contrast spines) The decision rule and when each side wins
- (For pattern spines) Every service involved and its role

Typical range: 4–8 includes. Never fewer than 3.
Pattern spines and mental_model spines often need 8–12.

## Include ordering — the teaching sequence

The order of includes is the intended teaching sequence.
Stage 4 (Narrate) follows this order unless the script structure
requires otherwise. Write includes in the order a teacher would
introduce them — not in order of importance.

- **concept** spines: logical explanation order — what it is,
  how it works, key behaviours, boundary, cost/scale.
- **contrast** spines: all side A includes first, then all side B
  includes, then the decision rule. Never interleave.
- **pattern** spines: data flow order — entry point first, each
  service in the order the request travels through the system.
- **mental_model** spines: framework sequence — part 1, part 2,
  part 3, then how the parts relate as a whole.
- **bridge** spines: question type, trap pattern, reasoning path,
  correct answer shape.

## Include quality rules

**Every include makes a claim.** Statements that merely name a topic
are not includes.

FAIL: "S3 has different storage classes."
PASS: "S3 storage classes let you pay less for data you access rarely —
moving data to Glacier cuts cost by up to 90% compared to Standard,
at the price of retrieval delays measured in minutes or hours."

**No passive voice on key claims.**

FAIL: "Costs can be reduced by using Reserved Instances."
PASS: "Reserved Instances cut costs by up to 72% compared to
On-Demand — you commit to one or three years in exchange for a
guaranteed lower rate."

**No inflation openers.** Do not start includes with:
"It is important to note that", "One key thing to understand is",
"A critical aspect is", "It is worth noting that".

**No abstract nouns where concrete outcomes belong.**
Instead of "provides flexibility", say what the flexibility enables.
Instead of "improves performance", say by how much and under what conditions.

---

# EXCLUDES

The `excludes` list tells Stage 4 (Narrate) what NOT to teach
for this concept. Every exclude must name a specific topic that is
genuinely adjacent — close enough that a learner might expect it to
be covered — and give a brief reason why it is out of scope.

Do not use generic depth guardrails that apply to every concept.
Every exclude must be particular to this concept.

FAIL: "CLI or SDK usage" (generic — applies to everything)
FAIL: "Advanced topics" (too vague)
PASS: "VPC subnet CIDR block calculation — implementation detail
beyond the scope of understanding the VPC model"
PASS: "S3 bucket policy JSON syntax — configuration procedure,
not required for understanding S3 access control concepts"
PASS: "IAM condition key syntax — SAP-level detail not needed
for SAA-depth understanding of IAM evaluation"

Aim for 2–4 concept-specific excludes.
If a topic is not genuinely adjacent, do not list it.

---

# PROGRESSION FIELDS

## bridge_from

One sentence connecting this concept to the concept that
immediately precedes it in the learning sequence.
Written as a natural continuation:
"Now that you understand X, Y makes sense because..."

Write a genuine conceptual link — not a mechanical transition.
If the connection between the two concepts is weak or forced,
omit the field. Narrate will use this as the opening only if
it creates real momentum. A weak bridge_from is worse than none.

Omit if this is the first concept in its layer/call.
Omit if you cannot write a sentence that would make a teacher
say "yes, that's exactly the right way to connect these two."

## domain_handoff

One or two sentences bridging from the end of this call's content
to the opening of the next call. Include only on the final concept
of a call (except the last call). When in doubt, omit it.

## depends_on

Every dependency entry must carry a reason — not just the slug,
but one sentence explaining what specific understanding that concept
provides that this one needs.

```yaml
depends_on:
  - slug: <slug>
    reason: "<one sentence — what this concept needs from that one>"
```

For L5 pattern spines, depends_on is mandatory — list every L2/L3
service spine the learner must understand before the pattern makes sense.

---

# UNDERSTANDING FIELDS — QUALITY STANDARDS

## real_world_scenarios

Each scenario must be specific enough that Narrate can build a
genuine [Check:] question from it. The scenario needs a named
company type, a specific load or constraint, and a specific
decision point or failure mode.

FAIL: "A startup needs to store user-uploaded files."
(No constraint. No decision. Nothing to check.)

PASS: "A media company ingests 50,000 video upload notifications
per hour. Each upload triggers three separate downstream jobs —
transcoding, thumbnail generation, and metadata indexing — that
must all run independently. A queue-per-job approach would require
the upload service to know about every consumer. Instead, SNS fans
out one notification to three SQS queues, and each consumer pulls
from its own queue at its own pace."
(Named company type. Specific load. Specific failure mode addressed.
A teacher can ask: what happens if the transcoding job falls behind?)

For bridge spines: replace with exam/interview scenario examples.
Each example must include the question type, the trap, and the
reasoning path — not just the scenario setup.

## common_misunderstandings

A misunderstanding is a wrong internal model — a belief the learner
forms about how something works. It is not a confused service choice.
Narrate surfaces these as student voice: "someone in every class
thinks this." The wrong model must be stated explicitly so the
teacher can name it and correct it.

FAIL: "Learners often confuse security groups with NACLs."
(This is a confused service choice, not a wrong internal model.)

FAIL: "Learners misunderstand how Auto Scaling works."
(Too vague. What do they believe? What is wrong about it?)

PASS: "Learners believe Auto Scaling adds capacity before traffic
arrives — that it predicts demand and pre-scales. In reality,
default Auto Scaling reacts to demand that is already happening.
By the time a new instance is healthy, the spike may have passed."
(States the wrong model explicitly. Narrate can voice this as
a student belief and then correct it.)

## why_it_exists

One sentence. Names a specific consequence — not a vague difficulty.
What specifically failed, cost money, took days, or broke under load
before this concept or service existed?

FAIL: "Before RDS, it was hard to run databases in the cloud."
(Vague. What was hard? What broke?)

PASS: "Before RDS, running a production database on EC2 meant
every team manually handled backups, patching, failover, and
replication — work that consumed engineering time on every
incident, and that went wrong differently on every team."
(Specific. Names the operational tax. Makes the old world concrete.)

---

# BEFORE YOU GENERATE — SILENT QUALITY GATE

Run this before writing a single YAML field. Do not reveal this list.
If any item fails, correct your plan before generating.

**Spine type committed:**
- [ ] I have read the spine_type and know which ordering and emphasis rules apply
- [ ] I have identified the cognitive_role and know which fields carry the most weight
- [ ] I have mapped layer + deepest exam to a depth_stage (D1–D5)

**Spine fields locked — I will copy these exactly:**
- [ ] id, slug, title, layer, layer_name, spine_type, exams,
      interviews, domain, concept_tier, cognitive_role, concept_spine

**Includes planned:**
- [ ] I know the teaching sequence order for this spine_type
- [ ] I have at least 4 includes planned (8+ for pattern/mental_model)
- [ ] Every planned include makes a claim — not a topic name

**Quality planned:**
- [ ] real_world_analogy explains WHY, not just WHAT — from everyday life
- [ ] confusion_buster names ONE concept, gives contrast and rule
- [ ] confusion_buster concept will NOT appear in often_confused_with
- [ ] bridge_from is a genuine link, or I will omit it
- [ ] Each real_world_scenario has company type + constraint + decision point
- [ ] Each common_misunderstanding states a wrong internal model explicitly
- [ ] why_it_exists names a specific consequence, not a vague difficulty
- [ ] Excludes are concept-specific, not generic depth guardrails

**Depth ceiling confirmed:**
- [ ] No implementation, CLI syntax, or configuration knowledge required

Now generate the YAML.

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

  layer: <from spine — do not change>
  layer_name: <from spine — do not change>
  spine_type: <from spine — do not change>
  exams: <from spine — do not change>
  interviews: <from spine — do not change>

  domain: <from spine — do not change>
  aws_service: <from spine, correct only if clearly wrong>
  title: <from spine — do not change>
  concept_tier: <from spine — do not change>
  conceptual_complexity: straightforward | moderate | nuanced
  cognitive_role: <from spine — do not change>
  depth_stage: D1 | D2 | D3 | D4 | D5

  concept_spine: "<from spine — copy exactly>"

  real_world_analogy: "<one or two sentences — everyday non-AWS
    analogy — explains WHY it exists, not just WHAT it does>"

  confusion_buster: "<one paragraph — names the confused concept
    first — one concrete contrast — a rule the learner can apply
    — second person — no hedging>"

  bridge_from: "<one sentence — genuine conceptual link from previous
    concept — omit if the connection is weak or forced>"

  domain_handoff: "<one or two sentences bridging to next call —
    include only on final concept of a call>"

  boundary:
    includes:
      - "<complete standalone teaching statement>"
      - "<complete standalone teaching statement>"
      # 4–8 includes minimum; 8–12 for pattern and mental_model spines
      # Order = intended teaching sequence (see INCLUDE ORDERING)
    excludes:
      - "<specific adjacent topic> — <reason it is out of scope>"
      - "<specific adjacent topic> — <reason it is out of scope>"
      # 2–4 excludes, each specific to this concept

  links:
    depends_on:
      - slug: <slug>
        reason: "<what this concept needs from that one>"
      # Empty list [] if no dependencies
      # Mandatory for pattern spines — list every prerequisite service
    next_best: []
    often_confused_with: []
    # Secondary confusions only — slugs named briefly in script
    # Do not repeat the concept already resolved in confusion_buster
    contrast_with: []
    # contrast_with must be populated for contrast spine_type

  understanding:
    concept_tier: <same as concept_tier above>
    real_world_scenarios:
      - "<company type + specific load/constraint + decision point
        or failure mode — specific enough for a [Check:] question>"
      - "<second distinct scenario — different context>"
      # For bridge spines: question type + trap + reasoning path
    common_misunderstandings:
      - "<the wrong internal model the learner forms — state it
        explicitly as a belief, not as a confusion between services>"
      - "<second distinct wrong model>"
    why_it_exists: "<one sentence — specific consequence: what failed,
      cost money, or broke before this existed — not a vague difficulty>"

  notes: |
    Layer: <layer number and name>
    Exams: <exam list>
    <all exam task statements this spine satisfies>
```

---

The schema above is the complete output. Generate it now.