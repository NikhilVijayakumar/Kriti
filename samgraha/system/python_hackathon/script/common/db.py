"""
db.py — SQLite schema and helpers for python_hackathon scoring.

Tables:
  standard_participants  — who's competing (keyed by team_name)
  standard_domain_scores — per (team, domain, kind, model) scores
  standard_narratives    — agent-written narrative sections
"""
import sqlite3
import os
import json
from datetime import datetime, timezone

DEFAULT_DB = os.path.join(
    os.path.dirname(__file__), "..", "..", "hackathon.db"
)
_WEIGHTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "calculation", "weights.yaml"
)


def get_canonical_domains():
    """Return domain key list from weights.yaml, normalized to underscores.
    Single source of truth — never hardcode domain names elsewhere."""
    import yaml
    with open(_WEIGHTS_FILE, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return [k.replace("-", "_") for k in cfg["domains"]]

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS standard_participants (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    standard            TEXT    NOT NULL,
    team_name           TEXT    NOT NULL,
    repo_path           TEXT    NOT NULL,
    team_leader         TEXT,
    members_json        TEXT,
    repo_https          TEXT,
    repo_ssh            TEXT,
    team_code           TEXT,
    metadata_json       TEXT,
    registered_at       TEXT    NOT NULL,
    UNIQUE(standard, team_name)
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
    # Migrate old schemas: participant_name -> team_name
    _migrate(conn)
    return conn


def _migrate(conn):
    """Handle schema evolution for existing databases."""
    cols = {row[1] for row in conn.execute("PRAGMA table_info(standard_participants)")}

    # Old schema had participant_name — migrate to team_name
    if "participant_name" in cols and "team_name" not in cols:
        try:
            conn.execute("ALTER TABLE standard_participants ADD COLUMN team_name TEXT")
        except sqlite3.OperationalError:
            pass
        conn.execute(
            "UPDATE standard_participants SET team_name=participant_name WHERE team_name IS NULL"
        )
        conn.commit()
    elif "participant_name" in cols and "team_name" in cols:
        # Both exist — fill any NULL team_names from participant_name
        conn.execute(
            "UPDATE standard_participants SET team_name=participant_name WHERE team_name IS NULL"
        )
        conn.commit()

    # Drop redundant columns if they exist (SQLite doesn't support DROP COLUMN
    # before 3.35.0, so we silently ignore).
    for col in ("presentation_order", "time_slot"):
        if col in cols:
            try:
                conn.execute(f"ALTER TABLE standard_participants DROP COLUMN {col}")
            except (sqlite3.OperationalError, AttributeError):
                pass

    # Ensure team_code column exists
    if "team_code" not in cols:
        try:
            conn.execute("ALTER TABLE standard_participants ADD COLUMN team_code TEXT")
        except sqlite3.OperationalError:
            pass

    conn.commit()


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Participant helpers
# ---------------------------------------------------------------------------

def register_participant(conn, standard, team_name, repo_path,
                         team_leader=None, members=None,
                         repo_https=None, repo_ssh=None, team_code=None,
                         metadata=None):
    """Insert or ignore a team. Returns participant id."""
    cur = conn.execute(
        "SELECT id FROM standard_participants WHERE standard=? AND team_name=?",
        (standard, team_name),
    )
    row = cur.fetchone()
    if row:
        return row["id"]
    cur = conn.execute(
        "INSERT INTO standard_participants "
        "(standard, team_name, repo_path, team_leader, "
        " members_json, repo_https, repo_ssh, team_code, "
        " metadata_json, registered_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            standard, team_name, repo_path,
            team_leader,
            json.dumps(members) if members else None,
            repo_https, repo_ssh, team_code,
            json.dumps(metadata) if metadata else None,
            now_iso(),
        ),
    )
    conn.commit()
    return cur.lastrowid


def list_participants(conn, standard):
    """Return all teams for a standard."""
    return conn.execute(
        "SELECT id, team_name, repo_path FROM standard_participants WHERE standard=?",
        (standard,),
    ).fetchall()


def get_team_profile(conn, participant_id):
    """Return team metadata dict for reports. All fields nullable except id."""
    row = conn.execute(
        "SELECT * FROM standard_participants WHERE id=?", (participant_id,)
    ).fetchone()
    if not row:
        return None
    members = json.loads(row["members_json"]) if row["members_json"] else []
    return {
        "team_name": row["team_name"],
        "team_leader": row["team_leader"] or "",
        "team_code": row["team_code"] or "",
        "members": members,
        "repo_https": row["repo_https"] or "",
        "repo_ssh": row["repo_ssh"] or "",
        "repo_path": row["repo_path"],
    }


# ---------------------------------------------------------------------------
# Domain-score helpers
# ---------------------------------------------------------------------------

def upsert_domain_score(conn, participant_id, domain, kind, model, score, evidence=None):
    """Insert or update a domain score row (UNIQUE on participant+domain+kind+model)."""
    evidence_json = json.dumps(evidence) if evidence is not None else None
    ts = now_iso()
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


def get_all_scores_as_dict(conn, standard, mode="both"):
    """
    Returns aggregated_scores dict shaped for statistics.py:
      {team_name: {domain: {"raw_score": float, "deterministic_score": float,
       "semantic_mean": float, "model_breakdown": {model: score}}}}

    Domains with zero audit data for a team get raw_score=0.0 (z-score
    population includes everyone, per loop.yaml z_score_population_rule).

    mode: "both" (default) | "det" (zero out semantic) | "sem" (zero out deterministic)
    """
    import yaml
    agg_dir = os.path.join(os.path.dirname(__file__), "..", "..", "calculation", "aggregation", "domain")
    all_domains = get_canonical_domains()

    participants = list_participants(conn, standard)
    result = {}
    for p in participants:
        tname = p["team_name"]
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

        team_output = {}
        for d in all_domains:
            if d not in domains:
                # Zero audit data for this domain — inject 0.0 so
                # statistics.py includes this team in the z-score population.
                team_output[d] = {
                    "raw_score": 0.0,
                    "deterministic_score": 0.0,
                    "semantic_mean": 0.0,
                    "model_breakdown": {},
                }
                continue

            data = domains[d]
            det = data["deterministic"] or 0.0
            sem_scores = list(data["semantic_models"].values())
            sem_mean = sum(sem_scores) / len(sem_scores) if sem_scores else 0.0

            # --mode filter: zero out the excluded kind
            if mode == "det":
                sem_mean = 0.0
            elif mode == "sem":
                det = 0.0

            det_w, sem_w = 0.60, 0.40
            import glob as globmod
            matches = globmod.glob(os.path.join(agg_dir, f"*-{d.replace('_', '-')}.yaml"))
            if matches:
                try:
                    with open(matches[0], "r", encoding="utf-8") as f:
                        agg = yaml.safe_load(f)
                    weights = agg.get("weights", {})
                    det_w = weights.get("deterministic", 0.60)
                    sem_w = weights.get("semantic", 0.40)
                except (yaml.YAMLError, OSError):
                    pass

            raw_score = round(det_w * det + sem_w * sem_mean, 2)

            team_output[d] = {
                "raw_score": raw_score,
                "deterministic_score": det,
                "semantic_mean": round(sem_mean, 2),
                "model_breakdown": data["semantic_models"],
            }
        result[tname] = team_output
    return result


def missing_semantic_combos(conn, standard, target_models):
    """Return list of (team_name, domain, model) that have no semantic row yet."""
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
                    missing.append((p["team_name"], d, m))
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
