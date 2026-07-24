"""classify_repo.py — entry router. Inspects the target repo to determine
its documentation state: NO_DOCS (refuse) or HAS_DOCS (proceed).
Persists to academic_repos.

Classification heuristic:
- has_implementation: any .py/.rs/.ts/.js source files beyond docs/config
  (kept as metadata for claim grounding, not used for branching)
- has_repo_documentation: scans the target repo's actual documentation
  surface (README, docs/, top-level .md files), excluding this pipeline's
  own output tree (docs/paper/). Requires >= min_doc_words total content.
"""
import os
import re
import sys
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402

SOURCE_EXTENSIONS = {".py", ".rs", ".ts", ".js", ".java", ".go", ".cpp", ".c", ".h"}
CONFIG_DIRS = {".git", ".github", ".vscode", ".idea", "__pycache__", "node_modules", ".venv", "venv"}
CONFIG_FILES = {"pyproject.toml", "setup.py", "setup.cfg", "Cargo.toml", "package.json",
                "requirements.txt", "go.mod", ".env", ".env.example"}

DEFAULT_MIN_DOC_WORDS = 200
DOC_EXCLUDE_PREFIXES = ("docs/paper",)


def count_source_files(repo_root):
    count = 0
    for dirpath, dirnames, filenames in os.walk(repo_root):
        dirnames[:] = [d for d in dirnames if d not in CONFIG_DIRS]
        rel = os.path.relpath(dirpath, repo_root)
        if rel.startswith(".") or rel.startswith("docs"):
            continue
        for f in filenames:
            if os.path.splitext(f)[1] in SOURCE_EXTENSIONS:
                count += 1
    return count


def _count_words(text):
    return len(re.findall(r'\S+', text))


def _scan_doc_file(filepath):
    """Read a documentation file and return its word count. Returns 0 on
    read errors or binary files."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            return _count_words(f.read())
    except (OSError, UnicodeDecodeError):
        return 0


def has_repo_documentation(repo_root, min_doc_words=DEFAULT_MIN_DOC_WORDS):
    """Scan the target repo's actual documentation surface.

    Surfaces checked:
    - README.md / README.rst at repo root
    - docs/** (excluding docs/paper/** which is this pipeline's output)
    - Any top-level *.md (CONTRIBUTING.md, ARCHITECTURE.md, etc.)

    Returns True only if total word count across all surfaces >= min_doc_words.
    """
    total_words = 0
    repo_str = str(repo_root)

    # 1. Root-level README
    for readme_name in ("README.md", "README.rst"):
        readme_path = os.path.join(repo_str, readme_name)
        if os.path.isfile(readme_path):
            total_words += _scan_doc_file(readme_path)

    # 2. docs/** (excluding docs/paper/**)
    docs_dir = os.path.join(repo_str, "docs")
    if os.path.isdir(docs_dir):
        for dirpath, dirnames, filenames in os.walk(docs_dir):
            rel = os.path.relpath(dirpath, repo_str)
            if any(rel.startswith(excl) for excl in DOC_EXCLUDE_PREFIXES):
                dirnames.clear()
                continue
            for f in filenames:
                if f.endswith((".md", ".rst", ".txt")):
                    total_words += _scan_doc_file(os.path.join(dirpath, f))

    # 3. Top-level *.md files (excluding README already counted)
    for f in os.listdir(repo_str):
        if f.endswith((".md", ".rst")) and f not in ("README.md", "README.rst"):
            fpath = os.path.join(repo_str, f)
            if os.path.isfile(fpath):
                total_words += _scan_doc_file(fpath)

    return total_words >= min_doc_words


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    standard = payload.get("standard", "base_academic")
    min_doc_words = payload.get("min_doc_words", DEFAULT_MIN_DOC_WORDS)

    repo_path = str(repo_root)
    src_count = count_source_files(repo_path)
    has_impl = src_count > 0
    has_docs = has_repo_documentation(repo_path, min_doc_words=min_doc_words)

    classification = "HAS_DOCS" if has_docs else "NO_DOCS"

    conn = academic_schema.get_conn(db_path)
    try:
        academic_schema.register_paper(conn, standard, repo_path)
        academic_schema.upsert_repo_classification(
            conn, standard, repo_path, classification,
            has_implementation=has_impl,
            metadata={"source_file_count": src_count, "min_doc_words": min_doc_words},
        )
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"repo classified as {classification} (impl={has_impl}, docs={has_docs}, src_files={src_count})",
                   classification=classification, has_implementation=has_impl,
                   has_docs=has_docs, source_file_count=src_count)


if __name__ == "__main__":
    main()
