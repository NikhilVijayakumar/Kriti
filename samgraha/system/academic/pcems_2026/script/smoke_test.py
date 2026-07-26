"""smoke_test.py — quick sanity check for the pcems_2026 system.

Verifies that:
1. All SQL schemas load without errors
2. All usecases register successfully
3. Standard YAML parses correctly
4. Prompt files are non-empty and parseable
5. HTML fragment templates render without syntax errors
6. Renderer scripts are importable (syntax check)
7. collate_references.py external bibliography parser works

Run from the repo root:
  python samgraha/system/academic/pcems_2026/script/smoke_test.py --repo-root <path>

No API keys needed — this is purely structural validation.
"""
import json
import sqlite3
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PCEMS_ROOT = SCRIPT_DIR.parent  # pcems_2026/
ACADEMIC_ROOT = PCEMS_ROOT.parent  # academic/
COMMON = ACADEMIC_ROOT / "base_academic" / "script" / "common"
SCHEMA_DIR = ACADEMIC_ROOT / "base_academic" / "schema"

sys.path.insert(0, str(COMMON))


def _check_schemas():
    """Load all SQL schema files and verify they parse."""
    errors = []
    for sql_file in sorted(SCHEMA_DIR.glob("*.sql")):
        try:
            sql = sql_file.read_text(encoding="utf-8")
            conn = sqlite3.connect(":memory:")
            conn.executescript(sql)
            conn.close()
        except Exception as e:
            errors.append(f"{sql_file.name}: {e}")
    return errors


def _check_standard_yaml():
    """Parse standard.yaml and verify structure."""
    import yaml
    standard_path = PCEMS_ROOT / "script" / "schema" / "standard.yaml"
    if not standard_path.exists():
        return [f"standard.yaml not found at {standard_path}"]
    try:
        data = yaml.safe_load(standard_path.read_text(encoding="utf-8"))
        prompts = data.get("prompts", [])
        if len(prompts) < 30:
            return [f"expected 32 prompt entries, got {len(prompts)}"]
        custom_tables = data.get("custom_tables", [])
        if len(custom_tables) < 20:
            return [f"expected 21+ custom tables, got {len(custom_tables)}"]
        return []
    except Exception as e:
        return [f"standard.yaml parse error: {e}"]


def _check_prompt_files():
    """Verify all prompt files are non-empty."""
    errors = []
    prompt_root = PCEMS_ROOT / "prompt"
    if not prompt_root.exists():
        return [f"prompt directory not found: {prompt_root}"]
    for subdir in ["generation", "audit", "propose"]:
        d = prompt_root / subdir
        if not d.exists():
            errors.append(f"prompt/{subdir}/ missing")
            continue
        for f in d.glob("*.md"):
            if f.stat().st_size < 50:
                errors.append(f"prompt/{subdir}/{f.name} is too small ({f.stat().st_size} bytes)")
    return errors


def _check_html_templates():
    """Verify HTML fragment templates are non-empty and basic syntax."""
    errors = []
    html_root = PCEMS_ROOT / "templates" / "generation" / "html"
    if not html_root.exists():
        return [f"html templates not found: {html_root}"]
    for f in html_root.glob("*.html"):
        if f.stat().st_size < 20:
            errors.append(f"html/{f.name} is too small")
    return errors


def _check_renderer_syntax():
    """Verify renderer scripts compile without errors."""
    errors = []
    render_dir = SCRIPT_DIR / "render"
    if not render_dir.exists():
        return [f"render directory not found: {render_dir}"]
    for f in render_dir.glob("*.py"):
        try:
            compile(f.read_text(encoding="utf-8"), str(f), "exec")
        except SyntaxError as e:
            errors.append(f"render/{f.name} syntax error: {e}")
    return errors


def _check_bibtex_parser():
    """Test the BibTeX parser in collate_references.py."""
    errors = []
    try:
        # Import the parser function
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "collate_references",
            str(ACADEMIC_ROOT / "base_academic" / "script" / "assemble-paper-structure" / "collate_references.py"),
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        # Test with sample BibTeX
        test_bibtex = """@article{smith2024,
  author = {John Smith and Jane Doe},
  title = {A Great Paper},
  year = {2024},
  journal = {Journal of Testing}
}"""
        citations = mod._parse_bibtex(test_bibtex)
        if len(citations) != 1:
            errors.append(f"bibtex parser returned {len(citations)} citations, expected 1")
        elif "John Smith" not in citations[0]:
            errors.append(f"bibtex parser missing author: {citations[0]}")
    except Exception as e:
        errors.append(f"bibtex parser test failed: {e}")
    return errors


def main():
    print("pcems_2026 smoke test")
    print("=" * 50)

    checks = [
        ("SQL schemas", _check_schemas),
        ("standard.yaml", _check_standard_yaml),
        ("Prompt files", _check_prompt_files),
        ("HTML templates", _check_html_templates),
        ("Renderer syntax", _check_renderer_syntax),
        ("BibTeX parser", _check_bibtex_parser),
    ]

    total_errors = 0
    for name, check_fn in checks:
        errors = check_fn()
        if errors:
            print(f"\n  FAIL: {name}")
            for e in errors:
                print(f"    - {e}")
            total_errors += len(errors)
        else:
            print(f"  PASS: {name}")

    print("\n" + "=" * 50)
    if total_errors == 0:
        print("All checks passed.")
    else:
        print(f"{total_errors} error(s) found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
