"""
db.py — SQLite schema and helpers for python_hackathon scoring.

Tables:
  standard_participants  — who's competing
  standard_domain_scores — per (participant, domain, kind, model) scores
  standard_narratives    — agent-written narrative sections
"""
import sqlite3
import os
import json
from datetime import datetime, timezone

DEFAULT_DB = os.path.join(
    os.path.dirname(__file__), "..", "hackathon.db"
)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS standard_participants (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    standard        TEXT    NOT NULL,
    participant_name TEXT   NOT NULL,
    repo_path       TEXT    NOT NULL,
    metadata_json   TEXT,
    registered_at   TEXT    NOT NULL,
    UNIQUE(standard, participant_name)
);

CREATE TABLE IF NOT EXISTS standard_domain_scores (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id  INTEGER NOT NULL REFERENCES standard_participants(id),
    domain          TEXT    NOT NULL,
    kind            TEXT    NOT NULL,
    model           TEXT    NOT NULL DEFAULT '',
    score           REAL    NOT NULL,
    raw_evidence_json TEXT,
    created_at      TEXT    NOT NULL,
    UNIQUE(participant_id, domain, kind, model)
);
CREATE INDEX IF NOT EXISTS idx_sds_participant_domain
    ON standard_domain_scores(participant_id, domain);

CREATE TABLE IF NOT EXISTS standard_narratives (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    participant_id  INTEGER REFERENCES standard_participants(id),
    domain          TEXT,
    sections_json   TEXT    NOT NULL,
    created_at      TEXT    NOT NULL
);
"""


def get_conn(db_path=None):
    """Open a connection, creating the DB and schema if needed."""
    path = db_path or DEFAULT_DB
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA_SQL)
    return conn


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Participant helpers
# ---------------------------------------------------------------------------

def register_participant(conn, standard, name, repo_path, metadata=None):
    """Insert or ignore a participant. Returns participant id."""
    cur = conn.execute(
        "SELECT id FROM standard_participants WHERE standard=? AND participant_name=?",
        (standard, name),
    )
    row = cur.fetchone()
    if row:
        return row["id"]
    cur = conn.execute(
        "INSERT INTO standard_participants (standard, participant_name, repo_path, metadata_json, registered_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (standard, name, repo_path, json.dumps(metadata) if metadata else None, now_iso()),
    )
    conn.commit()
    return cur.lastrowid


def list_participants(conn, standard):
    """Return all participants for a standard."""
    return conn.execute(
        "SELECT id, participant_name, repo_path FROM standard_participants WHERE standard=?",
        (standard,),
    ).fetchall()


# ---------------------------------------------------------------------------
# Domain-score helpers
# ---------------------------------------------------------------------------

def upsert_domain_score(conn, participant_id, domain, kind, model, score, evidence=None):
    """Insert or update a domain score row (UNIQUE on participant+domain+kind+model)."""
    evidence_json = json.dumps(evidence) if evidence is not None else None
    ts = now_iso()
    # Try update first
    cur = conn.execute(
        "UPDATE standard_domain_scores SET score=?, raw_evidence_json=?, created_at=? "
        "WHERE participant_id=? AND domain=? AND kind=? AND model=?",
        (score, evidence_json, ts, participant_id, domain, kind, model),
    )
    if cur.rowcount == 0:
        conn.execute(
            "INSERT INTO standard_domain_scores (participant_id, domain, kind, model, score, raw_evidence_json, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (participant_id, domain, kind, model, score, evidence_json, ts),
        )
    conn.commit()


def get_domain_scores(conn, participant_id, domain=None):
    """Return all score rows for a participant, optionally filtered by domain."""
    if domain:
        return conn.execute(
            "SELECT * FROM standard_domain_scores WHERE participant_id=? AND domain=?",
            (participant_id, domain),
        ).fetchall()
    return conn.execute(
        "SELECT * FROM standard_domain_scores WHERE participant_id=?",
        (participant_id,),
    ).fetchall()


def get_all_scores_as_dict(conn, standard):
    """
    Returns aggregated_scores dict shaped for statistics.py:
      {participant_name: {domain: {"raw_score": float, "deterministic_score": float,
       "semantic_mean": float, "model_breakdown": {model: score}}}}

    Semantic score per domain = mean of all model rows for that (participant, domain).
    Deterministic score = the single row's score.
    raw_score = weighted merge from aggregation YAML.
    """
    import yaml
    agg_dir = os.path.join(os.path.dirname(__file__), "..", "calculation", "aggregation", "domain")

    participants = list_participants(conn, standard)
    result = {}
    for p in participants:
        pname = p["participant_name"]
        rows = get_domain_scores(conn, p["id"])
        domains = {}
        for r in rows:
            d = r["domain"]
            if d not in domains:
                domains[d] = {"deterministic": None, "semantic_models": {}}
            if r["kind"] == "deterministic":
                domains[d]["deterministic"] = r["score"]
            elif r["kind"] == "semantic":
                domains[d]["semantic_models"][r["model"]] = r["score"]

        # Build output with raw_score per domain
        team_output = {}
        for d, data in domains.items():
            det = data["deterministic"] or 0.0
            sem_scores = list(data["semantic_models"].values())
            sem_mean = sum(sem_scores) / len(sem_scores) if sem_scores else 0.0

            # Read aggregation weights
            det_w, sem_w = 0.60, 0.40
            # Find the directory name for this domain
            import glob as globmod
            matches = globmod.glob(os.path.join(agg_dir, f"*-{d.replace('_', '-')}.yaml"))
            if matches:
                try:
                    with open(matches[0], "r", encoding="utf-8") as f:
                        agg = yaml.safe_load(f)
                    w = agg.get("weights", {})
                    det_w = w.get("deterministic", 0.60)
                    sem_w = w.get("semantic", 0.40)
                except (yaml.YAMLError, OSError):
                    pass

            raw_score = round(det_w * det + sem_w * sem_mean, 2)

            team_output[d] = {
                "raw_score": raw_score,
                "deterministic_score": det,
                "semantic_mean": round(sem_mean, 2),
                "model_breakdown": data["semantic_models"],
            }
        result[pname] = team_output
    return result


def missing_semantic_combos(conn, standard, target_models):
    """Return list of (participant_name, domain, model) that have no semantic row yet."""
    participants = list_participants(conn, standard)
    domains = set()
    for p in participants:
        for r in get_domain_scores(conn, p["id"]):
            domains.add(r["domain"])
    missing = []
    for p in participants:
        for d in domains:
            for m in target_models:
                row = conn.execute(
                    "SELECT id FROM standard_domain_scores "
                    "WHERE participant_id=? AND domain=? AND kind='semantic' AND model=?",
                    (p["id"], d, m),
                ).fetchone()
                if not row:
                    missing.append((p["participant_name"], d, m))
    return missing


# ---------------------------------------------------------------------------
# Narrative helpers
# ---------------------------------------------------------------------------

def upsert_narrative(conn, participant_id, domain, sections):
    """
    Insert or update a narrative. sections is a list of {"heading": ..., "text": ...}.
    For the competition-wide narrative, participant_id and domain are NULL.
    """
    sections_json = json.dumps(sections)
    ts = now_iso()
    # Find existing
    if participant_id is None and domain is None:
        existing = conn.execute(
            "SELECT id FROM standard_narratives WHERE participant_id IS NULL AND domain IS NULL"
        ).fetchone()
    else:
        existing = conn.execute(
            "SELECT id FROM standard_narratives WHERE participant_id=? AND domain=?",
            (participant_id, domain),
        ).fetchone()
    if existing:
        conn.execute(
            "UPDATE standard_narratives SET sections_json=?, created_at=? WHERE id=?",
            (sections_json, ts, existing["id"]),
        )
    else:
        conn.execute(
            "INSERT INTO standard_narratives (participant_id, domain, sections_json, created_at) "
            "VALUES (?, ?, ?, ?)",
            (participant_id, domain, sections_json, ts),
        )
    conn.commit()


def get_narrative(conn, participant_id, domain):
    """Get narrative sections for a (participant, domain) or the competition-wide one."""
    if participant_id is None and domain is None:
        row = conn.execute(
            "SELECT sections_json FROM standard_narratives WHERE participant_id IS NULL AND domain IS NULL"
        ).fetchone()
    else:
        row = conn.execute(
            "SELECT sections_json FROM standard_narratives WHERE participant_id=? AND domain=?",
            (participant_id, domain),
        ).fetchone()
    if row:
        return json.loads(row["sections_json"])
    return None
