"""
02_pipeline/run.py
Stages 3–5 — Expand, Narrate, Render.

Output files are nested by layer and part:
  output/01_concepts/layer_3/part_7/0271_slug.yaml
  output/02_narrated/layer_3/part_7/0271_slug.md  ← updated in-place by curate
  output/03_rendered/layer_3/part_7/0271_slug.html

Narration is multipart:
  1. A planning call splits the includes array into N parts
  2. N separate narration calls generate each part
  3. All parts are combined into one .md file with --- section breaks

Whiteboard and Publish are separate scripts:
  python 02_pipeline/run_whiteboard.py --spine 47
  python 02_pipeline/run_publish.py --spine 47

Usage:
    python 02_pipeline/run.py --spine 47
    python 02_pipeline/run.py --from 1 --to 50
    python 02_pipeline/run.py --spines 47 755 802
    python 02_pipeline/run.py --layer 2
    python 02_pipeline/run.py --all

    python 02_pipeline/run.py --spine 47 --start-stage narrate
    python 02_pipeline/run.py --spine 47 --start-stage curate
    python 02_pipeline/run.py --spine 47 --start-stage render
    python 02_pipeline/run.py --all --resume
    python 02_pipeline/run.py --from 1 --to 50
    python 02_pipeline/run.py --spines 47 755 802 --dry-run

    python 02_pipeline/run.py --combine
    python 02_pipeline/run.py --complete
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import time
from pathlib import Path
from typing import Optional

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.api import call_claude
from utils.call_plan import get_part_folder
from utils.config import config
from utils.usage_log import compute_cost, log_usage
from pipeline_common import (
    _part_subdir,
    _select_spines,
    _strip_front_matter,
    _load_spines,
    _get_spine,
    concept_path,
    narrated_path,
    whiteboard_path,
    rendered_path,
    merged_path,
    published_path,
    combined_dir,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
STAGES        = ["expand", "narrate", "curate", "render"]
STAGE_INDEXES = {s: i for i, s in enumerate(STAGES)}
LOG_FILE      = config.paths.logs_dir / "usage_run.tsv"


# ---------------------------------------------------------------------------
# Nested path helpers
# ---------------------------------------------------------------------------

# Path helpers, spine loaders, and _select_spines live in pipeline_common.py

def _load_prompt(name: str) -> str:
    path = config.paths.prompts_dir / f"{name}_prompt.md"
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {path}")
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Stage 3 — Expand
# ---------------------------------------------------------------------------

def run_expand(spine: dict, dry_run: bool = False) -> Optional[str]:
    spine_id = spine["id"]
    slug     = spine["slug"]
    out_path = concept_path(spine_id, slug)

    if dry_run:
        print(f"  [expand]  would write → {_part_subdir(spine_id)}/{out_path.name}")
        return None

    prompt       = _load_prompt("expand")
    spine_yaml   = yaml.dump([spine], allow_unicode=True, sort_keys=False, default_flow_style=False)
    user_content = f"{prompt}\n\n---\n\n# SPINE INPUT\n\n{spine_yaml}"

    t0 = time.monotonic()
    raw, in_tok, out_tok = call_claude(user_content)
    duration = time.monotonic() - t0
    cost     = compute_cost(in_tok, out_tok)

    clean = _strip_code_fence(raw, "yaml")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(clean, encoding="utf-8")

    log_usage(LOG_FILE, "expand", spine_id, slug, in_tok, out_tok, cost, duration, "ok")
    print(f"  [expand]  {in_tok:,}→{out_tok:,} tok  ${cost:.4f}  {duration:.1f}s  → {out_path.name}")
    return clean


# ---------------------------------------------------------------------------
# Stage 4 — Narrate (multipart)
# ---------------------------------------------------------------------------

def _parse_concept_entry(concept_yaml: str) -> dict:
    """Load the first item from the expanded concept YAML."""
    data = yaml.safe_load(concept_yaml)
    if isinstance(data, list) and data:
        return data[0]
    if isinstance(data, dict):
        return data
    return {}


def _get_includes(concept: dict) -> list[str]:
    """Extract boundary.includes as a list of strings."""
    return concept.get("boundary", {}).get("includes", [])


def _plan_narration(concept_yaml: str, spine_id: int, slug: str) -> list[dict]:
    """
    Phase A — one API call that returns a JSON plan:
    [{"part": 1, "include_indexes": [...], "focus": "...", "handoff_to_next": "..."}, ...]

    If the concept has 4 or fewer includes, returns a single-part plan without an API call.
    """
    concept  = _parse_concept_entry(concept_yaml)
    includes = _get_includes(concept)
    n        = len(includes)

    # Single part — no planning call needed
    if n <= 4:
        return [{"part": 1, "include_indexes": list(range(n)), "focus": "Full concept"}]

    plan_prompt = _load_prompt("narrate_plan")
    user_content = f"{plan_prompt}\n\n{concept_yaml}"

    t0 = time.monotonic()
    raw, in_tok, out_tok = call_claude(user_content)
    duration = time.monotonic() - t0
    cost     = compute_cost(in_tok, out_tok)

    log_usage(LOG_FILE, "narrate_plan", spine_id, slug, in_tok, out_tok, cost, duration, "ok")
    print(f"  [plan]    {in_tok:,}→{out_tok:,} tok  ${cost:.4f}  {duration:.1f}s  ({n} includes)")

    # Parse JSON — strip fences and fix common model errors
    cleaned = re.sub(r"^```json\s*|^```\s*|\s*```$", "", raw.strip(), flags=re.MULTILINE).strip()
    # Fix trailing commas before } or ] — common LLM JSON error
    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)
    try:
        plan_data = json.loads(cleaned)
        parts = plan_data.get("parts", plan_data) if isinstance(plan_data, dict) else plan_data
        return parts
    except json.JSONDecodeError as e:
        print(f"  [warn] plan JSON parse failed ({e}) — falling back to single part", file=sys.stderr)
        return [{"part": 1, "include_indexes": list(range(n)), "focus": "Full concept"}]


def _extract_last_paragraph(text: str) -> str:
    """Return the last non-empty paragraph of a script text."""
    paragraphs = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
    return paragraphs[-1] if paragraphs else ""


def _build_narrate_user_content(
    prompt: str,
    concept_yaml: str,
    part_plan: dict,
    all_includes: list[str],
    is_first_part: bool,
    is_last_part: bool,
    total_parts: int,
    handoff_line: Optional[str],
    prev_part_ending: Optional[str],
) -> str:
    """
    Assemble the complete user message for one narration part call.
    """
    lines: list[str] = [prompt, "\n\n---\n\n# CONCEPT INPUT\n\n", concept_yaml]

    # Inject the subset of includes this part covers
    indexes      = part_plan.get("include_indexes", [])
    part_focus   = part_plan.get("focus", "")
    part_num     = part_plan.get("part", 1)
    part_includes = [all_includes[i] for i in indexes if i < len(all_includes)]

    lines.append("\n\n---\n\n# NARRATION SCOPE FOR THIS PART\n")
    lines.append(f"Part {part_num} of {total_parts}.")
    if part_focus:
        lines.append(f"Focus: {part_focus}")
    lines.append(f"\nCover ONLY these includes (index {indexes[0]}–{indexes[-1]} from boundary.includes):\n")
    for idx, include_text in zip(indexes, part_includes):
        lines.append(f"  [{idx}] {include_text}")

    if not is_first_part:
        lines.append("\n\n---\n\n# CONTINUATION CONTEXT\n")
        lines.append("This is a continuation. Do NOT open with an entry point.")
        lines.append("Do NOT re-introduce the concept or the analogy.")
        lines.append("Open mid-flow from the handoff line and previous ending below.\n")
        if handoff_line:
            lines.append(f"HANDOFF LINE: {handoff_line}\n")
        if prev_part_ending:
            lines.append(f"PREVIOUS PART ENDING:\n{prev_part_ending}")

    if not is_last_part:
        lines.append(
            "\n\n---\n\n# THIS IS NOT THE FINAL PART\n"
            "Do NOT write a landing line. Do NOT close the concept.\n"
            "End at a natural breath point on the last include — "
            "leave momentum for the next part."
        )
    else:
        lines.append(
            "\n\n---\n\n# THIS IS THE FINAL PART\n"
            "End with the landing line — one sentence, repeatable three months later."
        )

    return "\n".join(lines)


def run_narrate(
    spine_id: int,
    slug: str,
    concept_yaml: str,
    dry_run: bool = False,
) -> Optional[str]:
    """
    Multipart narration: plan call + N narration calls.
    Returns the combined markdown string (all parts joined with --- breaks).
    """
    out_path = narrated_path(spine_id, slug)

    if dry_run:
        print(f"  [narrate] would write → {_part_subdir(spine_id)}/{out_path.name}")
        return None

    # Phase A — plan
    parts = _plan_narration(concept_yaml, spine_id, slug)
    total = len(parts)
    concept  = _parse_concept_entry(concept_yaml)
    includes = _get_includes(concept)

    # Pull the front matter fields we need for the file header
    fm_fields = {
        "id":         concept.get("id", spine_id),
        "slug":       concept.get("slug", slug),
        "title":      concept.get("title", slug),
        "layer":      concept.get("layer", ""),
        "layer_name": concept.get("layer_name", ""),
        "exams":      concept.get("exams", []),
        "interviews": concept.get("interviews", False),
    }
    fm_yaml = yaml.dump(fm_fields, allow_unicode=True, sort_keys=False, default_flow_style=False).strip()

    narrate_prompt = _load_prompt("narrate")
    part_texts: list[str] = []
    prev_ending: Optional[str] = None

    # Phase B — one call per part
    for i, part_plan in enumerate(parts):
        is_first  = (i == 0)
        is_last   = (i == total - 1)
        part_num  = part_plan.get("part", i + 1)

        # Handoff from the previous part boundary in the plan
        if not is_first and i > 0:
            handoff = parts[i - 1].get("handoff_to_next")
        else:
            handoff = None

        user_content = _build_narrate_user_content(
            prompt           = narrate_prompt,
            concept_yaml     = concept_yaml,
            part_plan        = part_plan,
            all_includes     = includes,
            is_first_part    = is_first,
            is_last_part     = is_last,
            total_parts      = total,
            handoff_line     = handoff,
            prev_part_ending = prev_ending,
        )

        t0 = time.monotonic()
        raw, in_tok, out_tok = call_claude(user_content)
        duration = time.monotonic() - t0
        cost     = compute_cost(in_tok, out_tok)

        # Strip front matter and any accidental code fences
        raw_clean = _strip_code_fence(raw, "markdown")
        raw_clean = _strip_code_fence(raw_clean, "md")
        _, body = _strip_front_matter(raw_clean)
        part_texts.append(body.strip())
        prev_ending = _extract_last_paragraph(body)

        log_usage(
            LOG_FILE, f"narrate_p{part_num}", spine_id, slug,
            in_tok, out_tok, cost, duration, "ok",
            notes=f"part={part_num}/{total}",
        )
        print(
            f"  [narrate] part {part_num}/{total}  "
            f"{in_tok:,}→{out_tok:,} tok  ${cost:.4f}  {duration:.1f}s"
        )

    # Combine: single front matter header + parts joined by ---
    separator = "\n\n---\n\n"
    combined  = f"---\n{fm_yaml}\n---\n\n" + separator.join(part_texts)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(combined, encoding="utf-8")
    print(f"  [narrate] combined {total} part(s) → {out_path.name}")
    return combined



# ---------------------------------------------------------------------------
# Stage 4c — Curate (seam repair, in-place update)
# ---------------------------------------------------------------------------

def run_curate(
    spine_id: int,
    slug: str,
    narrated_md: str,
    dry_run: bool = False,
) -> Optional[str]:
    """
    Stage 4c — Curate.
    Repairs section-boundary seams in the narrated script.
    Updates the narrated .md file in place.
    Returns the curated markdown string.
    """
    out_path = narrated_path(spine_id, slug)

    if dry_run:
        print(f"  [curate]  would update → {_part_subdir(spine_id)}/{out_path.name}")
        return narrated_md

    fm, body = _strip_front_matter(narrated_md)
    title    = fm.get("title", slug)

    # Count sections — if 0 or 1 section, no seams to repair
    section_count = len(re.findall(r"^##\s+", body, re.MULTILINE))
    if section_count < 2:
        print(f"  [curate]  SKIP — {section_count} section(s), no seams to repair")
        return narrated_md

    prompt = _load_prompt("narration_curate")
    filled = (
        prompt
        .replace("{{TITLE}}",  title)
        .replace("{{SCRIPT}}", narrated_md)   # pass full md including front matter
    )

    t0 = time.monotonic()
    raw, in_tok, out_tok = call_claude(filled)
    duration = time.monotonic() - t0
    cost     = compute_cost(in_tok, out_tok)

    # Strip the CURATE_REPORT block before saving
    report_match = re.search(
        r"\n---\nCURATE_REPORT:.*$", raw, re.DOTALL
    )
    report_text = ""
    if report_match:
        report_text = report_match.group(0).strip()
        curated = raw[:report_match.start()].strip()
    else:
        curated = raw.strip()
        print(f"  [curate]  WARN — no CURATE_REPORT block found in output", file=sys.stderr)

    # Sanity check — curated output must have front matter
    if not curated.lstrip().startswith("---"):
        print(f"  [curate]  WARN — output missing front matter, keeping original", file=sys.stderr)
        return narrated_md

    # Parse and log the report
    notes = ""
    if report_text:
        m = re.search(r"word_delta_pct:\s*([\d.]+)%", report_text)
        if m:
            notes = f"delta={m.group(1)}%"
            delta = float(m.group(1))
            if delta > 15:
                print(f"  [curate]  WARN — word delta {delta:.1f}% exceeds 15% budget", file=sys.stderr)

    # Update the narrated file in place
    out_path.write_text(curated, encoding="utf-8")

    log_usage(LOG_FILE, "curate", spine_id, slug, in_tok, out_tok, cost, duration, "ok", notes=notes)
    print(f"  [curate]  {in_tok:,}\u2192{out_tok:,} tok  ${cost:.4f}  {duration:.1f}s  {notes}")
    return curated

# ---------------------------------------------------------------------------
# Stage 4b — Whiteboard
# ---------------------------------------------------------------------------

def run_whiteboard(
    spine_id: int,
    slug: str,
    narrated_md: str,
    dry_run: bool = False,
) -> Optional[str]:
    """
    Stage 4b — Whiteboard.
    One API call: narrated script in, self-contained interactive HTML out.
    The model draws one SVG diagram per section using the governing question:
    what would a teacher draw on the whiteboard at this moment in the lesson?
    """
    out_path = whiteboard_path(spine_id, slug)

    if dry_run:
        print(f"  [whiteboard] would write → {_part_subdir(spine_id)}/{out_path.name}")
        return None

    fm, body = _strip_front_matter(narrated_md)
    title    = fm.get("title", slug)
    layer    = str(fm.get("layer_name", fm.get("layer", "")))
    exams    = ", ".join(fm.get("exams") or [])

    prompt = _load_prompt("whiteboard")
    filled = (
        prompt
        .replace("{{TITLE}}",  title)
        .replace("{{LAYER}}",  layer)
        .replace("{{EXAMS}}",  exams)
        .replace("{{SCRIPT}}", body)
    )

    t0 = time.monotonic()
    # SVG whiteboards are verbose. Use 32k tokens to avoid truncation.
    raw, in_tok, out_tok = call_claude(filled, max_tokens=32000)
    duration = time.monotonic() - t0
    cost     = compute_cost(in_tok, out_tok)

    frag = _strip_code_fence(raw, "html")

    # Detect truncation: a complete document ends with </html>
    if not frag.rstrip().lower().endswith("</html>"):
        print(f"  [whiteboard] WARN — output appears truncated (does not end with </html>)", file=sys.stderr)
        print(f"  [whiteboard] WARN — out_tok={out_tok} — consider reducing panel count or script length", file=sys.stderr)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(frag, encoding="utf-8")

    log_usage(LOG_FILE, "whiteboard", spine_id, slug, in_tok, out_tok, cost, duration, "ok")
    print(f"  [whiteboard] {in_tok:,}→{out_tok:,} tok  ${cost:.4f}  {duration:.1f}s  → {out_path.name}")
    return frag

# Stage 5 — Render
# ---------------------------------------------------------------------------


def run_render(spine_id: int, slug: str, narrated_md: str, dry_run: bool = False) -> Optional[str]:
    out_path = rendered_path(spine_id, slug)

    if dry_run:
        print(f"  [render]  would write → {_part_subdir(spine_id)}/{out_path.name}")
        return None

    fm, body = _strip_front_matter(narrated_md)
    title    = fm.get("title", slug)
    layer    = str(fm.get("layer", ""))
    exams    = ", ".join(fm.get("exams") or [])


    prompt = _load_prompt("render")
    filled = (
        prompt
        .replace("{{TITLE}}",    title)
        .replace("{{LAYER}}",    layer)
        .replace("{{EXAMS}}",    exams)
        .replace("{{MARKDOWN}}", body)
    )

    t0 = time.monotonic()
    raw, in_tok, out_tok = call_claude(filled)
    duration = time.monotonic() - t0
    cost     = compute_cost(in_tok, out_tok)

    html = _strip_code_fence(raw, "html")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

    log_usage(LOG_FILE, "render", spine_id, slug, in_tok, out_tok, cost, duration, "ok")
    print(f"  [render]  {in_tok:,}→{out_tok:,} tok  ${cost:.4f}  {duration:.1f}s  → {out_path.name}")
    return html


def _strip_code_fence(text: str, lang: str = "") -> str:
    text = text.strip()
    text = re.sub(rf"^```{lang}\s*\n?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\n?```\s*$", "", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Stage 6 — Publish (HTML → PDF)
# ---------------------------------------------------------------------------

def run_publish_one(spine_id: int, slug: str, dry_run: bool = False, overwrite: bool = False) -> None:
    html_path = rendered_path(spine_id, slug)
    pdf_path  = published_path(spine_id, slug)

    if not html_path.exists():
        print(f"  [publish] SKIP — no HTML (run render first): {slug}", file=sys.stderr)
        return

    if not overwrite and pdf_path.exists() and html_path.stat().st_mtime <= pdf_path.stat().st_mtime:
        print(f"  [publish] SKIP — PDF up to date: {slug}")
        log_usage(LOG_FILE, "publish", spine_id, slug, status="skip", cost_usd=0)
        return

    if dry_run:
        print(f"  [publish] would write → {pdf_path.name}")
        return

    try:
        from weasyprint import HTML as WeasyprintHTML
        logging.getLogger("weasyprint").setLevel(
            getattr(logging, config.pdf.weasyprint_log_level, logging.ERROR)
        )
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        t0 = time.monotonic()
        WeasyprintHTML(filename=str(html_path)).write_pdf(
            target=str(pdf_path),
            presentational_hints=True,
        )
        duration = time.monotonic() - t0
        print(f"  [publish] {pdf_path.name}  {duration:.1f}s")
        log_usage(LOG_FILE, "publish", spine_id, slug, duration_s=duration, status="ok", cost_usd=0)
    except Exception as e:
        print(f"  [publish] ERROR {slug}: {e}", file=sys.stderr)
        log_usage(LOG_FILE, "publish", spine_id, slug, status="error", notes=str(e)[:200])


def run_combine(dry_run: bool = False) -> None:
    """Build per-layer combined PDFs and/or one complete PDF."""
    try:
        from pypdf import PdfWriter
    except ImportError:
        print("[error] pypdf not installed: pip install pypdf", file=sys.stderr)
        sys.exit(1)

    layer_names = {
        1: "foundations", 2: "core_mechanisms", 3: "service_mastery",
        4: "decision_patterns", 5: "architectural_patterns", 6: "exam_bridges",
    }
    ind_dir = config.paths.output_published_dir / config.pdf.individual_subdir
    com_dir = combined_dir()
    com_dir.mkdir(parents=True, exist_ok=True)

    # Glob recursively — PDFs are now nested under layer/part subfolders
    all_pdfs: list[Path] = sorted(ind_dir.rglob("*.pdf"))
    if not all_pdfs:
        print("[combine] No individual PDFs found. Run --publish first.")
        return

    spines_by_id = {s["id"]: s for s in _load_spines()}
    layer_pdfs: dict[int, list[Path]] = {i: [] for i in range(1, 7)}

    for pdf_path in all_pdfs:
        m = re.match(r"^(\d+)_", pdf_path.name)
        if m:
            sid   = int(m.group(1))
            spine = spines_by_id.get(sid)
            if spine:
                layer_pdfs[spine["layer"]].append(pdf_path)

    if config.pdf.combined_by_layer:
        for layer, pdfs in layer_pdfs.items():
            if not pdfs:
                continue
            out = com_dir / f"layer_{layer}_{layer_names[layer]}.pdf"
            if dry_run:
                print(f"  [combine] would write → {out.name}  ({len(pdfs)} PDFs)")
                continue
            writer = PdfWriter()
            for p in sorted(pdfs):
                writer.append(str(p))
            with open(out, "wb") as f:
                writer.write(f)
            print(f"  [combine] {out.name}  ({len(pdfs)} PDFs)")

    if config.pdf.combined_complete:
        out = com_dir / "aws_concept_mastery_complete.pdf"
        if dry_run:
            print(f"  [combine] would write → {out.name}  ({len(all_pdfs)} PDFs total)")
            return
        writer = PdfWriter()
        for p in sorted(all_pdfs):
            writer.append(str(p))
        with open(out, "wb") as f:
            writer.write(f)
        print(f"  [combine] {out.name}  ({len(all_pdfs)} PDFs total)")


# ---------------------------------------------------------------------------
# Main pipeline loop
# ---------------------------------------------------------------------------

def _sum_spine_cost(log_file: Path, spine_id: int, bytes_before: int) -> float:
    """
    Sum the cost_usd column for all log entries written for this spine
    since bytes_before in the log file. Uses csv.DictReader for robustness.
    """
    if not log_file.exists():
        return 0.0
    try:
        import csv as _csv
        text = log_file.read_text(encoding="utf-8")
        new_text = text[bytes_before:]
        if not new_text.strip():
            return 0.0
        # Prepend header if the new chunk doesn't start with it
        if not new_text.startswith("timestamp"):
            header_end = text.index("\n") + 1
            header = text[:header_end]
            new_text = header + new_text
        total = 0.0
        for row in _csv.DictReader(new_text.splitlines(), delimiter="\t"):
            try:
                if int(row.get("spine_id", -1)) == spine_id:
                    total += float(row.get("cost_usd", 0) or 0)
            except (ValueError, TypeError):
                pass
        return total
    except Exception:
        return 0.0



def process_spine(
    spine: dict,
    start_stage: str,
    resume: bool,
    overwrite: bool,
    dry_run: bool,
) -> None:
    spine_id = spine["id"]
    slug     = spine["slug"]

    if spine.get("approved") is False:
        print(f"[{spine_id:04d}] {slug}  SKIP (approved: false)")
        log_usage(LOG_FILE, "skip", spine_id, slug, status="skip")
        return

    start_idx  = STAGE_INDEXES.get(start_stage, 0)
    part_label = _part_subdir(spine_id)
    t_spine_start = time.monotonic()
    print(f"\n[{spine_id:04d}] {slug}  ({part_label})")

    # Track total cost for this spine by reading the log before and after
    _log_size_before = LOG_FILE.stat().st_size if LOG_FILE.exists() else 0

    try:
        # ── Stage 3: Expand ────────────────────────────────────────────────
        concept_yaml: Optional[str] = None
        if start_idx <= STAGE_INDEXES["expand"]:
            out = concept_path(spine_id, slug)
            if not overwrite and resume and out.exists():
                print(f"  [expand]  SKIP (exists)")
                concept_yaml = out.read_text(encoding="utf-8")
            else:
                if overwrite and out.exists():
                    print(f"  [expand]  OVERWRITE")
                concept_yaml = run_expand(spine, dry_run=dry_run)
        else:
            out = concept_path(spine_id, slug)
            if out.exists():
                concept_yaml = out.read_text(encoding="utf-8")
            else:
                print(f"  [expand]  MISSING — run expand first", file=sys.stderr)
                return

        # ── Stage 4: Narrate ───────────────────────────────────────────────
        narrated_md: Optional[str] = None
        if start_idx <= STAGE_INDEXES["narrate"]:
            out = narrated_path(spine_id, slug)
            if not overwrite and resume and out.exists():
                print(f"  [narrate] SKIP (exists)")
                narrated_md = out.read_text(encoding="utf-8")
            else:
                if overwrite and out.exists():
                    print(f"  [narrate] OVERWRITE")
                if concept_yaml:
                    narrated_md = run_narrate(spine_id, slug, concept_yaml, dry_run=dry_run)
        else:
            out = narrated_path(spine_id, slug)
            if out.exists():
                narrated_md = out.read_text(encoding="utf-8")
            else:
                print(f"  [narrate] MISSING — run narrate first", file=sys.stderr)
                return

        # ── Stage 4c: Curate ───────────────────────────────────────────────
        if start_idx <= STAGE_INDEXES["curate"]:
            if not overwrite and resume and narrated_path(spine_id, slug).exists():
                # Check if already curated by comparing mtime — if narrated
                # file hasn't changed since last curate, skip
                pass  # always re-curate when in range unless resume skips narrate too
            if narrated_md:
                narrated_md = run_curate(spine_id, slug, narrated_md, dry_run=dry_run)

        # ── Stage 5: Render ────────────────────────────────────────────────
        if start_idx <= STAGE_INDEXES["render"]:
            out = rendered_path(spine_id, slug)
            if not overwrite and resume and out.exists():
                print(f"  [render]  SKIP (exists)")
            else:
                if overwrite and out.exists():
                    print(f"  [render]  OVERWRITE")
                if narrated_md:
                    run_render(spine_id, slug, narrated_md, dry_run=dry_run)



        # ── Spine cost summary ─────────────────────────────────────────────
        t_spine_total = time.monotonic() - t_spine_start
        spine_cost = _sum_spine_cost(LOG_FILE, spine_id, _log_size_before)
        print(f"  {'─'*50}")
        print(f"  [{spine_id:04d}] total  {t_spine_total:.0f}s  ${spine_cost:.4f}")

    except Exception as e:
        print(f"  [error] {slug}: {e}", file=sys.stderr)
        log_usage(LOG_FILE, "error", spine_id, slug, status="error", notes=str(e)[:200])


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stages 3–6 — Expand, Narrate (multipart), Render, Publish"
    )

    target = parser.add_mutually_exclusive_group()
    target.add_argument("--spine",  type=int, metavar="N",
                        help="Single spine ID")
    target.add_argument("--spines", type=int, nargs="+", metavar="N",
                        help="One or more spine IDs: --spines 47 755 802")
    target.add_argument("--layer",  type=int, metavar="N",
                        help="All spines in layer N")
    target.add_argument("--all",    action="store_true",
                        help="All spines")

    parser.add_argument("--from", type=int, dest="from_id", metavar="N",
                        help="Range start (inclusive spine ID)")
    parser.add_argument("--to",   type=int, dest="to_id",   metavar="N",
                        help="Range end (inclusive spine ID)")
    parser.add_argument("--start-stage", choices=STAGES, default="expand")
    parser.add_argument("--resume",    action="store_true")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing concept, narrated, and rendered files")
    parser.add_argument("--dry-run",   action="store_true")
    parser.add_argument("--combine",  action="store_true")
    parser.add_argument("--complete", action="store_true")

    args = parser.parse_args()
    config.paths.logs_dir.mkdir(parents=True, exist_ok=True)

    if args.combine or args.complete:
        run_combine(dry_run=args.dry_run)
        return

    spines = _select_spines(args)
    total  = len(spines)

    if total == 0:
        print("[warn] No spines matched the selection criteria.")
        return

    print(f"\n{'─' * 60}")
    print(f"  run.py — {total} spine(s)")
    print(f"  Start stage : {args.start_stage}")
    if len(spines) == 1:
        print(f"  Output path : {_part_subdir(spines[0]['id'])}/")
    else:
        print(f"  Output path : layer_N/part_N/ (nested per spine)")
    if args.resume:    print("  Resume      : on")
    if args.overwrite: print("  Overwrite   : on — existing files will be replaced")
    if args.dry_run:   print("  DRY RUN     : no API calls")
    print(f"{'─' * 60}")

    for spine in spines:
        process_spine(
            spine       = spine,
            start_stage = args.start_stage,
            resume      = args.resume,
            overwrite   = args.overwrite,
            dry_run     = args.dry_run,
        )

    print(f"\n{'─' * 60}")
    print(f"  Done — {total} spine(s) | log: {LOG_FILE}")
    print(f"{'─' * 60}\n")


if __name__ == "__main__":
    main()