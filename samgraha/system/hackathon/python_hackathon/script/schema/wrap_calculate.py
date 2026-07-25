"""wrap_calculate.py — samgraha adapter for run_calculate.py (usecase 3)."""
from _adapter import SCRIPTS_DIR, parse_step_args, run_driver, python_interpreter

DRIVER = SCRIPTS_DIR / "run_calculate.py"


def main():
    repo_root, db_path, payload, out_path = parse_step_args()

    argv = [python_interpreter(repo_root), str(DRIVER), "--db", db_path,
            "--standard", payload.get("standard", "python_hackathon"),
            "--mode", payload.get("mode", "both")]
    if payload.get("output_dir"):
        argv += ["--output-dir", payload["output_dir"]]

    run_driver(argv, out_path, repo_root)


if __name__ == "__main__":
    main()
