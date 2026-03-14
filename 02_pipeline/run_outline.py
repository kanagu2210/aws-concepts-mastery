"""
02_pipeline/run_outline.py
Stage 1 — Generate concept spines via sequential API calls.

The number and structure of calls is defined in input/syllabus.yaml
under the `call_plan` key.

Usage:
    python 02_pipeline/run_outline.py --dry-run   # show call plan, no API calls
    python 02_pipeline/run_outline.py             # run all calls
    python 02_pipeline/run_outline.py --resume    # skip calls already backed up
    python 02_pipeline/run_outline.py --call 5    # run a single call by number (1-indexed)

Output:
    input/concept_spines.yaml       — final merged spine list
    logs/backups/outline/call_*.yaml — per-call backup (written before merging)
    logs/usage_outline.tsv           — token and cost log
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import yaml

# Make sure project root is on sys.path when running as a script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.api import call_claude
from utils.config import config, syllabus, syllabus_outline_plan
from utils.usage_log import compute_cost, log_usage


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_prompt() -> str:
    prompt_path = config.paths.prompts_dir / "outline_prompt.md"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt not found: {prompt_path}")
    text = prompt_path.read_text(encoding="utf-8")

    # Inject syllabus variables into the outline prompt
    from utils.config import (
        syllabus_analogy_block,
        syllabus_milestone_depth_block,
        syllabus_phase_block,
        syllabus_area_block,
        syllabus_milestone_tags,
    )

    replacements = {
        "{{SUBJECT}}":           syllabus.get("subject", ""),
        "{{SUBJECT_SHORT}}":     syllabus.get("subject_short", ""),
        "{{PROJECT_NAME}}":      syllabus.get("project_name", ""),
        "{{EXPERT_ROLE}}":       syllabus.get("expert_role", "").strip(),
        "{{PHASE_DESCRIPTIONS}}": syllabus_phase_block(),
        "{{AREA_LIST}}":       syllabus_area_block(),
        "{{MILESTONE_DEPTH_MAP}}":    syllabus_milestone_depth_block(),
        "{{COVERAGE_MAP}}": syllabus.get("coverage_map", "").strip(),
        "{{TEACHING_NOTES}}":    syllabus.get("teaching_notes", "").strip(),
        "{{ENTITY_FIELD}}":     syllabus.get("concept_schema", {}).get("entity_field", "service"),
        "{{ALLOWED_TYPES}}": ", ".join(
            syllabus.get("concept_schema", {}).get("allowed_types", [])
        ),
        "{{ALLOWED_TIERS}}": ", ".join(
            syllabus.get("concept_schema", {}).get("allowed_tiers", [])
        ),
        "{{ALLOWED_ROLES}}": ", ".join(
            syllabus.get("concept_schema", {}).get("allowed_roles", [])
        ),
        "{{ALLOWED_MILESTONES}}": ", ".join(syllabus_milestone_tags()),
        "{{ALLOWED_AREAS}}": "\n".join(
            f"  {d['name']}" for d in syllabus.get("areas", [])
        ),
    }

    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)

    return text


def _backup_path(call_index: int) -> Path:
    """Path for per-call YAML backup, e.g. logs/backups/outline/call_05.yaml"""
    return config.paths.backups_outline_dir / f"call_{call_index:02d}.yaml"


def _load_existing_slugs() -> list[str]:
    """
    Collect all slugs already generated from backups.
    This is what gets injected as {existing_slugs} into the prompt.
    """
    slugs: list[str] = []
    backup_dir = config.paths.backups_outline_dir
    if not backup_dir.exists():
        return slugs
    for backup_file in sorted(backup_dir.glob("call_*.yaml")):
        try:
            data = yaml.safe_load(backup_file.read_text(encoding="utf-8"))
            if isinstance(data, list):
                for spine in data:
                    if isinstance(spine, dict) and "slug" in spine:
                        slugs.append(spine["slug"])
        except Exception:
            pass
    return slugs


def _inject_vars(prompt: str, call_name: str, domain: str, start_id: int, target: int, existing_slugs: list[str]) -> str:
    """Replace all {placeholders} in the prompt with actual values."""
    slugs_block = "\n".join(existing_slugs) if existing_slugs else "(none yet)"
    return (
        prompt
        .replace("{domain_call}",   call_name)
        .replace("{domain_value}",  domain)
        .replace("{start_id}",      str(start_id))
        .replace("{target_count}",  str(target))
        .replace("{existing_slugs}", slugs_block)
    )


def _parse_yaml_response(raw: str, call_name: str) -> list[dict]:
    """
    Parse the YAML returned by the API.
    The model may append a comment line like:
        # Call: ... | Count: ... | IDs: ...
    Strip that before parsing.
    """
    lines = raw.splitlines()
    yaml_lines = [l for l in lines if not l.strip().startswith("# Call:")]
    cleaned = "\n".join(yaml_lines).strip()

    try:
        parsed = yaml.safe_load(cleaned)
    except yaml.YAMLError as e:
        raise ValueError(f"YAML parse error for '{call_name}':\n{e}\n\nRaw output:\n{raw[:500]}")

    if not isinstance(parsed, list):
        raise ValueError(
            f"Expected a YAML list for '{call_name}', got {type(parsed).__name__}.\n"
            f"Raw output:\n{raw[:500]}"
        )
    return parsed


def _merge_to_master(new_spines: list[dict]) -> None:
    """Append new spines to input/concept_spines.yaml, creating it if needed."""
    master_path = config.paths.input_dir / "concept_spines.yaml"
    config.paths.input_dir.mkdir(parents=True, exist_ok=True)

    existing: list[dict] = []
    if master_path.exists():
        data = yaml.safe_load(master_path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            existing = data

    # Avoid duplicate IDs if re-running a call
    existing_ids = {s.get("id") for s in existing}
    to_add = [s for s in new_spines if s.get("id") not in existing_ids]
    merged = existing + to_add

    with open(master_path, "w", encoding="utf-8") as f:
        yaml.dump(merged, f, allow_unicode=True, sort_keys=False, default_flow_style=False)


def _print_plan(calls: list[tuple]) -> None:
    project_name = syllabus.get("project_name", "Concept Mastery")
    print(f"\n{'─' * 70}")
    print(f"  {project_name} — Outline Generator")
    print(f"  {len(calls)} calls planned")
    print(f"{'─' * 70}")
    total = 0
    for i, (name, _, start, count) in enumerate(calls, 1):
        print(f"  [{i:02d}] {name:<55} {count:>4} spines  IDs {start}–{start+count-1}")
        total += count
    print(f"{'─' * 70}")
    print(f"  Total: {total} spines\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(args: argparse.Namespace) -> None:
    prompt_template = _load_prompt()
    log_file = config.paths.logs_dir / "usage_outline.tsv"
    config.paths.backups_outline_dir.mkdir(parents=True, exist_ok=True)
    config.paths.logs_dir.mkdir(parents=True, exist_ok=True)

    # Load call plan from syllabus
    full_call_plan = syllabus_outline_plan()

    # Filter to a single call if --call N was passed
    calls = full_call_plan
    if args.call is not None:
        if not (1 <= args.call <= len(full_call_plan)):
            print(f"[error] --call must be between 1 and {len(full_call_plan)}", file=sys.stderr)
            sys.exit(1)
        calls = [full_call_plan[args.call - 1]]

    _print_plan(calls)

    if args.dry_run:
        print("[dry-run] No API calls made.")
        return

    for i, (call_name, domain, start_id, target) in enumerate(calls, 1):
        # Use the original index in full_call_plan for backup file naming
        plan_index = full_call_plan.index((call_name, domain, start_id, target)) + 1
        backup = _backup_path(plan_index)

        # Resume: skip if backup already exists
        if args.resume and backup.exists():
            print(f"[skip] call {plan_index:02d}: {call_name} — backup exists")
            continue

        print(f"\n[call {plan_index:02d}/{len(full_call_plan)}] {call_name}")
        print(f"         IDs {start_id}–{start_id + target - 1}  target={target}")

        existing_slugs = _load_existing_slugs()
        prompt = _inject_vars(prompt_template, call_name, domain, start_id, target, existing_slugs)

        t0 = time.monotonic()
        try:
            raw, in_tok, out_tok = call_claude(prompt)
            duration = time.monotonic() - t0
            cost = compute_cost(in_tok, out_tok)

            spines = _parse_yaml_response(raw, call_name)
            actual_count = len(spines)

            # Write backup before merging
            backup.write_text(raw, encoding="utf-8")

            # Merge into master
            _merge_to_master(spines)

            print(f"         ✓ {actual_count} spines  {in_tok:,} in / {out_tok:,} out  ${cost:.4f}  {duration:.1f}s")

            if actual_count != target:
                print(f"  [warn] expected {target} spines, got {actual_count}")

            log_usage(
                log_file=log_file,
                stage="outline",
                spine_id=f"{start_id}-{start_id + target - 1}",
                slug=call_name,
                input_tokens=in_tok,
                output_tokens=out_tok,
                cost_usd=cost,
                duration_s=duration,
                status="ok",
                notes=f"count={actual_count}",
            )

        except Exception as e:
            duration = time.monotonic() - t0
            print(f"  [error] call {plan_index:02d} failed: {e}", file=sys.stderr)
            log_usage(
                log_file=log_file,
                stage="outline",
                spine_id=f"{start_id}-{start_id + target - 1}",
                slug=call_name,
                duration_s=duration,
                status="error",
                notes=str(e)[:200],
            )
            print("  Continuing to next call...", file=sys.stderr)

    print("\n[done] run_outline.py complete.")
    print(f"       Spines written to: {config.paths.input_dir / 'concept_spines.yaml'}")
    print(f"       Backups at:        {config.paths.backups_outline_dir}")


def main() -> None:
    total_calls = len(syllabus_outline_plan())
    parser = argparse.ArgumentParser(
        description=f"Stage 1 — Generate concept spines ({total_calls} API calls)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print call plan without making any API calls"
    )
    parser.add_argument(
        "--resume", action="store_true",
        help="Skip calls that already have a backup file"
    )
    parser.add_argument(
        "--call", type=int, metavar="N",
        help="Run only call number N (1-indexed)"
    )
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
