"""calculate.py — two-bucket scoring. Reads semantic + deterministic scores,
computes final_score per final_score.yaml's 50/50 formula, applies
score_bands, calculates trend, and records to academic_score_history.
"""
import json
import os
import sys
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402

CALC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "calculation")


def _load_yaml(filename):
    yaml_path = os.path.join(CALC_DIR, filename)
    if not os.path.isfile(yaml_path):
        return None
    try:
        import yaml
    except ImportError:
        return None
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)


def _lookup_band(score, bands):
    """Find the rating band for a score."""
    for band in bands:
        if band["min"] <= score <= band["max"]:
            return band["rating"]
    return "Unknown"


def _compute_trend(current, previous, trend_cfg):
    """Compute trend label based on tolerance."""
    if previous is None:
        return "baseline"
    tolerance = trend_cfg.get("tolerance", {}).get("floor", 0.1)
    diff = current - previous
    if diff > tolerance:
        return "Improved"
    elif diff < -tolerance:
        return "Regressed"
    return "Unchanged"


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload.get("paper_id")

    if not paper_id:
        write_envelope(out_path, status="error", message="missing paper_id")
        return

    # Load calculation configs
    final_score_cfg = _load_yaml("summary/final_score.yaml")
    score_bands_cfg = _load_yaml("summary/score_bands.yaml")
    trend_cfg = _load_yaml("summary/trend.yaml")

    if not final_score_cfg or not score_bands_cfg:
        write_envelope(out_path, status="error",
                       message="missing calculation config files")
        return

    # Extract weights
    inputs = final_score_cfg.get("inputs", [])
    weights = {}
    for inp in inputs:
        weights[inp["name"]] = inp.get("weight", 50)

    bands = score_bands_cfg.get("bands", [])
    total_weight = sum(weights.values()) or 100

    conn = academic_schema.get_conn(db_path)
    try:
        domains = academic_schema.get_all_domains(conn)
        results = []

        for domain_id, domain_key, display_name, sort_order in domains:
            # Get latest semantic score
            sem_row = conn.execute(
                "SELECT overall_score FROM academic_semantic_runs "
                "WHERE paper_id=? AND domain_id=? "
                "ORDER BY run_number DESC LIMIT 1",
                (paper_id, domain_id),
            ).fetchone()
            sem_score = sem_row["overall_score"] if sem_row else None

            # Get latest deterministic score (compute from findings)
            det_row = conn.execute(
                "SELECT verdict, findings FROM academic_deterministic_findings "
                "WHERE paper_id=? AND domain_id=? "
                "ORDER BY run_number DESC LIMIT 1",
                (paper_id, domain_id),
            ).fetchone()

            det_score = None
            if det_row:
                findings = json.loads(det_row["findings"]) if det_row["findings"] else []
                if findings:
                    passed = sum(1 for f in findings if f.get("passed", False))
                    det_score = (passed / len(findings)) * 100 if findings else 100.0
                else:
                    det_score = 100.0 if det_row["verdict"] == "PASS" else 0.0

            # Compute weighted final score
            if sem_score is not None and det_score is not None:
                final = (weights.get("semantic_document", 50) / total_weight * sem_score +
                         weights.get("deterministic_document", 50) / total_weight * det_score)
            elif sem_score is not None:
                final = sem_score  # fallback: semantic only
            elif det_score is not None:
                final = det_score  # fallback: deterministic only
            else:
                final = 0.0

            score_band = _lookup_band(final, bands)

            # Get previous score for trend
            history = academic_schema.get_score_history(conn, paper_id, domain_key)
            prev_score = history[-1]["final_score"] if history else None
            trend = _compute_trend(final, prev_score, trend_cfg)

            trend_delta = final - prev_score if prev_score is not None else None

            # Record
            academic_schema.record_score_snapshot(
                conn, paper_id, domain_key, final, score_band, trend_delta
            )

            results.append({
                "domain": domain_key,
                "semantic_score": sem_score,
                "deterministic_score": det_score,
                "final_score": round(final, 2),
                "score_band": score_band,
                "trend": trend,
            })

        # Whole-paper score (mean of domain finals)
        if results:
            all_finals = [r["final_score"] for r in results if r["final_score"] is not None]
            whole_paper = sum(all_finals) / len(all_finals) if all_finals else 0.0
            whole_band = _lookup_band(whole_paper, bands)

            prev_whole = academic_schema.get_score_history(conn, paper_id)
            prev_whole_scores = [h["final_score"] for h in prev_whole if h["domain_id"] is None]
            prev_whole_score = prev_whole_scores[-1] if prev_whole_scores else None
            whole_trend = _compute_trend(whole_paper, prev_whole_score, trend_cfg)
            whole_delta = whole_paper - prev_whole_score if prev_whole_score is not None else None

            academic_schema.record_score_snapshot(
                conn, paper_id, None, whole_paper, whole_band, whole_delta
            )

            results.append({
                "domain": None,
                "final_score": round(whole_paper, 2),
                "score_band": whole_band,
                "trend": whole_trend,
            })

        write_envelope(out_path, status="ok",
                       message=f"calculated scores for {len(results)} entries",
                       results=results)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
