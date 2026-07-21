#!/usr/bin/env python3
"""
run_pipeline.py — Master orchestrator: run all stages in order.

Executes the full pipeline for all teams:
  1. Deterministic audit  (run_det_audit.py)
  2. Calculation          (run_calculate.py)
  3. Markdown + Charts    (run_render.py)
  4. HTML reports         (run_html.py)
  5. PDF generation       (run_pdf.py)

Skips stages with --skip flags. Stops on first failure unless --no-stop.

Usage:
  python run_pipeline.py
  python run_pipeline.py --skip-det --skip-pdf
  python run_pipeline.py --team "Goal GPT"
  python run_pipeline.py --no-stop
"""
import argparse
import os
import sys
import time

_script = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _script)

from run_det_audit import main as det_main
from run_calculate import main as calc_main
from run_render import main as render_main
from run_html import main as html_main
from run_pdf import main as pdf_main

STAGES = [
    ("Deterministic Audit", "det", det_main),
    ("Calculation",         "calc", calc_main),
    ("Markdown + Charts",   "render", render_main),
    ("HTML Reports",        "html", html_main),
    ("PDF Generation",      "pdf", pdf_main),
]


def _patch_args(stage_key, args):
    """Rewrite sys.argv for each stage's main() function."""
    argv = ["run_pipeline.py"]
    argv.extend(["--standard", args.standard])
    if args.db:
        argv.extend(["--db", args.db])
    if args.team:
        argv.extend(["--team", args.team])

    if stage_key == "det":
        if args.skip_existing:
            argv.append("--skip-existing")
    elif stage_key in ("calc", "render", "html"):
        argv.extend(["--mode", args.mode])
    elif stage_key == "pdf":
        pass  # pdf uses its own arg set

    return argv


def main():
    parser = argparse.ArgumentParser(
        description="Master orchestrator: run all pipeline stages in order"
    )
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    parser.add_argument("--team", default=None, help="Process only this team")
    parser.add_argument("--mode", choices=["det", "sem", "both"], default="both")
    parser.add_argument("--skip-det", action="store_true", help="Skip deterministic audit")
    parser.add_argument("--skip-calc", action="store_true", help="Skip calculation")
    parser.add_argument("--skip-render", action="store_true", help="Skip markdown+charts")
    parser.add_argument("--skip-html", action="store_true", help="Skip HTML reports")
    parser.add_argument("--skip-pdf", action="store_true", help="Skip PDF generation")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip teams with existing scores in det audit")
    parser.add_argument("--no-stop", action="store_true",
                        help="Continue even if a stage fails")
    args = parser.parse_args()

    skip_map = {
        "det": args.skip_det,
        "calc": args.skip_calc,
        "render": args.skip_render,
        "html": args.skip_html,
        "pdf": args.skip_pdf,
    }

    print(f"{'='*60}")
    print(f"PIPELINE: {args.standard}")
    print(f"{'='*60}")

    results = []
    for label, key, func in STAGES:
        if skip_map.get(key):
            print(f"\n[{label}] SKIPPED (--skip-{key})")
            results.append((label, "SKIPPED"))
            continue

        print(f"\n{'='*60}")
        print(f"STAGE: {label}")
        print(f"{'='*60}")

        old_argv = sys.argv
        sys.argv = _patch_args(key, args)
        start = time.time()

        try:
            func()
            elapsed = time.time() - start
            print(f"[{label}] PASS ({elapsed:.1f}s)")
            results.append((label, "PASS"))
        except SystemExit as e:
            elapsed = time.time() - start
            if e.code == 0:
                print(f"[{label}] PASS ({elapsed:.1f}s)")
                results.append((label, "PASS"))
            else:
                print(f"[{label}] FAIL ({elapsed:.1f}s)")
                results.append((label, "FAIL"))
                if not args.no_stop:
                    print(f"\nStopping (--no-stop to continue past failures)")
                    break
        except Exception as e:
            elapsed = time.time() - start
            print(f"[{label}] ERROR: {e} ({elapsed:.1f}s)")
            results.append((label, "ERROR"))
            if not args.no_stop:
                print(f"\nStopping (--no-stop to continue past failures)")
                break
        finally:
            sys.argv = old_argv

    # Summary
    print(f"\n{'='*60}")
    print("PIPELINE SUMMARY")
    print(f"{'='*60}")
    for label, status in results:
        icon = "+" if status in ("PASS", "SKIPPED") else "!"
        print(f"  [{icon}] {label}: {status}")
    print(f"{'='*60}")

    all_ok = all(s in ("PASS", "SKIPPED") for _, s in results)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
