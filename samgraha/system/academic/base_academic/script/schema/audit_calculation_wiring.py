"""audit_calculation_wiring.py — re-derives consumed_by for every row in
academic_calculation_dependencies by grepping known calculation-reading
scripts' source for references to calc_path. Static, source-level check
(not a runtime trace) — same trust level as the rest of this standard's
"confirmed by reading the script" evidence style. Run manually or as
part of a schema-health check; not wired into run_full_workflow.py's
per-paper pipeline (this is standard-level metadata, not per-run work)."""
import sys
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402

# Scripts known to read calculation YAML files at runtime.
# Paths are relative to the system dir (base_academic/).
_READER_SCRIPTS = {
    "calculate": "script/calculate/calculate.py",
    "check-word-budget": "script/assemble-paper-structure/check_word_budget.py",
    "deterministic-audit": "script/deterministic-audit/deterministic_audit.py",
}


def _load_script_contents():
    """Read each reader script once, return {name: content}. Resolved
    against base_academic's own directory (SCRIPTS_DIR.parent — SCRIPTS_
    DIR is base_academic/script/, imported from _adapter), never against
    --repo-root: _READER_SCRIPTS' paths (script/calculate/calculate.py,
    etc.) are part of the *standard*, not the target paper's repo — a
    target repo never has a script/calculate/calculate.py of its own.
    Using repo_root here would silently find nothing for every normal
    invocation (repo_root is always the audited paper's repo, per every
    other script's --repo-root/--in/--out contract in this standard)."""
    contents = {}
    base = SCRIPTS_DIR.parent
    for name, rel_path in _READER_SCRIPTS.items():
        full = base / rel_path
        if full.exists():
            contents[name] = full.read_text(encoding="utf-8")
    return contents


def _script_reads_calc_path(content, calc_path, domain_keys):
    """True if `content` looks like it reads calc_path. Two matches:
    exact literal (fixed-name files like report/summary/final_score.yaml,
    passed to _load_yaml() as one string) and directory-prefix, gated to
    domain-parameterized filenames only (generation/{domain}.yaml —
    confirmed by reading check_word_budget.py/deterministic_audit.py
    that neither ever contains the literal joined path, both build it as
    `.../ "generation" / f"{domain}.yaml"`).

    The directory-prefix fallback is deliberately restricted to
    calc_paths whose basename is a real domain key — confirmed the hard
    way that without this restriction, report/summary/final_score.yaml
    (a fixed name, never read by check-word-budget.py) false-positive-
    matched against check-word-budget.py anyway, because that script
    *also* reads report/summary/paper-budget.yaml (a different fixed
    file in the same directory) — its source legitimately contains the
    quoted literals "report" and "summary" for an unrelated reason, and
    a bare directory-segment check can't tell the two files in the same
    directory apart. Restricting the fallback to domain-parameterized
    names is exactly the case it needs to cover (a real f"{domain}.yaml"
    construction) and excludes every fixed-name file, which must match
    on the exact literal or not at all."""
    if calc_path in content:
        return True
    if "/" not in calc_path:
        return False
    stem = calc_path.rsplit("/", 1)[-1].removesuffix(".yaml")
    if stem not in domain_keys:
        return False
    dir_part = calc_path.rsplit("/", 1)[0]
    segments = dir_part.split("/")
    return all(f'"{seg}"' in content or f"'{seg}'" in content for seg in segments)


def audit(conn):
    """Check every dependency edge against reader script source.
    Returns list of (id, calc_path, old_consumed_by, new_consumed_by) drift rows.
    A calc_path can have more than one real reader (generation/{domain}.yaml
    is read by both check-word-budget and deterministic-audit) — collects
    every match, comma-joined, rather than stopping at the first (schema/23's
    consumed_by is a list, not a single winner)."""
    script_contents = _load_script_contents()
    domain_keys = {r[0] for r in conn.execute("SELECT key FROM academic_domains")}
    rows = conn.execute(
        "SELECT id, calc_path, consumed_by FROM academic_calculation_dependencies"
    ).fetchall()
    changed = []
    for row in rows:
        calc_path = row["calc_path"]
        readers = [name for name, content in script_contents.items()
                  if _script_reads_calc_path(content, calc_path, domain_keys)]
        actual_reader = ",".join(sorted(readers)) if readers else None
        if actual_reader != row["consumed_by"]:
            changed.append((row["id"], calc_path, row["consumed_by"], actual_reader))
        conn.execute(
            "UPDATE academic_calculation_dependencies "
            "SET consumed_by=?, last_audited_at=datetime('now') WHERE id=?",
            (actual_reader, row["id"]),
        )
    conn.commit()
    return changed


def main():
    _repo_root, db_path, payload, out_path = parse_step_args()
    conn = academic_schema.get_conn(db_path)
    try:
        changed = audit(conn)
        write_envelope(
            out_path,
            status="ok",
            message=f"audited {len(changed)} drift rows" if changed else "no drift",
            drift=changed,
        )
    finally:
        conn.close()


if __name__ == "__main__":
    main()
