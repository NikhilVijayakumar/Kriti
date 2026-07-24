"""
academic_schema.py — base_academic's OWN normalized tables in knowledge.db,
catalogued via standard.yaml's custom_tables.

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
import sqlite3
from datetime import datetime, timezone

_STANDARD = "base_academic"

_SCHEMA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "schema")


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

def upsert_module(conn, paper_id, module_name, module_path="", sort_order=0, metadata=None):
    existing = conn.execute(
        "SELECT id FROM academic_modules WHERE paper_id=? AND module_name=?",
        (paper_id, module_name),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE academic_modules SET module_path=?, sort_order=?, metadata=? WHERE id=?",
            (module_path, sort_order, json.dumps(metadata or {}), existing["id"]),
        )
        conn.commit()
        return existing["id"]
    cur = conn.execute(
        "INSERT INTO academic_modules (paper_id, module_name, module_path, sort_order, metadata) "
        "VALUES (?, ?, ?, ?, ?)",
        (paper_id, module_name, module_path, sort_order, json.dumps(metadata or {})),
    )
    conn.commit()
    return cur.lastrowid


def get_modules(conn, paper_id):
    rows = conn.execute(
        "SELECT id, module_name, module_path, sort_order FROM academic_modules "
        "WHERE paper_id=? ORDER BY sort_order", (paper_id,)
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
# Semantic score helpers — APPEND-ONLY (no UPDATE, no DELETE)
# ---------------------------------------------------------------------------

def upsert_semantic_score(conn, paper_id, domain, model, score, result=None,
                          scope="section", computed_against=None):
    """Append a new semantic run.  Never updates or deletes existing rows.
    run_number auto-increments per (paper, domain, scope, model).
    scope='cross-section' or 'document' → domain must be None.
    computed_against is a dict of {domain_key: iteration} snapshots for
    cross-section/document runs, so staleness can be detected when humanize
    changes a domain draft."""
    domain_id = None
    if scope == "section":
        domain_id = get_domain_id(conn, domain)
        if domain_id is None:
            raise ValueError(f"unknown domain '{domain}' — not in academic_domains")
    ts = now_iso()
    result = result or {}
    reasoning = result.get("reasoning", "")

    max_run = conn.execute(
        "SELECT COALESCE(MAX(run_number), 0) FROM academic_semantic_runs "
        "WHERE paper_id=? AND domain_id IS ? AND scope=? AND model=?",
        (paper_id, domain_id, scope, model or ""),
    ).fetchone()[0]
    cur = conn.execute(
        "INSERT INTO academic_semantic_runs "
        "(standard, paper_id, domain_id, scope, model, run_number, overall_score, reasoning, computed_against, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (_STANDARD, paper_id, domain_id, scope, model or "", max_run + 1, score, reasoning,
         json.dumps(computed_against or {}), ts),
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


def get_domain_scores(conn, paper_id, domain=None, scope="section"):
    domain_filter = "AND d.key=?" if domain else ""
    params = (paper_id, domain) if domain else (paper_id,)
    rows = conn.execute(
        f"SELECT d.key AS domain, s.model, s.overall_score, s.reasoning "
        f"FROM academic_semantic_runs s JOIN academic_domains d ON d.id=s.domain_id "
        f"WHERE s.paper_id=? AND s.scope=? {domain_filter}",
        (paper_id, scope) + params,
    ).fetchall()
    return [dict(r) for r in rows]


def get_latest_semantic_score(conn, paper_id, domain, model="", scope="section"):
    """Get the most recent semantic run for a (paper, domain, model, scope)."""
    if scope == "section":
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


def usecase_status(conn, paper_id, usecase_name):
    """Returns (complete: bool, detail: list[str]) for a usecase's
    completion criteria. Same predicate backs both the CLI verify script
    and the runtime dependency gate."""
    if usecase_name not in _USECASE_PREDICATES:
        return False, [f"unknown usecase '{usecase_name}'"]
    _, fn = _USECASE_PREDICATES[usecase_name]
    return fn(conn, paper_id)


@_register_usecase("schema-init", "20 academic_* tables exist")
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


@_register_usecase("novelty-analysis", "at least 1 cross-module novelty analysis exists")
def _uc_novelty(conn, paper_id):
    row = conn.execute(
        "SELECT COUNT(*) FROM academic_cross_module_analysis "
        "WHERE paper_id=? AND analysis_kind='novelty'",
        (paper_id,),
    ).fetchone()
    count = row[0]
    if count < 1:
        return False, [f"novelty analyses: {count}"]
    return True, [f"novelty analyses: {count}"]


@_register_usecase("gap-analysis", "at least 1 cross-module gap analysis exists")
def _uc_gaps(conn, paper_id):
    row = conn.execute(
        "SELECT COUNT(*) FROM academic_cross_module_analysis "
        "WHERE paper_id=? AND analysis_kind='gaps'",
        (paper_id,),
    ).fetchone()
    count = row[0]
    if count < 1:
        return False, [f"gap analyses: {count}"]
    return True, [f"gap analyses: {count}"]


@_register_usecase("mathematics-and-diagrams", "at least 1 math/architecture analysis exists")
def _uc_math(conn, paper_id):
    row = conn.execute(
        "SELECT COUNT(*) FROM academic_cross_module_analysis "
        "WHERE paper_id=? AND analysis_kind IN ('mathematics','architecture')",
        (paper_id,),
    ).fetchone()
    count = row[0]
    if count < 1:
        return False, [f"math/arch analyses: {count}"]
    return True, [f"math/arch analyses: {count}"]


@_register_usecase("assemble-paper-structure",
                    "every structural domain has an academic_narratives row")
def _uc_assemble(conn, paper_id):
    domains = conn.execute(
        "SELECT key FROM academic_domains "
        "ORDER BY sort_order"
    ).fetchall()
    missing = []
    for (dk,) in domains:
        row = conn.execute(
            "SELECT COUNT(*) FROM academic_narratives "
            "WHERE paper_id=? AND domain_id=(SELECT id FROM academic_domains WHERE key=?)",
            (paper_id, dk),
        ).fetchone()
        if row[0] < 1:
            missing.append(dk)
    if missing:
        return False, [f"missing narratives: {', '.join(missing)}"]
    return True, [f"all {len(domains)} domains have narratives"]


@_register_usecase("deterministic-audit",
                    "every domain has a PASS deterministic verdict")
def _uc_det_audit(conn, paper_id):
    domains = conn.execute("SELECT key FROM academic_domains ORDER BY sort_order").fetchall()
    failed = []
    for (dk,) in domains:
        row = conn.execute(
            "SELECT verdict FROM academic_deterministic_findings "
            "WHERE paper_id=? AND domain_id=(SELECT id FROM academic_domains WHERE key=?) "
            "ORDER BY run_number DESC LIMIT 1",
            (paper_id, dk),
        ).fetchone()
        if not row or row["verdict"] != "PASS":
            failed.append(dk)
    if failed:
        return False, [f"non-PASS domains: {', '.join(failed)}"]
    return True, [f"all {len(domains)} domains PASS"]


@_register_usecase("semantic-audit",
                    "every domain has >= 1 semantic run with scope='section'")
def _uc_sem_audit(conn, paper_id):
    domains = conn.execute("SELECT key FROM academic_domains ORDER BY sort_order").fetchall()
    missing = []
    for (dk,) in domains:
        row = conn.execute(
            "SELECT COUNT(*) FROM academic_semantic_runs "
            "WHERE paper_id=? AND scope='section' "
            "AND domain_id=(SELECT id FROM academic_domains WHERE key=?)",
            (paper_id, dk),
        ).fetchone()
        if row[0] < 1:
            missing.append(dk)
    if missing:
        return False, [f"unscored domains: {', '.join(missing)}"]
    return True, [f"all {len(domains)} domains scored"]


@_register_usecase("plagiarism-forensic-audit",
                    "every domain has a forensic plagiarism verdict")
def _uc_plagiarism(conn, paper_id):
    domains = conn.execute("SELECT key FROM academic_domains ORDER BY sort_order").fetchall()
    missing = []
    for (dk,) in domains:
        row = conn.execute(
            "SELECT verdict FROM academic_plagiarism_findings "
            "WHERE paper_id=? AND pass_type='forensic' "
            "AND domain_id=(SELECT id FROM academic_domains WHERE key=?) "
            "ORDER BY run_number DESC LIMIT 1",
            (paper_id, dk),
        ).fetchone()
        if not row:
            missing.append(dk)
    if missing:
        return False, [f"unaudited domains: {', '.join(missing)}"]
    return True, [f"all {len(domains)} domains audited"]


@_register_usecase("humanize",
                    "all humanize-flagged domains have >= 1 humanize pass")
def _uc_humanize(conn, paper_id):
    flagged = conn.execute(
        "SELECT DISTINCT domain_id FROM academic_plagiarism_findings "
        "WHERE paper_id=? AND verdict='FAIL' AND pass_type='forensic'",
        (paper_id,),
    ).fetchall()
    unhumanized = []
    for (did,) in flagged:
        row = conn.execute(
            "SELECT COUNT(*) FROM academic_humanize_passes "
            "WHERE paper_id=? AND domain_id=?",
            (paper_id, did),
        ).fetchone()
        if row[0] < 1:
            dk = conn.execute(
                "SELECT key FROM academic_domains WHERE id=?", (did,)
            ).fetchone()
            unhumanized.append(dk["key"] if dk else f"id={did}")
    if unhumanized:
        return False, [f"unhumanized: {', '.join(unhumanized)}"]
    return True, [f"all flagged domains humanized"]


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

def record_deterministic_findings(conn, paper_id, domain, verdict, findings=None):
    """Append a deterministic audit result. Never updates existing rows."""
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
        "(paper_id, domain_id, run_number, verdict, findings, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (paper_id, domain_id, max_run + 1, verdict,
         json.dumps(findings or []), ts),
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

def upsert_humanize_pass(conn, paper_id, domain, iteration, change_summary, risk_flags=None, model=""):
    domain_id = get_domain_id(conn, domain)
    ts = now_iso()
    existing = conn.execute(
        "SELECT id FROM academic_humanize_passes WHERE paper_id=? AND domain_id=? AND iteration=?",
        (paper_id, domain_id, iteration),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE academic_humanize_passes SET change_summary=?, risk_flags=?, model=?, created_at=? WHERE id=?",
            (change_summary, json.dumps(risk_flags or []), model, ts, existing["id"]),
        )
    else:
        conn.execute(
            "INSERT INTO academic_humanize_passes (paper_id, domain_id, iteration, change_summary, risk_flags, model, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (paper_id, domain_id, iteration, change_summary, json.dumps(risk_flags or []), model, ts),
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
                         content_hash=None, file_path=""):
    """Record a rendered chart image.  Returns the row id."""
    chart_type = conn.execute(
        "SELECT id FROM academic_visualization_types WHERE chart_key=?", (chart_key,)
    ).fetchone()
    if not chart_type:
        raise ValueError(f"unknown chart_key '{chart_key}' — not in academic_visualization_types")
    domain_id = get_domain_id(conn, domain_key) if domain_key else None
    ts = now_iso()
    cur = conn.execute(
        "INSERT INTO academic_visualizations (chart_type_id, paper_id, domain_id, content_hash, file_path, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (chart_type["id"], paper_id, domain_id, content_hash, file_path, ts),
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
                  score_band=None, report_kind="paper"):
    """Record a new report, setting prior is_latest=0 for same paper+report_kind+format."""
    ts = now_iso()
    conn.execute(
        "UPDATE academic_report_history SET is_latest=0 "
        "WHERE paper_id=? AND report_kind=? AND format=? AND is_latest=1",
        (paper_id, report_kind, format),
    )
    cur = conn.execute(
        "INSERT INTO academic_report_history (paper_id, report_kind, format, final_score, score_band, file_path, is_latest, created_at) "
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
    """Scan prompt/ (dispatched semantic prompt content) and templates/
    (scaffold manifests/output templates a script reads directly) and
    catalog both. scope = the immediate subdirectory name relative to
    each root (a usecase folder under prompt/, or whatever's left under
    templates/) — directory-driven, not a hand-maintained list, so a new
    usecase folder is picked up without touching this function."""
    roots = [
        ("prompt", os.path.join(system_dir, "prompt")),
        ("scaffold", os.path.join(system_dir, "templates")),
    ]

    for kind, root_dir in roots:
        if not os.path.isdir(root_dir):
            continue
        for dirpath, _dirnames, filenames in os.walk(root_dir):
            rel = os.path.relpath(dirpath, root_dir)
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
