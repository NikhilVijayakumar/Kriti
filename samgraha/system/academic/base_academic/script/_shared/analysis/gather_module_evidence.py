"""gather_module_evidence.py — pre-script for module analysis triads.
Gathers one module's source files, imports, docstrings, signatures.

Expected --in payload: {paper_id: int, module_name: str}
"""
import ast
import os
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def analyze_python_file(filepath):
    info = {"path": "", "classes": [], "functions": [], "imports": [], "docstring": ""}
    info["path"] = filepath
    try:
        with open(filepath, encoding="utf-8", errors="replace") as f:
            source = f.read()
        tree = ast.parse(source, filename=filepath)
        info["docstring"] = ast.get_docstring(tree) or ""
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    info["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    info["imports"].append(node.module)
            elif isinstance(node, ast.ClassDef):
                cls = {"name": node.name, "docstring": ast.get_docstring(node) or "", "methods": []}
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        cls["methods"].append({
                            "name": item.name,
                            "docstring": ast.get_docstring(item) or "",
                            "args": [a.arg for a in item.args.args],
                        })
                info["classes"].append(cls)
            elif isinstance(node, ast.FunctionDef):
                info["functions"].append({
                    "name": node.name,
                    "docstring": ast.get_docstring(node) or "",
                    "args": [a.arg for a in node.args.args],
                })
    except (SyntaxError, ValueError):
        pass
    return info


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    module_name = payload["module_name"]

    conn = academic_schema.get_conn(db_path)
    try:
        paper = academic_schema.get_paper(conn, paper_id)
    finally:
        conn.close()

    repo_root_path = paper["repo_root"] if paper else str(repo_root)
    module_path = os.path.join(repo_root_path, module_name)

    files_info = []
    if os.path.isdir(module_path):
        for root, dirs, files in os.walk(module_path):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in {"__pycache__", "node_modules", ".venv"}]
            for f in sorted(files):
                fp = os.path.join(root, f)
                rel = os.path.relpath(fp, module_path)
                if f.endswith(".py"):
                    info = analyze_python_file(fp)
                    info["path"] = rel
                    files_info.append(info)
                elif f.endswith((".rs", ".ts", ".js", ".go")):
                    try:
                        with open(fp, encoding="utf-8", errors="replace") as fh:
                            content = fh.read()[:3000]
                        files_info.append({"path": rel, "content_preview": content})
                    except Exception:
                        pass
                if len(files_info) > 50:
                    break
            if len(files_info) > 50:
                break

    write_envelope(out_path, status="ok",
                   message=f"gathered evidence for module={module_name} ({len(files_info)} files)",
                   module_name=module_name, files=files_info, file_count=len(files_info))


if __name__ == "__main__":
    main()
