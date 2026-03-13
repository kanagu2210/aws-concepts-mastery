"""
02_pipeline/run.py
Stages 3–6 — Expand, Narrate, Render, and optionally Publish each spine.

Usage:
    python 02_pipeline/run.py --spine 47
    python 02_pipeline/run.py --from 1 --to 50
    python 02_pipeline/run.py --layer 2
    python 02_pipeline/run.py --all

    # Control which stages run
    python 02_pipeline/run.py --spine 47 --start-stage narrate
    python 02_pipeline/run.py --spine 47 --publish        # also run publish (stage 6)

    # Resume / dry-run
    python 02_pipeline/run.py --all --resume
    python 02_pipeline/run.py --from 1 --to 50 --dry-run

    # PDF modes (require individual PDFs to already exist)
    python 02_pipeline/run.py --combine     # combine per layer
    python 02_pipeline/run.py --complete    # single complete PDF

Default stages: expand → narrate → render (no publish)
Publish is opt-in: --publish flag or --combine / --complete
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
import time
from pathlib import Path
from typing import Optional

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.api import call_claude
from utils.config import config
from utils.usage_log import compute_cost, log_usage

# ---------------------------------------------------------------------------
# Stage constants
# ---------------------------------------------------------------------------
STAGES        = ["expand", "narrate", "render"]
STAGE_INDEXES = {s: i for i, s in enumerate(STAGES)}

LOG_FILE = config.paths.logs_dir / "usage_run.tsv"


# ---------------------------------------------------------------------------
# File path helpers
# ---------------------------------------------------------------------------

def concept_path(spine_id: int, slug: str) -> Path:
    return config.paths.output_concepts_dir / f"{spine_id:04d}_{slug}.yaml"

def narrated_path(spine_id: int, slug: str) -> Path:
    return config.paths.output_narrated_dir / f"{spine_id:04d}_{slug}.md"

def rendered_path(spine_id: int, slug: str) -> Path:
    return config.paths.output_rendered_dir / f"{spine_id:04d}_{slug}.html"

def published_path(spine_id: int, slug: str) -> Path:
    return (
        config.paths.output_published_dir
        / config.pdf.individual_subdir
        / f"{spine_id:04d}_{slug}.pdf"
    )

def combined_dir() -> Path:
    return config.paths.output_published_dir / config.pdf.combined_subdir


# ---------------------------------------------------------------------------
# Load helpers
# ---------------------------------------------------------------------------

def _load_spines(layer_filter: Optional[int] = None) -> list[dict]:
    spines_path = config.paths.input_dir / "concept_spines.yaml"
    if not spines_path.exists():
        print(f"[error] {spines_path} not found. Run run_outline.py first.", file=sys.stderr)
        sys.exit(1)
    raw = yaml.safe_load(spines_path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        print("[error] concept_spines.yaml must be a list.", file=sys.stderr)
        sys.exit(1)
    spines = raw
    if layer_filter is not None:
        spines = [s for s in spines if s.get("layer") == layer_filter]
    return spines


def _get_spine(spine_id: int) -> dict:
    for s in _load_spines():
        if s.get("id") == spine_id:
            return s
    print(f"[error] Spine id={spine_id} not found in concept_spines.yaml", file=sys.stderr)
    sys.exit(1)


def _select_spines(args: argparse.Namespace) -> list[dict]:
    if args.spine is not None:
        return [_get_spine(args.spine)]
    all_spines = _load_spines()
    if args.layer is not None:
        all_spines = [s for s in all_spines if s.get("layer") == args.layer]
    if getattr(args, "from_id", None) is not None:
        all_spines = [s for s in all_spines if s.get("id") >= args.from_id]
    if getattr(args, "to_id", None) is not None:
        all_spines = [s for s in all_spines if s.get("id") <= args.to_id]
    if not args.all and args.spine is None and args.layer is None \
            and getattr(args, "from_id", None) is None:
        print("[error] Specify a target: --spine N, --from/--to, --layer N, or --all", file=sys.stderr)
        sys.exit(1)
    return all_spines


def _load_prompt(name: str) -> str:
    path = config.paths.prompts_dir / f"{name}_prompt.md"
    if not path.exists():
        raise FileNotFoundError(f"Prompt not found: {path}")
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Stage 3 — Expand
# ---------------------------------------------------------------------------

def run_expand(spine: dict, dry_run: bool = False) -> Optional[str]:
    """
    Call Claude with the expand prompt + raw spine YAML.
    Returns the expanded YAML string, or None on skip/error.
    """
    spine_id = spine["id"]
    slug     = spine["slug"]
    out_path = concept_path(spine_id, slug)

    if dry_run:
        print(f"  [expand] would write → {out_path.name}")
        return None

    prompt = _load_prompt("expand")
    user_content = yaml.dump([spine], allow_unicode=True, sort_keys=False, default_flow_style=False)

    t0 = time.monotonic()
    raw, in_tok, out_tok = call_claude(
        f"{prompt}\n\n---\n\n# SPINE INPUT\n\n{user_content}"
    )
    duration = time.monotonic() - t0
    cost = compute_cost(in_tok, out_tok)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(raw, encoding="utf-8")

    log_usage(LOG_FILE, "expand", spine_id, slug, in_tok, out_tok, cost, duration, "ok")
    print(f"  [expand]  {in_tok:,}→{out_tok:,} tok  ${cost:.4f}  {duration:.1f}s  → {out_path.name}")
    return raw


# ---------------------------------------------------------------------------
# Stage 4 — Narrate
# ---------------------------------------------------------------------------

def run_narrate(spine_id: int, slug: str, concept_yaml: str, dry_run: bool = False) -> Optional[str]:
    """
    Call Claude with the narrate prompt + expanded concept YAML.
    Returns the narrated markdown string, or None on skip/error.
    """
    out_path = narrated_path(spine_id, slug)

    if dry_run:
        print(f"  [narrate] would write → {out_path.name}")
        return None

    prompt = _load_prompt("narrate")
    t0 = time.monotonic()
    raw, in_tok, out_tok = call_claude(
        f"{prompt}\n\n---\n\n# CONCEPT INPUT\n\n{concept_yaml}"
    )
    duration = time.monotonic() - t0
    cost = compute_cost(in_tok, out_tok)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(raw, encoding="utf-8")

    log_usage(LOG_FILE, "narrate", spine_id, slug, in_tok, out_tok, cost, duration, "ok")
    print(f"  [narrate] {in_tok:,}→{out_tok:,} tok  ${cost:.4f}  {duration:.1f}s  → {out_path.name}")
    return raw


# ---------------------------------------------------------------------------
# Stage 5 — Render
# ---------------------------------------------------------------------------

def _parse_front_matter(md: str) -> tuple[dict, str]:
    """
    Split YAML front matter from markdown body.
    Returns (front_matter_dict, body_text).
    """
    if not md.startswith("---"):
        return {}, md
    end = md.find("\n---", 3)
    if end == -1:
        return {}, md
    fm_text = md[3:end].strip()
    body    = md[end + 4:].strip()
    fm      = yaml.safe_load(fm_text) or {}
    return fm, body


def run_render(spine_id: int, slug: str, narrated_md: str, dry_run: bool = False) -> Optional[str]:
    """
    Inject TITLE/LAYER/EXAMS/MARKDOWN into render_prompt and call Claude.
    Returns the HTML string, or None on skip/error.
    """
    out_path = rendered_path(spine_id, slug)

    if dry_run:
        print(f"  [render]  would write → {out_path.name}")
        return None

    fm, body = _parse_front_matter(narrated_md)
    title = fm.get("title", slug)
    layer = str(fm.get("layer", ""))
    exams = ", ".join(fm.get("exams", []))

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
    cost = compute_cost(in_tok, out_tok)

    # Strip accidental markdown fences if model added them
    html = _strip_fences(raw, "html")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

    log_usage(LOG_FILE, "render", spine_id, slug, in_tok, out_tok, cost, duration, "ok")
    print(f"  [render]  {in_tok:,}→{out_tok:,} tok  ${cost:.4f}  {duration:.1f}s  → {out_path.name}")
    return html


def _strip_fences(text: str, lang: str = "") -> str:
    """Remove ```html / ``` wrappers if the model added them."""
    text = text.strip()
    fence_open  = re.compile(rf"^```{lang}\s*\n?", re.IGNORECASE)
    fence_close = re.compile(r"\n?```\s*$")
    text = fence_open.sub("", text)
    text = fence_close.sub("", text)
    return text.strip()


# ---------------------------------------------------------------------------
# Stage 6 — Publish (HTML → PDF via WeasyPrint)
# ---------------------------------------------------------------------------

def run_publish_one(spine_id: int, slug: str, dry_run: bool = False) -> None:
    """Convert one HTML file to one PDF. Skip if PDF is up to date."""
    html_path = rendered_path(spine_id, slug)
    pdf_path  = published_path(spine_id, slug)

    if not html_path.exists():
        print(f"  [publish] SKIP {slug} — no HTML file (run render first)", file=sys.stderr)
        return

    if pdf_path.exists() and html_path.stat().st_mtime <= pdf_path.stat().st_mtime:
        print(f"  [publish] SKIP {slug} — PDF up to date")
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
    """Build per-layer combined PDFs and optionally one complete PDF."""
    try:
        from pypdf import PdfWriter
    except ImportError:
        print("[error] pypdf not installed. Run: pip install pypdf", file=sys.stderr)
        sys.exit(1)

    ind_dir = config.paths.output_published_dir / config.pdf.individual_subdir
    com_dir = combined_dir()
    com_dir.mkdir(parents=True, exist_ok=True)

    layer_names = {
        1: "foundations",
        2: "core_mechanisms",
        3: "service_mastery",
        4: "decision_patterns",
        5: "architectural_patterns",
        6: "exam_bridges",
    }

    all_pdfs: list[Path] = sorted(ind_dir.glob("*.pdf"))
    if not all_pdfs:
        print("[combine] No individual PDFs found. Run --publish first.")
        return

    # Map PDFs to layers by loading spines
    spines_by_id = {s["id"]: s for s in _load_spines()}

    layer_pdfs: dict[int, list[Path]] = {i: [] for i in range(1, 7)}
    for pdf_path in all_pdfs:
        # Extract id from filename e.g. 0047_slug.pdf
        match = re.match(r"^(\d+)_", pdf_path.name)
        if match:
            sid = int(match.group(1))
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
            print(f"  [combine] would write → {out.name}  ({len(all_pdfs)} PDFs)")
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

def process_spine(
    spine: dict,
    start_stage: str,
    do_publish: bool,
    resume: bool,
    dry_run: bool,
) -> None:
    spine_id = spine["id"]
    slug     = spine["slug"]

    # Skip if approved: false
    if spine.get("approved") is False:
        print(f"[{spine_id:04d}] {slug}  SKIP (approved: false)")
        log_usage(LOG_FILE, "skip", spine_id, slug, status="skip")
        return

    start_idx = STAGE_INDEXES.get(start_stage, 0)
    print(f"\n[{spine_id:04d}] {slug}")

    try:
        # ── Stage 3: Expand ────────────────────────────────────────────────
        concept_yaml: Optional[str] = None
        if start_idx <= STAGE_INDEXES["expand"]:
            out = concept_path(spine_id, slug)
            if resume and out.exists():
                print(f"  [expand]  SKIP (file exists)")
                concept_yaml = out.read_text(encoding="utf-8")
            else:
                concept_yaml = run_expand(spine, dry_run=dry_run)
        else:
            # Starting after expand — load existing file
            out = concept_path(spine_id, slug)
            if out.exists():
                concept_yaml = out.read_text(encoding="utf-8")
            else:
                print(f"  [expand]  MISSING — cannot start at '{start_stage}' without it", file=sys.stderr)
                return

        # ── Stage 4: Narrate ───────────────────────────────────────────────
        narrated_md: Optional[str] = None
        if start_idx <= STAGE_INDEXES["narrate"]:
            out = narrated_path(spine_id, slug)
            if resume and out.exists():
                print(f"  [narrate] SKIP (file exists)")
                narrated_md = out.read_text(encoding="utf-8")
            elif concept_yaml:
                narrated_md = run_narrate(spine_id, slug, concept_yaml, dry_run=dry_run)
        else:
            out = narrated_path(spine_id, slug)
            if out.exists():
                narrated_md = out.read_text(encoding="utf-8")
            else:
                print(f"  [narrate] MISSING — cannot start at '{start_stage}' without it", file=sys.stderr)
                return

        # ── Stage 5: Render ────────────────────────────────────────────────
        if start_idx <= STAGE_INDEXES["render"]:
            out = rendered_path(spine_id, slug)
            if resume and out.exists():
                print(f"  [render]  SKIP (file exists)")
            elif narrated_md:
                run_render(spine_id, slug, narrated_md, dry_run=dry_run)

        # ── Stage 6: Publish ───────────────────────────────────────────────
        if do_publish:
            run_publish_one(spine_id, slug, dry_run=dry_run)

    except Exception as e:
        print(f"  [error] {slug}: {e}", file=sys.stderr)
        log_usage(LOG_FILE, "error", spine_id, slug, status="error", notes=str(e)[:200])


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stages 3–6 — Expand, Narrate, Render, Publish"
    )

    # Selection
    target = parser.add_mutually_exclusive_group()
    target.add_argument("--spine",  type=int, metavar="N", help="Process one spine by ID")
    target.add_argument("--layer",  type=int, metavar="N", help="Process all spines in a layer (1–6)")
    target.add_argument("--all",    action="store_true",   help="Process all spines")

    parser.add_argument("--from",   type=int, dest="from_id", metavar="N", help="Start of ID range")
    parser.add_argument("--to",     type=int, dest="to_id",   metavar="N", help="End of ID range (inclusive)")

    # Stage control
    parser.add_argument(
        "--start-stage",
        choices=STAGES,
        default="expand",
        help="Stage to start from (default: expand)"
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Also run Stage 6 (HTML → PDF) for each spine"
    )

    # Modes
    parser.add_argument("--resume",  action="store_true", help="Skip spines with existing output files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would run without calling the API")

    # PDF-only modes
    parser.add_argument("--combine",  action="store_true", help="Build combined PDFs by layer")
    parser.add_argument("--complete", action="store_true", help="Build single complete PDF")

    args = parser.parse_args()

    config.paths.logs_dir.mkdir(parents=True, exist_ok=True)

    # ── PDF-only modes ──────────────────────────────────────────────────────
    if args.combine or args.complete:
        run_combine(dry_run=args.dry_run)
        return

    # ── Normal pipeline ─────────────────────────────────────────────────────
    spines = _select_spines(args)
    total  = len(spines)

    if total == 0:
        print("[warn] No spines matched the selection criteria.")
        return

    print(f"\n{'─' * 60}")
    print(f"  run.py — {total} spine(s) selected")
    print(f"  Start stage: {args.start_stage}")
    if args.publish:
        print("  Publish: enabled")
    if args.resume:
        print("  Resume: on — existing outputs will be skipped")
    if args.dry_run:
        print("  DRY RUN — no API calls or file writes")
    print(f"{'─' * 60}")

    for spine in spines:
        process_spine(
            spine       = spine,
            start_stage = args.start_stage,
            do_publish  = args.publish,
            resume      = args.resume,
            dry_run     = args.dry_run,
        )

    print(f"\n{'─' * 60}")
    print(f"  Done — {total} spine(s) processed")
    print(f"  Log: {LOG_FILE}")
    print(f"{'─' * 60}\n")


if __name__ == "__main__":
    main()