"""
utils/config.py
Loads config.yaml and .env, exposes all settings as a Config dataclass.

Usage:
    from utils.config import config
    print(config.model)
    print(config.paths.prompts_dir)
"""

from __future__ import annotations

import os
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
        combined_complete    = pr.get("combined_complete",   True),
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


# Singleton — all scripts import this directly
config: Config = _load()