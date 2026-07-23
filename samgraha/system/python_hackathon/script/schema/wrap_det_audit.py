"""wrap_det_audit.py — samgraha adapter for run_det_audit.py (usecase 2a).
One call already loops every domain internally (DOMAIN_AUDIT_MODULES) —
that loop is not re-implemented here, only invoked."""
from _adapter import SCRIPTS_DIR, parse_step_args, run_driver, python_interpreter

DRIVER = SCRIPTS_DIR / "run_det_audit.py"


def main():
    repo_root, db_path, payload, out_path = parse_step_args()

    argv = [python_interpreter(repo_root), str(DRIVER), "--db", db_path,
            "--standard", payload.get("standard", "python_hackathon")]
    if payload.get("team"):
        argv += ["--team", payload["team"]]
    if payload.get("skip_existing"):
        argv.append("--skip-existing")

    run_driver(argv, out_path, repo_root)


if __name__ == "__main__":
    main()
