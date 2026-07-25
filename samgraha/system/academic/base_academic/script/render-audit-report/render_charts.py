"""render_charts.py — generates chart images from score/audit data using
matplotlib (Agg backend). Records each chart in academic_visualizations.
"""
import hashlib
import json
import os
import struct
import sys
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def _png_dimensions(path):
    """Read actual width/height straight from the PNG's IHDR chunk — every
    chart here saves with bbox_inches="tight", which crops to content, so
    figsize*dpi is NOT the real saved size; only the file itself knows.
    Stdlib struct read, no Pillow dependency for two integers."""
    with open(path, "rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        return None, None
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def _record_chart(conn, chart_key, paper_id, fpath, commit_sha, params=None, content_hash=None):
    """Shared academic_visualizations insert for every chart call site —
    width/height come from the actual saved PNG (§0's bbox_inches="tight"
    reasoning), generation_params is whatever inputs shaped this specific
    render (each chart function's own return dict's "params" key)."""
    width, height = _png_dimensions(fpath)
    academic_schema.record_visualization(
        conn, chart_key, paper_id, content_hash=content_hash, file_path=fpath,
        commit_sha=commit_sha,
        generation_params=json.dumps(params) if params is not None else None,
        width=width, height=height,
    )


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
    return {"chart": "cross-section-score", "path": output_path,
            "params": {"score": score}}


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
    return {"chart": "document-review-score", "path": output_path,
            "params": {"score": score}}


# ---------------------------------------------------------------------------
# New chart types — §5 of the template+visualization depth proposal
# ---------------------------------------------------------------------------

_CHART_PIPELINE_STAGES = [
    ("generate", "Generate"), ("cite", "Cite"), ("enrich", "Enrich"),
    ("budget", "Budget"), ("det_audit", "Det-Audit"),
    ("sem_audit", "Sem-Audit"), ("plagiarism", "Plagiarism"),
    ("humanize_det", "Humanize-Det"), ("humanize_sem", "Humanize-Sem"),
]


def _pipeline_progress_matrix(plt, paper_id, conn, domains, output_path):
    """12×9 heatmap: domains × pipeline stages, PASS(green)/FAIL(red)/pending(grey)."""
    import numpy as np
    from academic_schema import usecase_status

    _PATTERN = [
        ("generate",          "generate-section-draft-{d}"),
        ("cite",              "section-citations-{d}"),
        ("enrich",            "section-supplementary-content-{d}"),
        ("budget",            "section-budget-fit-{d}"),
        ("det_audit",         "deterministic-audit-{d}"),
        ("sem_audit",         "semantic-audit-{d}"),
        ("plagiarism",        "plagiarism-forensic-audit-{d}"),
        ("humanize_det",      "humanize-deterministic-{d}"),
        ("humanize_sem",      "humanize-semantic-{d}"),
    ]

    n_domains = len(domains)
    n_stages = len(_PATTERN)
    matrix = np.full((n_domains, n_stages), 0.5)  # 0.5 = pending (grey)
    stage_labels = [s[0] for s in _PATTERN]

    for i, (_, domain_key, _, _) in enumerate(domains):
        for j, (_, tpl) in enumerate(_PATTERN):
            uc_name = tpl.replace("{d}", domain_key)
            complete, _ = usecase_status(conn, paper_id, uc_name)
            matrix[i, j] = 1.0 if complete else 0.0

    fig, ax = plt.subplots(figsize=(max(10, n_stages * 0.9),
                                    max(4, n_domains * 0.5)))
    cmap = plt.cm.colors.ListedColormap(["#e74c3c", "#bdc3c7", "#2ecc71"])
    bounds = [-0.5, 0.25, 0.75, 1.5]
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)
    im = ax.imshow(matrix, cmap=cmap, norm=norm, aspect="auto")
    ax.set_xticks(range(n_stages))
    ax.set_xticklabels(stage_labels, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(n_domains))
    ax.set_yticklabels([d[1] for d in domains], fontsize=9)
    ax.set_title("Pipeline Progress")
    plt.colorbar(im, ax=ax, ticks=[0, 0.5, 1],
                 label="FAIL / Pending / PASS")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return {"chart": "pipeline-progress-matrix", "path": output_path,
            "params": {"domain_count": n_domains, "stage_count": n_stages,
                       "stages": stage_labels}}


def _section_part_score_comparison(plt, paper_id, conn, domains, output_path):
    """Grouped bar per domain: citations / enrichment / budget-fit / full scores."""
    import numpy as np

    full_scores = []
    part_data = {"citations": [], "enrichment": [], "budget-fit": []}

    for domain_id, domain_key, _, _ in domains:
        # Full score
        sem = conn.execute(
            "SELECT overall_score FROM academic_semantic_runs "
            "WHERE paper_id=? AND domain_id=? AND scope='section-full' "
            "ORDER BY run_number DESC LIMIT 1",
            (paper_id, domain_id),
        ).fetchone()
        full_scores.append(round(sem["overall_score"], 1) if sem else 0)

        # Part scores (latest per part_kind)
        for pk in ("citations", "enrichment", "budget-fit"):
            row = conn.execute(
                "SELECT overall_score FROM academic_semantic_runs "
                "WHERE paper_id=? AND domain_id=? AND scope='section-part' "
                "AND part_kind=? ORDER BY run_number DESC LIMIT 1",
                (paper_id, domain_id, pk),
            ).fetchone()
            part_data[pk].append(round(row["overall_score"], 1) if row else 0)

    n = len(domains)
    x = np.arange(n)
    width = 0.2
    fig, ax = plt.subplots(figsize=(max(10, n * 0.8), 5))

    colors = {"citations": "#3498db", "enrichment": "#e67e22",
              "budget-fit": "#9b59b6", "full": "#2ecc71"}
    labels_map = {"citations": "Citations", "enrichment": "Enrichment",
                  "budget-fit": "Budget-Fit", "full": "Full"}

    bars_full = ax.bar(x - 1.5 * width, full_scores, width,
                       color=colors["full"], label=labels_map["full"])
    for i, (pk, vals) in enumerate(part_data.items()):
        bars = ax.bar(x + (i - 0.5) * width, vals, width,
                      color=colors[pk], label=labels_map[pk])

    ax.set_xticks(x)
    ax.set_xticklabels([d[1] for d in domains], rotation=45, ha="right",
                        fontsize=8)
    ax.set_ylabel("Score")
    ax.set_title("Section-Part vs Full Score Comparison")
    ax.set_xlim(-0.5, n - 0.5)
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return {"chart": "section-part-score-comparison", "path": output_path,
            "params": {"domain_keys": [d[1] for d in domains],
                       "full_scores": full_scores, "part_scores": part_data}}


def _citation_count_bar(plt, paper_id, conn, domains, output_path):
    """Stacked bar per domain: in-repo vs literature citation counts."""
    import numpy as np

    domain_keys = []
    in_repo_counts = []
    lit_counts = []

    for _, domain_key, _, _ in domains:
        domain_id = conn.execute(
            "SELECT id FROM academic_domains WHERE key=?",
            (domain_key,),
        ).fetchone()
        if not domain_id:
            continue
        row = conn.execute(
            "SELECT COUNT(*) AS total, "
            "SUM(CASE WHEN source_kind='in-repo' THEN 1 ELSE 0 END) AS in_repo, "
            "SUM(CASE WHEN source_kind='literature' THEN 1 ELSE 0 END) AS literature "
            "FROM academic_section_citations "
            "WHERE paper_id=? AND domain_id=?",
            (paper_id, domain_id["id"]),
        ).fetchone()
        if row and row["total"] > 0:
            domain_keys.append(domain_key)
            in_repo_counts.append(row["in_repo"] or 0)
            lit_counts.append(row["literature"] or 0)

    if not domain_keys:
        return None

    n = len(domain_keys)
    x = np.arange(n)
    fig, ax = plt.subplots(figsize=(max(8, n * 0.7), 5))
    ax.bar(x, in_repo_counts, 0.6, label="In-Repo", color="#3498db")
    ax.bar(x, lit_counts, 0.6, bottom=in_repo_counts,
           label="Literature", color="#e67e22")
    ax.set_xticks(x)
    ax.set_xticklabels(domain_keys, rotation=45, ha="right", fontsize=9)
    ax.set_ylabel("Citation Count")
    ax.set_title("Citations per Domain")
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return {"chart": "citation-count-bar", "path": output_path,
            "params": {"domain_keys": domain_keys, "in_repo_counts": in_repo_counts,
                       "literature_counts": lit_counts}}


def _load_domain_word_count_range(calc_dir, domain_key):
    """Extract min/max from a domain's deterministic YAML word_count_in_range check."""
    import yaml
    ypath = os.path.join(calc_dir, "generation", f"{domain_key}.yaml")
    if not os.path.isfile(ypath):
        return None, None
    with open(ypath) as f:
        data = yaml.safe_load(f)
    for check in data.get("checks", []):
        if check.get("rule") == "word_count_in_range":
            cfg = check.get("config", {})
            return cfg.get("min"), cfg.get("max")
    return None, None


def _budget_fit_gauge(plt, paper_id, conn, domains, calc_dir, output_path):
    """Per-domain word count vs configured [min, max], horizontal gauge."""
    import numpy as np

    domain_keys = []
    word_counts = []
    ranges = []

    for _, domain_key, _, _ in domains:
        domain_id = conn.execute(
            "SELECT id FROM academic_domains WHERE key=?",
            (domain_key,),
        ).fetchone()
        if not domain_id:
            continue
        wc_min, wc_max = _load_domain_word_count_range(calc_dir, domain_key)
        if wc_min is None:
            continue
        # Get word count from the budget-fit stage narrative
        row = conn.execute(
            "SELECT word_count FROM academic_narrative_sections "
            "WHERE paper_id=? AND domain_id=? "
            "ORDER BY id DESC LIMIT 1",
            (paper_id, domain_id["id"]),
        ).fetchone()
        wc = row["word_count"] if row and row["word_count"] else 0
        domain_keys.append(domain_key)
        word_counts.append(wc)
        ranges.append((wc_min, wc_max))

    if not domain_keys:
        return None

    n = len(domain_keys)
    fig, ax = plt.subplots(figsize=(10, max(3, n * 0.5)))

    for i, (dk, wc, (lo, hi)) in enumerate(
            zip(domain_keys, word_counts, ranges)):
        color = "#2ecc71" if lo <= wc <= hi else "#e74c3c"
        ax.barh(i, wc, color=color, height=0.5, zorder=2)
        ax.barh(i, hi - lo, left=lo, color="#ecf0f1", height=0.7, zorder=1)
        ax.text(wc + (hi * 0.02), i, str(wc), va="center", fontsize=8)

    ax.set_yticks(range(n))
    ax.set_yticklabels(domain_keys, fontsize=9)
    ax.set_xlabel("Word Count")
    ax.set_title("Budget-Fit: Word Count vs Range")
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return {"chart": "budget-fit-gauge", "path": output_path,
            "params": {"domain_keys": domain_keys, "word_counts": word_counts,
                       "ranges": ranges}}


def _whole_paper_budget_gauge(plt, paper_id, conn, calc_dir, output_path):
    """Total word count vs paper-budget.yaml's range."""
    import yaml
    import numpy as np

    # Get configured range
    budget_path = os.path.join(calc_dir, "report", "summary", "paper-budget.yaml")
    if not os.path.isfile(budget_path):
        return None
    with open(budget_path) as f:
        budget = yaml.safe_load(f)
    twc = budget.get("total_word_count", {})
    wc_min = twc.get("min", 0)
    wc_max = twc.get("max", 0)

    # Get actual total word count from budget-fit narratives
    row = conn.execute(
        "SELECT SUM(ns.word_count) AS total_wc "
        "FROM academic_narrative_sections ns "
        "JOIN academic_narratives n ON n.id = ns.narrative_id "
        "WHERE n.paper_id=? AND n.stage='budget-fit'",
        (paper_id,),
    ).fetchone()
    total_wc = row["total_wc"] if row and row["total_wc"] else 0

    fig, ax = plt.subplots(figsize=(8, 3))
    color = "#2ecc71" if wc_min <= total_wc <= wc_max else "#e74c3c"
    # Background range bar
    ax.barh(0, wc_max - wc_min, left=wc_min, color="#ecf0f1",
            height=0.6, zorder=1)
    # Actual word count bar
    ax.barh(0, total_wc, color=color, height=0.5, zorder=2)
    ax.text(total_wc + (wc_max * 0.01), 0, str(total_wc),
            va="center", fontsize=10)
    ax.set_yticks([0])
    ax.set_yticklabels(["Total"])
    ax.set_xlabel("Word Count")
    ax.set_title(f"Whole-Paper Budget: [{wc_min}, {wc_max}]")
    ax.set_xlim(0, wc_max * 1.15)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return {"chart": "whole-paper-budget-gauge", "path": output_path,
            "params": {"total_word_count": total_wc, "range": [wc_min, wc_max]}}


def _humanize_pass_chart(plt, paper_id, conn, domains, output_path):
    """Bar per domain: deterministic-only resolved vs needed-semantic-pass."""
    import numpy as np

    domain_keys = []
    det_only = []
    needed_sem = []

    for _, domain_key, _, _ in domains:
        domain_id = conn.execute(
            "SELECT id FROM academic_domains WHERE key=?",
            (domain_key,),
        ).fetchone()
        if not domain_id:
            continue

        # Check if flagged by plagiarism
        flagged = conn.execute(
            "SELECT 1 FROM academic_plagiarism_findings "
            "WHERE paper_id=? AND domain_id=? AND verdict='FAIL' "
            "AND pass_type='forensic' LIMIT 1",
            (paper_id, domain_id["id"]),
        ).fetchone()
        if not flagged:
            continue

        det_count = conn.execute(
            "SELECT COUNT(*) FROM academic_humanize_passes "
            "WHERE paper_id=? AND domain_id=? AND pass_kind='deterministic'",
            (paper_id, domain_id["id"]),
        ).fetchone()[0]
        sem_count = conn.execute(
            "SELECT COUNT(*) FROM academic_humanize_passes "
            "WHERE paper_id=? AND domain_id=? AND pass_kind='semantic'",
            (paper_id, domain_id["id"]),
        ).fetchone()[0]

        domain_keys.append(domain_key)
        det_only.append(det_count)
        needed_sem.append(sem_count)

    if not domain_keys:
        return None

    n = len(domain_keys)
    x = np.arange(n)
    fig, ax = plt.subplots(figsize=(max(8, n * 0.7), 4))
    ax.bar(x - 0.2, det_only, 0.35, label="Deterministic Pass",
           color="#3498db")
    ax.bar(x + 0.2, needed_sem, 0.35, label="Semantic Pass",
           color="#e67e22")
    ax.set_xticks(x)
    ax.set_xticklabels(domain_keys, rotation=45, ha="right", fontsize=9)
    ax.set_ylabel("Pass Count")
    ax.set_title("Humanize Passes by Domain")
    ax.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return {"chart": "humanize-pass-chart", "path": output_path,
            "params": {"domain_keys": domain_keys, "deterministic_pass_counts": det_only,
                       "semantic_pass_counts": needed_sem}}


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload.get("paper_id")
    chart_specs = payload.get("charts", ["domain-score-bar"])
    commit_sha = payload.get("commit_sha", "")

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
                _record_chart(conn, "domain-score-bar", paper_id, fpath, commit_sha,
                             params={"domain_keys": domain_keys, "scores": scores},
                             content_hash=content_hash)
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
                _record_chart(conn, "deterministic-findings-heatmap", paper_id, fpath, commit_sha,
                             params={"domain_keys": list(check_results.keys())})
                generated.append({"chart": "deterministic-findings-heatmap",
                                  "path": fpath})

        if "cross-section-score" in chart_specs:
            fpath = os.path.join(output_dir, "cross-section-score.png")
            result = _cross_section_score_chart(plt, paper_id, conn, fpath)
            if result:
                _record_chart(conn, "cross-section-score", paper_id, fpath, commit_sha,
                             params=result.get("params"))
                generated.append(result)

        if "document-review-score" in chart_specs:
            fpath = os.path.join(output_dir, "document-review-score.png")
            result = _document_review_score_chart(plt, paper_id, conn, fpath)
            if result:
                _record_chart(conn, "document-review-score", paper_id, fpath, commit_sha,
                             params=result.get("params"))
                generated.append(result)

        calc_dir = str(SCRIPTS_DIR / ".." / "calculation")

        if "pipeline-progress-matrix" in chart_specs:
            fpath = os.path.join(output_dir, "pipeline-progress-matrix.png")
            result = _pipeline_progress_matrix(
                plt, paper_id, conn, domains, fpath)
            if result:
                _record_chart(conn, "pipeline-progress-matrix", paper_id, fpath, commit_sha,
                             params=result.get("params"))
                generated.append(result)

        if "section-part-score-comparison" in chart_specs:
            fpath = os.path.join(output_dir, "section-part-score-comparison.png")
            result = _section_part_score_comparison(
                plt, paper_id, conn, domains, fpath)
            if result:
                _record_chart(conn, "section-part-score-comparison", paper_id, fpath, commit_sha,
                             params=result.get("params"))
                generated.append(result)

        if "citation-count-bar" in chart_specs:
            fpath = os.path.join(output_dir, "citation-count-bar.png")
            result = _citation_count_bar(
                plt, paper_id, conn, domains, fpath)
            if result:
                _record_chart(conn, "citation-count-bar", paper_id, fpath, commit_sha,
                             params=result.get("params"))
                generated.append(result)

        if "budget-fit-gauge" in chart_specs:
            fpath = os.path.join(output_dir, "budget-fit-gauge.png")
            result = _budget_fit_gauge(
                plt, paper_id, conn, domains, calc_dir, fpath)
            if result:
                _record_chart(conn, "budget-fit-gauge", paper_id, fpath, commit_sha,
                             params=result.get("params"))
                generated.append(result)

        if "whole-paper-budget-gauge" in chart_specs:
            fpath = os.path.join(output_dir, "whole-paper-budget-gauge.png")
            result = _whole_paper_budget_gauge(
                plt, paper_id, conn, calc_dir, fpath)
            if result:
                _record_chart(conn, "whole-paper-budget-gauge", paper_id, fpath, commit_sha,
                             params=result.get("params"))
                generated.append(result)

        if "humanize-pass-chart" in chart_specs:
            fpath = os.path.join(output_dir, "humanize-pass-chart.png")
            result = _humanize_pass_chart(
                plt, paper_id, conn, domains, fpath)
            if result:
                _record_chart(conn, "humanize-pass-chart", paper_id, fpath, commit_sha,
                             params=result.get("params"))
                generated.append(result)

        write_envelope(out_path, status="ok",
                       message=f"generated {len(generated)} charts",
                       charts=generated)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
