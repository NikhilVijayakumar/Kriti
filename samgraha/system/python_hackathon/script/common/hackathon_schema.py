"""
hackathon_schema.py — python_hackathon's OWN normalized tables in
knowledge.db, catalogued via standard.yaml's custom_tables (not the archived
doc-audit tables documents/standard_audit_runs/semantic_reports).

SCHEMA_SQL below mirrors ../../schema/*.sql exactly — same discipline as
samgraha's own schema/knowledge/*.sql vs core_schema.rs: those files are the
canonical reference copy, this is the source of truth. Keep them in sync by
hand if this changes.

Every driver script imports the same-named functions from here that it used
to import from db.py — a one-line import swap per file, no other logic
touched. Function signatures/return shapes below are kept identical to the
previous single-table design even though the storage is now normalized, so
render_reports.py / run_calculate.py / etc never had to change again for
this pass.

Tables (see .samgraha/schema/README.md for the full rationale):
  hackathon_teams                    — one row per team
  hackathon_domains                  — lookup: the 10 scoring domains + weights
  hackathon_deterministic_scores     — one row per (team, domain) det. audit
  hackathon_semantic_runs            — one row per (team, domain, model) semantic run
  hackathon_semantic_dimension_scores — one row per (run, dimension) — the
                                        "separate table for evidence" per model
  hackathon_semantic_findings        — one row per (run, strength|weakness|recommendation)
  hackathon_narratives                — one row per (team, domain) narrative + which model wrote it
  hackathon_narrative_sections       — one row per (narrative, heading/text) section
  hackathon_templates                 — catalog of markdown/html report templates on disk
  hackathon_visualization_types      — catalog of chart kinds render_charts.py can produce
  hackathon_visualizations            — one row per actually-generated chart file (backtrace, no re-render)

View:
  hackathon_semantic_domain_means — AVG(overall_score) per (team, domain) across
    models, computed straight from hackathon_semantic_runs. Never recomputed by
    rerunning an LLM — it's a live SQL aggregate over what's already stored.
"""
import json
import sqlite3
from datetime import datetime, timezone

from db import get_canonical_domains  # noqa: F401 — re-exported, table-independent

_STANDARD = "python_hackathon"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS hackathon_teams (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard      TEXT    NOT NULL,
    team_name     TEXT    NOT NULL,
    repo_path     TEXT    NOT NULL DEFAULT '',
    team_leader   TEXT    NOT NULL DEFAULT '',
    team_code     TEXT    NOT NULL DEFAULT '',
    repo_https    TEXT    NOT NULL DEFAULT '',
    repo_ssh      TEXT    NOT NULL DEFAULT '',
    members       TEXT    NOT NULL DEFAULT '[]',
    metadata      TEXT    NOT NULL DEFAULT '{}',
    created_at    TEXT    NOT NULL,
    updated_at    TEXT    NOT NULL,
    UNIQUE(standard, team_name)
);

CREATE TABLE IF NOT EXISTS hackathon_domains (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    key           TEXT    NOT NULL UNIQUE,
    display_name  TEXT    NOT NULL,
    sort_order    INTEGER NOT NULL,
    weight        REAL    NOT NULL DEFAULT 0,
    det_weight    REAL    NOT NULL DEFAULT 0.60,
    sem_weight    REAL    NOT NULL DEFAULT 0.40,
    audit_module  TEXT    NOT NULL DEFAULT ''  -- which usecase-2a-det-audit/*.py handles this domain
);

CREATE TABLE IF NOT EXISTS hackathon_deterministic_scores (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard      TEXT    NOT NULL,
    team_id       INTEGER NOT NULL REFERENCES hackathon_teams(id) ON DELETE CASCADE,
    domain_id     INTEGER NOT NULL REFERENCES hackathon_domains(id) ON DELETE CASCADE,
    score         REAL    NOT NULL,
    rules_passed  INTEGER,
    rules_total   INTEGER,
    evidence      TEXT    NOT NULL DEFAULT '{}',
    created_at    TEXT    NOT NULL,
    UNIQUE(team_id, domain_id)
);

CREATE TABLE IF NOT EXISTS hackathon_semantic_runs (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard      TEXT    NOT NULL,
    team_id       INTEGER NOT NULL REFERENCES hackathon_teams(id) ON DELETE CASCADE,
    domain_id     INTEGER NOT NULL REFERENCES hackathon_domains(id) ON DELETE CASCADE,
    model         TEXT    NOT NULL,
    overall_score REAL    NOT NULL,
    reasoning     TEXT    NOT NULL DEFAULT '',
    created_at    TEXT    NOT NULL,
    UNIQUE(team_id, domain_id, model)
);

CREATE TABLE IF NOT EXISTS hackathon_semantic_dimension_scores (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id        INTEGER NOT NULL REFERENCES hackathon_semantic_runs(id) ON DELETE CASCADE,
    dimension_key TEXT    NOT NULL,
    score         REAL    NOT NULL,
    evidence      TEXT    NOT NULL DEFAULT '',
    UNIQUE(run_id, dimension_key)
);

CREATE TABLE IF NOT EXISTS hackathon_semantic_findings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id        INTEGER NOT NULL REFERENCES hackathon_semantic_runs(id) ON DELETE CASCADE,
    finding_type  TEXT    NOT NULL CHECK (finding_type IN ('strength','weakness','recommendation')),
    text          TEXT    NOT NULL,
    sort_order    INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS hackathon_narratives (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard      TEXT    NOT NULL,
    team_id       INTEGER REFERENCES hackathon_teams(id) ON DELETE CASCADE,
    domain_id     INTEGER REFERENCES hackathon_domains(id) ON DELETE CASCADE,
    model         TEXT    NOT NULL DEFAULT '',
    created_at    TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_hackathon_narratives_lookup
    ON hackathon_narratives(standard, team_id, domain_id);

CREATE TABLE IF NOT EXISTS hackathon_narrative_sections (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    narrative_id  INTEGER NOT NULL REFERENCES hackathon_narratives(id) ON DELETE CASCADE,
    heading       TEXT    NOT NULL,
    text          TEXT    NOT NULL,
    sort_order    INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS hackathon_templates (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    format        TEXT    NOT NULL CHECK (format IN ('markdown','html')),
    report_type   TEXT    NOT NULL CHECK (report_type IN ('deterministic','semantic','summary','leaderboard','team-final-summary')),
    domain_id     INTEGER REFERENCES hackathon_domains(id) ON DELETE CASCADE,
    file_path     TEXT    NOT NULL,
    UNIQUE(format, report_type, domain_id)
);

CREATE TABLE IF NOT EXISTS hackathon_visualization_types (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_key     TEXT    NOT NULL UNIQUE,
    scope         TEXT    NOT NULL CHECK (scope IN ('per_team_domain','per_domain','per_team','global')),
    description   TEXT    NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS hackathon_visualizations (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    chart_type_id INTEGER NOT NULL REFERENCES hackathon_visualization_types(id) ON DELETE CASCADE,
    team_id       INTEGER REFERENCES hackathon_teams(id) ON DELETE CASCADE,
    domain_id     INTEGER REFERENCES hackathon_domains(id) ON DELETE CASCADE,
    file_path     TEXT    NOT NULL,
    created_at    TEXT    NOT NULL
);

CREATE VIEW IF NOT EXISTS hackathon_semantic_domain_means AS
    SELECT standard, team_id, domain_id,
           AVG(overall_score) AS semantic_mean,
           COUNT(*) AS model_count
    FROM hackathon_semantic_runs
    GROUP BY standard, team_id, domain_id;
"""

# Static reference data — the source of truth for what's actually on disk
# and in render_charts.py, so hackathon_templates/hackathon_visualization_types
# reflect reality instead of drifting out of sync with it.
_VISUALIZATION_TYPES = [
    ("field_distribution", "per_team_domain", "team's domain score vs global median/MAD"),
    ("rank_distribution", "per_domain", "all teams' adjusted score for one domain, ranked"),
    ("det_sem_contribution", "per_team_domain", "deterministic vs semantic weighted contribution"),
    ("rule_pass_rate", "per_team_domain", "deterministic rule pass/fail breakdown"),
    ("model_spread", "per_team_domain", "per-model semantic score spread for one domain"),
    ("team_radar", "per_team", "team's adjusted score across all domains"),
    ("domain_weights", "global", "static chart of domain weight allocation"),
]

_REPORT_TYPES_BY_FORMAT = {
    "markdown": ("deterministic.md", "semantic.md", "summary.md"),
    "html": ("deterministic.html", "semantic.html", "summary.html"),
}
_GLOBAL_TEMPLATES = {
    "markdown": {"leaderboard": "global-leaderboard.md", "team-final-summary": "team-final-summary.md"},
    "html": {"leaderboard": "global-leaderboard.html", "team-final-summary": "team-final-summary.html"},
}


def ensure_schema(conn):
    conn.executescript(SCHEMA_SQL)
    conn.commit()


def get_conn(db_path):
    """Open knowledge.db and guarantee this standard's own tables (+ lookup
    rows) exist — defensive: also created explicitly by the init-schema step
    script, but a driver run out of order should never hit 'no such table'."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    ensure_schema(conn)
    return conn


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Domain lookup — seeded once from weights.yaml + calculation/aggregation/domain/*.yaml,
# the same files the old per-call logic in get_all_scores_as_dict already read.
# ---------------------------------------------------------------------------

def seed_domains(conn, scripts_dir):
    """Populate hackathon_domains from weights.yaml (canonical order/weight)
    joined with each domain's real det/sem split from
    calculation/aggregation/domain/*.yaml. Idempotent — safe to call every
    init-schema run."""
    import glob as globmod
    import os
    import yaml
    from det_audit import DOMAIN_AUDIT_MODULES  # the one remaining code-side mapping — seeded in, not re-imported at runtime

    system_dir = os.path.join(scripts_dir, "..")
    weights_file = os.path.join(system_dir, "calculation", "weights.yaml")
    agg_dir = os.path.join(system_dir, "calculation", "aggregation", "domain")

    with open(weights_file, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    display_overrides = {"mlops": "MLOps", "ai-explanations": "AI Explanations"}
    ts_order = 0
    for raw_key, spec in cfg["domains"].items():
        key = raw_key.replace("-", "_")
        display_name = display_overrides.get(raw_key, raw_key.replace("-", " ").title())
        weight = spec.get("weight", 0)
        audit_module = DOMAIN_AUDIT_MODULES.get(key, "")

        det_w, sem_w = 0.60, 0.40
        matches = globmod.glob(os.path.join(agg_dir, f"*-{raw_key}.yaml"))
        if matches:
            with open(matches[0], "r", encoding="utf-8") as f:
                agg = yaml.safe_load(f)
            w = agg.get("weights", {})
            det_w = w.get("deterministic", det_w)
            sem_w = w.get("semantic", sem_w)

        conn.execute(
            "INSERT INTO hackathon_domains (key, display_name, sort_order, weight, det_weight, sem_weight, audit_module) "
            "VALUES (?, ?, ?, ?, ?, ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET "
            "display_name=excluded.display_name, sort_order=excluded.sort_order, "
            "weight=excluded.weight, det_weight=excluded.det_weight, sem_weight=excluded.sem_weight, "
            "audit_module=excluded.audit_module",
            (key, display_name, ts_order, weight, det_w, sem_w, audit_module),
        )
        ts_order += 1
    conn.commit()


def seed_templates(conn, scripts_dir):
    """Catalog every report template actually on disk under
    templates/reports/{markdown,html}/ — real paths, not guessed."""
    import os

    system_dir = os.path.join(scripts_dir, "..")
    domains = get_all_domains(conn)  # [(id, key, dir_name), ...]

    def _upsert_template(fmt, report_type, domain_id, abs_path):
        # ON CONFLICT can't dedupe domain_id=NULL rows (SQLite treats every
        # NULL as distinct, so the UNIQUE constraint never fires for the
        # global templates) — same class of issue upsert_narrative() already
        # works around, same fix: an explicit `IS`-based existence check.
        existing = conn.execute(
            "SELECT id FROM hackathon_templates WHERE format=? AND report_type=? AND domain_id IS ?",
            (fmt, report_type, domain_id),
        ).fetchone()
        if existing:
            conn.execute("UPDATE hackathon_templates SET file_path=? WHERE id=?", (abs_path, existing["id"]))
        else:
            conn.execute(
                "INSERT INTO hackathon_templates (format, report_type, domain_id, file_path) VALUES (?, ?, ?, ?)",
                (fmt, report_type, domain_id, abs_path),
            )

    for fmt, filenames in _REPORT_TYPES_BY_FORMAT.items():
        for domain_id, key, dir_name in domains:
            for filename in filenames:
                report_type = filename.rsplit(".", 1)[0]
                rel = os.path.join("templates", "reports", fmt, "domain", dir_name, filename)
                abs_path = os.path.join(system_dir, rel)
                if not os.path.isfile(abs_path):
                    continue
                _upsert_template(fmt, report_type, domain_id, abs_path)
        for report_type, filename in _GLOBAL_TEMPLATES[fmt].items():
            rel = os.path.join("templates", "reports", fmt, filename)
            abs_path = os.path.join(system_dir, rel)
            if not os.path.isfile(abs_path):
                continue
            _upsert_template(fmt, report_type, None, abs_path)
    conn.commit()


def seed_visualization_types(conn):
    for chart_key, scope, description in _VISUALIZATION_TYPES:
        conn.execute(
            "INSERT INTO hackathon_visualization_types (chart_key, scope, description) "
            "VALUES (?, ?, ?) "
            "ON CONFLICT(chart_key) DO UPDATE SET scope=excluded.scope, description=excluded.description",
            (chart_key, scope, description),
        )
    conn.commit()


def get_all_domains(conn):
    """[(domain_id, key, dir_name), ...] ordered by sort_order. dir_name is
    the '01-infrastructure' style prefix templates/*.yaml files actually use
    on disk, derived from sort_order+key. Thin convenience wrapper over
    get_domain_rows() for the two call sites that only need id/key/dir_name."""
    return [(r["id"], r["key"], r["dir_name"]) for r in get_domain_rows(conn)]


def get_domain_rows(conn):
    """Every hackathon_domains column, plus the derived dir_name, as plain
    dicts ordered by sort_order — the single source callers should read
    instead of hardcoding their own domain list/weights/audit-module map
    (common/render_reports.py and common/det_audit.py used to)."""
    rows = conn.execute(
        "SELECT id, key, display_name, sort_order, weight, det_weight, sem_weight, audit_module "
        "FROM hackathon_domains ORDER BY sort_order"
    ).fetchall()
    return [
        {
            "id": r["id"], "key": r["key"], "display_name": r["display_name"],
            "sort_order": r["sort_order"], "weight": r["weight"],
            "det_weight": r["det_weight"], "sem_weight": r["sem_weight"],
            "audit_module": r["audit_module"],
            "dir_name": f"{r['sort_order'] + 1:02d}-{r['key'].replace('_', '-')}",
        }
        for r in rows
    ]


def get_domain_id(conn, domain_key):
    row = conn.execute("SELECT id FROM hackathon_domains WHERE key=?", (domain_key,)).fetchone()
    return row["id"] if row else None


def get_audit_module(conn, domain_key):
    row = conn.execute("SELECT audit_module FROM hackathon_domains WHERE key=?", (domain_key,)).fetchone()
    return row["audit_module"] if row else None


def get_template(conn, fmt, report_type, domain_key=None):
    """Look up a template's real file_path from hackathon_templates — the
    thing common/render_reports.py's _load_template()/_load_html_template()
    call instead of building `templates/reports/{fmt}/domain/{dir_name}/
    {report_type}.{ext}` themselves. Raises if the row isn't there (a
    missing template is a schema-init/seed_templates bug, not something to
    silently skip)."""
    domain_id = get_domain_id(conn, domain_key) if domain_key else None
    row = conn.execute(
        "SELECT file_path FROM hackathon_templates WHERE format=? AND report_type=? AND domain_id IS ?",
        (fmt, report_type, domain_id),
    ).fetchone()
    if not row:
        raise ValueError(f"no hackathon_templates row for format={fmt!r} report_type={report_type!r} domain={domain_key!r} — rerun schema-init/seed_templates")
    return row["file_path"]


# ---------------------------------------------------------------------------
# Team helpers
# ---------------------------------------------------------------------------

def register_participant(conn, standard, team_name, repo_path,
                          team_leader=None, members=None,
                          repo_https=None, repo_ssh=None, team_code=None,
                          metadata=None):
    cur = conn.execute(
        "SELECT id FROM hackathon_teams WHERE standard=? AND team_name=?",
        (standard, team_name),
    )
    row = cur.fetchone()
    if row:
        return row["id"]

    ts = now_iso()
    cur = conn.execute(
        "INSERT INTO hackathon_teams "
        "(standard, team_name, repo_path, team_leader, team_code, repo_https, repo_ssh, members, metadata, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            standard, team_name, repo_path,
            team_leader or "", team_code or "", repo_https or "", repo_ssh or "",
            json.dumps(members or []), json.dumps(metadata or {}),
            ts, ts,
        ),
    )
    conn.commit()
    return cur.lastrowid


def list_participants(conn, standard):
    rows = conn.execute(
        "SELECT id, team_name, repo_path FROM hackathon_teams WHERE standard=?",
        (standard,),
    ).fetchall()
    return [{"id": r["id"], "team_name": r["team_name"], "repo_path": r["repo_path"]} for r in rows]


def get_team_profile(conn, team_id):
    row = conn.execute("SELECT * FROM hackathon_teams WHERE id=?", (team_id,)).fetchone()
    if not row:
        return None
    members = json.loads(row["members"]) if row["members"] else []

    def _fmt_member(m):
        if isinstance(m, dict):
            name = m.get("name", "")
            emp_id = m.get("employee_id", "")
            return f"{name} ({emp_id})" if emp_id else name
        return str(m)

    return {
        "team_name": row["team_name"],
        "team_leader": row["team_leader"],
        "team_code": row["team_code"],
        "members": [_fmt_member(m) for m in members],
        "repo_https": row["repo_https"],
        "repo_ssh": row["repo_ssh"],
        "repo_path": row["repo_path"],
    }


# ---------------------------------------------------------------------------
# Domain-score helpers — dispatch to the deterministic or semantic tables by
# `kind`; callers (common/det_audit.py, persist_domain_semantic_score.py)
# never changed their call shape.
# ---------------------------------------------------------------------------

def upsert_domain_score(conn, participant_id, domain, kind, model, score, evidence=None):
    domain_id = get_domain_id(conn, domain)
    if domain_id is None:
        raise ValueError(f"unknown domain '{domain}' — not in hackathon_domains (run init-schema/seed_domains first)")
    ts = now_iso()

    if kind == "deterministic":
        evidence_json = json.dumps(evidence or {})
        existing = conn.execute(
            "SELECT id FROM hackathon_deterministic_scores WHERE team_id=? AND domain_id=?",
            (participant_id, domain_id),
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE hackathon_deterministic_scores SET score=?, evidence=?, created_at=? WHERE id=?",
                (score, evidence_json, ts, existing["id"]),
            )
        else:
            conn.execute(
                "INSERT INTO hackathon_deterministic_scores (standard, team_id, domain_id, score, evidence, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (_STANDARD, participant_id, domain_id, score, evidence_json, ts),
            )
        conn.commit()
        return

    if kind == "semantic":
        result = evidence or {}
        reasoning = result.get("reasoning", "")
        existing = conn.execute(
            "SELECT id FROM hackathon_semantic_runs WHERE team_id=? AND domain_id=? AND model=?",
            (participant_id, domain_id, model or ""),
        ).fetchone()
        if existing:
            run_id = existing["id"]
            conn.execute(
                "UPDATE hackathon_semantic_runs SET overall_score=?, reasoning=?, created_at=? WHERE id=?",
                (score, reasoning, ts, run_id),
            )
            conn.execute("DELETE FROM hackathon_semantic_dimension_scores WHERE run_id=?", (run_id,))
            conn.execute("DELETE FROM hackathon_semantic_findings WHERE run_id=?", (run_id,))
        else:
            cur = conn.execute(
                "INSERT INTO hackathon_semantic_runs (standard, team_id, domain_id, model, overall_score, reasoning, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (_STANDARD, participant_id, domain_id, model or "", score, reasoning, ts),
            )
            run_id = cur.lastrowid

        for dim_key, dim in (result.get("dimension_scores") or {}).items():
            dim_score = dim.get("score") if isinstance(dim, dict) else dim
            dim_evidence = dim.get("evidence", "") if isinstance(dim, dict) else ""
            conn.execute(
                "INSERT INTO hackathon_semantic_dimension_scores (run_id, dimension_key, score, evidence) "
                "VALUES (?, ?, ?, ?)",
                (run_id, dim_key, dim_score, dim_evidence),
            )

        for finding_type, key in (("strength", "strengths"), ("weakness", "weaknesses"), ("recommendation", "recommendations")):
            for i, text in enumerate(result.get(key) or []):
                conn.execute(
                    "INSERT INTO hackathon_semantic_findings (run_id, finding_type, text, sort_order) VALUES (?, ?, ?, ?)",
                    (run_id, finding_type, text, i),
                )
        conn.commit()
        return

    raise ValueError(f"unknown kind '{kind}' — must be 'deterministic' or 'semantic'")


def get_domain_scores(conn, participant_id, domain=None):
    """Same return shape as before ({domain, kind, score, model,
    raw_evidence_json}), now assembled from the normalized tables —
    render_reports.py's fetch_deterministic_data/fetch_semantic_data read
    raw_evidence_json exactly as they did before this split."""
    domain_filter = "AND d.key=?" if domain else ""
    params = (participant_id, domain) if domain else (participant_id,)

    det_rows = conn.execute(
        f"SELECT d.key AS domain, s.score, s.evidence "
        f"FROM hackathon_deterministic_scores s JOIN hackathon_domains d ON d.id=s.domain_id "
        f"WHERE s.team_id=? {domain_filter}",
        params,
    ).fetchall()
    results = [
        {"domain": r["domain"], "kind": "deterministic", "score": r["score"], "model": "", "raw_evidence_json": r["evidence"]}
        for r in det_rows
    ]

    sem_runs = conn.execute(
        f"SELECT s.id, d.key AS domain, s.model, s.overall_score, s.reasoning "
        f"FROM hackathon_semantic_runs s JOIN hackathon_domains d ON d.id=s.domain_id "
        f"WHERE s.team_id=? {domain_filter}",
        params,
    ).fetchall()
    for run in sem_runs:
        dims = conn.execute(
            "SELECT dimension_key, score, evidence FROM hackathon_semantic_dimension_scores WHERE run_id=?",
            (run["id"],),
        ).fetchall()
        findings = conn.execute(
            "SELECT finding_type, text FROM hackathon_semantic_findings WHERE run_id=? ORDER BY sort_order",
            (run["id"],),
        ).fetchall()
        result = {
            "overall_score": run["overall_score"],
            "reasoning": run["reasoning"],
            "dimension_scores": {d["dimension_key"]: {"score": d["score"], "evidence": d["evidence"]} for d in dims},
            "strengths": [f["text"] for f in findings if f["finding_type"] == "strength"],
            "weaknesses": [f["text"] for f in findings if f["finding_type"] == "weakness"],
            "recommendations": [f["text"] for f in findings if f["finding_type"] == "recommendation"],
        }
        results.append({
            "domain": run["domain"], "kind": "semantic", "score": run["overall_score"],
            "model": run["model"], "raw_evidence_json": json.dumps(result),
        })
    return results


def get_all_scores_as_dict(conn, standard, mode="both"):
    """Same return shape as before ({team: {domain: {raw_score,
    deterministic_score, semantic_mean, model_breakdown}}}), now reading
    hackathon_semantic_domain_means (the view) for the mean instead of
    averaging in Python — the aggregate is a live SQL query over already-
    stored per-model rows, never a re-run of the semantic step."""
    domains = get_domain_rows(conn)
    participants = list_participants(conn, standard)
    result = {}
    for p in participants:
        pid = p["id"]
        team_output = {}
        for d in domains:
            domain_id, key = d["id"], d["key"]
            det_row = conn.execute(
                "SELECT score FROM hackathon_deterministic_scores WHERE team_id=? AND domain_id=?",
                (pid, domain_id),
            ).fetchone()
            det = det_row["score"] if det_row else 0.0

            model_rows = conn.execute(
                "SELECT model, overall_score FROM hackathon_semantic_runs WHERE team_id=? AND domain_id=?",
                (pid, domain_id),
            ).fetchall()
            model_breakdown = {r["model"]: r["overall_score"] for r in model_rows}
            mean_row = conn.execute(
                "SELECT semantic_mean FROM hackathon_semantic_domain_means WHERE team_id=? AND domain_id=?",
                (pid, domain_id),
            ).fetchone()
            sem_mean = mean_row["semantic_mean"] if mean_row else 0.0

            eff_det, eff_sem = det, sem_mean
            if mode == "det":
                eff_sem = 0.0
            elif mode == "sem":
                eff_det = 0.0

            team_output[key] = {
                "raw_score": round(d["det_weight"] * eff_det + d["sem_weight"] * eff_sem, 2),
                "deterministic_score": eff_det,
                "semantic_mean": round(sem_mean, 2),
                "model_breakdown": model_breakdown,
            }
        result[p["team_name"]] = team_output
    return result


def missing_semantic_combos(conn, standard, target_models):
    participants = list_participants(conn, standard)
    domains = get_all_domains(conn)
    missing = []
    for p in participants:
        for domain_id, key, _ in domains:
            for m in target_models:
                row = conn.execute(
                    "SELECT 1 FROM hackathon_semantic_runs WHERE team_id=? AND domain_id=? AND model=?",
                    (p["id"], domain_id, m),
                ).fetchone()
                if not row:
                    missing.append((p["team_name"], key, m))
    return missing


# ---------------------------------------------------------------------------
# Narrative helpers — team_id/domain_id are nullable (competition-wide
# narrative); sections normalized into hackathon_narrative_sections.
# ---------------------------------------------------------------------------

def upsert_narrative(conn, participant_id, domain, sections, model=None):
    domain_id = get_domain_id(conn, domain) if domain else None
    ts = now_iso()
    existing = conn.execute(
        "SELECT id FROM hackathon_narratives WHERE standard=? AND team_id IS ? AND domain_id IS ?",
        (_STANDARD, participant_id, domain_id),
    ).fetchone()
    if existing:
        narrative_id = existing["id"]
        conn.execute(
            "UPDATE hackathon_narratives SET model=?, created_at=? WHERE id=?",
            (model or "", ts, narrative_id),
        )
        conn.execute("DELETE FROM hackathon_narrative_sections WHERE narrative_id=?", (narrative_id,))
    else:
        cur = conn.execute(
            "INSERT INTO hackathon_narratives (standard, team_id, domain_id, model, created_at) VALUES (?, ?, ?, ?, ?)",
            (_STANDARD, participant_id, domain_id, model or "", ts),
        )
        narrative_id = cur.lastrowid

    for i, section in enumerate(sections or []):
        conn.execute(
            "INSERT INTO hackathon_narrative_sections (narrative_id, heading, text, sort_order) VALUES (?, ?, ?, ?)",
            (narrative_id, section.get("heading", ""), section.get("text", ""), i),
        )
    conn.commit()


def get_narrative(conn, participant_id, domain):
    """Same return shape as before — a plain list of {heading, text} dicts,
    or None if no narrative exists yet."""
    domain_id = get_domain_id(conn, domain) if domain else None
    row = conn.execute(
        "SELECT id FROM hackathon_narratives WHERE standard=? AND team_id IS ? AND domain_id IS ?",
        (_STANDARD, participant_id, domain_id),
    ).fetchone()
    if not row:
        return None
    sections = conn.execute(
        "SELECT heading, text FROM hackathon_narrative_sections WHERE narrative_id=? ORDER BY sort_order",
        (row["id"],),
    ).fetchall()
    return [{"heading": s["heading"], "text": s["text"]} for s in sections]


# ---------------------------------------------------------------------------
# Visualization artifact tracking — backtrace: a report step checks this
# before calling render_charts.py again for the same (chart, team, domain).
# ---------------------------------------------------------------------------

def record_visualization(conn, chart_key, file_path, team_id=None, domain_key=None):
    chart_row = conn.execute("SELECT id FROM hackathon_visualization_types WHERE chart_key=?", (chart_key,)).fetchone()
    if not chart_row:
        raise ValueError(f"unknown chart_key '{chart_key}' — not in hackathon_visualization_types")
    domain_id = get_domain_id(conn, domain_key) if domain_key else None
    conn.execute(
        "INSERT INTO hackathon_visualizations (chart_type_id, team_id, domain_id, file_path, created_at) VALUES (?, ?, ?, ?, ?)",
        (chart_row["id"], team_id, domain_id, file_path, now_iso()),
    )
    conn.commit()


def get_visualization(conn, chart_key, team_id=None, domain_key=None):
    """Return the most recent generated file_path for this
    (chart_key, team, domain) combination, or None — the check a report step
    makes before re-rendering a chart it already has."""
    chart_row = conn.execute("SELECT id FROM hackathon_visualization_types WHERE chart_key=?", (chart_key,)).fetchone()
    if not chart_row:
        return None
    domain_id = get_domain_id(conn, domain_key) if domain_key else None
    row = conn.execute(
        "SELECT file_path FROM hackathon_visualizations "
        "WHERE chart_type_id=? AND team_id IS ? AND domain_id IS ? "
        "ORDER BY id DESC LIMIT 1",
        (chart_row["id"], team_id, domain_id),
    ).fetchone()
    return row["file_path"] if row else None
