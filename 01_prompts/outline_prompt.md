# AWS Concept Mastery — Outline Generator
## Stage 1 of 6 — Spine Planning
### outline_prompt.md

---

# PURPOSE

Generate concept spines for a 1000-spine AWS mastery curriculum
covering CCP (CLF-C02), SAA (SAA-C03), and SAP (SAP-C02) exams
plus interview preparation.

A spine is a minimal planning record — not a full concept. It contains
only the fields needed to plan and sequence the full concept set.
Stage 3 (expand) will turn each spine into a full teaching concept.
Stage 2 (curate) validates the spine list before any expansion begins.
Nothing gets fully generated until the spine list is curated and approved.

This is NOT an exam cram tool. It is organised by how AWS actually
works. Exam domains are metadata — not the organising principle.

---

# YOUR ROLE

You are an AWS expert and curriculum architect.

Your job is to produce concept spines that build genuine understanding —
deep enough that exam questions and interview scenarios become easy
as a byproduct. Organised by layer, not by exam domain.

---

# THE 6-LAYER ARCHITECTURE

The curriculum is organised into 6 layers. Each layer has a distinct
cognitive purpose. Read these carefully — they determine what you
generate and how deep you go.

```
Layer 1 — Foundations (50 total spines)
    The 8 big ideas that everything else hangs on.
    Why cloud exists. AWS design philosophy.
    The mental models a learner needs before anything else.
    A learner who masters L1 can reason about any AWS question
    they have never seen before.
    Exam coverage: CCP Tasks 1.1, 1.2, 1.3

Layer 2 — Core Mechanisms (100 total spines)
    How AWS actually works conceptually — not implementation
    details but the conceptual mechanisms.
    IAM evaluation logic. VPC routing model. S3 consistency.
    EC2 scheduling. Lambda execution model. RDS replication.
    A learner who masters L2 can predict how a service will
    behave in a scenario they have not seen.
    Exam coverage: CCP 2.1, 2.3 | SAA 1.1, 1.2 | SAP security tasks

Layer 3 — Service Mastery (350 total spines)
    Every significant in-scope service across CCP + SAA + SAP.
    What it is. Why it exists. What problem it solves.
    Where its boundaries are. What it costs to use it.
    Organised by service category — NOT by exam domain.
    A learner who masters L3 knows every tool in the AWS toolbox.
    Exam coverage: CCP 3.x | SAA service-level tasks | SAP service depth

Layer 4 — Decision Patterns (250 total spines)
    When to use X vs Y. Every high-stakes choice point.
    SQS vs SNS vs EventBridge. RDS vs DynamoDB vs ElastiCache.
    Reserved vs Spot. Multi-AZ vs Multi-Region.
    Organised by decision type: resilience, cost, security,
    data, integration decisions.
    A learner who masters L4 can select the right service for
    any requirement without hesitation.
    Exam coverage: SAA Tasks 1-4 heavily | SAP trade-off questions

Layer 5 — Architectural Patterns (180 total spines)
    How services compose into real systems.
    Three-tier web app. Event-driven pipeline. Serverless.
    Hybrid network. Multi-account governance. Data lake.
    Disaster recovery. Migration patterns (6Rs applied).
    A learner who masters L5 can design a complete AWS
    architecture from requirements.
    Exam coverage: SAP Tasks 1-4 heavily | interview design questions

Layer 6 — Exam and Interview Bridges (70 total spines)
    Thin layer mapping mastery to performance.
    NOT new concepts. Maps L1-L5 understanding to how it
    appears in exam questions and interviews.
    Common traps. Distractor patterns. Scenario frameworks.
    Read last — this is where understanding is applied.
```

---

# COMPLETE SPINE SCHEMA

Every spine must have exactly these fields — no more, no less:

```yaml
- id: 47
  slug: iam-permission-evaluation-model
  title: How IAM Actually Decides to Allow or Deny

  layer: 2
  layer_name: Core Mechanisms

  spine_type: mental_model
  # Allowed values:
  #   mental_model  — a framework that organises multiple concepts
  #   concept       — a single service or concept (most spines)
  #   contrast      — distinguishes between two or more things
  #   pattern       — a reusable architectural pattern (L5 mainly)
  #   bridge        — maps understanding to exam/interview format (L6 only)

  exams: [CCP, SAA, SAP]
  # Which exams this spine covers. Every spine must have at least one.
  # Allowed values: CCP, SAA, SAP (list, any combination)

  interviews: true
  # true if this concept is commonly asked in AWS interviews
  # false otherwise

  domain: Security and Compliance
  # Official exam domain — used for coverage verification only.
  # Allowed values:
  #   Cloud Concepts
  #   Security and Compliance
  #   Cloud Technology and Services
  #   Billing, Pricing, and Support
  #   Cross-Domain   (for L4/L5/L6 spines that span multiple domains)

  aws_service: AWS IAM
  # "General" or official in-scope AWS service name

  concept_tier: foundation
  # Allowed values: foundation | core | extension

  cognitive_role: model
  # Allowed values: definition | contrast | model | application
  # "map" is banned.

  concept_spine: "Every AWS API call passes through IAM evaluation
    in a fixed sequence — explicit deny always wins, then an explicit
    allow must exist — so you can always reason about access by
    following the evaluation logic rather than memorising policies."
  # One sentence. One idea. No "and" joining two ideas.
  # Written as a confident human teaching statement.

  notes: "CCP Task 2.3 | SAA Task 1.1 | SAP Task 2.1"
  # All exam task statements this spine satisfies.

  # approved is NOT set by Claude. It is set manually during curation.
  # Do not include this field in generated output.
  # After Stage 2 (Curate), a human may add:
  #   approved: false   — to hold this spine back from the pipeline
  # Absent or approved: true → spine runs normally.
```

---

# GENERATION PLAN — 51 CALLS, 20 SPINES EACH

You will be asked to generate spines for ONE call at a time.
Each call specifies: CALL_NAME, START_ID, and TARGET.

Hard limit: exactly 20 spines per call (10 for half-calls).
Never exceed the target. Never pad to inflate.

## Call sequence and targets

```
# Layer 1: Foundations — 3 calls, 50 spines
Layer 1 Part 1: The 8 Big Ideas of Cloud and AWS                    → 20
Layer 1 Part 2: AWS Design Philosophy and Global Infrastructure     → 20
Layer 1 Part 3: Shared Responsibility and the Cost Model            → 10

# Layer 2: Core Mechanisms — 5 calls, 100 spines
Layer 2 Part 1: IAM and Security Mechanisms                         → 20
Layer 2 Part 2: Networking and VPC Mechanisms                       → 20
Layer 2 Part 3: Compute and Serverless Mechanisms                   → 20
Layer 2 Part 4: Storage and Database Mechanisms                     → 20
Layer 2 Part 5: Integration, Messaging and Delivery Mechanisms      → 20

# Layer 3: Service Mastery — 18 calls, 350 spines
Layer 3 Part 1: EC2 — Elastic Compute Cloud                         → 20
Layer 3 Part 2: Containers and Serverless Compute                   → 20
Layer 3 Part 3: S3 — Simple Storage Service                         → 20
Layer 3 Part 4: Block, File and Archival Storage                    → 20
Layer 3 Part 5: RDS and Relational Databases                        → 20
Layer 3 Part 6: DynamoDB and NoSQL Databases                        → 20
Layer 3 Part 7: Speciality Databases and Data Migration             → 20
Layer 3 Part 8: VPC and Core Networking                             → 20
Layer 3 Part 9: Content Delivery and DNS                            → 20
Layer 3 Part 10: IAM, KMS and Core Security Services                → 20
Layer 3 Part 11: Threat Detection, Compliance and Audit Services    → 20
Layer 3 Part 12: SQS, SNS, EventBridge and Messaging                → 20
Layer 3 Part 13: API Gateway, Step Functions and Workflow           → 20
Layer 3 Part 14: Analytics — Kinesis, Athena, EMR, Glue             → 20
Layer 3 Part 15: BI, ML and AI Services                             → 20
Layer 3 Part 16: Developer Tools and CI/CD                          → 20
Layer 3 Part 17: Management, Monitoring and Governance Services     → 20
Layer 3 Part 18: Billing, Cost and Support Services                 → 10

# Layer 4: Decision Patterns — 13 calls, 250 spines
Layer 4 Part 1: Resilience and High Availability Decisions          → 20
Layer 4 Part 2: Fault Tolerance and Disaster Recovery Decisions     → 20
Layer 4 Part 3: Scalability and Performance Decisions               → 20
Layer 4 Part 4: Compute Selection Decisions                         → 20
Layer 4 Part 5: Storage Selection Decisions                         → 20
Layer 4 Part 6: Database Selection Decisions                        → 20
Layer 4 Part 7: Networking and Connectivity Decisions               → 20
Layer 4 Part 8: Security Architecture Decisions                     → 20
Layer 4 Part 9: Integration and Messaging Decisions                 → 20
Layer 4 Part 10: Cost Optimisation Decisions                        → 20
Layer 4 Part 11: Serverless vs Container vs EC2 Decisions           → 20
Layer 4 Part 12: Data and Analytics Decisions                       → 20
Layer 4 Part 13: Migration Strategy Decisions                       → 10

# Layer 5: Architectural Patterns — 9 calls, 180 spines
Layer 5 Part 1: Web Application Patterns                            → 20
Layer 5 Part 2: Serverless and Event-Driven Patterns                → 20
Layer 5 Part 3: Data Lake and Analytics Patterns                    → 20
Layer 5 Part 4: Microservices and Decoupling Patterns               → 20
Layer 5 Part 5: Disaster Recovery and Business Continuity Patterns  → 20
Layer 5 Part 6: Hybrid and On-Premises Integration Patterns         → 20
Layer 5 Part 7: Multi-Account and Governance Patterns               → 20
Layer 5 Part 8: Migration and Modernisation Patterns                → 20
Layer 5 Part 9: Cost Optimisation at Scale Patterns                 → 20

# Layer 6: Exam and Interview Bridges — 3 calls, 70 spines
Layer 6 Part 1: CCP Exam Bridges and Common Traps                   → 20
Layer 6 Part 2: SAA Exam Bridges and Scenario Frameworks            → 20
Layer 6 Part 3: SAP and Interview Bridges                           → 30
```

---

# EXAM COVERAGE MAP (MANDATORY)

Every task statement below must be satisfied by at least one spine.
Use this as your checklist. Do not skip any item.
Tag every spine with the task statements it satisfies in the `notes` field.

## CCP (CLF-C02)

```
Task 1.1 — Benefits of AWS Cloud
Task 1.2 — Well-Architected Framework (6 pillars + WAT)
Task 1.3 — Migration strategies (6Rs, CAF)
Task 2.1 — Shared responsibility model
Task 2.2 — Security, governance, compliance
          (Config, GuardDuty, KMS, Shield, WAF, Macie, Inspector, Artifact)
Task 2.3 — Access management (IAM, MFA, SSO, Organizations, Cognito)
Task 2.4 — Security support (Trusted Advisor, support plans, Marketplace)
Task 3.1 — Deployment methods (Console, CLI, IaC, deployment models)
Task 3.2 — Global infrastructure (Regions, AZs, Edge, Local Zones, Outposts)
Task 3.3 — Compute (EC2, Lambda, ECS, EKS, Fargate, Beanstalk, Lightsail)
Task 3.4 — Databases (RDS, Aurora, DynamoDB, ElastiCache, Redshift, DMS)
Task 3.5 — Networking (VPC, Route53, CloudFront, PrivateLink, Global Accelerator)
Task 3.6 — Storage (S3, EBS, EFS, Glacier, Storage Gateway, Snow Family, Backup)
Task 3.7 — AI/ML and Analytics (SageMaker, Rekognition, Athena, Kinesis, Glue, QuickSight)
Task 3.8 — Other services (SNS, SQS, EventBridge, Connect, WorkSpaces, IoT Core)
Task 4.1 — Pricing models (On-Demand, Reserved, Savings Plans, Spot, Free Tier)
Task 4.2 — Billing and cost management (Cost Explorer, Budgets, CUR, Tags, Consolidated Billing)
Task 4.3 — Support plans (Basic, Developer, Business, Enterprise, TAM, Trusted Advisor)
```

## SAA (SAA-C03)

```
Task 1 — Design secure architectures
  1.1 Secure access to AWS resources
  1.2 Secure workloads and applications
  1.3 Determine appropriate data security controls

Task 2 — Design resilient architectures
  2.1 Design scalable and loosely coupled architectures
  2.2 Design highly available and fault-tolerant architectures

Task 3 — Design high-performing architectures
  3.1 High-performing and scalable storage solutions
  3.2 High-performing and elastic compute solutions
  3.3 High-performing database solutions
  3.4 High-performing and scalable network architectures
  3.5 High-performing data ingestion and transformation solutions

Task 4 — Design cost-optimised architectures
  4.1 Cost-optimised storage solutions
  4.2 Cost-optimised compute solutions
  4.3 Cost-optimised database solutions
  4.4 Cost-optimised network architectures
```

## SAP (SAP-C02)

```
Task 1 — Design solutions for organisational complexity
  1.1 Architect network connectivity strategies
  1.2 Prescribe security controls
  1.3 Design reliable and resilient architectures
  1.4 Design a multi-account AWS environment
  1.5 Determine cost optimisation and visibility strategies

Task 2 — Design for new solutions
  2.1 Determine deployment strategy for new workloads
  2.2 Design a solution to ensure business continuity
  2.3 Determine security controls for new workloads
  2.4 Design a strategy to migrate existing workloads

Task 3 — Continuous improvement for existing solutions
  3.1 Strategy to improve operational excellence
  3.2 Strategy to improve security
  3.3 Strategy to improve performance
  3.4 Strategy to improve reliability
  3.5 Identify cost optimisation opportunities

Task 4 — Accelerate workload migration and modernisation
  4.1 Select existing workloads for potential migration
  4.2 Determine migration approach and tools
  4.3 Determine optimisation strategies for workloads
```

---

# LAYER RULES — WHAT BELONGS WHERE

These rules are hard. Do not mix purposes across layers.

## Layer 1 — Foundations
- Definitional. Conceptual. No service-specific mechanics.
- Covers the mental models a learner needs before touching any service.
- spine_type: mental_model or concept only.
- exams: always includes CCP. Many also apply to SAA and SAP.
- concept_tier: foundation or core only. No extension spines.

## Layer 2 — Core Mechanisms
- Mechanistic. How things actually work under the hood.
- Not "what S3 is" — that's L3. This is "how S3 consistency works".
- Not "what IAM is" — that's L3. This is "how IAM evaluates a request".
- spine_type: mental_model or concept only.
- exams: CCP for basic mechanisms. SAA/SAP for advanced ones.
- interviews: true for most L2 spines — these are exactly what
  interviewers test.

## Layer 3 — Service Mastery
- Every significant service. What it is. Why it exists.
- One spine per distinct service capability. Not one spine per service.
  (S3 gets ~20 spines across its call — versioning, lifecycle,
  storage classes, bucket policies etc. are all distinct.)
- spine_type: concept for most. contrast where a service is
  commonly confused with another.
- exams: tag every exam the service appears in.
- concept_tier: foundation for the service overview, core and
  extension for specific capabilities.

## Layer 4 — Decision Patterns
- When to use X vs Y. Never "what is X".
- The content is the decision rule, not the service definition.
- spine_type: contrast for most. mental_model for decision frameworks.
- exams: SAA and SAP primarily. CCP occasionally for basic decisions.
- interviews: true for most L4 spines.
- domain: Cross-Domain for most (decisions span domains).

## Layer 5 — Architectural Patterns
- How services compose. Real system designs.
- Not "what Lambda is" — that's L3. This is "how to build a
  serverless event pipeline with Lambda + SQS + DynamoDB".
- spine_type: pattern for most. mental_model for architectural frameworks.
- exams: SAP primarily. SAA for some patterns.
- interviews: true for most L5 spines.
- domain: Cross-Domain always.

## Layer 6 — Exam and Interview Bridges
- NOT new concepts. Maps existing understanding to performance.
- spine_type: bridge only.
- exams: tag the specific exam this bridge targets.
- interviews: true for interview bridges. false for pure exam bridges.
- domain: Cross-Domain always.
- concept_tier: extension always.

---

# ANTI-DUPLICATION RULES

The spine list grows call by call. Each call receives the already-
generated slug list as context. Check every slug before generating.

## Rule 1 — No same concept at different layers
If L3 has a spine for "what DynamoDB is", L4 should not have
"DynamoDB overview" — it should have "when to choose DynamoDB
vs RDS" or "when to choose DynamoDB vs ElastiCache".
Layer determines angle. If the angle is the same, it's a duplicate.

## Rule 2 — No same service, same angle
Two spines covering the same service from the same teaching angle
must be merged.

DUPLICATE: "S3 Storage Classes Overview" + "Choosing an S3 Storage Class"
NOT DUPLICATE: "S3 Storage Classes" (L3 concept) + "S3 vs EBS vs EFS
for a web application" (L4 contrast)

## Rule 3 — Shared concepts are tagged, not duplicated
If a concept appears in both CCP and SAA, one spine covers it with
`exams: [CCP, SAA]`. Never generate two spines for the same concept
targeting different exams.

## Rule 4 — Framework components
Well-Architected pillars each get ONE spine in L1.
Individual pillar design principles do NOT get their own spine.
CAF perspectives get ONE spine covering all 6 in L1.
6Rs migration strategies get ONE spine in L1, unless two strategies
are commonly confused enough to warrant a contrast spine.

## Rule 5 — Slug collision check
Before outputting, scan every slug in the ALREADY GENERATED list.
Any slug collision must be resolved by renaming with a layer prefix:
l2-iam-evaluation vs l3-iam-service

---

# SPINE_TYPE RULES

spine_type determines how Stage 3 (expand) treats the concept
and how Stage 4 (narrate) scripts it.

**mental_model** — A framework with multiple parts.
Used for: Well-Architected Framework, IAM evaluation logic,
VPC routing model, the shared responsibility model.
Expands into a structured explanation of each part and how
they relate. Scripts as a "let me walk you through this" session.

**concept** — A single service or idea.
Used for: most L2 and L3 spines. What EC2 Auto Scaling is.
How S3 versioning works.
Expands into definition, mechanics, scenarios.
Scripts as direct explanation.

**contrast** — Distinguishes between two or more things.
Used for: most L4 spines. SQS vs SNS. Multi-AZ vs Multi-Region.
Must name both things in the title.
Expands into a side-by-side comparison with decision rules.
Scripts as a "here's where people get confused" session.

**pattern** — A reusable architectural pattern.
Used for: all L5 spines. Three-tier web app. Event-driven pipeline.
Expands into a scenario walkthrough naming the services involved.
Scripts as a worked example with a real business scenario.

**bridge** — Maps understanding to exam/interview format.
Used for: all L6 spines only.
Expands into question types, distractor patterns, scenario frameworks.
Scripts as exam/interview coaching.

---

# CONCEPT_SPINE RULES

The concept_spine is one sentence. One idea.

Written as a confident human teaching statement — not a definition
label, not a fact, not a feature list.

No "and" joining two ideas.

The test: could a teacher speak this sentence to a class and have
it land as a genuine insight? If yes — good. If it sounds like
a documentation summary — rewrite it.

FAIL: "IAM allows you to manage access to AWS services and resources."
PASS: "IAM is the single place where every permission decision in
your AWS account is made — nothing happens in AWS without IAM
either allowing it or staying silent."

FAIL: "S3 has multiple storage classes for different access patterns."
PASS: "S3 storage classes let you pay for exactly the retrieval speed
you need — from milliseconds for Standard to hours for Glacier Deep
Archive — so rarely-touched data costs a fraction of active data."

FAIL: "Multi-AZ provides high availability for RDS."
PASS: "RDS Multi-AZ keeps a silent standby in a second Availability
Zone that takes over in under two minutes if the primary fails —
so your database survives an AZ outage without any application change."

---

# CONCEPT TIER RULES

**foundation** — The concept everything else in this layer builds on.
Max 15% of any call. Used sparingly.

**core** — The main body of the call. ~60% of spines.

**extension** — Nuance, specificity, important distinctions.
Minimum 20% of any call. Never skip extension spines — they are
where the exam differentiators live.

---

# SEQUENCING RULES

Within each call, order spines as a learning arc:
1. Foundation concepts first, in dependency order
2. Core concepts next, each following what it builds on
3. Extension concepts last

IDs are globally sequential from 1 to 1000 across all calls.
Never reset between calls. Each call receives START_ID.

---

# SLUG RULES

Globally unique kebab-case.
Use layer + domain-context prefixes where collision risk exists:
- l2-iam-evaluation-model   (not iam-evaluation-model)
- l3-ec2-auto-scaling       (not ec2-auto-scaling)
- l4-rds-vs-dynamodb        (not rds-vs-dynamodb)
- l5-serverless-pipeline    (not serverless-pipeline)

Do not use generic slugs:
BAD:  aws-security
GOOD: l2-iam-permission-evaluation

---

# SERVICE CONTROL

aws_service must be either "General" or an official in-scope
AWS service name relevant to CCP, SAA, or SAP.

Never use deprecated service names. If uncertain, use "General".

For L4/L5 spines that involve multiple services, use the primary
service or "General".

---

# OUTPUT FORMAT

Return ONLY valid YAML. No markdown fences. No commentary.
No explanation before or after the YAML.

Start directly with `- id:` for the first spine.

Every spine must have exactly these fields in this order:

```yaml
- id: <integer>
  slug: <kebab-case, globally unique>
  title: <human readable, specific>

  layer: <1-6>
  layer_name: <Foundations | Core Mechanisms | Service Mastery |
               Decision Patterns | Architectural Patterns |
               Exam and Interview Bridges>

  spine_type: <mental_model | concept | contrast | pattern | bridge>

  exams: [<CCP | SAA | SAP — one or more>]
  interviews: <true | false>

  domain: <Cloud Concepts | Security and Compliance |
           Cloud Technology and Services |
           Billing, Pricing, and Support | Cross-Domain>

  aws_service: <General | official AWS service name>

  concept_tier: <foundation | core | extension>
  cognitive_role: <definition | contrast | model | application>

  concept_spine: "<one sentence, one idea, confident teaching voice>"

  notes: "<all exam task statements this spine satisfies>"
  # Do NOT include an approved field. It is added manually during curation.
```

After outputting all spines for the call, append a single summary line:
# Call: <call name> | Count: <n> | IDs: <start>–<end>

---

# PLANNING PHASE (SILENT — DO NOT OUTPUT)

Before generating any YAML, complete this silently:

## Step 1 — Scope check
Read the call name carefully. What services, mechanisms, or patterns
are in scope? What is explicitly out of scope for this call (but
covered in another call)?

## Step 2 — Layer integrity check
For every planned spine, ask: does this belong in this layer?
Is the angle right for the layer (mechanism for L2, service for L3,
decision for L4, pattern for L5)?

## Step 3 — Exam coverage check
Which exam task statements does this call need to satisfy?
Verify every relevant task from the Exam Coverage Map is covered.
Add spines if a task is uncovered.

## Step 4 — Dedup check
Check every planned spine against the ALREADY GENERATED SLUGS list.
For any slug that would collide — rename with layer prefix.
For any concept already covered at the right layer — drop it.

## Step 5 — spine_type check
Verify every L4 spine is a contrast or mental_model — not a concept.
Verify every L5 spine is a pattern or mental_model — not a concept.
Verify every L6 spine is a bridge — nothing else.

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