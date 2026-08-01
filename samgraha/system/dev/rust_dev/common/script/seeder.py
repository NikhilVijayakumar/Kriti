"""seeder.py -- rust_dev's seeder for samgraha's MCP activation path.

Reads common/schema-manifest/standard.yaml, creates rust_dev's dev_*
tables (common/schema/*.sql, via dev_schema.ensure_schema), seeds
domains/scripts/prompts/usecases (with steps) into knowledge.db.

Ported from pcems_2026/common/script/seeder.py's shape (proposal 6 §1's
reference: "same file pcems's seeder.py already builds its domain-lookup
data in") but simpler in one real way: rust_dev's standard.yaml already
declares each usecase's `steps:` directly (even when empty), so there is
no pcems-style name-prefix step-expansion table to maintain here -- this
file reads what standard.yaml says and writes exactly that. The one piece
of logic this file adds that pure struct-parsing (register_standard.rs's
now-dead per-repo path, per proposal 6 §1's confirmed read of
activate_standard) never had: resolving `domain:` -> `tier` via
plan/core/tiers.yaml and folding it into usecase.data as `tier`, proposal
6 §2's mechanism -- register_standard.rs's UsecaseDecl has no generic
`data:` passthrough, so this is the only place `tier` can be written.

Expected --in envelope: { _samgraha_dir, _knowledge_db } (matches every
other capability script's contract; db_path is recomputed from
--repo-root the same way _adapter.parse_step_args() does for every other
script, not read from the envelope -- same as pcems's seeder.py).
Returns: {"status": "ok"} on success.

Run by samgraha's activate_standard (crates/services/src/seeder.rs), not
standalone -- it deletes this standard's existing knowledge.db rows
immediately before invoking this script (register_standard.rs's
`delete_existing`, §3.9 step 3), so every insert below can assume a clean
slate; the SELECT-before-INSERT idempotency checks are kept anyway,
matching pcems's own defensive pattern, in case this script is ever run
twice against the same DB outside that flow.
"""
import json
import sys
from pathlib import Path

import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
RUST_DEV_ROOT = SCRIPT_DIR.parent.parent  # rust_dev/ (seeder.py lives at common/script/)
sys.path.insert(0, str(SCRIPT_DIR))
from _adapter import parse_step_args, write_envelope  # noqa: E402
import dev_schema  # noqa: E402


def _load_domain_tier_map():
    """plan/core/tiers.yaml's tiers: list -> {domain_key: tier_number}."""
    tiers_path = RUST_DEV_ROOT / "plan" / "core" / "tiers.yaml"
    with open(tiers_path, "r", encoding="utf-8") as f:
        tiers_doc = yaml.safe_load(f)
    domain_tier = {}
    for entry in tiers_doc.get("tiers", []):
        tier_number = entry["tier"]
        for domain_key in entry.get("domains", []):
            domain_tier[domain_key] = tier_number
    return domain_tier


def _resolve_location(location, manifest_dir):
    """location is relative to standard.yaml's own directory
    (common/schema-manifest/), per every standard.yaml's own header
    comment convention -- absolute already if it starts with a root."""
    loc = Path(location)
    if loc.is_absolute():
        return str(loc)
    return str((manifest_dir / location).resolve())


def _read_prompt_content(location, manifest_dir):
    target = Path(_resolve_location(location, manifest_dir))
    if target.exists():
        return target.read_text(encoding="utf-8")
    return f"[prompt file not found: {location} -> {target}]"


def main():
    repo_root, db_path, payload, out_path = parse_step_args()

    yaml_path = SCRIPT_DIR.parent / "schema-manifest" / "standard.yaml"
    manifest_dir = yaml_path.parent
    if not yaml_path.exists():
        write_envelope(out_path, status="error",
                        message=f"standard.yaml not found at {yaml_path}")
        return
    with open(yaml_path, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    standard = spec.get("name", "rust_dev")
    domain_tier = _load_domain_tier_map()

    conn = dev_schema.get_conn(db_path)

    # 1. Seed domains (samgraha's generic `domain` table -- rust_dev's own
    # dev_* tables have nothing domain-lookup-shaped to seed separately,
    # unlike pcems's academic_domains).
    domain_id_map = {}
    for d in spec.get("domains", []):
        key = d["key"]
        existing = conn.execute(
            "SELECT id FROM domain WHERE standard=? AND key=?",
            (standard, key),
        ).fetchone()
        if existing:
            domain_id_map[key] = existing["id"]
        else:
            cur = conn.execute(
                "INSERT INTO domain (standard, key, sort_order, description) VALUES (?, ?, ?, ?)",
                (standard, key, d.get("sort_order", 0), d.get("description", "")),
            )
            domain_id_map[key] = cur.lastrowid
    conn.commit()

    # 2. Insert scripts from standard.yaml (empty today -- proposal 3/5/7's
    # script content isn't written yet; this loop is a no-op until it is,
    # no seeder change needed when it lands).
    script_id_map = {}
    for s in spec.get("scripts", []):
        name = s["name"]
        abs_loc = _resolve_location(s["location"], manifest_dir)
        existing = conn.execute(
            "SELECT id FROM script WHERE standard=? AND name=?",
            (standard, name),
        ).fetchone()
        if existing:
            script_id_map[name] = existing["id"]
        else:
            cur = conn.execute(
                "INSERT INTO script (standard, name, location, purpose) VALUES (?, ?, ?, ?)",
                (standard, name, abs_loc, s.get("purpose", "")),
            )
            script_id_map[name] = cur.lastrowid

    # 3. Insert prompts from standard.yaml (also empty today, same reason).
    prompt_id_map = {}
    for p in spec.get("prompts", []):
        name = p["name"]
        content = _read_prompt_content(p["location"], manifest_dir)
        existing = conn.execute(
            "SELECT id FROM prompt WHERE standard=? AND name=?",
            (standard, name),
        ).fetchone()
        if existing:
            prompt_id_map[name] = existing["id"]
        else:
            cur = conn.execute(
                "INSERT INTO prompt (standard, name, content, purpose) VALUES (?, ?, ?, ?)",
                (standard, name, content, p.get("purpose", f"prompt: {name}")),
            )
            prompt_id_map[name] = cur.lastrowid
    conn.commit()

    # 4. Insert usecases + steps. `tier` is resolved here (proposal 6 §2)
    # and folded into usecase.data JSON -- the one thing the now-dead
    # generic struct-parsing path could never do (no data: passthrough).
    for uc in spec.get("usecases", []):
        uc_name = uc["name"]
        uc_desc = uc.get("description", "")
        domain_key = uc.get("domain")
        domain_id = domain_id_map.get(domain_key) if domain_key else None
        tier_number = domain_tier.get(domain_key) if domain_key else None

        data = {
            "driver": uc.get("driver", "samgraha"),
            "depends_on": uc.get("depends_on", []),
            "verify_script": uc.get("verify_script"),
        }
        if tier_number is not None:
            data["tier"] = tier_number

        existing_uc = conn.execute(
            "SELECT id FROM usecase WHERE standard=? AND name=?",
            (standard, uc_name),
        ).fetchone()
        if existing_uc:
            uc_id = existing_uc["id"]
            conn.execute(
                "UPDATE usecase SET description=?, domain_id=?, data=? WHERE id=?",
                (uc_desc, domain_id, json.dumps(data), uc_id),
            )
        else:
            cur = conn.execute(
                "INSERT INTO usecase (standard, name, description, domain_id, data) VALUES (?, ?, ?, ?, ?)",
                (standard, uc_name, uc_desc, domain_id, json.dumps(data)),
            )
            uc_id = cur.lastrowid

        for step in uc.get("steps", []):
            order = step["order"]
            kind = step["kind"]
            desc = step.get("description", "")

            existing_step = conn.execute(
                "SELECT id FROM step WHERE usecase_id=? AND step_order=?",
                (uc_id, order),
            ).fetchone()
            if existing_step:
                step_id = existing_step["id"]
            else:
                cur = conn.execute(
                    "INSERT INTO step (usecase_id, step_order, kind, description) VALUES (?, ?, ?, ?)",
                    (uc_id, order, kind, desc),
                )
                step_id = cur.lastrowid

            if kind == "deterministic" and "script" in step:
                sname = step["script"]
                if sname in script_id_map:
                    conn.execute(
                        "INSERT OR IGNORE INTO step_script (step_id, script_id) VALUES (?, ?)",
                        (step_id, script_id_map[sname]),
                    )
            elif kind == "semantic" and "prompt" in step:
                pname = step["prompt"]
                if pname in prompt_id_map:
                    conn.execute(
                        "INSERT OR IGNORE INTO step_prompt (step_id, prompt_id) VALUES (?, ?)",
                        (step_id, prompt_id_map[pname]),
                    )

    conn.commit()
    conn.close()

    write_envelope(out_path, status="ok",
                    message=f"rust_dev seeder: dev_* tables created, "
                            f"{len(domain_id_map)} domains, "
                            f"{len(script_id_map)} scripts, "
                            f"{len(prompt_id_map)} prompts, "
                            f"{len(spec.get('usecases', []))} usecases seeded")


if __name__ == "__main__":
    main()
