"""
02_pipeline/pipeline_common.py
Shared helpers used by run.py, run_whiteboard.py, and run_publish.py.

Keeping shared code here avoids circular imports that occur when
run_whiteboard.py and run_publish.py try to import from run.py.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.call_plan import get_part_folder
from utils.config import config


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def _part_subdir(spine_id: int) -> str:
    """Return e.g. 'layer_3/part_7' for a given spine_id."""
    return get_part_folder(spine_id)


def concept_path(spine_id: int, slug: str) -> Path:
    return config.paths.output_concepts_dir / _part_subdir(spine_id) / f"{spine_id:04d}_{slug}.yaml"


def narrated_path(spine_id: int, slug: str) -> Path:
    return config.paths.output_narrated_dir / _part_subdir(spine_id) / f"{spine_id:04d}_{slug}.md"


def whiteboard_path(spine_id: int, slug: str) -> Path:
    return config.paths.output_whiteboard_dir / _part_subdir(spine_id) / f"{spine_id:04d}_{slug}.html"


def rendered_path(spine_id: int, slug: str) -> Path:
    return config.paths.output_rendered_dir / _part_subdir(spine_id) / f"{spine_id:04d}_{slug}.html"


def merged_path(spine_id: int, slug: str) -> Path:
    return config.paths.output_merged_dir / _part_subdir(spine_id) / f"{spine_id:04d}_{slug}.html"


def published_path(spine_id: int, slug: str) -> Path:
    return (
        config.paths.output_published_dir
        / config.pdf.individual_subdir
        / _part_subdir(spine_id)
        / f"{spine_id:04d}_{slug}.pdf"
    )


def combined_dir() -> Path:
    return config.paths.output_published_dir / config.pdf.combined_subdir


# ---------------------------------------------------------------------------
# Spine loading
# ---------------------------------------------------------------------------

def _load_spines() -> list[dict]:
    spines_path = config.paths.input_dir / "concept_spines.yaml"
    if not spines_path.exists():
        print(f"[error] {spines_path} not found. Run run_outline.py first.", file=sys.stderr)
        sys.exit(1)
    raw = yaml.safe_load(spines_path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        print("[error] concept_spines.yaml must be a list.", file=sys.stderr)
        sys.exit(1)
    return raw


def _get_spine(spine_id: int) -> dict:
    for s in _load_spines():
        if s.get("id") == spine_id:
            return s
    print(f"[error] Spine id={spine_id} not found.", file=sys.stderr)
    sys.exit(1)


def _select_spines(args: argparse.Namespace) -> list[dict]:
    """
    Resolve CLI selection arguments to a list of spine dicts.

    Supported selections (combinable):
      --spine N          single spine by ID
      --spines N N N     multiple spine IDs
      --from N --to N    inclusive ID range (either bound optional)
      --layer N          all spines in a layer
      --all              every spine
    """
    if getattr(args, "spine", None) is not None:
        return [_get_spine(args.spine)]

    if getattr(args, "spines", None):
        return [_get_spine(sid) for sid in args.spines]

    all_spines = _load_spines()

    if getattr(args, "layer", None) is not None:
        all_spines = [s for s in all_spines if s.get("layer") == args.layer]

    from_id = getattr(args, "from_id", None)
    to_id   = getattr(args, "to_id",   None)
    if from_id is not None:
        all_spines = [s for s in all_spines if s.get("id") >= from_id]
    if to_id is not None:
        all_spines = [s for s in all_spines if s.get("id") <= to_id]

    has_range = from_id is not None or to_id is not None
    has_layer = getattr(args, "layer", None) is not None
    has_all   = getattr(args, "all", False)

    if not has_all and not has_layer and not has_range:
        print(
            "[error] Specify a target: --spine N | --spines N N ... | "
            "--from N --to N | --layer N | --all",
            file=sys.stderr,
        )
        sys.exit(1)

    return all_spines


# ---------------------------------------------------------------------------
# Markdown helpers
# ---------------------------------------------------------------------------

def _strip_front_matter(md: str) -> tuple[dict, str]:
    """Split YAML front matter from body. Returns (fm_dict, body)."""
    if not md.lstrip().startswith("---"):
        return {}, md
    start = md.index("---")
    rest  = md[start + 3:]
    end   = rest.find("\n---")
    if end == -1:
        return {}, md
    fm_text = rest[:end].strip()
    body    = rest[end + 4:].strip()
    fm      = yaml.safe_load(fm_text) or {}
    return fm, body