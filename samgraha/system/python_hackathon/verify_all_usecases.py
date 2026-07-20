#!/usr/bin/env python3
"""verify_all_usecases.py — Orchestrator: runs all use-case verify scripts in order."""
import argparse
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def run_verify(script_name, args_list):
    """Import and run a verify script's main() function."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        script_name, os.path.join(SCRIPT_DIR, script_name)
    )
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        old_argv = sys.argv
        sys.argv = [script_name] + args_list
        try:
            module.main()
        finally:
            sys.argv = old_argv
        return True
    except SystemExit as e:
        return e.code == 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--standard", default="python_hackathon")
    parser.add_argument("--db", default=None)
    parser.add_argument("--team", default=None)
    parser.add_argument("--stop-on-fail", action="store_true", default=True)
    args = parser.parse_args()

    extra = []
    if args.db:
        extra.extend(["--db", args.db])
    if args.team:
        extra.extend(["--team", args.team])

    std_flag = ["--standard", args.standard]

    scripts = [
        ("1 - Init", "verify_usecase_1_init.py"),
        ("2a - Deterministic Audit", "verify_usecase_2a_audit_deterministic.py"),
        ("2b - Semantic Audit", "verify_usecase_2b_audit_semantic.py"),
        ("3 - Calculate", "verify_usecase_3_calculate.py"),
        ("4 - Analysis", "verify_usecase_4_analysis.py"),
        ("5 - Markdown+Charts", "verify_usecase_5_markdown_charts.py"),
        ("6 - HTML Report", "verify_usecase_6_html_report.py"),
        ("7 - PDF Generation", "verify_usecase_7_pdf_generation.py"),
    ]

    results = []
    for label, script in scripts:
        passed = run_verify(script, std_flag + extra)
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
