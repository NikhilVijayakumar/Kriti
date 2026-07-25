"""
db.py — SQLite helpers for python_hackathon scoring.

Uses samgraha's knowledge.db instead of a standalone hackathon.db.

Mapping:
  documents              — one row per team (path=team_name, metadata=JSON)
  standard_audit_runs    — per (team, domain) deterministic/semantic scores
  audit_results          — individual findings per team
  semantic_reports       — narrative sections per (team, domain)
"""
import sqlite3
import os
import json
from datetime import datetime, timezone

# Default to knowledge.db in .samgraha/
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = os.path.join(_SCRIPT_DIR, "..", "..", "knowledge.db")
_WEIGHTS_FILE = os.path.join(_SCRIPT_DIR, "..", "..", "calculation", "weights.yaml")
_STANDARD = "python_hackathon"


def get_canonical_domains():
    """Return domain key list from weights.yaml, normalized to underscores."""
    import yaml
    with open(_WEIGHTS_FILE, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return [k.replace("-", "_") for k in cfg["domains"]]


def get_conn(db_path=None):
    """Open a connection to knowledge.db."""
    path = db_path or DEFAULT_DB
    if not os.path.exists(path):
        raise FileNotFoundError(f"knowledge.db not found at {path}. Run samgraha init first.")
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Team (document) helpers
# ---------------------------------------------------------------------------

def register_participant(conn, standard, team_name, repo_path,
                         team_leader=None, members=None,
                         repo_https=None, repo_ssh=None, team_code=None,
                         metadata=None):
    """Insert or ignore a team as a document in knowledge.db. Returns document id."""
    cur = conn.execute(
        "SELECT id FROM documents WHERE standard=? AND path=?",
        (standard, team_name),
    )
    row = cur.fetchone()
    if row:
        return row["id"]

    team_meta = {
        "repo_path": repo_path,
        "team_leader": team_leader or "",
        "members": members or [],
        "repo_https": repo_https or "",
        "repo_ssh": repo_ssh or "",
        "team_code": team_code or "",
    }
    if metadata:
        team_meta.update(metadata)

    ts = now_iso()
    cur = conn.execute(
        "INSERT INTO documents (path, hash, standard, title, body, metadata, created_at, updated_at, quality) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            team_name,
            "",  # hash — not applicable for teams
            standard,
            team_name,
            f"Hackathon team: {team_name}",
            json.dumps(team_meta),
            ts,
            ts,
            "{}",
        ),
    )
    conn.commit()
    return cur.lastrowid


def list_participants(conn, standard):
    """Return all teams for a standard. Returns rows with id, team_name (=path), repo_path."""
    rows = conn.execute(
        "SELECT id, path as team_name, metadata FROM documents WHERE standard=?",
        (standard,),
    ).fetchall()
    result = []
    for r in rows:
        meta = json.loads(r["metadata"]) if r["metadata"] else {}
        result.append({
            "id": r["id"],
            "team_name": r["team_name"],
            "repo_path": meta.get("repo_path", ""),
        })
    return result


def get_team_profile(conn, document_id):
    """Return team metadata dict for reports."""
    row = conn.execute(
        "SELECT * FROM documents WHERE id=?", (document_id,)
    ).fetchone()
    if not row:
        return None
    meta = json.loads(row["metadata"]) if row["metadata"] else {}
    members = meta.get("members", [])
    if isinstance(members, str):
        try:
            members = json.loads(members)
        except json.JSONDecodeError:
            members = [members]

    # Normalize to display strings — members may be {"name","employee_id"} dicts
    # (from teams.json) or plain strings; templates expect plain text.
    def _fmt_member(m):
        if isinstance(m, dict):
            name = m.get("name", "")
            emp_id = m.get("employee_id", "")
            return f"{name} ({emp_id})" if emp_id else name
        return str(m)

    members = [_fmt_member(m) for m in members]

    return {
        "team_name": row["path"],
        "team_leader": meta.get("team_leader", ""),
        "team_code": meta.get("team_code", ""),
        "members": members,
        "repo_https": meta.get("repo_https", ""),
        "repo_ssh": meta.get("repo_ssh", ""),
        "repo_path": meta.get("repo_path", ""),
    }


# ---------------------------------------------------------------------------
# Domain-score helpers (standard_audit_runs)
# ---------------------------------------------------------------------------

def upsert_domain_score(conn, participant_id, domain, kind, model, score, evidence=None):
    """Insert or update a domain score in standard_audit_runs.

    participant_id is the document_id (team).
    kind: 'deterministic' or 'semantic'
    model: '' for deterministic, model name for semantic
    """
    report_data = json.loads(evidence) if isinstance(evidence, str) else (evidence or {})
    report_data["_document_id"] = participant_id
    report_data["_kind"] = kind
    report_json = json.dumps(report_data)
    ts = now_iso()

    # Use exact match on document_id embedded in report
    existing = conn.execute(
        "SELECT id FROM standard_audit_runs "
        "WHERE standard=? AND pipeline=? AND COALESCE(model, '')=? "
        "AND json_extract(report, '$._document_id')=?",
        (_STANDARD, domain, model or '', participant_id),
    ).fetchone()

    if existing:
        conn.execute(
            "UPDATE standard_audit_runs SET score=?, report=?, created_at=? WHERE id=?",
            (score, report_json, ts, existing["id"]),
        )
    else:
        conn.execute(
            "INSERT INTO standard_audit_runs (standard, pipeline, model, score, report, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (_STANDARD, domain, model or '', score, report_json, ts),
        )
    conn.commit()


def get_domain_scores(conn, participant_id, domain=None):
    """Return all score rows for a team, optionally filtered by domain."""
    rows = conn.execute(
        "SELECT * FROM standard_audit_runs WHERE standard=? "
        "AND json_extract(report, '$._document_id')=?",
        (_STANDARD, participant_id),
    ).fetchall()
    if domain:
        rows = [r for r in rows if r["pipeline"] == domain]
    # Reshape to match old API: domain, kind, score, model
    result = []
    for r in rows:
        report = json.loads(r["report"]) if r["report"] else {}
        result.append({
            "domain": r["pipeline"],
            "kind": report.get("_kind", "deterministic"),
            "score": r["score"],
            "model": r["model"] or "",
            "raw_evidence_json": r["report"],
        })
    return result


def get_all_scores_as_dict(conn, standard, mode="both"):
    """
    Returns aggregated_scores dict shaped for statistics.py:
      {team_name: {domain: {"raw_score": float, "deterministic_score": float,
       "semantic_mean": float, "model_breakdown": {model: score}}}}
    """
    import yaml
    import glob as globmod
    agg_dir = os.path.join(_SCRIPT_DIR, "..", "..", "calculation", "aggregation", "domain")
    all_domains = get_canonical_domains()

    participants = list_participants(conn, standard)
    result = {}
    for p in participants:
        tname = p["team_name"]
        pid = p["id"]
        rows = get_domain_scores(conn, pid)
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

            if mode == "det":
                sem_mean = 0.0
            elif mode == "sem":
                det = 0.0

            det_w, sem_w = 0.60, 0.40
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
                rows = get_domain_scores(conn, p["id"], domain=d)
                has_semantic = any(r["kind"] == "semantic" and r["model"] == m for r in rows)
                if not has_semantic:
                    missing.append((p["team_name"], d, m))
    return missing


# ---------------------------------------------------------------------------
# Narrative helpers (semantic_reports)
# ---------------------------------------------------------------------------

def upsert_narrative(conn, participant_id, domain, sections):
    """Insert or update a narrative in semantic_reports."""
    sections_json = json.dumps(sections)
    ts = now_iso()
    existing = conn.execute(
        "SELECT id FROM semantic_reports WHERE document_id=? AND domain=?",
        (participant_id, domain),
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE semantic_reports SET findings=?, created_at=? WHERE id=?",
            (sections_json, ts, existing["id"]),
        )
    else:
        conn.execute(
            "INSERT INTO semantic_reports (report_uuid, stage, domain, document_id, score, findings, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (f"narrative-{participant_id}-{domain}", "narrative", domain, participant_id, 0, sections_json, ts),
        )
    conn.commit()


def get_narrative(conn, participant_id, domain):
    """Get narrative sections for a (participant, domain)."""
    row = conn.execute(
        "SELECT findings FROM semantic_reports WHERE document_id=? AND domain=?",
        (participant_id, domain),
    ).fetchone()
    if row:
        return json.loads(row["findings"])
    return None
