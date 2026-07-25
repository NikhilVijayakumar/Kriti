"""git_gate.py — pre-flight clean-tree gate for audit workflows.

Called once at the top of run_full_workflow.py. Aborts if the audited
repo has uncommitted changes — audit results must be reproducible
against a specific commit.
"""
import subprocess
from pathlib import Path


def require_clean_tree(repo_root):
    """Abort the whole workflow if repo_root has staged, unstaged,
    or untracked changes. No override — auditing uncommitted state
    defeats the purpose of recording commit_sha."""
    result = subprocess.run(
        ["git", "-C", str(repo_root), "status", "--porcelain"],
        capture_output=True, text=True, check=True)
    if result.stdout.strip():
        raise SystemExit(
            "audit blocked: uncommitted or untracked changes in "
            f"{repo_root}:\n{result.stdout}\n"
            "Commit these changes, or add them to .gitignore if they're "
            "not meant to be tracked, before running the audit. The "
            "deterministic and semantic audits record the commit hash "
            "they ran against — an audit against a dirty tree can't be "
            "reproduced or trusted later.")


def current_commit(repo_root):
    """Return the current HEAD commit SHA."""
    return subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True).stdout.strip()
