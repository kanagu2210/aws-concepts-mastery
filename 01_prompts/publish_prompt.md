# AWS Concept Mastery — Publisher
## Stage 6 of 6 — HTML to PDF (Publish)
### publish_prompt.md

---

# PURPOSE

Stage 6 converts the HTML files produced by Stage 5 (Render)
into PDF files using WeasyPrint.

This is not a prompt for Claude. It is the specification for
the `--publish`, `--combine`, and `--complete` modes of `run.py`
— the main pipeline script.

---

# WHAT THIS STAGE DOES

Input:  `.html` files from `output/03_rendered/` (produced by Stage 5)
Output: One `.pdf` file per concept in `output/04_published/individual/`
        Combined `.pdf` files per layer in `output/04_published/combined/`
        One complete `.pdf` in `output/04_published/combined/`

Stage 6 only reads the HTML files — the narrated `.md` files
are already embedded in the HTML by Stage 5. They are stored
in `output/02_narrated/` for independent use (editing, text-to-speech,
review) but Stage 6 does not need to read them directly.

---

# PROJECT STRUCTURE

```
aws-concepts-mastery/
├── 01_prompts/
│   ├── outline_prompt.md
│   ├── expand_prompt.md
│   ├── narrate_prompt.md
│   ├── render_prompt.md
│   └── publish_prompt.md          ← this file
├── 02_pipeline/
│   ├── run_outline.py             ← one-time spine generation
│   └── run.py                     ← stages 1–4 per spine (+ publish modes)
├── input/
│   └── concept_spines.yaml        ← reviewed and approved spine list
├── output/
│   ├── 01_concepts/               ← Stage 3 output (expanded concept YAMLs)
│   ├── 02_narrated/               ← Stage 4 output (teaching script .md files)
│   │   └── 0047_iam-permission-evaluation-model.md
│   ├── 03_rendered/               ← Stage 5 output (HTML pages)
│   │   └── 0047_iam-permission-evaluation-model.html
│   └── 04_published/              ← Stage 6 output (PDFs)
│       ├── individual/
│       │   └── 0047_iam-permission-evaluation-model.pdf
│       └── combined/
│           ├── layer_1_foundations.pdf
│           ├── layer_2_core_mechanisms.pdf
│           ├── layer_3_service_mastery.pdf
│           ├── layer_4_decision_patterns.pdf
│           ├── layer_5_architectural_patterns.pdf
│           ├── layer_6_exam_bridges.pdf
│           └── aws_concept_mastery_complete.pdf
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── api.py
│   └── usage_log.py
├── logs/
│   ├── usage_outline.tsv
│   ├── usage_run.tsv
│   └── backups/
├── config.yaml
├── .env
└── requirements.txt
```

---

# DEPENDENCIES

```bash
pip install weasyprint --break-system-packages
```

WeasyPrint requires system dependencies on some platforms:

```bash
# Ubuntu / Debian
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0

# macOS (via Homebrew)
brew install pango
```

WeasyPrint version: 60.0 or later.
Check with: `python -c "import weasyprint; print(weasyprint.__version__)"`

---

# run.py PUBLISH MODES — FULL SPECIFICATION

## Command line interface

Publish is not part of the default pipeline. It is triggered only
by passing one of these flags to `run.py`:

```bash
# Publish a single concept (HTML → PDF)
python 02_pipeline/run.py --spine 47 --publish

# Publish a range of concepts
python 02_pipeline/run.py --from 1 --to 50 --publish

# Publish all concepts in a layer
python 02_pipeline/run.py --layer 2 --publish

# Publish all concepts
python 02_pipeline/run.py --all --publish

# Build combined PDFs by layer (requires individual PDFs to exist)
python 02_pipeline/run.py --combine

# Build the single complete PDF (requires all individual PDFs)
python 02_pipeline/run.py --complete

# Dry run — list what would be generated without generating
python 02_pipeline/run.py --all --publish --dry-run
```

## Core logic

```python
from weasyprint import HTML
from pathlib import Path

def render_pdf(html_path: Path, pdf_path: Path) -> None:
    """Convert one HTML file to one PDF file."""
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(filename=str(html_path)).write_pdf(
        target=str(pdf_path),
        presentational_hints=True,
    )
```

`presentational_hints=True` tells WeasyPrint to respect HTML
presentational attributes (width, height, bgcolor etc.) in
addition to CSS. Always pass this flag.

## Resume behaviour

Before generating a PDF, check if it already exists.
If it exists and the HTML source has not been modified since
the PDF was generated — skip it.

Use file modification timestamps for this check:

```python
def needs_regeneration(html_path: Path, pdf_path: Path) -> bool:
    if not pdf_path.exists():
        return True
    return html_path.stat().st_mtime > pdf_path.stat().st_mtime
```

## Ordering

Individual PDFs are named `<id>_<slug>.pdf` so they sort correctly
by concept ID. Combined PDFs are assembled in ID order within each layer.

```python
# Correct naming
pdf_name = f"{concept_id:04d}_{slug}.pdf"
# e.g. 0047_iam-permission-evaluation-model.pdf
```

## Combining PDFs

Use pypdf to merge individual PDFs into layer and complete combined files:

```bash
pip install pypdf --break-system-packages
```

```python
from pypdf import PdfWriter

def combine_pdfs(pdf_paths: list[Path], output_path: Path) -> None:
    writer = PdfWriter()
    for path in sorted(pdf_paths):
        writer.append(str(path))
    with open(output_path, "wb") as f:
        writer.write(f)
```

## Logging

Log each conversion to `logs/usage_run.tsv` using the same
`usage_log.py` utility as other stages. Use `stage = "publish"`
and `cost_usd = 0` since this stage makes no API calls.

```
timestamp   stage     spine_id  slug    pages   duration_s  status
```

## Error handling

WeasyPrint may warn about unsupported CSS properties.
Capture warnings and log them — do not treat them as fatal errors.
Only treat an exception that prevents PDF output as a failure.

```python
import logging

# Suppress WeasyPrint CSS warnings that don't affect output
logging.getLogger('weasyprint').setLevel(logging.ERROR)
```

If a single concept fails, log the error and continue to the next.
Never let one failure abort a batch run.

## Progress reporting

For batch runs, print progress to stdout:

```
[PDF] 0001_what-cloud-computing-actually-is.pdf ... done (1.2s)
[PDF] 0002_on-demand-vs-traditional-infrastructure.pdf ... done (0.9s)
[SKIP] 0003_aws-global-infrastructure.pdf — up to date
...
[DONE] Layer 1: 10 generated, 40 skipped, 0 failed
```

---

# WEASYPRINT CSS NOTES

## What renders correctly

- All layout skeletons from Stage 5 (L1–L10)
- CSS Grid and Flexbox — fully supported
- Google Fonts via CDN — fetched at render time (requires internet)
- CSS custom properties — supported
- `box-shadow` — renders correctly
- `transform: rotate()` — renders correctly
- `border-radius` — renders correctly
- Background colours and images — preserved when
  `print-color-adjust: exact` is set in the HTML

## What does not render

- `position: sticky` — ignored (Stage 5 already bans this)
- CSS animations — ignored (Stage 5 already bans this)
- JavaScript — not executed (Stage 5 already bans JS)
- `backdrop-filter` — ignored

## Offline font fallback

If Google Fonts CDN is unavailable at render time, WeasyPrint
falls back to system fonts. This changes the visual appearance.

For production runs, either:
1. Ensure internet access during PDF generation, or
2. Download fonts and self-host them in `assets/fonts/`
   and update the HTML `@font-face` declarations accordingly.

The config.yaml should have an `offline_fonts: true/false` flag
that `run.py` reads to decide which approach to use.

---

# config.yaml ADDITIONS

Add these keys to config.yaml for Stage 6:

```yaml
pdf:
  rendered_dir: "output/03_rendered"
  output_dir: "output/04_published"
  individual_subdir: "individual"
  combined_subdir: "combined"
  offline_fonts: false          # set true for air-gapped environments
  weasyprint_log_level: "ERROR" # ERROR | WARNING | INFO
  combined_by_layer: true       # generate per-layer combined PDFs
  combined_complete: true       # generate single complete PDF
```

---

# PIPELINE SUMMARY

For reference — the complete pipeline:

| Stage | Name    | Triggered by              | Prompt              | Output                          |
|-------|---------|---------------------------|---------------------|---------------------------------|
| 1     | Outline | run_outline.py            | outline_prompt.md   | input/concept_spines.yaml       |
| 2     | Curate  | run_curate.py             | (no prompt)         | terminal report — you edit yaml |
| 3     | Expand  | run.py (default)          | expand_prompt.md    | output/01_concepts/             |
| 4     | Narrate | run.py (default)          | narrate_prompt.md   | output/02_narrated/             |
| 5     | Render  | run.py (default)          | render_prompt.md    | output/03_rendered/             |
| 6     | Publish | run.py (--publish flag)   | publish_prompt.md   | output/04_published/            |