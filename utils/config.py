"""
utils/config.py
Loads config.yaml, .env, and input/syllabus.yaml.
Exposes all settings as a Config dataclass.

Usage:
    from utils.config import config, syllabus
    print(config.model)
    print(config.paths.prompts_dir)
    print(syllabus["project_name"])
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# Project root = two levels up from this file (utils/config.py → root)
_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_PATH = _ROOT / "config.yaml"


# ---------------------------------------------------------------------------
# Sub-configs
# ---------------------------------------------------------------------------

@dataclass
class PathsConfig:
    prompts_dir: Path
    input_dir: Path
    output_concepts_dir: Path
    output_narrated_dir: Path
    output_whiteboard_dir: Path
    output_rendered_dir: Path
    output_published_dir: Path
    logs_dir: Path
    backups_outline_dir: Path
    backups_expand_dir: Path


@dataclass
class PdfConfig:
    page_size: str = "A4"
    margin_top: str = "20mm"
    margin_bottom: str = "20mm"
    margin_left: str = "18mm"
    margin_right: str = "18mm"
    rendered_dir: str = "output/03_rendered"
    output_dir: str = "output/04_published"
    individual_subdir: str = "individual"
    combined_subdir: str = "combined"
    offline_fonts: bool = False
    weasyprint_log_level: str = "ERROR"
    combined_by_layer: bool = True
    combined_complete: bool = True


@dataclass
class Config:
    model: str
    max_tokens: int
    paths: PathsConfig
    pdf: PdfConfig
    api_key: str = field(default="", repr=False)


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

def _read_env_file() -> dict[str, str]:
    """Read key=value pairs from .env if it exists."""
    env_path = _ROOT / ".env"
    result: dict[str, str] = {}
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def _load() -> Config:
    if not _CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"config.yaml not found at {_CONFIG_PATH}\n"
            "Run all scripts from the project root directory."
        )

    with open(_CONFIG_PATH) as f:
        raw = yaml.safe_load(f) or {}

    # Paths
    p = raw.get("paths", {})
    paths = PathsConfig(
        prompts_dir           = _ROOT / p.get("prompts_dir",            "01_prompts"),
        input_dir             = _ROOT / p.get("input_dir",              "input"),
        output_concepts_dir   = _ROOT / p.get("output_concepts_dir",    "output/01_concepts"),
        output_narrated_dir   = _ROOT / p.get("output_narrated_dir",    "output/02_narrated"),
        output_whiteboard_dir = _ROOT / p.get("output_whiteboard_dir",  "output/02b_whiteboards"),
        output_rendered_dir   = _ROOT / p.get("output_rendered_dir",    "output/03_rendered"),
        output_published_dir  = _ROOT / p.get("output_published_dir",   "output/04_published"),
        logs_dir              = _ROOT / p.get("logs_dir",               "logs"),
        backups_outline_dir   = _ROOT / p.get("backups_outline_dir",    "logs/backups/outline"),
        backups_expand_dir    = _ROOT / p.get("backups_expand_dir",     "logs/backups/expand"),
    )

    # PDF
    pr = raw.get("pdf", {})
    pdf = PdfConfig(
        page_size            = pr.get("page_size",           "A4"),
        margin_top           = pr.get("margin_top",          "20mm"),
        margin_bottom        = pr.get("margin_bottom",       "20mm"),
        margin_left          = pr.get("margin_left",         "18mm"),
        margin_right         = pr.get("margin_right",        "18mm"),
        rendered_dir         = pr.get("rendered_dir",        "output/03_rendered"),
        output_dir           = pr.get("output_dir",          "output/04_published"),
        individual_subdir    = pr.get("individual_subdir",   "individual"),
        combined_subdir      = pr.get("combined_subdir",     "combined"),
        offline_fonts        = pr.get("offline_fonts",       False),
        weasyprint_log_level = pr.get("weasyprint_log_level","ERROR"),
        combined_by_layer    = pr.get("combined_by_layer",   True),
        combined_complete    = pr.get("combined_complete",    True),
    )

    # API key: environment variable wins over .env file
    env_file = _read_env_file()
    api_key = (
        os.environ.get("ANTHROPIC_API_KEY")
        or env_file.get("ANTHROPIC_API_KEY")
        or ""
    )
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY not found.\n"
            "  Option 1: add it to your .env file:  ANTHROPIC_API_KEY=sk-ant-...\n"
            "  Option 2: export it in your shell:   export ANTHROPIC_API_KEY=sk-ant-..."
        )

    return Config(
        model      = raw.get("model",      "claude-sonnet-4-20250514"),
        max_tokens = raw.get("max_tokens", 8000),
        paths      = paths,
        pdf        = pdf,
        api_key    = api_key,
    )


# ---------------------------------------------------------------------------
# Syllabus loader
# ---------------------------------------------------------------------------

def _load_syllabus() -> dict:
    """
    Load input/syllabus.yaml — the single subject-specific input file.
    Returns the parsed dict.  Cached at module level as `syllabus`.
    """
    syllabus_path = _ROOT / "input" / "syllabus.yaml"
    if not syllabus_path.exists():
        print(
            f"[error] input/syllabus.yaml not found at {syllabus_path}\n"
            "  Create a syllabus.yaml to define your course.",
            file=sys.stderr,
        )
        sys.exit(1)
    raw = yaml.safe_load(syllabus_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        print("[error] syllabus.yaml must be a YAML mapping.", file=sys.stderr)
        sys.exit(1)
    return raw


# ---------------------------------------------------------------------------
# Syllabus convenience helpers
# ---------------------------------------------------------------------------

def syllabus_phase_names() -> dict[int, str]:
    """Return {1: 'Foundations', 2: 'Core Mechanisms', ...} from syllabus."""
    phases = syllabus.get("phases", {})
    return {int(k): v["name"] for k, v in phases.items()}


def syllabus_phase_name_slug(phase: int) -> str:
    """Return e.g. 'foundations' or 'core_mechanisms' for a phase number."""
    name = syllabus_phase_names().get(phase, f"phase_{phase}")
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def syllabus_milestone_tags() -> list[str]:
    """Return the list of milestone tag keys, e.g. ['CCP', 'SAA', 'SAP']."""
    return list(syllabus.get("milestones", {}).keys())


def syllabus_milestone_colors() -> dict[str, str]:
    """Return {milestone_tag: badge_color} from syllabus."""
    return {
        tag: info.get("badge_color", "#999999")
        for tag, info in syllabus.get("milestones", {}).items()
    }


def syllabus_allowed_areas() -> set[str]:
    """Return the set of allowed area names."""
    return {d["name"] for d in syllabus.get("areas", [])}


def syllabus_outline_plan() -> list[tuple[str, str, int, int]]:
    """Return outline plan as list of (call_name, area, start_id, target_count)."""
    return [
        (e["call_name"], e["area"], e["start_id"], e["target_count"])
        for e in syllabus.get("outline_plan", [])
    ]


def syllabus_analogy_block() -> str:
    """Format the analogy_sources for prompt injection."""
    sources = syllabus.get("analogy_sources", [])
    lines = []
    for s in sources:
        lines.append(f"**{s['name']} ({s['context']})**")
        lines.append(f"Use for: {s['use_for']}")
        lines.append("")
    return "\n".join(lines)


def syllabus_milestone_depth_block() -> str:
    """Format milestone depth mapping for prompt injection."""
    milestones = syllabus.get("milestones", {})
    lines = []
    for tag, info in milestones.items():
        lines.append(f"- {tag} ({info['full_name']}): depth {info['depth']}")
    return "\n".join(lines)


def syllabus_phase_block() -> str:
    """Format phase descriptions for prompt injection."""
    phases = syllabus.get("phases", {})
    lines = []
    for num, info in sorted(phases.items(), key=lambda x: int(x[0])):
        lines.append(f"Phase {num} — {info['name']}")
        lines.append(f"  {info['description'].strip()}")
        lines.append(f"  Target: {info.get('target_count', '?')} concepts")
        types = info.get("required_types") or info.get("allowed_types", [])
        lines.append(f"  Concept types: {', '.join(types)}")
        lines.append("")
    return "\n".join(lines)


def syllabus_area_block() -> str:
    """Format areas for prompt injection."""
    areas = syllabus.get("areas", [])
    return "\n".join(f"- {d['name']}: {d['description']}" for d in areas)


# Singletons — all scripts import these directly
config: Config = _load()
syllabus: dict = _load_syllabus()
