"""run_domain_evidence.py — pre-script opening the semantic-audit triad
(pre: this -> semantic: audit/semantic/document/*.prompt.md -> post:
persist_domain_semantic_score.py). Gathers exactly the same evidence a
deterministic audit run already gathers for this domain, by calling
common/det_audit.py's run_audit_script() directly — reuses the existing
audit_*.py scripts unchanged, just returns the evidence in the envelope
instead of writing a deterministic score with it. The calling agent reads
this envelope's "evidence" field, then calls prepare_semantic_step for the
matching prompt to reason over it.

Expected --in payload: {"team_name": str, "domain": str}
"""
import os
import sys
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import hackathon_schema  # noqa: E402
from det_audit import run_audit_script, discover_entrypoint  # noqa: E402


def main():
    repo_root, db_path, payload, out_path = parse_step_args()

    team_name = payload["team_name"]
    domain = payload["domain"]
    standard = payload.get("standard", "python_hackathon")

    conn = hackathon_schema.get_conn(db_path)
    try:
        module_name = hackathon_schema.get_audit_module(conn, domain)
        participant = next(
            (p for p in hackathon_schema.list_participants(conn, standard) if p["team_name"] == team_name),
            None,
        )
    finally:
        conn.close()

    if not module_name:
        write_envelope(out_path, status="error", message=f"unknown domain '{domain}'")
        return
    if participant is None:
        write_envelope(out_path, status="error", message=f"unknown team_name '{team_name}'")
        return

    repo_path = participant["repo_path"]
    entrypoint = discover_entrypoint(repo_path) if domain == "runtime" else None
    evidence, err = run_audit_script(module_name, repo_path, entrypoint)
    if err:
        write_envelope(out_path, status="error", message=err)
        return

    if domain == "runtime":
        for fname in ("main.py", "app.py", "run.py"):
            evidence[fname] = os.path.isfile(os.path.join(repo_path, fname))

    write_envelope(out_path, status="ok", message=f"gathered evidence for {team_name}/{domain}",
                   evidence=evidence, team_name=team_name, domain=domain)


if __name__ == "__main__":
    main()
