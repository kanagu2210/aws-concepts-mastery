"""
02_pipeline/run_publish.py
Stage 6 — Publish rendered HTML to PDF.

Reads rendered HTML from output/03_rendered/ and produces PDFs
in output/04_published/individual/.

Optionally combines all PDFs into per-layer and complete bundles.

Runs independently of the main pipeline. Requires rendered HTML first.

Usage:
    python 02_pipeline/run_publish.py --spine 47
    python 02_pipeline/run_publish.py --from 1 --to 50
    python 02_pipeline/run_publish.py --spines 47 755 802
    python 02_pipeline/run_publish.py --layer 3
    python 02_pipeline/run_publish.py --all

    python 02_pipeline/run_publish.py --all --resume
    python 02_pipeline/run_publish.py --all --overwrite
    python 02_pipeline/run_publish.py --spine 47 --dry-run

    # Combine PDFs into per-layer and complete bundles
    python 02_pipeline/run_publish.py --combine
    python 02_pipeline/run_publish.py --complete
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline_common import (
    _select_spines,
    _part_subdir,
)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run import run_publish_one, run_combine
from utils.config import config
from utils.usage_log import log_usage

LOG_FILE = config.paths.logs_dir / "usage_publish.tsv"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stage 6 — Publish rendered HTML to PDF"
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
    parser.add_argument("--resume",    action="store_true", help="Skip PDFs that are already up to date")
    parser.add_argument("--overwrite", action="store_true", help="Regenerate PDFs even if up to date")
    parser.add_argument("--dry-run",   action="store_true", help="Print what would run, write nothing")
    parser.add_argument("--combine",   action="store_true", help="Combine individual PDFs into per-layer bundles")
    parser.add_argument("--complete",  action="store_true", help="Build the complete combined PDF")

    args = parser.parse_args()
    config.paths.logs_dir.mkdir(parents=True, exist_ok=True)

    if args.combine or args.complete:
        run_combine(dry_run=args.dry_run)
        return

    spines = _select_spines(args)
    total  = len(spines)

    if total == 0:
        print("[warn] No spines matched the selection criteria.")
        return

    print(f"\n{'─' * 60}")
    print(f"  run_publish.py — {total} spine(s)")
    if len(spines) == 1:
        print(f"  Output path : {_part_subdir(spines[0]['id'])}/")
    if args.resume:    print("  Resume      : on — skipping up-to-date PDFs")
    if args.overwrite: print("  Overwrite   : on — regenerating all")
    if args.dry_run:   print("  DRY RUN     : no files written")
    print(f"{'─' * 60}")

    done = skipped = errors = 0

    for spine in spines:
        spine_id = spine["id"]
        slug     = spine["slug"]

        try:
            run_publish_one(
                spine_id  = spine_id,
                slug      = slug,
                dry_run   = args.dry_run,
                overwrite = args.overwrite,
            )
            done += 1

        except Exception as e:
            print(f"  [{spine_id:04d}] ERROR — {e}", file=sys.stderr)
            log_usage(LOG_FILE, "error", spine_id, slug, status="error", notes=str(e)[:200])
            errors += 1

    print(f"\n{'─' * 60}")
    print(f"  Done — {done} published | {errors} errors")
    print(f"  Log : {LOG_FILE}")
    print(f"{'─' * 60}\n")


if __name__ == "__main__":
    main()