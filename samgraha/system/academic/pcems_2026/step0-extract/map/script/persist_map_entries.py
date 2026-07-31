"""persist_map_entries.py — persist structured map entries (tables, figures,
equations, algorithms) from the LLM's structured output into the appropriate
academic_{table,figure,equation,algorithm}_map table.

Idempotent — re-running extracts that produce identical map_keys updates
existing rows in place.

Deterministic map_key override: the LLM provides the map_key in its output,
but the persist step re-derives it from content fields (caption for tables,
name for algorithms, asset_path for figures) and overrides the LLM's value
if it doesn't match. This guarantees rerun stability identical to proposal
01's _slugify() — the prompt instruction is a hint, not the enforcement
mechanism.

Expected --in payload:
  {paper_id: int, domain: str, entries: [{map_key, caption, ...}]}
  The entry shape varies by domain — keys beyond map_key are passed
  directly as column=value pairs.
"""
import re as _re
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys

sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
import academic_schema


def _slugify(text):
    text = text.lower().strip()
    text = _re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


def _derive_map_key(domain, entry, existing_keys):
    """Re-derive the expected map_key from content fields, overriding the
    LLM-provided one. Returns (map_key, corrected) where corrected is True
    if the key differed from what the entry originally carried."""
    llm_key = entry.get("map_key", "")
    expected = None

    if domain == "table":
        caption = entry.get("caption", "")
        if caption:
            expected = f"tbl-{_slugify(caption)}"
    elif domain == "algorithm":
        name = entry.get("name", "")
        if name:
            expected = f"alg-{_slugify(name)}"
    elif domain == "figure":
        asset_path = entry.get("asset_path", "")
        if asset_path:
            stem = _Path(asset_path).stem
            if stem:
                expected = f"fig-{_slugify(stem)}"
        if not expected:
            caption = entry.get("caption", "")
            if caption:
                expected = f"fig-{_slugify(caption)}"
    elif domain == "equation":
        # No deterministic slug source — defer to LLM-provided key
        expected = llm_key or None

    if not expected:
        expected = llm_key or "unknown"

    # Dedup against existing keys
    base = expected
    suffix = 2
    while expected in existing_keys:
        expected = f"{base}-{suffix}"
        suffix += 1
    existing_keys.add(expected)

    corrected = expected != llm_key
    return expected, corrected


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    domain = payload["domain"]
    entries = payload.get("entries", [])

    conn = academic_schema.get_conn(db_path)
    try:
        table, domain_id = academic_schema._map_info(domain)
    except ValueError:
        write_envelope(out_path, status="error",
                       message=f"unknown map domain: {domain}")
        conn.close()
        return

    try:
        # Pre-populate existing map_keys from DB for dedup
        existing_keys = set()
        for r in conn.execute(
            f"SELECT map_key FROM {table} WHERE paper_id=?",
            (paper_id,),
        ).fetchall():
            existing_keys.add(r["map_key"])

        inserted = 0
        updated = 0
        corrected_count = 0

        for entry in entries:
            # Override LLM's map_key with deterministic derivation
            map_key, corrected = _derive_map_key(domain, entry, existing_keys)
            entry.pop("map_key", None)  # remove LLM's key if present
            # Step 0 extracts, it doesn't decide which manuscript section
            # an asset belongs in — strip target_section even if the LLM
            # guessed one; a Step 1 assignment step fills it in later.
            entry.pop("target_section", None)
            if corrected:
                corrected_count += 1

            existing = conn.execute(
                f"SELECT id FROM {table} WHERE paper_id=? AND map_key=?",
                (paper_id, map_key),
            ).fetchone()

            if existing:
                set_cols = {k: v for k, v in entry.items()
                            if k not in ("paper_id", "map_key", "domain_id", "created_at")}
                if set_cols:
                    set_clause = ", ".join(f"{k}=?" for k in set_cols)
                    conn.execute(
                        f"UPDATE {table} SET {set_clause} WHERE id=?",
                        list(set_cols.values()) + [existing["id"]],
                    )
                updated += 1
            else:
                col_names = ["paper_id", "domain_id", "map_key", "created_at"]
                col_vals = [paper_id, domain_id, map_key, academic_schema.now_iso()]
                for k, v in entry.items():
                    if k not in ("paper_id", "domain_id", "map_key", "created_at"):
                        col_names.append(k)
                        col_vals.append(v)
                placeholders = ["?"] * len(col_names)
                conn.execute(
                    f"INSERT INTO {table} ({', '.join(col_names)}) "
                    f"VALUES ({', '.join(placeholders)})",
                    col_vals,
                )
                inserted += 1

        conn.commit()
    except Exception:
        conn.close()
        raise
    conn.close()

    msg = f"persisted {len(entries)} {domain} map entries ({inserted} new, {updated} updated)"
    if corrected_count:
        msg += f", {corrected_count} map_keys corrected to deterministic form"
    msg += f" for paper {paper_id}"

    write_envelope(out_path, status="ok",
                   message=msg,
                   paper_id=paper_id, domain=domain,
                   entry_count=len(entries),
                   inserted=inserted, updated=updated,
                   map_keys_corrected=corrected_count)


if __name__ == "__main__":
    main()
