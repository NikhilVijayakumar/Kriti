"""
_adapter.py — shared glue for samgraha's fixed capability-script contract
(--repo-root --in --out, JSON envelope out). Every wrap_*.py and glue script
here uses this to interact with samgraha. Direct glue scripts call
write_envelope() directly; wrapper scripts around existing drivers call
run_driver() to subprocess the driver and capture its exit status.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent


def parse_step_args():
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", required=True)
    p.add_argument("--in", dest="in_path", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    repo_root = Path(args.repo_root)
    in_file = Path(args.in_path)
    payload = json.loads(in_file.read_text()) if in_file.stat().st_size else {}
    db_path = str(repo_root / ".samgraha" / "knowledge.db")
    return repo_root, db_path, payload, Path(args.out)


def python_interpreter(repo_root):
    for candidate in (repo_root / ".venv" / "bin" / "python3", repo_root / ".venv" / "Scripts" / "python.exe"):
        if candidate.is_file():
            return str(candidate)
    return sys.executable


def _driver_env(repo_root):
    env = os.environ.copy()
    env_file = repo_root / ".env"
    if env_file.is_file():
        try:
            from dotenv import dotenv_values
            for k, v in dotenv_values(env_file).items():
                env.setdefault(k, v or "")
        except ImportError:
            pass
    return env


def run_driver(argv, out_path, repo_root=None):
    kwargs = {"capture_output": True, "text": True}
    if repo_root is not None:
        kwargs["cwd"] = str(repo_root)
        kwargs["env"] = _driver_env(repo_root)
    result = subprocess.run(argv, **kwargs)
    ok = result.returncode == 0
    envelope = {
        "status": "ok" if ok else "error",
        "message": (result.stdout or "")[-4000:] if ok else ((result.stderr or result.stdout or "")[-4000:]),
        "written": [],
    }
    out_path.write_text(json.dumps(envelope))
    return envelope


def write_envelope(out_path, status="ok", message="", **extra):
    envelope = {"status": status, "message": message, "written": [], **extra}
    out_path.write_text(json.dumps(envelope))
    return envelope
