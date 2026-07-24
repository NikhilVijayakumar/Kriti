"""render_charts.py — generates chart images from score/audit data using
matplotlib (Agg backend). Records each chart in academic_visualizations.
"""
import hashlib
import json
import os
import sys
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def _get_chart_backend():
    """Get matplotlib backend, preferring Agg for headless."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        return plt
    except ImportError:
        return None


def _domain_score_bar(plt, domains, scores, output_path):
    """Bar chart of latest domain scores."""
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["#2ecc71" if s >= 80 else "#f39c12" if s >= 60 else "#e74c3c"
              for s in scores]
    bars = ax.barh(domains, scores, color=colors)
    ax.set_xlabel("Score")
    ax.set_title("Domain Scores (Latest)")
    ax.set_xlim(0, 100)
    for bar, score in zip(bars, scores):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                f'{score:.1f}', va='center', fontsize=9)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _deterministic_findings_heatmap(plt, domains, check_results, output_path):
    """Heatmap of deterministic check pass/fail across domains."""
    import numpy as np
    n_domains = len(domains)
    n_checks = max(len(v) for v in check_results.values()) if check_results else 0
    if n_checks == 0:
        return

    matrix = np.zeros((n_domains, n_checks))
    check_labels = set()
    for i, domain in enumerate(domains):
        for j, check in enumerate(check_results.get(domain, [])):
            matrix[i, j] = 1 if check.get("passed", False) else 0
            check_labels.add(check.get("check_id", f"check-{j}"))

    fig, ax = plt.subplots(figsize=(max(10, n_checks * 0.8), max(4, n_domains * 0.5)))
    im = ax.imshow(matrix, cmap="RdYlGn", aspect="auto", vmin=0, vmax=1)
    ax.set_xticks(range(n_checks))
    ax.set_xticklabels(sorted(check_labels), rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(n_domains))
    ax.set_yticklabels(domains, fontsize=9)
    ax.set_title("Deterministic Audit Results")
    plt.colorbar(im, ax=ax, label="Pass (1) / Fail (0)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _cross_section_score_chart(plt, paper_id, conn, output_path):
    """Bar chart of cross-section semantic score."""
    row = conn.execute(
        "SELECT overall_score, reasoning FROM academic_semantic_runs "
        "WHERE paper_id=? AND scope='cross-section' "
        "ORDER BY run_number DESC LIMIT 1",
        (paper_id,),
    ).fetchone()
    if not row:
        return None
    score = row["overall_score"]
    fig, ax = plt.subplots(figsize=(6, 3))
    color = "#2ecc71" if score >= 80 else "#f39c12" if score >= 60 else "#e74c3c"
    ax.barh(["Cross-Section"], [score], color=color, height=0.5)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Score")
    ax.set_title("Cross-Section Consistency Score")
    ax.text(score + 1, 0, f"{score:.1f}", va="center", fontsize=10)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return {"chart": "cross-section-score", "path": output_path}


def _document_review_score_chart(plt, paper_id, conn, output_path):
    """Bar chart of document-level semantic score."""
    row = conn.execute(
        "SELECT overall_score, reasoning FROM academic_semantic_runs "
        "WHERE paper_id=? AND scope='document' "
        "ORDER BY run_number DESC LIMIT 1",
        (paper_id,),
    ).fetchone()
    if not row:
        return None
    score = row["overall_score"]
    fig, ax = plt.subplots(figsize=(6, 3))
    color = "#2ecc71" if score >= 80 else "#f39c12" if score >= 60 else "#e74c3c"
    ax.barh(["Document"], [score], color=color, height=0.5)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Score")
    ax.set_title("Document Review Score")
    ax.text(score + 1, 0, f"{score:.1f}", va="center", fontsize=10)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return {"chart": "document-review-score", "path": output_path}


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload.get("paper_id")
    chart_specs = payload.get("charts", ["domain-score-bar"])

    if not paper_id:
        write_envelope(out_path, status="error", message="missing paper_id")
        return

    plt = _get_chart_backend()
    if plt is None:
        write_envelope(out_path, status="error",
                       message="matplotlib not available")
        return

    conn = academic_schema.get_conn(db_path)
    try:
        domains = academic_schema.get_all_domains(conn)
        output_dir = os.path.join(str(repo_root), "docs", "paper",
                                  f"paper-{paper_id}", "charts")
        os.makedirs(output_dir, exist_ok=True)

        generated = []

        if "domain-score-bar" in chart_specs:
            domain_keys = []
            scores = []
            for domain_id, domain_key, display_name, sort_order in domains:
                row = conn.execute(
                    "SELECT final_score FROM academic_score_history "
                    "WHERE paper_id=? AND domain_id=? "
                    "ORDER BY calculated_at DESC LIMIT 1",
                    (paper_id, domain_id),
                ).fetchone()
                if row:
                    domain_keys.append(domain_key)
                    scores.append(row["final_score"])

            if domain_keys:
                fpath = os.path.join(output_dir, "domain-scores.png")
                _domain_score_bar(plt, domain_keys, scores, fpath)
                content_hash = hashlib.md5(json.dumps(scores).encode()).hexdigest()
                academic_schema.record_visualization(
                    conn, "domain-score-bar", paper_id,
                    content_hash=content_hash, file_path=fpath
                )
                generated.append({"chart": "domain-score-bar", "path": fpath})

        if "deterministic-findings-heatmap" in chart_specs:
            check_results = {}
            for domain_id, domain_key, display_name, sort_order in domains:
                det = conn.execute(
                    "SELECT findings FROM academic_deterministic_findings "
                    "WHERE paper_id=? AND domain_id=? "
                    "ORDER BY run_number DESC LIMIT 1",
                    (paper_id, domain_id),
                ).fetchone()
                if det and det["findings"]:
                    check_results[domain_key] = json.loads(det["findings"])

            if check_results:
                fpath = os.path.join(output_dir, "deterministic-heatmap.png")
                _deterministic_findings_heatmap(
                    plt, list(check_results.keys()), check_results, fpath
                )
                academic_schema.record_visualization(
                    conn, "deterministic-findings-heatmap", paper_id,
                    file_path=fpath
                )
                generated.append({"chart": "deterministic-findings-heatmap",
                                  "path": fpath})

        if "cross-section-score" in chart_specs:
            fpath = os.path.join(output_dir, "cross-section-score.png")
            result = _cross_section_score_chart(plt, paper_id, conn, fpath)
            if result:
                academic_schema.record_visualization(
                    conn, "cross-section-score", paper_id,
                    file_path=fpath
                )
                generated.append(result)

        if "document-review-score" in chart_specs:
            fpath = os.path.join(output_dir, "document-review-score.png")
            result = _document_review_score_chart(plt, paper_id, conn, fpath)
            if result:
                academic_schema.record_visualization(
                    conn, "document-review-score", paper_id,
                    file_path=fpath
                )
                generated.append(result)

        write_envelope(out_path, status="ok",
                       message=f"generated {len(generated)} charts",
                       charts=generated)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
