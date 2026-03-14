"""
02_pipeline/run_curate.py
Stage 2 — Validate concept_spines.yaml and print a curation report.

Makes NO API calls. Writes NOTHING to concept_spines.yaml.
All output is to stdout only. You edit the yaml file manually after reviewing.

Usage:
    python 02_pipeline/run_curate.py              # full report
    python 02_pipeline/run_curate.py --layer 3    # filter to one layer
    python 02_pipeline/run_curate.py --fix        # show only problems (no coverage table)
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.config import (
    config,
    syllabus,
    syllabus_phase_names,
    syllabus_milestone_tags,
    syllabus_allowed_areas,
)

# ---------------------------------------------------------------------------
# Derive allowed values from syllabus
# ---------------------------------------------------------------------------
_spine_fields      = syllabus.get("concept_schema", {})
ALLOWED_SPINE_TYPES     = set(_spine_fields.get("allowed_types", []))
ALLOWED_CONCEPT_TIERS   = set(_spine_fields.get("allowed_tiers", []))
ALLOWED_COGNITIVE_ROLES = set(_spine_fields.get("allowed_roles", []))
ALLOWED_MILESTONES           = set(syllabus_milestone_tags())
ALLOWED_AREAS         = syllabus_allowed_areas()

PHASE_NAMES = syllabus_phase_names()
PHASE_TARGETS = {
    int(k): v.get("target_count", 0)
    for k, v in syllabus.get("phases", {}).items()
}

# Build layer-type rules from syllabus
_PHASE_REQUIRED_TYPES: dict[int, set[str]] = {}
_PHASE_ALLOWED_TYPES: dict[int, set[str]] = {}
for _lnum, _linfo in syllabus.get("phases", {}).items():
    _lnum = int(_lnum)
    if "required_types" in _linfo:
        _PHASE_REQUIRED_TYPES[_lnum] = set(_linfo["required_types"])
    elif "allowed_types" in _linfo:
        _PHASE_ALLOWED_TYPES[_lnum] = set(_linfo["allowed_types"])

SERVICE_FIELD = _spine_fields.get("entity_field", "service")

REQUIRED_FIELDS = [
    "id", "slug", "title", "phase", "phase_name",
    "concept_type", "milestones", "applied", "area",
    SERVICE_FIELD, "concept_tier", "cognitive_role",
    "core_idea", "notes",
]


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_spine(spine: dict, index: int) -> list[str]:
    """Return a list of problem descriptions for one spine. Empty = clean."""
    problems: list[str] = []
    sid = spine.get("id", f"[index {index}]")
    prefix = f"id={sid}"

    # Required fields present
    for field_name in REQUIRED_FIELDS:
        if field_name not in spine:
            problems.append(f"{prefix}: missing field '{field_name}'")

    # Field value checks
    if spine.get("concept_type") not in ALLOWED_SPINE_TYPES:
        problems.append(f"{prefix}: invalid concept_type '{spine.get('concept_type')}'")

    if not isinstance(spine.get("milestones"), list) or not spine.get("milestones"):
        problems.append(f"{prefix}: 'milestones' must be a non-empty list")
    else:
        bad = [e for e in spine["milestones"] if e not in ALLOWED_MILESTONES]
        if bad:
            problems.append(f"{prefix}: unknown milestones {bad}")

    if spine.get("area") not in ALLOWED_AREAS:
        problems.append(f"{prefix}: invalid area '{spine.get('area')}'")

    if spine.get("concept_tier") not in ALLOWED_CONCEPT_TIERS:
        problems.append(f"{prefix}: invalid concept_tier '{spine.get('concept_tier')}'")

    if spine.get("cognitive_role") not in ALLOWED_COGNITIVE_ROLES:
        problems.append(f"{prefix}: invalid cognitive_role '{spine.get('cognitive_role')}'")

    if not isinstance(spine.get("applied"), bool):
        problems.append(f"{prefix}: 'applied' must be true or false")

    phase = spine.get("phase")
    valid_phases = set(PHASE_NAMES.keys())
    if phase not in valid_phases:
        problems.append(f"{prefix}: 'phase' must be one of {sorted(valid_phases)}, got {phase!r}")

    # Phase-type integrity rules from syllabus
    ctype = spine.get("concept_type")
    if phase in _PHASE_REQUIRED_TYPES:
        if ctype not in _PHASE_REQUIRED_TYPES[phase]:
            problems.append(
                f"{prefix}: P{phase} concept must be concept_type={_PHASE_REQUIRED_TYPES[phase]}, got '{ctype}'"
            )
    elif phase in _PHASE_ALLOWED_TYPES:
        if ctype not in _PHASE_ALLOWED_TYPES[phase]:
            problems.append(
                f"{prefix}: P{phase} concept should be {_PHASE_ALLOWED_TYPES[phase]}, got '{ctype}'"
            )

    # Core idea must not be empty and should not be too short
    cs = spine.get("core_idea", "")
    if not cs or len(str(cs).strip()) < 20:
        problems.append(f"{prefix}: core_idea is missing or too short")

    # approved field should not be set by Claude (warn only if value is not false)
    if "approved" in spine and spine["approved"] is not False:
        problems.append(f"{prefix}: 'approved' field present with value {spine['approved']!r} — remove it (only approved: false is valid)")

    return problems


# ---------------------------------------------------------------------------
# Coverage checks
# ---------------------------------------------------------------------------

def coverage_summary(spines: list[dict]) -> dict:
    """Return per-layer counts and exam coverage."""
    layer_counts: dict[int, int] = defaultdict(int)
    exam_counts: dict[str, int]  = defaultdict(int)
    tier_counts: dict[str, int]  = defaultdict(int)
    approved_false = 0

    for spine in spines:
        layer = spine.get("phase")
        if isinstance(layer, int):
            layer_counts[layer] += 1
        for exam in (spine.get("milestones") or []):
            exam_counts[exam] += 1
        tier = spine.get("concept_tier")
        if tier:
            tier_counts[tier] += 1
        if spine.get("approved") is False:
            approved_false += 1

    return {
        "total":          len(spines),
        "layer_counts":   dict(layer_counts),
        "exam_counts":    dict(exam_counts),
        "tier_counts":    dict(tier_counts),
        "approved_false": approved_false,
    }


def duplicate_slugs(spines: list[dict]) -> list[str]:
    seen: dict[str, int] = {}
    dupes: list[str] = []
    for spine in spines:
        slug = spine.get("slug")
        if not slug:
            continue
        if slug in seen:
            dupes.append(slug)
        seen[slug] = seen.get(slug, 0) + 1
    return dupes


def duplicate_ids(spines: list[dict]) -> list[int]:
    seen: dict[int, int] = {}
    dupes: list[int] = []
    for spine in spines:
        sid = spine.get("id")
        if not isinstance(sid, int):
            continue
        if sid in seen:
            dupes.append(sid)
        seen[sid] = seen.get(sid, 0) + 1
    return dupes


# ---------------------------------------------------------------------------
# Report printing
# ---------------------------------------------------------------------------

SEP = "─" * 70

def _bar(count: int, target: int, width: int = 20) -> str:
    if target == 0:
        return "[ no target ]"
    filled = int(width * min(count, target) / target)
    bar = "█" * filled + "░" * (width - filled)
    pct = count / target * 100
    return f"[{bar}] {count:>4}/{target}  ({pct:.0f}%)"


def print_report(spines: list[dict], phase_filter: int | None, problems_only: bool) -> None:
    project_name = syllabus.get("project_name", "Concept Mastery")
    print(f"\n{SEP}")
    print(f"  {project_name} — Spine Curation Report")
    print(SEP)

    # ── filter ───────────────────────────────────────────────────────────────
    if phase_filter is not None:
        spines = [s for s in spines if s.get("phase") == phase_filter]
        print(f"  Filtered to layer {phase_filter} — {len(spines)} spines\n")

    # ── validation ───────────────────────────────────────────────────────────
    all_problems: list[str] = []
    for i, spine in enumerate(spines):
        all_problems.extend(validate_spine(spine, i))

    duped_slugs = duplicate_slugs(spines)
    duped_ids   = duplicate_ids(spines)

    if duped_slugs:
        for slug in duped_slugs:
            all_problems.append(f"DUPLICATE SLUG: '{slug}'")
    if duped_ids:
        for sid in duped_ids:
            all_problems.append(f"DUPLICATE ID: {sid}")

    if all_problems:
        print(f"  ⚠  {len(all_problems)} problem(s) found:\n")
        for p in all_problems:
            print(f"  • {p}")
        print()
    else:
        print(f"  ✓ Validation clean — no problems found\n")

    if problems_only:
        return

    # ── coverage table ───────────────────────────────────────────────────────
    cov = coverage_summary(spines)

    print(f"  Total spines: {cov['total']}")
    if cov["approved_false"]:
        print(f"  Held back (approved: false): {cov['approved_false']}")
    print()

    print("  Phase coverage:")
    for layer in sorted(PHASE_NAMES.keys()):
        name   = PHASE_NAMES[layer]
        target = PHASE_TARGETS.get(layer, 0)
        count  = cov["layer_counts"].get(layer, 0)
        bar    = _bar(count, target)
        print(f"    L{layer} {name:<30} {bar}")
    print()

    print("  Milestone coverage (spines tagged):")
    for exam in sorted(ALLOWED_MILESTONES):
        count = cov["exam_counts"].get(exam, 0)
        print(f"    {exam}: {count}")
    print()

    print("  Concept tier distribution:")
    for tier in sorted(ALLOWED_CONCEPT_TIERS):
        count = cov["tier_counts"].get(tier, 0)
        pct   = count / cov["total"] * 100 if cov["total"] else 0
        print(f"    {tier:<12} {count:>4}  ({pct:.0f}%)")
    print()

    # ── per-layer detail ─────────────────────────────────────────────────────
    if phase_filter is None:
        print("  Spine types per layer:")
        for layer in sorted(PHASE_NAMES.keys()):
            layer_spines = [s for s in spines if s.get("phase") == layer]
            type_counts: dict[str, int] = defaultdict(int)
            for s in layer_spines:
                type_counts[s.get("concept_type", "?")] += 1
            if type_counts:
                breakdown = "  ".join(f"{t}={n}" for t, n in sorted(type_counts.items()))
                print(f"    L{layer}: {breakdown}")
        print()

    print(SEP)
    print("  Next steps:")
    if all_problems:
        print("  1. Fix the problems listed above in input/concept_spines.yaml")
        print("  2. Re-run run_curate.py to confirm clean")
    else:
        print("  1. Review spines — set approved: false on any you want to hold back")
        print("  2. Run: python 02_pipeline/run.py --all")
    print(SEP + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stage 2 — Validate and report on concept_spines.yaml (read-only)"
    )
    parser.add_argument(
        "--layer", type=int, metavar="N",
        help="Show report for a single layer only"
    )
    parser.add_argument(
        "--fix", action="store_true",
        help="Show only validation problems — skip coverage tables"
    )
    args = parser.parse_args()

    spines_path = config.paths.input_dir / "concept_spines.yaml"
    if not spines_path.exists():
        print(f"[error] {spines_path} not found.", file=sys.stderr)
        print("  Run run_outline.py first to generate spines.", file=sys.stderr)
        sys.exit(1)

    raw = yaml.safe_load(spines_path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        print(f"[error] concept_spines.yaml must be a YAML list, got {type(raw).__name__}", file=sys.stderr)
        sys.exit(1)

    print_report(raw, phase_filter=args.layer, problems_only=args.fix)


if __name__ == "__main__":
    main()
