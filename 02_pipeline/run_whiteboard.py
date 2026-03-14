"""
02_pipeline/run_whiteboard.py
Stage 4b — Whiteboard generation.

Reads narrated scripts from output/02_narrated/ and produces
standalone scrollable SVG whiteboard HTML files in output/02b_whiteboards/.

Runs independently of the main pipeline. Requires narration to exist first.

Usage:
    python 02_pipeline/run_whiteboard.py --spine 47
    python 02_pipeline/run_whiteboard.py --from 1 --to 50
    python 02_pipeline/run_whiteboard.py --spines 47 755 802
    python 02_pipeline/run_whiteboard.py --layer 3
    python 02_pipeline/run_whiteboard.py --all

    python 02_pipeline/run_whiteboard.py --all --resume
    python 02_pipeline/run_whiteboard.py --all --overwrite
    python 02_pipeline/run_whiteboard.py --spine 47 --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline_common import (
    _select_spines,
    _part_subdir,
    narrated_path,
    whiteboard_path,
    _strip_front_matter,
)

# Import the stage function from run — this is safe because run.py
# no longer imports from run_whiteboard.py (no circular dependency)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run import run_whiteboard
from utils.config import config
from utils.usage_log import log_usage

LOG_FILE = config.paths.logs_dir / "usage_whiteboard.tsv"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stage 4b — Generate whiteboard HTML from narrated scripts"
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
    parser.add_argument("--resume",    action="store_true", help="Skip spines that already have a whiteboard")
    parser.add_argument("--overwrite", action="store_true", help="Regenerate even if whiteboard exists")
    parser.add_argument("--dry-run",   action="store_true", help="Print what would run, make no API calls")

    args = parser.parse_args()
    config.paths.logs_dir.mkdir(parents=True, exist_ok=True)

    spines = _select_spines(args)
    total  = len(spines)

    if total == 0:
        print("[warn] No spines matched the selection criteria.")
        return

    print(f"\n{'─' * 60}")
    print(f"  run_whiteboard.py — {total} spine(s)")
    if len(spines) == 1:
        print(f"  Output path : {_part_subdir(spines[0]['id'])}/")
    if args.resume:    print("  Resume      : on — skipping existing")
    if args.overwrite: print("  Overwrite   : on — regenerating all")
    if args.dry_run:   print("  DRY RUN     : no API calls")
    print(f"{'─' * 60}")

    done = skipped = missing = errors = 0

    for spine in spines:
        spine_id = spine["id"]
        slug     = spine["slug"]

        try:
            n_path = narrated_path(spine_id, slug)
            w_path = whiteboard_path(spine_id, slug)

            if not n_path.exists():
                print(f"  [{spine_id:04d}] SKIP — narrated file missing ({n_path.name})")
                missing += 1
                continue

            if args.resume and not args.overwrite and w_path.exists():
                print(f"  [{spine_id:04d}] SKIP — whiteboard exists ({w_path.name})")
                skipped += 1
                continue

            if args.overwrite and w_path.exists():
                print(f"  [{spine_id:04d}] OVERWRITE")

            narrated_md = n_path.read_text(encoding="utf-8")
            print(f"  [{spine_id:04d}] {slug}")
            run_whiteboard(spine_id, slug, narrated_md, dry_run=args.dry_run)
            done += 1

        except Exception as e:
            print(f"  [{spine_id:04d}] ERROR — {e}", file=sys.stderr)
            log_usage(LOG_FILE, "error", spine_id, slug, status="error", notes=str(e)[:200])
            errors += 1

    print(f"\n{'─' * 60}")
    print(f"  Done — {done} generated | {skipped} skipped | {missing} missing narration | {errors} errors")
    print(f"  Log : {LOG_FILE}")
    print(f"{'─' * 60}\n")


if __name__ == "__main__":
    main()