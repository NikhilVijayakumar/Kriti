"""discover_modules.py — discover module boundaries (top-level packages)
in the target repo. Persists to academic_modules.
"""
import os
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def discover_top_level_packages(repo_root):
    packages = []
    repo_name = os.path.basename(str(repo_root))
    for item in sorted(os.listdir(str(repo_root))):
        item_path = os.path.join(str(repo_root), item)
        if not os.path.isdir(item_path):
            continue
        if item.startswith(".") or item.startswith("__"):
            continue
        if item in {"docs", "tests", "test", "scripts", "config", ".git",
                     "node_modules", ".venv", "venv", "__pycache__"}:
            continue
        has_code = False
        for root, dirs, files in os.walk(item_path):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in {"__pycache__", "node_modules", ".venv"}]
            if any(f.endswith((".py", ".rs", ".ts", ".js")) for f in files):
                has_code = True
                break
        if has_code:
            packages.append(item)
    return packages


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    standard = payload.get("standard", "base_academic")
    repo_path = str(repo_root)

    conn = academic_schema.get_conn(db_path)
    try:
        paper_id = academic_schema.register_paper(conn, standard, repo_path)
        packages = discover_top_level_packages(repo_path)
        for i, pkg in enumerate(packages):
            pkg_path = os.path.join(repo_path, pkg)
            academic_schema.upsert_module(conn, paper_id, pkg, pkg_path, sort_order=i)
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"discovered {len(packages)} modules: {', '.join(packages)}",
                   modules=packages, count=len(packages))


if __name__ == "__main__":
    main()
