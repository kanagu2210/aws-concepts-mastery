# AWS Concept Mastery — Project Folder Structure

```
aws-concepts-mastery/
│
│   # ── ROOT FILES ──────────────────────────────────────────────────────
│
├── config.yaml
│   # Central configuration file.
│   # Stores model name, max_tokens, all directory paths, and PDF settings.
│   # Every script reads from this — never hardcode paths in scripts.
│
├── .env
│   # Your Anthropic API key. Never commit this to git.
│   # ANTHROPIC_API_KEY=sk-ant-...
│
├── .gitignore
│   # Committed:    01_prompts/, input/, utils/, config.yaml, requirements.txt
│   # NOT committed: .env, venv/, output/, logs/
│
├── requirements.txt
│   # anthropic, pyyaml, weasyprint, pypdf
│
│
│   # ── 01_prompts ───────────────────────────────────────────────────────
│   # All Claude prompt templates. One per stage.
│   # Committed to git — these are the instructions that drive generation.
│   # Edit these to change how Claude generates content.
│   # Scripts in 02_pipeline/ load these and inject variables before
│   # calling the API.
│
├── 01_prompts/
│   │
│   ├── outline_prompt.md
│   │   # Used by run_outline.py — Stage 1.
│   │   # Tells Claude how to generate concept spines.
│   │   # 51 API calls × 20 spines = 1000 spines total.
│   │   # Variables injected: {domain_call}, {start_id},
│   │   # {target_count}, {domain_value}, {existing_slugs}
│   │
│   ├── expand_prompt.md
│   │   # Used by run.py — Stage 3 (Expand).
│   │   # Tells Claude how to expand one spine into a full concept.
│   │   # Variables injected: {spine_yaml}
│   │
│   ├── narrate_prompt.md
│   │   # Used by run.py — Stage 4 (Narrate).
│   │   # Tells Claude how to write a spoken teaching script.
│   │   # Variables injected: {concept_yaml}
│   │
│   ├── render_prompt.md
│   │   # Used by run.py — Stage 5 (Render).
│   │   # Tells Claude how to render a script as a PDF-ready HTML page.
│   │   # Variables injected: {{TITLE}}, {{LAYER}}, {{EXAMS}}, {{MARKDOWN}}
│   │
│   └── publish_prompt.md
│       # Specification for run.py — Stage 6 (Publish).
│       # Not a Claude prompt — documents the WeasyPrint PDF generation logic.
│       # No variables — this stage makes no API calls.
│
│
│   # ── 02_pipeline ──────────────────────────────────────────────────────
│   # Three scripts. Committed to git.
│   #
│   # Correct order of operations:
│   #   1. python 02_pipeline/run_outline.py    ← Stage 1: generate all spines
│   #   2. python 02_pipeline/run_curate.py     ← Stage 2: validate + review report
│   #   3. edit input/concept_spines.yaml       ← set approved: false on any spine to hold back
│   #   4. python 02_pipeline/run.py            ← Stages 3–6: pipeline per spine
│
├── 02_pipeline/
│   │
│   ├── run_outline.py
│   │   # Stage 1 — Spine Generation.
│   │   # One-time script. Run once before anything else.
│   │   # Generates all 1000 concept spines across 51 API calls.
│   │   # Reads:  01_prompts/outline_prompt.md
│   │   # Writes: input/concept_spines.yaml
│   │   #         logs/backups/outline/ (per-call backups)
│   │   #
│   │   # Usage:
│   │   #   python 02_pipeline/run_outline.py --dry-run
│   │   #   python 02_pipeline/run_outline.py
│   │   #   python 02_pipeline/run_outline.py --resume
│   │
│   ├── run_curate.py
│   │   # Stage 2 — Curation.
│   │   # Run after run_outline.py, before run.py.
│   │   # Makes NO API calls. Reads concept_spines.yaml and prints
│   │   # a structured validation report to the terminal.
│   │   #
│   │   # Does NOT modify concept_spines.yaml — that is your job.
│   │   # After reading the report, open input/concept_spines.yaml
│   │   # and add approved: false at the top of any spine to hold back.
│   │   # Spines with no approved field → run.
│   │   # Spines with approved: true   → run.
│   │   # Spines with approved: false  → skipped by run.py.
│   │   #
│   │   # Checks performed:
│   │   #
│   │   #   STRUCTURAL
│   │   #   — ID sequence is unbroken (no gaps, no duplicates)
│   │   #   — No duplicate slugs
│   │   #   — Layer spine counts match targets (50/100/350/250/180/70)
│   │   #   — spine_type valid per layer rules
│   │   #       L4: contrast or mental_model only
│   │   #       L5: pattern or mental_model only
│   │   #       L6: bridge only
│   │   #   — concept_tier valid per layer rules
│   │   #       L1: foundation or core only (no extension)
│   │   #       L6: extension only
│   │   #   — exams field not empty on any spine
│   │   #   — concept_spine contains no " and " joining two ideas
│   │   #   — notes field populated on every spine
│   │   #
│   │   #   COVERAGE
│   │   #   — Every CCP task statement (1.1–4.3) covered by at least one spine
│   │   #   — Every SAA task statement covered by at least one spine
│   │   #   — Every SAP task statement covered by at least one spine
│   │   #   — Every major in-scope AWS service has at least one L3 spine
│   │   #   — Every major L4 decision pattern present
│   │   #   — Every major L5 architectural pattern present
│   │   #
│   │   #   QUALITY FLAGS (advisory — not errors)
│   │   #   — concept_spine sounds like documentation (no genuine insight)
│   │   #   — contrast spine title missing one or both things being contrasted
│   │   #   — bridge spine at wrong layer (not L6)
│   │   #   — L2 spine that describes a service rather than its mechanism
│   │   #   — L5 spine with spine_type: concept instead of pattern
│   │   #
│   │   # Usage:
│   │   #   python 02_pipeline/run_curate.py
│   │   #   python 02_pipeline/run_curate.py --layer 3
│   │   #   python 02_pipeline/run_curate.py --errors-only
│   │
│   └── run.py
│       # Stages 3–6 — Main pipeline script.
│       # Run after run_curate.py and after editing concept_spines.yaml.
│       # Skips any spine with approved: false — prints a skip line for each.
│       # Default pipeline runs 3 stages per spine:
│       #   Stage 3 — Expand:   spine → full concept
│       #   Stage 4 — Narrate:  concept → teaching script (.md)
│       #   Stage 5 — Render:   script → HTML page
│       #
│       # Publish (HTML → PDF) is NOT part of the default pipeline.
│       # Trigger it explicitly with --publish, --combine, or --complete.
│       #
│       # Reads:  input/concept_spines.yaml
│       #         01_prompts/expand_prompt.md
│       #         01_prompts/narrate_prompt.md
│       #         01_prompts/render_prompt.md
│       #
│       # Writes: output/01_concepts/<id>_<slug>.yaml
│       #         output/02_narrated/<id>_<slug>.md
│       #         output/03_rendered/<id>_<slug>.html
│       #         output/04_published/individual/<id>_<slug>.pdf (--publish only)
│       #
│       # Usage:
│       #
│       #   — Normal runs (expand + narrate + render) —
│       #   python 02_pipeline/run.py --spine 47
│       #   python 02_pipeline/run.py --from 1 --to 50
│       #   python 02_pipeline/run.py --layer 2
│       #   python 02_pipeline/run.py --all
│       #   python 02_pipeline/run.py --from 1 --to 50 --dry-run
│       #   python 02_pipeline/run.py --from 1 --to 50 --resume
│       #   python 02_pipeline/run.py --spine 47 --start-stage narrate
│       #   # --start-stage skips earlier stages already completed
│       #   # values: expand | narrate | render
│       #
│       #   — Publish runs (only when PDFs are needed) —
│       #   python 02_pipeline/run.py --spine 47 --publish
│       #   python 02_pipeline/run.py --from 1 --to 50 --publish
│       #   python 02_pipeline/run.py --layer 2 --publish
│       #   python 02_pipeline/run.py --combine
│       #   python 02_pipeline/run.py --complete
│
│
│   # ── input ────────────────────────────────────────────────────────────
│   # Human-reviewed source data. Committed to git.
│   # concept_spines.yaml is written by run_outline.py, validated by
│   # run_curate.py, and curated by you before run.py is executed.
│
├── input/
│   └── concept_spines.yaml
│       # All 1000 concept spines.
│       # Written by run_outline.py. Validated by run_curate.py.
│       # Curated by you — set approved: false at the top of any spine
│       # you want to hold back from the pipeline.
│       #
│       # approved field rules:
│       #   (field absent)   → spine runs — default behaviour
│       #   approved: true   → spine runs
│       #   approved: false  → spine skipped — run.py prints:
│       #                      [SKIP] 0047_slug — approved: false
│       #
│       # Each spine: approved (optional), id, slug, title, layer,
│       # layer_name, spine_type, exams, interviews, domain, aws_service,
│       # concept_tier, cognitive_role, concept_spine, notes.
│       #
│       # approved sits at the top of the spine so it is immediately
│       # visible when scanning the file.
│
│
│   # ── output ───────────────────────────────────────────────────────────
│   # All generated content. NOT committed to git.
│   # One subfolder per pipeline stage, numbered in pipeline order.
│   # Delete this entire folder for a clean slate — nothing here
│   # cannot be regenerated from input/ and 01_prompts/.
│
├── output/
│   │
│   ├── 01_concepts/
│   │   # Expanded concepts. Stage 3 output of run.py (Expand).
│   │   # One .yaml file per concept — not one large file.
│   │   # A failed expand on spine 47 affects only that file.
│   │   ├── 0001_what-cloud-computing-actually-is.yaml
│   │   ├── 0002_on-demand-vs-traditional-infrastructure.yaml
│   │   ├── ...
│   │   └── 1000_sap-interview-bridges.yaml
│   │
│   ├── 02_narrated/
│   │   # Spoken teaching scripts. Stage 4 output of run.py (Narrate).
│   │   # One .md file per concept.
│   │   # Each file: YAML front matter + full teaching script.
│   │   # Use independently for: human review, editing, text-to-speech.
│   │   ├── 0001_what-cloud-computing-actually-is.md
│   │   ├── 0002_on-demand-vs-traditional-infrastructure.md
│   │   ├── ...
│   │   └── 1000_sap-interview-bridges.md
│   │
│   ├── 03_rendered/
│   │   # Self-contained HTML pages. Stage 5 output of run.py (Render).
│   │   # One .html file per concept. Opens in any browser, no server needed.
│   │   # PDF-first CSS — preview in browser before publishing.
│   │   ├── 0001_what-cloud-computing-actually-is.html
│   │   ├── 0002_on-demand-vs-traditional-infrastructure.html
│   │   ├── ...
│   │   └── 1000_sap-interview-bridges.html
│   │
│   └── 04_published/
│       # Final PDF output. Stage 6 output of run.py (Publish).
│       # Only generated when --publish, --combine, or --complete is passed.
│       │
│       ├── individual/
│       │   # One PDF per concept.
│       │   ├── 0001_what-cloud-computing-actually-is.pdf
│       │   ├── 0002_on-demand-vs-traditional-infrastructure.pdf
│       │   ├── ...
│       │   └── 1000_sap-interview-bridges.pdf
│       │
│       └── combined/
│           # Merged PDFs. Generated by --combine and --complete flags.
│           ├── layer_1_foundations.pdf
│           ├── layer_2_core_mechanisms.pdf
│           ├── layer_3_service_mastery.pdf
│           ├── layer_4_decision_patterns.pdf
│           ├── layer_5_architectural_patterns.pdf
│           ├── layer_6_exam_bridges.pdf
│           └── aws_concept_mastery_complete.pdf
│
│
│   # ── utils ─────────────────────────────────────────────────────────────
│   # Shared Python modules. Committed to git.
│   # Imported by all pipeline scripts — never duplicate logic.
│
├── utils/
│   ├── __init__.py
│   │   # Makes utils a proper Python package — required for imports.
│   │
│   ├── config.py
│   │   # Loads config.yaml. Exposes all settings as a typed object.
│   │   # Usage: from utils.config import config
│   │
│   ├── api.py
│   │   # Anthropic API wrapper.
│   │   # Handles: client setup, streaming, retries with backoff, error logging.
│   │   # All API calls go through this — never call the API directly.
│   │   # Usage: from utils.api import call_claude
│   │
│   └── usage_log.py
│       # Logs every API call to logs/usage_*.tsv.
│       # Columns: timestamp, stage, spine_id, slug, input_tokens,
│       #          output_tokens, cost_usd, duration_s, status
│       # Usage: from utils.usage_log import log_usage
│
│
│   # ── logs ──────────────────────────────────────────────────────────────
│   # Runtime logs and backups. NOT committed to git.
│   # TSV files track every API call — monitor cost and debug failures.
│
└── logs/
    │
    ├── usage_outline.tsv
    │   # One row per API call in run_outline.py. 51 rows when complete.
    │
    ├── usage_run.tsv
    │   # One row per stage per spine in run.py. Up to 3000 rows when complete.
    │   # Publish stage logged here with cost_usd = 0.
    │   # Skipped spines logged here with status = skipped.
    │
    └── backups/
        │   # Safety net. Only outline and expand backed up here —
        │   # narrate and render already saved in output/02_narrated/
        │   # and output/03_rendered/.
        │
        ├── outline/
        │   # One .yaml per outline API call (51 files when complete).
        │   # If run_outline.py fails mid-run, resume from last backup.
        │   ├── layer_1_part_1_the_8_big_ideas.yaml
        │   └── ...
        │
        └── expand/
            # One .yaml per expanded concept (1000 files when complete).
            # Mirrors output/01_concepts/ — restore from here if deleted.
            ├── 0001_what-cloud-computing-actually-is.yaml
            └── ...
```