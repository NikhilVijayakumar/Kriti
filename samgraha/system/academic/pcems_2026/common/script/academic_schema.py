"""
academic_schema.py — pcems_2026's own copy of the shared academic_*
normalized tables in knowledge.db, catalogued via standard.yaml's
custom_tables. Forked from base_academic/script/common/academic_schema.py
so pcems_2026 carries no cross-standard file references — samgraha
registers each standard's own catalog independently, so a standard
shouldn't reach into another's script/prompt/schema files. Diverges from
base_academic's copy over time; apply fixes to both if they still share
a bug.

Tables (DDL source of truth: schema/*.sql files, read by ensure_schema):
  academic_papers              — one row per registered paper (repo + system)
  academic_repos               — one row per (repo_root, system) classification result
                                 (2-state: NO_DOCS / HAS_DOCS)
  academic_domains             — lookup: scoring domains for the concrete system
  academic_modules             — one row per detected module in a repo
  academic_module_analysis     — per (module, analysis_kind) section content
  academic_cross_module_analysis — per (repo, analysis_kind) section content
  academic_narratives          — one row per (paper, domain) — stores section drafts
                                 with stage (generate/humanize) + iteration
  academic_narrative_sections  — per-narrative {heading, text} sections
  academic_semantic_runs       — append-only, one row per (paper, domain, model, run_number)
  academic_semantic_dimension_scores — per-dimension score+evidence for a semantic run
  academic_semantic_findings   — per-run strengths/weaknesses/recommendations
  academic_plagiarism_findings — per (paper, domain, run, pass_type, check_kind): PASS/FAIL + flagged spans
  academic_humanize_passes     — per (paper, domain, iteration): change summary + risk flags
  academic_templates           — catalog of markdown report templates on disk
  academic_score_history       — one row per calculate.py run (trend tracking)
  academic_visualization_types — chart type catalog
  academic_visualizations      — one row per rendered chart image
  academic_report_history      — one row per render run (paper or audit track)
  academic_deterministic_findings — per (paper, domain, run): deterministic audit verdict + findings
"""
import json
import os
import re
import sqlite3
from datetime import datetime, timezone

import yaml

_STANDARD = "pcems_2026"

_SCHEMA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "schema")
_CALC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "calculation")


def _paper_word_count(conn, paper_id, stage):
    """Sum word count across every domain's latest section text at a given
    stage — same \\b\\w+\\b counting check_word_budget.py uses per-domain,
    applied here across the whole paper."""
    rows = conn.execute(
        "SELECT s.text FROM academic_narrative_sections s "
        "JOIN academic_narratives n ON n.id = s.narrative_id "
        "WHERE n.paper_id=? AND n.stage=?",
        (paper_id, stage),
    ).fetchall()
    return sum(len(re.findall(r"\b\w+\b", r["text"] or "")) for r in rows)


def _paper_budget_range():
    """(min, max) from calculation/report/summary/paper-budget.yaml, or (None, None)
    if the file is absent — callers skip the total-budget check in that case."""
    path = os.path.normpath(os.path.join(_CALC_DIR, "report", "summary", "paper-budget.yaml"))
    if not os.path.exists(path):
        return None, None
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    total = data.get("total_word_count", {})
    return total.get("min"), total.get("max")


def ensure_schema(conn):
    """Read and execute all schema/*.sql files in order."""
    schema_dir = os.path.normpath(_SCHEMA_DIR)
    if not os.path.isdir(schema_dir):
        raise RuntimeError(f"schema directory not found: {schema_dir}")
    sql_files = sorted(f for f in os.listdir(schema_dir) if f.endswith(".sql"))
    for fname in sql_files:
        fpath = os.path.join(schema_dir, fname)
        with open(fpath, "r", encoding="utf-8") as fh:
            sql = fh.read()
        conn.executescript(sql)
    conn.commit()


def get_conn(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    ensure_schema(conn)
    return conn


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Paper helpers
# ---------------------------------------------------------------------------

def register_paper(conn, standard, repo_root, title="", paper_type="paper"):
    row = conn.execute(
        "SELECT id FROM academic_papers WHERE standard=? AND repo_root=?",
        (standard, repo_root),
    ).fetchone()
    if row:
        conn.execute(
            "UPDATE academic_papers SET title=?, updated_at=? WHERE id=?",
            (title or "", now_iso(), row["id"]),
        )
        conn.commit()
        return row["id"]
    ts = now_iso()
    cur = conn.execute(
        "INSERT INTO academic_papers (standard, repo_root, title, paper_type, status, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, 'draft', ?, ?)",
        (standard, repo_root, title or "", paper_type, ts, ts),
    )
    conn.commit()
    return cur.lastrowid


def get_paper(conn, paper_id):
    return conn.execute("SELECT * FROM academic_papers WHERE id=?", (paper_id,)).fetchone()


def set_paper_metadata(conn, paper_id, key, value):
    """Set a single key in the paper's metadata JSON blob."""
    import json
    paper = get_paper(conn, paper_id)
    if not paper:
        return
    meta = {}
    if paper["metadata"]:
        try:
            meta = json.loads(paper["metadata"])
        except (TypeError, ValueError):
            pass
    meta[key] = value
    conn.execute(
        "UPDATE academic_papers SET metadata=?, updated_at=? WHERE id=?",
        (json.dumps(meta), now_iso(), paper_id),
    )
    conn.commit()


_ALLOWED_METADATA_KEYS = {
    "schema": None,  # None = object, any sub-keys OK (meta-schema info)
    "paper": {"id", "slug", "title", "short_title", "language", "document_type"},
    "publication": {
        "profile", "venue_full_name", "page_limit", "word_limit",
        "link", "call_for_paper", "guideline", "submission_type",
    },
    "authors": {"corresponding_author", "authors"},
    "affiliations": None,  # array of objects — each item checked separately
    "classification": {"language", "domain", "research_area", "keywords"},
    "modules": {"primary", "dependent", "cross_library"},
    "status": {"stage", "version", "created", "updated"},
    "custom": ...,  # sentinel: any keys allowed
}

_ALLOWED_AUTHOR_KEYS = {
    "id", "order", "title", "first_name", "middle_name", "last_name",
    "full_name", "role", "email", "affiliation", "orcid",
    "google_scholar", "linkedin",
}

_ALLOWED_AFFILIATION_KEYS = {
    "id", "institution", "department", "city", "state", "country",
}

_ALLOWED_MODULE_PRIMARY_KEYS = {
    "name", "path", "interest_weight", "existing_draft", "draft",
}

_ALLOWED_MODULE_DEPENDENT_KEYS = {
    "name", "path", "interest_weight", "reason",
}


def _walk_unknown_keys(data, path, allowed, problems):
    """Recursively walk ``data`` and append ``path`` strings to
    ``problems`` for keys not present in ``allowed``.

    ``allowed`` conventions:
    ``...`` (Ellipsis) — any key at this level is OK (escape hatch).
    ``None`` — treat value as opaque; no sub-key check.
    ``set()`` — exact set of allowed keys; recurse into each sub-value if
    it is a dict (whose allowed keys are determined by the caller).
    """
    if not isinstance(data, dict):
        return
    if allowed is ...:
        return
    if allowed is None:
        return
    for key in data:
        if key not in allowed:
            problems.append(f"unexpected key '{'.'.join(path + [key])}'")
            continue
        val = data[key]
        sub_path = path + [key]
        if key == "authors":
            if isinstance(val, dict):
                _walk_unknown_keys(val, sub_path, _ALLOWED_AUTHOR_KEYS.union({"authors", "corresponding_author"}), problems)
                author_list = val.get("authors", [])
                if isinstance(author_list, list):
                    for i, a in enumerate(author_list):
                        if isinstance(a, dict):
                            _walk_unknown_keys(a, sub_path + [str(i)], _ALLOWED_AUTHOR_KEYS, problems)
        elif key == "affiliations":
            if isinstance(val, list):
                for i, af in enumerate(val):
                    if isinstance(af, dict):
                        _walk_unknown_keys(af, sub_path + [str(i)], _ALLOWED_AFFILIATION_KEYS, problems)
        elif key == "modules":
            if isinstance(val, dict):
                _walk_unknown_keys(val, sub_path, {"primary", "dependent", "cross_library"}, problems)
                primary = val.get("primary")
                if isinstance(primary, dict):
                    _walk_unknown_keys(primary, sub_path + ["primary"], _ALLOWED_MODULE_PRIMARY_KEYS, problems)
                dep_list = val.get("dependent", [])
                if isinstance(dep_list, list):
                    for i, dep in enumerate(dep_list):
                        if isinstance(dep, dict):
                            _walk_unknown_keys(dep, sub_path + ["dependent", str(i)], _ALLOWED_MODULE_DEPENDENT_KEYS, problems)
        elif isinstance(val, dict):
            # allowed may be a flat set (e.g. the modules: top-level check) —
            # only dict-shaped `allowed` carries per-key sub-schemas to
            # recurse into; a flat set means this level's own recursion
            # (if any) is handled explicitly by the caller (see "modules"
            # branch above for primary/dependent), not generically here.
            sub_allowed = allowed.get(key) if isinstance(allowed, dict) else None
            if sub_allowed is not None and sub_allowed is not ...:
                _walk_unknown_keys(val, sub_path, sub_allowed, problems)


def validate_paper_metadata(data):
    """Validate paper metadata dict (parsed yaml). Returns list of
    problem strings — empty list = valid.

    Enforces a schema-lock: any key not in _ALLOWED_METADATA_KEYS at
    any nesting depth is reported as 'unexpected key'.  The ``custom``
    top-level key is the escape hatch (any sub-keys allowed).
    """
    problems = []

    # Schema-lock: reject unknown keys at all levels
    _walk_unknown_keys(data, [], _ALLOWED_METADATA_KEYS, problems)

    paper = data.get("paper", {})
    if not paper.get("id"):
        problems.append("paper.id is missing or empty")
    if not paper.get("title"):
        problems.append("paper.title is missing or empty")

    authors_block = data.get("authors", {})
    author_list = authors_block.get("authors", [])
    if not author_list:
        problems.append("authors.authors[] is empty or missing")
    else:
        author_ids = set()
        for i, a in enumerate(author_list):
            if not a.get("full_name"):
                problems.append(f"authors.authors[{i}].full_name is missing or empty")
            email = a.get("email", "")
            if email and not re.match(r".+@.+\..+", email):
                problems.append(f"authors.authors[{i}].email '{email}' does not match basic email pattern")
            aid = a.get("id")
            if aid is not None:
                author_ids.add(aid)
            else:
                problems.append(f"authors.authors[{i}].id is missing")

        corresponding = authors_block.get("corresponding_author")
        if corresponding is not None and corresponding not in author_ids:
            problems.append(
                f"authors.corresponding_author={corresponding} does not "
                f"reference any id in authors.authors[]"
            )

    affiliations_list = data.get("affiliations", [])
    if not affiliations_list:
        problems.append("affiliations[] is empty or missing")
    aff_ids = {a.get("id") for a in affiliations_list if a.get("id") is not None}

    if author_list:
        for i, a in enumerate(author_list):
            aff_ref = a.get("affiliation")
            if aff_ref is not None and aff_ref not in aff_ids:
                problems.append(
                    f"authors.authors[{i}].affiliation={aff_ref} does not "
                    f"reference any id in affiliations[]"
                )

    modules_block = data.get("modules", {})
    dep_list = modules_block.get("dependent", [])
    for i, dep in enumerate(dep_list):
        if isinstance(dep, dict) and not dep.get("reason"):
            problems.append(f"modules.dependent[{i}].reason is missing or empty")

    pub = data.get("publication", {})
    vfn = pub.get("venue_full_name")
    if vfn is not None and not isinstance(vfn, str):
        problems.append("publication.venue_full_name must be a string or absent")
    pl = pub.get("page_limit")
    if pl is not None and (not isinstance(pl, int) or pl < 1):
        problems.append("publication.page_limit must be a positive integer or absent")
    wl = pub.get("word_limit")
    if wl is not None and (not isinstance(wl, int) or wl < 1):
        problems.append("publication.word_limit must be a positive integer or absent")

    return problems


# ---------------------------------------------------------------------------
# Map helpers (extraction-map tables 27-30)
# ---------------------------------------------------------------------------

_MAP_TABLES = {
    "table":     "academic_table_map",
    "figure":    "academic_figure_map",
    "equation":  "academic_equation_map",
    "algorithm": "academic_algorithm_map",
}

_MAP_DOMAIN_IDS = {
    "table":     15,
    "figure":    16,
    "equation":  10,
    "algorithm": 10,
}


def _map_info(domain):
    table = _MAP_TABLES.get(domain)
    if not table:
        raise ValueError(f"unknown map domain: {domain} (expected one of {list(_MAP_TABLES)})")
    domain_id = _MAP_DOMAIN_IDS.get(domain)
    return table, domain_id


def insert_map_entry(conn, paper_id, domain, map_key, **cols):
    """Insert or update (by paper_id+map_key) a map entry.

    Accepted keyword columns vary by domain — they are passed directly as
    SQL column=value pairs. `domain_id` is auto-resolved from the domain
    key. `created_at` is auto-set on insert only.

    Returns the row id.
    """
    table, domain_id = _map_info(domain)
    ts = now_iso()
    existing = conn.execute(
        f"SELECT id FROM {table} WHERE paper_id=? AND map_key=?",
        (paper_id, map_key),
    ).fetchone()
    if existing:
        if cols:
            set_clause = ", ".join(f"{k}=?" for k in cols)
            conn.execute(
                f"UPDATE {table} SET {set_clause} WHERE id=?",
                list(cols.values()) + [existing["id"]],
            )
            conn.commit()
        return existing["id"]
    col_names = ["paper_id", "domain_id", "map_key", "created_at"] + list(cols.keys())
    placeholders = ["?"] * len(col_names)
    vals = [paper_id, domain_id, map_key, ts] + list(cols.values())
    cur = conn.execute(
        f"INSERT INTO {table} ({', '.join(col_names)}) "
        f"VALUES ({', '.join(placeholders)})",
        vals,
    )
    conn.commit()
    return cur.lastrowid


def get_map(conn, paper_id, domain, order_by="map_key"):
    """Fetch all map entries for a paper+domain, ordered."""
    table, _ = _map_info(domain)
    rows = conn.execute(
        f"SELECT * FROM {table} WHERE paper_id=? ORDER BY {order_by}",
        (paper_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def get_map_entry(conn, paper_id, domain, map_key):
    """Fetch a single map entry by map_key."""
    table, _ = _map_info(domain)
    row = conn.execute(
        f"SELECT * FROM {table} WHERE paper_id=? AND map_key=?",
        (paper_id, map_key),
    ).fetchone()
    return dict(row) if row else None


def delete_map_entry(conn, paper_id, domain, map_key):
    """Delete a single map entry by map_key. Returns True if a row was deleted."""
    table, _ = _map_info(domain)
    cur = conn.execute(
        f"DELETE FROM {table} WHERE paper_id=? AND map_key=?",
        (paper_id, map_key),
    )
    conn.commit()
    return cur.rowcount > 0


def count_map_entries(conn, paper_id, domain):
    """Count map entries for a paper+domain."""
    table, _ = _map_info(domain)
    row = conn.execute(
        f"SELECT COUNT(*) AS cnt FROM {table} WHERE paper_id=?",
        (paper_id,),
    ).fetchone()
    return row["cnt"] if row else 0


# ---------------------------------------------------------------------------
# Repo classification
# ---------------------------------------------------------------------------

def upsert_repo_classification(conn, standard, repo_root, classification,
                                has_implementation=False, module_count=0, metadata=None):
    ts = now_iso()
    existing = conn.execute(
        "SELECT id FROM academic_repos WHERE standard=? AND repo_root=?",
        (standard, repo_root),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE academic_repos SET classification=?, has_implementation=?, "
            "module_count=?, metadata=?, updated_at=? WHERE id=?",
            (classification, int(has_implementation),
             module_count, json.dumps(metadata or {}), ts, existing["id"]),
        )
        conn.commit()
        return existing["id"]
    cur = conn.execute(
        "INSERT INTO academic_repos (standard, repo_root, classification, has_implementation, "
        "module_count, metadata, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (standard, repo_root, classification, int(has_implementation),
         module_count, json.dumps(metadata or {}), ts, ts),
    )
    conn.commit()
    return cur.lastrowid


def get_repo_classification(conn, standard, repo_root):
    row = conn.execute(
        "SELECT * FROM academic_repos WHERE standard=? AND repo_root=?",
        (standard, repo_root),
    ).fetchone()
    return dict(row) if row else None


# ---------------------------------------------------------------------------
# Domain helpers
# ---------------------------------------------------------------------------

def seed_domains(conn, domains_list):
    """Seed domains from a list of (key, display_name, sort_order, weight) tuples.
    Idempotent — safe to call every init-schema run."""
    for key, display_name, sort_order, weight in domains_list:
        conn.execute(
            "INSERT INTO academic_domains (key, display_name, sort_order, weight) "
            "VALUES (?, ?, ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET "
            "display_name=excluded.display_name, sort_order=excluded.sort_order, weight=excluded.weight",
            (key, display_name, sort_order, weight),
        )
    conn.commit()


def get_all_domains(conn):
    """[(id, key, display_name, sort_order), ...] ordered by sort_order."""
    rows = conn.execute(
        "SELECT id, key, display_name, sort_order FROM academic_domains ORDER BY sort_order"
    ).fetchall()
    return [(r["id"], r["key"], r["display_name"], r["sort_order"]) for r in rows]


def get_domain_id(conn, domain_key):
    row = conn.execute("SELECT id FROM academic_domains WHERE key=?", (domain_key,)).fetchone()
    return row["id"] if row else None


# ---------------------------------------------------------------------------
# Module helpers
# ---------------------------------------------------------------------------

def upsert_module(conn, paper_id, module_name, module_path="", sort_order=0,
                  role="primary", interest_weight=0.5, reason="",
                  existing_draft_publisher="", existing_draft_status="", existing_draft_path=""):
    existing = conn.execute(
        "SELECT id FROM academic_modules WHERE paper_id=? AND module_name=?",
        (paper_id, module_name),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE academic_modules SET module_path=?, sort_order=?, "
            "role=?, interest_weight=?, reason=?, "
            "existing_draft_publisher=?, existing_draft_status=?, existing_draft_path=? "
            "WHERE id=?",
            (module_path, sort_order,
             role, interest_weight, reason,
             existing_draft_publisher, existing_draft_status, existing_draft_path,
             existing["id"]),
        )
        conn.commit()
        return existing["id"]
    cur = conn.execute(
        "INSERT INTO academic_modules "
        "(paper_id, module_name, module_path, sort_order, "
        " role, interest_weight, reason, "
        " existing_draft_publisher, existing_draft_status, existing_draft_path) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (paper_id, module_name, module_path, sort_order,
         role, interest_weight, reason,
         existing_draft_publisher, existing_draft_status, existing_draft_path),
    )
    conn.commit()
    return cur.lastrowid


def get_modules(conn, paper_id):
    rows = conn.execute(
        "SELECT id, module_name, module_path, role, interest_weight, reason, "
        "existing_draft_publisher, existing_draft_status, existing_draft_path, sort_order "
        "FROM academic_modules WHERE paper_id=? ORDER BY sort_order", (paper_id,)
    ).fetchall()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Module analysis helpers
# ---------------------------------------------------------------------------

def upsert_module_analysis(conn, module_id, analysis_kind, content, model="", file_path=""):
    ts = now_iso()
    existing = conn.execute(
        "SELECT id FROM academic_module_analysis WHERE module_id=? AND analysis_kind=?",
        (module_id, analysis_kind),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE academic_module_analysis SET content=?, model=?, file_path=?, created_at=? WHERE id=?",
            (content, model, file_path, ts, existing["id"]),
        )
    else:
        conn.execute(
            "INSERT INTO academic_module_analysis (module_id, analysis_kind, content, model, file_path, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (module_id, analysis_kind, content, model, file_path, ts),
        )
    conn.commit()


def get_module_analysis(conn, module_id, analysis_kind=None):
    if analysis_kind:
        row = conn.execute(
            "SELECT * FROM academic_module_analysis WHERE module_id=? AND analysis_kind=?",
            (module_id, analysis_kind),
        ).fetchone()
        return dict(row) if row else None
    rows = conn.execute(
        "SELECT * FROM academic_module_analysis WHERE module_id=? ORDER BY id", (module_id,)
    ).fetchall()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Cross-module analysis helpers
# ---------------------------------------------------------------------------

def upsert_cross_module_analysis(conn, paper_id, analysis_kind, content, model="", file_path=""):
    ts = now_iso()
    existing = conn.execute(
        "SELECT id FROM academic_cross_module_analysis WHERE paper_id=? AND analysis_kind=?",
        (paper_id, analysis_kind),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE academic_cross_module_analysis SET content=?, model=?, file_path=?, created_at=? WHERE id=?",
            (content, model, file_path, ts, existing["id"]),
        )
    else:
        conn.execute(
            "INSERT INTO academic_cross_module_analysis (paper_id, analysis_kind, content, model, file_path, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (paper_id, analysis_kind, content, model, file_path, ts),
        )
    conn.commit()


def get_cross_module_analysis(conn, paper_id, analysis_kind=None):
    if analysis_kind:
        row = conn.execute(
            "SELECT * FROM academic_cross_module_analysis WHERE paper_id=? AND analysis_kind=?",
            (paper_id, analysis_kind),
        ).fetchone()
        return dict(row) if row else None
    rows = conn.execute(
        "SELECT * FROM academic_cross_module_analysis WHERE paper_id=? ORDER BY id", (paper_id,)
    ).fetchall()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Narrative / section-draft helpers
# ---------------------------------------------------------------------------

def upsert_narrative(conn, paper_id, domain, sections, stage="generate",
                     iteration=0, validated=False, model=None):
    domain_id = get_domain_id(conn, domain) if domain else None
    ts = now_iso()
    existing = conn.execute(
        "SELECT id FROM academic_narratives WHERE paper_id=? AND domain_id IS ? AND stage=? AND iteration=?",
        (paper_id, domain_id, stage, iteration),
    ).fetchone()
    if existing:
        narrative_id = existing["id"]
        conn.execute(
            "UPDATE academic_narratives SET validated=?, model=?, created_at=? WHERE id=?",
            (int(validated), model or "", ts, narrative_id),
        )
        conn.execute("DELETE FROM academic_narrative_sections WHERE narrative_id=?", (narrative_id,))
    else:
        cur = conn.execute(
            "INSERT INTO academic_narratives (standard, paper_id, domain_id, stage, iteration, validated, model, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (_STANDARD, paper_id, domain_id, stage, iteration, int(validated), model or "", ts),
        )
        narrative_id = cur.lastrowid

    for i, section in enumerate(sections or []):
        conn.execute(
            "INSERT INTO academic_narrative_sections (narrative_id, heading, text, sort_order) VALUES (?, ?, ?, ?)",
            (narrative_id, section.get("heading", ""), section.get("text", ""), i),
        )
    conn.commit()


def get_narrative(conn, paper_id, domain, stage=None, iteration=None):
    domain_id = get_domain_id(conn, domain) if domain else None
    conditions = ["paper_id=?", "domain_id IS ?"]
    params = [paper_id, domain_id]
    if stage:
        conditions.append("stage=?")
        params.append(stage)
    if iteration is not None:
        conditions.append("iteration=?")
        params.append(iteration)
    where = " AND ".join(conditions)
    row = conn.execute(
        f"SELECT id FROM academic_narratives WHERE {where} ORDER BY iteration DESC LIMIT 1",
        params,
    ).fetchone()
    if not row:
        return None
    sections = conn.execute(
        "SELECT heading, text FROM academic_narrative_sections WHERE narrative_id=? ORDER BY sort_order",
        (row["id"],),
    ).fetchall()
    return [{"heading": s["heading"], "text": s["text"]} for s in sections]


def get_latest_narrative_info(conn, paper_id, domain):
    """Return (stage, iteration, validated) for the most recent narrative of a domain."""
    domain_id = get_domain_id(conn, domain) if domain else None
    row = conn.execute(
        "SELECT stage, iteration, validated FROM academic_narratives "
        "WHERE paper_id=? AND domain_id IS ? ORDER BY iteration DESC LIMIT 1",
        (paper_id, domain_id),
    ).fetchone()
    return (row["stage"], row["iteration"], bool(row["validated"])) if row else None


# ---------------------------------------------------------------------------
# Section citation helpers — APPEND-ONLY
# ---------------------------------------------------------------------------

def insert_section_citation(conn, paper_id, domain, source_kind, citation):
    """Insert a single citation for a (paper, domain).  source_kind is 'in-repo' or 'literature'."""
    domain_id = get_domain_id(conn, domain)
    ts = now_iso()
    conn.execute(
        "INSERT INTO academic_section_citations (paper_id, domain_id, source_kind, citation, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (paper_id, domain_id, source_kind, citation, ts),
    )
    conn.commit()


def get_section_citations(conn, paper_id, domain=None, source_kind=None):
    """Return all citations for a paper, optionally filtered by domain and/or source_kind."""
    conditions = ["paper_id=?"]
    params = [paper_id]
    if domain:
        conditions.append("domain_id=(SELECT id FROM academic_domains WHERE key=?)")
        params.append(domain)
    if source_kind:
        conditions.append("source_kind=?")
        params.append(source_kind)
    where = " AND ".join(conditions)
    rows = conn.execute(
        f"SELECT c.*, d.key AS domain_key FROM academic_section_citations c "
        f"JOIN academic_domains d ON d.id=c.domain_id "
        f"WHERE {where} ORDER BY c.id",
        params,
    ).fetchall()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Literature citation helpers — academic_literature_citation table (schema/22)
# ---------------------------------------------------------------------------

def get_literature_citations(conn, paper_id):
    """Return all literature citations for a paper, ordered by number."""
    rows = conn.execute(
        "SELECT * FROM academic_literature_citation "
        "WHERE paper_id=? ORDER BY number",
        (paper_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def insert_literature_citation(conn, paper_id, cite_key, authors, year,
                               title, venue="", volume="", issue="",
                               pages="", doi="", raw_markdown="", number=None):
    """UPSERT a literature citation by paper_id + cite_key."""
    ts = now_iso()
    existing = conn.execute(
        "SELECT id FROM academic_literature_citation "
        "WHERE paper_id=? AND cite_key=?",
        (paper_id, cite_key),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE academic_literature_citation SET "
            "number=?, authors=?, year=?, title=?, venue=?, volume=?, "
            "issue=?, pages=?, doi=?, raw_markdown=?, created_at=? "
            "WHERE id=?",
            (number, authors, year, title, venue, volume, issue,
             pages, doi, raw_markdown, ts, existing["id"]),
        )
        conn.commit()
        return existing["id"]
    cur = conn.execute(
        "INSERT INTO academic_literature_citation "
        "(paper_id, cite_key, number, authors, year, title, venue, "
        "volume, issue, pages, doi, raw_markdown, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (paper_id, cite_key, number, authors, year, title, venue,
         volume, issue, pages, doi, raw_markdown, ts),
    )
    conn.commit()
    return cur.lastrowid


def update_paper_identity(conn, paper_id, title, metadata=None):
    """Update academic_papers title and metadata JSON blob."""
    metadata_json = json.dumps(metadata or {})
    conn.execute(
        "UPDATE academic_papers SET title=?, metadata=?, updated_at=? WHERE id=?",
        (title, metadata_json, now_iso(), paper_id),
    )
    conn.commit()


# ---------------------------------------------------------------------------
# Section profile helpers — academic_section_profile table (schema/31)
# ---------------------------------------------------------------------------

def get_section_profile(conn, paper_id, domain_key=None):
    """Return section profile row(s) for a paper.

    When domain_key is None, returns all profiles for the paper (as a list
    of dicts).  When domain_key is given, returns a single dict or None."""
    if domain_key:
        row = conn.execute(
            "SELECT p.*, d.key AS domain_key "
            "FROM academic_section_profile p "
            "JOIN academic_domains d ON d.id=p.domain_id "
            "WHERE p.paper_id=? AND d.key=?",
            (paper_id, domain_key),
        ).fetchone()
        return dict(row) if row else None
    rows = conn.execute(
        "SELECT p.*, d.key AS domain_key "
        "FROM academic_section_profile p "
        "JOIN academic_domains d ON d.id=p.domain_id "
        "WHERE p.paper_id=? ORDER BY d.sort_order",
        (paper_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def upsert_section_profile(conn, paper_id, domain_key, word_budget=None,
                            source_analysis=None, profile_notes=""):
    """Insert or update a section profile for (paper, domain).

    source_analysis is stored as a JSON array of analysis_kind strings
    (e.g. ['novelty', 'gaps', 'figures'])."""
    domain_id = get_domain_id(conn, domain_key)
    if domain_id is None:
        raise ValueError(f"unknown domain '{domain_key}'")
    import json
    ts = now_iso()
    existing = conn.execute(
        "SELECT id FROM academic_section_profile "
        "WHERE paper_id=? AND domain_id=?",
        (paper_id, domain_id),
    ).fetchone()
    source_json = json.dumps(source_analysis or [])
    if existing:
        conn.execute(
            "UPDATE academic_section_profile SET "
            "word_budget=?, source_analysis=?, profile_notes=?, updated_at=? "
            "WHERE id=?",
            (word_budget, source_json, profile_notes, ts, existing["id"]),
        )
        conn.commit()
        return existing["id"]
    cur = conn.execute(
        "INSERT INTO academic_section_profile "
        "(paper_id, domain_id, word_budget, source_analysis, profile_notes, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (paper_id, domain_id, word_budget, source_json, profile_notes, ts, ts),
    )
    conn.commit()
    return cur.lastrowid


# ---------------------------------------------------------------------------
# Keyword map helpers — academic_keyword_map table (schema/32)
# ---------------------------------------------------------------------------

def get_keyword_map(conn, paper_id, module_id=None):
    """Return keyword_map rows for a paper.  When module_id is given,
    returns only that module's rows.  Each row includes module_name."""
    if module_id:
        rows = conn.execute(
            "SELECT m.*, r.name AS module_name FROM academic_keyword_map m "
            "JOIN academic_modules r ON r.id=m.module_id "
            "WHERE m.paper_id=? AND m.module_id=? "
            "ORDER BY m.keyword",
            (paper_id, module_id),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT m.*, r.name AS module_name FROM academic_keyword_map m "
            "JOIN academic_modules r ON r.id=m.module_id "
            "WHERE m.paper_id=? ORDER BY r.name, m.keyword",
            (paper_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def upsert_keyword_map(conn, paper_id, module_id, keyword,
                       relevance_note="", source_evidence=""):
    """Insert or update a keyword_map row.  Returns the row id."""
    ts = now_iso()
    existing = conn.execute(
        "SELECT id FROM academic_keyword_map "
        "WHERE paper_id=? AND module_id=? AND keyword=?",
        (paper_id, module_id, keyword),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE academic_keyword_map SET "
            "relevance_note=?, source_evidence=?, created_at=? "
            "WHERE id=?",
            (relevance_note, source_evidence, ts, existing["id"]),
        )
        conn.commit()
        return existing["id"]
    cur = conn.execute(
        "INSERT INTO academic_keyword_map "
        "(paper_id, module_id, keyword, relevance_note, source_evidence, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (paper_id, module_id, keyword, relevance_note, source_evidence, ts),
    )
    conn.commit()
    return cur.lastrowid


def verify_keyword_coverage(conn, paper_id, declared_keywords):
    """Compare discovered keyword_map rows against declared_keywords list.
    Returns dict: {gaps: [...], candidates: [...], covered: [...], missed: [...]}"""
    rows = conn.execute(
        "SELECT DISTINCT keyword FROM academic_keyword_map WHERE paper_id=?",
        (paper_id,),
    ).fetchall()
    discovered = {r["keyword"] for r in rows}
    declared = set(declared_keywords or [])
    return {
        "covered": sorted(declared & discovered),
        "missed": sorted(declared - discovered),
        "gaps": sorted(discovered - declared),  # un-declared keywords found in modules
        "candidates": sorted(discovered - declared),
    }


# ---------------------------------------------------------------------------
# Semantic score helpers — APPEND-ONLY (no UPDATE, no DELETE)
# ---------------------------------------------------------------------------

def upsert_semantic_score(conn, paper_id, domain, model, score, result=None,
                          scope="section-full", part_kind=None,
                          commit_sha=""):
    """Append a new semantic run.  Never updates or deletes existing rows.
    run_number auto-increments per (paper, domain, scope, model, part_kind).
    scope='cross-section' or 'document' → domain must be None.
    part_kind is only meaningful when scope='section-part' — one of
    'citations', 'enrichment', 'budget-fit'.  NULL for all other scopes.
    commit_sha is the git commit this audit ran against — used for
    skip-if-unchanged cache checks in the orchestrator."""
    domain_id = None
    if scope in ("section-full", "section-part"):
        domain_id = get_domain_id(conn, domain)
        if domain_id is None:
            raise ValueError(f"unknown domain '{domain}' — not in academic_domains")
    ts = now_iso()
    result = result or {}
    reasoning = result.get("reasoning", "")

    max_run = conn.execute(
        "SELECT COALESCE(MAX(run_number), 0) FROM academic_semantic_runs "
        "WHERE paper_id=? AND domain_id IS ? AND scope=? AND model=? "
        "AND part_kind IS ?",
        (paper_id, domain_id, scope, model or "", part_kind),
    ).fetchone()[0]
    cur = conn.execute(
        "INSERT INTO academic_semantic_runs "
        "(standard, paper_id, domain_id, scope, model, run_number, overall_score, reasoning, part_kind, commit_sha, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (_STANDARD, paper_id, domain_id, scope, model or "", max_run + 1, score, reasoning,
         part_kind, commit_sha, ts),
    )
    run_id = cur.lastrowid

    for dim_key, dim in (result.get("dimension_scores") or {}).items():
        dim_score = dim.get("score") if isinstance(dim, dict) else dim
        dim_evidence = dim.get("evidence", "") if isinstance(dim, dict) else ""
        conn.execute(
            "INSERT INTO academic_semantic_dimension_scores (run_id, dimension_key, score, evidence) "
            "VALUES (?, ?, ?, ?)", (run_id, dim_key, dim_score, dim_evidence),
        )

    for finding_type, key in (("strength", "strengths"), ("weakness", "weaknesses"), ("recommendation", "recommendations")):
        for i, text in enumerate(result.get(key) or []):
            conn.execute(
                "INSERT INTO academic_semantic_findings (run_id, finding_type, text, sort_order) VALUES (?, ?, ?, ?)",
                (run_id, finding_type, text, i),
            )
    conn.commit()


def get_domain_scores(conn, paper_id, domain=None, scope="section-full"):
    domain_filter = "AND d.key=?" if domain else ""
    params = (paper_id, domain) if domain else (paper_id,)
    rows = conn.execute(
        f"SELECT d.key AS domain, s.model, s.overall_score, s.reasoning "
        f"FROM academic_semantic_runs s JOIN academic_domains d ON d.id=s.domain_id "
        f"WHERE s.paper_id=? AND s.scope=? {domain_filter}",
        (paper_id, scope) + params,
    ).fetchall()
    return [dict(r) for r in rows]


def get_latest_semantic_score(conn, paper_id, domain, model="", scope="section-full"):
    """Get the most recent semantic run for a (paper, domain, model, scope)."""
    if scope in ("section-full", "section-part"):
        domain_id = get_domain_id(conn, domain)
        where = "WHERE paper_id=? AND domain_id=? AND scope=?"
        params = (paper_id, domain_id, scope)
    else:
        where = "WHERE paper_id=? AND domain_id IS NULL AND scope=?"
        params = (paper_id, scope)
    if model:
        where += " AND model=?"
        params += (model,)
    row = conn.execute(
        f"SELECT * FROM academic_semantic_runs {where} "
        "ORDER BY run_number DESC LIMIT 1",
        params,
    ).fetchone()
    return dict(row) if row else None


# ---------------------------------------------------------------------------
# Usecase dependency / completion predicates
# ---------------------------------------------------------------------------

# Registry: usecase_name → (description, predicate_fn)
# predicate_fn(conn, paper_id) → (complete: bool, detail: list[str])
_USECASE_PREDICATES = {}


def _register_usecase(name, description):
    """Decorator to register a usecase completion predicate."""
    def decorator(fn):
        _USECASE_PREDICATES[name] = (description, fn)
        return fn
    return decorator


def _register_usecase_fn(name, description, fn):
    """Non-decorator form — used by the per-domain registration loops below,
    where the predicate is built by a factory closure instead of a literal
    def. Same registry, same usecase_status() lookup either way."""
    _USECASE_PREDICATES[name] = (description, fn)


# base_academic's own 12 structural domains, per _master-schema.yaml's
# sections: list (order matches). Hardcoded here per
# base_academic-usecase-atomicity-proposal.md's per-domain usecase split —
# a concrete system with a different domain set gets its own copy of the
# per-domain usecase files/predicates/registry entries when it's built
# (same override surface it already has for templates/rubrics), since
# these predicates are looked up by name at call time, not derived from
# academic_domains at import time.
STRUCTURAL_DOMAINS = [
    "title-and-metadata", "abstract", "introduction", "related-work",
    "problem-definition", "methodology", "experimental-setup", "results",
    "discussion", "limitations", "conclusion", "references",
]
GENERATED_DOMAINS = [d for d in STRUCTURAL_DOMAINS if d != "references"]
CITE_CONTEXT_DOMAINS = {"related-work", "introduction", "discussion"}


def _domain_id(conn, key):
    row = conn.execute("SELECT id FROM academic_domains WHERE key=?", (key,)).fetchone()
    return row["id"] if row else None


def usecase_status(conn, paper_id, usecase_name):
    """Returns (complete: bool, detail: list[str]) for a usecase's
    completion criteria. Same predicate backs both the CLI verify script
    and the runtime dependency gate."""
    if usecase_name not in _USECASE_PREDICATES:
        for prefix, factory in _PER_DOMAIN_PREDICATE_FACTORIES:
            if usecase_name.startswith(prefix):
                domain = usecase_name[len(prefix):]
                if _domain_id(conn, domain) is not None:
                    return factory(domain)(conn, paper_id)
                break
        return False, [f"unknown usecase '{usecase_name}'"]
    _, fn = _USECASE_PREDICATES[usecase_name]
    return fn(conn, paper_id)


@_register_usecase("schema-init", "21 academic_* tables exist")
def _uc_schema_init(conn, paper_id):
    tables = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name LIKE 'academic_%'"
    ).fetchall()
    names = {r[0] for r in tables}
    required = {
        "academic_papers", "academic_repos", "academic_domains",
        "academic_modules", "academic_module_analysis",
        "academic_cross_module_analysis", "academic_narratives",
        "academic_narrative_sections", "academic_semantic_runs",
        "academic_semantic_dimension_scores", "academic_semantic_findings",
        "academic_plagiarism_findings", "academic_humanize_passes",
        "academic_templates", "academic_score_history",
        "academic_deterministic_findings",
        "academic_visualization_types", "academic_visualizations",
        "academic_report_history",
        "academic_section_citations",   # fixes pre-existing gap
        "academic_literature_citation", # curated literature citations (schema/22)
        "academic_proposal_review",     # proposal gate (schema/24)
        "academic_proposal_scope",      # proposal scope (schema/25)
        "academic_proposal_analysis_ref",  # proposal analysis refs (schema/26)
        "academic_calculation_dependencies",  # calc dependency edges
        "academic_section_profile",  # section profiles (schema/31)
        "academic_keyword_map",  # keyword coverage (schema/32)
    }
    missing = required - names
    if missing:
        return False, [f"missing tables: {', '.join(sorted(missing))}"]
    return True, ["all tables present"]


@_register_usecase("classify-repo", "academic_repos has HAS_DOCS classification")
def _uc_classify_repo(conn, paper_id):
    row = conn.execute(
        "SELECT r.classification FROM academic_repos r "
        "JOIN academic_papers p ON p.standard=r.standard AND p.repo_root=r.repo_root "
        "WHERE p.id=?",
        (paper_id,),
    ).fetchone()
    if not row:
        return False, ["no classification row"]
    if row["classification"] != "HAS_DOCS":
        return False, [f"classification={row['classification']}"]
    return True, [f"classification={row['classification']}"]


def _uc_analysis_kind(conn, paper_id, kind, label=None):
    """Generic predicate: at least 1 cross-module {kind} analysis exists."""
    row = conn.execute(
        "SELECT COUNT(*) FROM academic_cross_module_analysis "
        "WHERE paper_id=? AND analysis_kind=?",
        (paper_id, kind),
    ).fetchone()
    count = row[0]
    display = label or kind
    if count < 1:
        return False, [f"{display} analyses: {count}"]
    return True, [f"{display} analyses: {count}"]


_register_usecase_fn("novelty-analysis",
    "at least 1 cross-module novelty analysis exists",
    lambda conn, pid: _uc_analysis_kind(conn, pid, "novelty", "novelty"))

_register_usecase_fn("gap-analysis",
    "at least 1 cross-module gap analysis exists",
    lambda conn, pid: _uc_analysis_kind(conn, pid, "gaps", "gap"))

_register_usecase_fn("mathematics-analysis",
    "at least 1 cross-module mathematics analysis exists",
    lambda conn, pid: _uc_analysis_kind(conn, pid, "mathematics", "math"))

_register_usecase_fn("figures-analysis",
    "at least 1 cross-module figures analysis exists",
    lambda conn, pid: _uc_analysis_kind(conn, pid, "figures", "figures"))

_register_usecase_fn("tables-analysis",
    "at least 1 cross-module tables analysis exists",
    lambda conn, pid: _uc_analysis_kind(conn, pid, "tables", "tables"))


@_register_usecase("build-keyword-map",
                    "at least 1 academic_keyword_map row exists")
def _uc_keyword_map(conn, paper_id):
    row = conn.execute(
        "SELECT COUNT(*) FROM academic_keyword_map WHERE paper_id=?",
        (paper_id,),
    ).fetchone()
    count = row[0]
    if count < 1:
        return False, [f"keyword_map entries: {count}"]
    return True, [f"keyword_map entries: {count}"]


@_register_usecase("diagram-architecture-analysis",
                    "at least 1 cross-module architecture/dependencies/interactions analysis exists")
def _uc_diagram_analysis(conn, paper_id):
    row = conn.execute(
        "SELECT COUNT(*) FROM academic_cross_module_analysis "
        "WHERE paper_id=? AND analysis_kind IN ('architecture','dependencies','interactions')",
        (paper_id,),
    ).fetchone()
    count = row[0]
    if count < 1:
        return False, [f"architecture analyses: {count}"]
    return True, [f"architecture analyses: {count}"]


# ---------------------------------------------------------------------------
# Per-domain usecase registration — generate-section-draft, section-citations,
# section-enrichment, section-budget-fit each get one usecase
# PER STRUCTURAL DOMAIN (base_academic-usecase-atomicity-proposal.md's
# per-domain split) instead of one usecase looping every domain. Each
# predicate below checks exactly one domain — a factory closure per domain,
# registered in a loop, not 40+ hand-duplicated functions.
# ---------------------------------------------------------------------------

def _make_stage_predicate(domain, stage):
    def predicate(conn, paper_id):
        row = conn.execute(
            "SELECT COUNT(*) FROM academic_narratives "
            "WHERE paper_id=? AND domain_id=? AND stage=?",
            (paper_id, _domain_id(conn, domain), stage),
        ).fetchone()
        if row[0] < 1:
            return False, [f"{domain}: no stage='{stage}' narrative"]
        return True, [f"{domain}: stage='{stage}' narrative present"]
    return predicate


for _domain in GENERATED_DOMAINS:
    _register_usecase_fn(
        f"generate-section-draft-{_domain}",
        f"{_domain} has a stage='generate' narrative",
        _make_stage_predicate(_domain, "generate"),
    )

# Cross-cutting generate usecases (novelty, gaps, mathematics) — not in
# GENERATED_DOMAINS but follow the same stage='generate' predicate.
for _domain in ("novelty", "gaps", "mathematics"):
    _register_usecase_fn(
        f"generate-section-draft-{_domain}",
        f"{_domain} has a stage='generate' narrative",
        _make_stage_predicate(_domain, "generate"),
    )


def _make_citation_predicate(domain):
    def predicate(conn, paper_id):
        row = conn.execute(
            "SELECT COUNT(*) FROM academic_section_citations "
            "WHERE paper_id=? AND domain_id=?",
            (paper_id, _domain_id(conn, domain)),
        ).fetchone()
        if row[0] < 1:
            return False, [f"{domain}: no citations"]
        return True, [f"{domain}: {row[0]} citations"]
    return predicate


for _domain in GENERATED_DOMAINS:
    _register_usecase_fn(
        f"section-citations-{_domain}",
        f"{_domain} has >= 1 citation in academic_section_citations",
        _make_citation_predicate(_domain),
    )


def _uc_section_citations_references(conn, paper_id):
    """Fan-in usecase — depends on every other domain's section-citations-*
    usecase completing first (enforced by collate_references.py calling
    usecase_status() per domain before it collates, not by this predicate,
    which only checks its own output exists)."""
    row = conn.execute(
        "SELECT COUNT(*) FROM academic_narratives "
        "WHERE paper_id=? AND domain_id=? AND stage='cite'",
        (paper_id, _domain_id(conn, "references")),
    ).fetchone()
    if row[0] < 1:
        return False, ["references: no stage='cite' narrative (collation not run)"]
    return True, ["references: collated"]


_register_usecase_fn(
    "section-citations-references",
    "references domain has a stage='cite' narrative collated from all other domains",
    _uc_section_citations_references,
)


for _domain in STRUCTURAL_DOMAINS:
    _register_usecase_fn(
        f"section-enrichment-{_domain}",
        f"{_domain} has a stage='enrich' narrative",
        _make_stage_predicate(_domain, "enrich"),
    )


def _make_budget_predicate(domain):
    def predicate(conn, paper_id):
        row = conn.execute(
            "SELECT COUNT(*) FROM academic_narratives "
            "WHERE paper_id=? AND domain_id=? AND stage='budget-fit'",
            (paper_id, _domain_id(conn, domain)),
        ).fetchone()
        if row[0] < 1:
            return False, [f"{domain}: no stage='budget-fit' narrative"]
        return True, [f"{domain}: stage='budget-fit' narrative present"]
    return predicate


for _domain in STRUCTURAL_DOMAINS:
    _register_usecase_fn(
        f"section-budget-fit-{_domain}",
        f"{_domain} has a stage='budget-fit' narrative",
        _make_budget_predicate(_domain),
    )


def _uc_section_budget_fit_total(conn, paper_id):
    """Fan-in usecase — whole-paper total is not a per-domain concern,
    same pattern as section-citations-references."""
    total_wc = _paper_word_count(conn, paper_id, "budget-fit")
    paper_min, paper_max = _paper_budget_range()
    if paper_min is not None and not (paper_min <= total_wc <= paper_max):
        return False, [f"whole-paper word count {total_wc} outside budget "
                        f"[{paper_min},{paper_max}] (calculation/report/summary/paper-budget.yaml)"]
    return True, [f"total_wc={total_wc}"]


_register_usecase_fn(
    "section-budget-fit-total",
    "whole-paper word count is within calculation/report/summary/paper-budget.yaml's range",
    _uc_section_budget_fit_total,
)


@_register_usecase("document-narrative-polish",
                    "every structural domain has a stage='polish' narrative + total in range")
def _uc_document_polish(conn, paper_id):
    # Query domains that have generate-stage narratives (i.e. domains
    # that go through the generation pipeline).  This correctly handles
    # concrete systems that rename structural domains (e.g. "findings"
    # instead of generic "results") without hardcoding names.
    domains = conn.execute(
        "SELECT DISTINCT ad.key FROM academic_domains ad "
        "JOIN academic_narratives an ON an.domain_id = ad.id "
        "WHERE an.stage = 'generate' "
        "ORDER BY ad.sort_order"
    ).fetchall()
    missing = []
    for (dk,) in domains:
        row = conn.execute(
            "SELECT COUNT(*) FROM academic_narratives "
            "WHERE paper_id=? AND domain_id=(SELECT id FROM academic_domains WHERE key=?) "
            "AND stage='polish'",
            (paper_id, dk),
        ).fetchone()
        if row[0] < 1:
            missing.append(dk)
    if missing:
        return False, [f"missing polish narratives: {', '.join(missing)}"]
    total_wc = _paper_word_count(conn, paper_id, "polish")
    paper_min, paper_max = _paper_budget_range()
    if paper_min is not None and not (paper_min <= total_wc <= paper_max):
        return False, [f"whole-paper word count {total_wc} outside budget "
                        f"[{paper_min},{paper_max}] (calculation/report/summary/paper-budget.yaml)"]
    return True, [f"all {len(domains)} domains have polish narratives, "
                  f"total_wc={total_wc}"]


def _make_det_audit_predicate(domain):
    def predicate(conn, paper_id):
        row = conn.execute(
            "SELECT verdict FROM academic_deterministic_findings "
            "WHERE paper_id=? AND domain_id=? "
            "ORDER BY run_number DESC LIMIT 1",
            (paper_id, _domain_id(conn, domain)),
        ).fetchone()
        if not row or row["verdict"] != "PASS":
            return False, [f"{domain}: verdict={row['verdict'] if row else 'none'}"]
        return True, [f"{domain}: PASS"]
    return predicate


for _domain in STRUCTURAL_DOMAINS:
    _register_usecase_fn(
        f"deterministic-audit-{_domain}",
        f"{_domain} has a PASS deterministic verdict",
        _make_det_audit_predicate(_domain),
    )


def _make_sem_audit_predicate(domain):
    def predicate(conn, paper_id):
        row = conn.execute(
            "SELECT COUNT(*) FROM academic_semantic_runs "
            "WHERE paper_id=? AND scope='section-full' AND domain_id=?",
            (paper_id, _domain_id(conn, domain)),
        ).fetchone()
        if row[0] < 1:
            return False, [f"{domain}: no section-full semantic run"]
        return True, [f"{domain}: {row[0]} semantic run(s)"]
    return predicate


for _domain in STRUCTURAL_DOMAINS:
    _register_usecase_fn(
        f"semantic-audit-{_domain}",
        f"{_domain} has >= 1 semantic run with scope='section-full'",
        _make_sem_audit_predicate(_domain),
    )


def _make_plagiarism_predicate(domain):
    def predicate(conn, paper_id):
        row = conn.execute(
            "SELECT verdict FROM academic_plagiarism_findings "
            "WHERE paper_id=? AND pass_type='forensic' AND domain_id=? "
            "ORDER BY run_number DESC LIMIT 1",
            (paper_id, _domain_id(conn, domain)),
        ).fetchone()
        if not row:
            return False, [f"{domain}: no forensic verdict"]
        return True, [f"{domain}: verdict={row['verdict']}"]
    return predicate


for _domain in STRUCTURAL_DOMAINS:
    _register_usecase_fn(
        f"plagiarism-forensic-audit-{_domain}",
        f"{_domain} has a forensic plagiarism verdict",
        _make_plagiarism_predicate(_domain),
    )


def _domain_flagged(conn, paper_id, domain):
    row = conn.execute(
        "SELECT 1 FROM academic_plagiarism_findings "
        "WHERE paper_id=? AND domain_id=? AND verdict='FAIL' AND pass_type='forensic' LIMIT 1",
        (paper_id, _domain_id(conn, domain)),
    ).fetchone()
    return row is not None


def _make_humanize_det_predicate(domain):
    def predicate(conn, paper_id):
        if not _domain_flagged(conn, paper_id, domain):
            return True, [f"{domain}: not flagged, no-op"]
        row = conn.execute(
            "SELECT COUNT(*) FROM academic_humanize_passes "
            "WHERE paper_id=? AND domain_id=? AND pass_kind='deterministic'",
            (paper_id, _domain_id(conn, domain)),
        ).fetchone()
        if row[0] < 1:
            return False, [f"{domain}: flagged, no deterministic pass"]
        return True, [f"{domain}: deterministic pass present"]
    return predicate


for _domain in STRUCTURAL_DOMAINS:
    _register_usecase_fn(
        f"humanize-deterministic-{_domain}",
        f"{_domain}: if flagged by plagiarism-forensic-audit, has >= 1 deterministic humanize pass",
        _make_humanize_det_predicate(_domain),
    )


def _make_humanize_sem_predicate(domain):
    def predicate(conn, paper_id):
        if not _domain_flagged(conn, paper_id, domain):
            return True, [f"{domain}: not flagged, no-op"]
        det_row = conn.execute(
            "SELECT COUNT(*) FROM academic_humanize_passes "
            "WHERE paper_id=? AND domain_id=? AND pass_kind='deterministic'",
            (paper_id, _domain_id(conn, domain)),
        ).fetchone()
        if det_row[0] < 1:
            return True, [f"{domain}: flagged but deterministic pass not run yet, no-op"]
        sem_row = conn.execute(
            "SELECT COUNT(*) FROM academic_humanize_passes "
            "WHERE paper_id=? AND domain_id=? AND pass_kind='semantic'",
            (paper_id, _domain_id(conn, domain)),
        ).fetchone()
        if sem_row[0] < 1:
            return False, [f"{domain}: flagged, deterministic pass done, no semantic pass"]
        return True, [f"{domain}: semantic pass present"]
    return predicate


for _domain in STRUCTURAL_DOMAINS:
    _register_usecase_fn(
        f"humanize-semantic-{_domain}",
        f"{_domain}: if still flagged after deterministic pass, has >= 1 semantic humanize pass",
        _make_humanize_sem_predicate(_domain),
    )


# Fallback for concrete systems whose domain keys don't match
# STRUCTURAL_DOMAINS/GENERATED_DOMAINS (e.g. pcems_2026's "findings" vs
# base_academic's generic "results") — the loops above only pre-register
# usecase names for base_academic's own 12 domains. Rather than requiring
# every concrete system to hand-copy these ~9 registration loops with its
# own domain list, resolve any {prefix}-{domain} name whose domain key
# actually exists in academic_domains directly against the same factories.
_PER_DOMAIN_PREDICATE_FACTORIES = [
    ("generate-section-draft-", lambda d: _make_stage_predicate(d, "generate")),
    ("section-citations-", _make_citation_predicate),
    ("section-enrichment-", lambda d: _make_stage_predicate(d, "enrich")),
    ("section-budget-fit-", _make_budget_predicate),
    ("deterministic-audit-", _make_det_audit_predicate),
    ("semantic-audit-", _make_sem_audit_predicate),
    ("plagiarism-forensic-audit-", _make_plagiarism_predicate),
    ("humanize-deterministic-", _make_humanize_det_predicate),
    ("humanize-semantic-", _make_humanize_sem_predicate),
]


@_register_usecase("cross-section-semantic-audit",
                    ">= 1 run with scope='cross-section'")
def _uc_cross_section(conn, paper_id):
    row = conn.execute(
        "SELECT COUNT(*) FROM academic_semantic_runs "
        "WHERE paper_id=? AND scope='cross-section'",
        (paper_id,),
    ).fetchone()
    if row[0] < 1:
        return False, ["no cross-section runs"]
    return True, [f"cross-section runs: {row[0]}"]


@_register_usecase("document-semantic-audit",
                    ">= 1 run with scope='document'")
def _uc_document(conn, paper_id):
    row = conn.execute(
        "SELECT COUNT(*) FROM academic_semantic_runs "
        "WHERE paper_id=? AND scope='document'",
        (paper_id,),
    ).fetchone()
    if row[0] < 1:
        return False, ["no document runs"]
    return True, [f"document runs: {row[0]}"]


@_register_usecase("reviewer-simulation",
                    ">= 1 run with domain_id=reviewer-simulation")
def _uc_reviewer_simulation(conn, paper_id):
    domain_id = _domain_id(conn, "reviewer-simulation")
    if domain_id is None:
        return False, ["reviewer-simulation domain not registered"]
    row = conn.execute(
        "SELECT COUNT(*) FROM academic_semantic_runs "
        "WHERE paper_id=? AND domain_id=?",
        (paper_id, domain_id),
    ).fetchone()
    if row[0] < 1:
        return False, ["no reviewer-simulation runs"]
    return True, [f"reviewer-simulation runs: {row[0]}"]


@_register_usecase("calculate",
                    "academic_score_history has a whole-paper row")
def _uc_calculate(conn, paper_id):
    row = conn.execute(
        "SELECT COUNT(*) FROM academic_score_history "
        "WHERE paper_id=? AND domain_id IS NULL",
        (paper_id,),
    ).fetchone()
    if row[0] < 1:
        return False, ["no whole-paper score row"]
    return True, [f"whole-paper score rows: {row[0]}"]


@_register_usecase("render-charts",
                    ">= 1 visualization exists for this paper")
def _uc_render_charts(conn, paper_id):
    row = conn.execute(
        "SELECT COUNT(*) FROM academic_visualizations "
        "WHERE paper_id=?",
        (paper_id,),
    ).fetchone()
    if row[0] < 1:
        return False, ["no visualizations"]
    return True, [f"visualizations: {row[0]}"]


@_register_usecase("render-audit-report",
                    ">= 1 report_history row with report_kind like 'audit-%'")
def _uc_render_audit(conn, paper_id):
    row = conn.execute(
        "SELECT COUNT(*) FROM academic_report_history "
        "WHERE paper_id=? AND report_kind LIKE 'audit-%'",
        (paper_id,),
    ).fetchone()
    if row[0] < 1:
        return False, ["no audit report rows"]
    return True, [f"audit report rows: {row[0]}"]


@_register_usecase("render-paper",
                    ">= 1 report_history row with report_kind='paper'")
def _uc_render_paper(conn, paper_id):
    row = conn.execute(
        "SELECT COUNT(*) FROM academic_report_history "
        "WHERE paper_id=? AND report_kind='paper'",
        (paper_id,),
    ).fetchone()
    if row[0] < 1:
        return False, ["no paper report rows"]
    return True, [f"paper report rows: {row[0]}"]


# ---------------------------------------------------------------------------
# Proposal-gate predicates — generation/audit/report may not start until an
# approved whole-paper proposal exists at the current commit (docs/proposal/
# base_academic-proposal-gate-workflow-proposal.md §2/§5). propose-fix has
# no registry entry here: it's domain-scoped (scope_domain_id set for a
# user-request fix), so its own verify script takes --domain and checks
# academic_proposal_review directly rather than going through usecase_status()
# with a single whole-paper name.
# ---------------------------------------------------------------------------

def _make_proposal_predicate(phase):
    def predicate(conn, paper_id):
        row = conn.execute(
            "SELECT 1 FROM proposal p "
            "JOIN usecase u ON u.id = p.usecase_id "
            "JOIN academic_proposal_review r ON r.proposal_id = p.id "
            "WHERE u.name=? AND r.paper_id=? AND r.review_status='approved' "
            "ORDER BY p.id DESC LIMIT 1",
            (f"propose-{phase}", paper_id),
        ).fetchone()
        if not row:
            return False, [f"no approved {phase} proposal"]
        return True, [f"approved {phase} proposal exists"]
    return predicate


for _phase in ("generation", "audit", "report"):
    _register_usecase_fn(f"propose-{_phase}",
                          f"an approved {_phase} proposal exists at the current commit",
                          _make_proposal_predicate(_phase))


_register_usecase_fn(
    "approve-proposal", "human-decision step — no completion criteria of its own",
    lambda conn, paper_id: (True, ["approve-proposal has no predicate; "
                                    "downstream gates check the row it produces, not this usecase itself"]),
)


# ---------------------------------------------------------------------------
# Proposal-id lookup — link_proposal_scope.py needs the generic proposal.id
# that run_script_step inserted after persist_proposal.py exited.  The
# proposal row's execution_id -> execution.step_id chain lets us find it
# by the persist-proposal step's ID.
# ---------------------------------------------------------------------------

def get_latest_proposal_id(conn, step_id):
    """Return the most recent proposal.id whose execution matches step_id."""
    row = conn.execute(
        "SELECT p.id FROM proposal p "
        "JOIN execution e ON e.id = p.execution_id "
        "WHERE e.step_id = ? ORDER BY e.id DESC LIMIT 1",
        (step_id,),
    ).fetchone()
    return row["id"] if row else None


def get_persist_proposal_step_id(conn, usecase_name, standard="pcems_2026"):
    """Return the step.id for the persist-proposal script within a usecase."""
    row = conn.execute(
        "SELECT s.id FROM step s "
        "JOIN step_script ss ON ss.step_id = s.id "
        "JOIN script sc ON sc.id = ss.script_id "
        "JOIN usecase u ON u.id = s.usecase_id "
        "WHERE u.standard = ? AND u.name = ? AND sc.name = 'persist-proposal' "
        "ORDER BY s.step_order LIMIT 1",
        (standard, usecase_name),
    ).fetchone()
    return row["id"] if row else None


# ---------------------------------------------------------------------------
# Score history helpers
# ---------------------------------------------------------------------------

def record_score_snapshot(conn, paper_id, domain_key, final_score, score_band, trend_delta=None):
    """Append a score snapshot (never updates).  domain_key=None for whole-paper."""
    domain_id = get_domain_id(conn, domain_key) if domain_key else None
    ts = now_iso()
    conn.execute(
        "INSERT INTO academic_score_history (paper_id, domain_id, final_score, score_band, trend_delta, calculated_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (paper_id, domain_id, final_score, score_band, trend_delta, ts),
    )
    conn.commit()


def get_score_history(conn, paper_id, domain_key=None):
    """Return score history rows for a paper, optionally filtered by domain."""
    if domain_key:
        domain_id = get_domain_id(conn, domain_key)
        rows = conn.execute(
            "SELECT * FROM academic_score_history WHERE paper_id=? AND domain_id=? ORDER BY calculated_at",
            (paper_id, domain_id),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM academic_score_history WHERE paper_id=? ORDER BY calculated_at",
            (paper_id,),
        ).fetchall()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Plagiarism helpers — supports pass_type + check_kind for 3-pass flow
# ---------------------------------------------------------------------------

def upsert_plagiarism_finding(conn, paper_id, domain, run_number, verdict,
                               flagged_spans=None, model="", pass_type="forensic",
                               check_kind="semantic"):
    domain_id = get_domain_id(conn, domain)
    ts = now_iso()
    existing = conn.execute(
        "SELECT id FROM academic_plagiarism_findings "
        "WHERE paper_id=? AND domain_id=? AND run_number=? AND pass_type=? AND check_kind=?",
        (paper_id, domain_id, run_number, pass_type, check_kind),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE academic_plagiarism_findings SET verdict=?, flagged_spans=?, model=?, created_at=? WHERE id=?",
            (verdict, json.dumps(flagged_spans or []), model, ts, existing["id"]),
        )
    else:
        conn.execute(
            "INSERT INTO academic_plagiarism_findings "
            "(paper_id, domain_id, run_number, pass_type, check_kind, verdict, flagged_spans, model, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (paper_id, domain_id, run_number, pass_type, check_kind, verdict,
             json.dumps(flagged_spans or []), model, ts),
        )
    conn.commit()


def get_plagiarism_finding(conn, paper_id, domain, run_number=None, pass_type="forensic",
                           check_kind=None):
    domain_id = get_domain_id(conn, domain)
    if check_kind:
        if run_number:
            row = conn.execute(
                "SELECT * FROM academic_plagiarism_findings "
                "WHERE paper_id=? AND domain_id=? AND run_number=? AND pass_type=? AND check_kind=?",
                (paper_id, domain_id, run_number, pass_type, check_kind),
            ).fetchone()
            return dict(row) if row else None
        row = conn.execute(
            "SELECT * FROM academic_plagiarism_findings "
            "WHERE paper_id=? AND domain_id=? AND pass_type=? AND check_kind=? "
            "ORDER BY run_number DESC LIMIT 1",
            (paper_id, domain_id, pass_type, check_kind),
        ).fetchone()
        return dict(row) if row else None
    if run_number:
        row = conn.execute(
            "SELECT * FROM academic_plagiarism_findings "
            "WHERE paper_id=? AND domain_id=? AND run_number=? AND pass_type=?",
            (paper_id, domain_id, run_number, pass_type),
        ).fetchone()
        return dict(row) if row else None
    row = conn.execute(
        "SELECT * FROM academic_plagiarism_findings "
        "WHERE paper_id=? AND domain_id=? AND pass_type=? "
        "ORDER BY run_number DESC LIMIT 1",
        (paper_id, domain_id, pass_type),
    ).fetchone()
    return dict(row) if row else None


# ---------------------------------------------------------------------------
# Deterministic findings helpers — append-only, one row per (paper, domain, run)
# ---------------------------------------------------------------------------

def record_deterministic_findings(conn, paper_id, domain, verdict, findings=None,
                                  commit_sha=""):
    """Append a deterministic audit result. Never updates existing rows.
    commit_sha is the git commit this audit ran against — used for
    skip-if-unchanged cache checks in the orchestrator."""
    domain_id = get_domain_id(conn, domain)
    if domain_id is None:
        raise ValueError(f"unknown domain '{domain}' — not in academic_domains")
    ts = now_iso()
    max_run = conn.execute(
        "SELECT COALESCE(MAX(run_number), 0) FROM academic_deterministic_findings "
        "WHERE paper_id=? AND domain_id=?",
        (paper_id, domain_id),
    ).fetchone()[0]
    cur = conn.execute(
        "INSERT INTO academic_deterministic_findings "
        "(paper_id, domain_id, run_number, verdict, findings, commit_sha, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (paper_id, domain_id, max_run + 1, verdict,
         json.dumps(findings or []), commit_sha, ts),
    )
    conn.commit()
    return cur.lastrowid


def get_latest_deterministic_findings(conn, paper_id, domain):
    """Get the most recent deterministic audit for a (paper, domain)."""
    domain_id = get_domain_id(conn, domain)
    if domain_id is None:
        return None
    row = conn.execute(
        "SELECT * FROM academic_deterministic_findings "
        "WHERE paper_id=? AND domain_id=? "
        "ORDER BY run_number DESC LIMIT 1",
        (paper_id, domain_id),
    ).fetchone()
    return dict(row) if row else None


def get_semantic_runs_for_commit(conn, paper_id, domain, scope, part_kind,
                                 commit_sha):
    """Return all semantic run rows matching a specific commit.
    Used by the orchestrator's skip-check: if the requested model already
    has a row for this commit+scope+part_kind, skip re-scoring."""
    domain_id = None
    if scope in ("section-full", "section-part"):
        domain_id = get_domain_id(conn, domain)
        if domain_id is None:
            return []
    rows = conn.execute(
        "SELECT * FROM academic_semantic_runs "
        "WHERE paper_id=? AND domain_id IS ? AND scope=? "
        "AND part_kind IS ? AND commit_sha=?",
        (paper_id, domain_id, scope, part_kind, commit_sha),
    ).fetchall()
    return [dict(r) for r in rows]


def get_deterministic_findings_history(conn, paper_id, domain=None):
    """Return deterministic findings history rows, optionally filtered by domain."""
    if domain:
        domain_id = get_domain_id(conn, domain)
        rows = conn.execute(
            "SELECT * FROM academic_deterministic_findings "
            "WHERE paper_id=? AND domain_id=? ORDER BY run_number",
            (paper_id, domain_id),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM academic_deterministic_findings "
            "WHERE paper_id=? ORDER BY run_number",
            (paper_id,),
        ).fetchall()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Humanize helpers
# ---------------------------------------------------------------------------

def upsert_humanize_pass(conn, paper_id, domain, iteration, change_summary,
                         risk_flags=None, model="", pass_kind="semantic"):
    domain_id = get_domain_id(conn, domain)
    ts = now_iso()
    existing = conn.execute(
        "SELECT id FROM academic_humanize_passes WHERE paper_id=? AND domain_id=? AND iteration=? AND pass_kind=?",
        (paper_id, domain_id, iteration, pass_kind),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE academic_humanize_passes SET change_summary=?, risk_flags=?, model=?, created_at=? WHERE id=?",
            (change_summary, json.dumps(risk_flags or []), model, ts, existing["id"]),
        )
    else:
        conn.execute(
            "INSERT INTO academic_humanize_passes (paper_id, domain_id, iteration, pass_kind, change_summary, risk_flags, model, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (paper_id, domain_id, iteration, pass_kind, change_summary, json.dumps(risk_flags or []), model, ts),
        )
    conn.commit()


# ---------------------------------------------------------------------------
# Visualization helpers
# ---------------------------------------------------------------------------

def seed_visualization_types(conn, chart_specs):
    """Seed chart types from a list of (chart_key, scope, description) tuples."""
    for chart_key, scope, description in chart_specs:
        conn.execute(
            "INSERT INTO academic_visualization_types (chart_key, scope, description) "
            "VALUES (?, ?, ?) "
            "ON CONFLICT(chart_key) DO UPDATE SET scope=excluded.scope, description=excluded.description",
            (chart_key, scope, description),
        )
    conn.commit()


def record_visualization(conn, chart_key, paper_id=None, domain_key=None,
                         content_hash=None, file_path="",
                         commit_sha=None, generation_params=None,
                         width=None, height=None):
    """Record a rendered chart image.  Returns the row id."""
    chart_type = conn.execute(
        "SELECT id FROM academic_visualization_types WHERE chart_key=?", (chart_key,)
    ).fetchone()
    if not chart_type:
        raise ValueError(f"unknown chart_key '{chart_key}' — not in academic_visualization_types")
    domain_id = get_domain_id(conn, domain_key) if domain_key else None
    ts = now_iso()
    cur = conn.execute(
        "INSERT INTO academic_visualizations "
        "(chart_type_id, paper_id, domain_id, content_hash, file_path, created_at, "
        " commit_sha, generation_params, width, height) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (chart_type["id"], paper_id, domain_id, content_hash, file_path, ts,
         commit_sha or "", generation_params, width, height),
    )
    conn.commit()
    return cur.lastrowid


def get_visualization(conn, chart_key, paper_id=None, domain_key=None, content_hash=None):
    """Check if a visualization already exists (for dedup)."""
    chart_type = conn.execute(
        "SELECT id FROM academic_visualization_types WHERE chart_key=?", (chart_key,)
    ).fetchone()
    if not chart_type:
        return None
    conditions = ["chart_type_id=?"]
    params = [chart_type["id"]]
    if paper_id:
        conditions.append("paper_id=?")
        params.append(paper_id)
    if domain_key:
        domain_id = get_domain_id(conn, domain_key)
        conditions.append("domain_id=?")
        params.append(domain_id)
    if content_hash:
        conditions.append("content_hash=?")
        params.append(content_hash)
    where = " AND ".join(conditions)
    row = conn.execute(
        f"SELECT * FROM academic_visualizations WHERE {where} ORDER BY id DESC LIMIT 1",
        params,
    ).fetchone()
    return dict(row) if row else None


# ---------------------------------------------------------------------------
# Report history helpers — supports report_kind for dual-track rendering
# ---------------------------------------------------------------------------

def record_report(conn, paper_id, format, file_path, final_score=None,
                  score_band=None, report_kind="paper",
                  scope_domain_id=None, map_kind=None):
    """Record a new report, setting prior is_latest=0 for same paper+report_kind+format."""
    ts = now_iso()
    conn.execute(
        "UPDATE academic_report_history SET is_latest=0 "
        "WHERE paper_id=? AND report_kind=? AND format=? AND is_latest=1",
        (paper_id, report_kind, format),
    )
    if scope_domain_id is not None or map_kind is not None:
        cur = conn.execute(
            "INSERT INTO academic_report_history "
            "(paper_id, report_kind, format, final_score, score_band, "
            " scope_domain_id, map_kind, file_path, is_latest, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?)",
            (paper_id, report_kind, format, final_score, score_band,
             scope_domain_id, map_kind, file_path, ts),
        )
    else:
        cur = conn.execute(
            "INSERT INTO academic_report_history "
            "(paper_id, report_kind, format, final_score, score_band, "
            " file_path, is_latest, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, 1, ?)",
            (paper_id, report_kind, format, final_score, score_band, file_path, ts),
        )
    conn.commit()
    return cur.lastrowid


def get_latest_report(conn, paper_id, format, report_kind="paper"):
    row = conn.execute(
        "SELECT * FROM academic_report_history WHERE paper_id=? AND format=? AND report_kind=? AND is_latest=1",
        (paper_id, format, report_kind),
    ).fetchone()
    return dict(row) if row else None


def list_report_history(conn, paper_id, format=None, report_kind=None):
    conditions = ["paper_id=?"]
    params = [paper_id]
    if format:
        conditions.append("format=?")
        params.append(format)
    if report_kind:
        conditions.append("report_kind=?")
        params.append(report_kind)
    where = " AND ".join(conditions)
    rows = conn.execute(
        f"SELECT * FROM academic_report_history WHERE {where} ORDER BY created_at DESC",
        params,
    ).fetchall()
    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Template catalog helpers
# ---------------------------------------------------------------------------

def seed_templates(conn, system_dir):
    """Scan top-level areas for prompt/ and templates/ trees, classify by path
    segment rather than a hardcoded root list — a new feature folder is
    picked up automatically because its sub-tree contains prompt/ or
    templates/ in its path."""
    top_areas = [
        system_dir,
        os.path.join(system_dir, "common"),
        os.path.join(system_dir, "step1-draft-for-completeness"),
        os.path.join(system_dir, "step2-edit-for-concision"),
        os.path.join(system_dir, "step3-plagiarism-humanize"),
        os.path.join(system_dir, "final-render"),
    ]

    for area in top_areas:
        if not os.path.isdir(area):
            continue
        for dirpath, _dirnames, filenames in os.walk(area):
            rel = os.path.relpath(dirpath, area)
            segs = rel.replace(os.sep, "/").split("/")
            if "prompt" in segs:
                kind = "prompt"
            elif "templates" in segs:
                kind = "scaffold"
            else:
                continue
            scope = "root" if rel == "." else rel.replace(os.sep, "/")
            for fname in filenames:
                if not fname.endswith((".md", ".yaml", ".html")):
                    continue
                name = fname.rsplit(".", 1)[0]
                file_path = os.path.join(dirpath, fname)
                existing = conn.execute(
                    "SELECT id FROM academic_templates WHERE template_kind=? AND scope=? AND name=?",
                    (kind, scope, name),
                ).fetchone()
                if existing:
                    conn.execute(
                        "UPDATE academic_templates SET file_path=? WHERE id=?",
                        (file_path, existing["id"]),
                    )
                else:
                    conn.execute(
                        "INSERT INTO academic_templates (template_kind, scope, name, file_path) VALUES (?, ?, ?, ?)",
                        (kind, scope, name, file_path),
                    )
    conn.commit()


# ---------------------------------------------------------------------------
# Step loading helpers (extracted from run_full_workflow.py for reuse
# by propose scripts and other callers)
# ---------------------------------------------------------------------------

def db_path(repo_root):
    """Standard knowledge.db location under a repo's .samgraha/ dir —
    same construction _adapter.parse_step_args() does inline for step
    scripts; shared here for callers outside the fixed step contract
    (request_fix.py, run_full_workflow.py)."""
    return os.path.join(str(repo_root), ".samgraha", "knowledge.db")


def resolve_paper_id(conn, repo_root):
    """Resolve paper_id from repo_root. Unlike get_paper_id() in
    run_full_workflow.py (which takes db_path+standard+repo_root),
    this assumes the caller already has a conn."""
    row = conn.execute(
        "SELECT id FROM academic_papers WHERE repo_root=?",
        (str(repo_root),)).fetchone()
    return row["id"] if row else None


def load_steps(db_path, standard):
    """Load all steps for a standard from knowledge.db.
    Extracted from run_full_workflow.py for shared use."""
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT step.id, usecase.name AS usecase, step.step_order, "
        "step.kind, step.description "
        "FROM step JOIN usecase ON step.usecase_id = usecase.id "
        "WHERE usecase.standard = ? ORDER BY usecase.id, step.step_order",
        (standard,),
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]


def steps_of(steps, usecase):
    """Filter a steps list to those belonging to a specific usecase."""
    return [s for s in steps if s["usecase"] == usecase]


def seed_calculation_dependencies(conn, edges):
    """Seed calculation dependency edges. Each edge is a dict with keys:
    calc_path, depends_on_kind, depends_on, consumed_by (or None — a
    comma-joined reader-script list if more than one script reads
    calc_path, schema/23; the initial seed's best-known guess, later
    kept accurate by audit_calculation_wiring.py, §4c). One row per
    (calc_path, depends_on_kind, depends_on) — consumed_by is NOT part
    of the identity key, it's this row's payload; re-seeding just
    refreshes it, same idempotent shape seed_domains() already uses."""
    for e in edges:
        conn.execute(
            "INSERT INTO academic_calculation_dependencies "
            "(calc_path, depends_on_kind, depends_on, consumed_by) "
            "VALUES (?, ?, ?, ?) "
            "ON CONFLICT(calc_path, depends_on_kind, depends_on) "
            "DO UPDATE SET consumed_by=excluded.consumed_by",
            (e["calc_path"], e["depends_on_kind"], e["depends_on"],
             e.get("consumed_by")),
        )
    conn.commit()
