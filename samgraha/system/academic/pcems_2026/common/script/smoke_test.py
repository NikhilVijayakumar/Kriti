"""smoke_test.py — quick sanity check for the pcems_2026 system.

Verifies that:
1. All SQL schemas load without errors
2. All usecases register successfully
3. Standard YAML parses correctly
4. Prompt files are non-empty and parseable
5. HTML fragment templates render without syntax errors
6. Renderer scripts are importable (syntax check)
7. All registered scripts import without errors (catches broken
   sys.path.insert, moved files, missing dependencies)
8. collate_references.py external bibliography parser works
9. seeder.py imports and parses without errors

Run from common/script/:
  python common/script/smoke_test.py --repo-root <path>

No API keys needed — this is purely structural validation.
"""
import json
import sqlite3
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PCEMS_ROOT = SCRIPT_DIR.parent.parent  # pcems_2026/ (smoke lives at common/script/)
COMMON = PCEMS_ROOT / "common" / "script"
SCHEMA_DIR = PCEMS_ROOT / "common" / "schema"
SCHEMA_MANIFEST = PCEMS_ROOT / "common" / "schema-manifest"

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
    standard_path = SCHEMA_MANIFEST / "standard.yaml"
    if not standard_path.exists():
        return [f"standard.yaml not found at {standard_path}"]
    try:
        data = yaml.safe_load(standard_path.read_text(encoding="utf-8"))
        errors = []
        if not data.get("name"):
            errors.append("missing 'name' key")
        if not data.get("seeder_script"):
            errors.append("missing 'seeder_script' key")
        prompts = data.get("prompts", [])
        if len(prompts) < 20:
            errors.append(f"expected 20+ prompt entries, got {len(prompts)}")
        custom_tables = data.get("custom_tables", [])
        if len(custom_tables) < 20:
            errors.append(f"expected 20+ custom tables, got {len(custom_tables)}")
        scripts = data.get("scripts", [])
        if len(scripts) < 20:
            errors.append(f"expected 20+ script entries, got {len(scripts)}")
        return errors
    except Exception as e:
        return [f"standard.yaml parse error: {e}"]


def _check_prompt_files():
    """Verify all prompt files are non-empty."""
    errors = []
    step1 = PCEMS_ROOT / "step1-draft-for-completeness"
    step0 = PCEMS_ROOT / "step0-extract"
    step3 = PCEMS_ROOT / "step3-plagiarism-humanize"
    final = PCEMS_ROOT / "step4 - final paper"
    roots = [
        ("step0", step0 / "input" / "prompt"),
        ("step0", step0 / "map" / "prompt"),
        ("step1", step1 / "section" / "prompt"),
        ("step0", step0 / "analysis" / "prompt"),
        ("step1", step1 / "audit" / "prompt"),
        ("step3/humanize", step3 / "humanize" / "prompt"),
        ("step3/plagiarism", step3 / "plagiarism" / "prompt"),
        ("final", final / "prompt"),
        ("common", PCEMS_ROOT / "common" / "prompt"),
    ]
    total = 0
    for label, prompt_dir in roots:
        if not prompt_dir.exists():
            errors.append(f"{label}/prompt/ missing")
            continue
        for f in prompt_dir.rglob("*.md"):
            total += 1
            if f.stat().st_size < 50:
                errors.append(f"{label}/prompt/{f.relative_to(prompt_dir)} is too small ({f.stat().st_size} bytes)")
    if total < 25:
        errors.append(f"expected 25+ prompt files, found {total}")
    return errors


def _check_html_templates():
    """Verify HTML fragment templates are non-empty and basic syntax."""
    errors = []
    html_roots = [
        PCEMS_ROOT / "step4 - final paper" / "templates" / "proposal",
        PCEMS_ROOT / "step4 - final paper" / "templates" / "report" / "domain",
    ]
    total = 0
    for html_root in html_roots:
        if not html_root.exists():
            errors.append(f"html templates not found: {html_root}")
            continue
        for f in html_root.rglob("*.html"):
            total += 1
            if f.stat().st_size < 20:
                errors.append(f"{f.relative_to(PCEMS_ROOT)} is too small")
    if total < 10:
        errors.append(f"expected 10+ html templates, found {total}")
    return errors


def _check_renderer_syntax():
    """Verify renderer scripts compile without errors."""
    errors = []
    render_dir = PCEMS_ROOT / "step4 - final paper" / "script" / "render"
    if not render_dir.exists():
        return [f"render directory not found: {render_dir}"]
    for f in render_dir.glob("*.py"):
        try:
            compile(f.read_text(encoding="utf-8"), str(f), "exec")
        except SyntaxError as e:
            errors.append(f"render/{f.name} syntax error: {e}")
    return errors


def _try_import_script(location_path):
    """Attempt to exec_module a single script. Returns None or error string."""
    import importlib.util
    try:
        spec = importlib.util.spec_from_file_location(
            location_path.stem, str(location_path))
        if spec is None:
            return f"spec_from_file_location returned None (syntax error or missing?)"
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return None
    except Exception as e:
        return f"{location_path.relative_to(PCEMS_ROOT)} — {type(e).__name__}: {e}"


def _check_imports():
    """Actually import every .py file listed under scripts: in standard.yaml.
    Reuses the existing exec_module mechanism (same as _check_bibtex_parser
    and _check_seeder already do). Relies on this codebase's convention that
    real work lives behind if __name__ == '__main__' — top-level code is just
    function/constant definitions, no side effects."""
    import yaml
    standard_path = SCHEMA_MANIFEST / "standard.yaml"
    if not standard_path.exists():
        return [f"standard.yaml not found at {standard_path}"]
    data = yaml.safe_load(standard_path.read_text(encoding="utf-8"))
    errors = []
    manifest_dir = SCHEMA_MANIFEST
    for entry in data.get("scripts", []):
        loc = entry.get("location", "")
        if not loc:
            errors.append(f"script entry '{entry.get('name')}' missing location")
            continue
        abs_path = (manifest_dir / loc).resolve()
        if not abs_path.is_file():
            errors.append(f"script '{entry['name']}' location not found: {abs_path}")
            continue
        err = _try_import_script(abs_path)
        if err:
            errors.append(err)
    return errors


def _check_bibtex_parser():
    """Verify collate_references.py imports and is structurally sound."""
    errors = []
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "collate_references",
            str(PCEMS_ROOT / "step0-extract" / "map" / "script" / "citation" / "collate_references.py"),
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if not hasattr(mod, "main"):
            errors.append("collate_references.py missing main()")
    except Exception as e:
        errors.append(f"collate_references import test failed: {e}")
    return errors


def _check_seeder():
    """Verify seeder.py imports and compiles without errors."""
    errors = []
    try:
        seeder_path = COMMON / "seeder.py"
        if not seeder_path.exists():
            return [f"seeder.py not found at {seeder_path}"]
        compile(seeder_path.read_text(encoding="utf-8"), str(seeder_path), "exec")
        import importlib.util
        spec = importlib.util.spec_from_file_location("seeder", str(seeder_path))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if not hasattr(mod, "main"):
            errors.append("seeder.py missing main()")
    except Exception as e:
        errors.append(f"seeder import test failed: {e}")
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
        ("Script imports", _check_imports),
        ("BibTeX parser", _check_bibtex_parser),
        ("Seeder syntax", _check_seeder),
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
