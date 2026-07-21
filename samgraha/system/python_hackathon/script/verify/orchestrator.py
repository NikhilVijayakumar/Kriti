#!/usr/bin/env python3
"""orchestrator.py — Runs all use-case verify scripts in strict order."""
import argparse
import os
import sys

VERIFY_DIR = os.path.dirname(os.path.abspath(__file__))

UC_SCRIPTS = [
    ("1 - Init",              "uc1_init.py"),
    ("2a - Deterministic",    "uc2a_det.py"),
    ("2b - Semantic",         "uc2b_sem.py"),
    ("3 - Calculate",         "uc3_calc.py"),
    ("4 - Analysis",          "uc4_analysis.py"),
    ("5 - Markdown+Charts",   "uc5_markdown.py"),
    ("6 - HTML Report",       "uc6_html.py"),
    ("7 - PDF Generation",    "uc7_pdf.py"),
]


def run_verify(label, script_name, args_list):
    import importlib.util
    path = os.path.join(VERIFY_DIR, script_name)
    spec = importlib.util.spec_from_file_location(script_name, path)
    module = importlib.util.module_from_spec(spec)
    old_argv = sys.argv
    sys.argv = [script_name] + args_list
    try:
        spec.loader.exec_module(module)
        module.main()
        return True
    except SystemExit as e:
        return e.code == 0
    finally:
        sys.argv = old_argv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    parser.add_argument("--team", default=None)
    parser.add_argument("--no-stop-on-fail", dest="stop_on_fail",
                        action="store_false", default=True,
                        help="Run all 7 checks regardless of failures (default: stop at first failure)")
    args = parser.parse_args()

    extra = []
    if args.db:
        extra.extend(["--db", args.db])
    if args.team:
        extra.extend(["--team", args.team])
    std_flag = ["--standard", args.standard]

    results = []
    for label, script in UC_SCRIPTS:
        passed = run_verify(label, script, std_flag + extra)
        status = "PASS" if passed else "FAIL"
        results.append((label, status))
        print(f"  {label}: {status}")
        if not passed and args.stop_on_fail:
            break

    print("\n" + "=" * 50)
    for label, status in results:
        icon = "+" if status == "PASS" else "!"
        print(f"  [{icon}] {label}: {status}")
    print("=" * 50)

    all_pass = all(s == "PASS" for _, s in results)
    if all_pass:
        print("All checks passed.")
        sys.exit(0)
    else:
        print("Some checks failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
