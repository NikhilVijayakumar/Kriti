"""
_adapter.py — shared glue for samgraha's fixed capability-script contract
(`--repo-root --in --out`, JSON envelope out). Every wrap_*.py here uses this
to call an existing scripts/*.py driver as a subprocess with translated CLI
args — the driver's own logic is never touched, only how it's invoked.
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
    """samgraha's own script_command() always spawns a wrap_*.py with the
    bare `python3` it finds on PATH (crates/common/src/env.rs's
    python_command() — no venv awareness, no per-repo config). That's fine
    for wrap_*.py itself (stdlib-only), but the *driver* it then subprocesses
    (run_render.py -> chevron, run_pdf.py -> pypdf/playwright, ...) needs
    whatever's in this repo's own .venv, not the bare interpreter. Use
    <repo_root>/.venv's python if it exists; fall back to sys.executable
    (matches the previous behavior) otherwise — never a hardcoded path."""
    for candidate in (repo_root / ".venv" / "bin" / "python3", repo_root / ".venv" / "Scripts" / "python.exe"):
        if candidate.is_file():
            return str(candidate)
    return sys.executable


def _driver_env(repo_root):
    """Every driver script (run_hackathon.py, export_team_pdfs.py, ...) reads
    its own config (PYTHON_HACKATHON_TEAMS_JSON etc) via os.environ, loaded
    through a bare `load_dotenv()` call that depends on python-dotenv's
    implicit caller-frame search — unreliable once the driver runs as a
    subprocess of samgraha's mcp binary instead of a directly-invoked script.
    Load <repo_root>/.env explicitly and merge it in (explicit env wins over
    .env, matching normal precedence) so this never depends on that search
    succeeding."""
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
    """Run an existing driver script as a subprocess, write its result as a
    samgraha capability envelope to out_path. Driver logic/output files are
    whatever the driver itself already produces — this only reports whether
    it exited cleanly."""
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
