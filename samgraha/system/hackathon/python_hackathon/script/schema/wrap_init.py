"""wrap_init.py — samgraha adapter for usecase-1-init/run_hackathon.py.
Translates the samgraha --repo-root/--in/--out contract into that script's
own --db/--standard/--team/--deterministic-only/--register CLI, unchanged."""
from _adapter import SCRIPTS_DIR, parse_step_args, run_driver, python_interpreter

DRIVER = SCRIPTS_DIR / "usecase-1-init" / "run_hackathon.py"


def main():
    repo_root, db_path, payload, out_path = parse_step_args()

    argv = [python_interpreter(repo_root), str(DRIVER), "--db", db_path,
            "--standard", payload.get("standard", "python_hackathon")]
    if payload.get("team"):
        argv += ["--team", payload["team"]]
    if payload.get("deterministic_only"):
        argv.append("--deterministic-only")
    if payload.get("register"):
        argv += ["--register", *payload["register"]]

    run_driver(argv, out_path, repo_root)


if __name__ == "__main__":
    main()
