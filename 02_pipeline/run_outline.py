"""
02_pipeline/run_outline.py
Stage 1 — Generate all 1000 concept spines in 51 sequential API calls.

Usage:
    python 02_pipeline/run_outline.py --dry-run   # show call plan, no API calls
    python 02_pipeline/run_outline.py             # run all 51 calls
    python 02_pipeline/run_outline.py --resume    # skip calls already backed up
    python 02_pipeline/run_outline.py --call 5    # run a single call by number (1-indexed)

Output:
    input/concept_spines.yaml       — final merged spine list
    logs/backups/outline/call_*.yaml — per-call backup (written before merging)
    logs/usage_outline.tsv           — token and cost log
"""

from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path

import yaml

# Make sure project root is on sys.path when running as a script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.api import call_claude
from utils.config import config
from utils.usage_log import compute_cost, log_usage

# ---------------------------------------------------------------------------
# Call plan — 51 calls, matches outline_prompt.md exactly
# ---------------------------------------------------------------------------
# Each entry: (call_name, domain_value, start_id, target_count)
CALL_PLAN: list[tuple[str, str, int, int]] = [
    # Layer 1 — Foundations (50 spines)
    ("Layer 1 Part 1: The 8 Big Ideas of Cloud and AWS",                 "Cloud Concepts",                  1,   20),
    ("Layer 1 Part 2: AWS Design Philosophy and Global Infrastructure",  "Cloud Concepts",                  21,  20),
    ("Layer 1 Part 3: Shared Responsibility and the Cost Model",         "Cloud Concepts",                  41,  10),
    # Layer 2 — Core Mechanisms (100 spines)
    ("Layer 2 Part 1: IAM and Security Mechanisms",                      "Security and Compliance",         51,  20),
    ("Layer 2 Part 2: Networking and VPC Mechanisms",                    "Cloud Technology and Services",   71,  20),
    ("Layer 2 Part 3: Compute and Serverless Mechanisms",                "Cloud Technology and Services",   91,  20),
    ("Layer 2 Part 4: Storage and Database Mechanisms",                  "Cloud Technology and Services",   111, 20),
    ("Layer 2 Part 5: Integration, Messaging and Delivery Mechanisms",   "Cloud Technology and Services",   131, 20),
    # Layer 3 — Service Mastery (350 spines)
    ("Layer 3 Part 1: EC2 — Elastic Compute Cloud",                      "Cloud Technology and Services",   151, 20),
    ("Layer 3 Part 2: Containers and Serverless Compute",                "Cloud Technology and Services",   171, 20),
    ("Layer 3 Part 3: S3 — Simple Storage Service",                      "Cloud Technology and Services",   191, 20),
    ("Layer 3 Part 4: Block, File and Archival Storage",                 "Cloud Technology and Services",   211, 20),
    ("Layer 3 Part 5: RDS and Relational Databases",                     "Cloud Technology and Services",   231, 20),
    ("Layer 3 Part 6: DynamoDB and NoSQL Databases",                     "Cloud Technology and Services",   251, 20),
    ("Layer 3 Part 7: Speciality Databases and Data Migration",          "Cloud Technology and Services",   271, 20),
    ("Layer 3 Part 8: VPC and Core Networking",                          "Cloud Technology and Services",   291, 20),
    ("Layer 3 Part 9: Content Delivery and DNS",                         "Cloud Technology and Services",   311, 20),
    ("Layer 3 Part 10: IAM, KMS and Core Security Services",             "Security and Compliance",         331, 20),
    ("Layer 3 Part 11: Threat Detection, Compliance and Audit Services", "Security and Compliance",         351, 20),
    ("Layer 3 Part 12: SQS, SNS, EventBridge and Messaging",             "Cloud Technology and Services",   371, 20),
    ("Layer 3 Part 13: API Gateway, Step Functions and Workflow",        "Cloud Technology and Services",   391, 20),
    ("Layer 3 Part 14: Analytics — Kinesis, Athena, EMR, Glue",         "Cloud Technology and Services",   411, 20),
    ("Layer 3 Part 15: BI, ML and AI Services",                          "Cloud Technology and Services",   431, 20),
    ("Layer 3 Part 16: Developer Tools and CI/CD",                       "Cloud Technology and Services",   451, 20),
    ("Layer 3 Part 17: Management, Monitoring and Governance Services",  "Cloud Technology and Services",   471, 20),
    ("Layer 3 Part 18: Billing, Cost and Support Services",              "Billing, Pricing, and Support",   491, 10),
    # Layer 4 — Decision Patterns (250 spines)
    ("Layer 4 Part 1: Resilience and High Availability Decisions",       "Cross-Domain",                    501, 20),
    ("Layer 4 Part 2: Fault Tolerance and Disaster Recovery Decisions",  "Cross-Domain",                    521, 20),
    ("Layer 4 Part 3: Scalability and Performance Decisions",            "Cross-Domain",                    541, 20),
    ("Layer 4 Part 4: Compute Selection Decisions",                      "Cross-Domain",                    561, 20),
    ("Layer 4 Part 5: Storage Selection Decisions",                      "Cross-Domain",                    581, 20),
    ("Layer 4 Part 6: Database Selection Decisions",                     "Cross-Domain",                    601, 20),
    ("Layer 4 Part 7: Networking and Connectivity Decisions",            "Cross-Domain",                    621, 20),
    ("Layer 4 Part 8: Security Architecture Decisions",                  "Cross-Domain",                    641, 20),
    ("Layer 4 Part 9: Integration and Messaging Decisions",              "Cross-Domain",                    661, 20),
    ("Layer 4 Part 10: Cost Optimisation Decisions",                     "Cross-Domain",                    681, 20),
    ("Layer 4 Part 11: Serverless vs Container vs EC2 Decisions",        "Cross-Domain",                    701, 20),
    ("Layer 4 Part 12: Data and Analytics Decisions",                    "Cross-Domain",                    721, 20),
    ("Layer 4 Part 13: Migration Strategy Decisions",                    "Cross-Domain",                    741, 10),
    # Layer 5 — Architectural Patterns (180 spines)
    ("Layer 5 Part 1: Web Application Patterns",                         "Cross-Domain",                    751, 20),
    ("Layer 5 Part 2: Serverless and Event-Driven Patterns",             "Cross-Domain",                    771, 20),
    ("Layer 5 Part 3: Data Lake and Analytics Patterns",                 "Cross-Domain",                    791, 20),
    ("Layer 5 Part 4: Microservices and Decoupling Patterns",            "Cross-Domain",                    811, 20),
    ("Layer 5 Part 5: Disaster Recovery and Business Continuity Patterns","Cross-Domain",                   831, 20),
    ("Layer 5 Part 6: Hybrid and On-Premises Integration Patterns",      "Cross-Domain",                    851, 20),
    ("Layer 5 Part 7: Multi-Account and Governance Patterns",            "Cross-Domain",                    871, 20),
    ("Layer 5 Part 8: Migration and Modernisation Patterns",             "Cross-Domain",                    891, 20),
    ("Layer 5 Part 9: Cost Optimisation at Scale Patterns",              "Cross-Domain",                    911, 20),
    # Layer 6 — Exam and Interview Bridges (70 spines)
    ("Layer 6 Part 1: CCP Exam Bridges and Common Traps",                "Cross-Domain",                    931, 20),
    ("Layer 6 Part 2: SAA Exam Bridges and Scenario Frameworks",         "Cross-Domain",                    951, 20),
    ("Layer 6 Part 3: SAP and Interview Bridges",                        "Cross-Domain",                    971, 30),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_prompt() -> str:
    prompt_path = config.paths.prompts_dir / "outline_prompt.md"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt not found: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


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
    print(f"\n{'─' * 70}")
    print(f"  run_outline.py — {len(calls)} calls planned")
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

    # Filter to a single call if --call N was passed
    calls = CALL_PLAN
    if args.call is not None:
        if not (1 <= args.call <= len(CALL_PLAN)):
            print(f"[error] --call must be between 1 and {len(CALL_PLAN)}", file=sys.stderr)
            sys.exit(1)
        calls = [CALL_PLAN[args.call - 1]]

    _print_plan(calls)

    if args.dry_run:
        print("[dry-run] No API calls made.")
        return

    for i, (call_name, domain, start_id, target) in enumerate(calls, 1):
        # Use the original index in CALL_PLAN for backup file naming
        plan_index = CALL_PLAN.index((call_name, domain, start_id, target)) + 1
        backup = _backup_path(plan_index)

        # Resume: skip if backup already exists
        if args.resume and backup.exists():
            print(f"[skip] call {plan_index:02d}: {call_name} — backup exists")
            continue

        print(f"\n[call {plan_index:02d}/{len(CALL_PLAN)}] {call_name}")
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
    parser = argparse.ArgumentParser(
        description="Stage 1 — Generate concept spines (51 API calls)"
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