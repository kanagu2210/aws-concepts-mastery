"""
utils/usage_log.py
Appends one TSV row per API call to logs/usage_outline.tsv or logs/usage_run.tsv.

TSV columns (all stages):
    timestamp   stage   spine_id   slug   input_tokens   output_tokens
    cost_usd    duration_s   status   notes

Usage:
    from utils.usage_log import log_usage
    log_usage(
        log_file=config.paths.logs_dir / "usage_run.tsv",
        stage="expand",
        spine_id=47,
        slug="l2-iam-evaluation-model",
        input_tokens=1200,
        output_tokens=850,
        cost_usd=0.0042,
        duration_s=3.1,
        status="ok",       # "ok" | "skip" | "error"
        notes="",
    )
"""

from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


# TSV column order — never change this once logs exist
_COLUMNS = [
    "timestamp",
    "stage",
    "spine_id",
    "slug",
    "input_tokens",
    "output_tokens",
    "cost_usd",
    "duration_s",
    "status",
    "notes",
]

# Anthropic pricing as of claude-sonnet-4-20250514 (USD per million tokens)
# Update these if pricing changes.
_INPUT_PRICE_PER_M  = 3.00   # $3.00 / 1M input tokens
_OUTPUT_PRICE_PER_M = 15.00  # $15.00 / 1M output tokens


def compute_cost(input_tokens: int, output_tokens: int) -> float:
    """Return estimated cost in USD for one API call."""
    return (
        input_tokens  / 1_000_000 * _INPUT_PRICE_PER_M
        + output_tokens / 1_000_000 * _OUTPUT_PRICE_PER_M
    )


def log_usage(
    log_file: Path,
    stage: str,
    spine_id: int | str,
    slug: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    cost_usd: float = 0.0,
    duration_s: float = 0.0,
    status: str = "ok",
    notes: str = "",
) -> None:
    """
    Append one row to the TSV log file.
    Creates the file and writes the header if it does not exist.
    Thread-safe for single-process sequential use (no locking needed here).
    """
    log_file = Path(log_file)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    write_header = not log_file.exists() or log_file.stat().st_size == 0

    with open(log_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_COLUMNS, delimiter="\t")
        if write_header:
            writer.writeheader()
        writer.writerow({
            "timestamp":     datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "stage":         stage,
            "spine_id":      str(spine_id),
            "slug":          slug,
            "input_tokens":  str(input_tokens),
            "output_tokens": str(output_tokens),
            "cost_usd":      f"{cost_usd:.6f}",
            "duration_s":    f"{duration_s:.2f}",
            "status":        status,
            "notes":         notes,
        })


def print_usage_summary(
    log_file: Path,
    stage_filter: str | None = None,
) -> None:
    """
    Print a short cost summary from an existing TSV log.
    Optionally filter to a specific stage.
    """
    log_file = Path(log_file)
    if not log_file.exists():
        print(f"[usage] No log file at {log_file}", file=sys.stderr)
        return

    total_input = 0
    total_output = 0
    total_cost = 0.0
    total_rows = 0
    errors = 0

    with open(log_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            if stage_filter and row.get("stage") != stage_filter:
                continue
            total_rows += 1
            total_input  += int(row.get("input_tokens",  0) or 0)
            total_output += int(row.get("output_tokens", 0) or 0)
            total_cost   += float(row.get("cost_usd",    0) or 0)
            if row.get("status") == "error":
                errors += 1

    label = f"stage={stage_filter}" if stage_filter else "all stages"
    print(
        f"[usage] {label} | calls={total_rows} | "
        f"input={total_input:,} | output={total_output:,} | "
        f"cost=${total_cost:.4f} | errors={errors}"
    )