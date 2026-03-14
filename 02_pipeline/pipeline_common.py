"""
02_pipeline/pipeline_common.py
Shared helpers used by run.py, run_whiteboard.py, and run_publish.py.

Keeping shared code here avoids circular imports that occur when
run_whiteboard.py and run_publish.py try to import from run.py.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.config import config, syllabus_outline_plan


# ---------------------------------------------------------------------------
# Part-folder derivation from syllabus outline_plan
# ---------------------------------------------------------------------------

_PART_INDEX: dict[int, str] | None = None


def _build_part_index() -> dict[int, str]:
    """
    Build a mapping: spine_id -> 'phase_N/part_N' from the syllabus outline_plan.
    Each outline_plan entry specifies call_name (contains 'Phase X Part Y'),
    start_id, and target_count.
    """
    index: dict[int, str] = {}
    for call_name, _area, start_id, target in syllabus_outline_plan():
        # Parse "Phase X Part Y" from the call name
        m = re.match(r"Phase\s+(\d+)\s+Part\s+(\d+)", call_name, re.IGNORECASE)
        if m:
            folder = f"phase_{int(m.group(1))}/part_{int(m.group(2))}"
        else:
            # Fallback: slugify the call name prefix
            prefix = call_name.split(":")[0].strip().lower()
            folder = re.sub(r"[^a-z0-9]+", "_", prefix).strip("_")
        for sid in range(start_id, start_id + target):
            index[sid] = folder
    return index


def _part_subdir(spine_id: int) -> str:
    """Return e.g. 'phase_3/part_7' for a given spine_id."""
    global _PART_INDEX
    if _PART_INDEX is None:
        _PART_INDEX = _build_part_index()
    if spine_id not in _PART_INDEX:
        raise ValueError(
            f"spine_id={spine_id} not found in syllabus outline_plan. "
            "Check input/syllabus.yaml outline_plan entries."
        )
    return _PART_INDEX[spine_id]


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

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
      --layer N          all spines in a phase (--layer kept as CLI shorthand)
      --all              every spine
    """
    if getattr(args, "spine", None) is not None:
        return [_get_spine(args.spine)]

    if getattr(args, "spines", None):
        return [_get_spine(sid) for sid in args.spines]

    all_spines = _load_spines()

    if getattr(args, "layer", None) is not None:
        all_spines = [s for s in all_spines if s.get("phase") == args.layer]

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
