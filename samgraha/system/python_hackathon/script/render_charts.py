"""
render_charts.py — 7 chart functions producing PNG files via matplotlib.

Each function takes data + output path, produces one chart.
Called by run_reporting.py after markdown template rendering.

Chart catalog (7 types):
  1. field_distribution    — team's score vs field distribution (per domain)
  2. rank_distribution     — all teams' scores for one domain
  3. det_sem_contribution  — weighted det/sem split for one domain
  4. rule_pass_rate        — severity × passed breakdown (per domain)
  5. model_spread          — dot-plot of semantic model scores (per domain)
  6. team_radar            — 10-spoke radar of team's domain scores
  7. domain_weights        — horizontal bar of scoring methodology weights
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
import yaml
from math import pi


SYSTEM_DIR = os.path.join(os.path.dirname(__file__), "..")
DOMAINS = [
    "01-infrastructure", "02-engineering", "03-testing",
    "04-documentation", "05-security", "06-mlops",
    "07-runtime", "08-team-workflow", "09-data-quality",
    "10-ai-explanations",
]
DOMAIN_NAMES = [
    "infrastructure", "engineering", "testing",
    "documentation", "security", "mlops",
    "runtime", "team_workflow", "data_quality",
    "ai_explanations",
]
DOMAIN_SHORT = [
    "Infra", "Eng", "Test", "Docs", "Sec",
    "MLOps", "Runtime", "Team", "DataQ", "AIExpl",
]

COLORS = {
    "primary": "#0969da",       # accent-fg
    "secondary": "#8250df",     # accent-emphasis (purple, Primer default)
    "success": "#1a7f37",       # success-fg
    "danger": "#cf222e",        # danger-fg
    "warning": "#9a6700",       # attention-fg
    "neutral": "#656d76",       # fg-muted
    "light": "#f6f8fa",         # canvas-subtle
    "bg": "#ffffff",            # canvas
    "text": "#1f2328",          # fg-default
}

SEVERITY_COLORS = {
    "error": COLORS["danger"],
    "warning": COLORS["warning"],
    "info": COLORS["neutral"],
}


def _ensure_dir(path):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)


def _apply_style(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="both", which="major", labelsize=9)
    ax.xaxis.label.set_fontsize(9)
    ax.yaxis.label.set_fontsize(9)


# ---------------------------------------------------------------------------
# Chart 1: Field Distribution
# ---------------------------------------------------------------------------

def chart_field_distribution(team_score, global_mean, global_stdev,
                             domain_name, output_path):
    """
    Show where one team's score sits against the field distribution.
    Uses a normal curve overlay on a bar histogram.
    """
    _ensure_dir(output_path)

    fig, ax = plt.subplots(figsize=(6, 3.5))

    # Generate synthetic distribution from mean/stdev
    if global_stdev > 0:
        x = np.linspace(max(0, global_mean - 3 * global_stdev),
                        min(100, global_mean + 3 * global_stdev), 100)
        y = (1 / (global_stdev * np.sqrt(2 * np.pi))) * np.exp(
            -0.5 * ((x - global_mean) / global_stdev) ** 2
        )
        ax.fill_between(x, y, alpha=0.15, color=COLORS["primary"])
        ax.plot(x, y, color=COLORS["primary"], linewidth=1.5)

    # Team marker
    ax.axvline(x=team_score, color=COLORS["danger"], linewidth=2,
               linestyle="--", label=f"Team: {team_score:.1f}")
    ax.axvline(x=global_mean, color=COLORS["primary"], linewidth=1.5,
               linestyle="-", label=f"Mean: {global_mean:.1f}")

    ax.set_title(f"Score Distribution — {domain_name}", fontsize=11,
                 fontweight="bold", color=COLORS["text"])
    ax.set_xlabel("Score")
    ax.set_ylabel("Density")
    ax.legend(fontsize=8, loc="upper right")
    _apply_style(ax)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight",
                facecolor=COLORS["bg"])
    plt.close(fig)


# ---------------------------------------------------------------------------
# Chart 2: Rank Distribution
# ---------------------------------------------------------------------------

def chart_rank_distribution(teams_data, domain_name, output_path):
    """
    Bar chart of all teams' scores for one domain, sorted descending.
    teams_data: list of {"team": str, "score": float}
    """
    _ensure_dir(output_path)

    sorted_teams = sorted(teams_data, key=lambda t: t["score"], reverse=True)
    names = [t["team"] for t in sorted_teams]
    scores = [t["score"] for t in sorted_teams]

    fig, ax = plt.subplots(figsize=(max(6, len(names) * 0.5), 4))

    bar_colors = [COLORS["primary"]] * len(names)
    if names:
        bar_colors[0] = COLORS["success"]

    ax.bar(range(len(names)), scores, color=bar_colors, edgecolor="white",
           linewidth=0.5)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha="right", fontsize=7)
    ax.set_ylabel("Score")
    ax.set_title(f"Rank Distribution — {domain_name}", fontsize=11,
                 fontweight="bold", color=COLORS["text"])
    _apply_style(ax)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight",
                facecolor=COLORS["bg"])
    plt.close(fig)


# ---------------------------------------------------------------------------
# Chart 3: Det vs Sem Contribution
# ---------------------------------------------------------------------------

def chart_det_sem_contribution(det_score, sem_score, det_weight, sem_weight,
                               domain_name, output_path):
    """
    Stacked horizontal bar showing weighted deterministic vs semantic
    contribution to the raw merge score.
    """
    _ensure_dir(output_path)

    det_contrib = det_weight * det_score
    sem_contrib = sem_weight * sem_score
    total = det_contrib + sem_contrib

    fig, ax = plt.subplots(figsize=(6, 2.5))

    ax.barh(0, det_contrib, color=COLORS["primary"], height=0.5,
            label=f"Deterministic ({det_weight:.0%}): {det_contrib:.1f}")
    ax.barh(0, sem_contrib, left=det_contrib, color=COLORS["secondary"],
            height=0.5, label=f"Semantic ({sem_weight:.0%}): {sem_contrib:.1f}")

    ax.set_xlim(0, max(total * 1.1, 1))
    ax.set_yticks([])
    ax.set_xlabel("Weighted Score Contribution")
    ax.set_title(f"Score Composition — {domain_name} (merge: {total:.1f})",
                 fontsize=11, fontweight="bold", color=COLORS["text"])
    ax.legend(fontsize=8, loc="upper right", framealpha=0.9)
    _apply_style(ax)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight",
                facecolor=COLORS["bg"])
    plt.close(fig)


# ---------------------------------------------------------------------------
# Chart 4: Rule Pass Rate
# ---------------------------------------------------------------------------

def chart_rule_pass_rate(rules, domain_name, output_path):
    """
    Grouped bar chart: severity (error/warning/info) × passed/failed.
    rules: list of {"severity": str, "passed": bool}
    """
    _ensure_dir(output_path)

    severities = ["error", "warning", "info"]
    buckets = {s: {"passed": 0, "failed": 0} for s in severities}

    for r in rules:
        sev = r.get("severity", "warning")
        if sev not in buckets:
            sev = "warning"
        if r.get("passed", False):
            buckets[sev]["passed"] += 1
        else:
            buckets[sev]["failed"] += 1

    labels = [s for s in severities if buckets[s]["passed"] + buckets[s]["failed"] > 0]
    passed_vals = [buckets[s]["passed"] for s in labels]
    failed_vals = [buckets[s]["failed"] for s in labels]
    bar_colors_pass = [COLORS["success"] for _ in labels]
    bar_colors_fail = [COLORS["danger"] for _ in labels]

    fig, ax = plt.subplots(figsize=(6, 3.5))

    x = np.arange(len(labels))
    width = 0.35

    if any(v > 0 for v in passed_vals):
        ax.bar(x - width / 2, passed_vals, width, color=COLORS["success"],
               label="Passed", edgecolor="white", linewidth=0.5)
    if any(v > 0 for v in failed_vals):
        ax.bar(x + width / 2, failed_vals, width, color=COLORS["danger"],
               label="Failed", edgecolor="white", linewidth=0.5)

    ax.set_xticks(x)
    ax.set_xticklabels([s.capitalize() for s in labels], fontsize=9)
    ax.set_ylabel("Rule Count")
    ax.set_title(f"Rule Pass Rate by Severity — {domain_name}", fontsize=11,
                 fontweight="bold", color=COLORS["text"])
    ax.legend(fontsize=8)
    _apply_style(ax)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight",
                facecolor=COLORS["bg"])
    plt.close(fig)


# ---------------------------------------------------------------------------
# Chart 5: Model Score Spread
# ---------------------------------------------------------------------------

def chart_model_spread(model_results, domain_name, output_path, mean_score=0):
    """
    Dot-plot of semantic model scores for one domain.
    model_results: list of {"model_name": str, "score": float}
    Skip if < 3 models (not enough for meaningful spread).
    """
    _ensure_dir(output_path)

    if len(model_results) < 3:
        return

    names = [m["model_name"] for m in model_results]
    scores = [m["score"] for m in model_results]

    fig, ax = plt.subplots(figsize=(6, max(2.5, len(names) * 0.6)))

    y_pos = range(len(names))
    ax.scatter(scores, y_pos, color=COLORS["secondary"], s=80, zorder=3)

    for i, (s, n) in enumerate(zip(scores, names)):
        ax.text(s + 1, i, f"{s:.1f}", va="center", fontsize=8, color=COLORS["text"])

    if mean_score > 0:
        ax.axvline(x=mean_score, color=COLORS["primary"], linewidth=1.5,
                   linestyle="--", alpha=0.7, label=f"Mean: {mean_score:.1f}")

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(names, fontsize=8)
    ax.set_xlabel("Score")
    ax.set_title(f"Model Score Spread — {domain_name}", fontsize=11,
                 fontweight="bold", color=COLORS["text"])
    if mean_score > 0:
        ax.legend(fontsize=8, loc="lower right")
    _apply_style(ax)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight",
                facecolor=COLORS["bg"])
    plt.close(fig)


# ---------------------------------------------------------------------------
# Chart 6: Team Radar
# ---------------------------------------------------------------------------

def chart_team_radar(domain_scores_list, team_name, output_path):
    """
    10-spoke radar chart of a team's domain scores.
    domain_scores_list: list of {"domain": str, "score": float}
    """
    _ensure_dir(output_path)

    labels = [d["domain"] for d in domain_scores_list]
    values = [d["score"] for d in domain_scores_list]
    n = len(labels)

    if n < 3:
        return

    # Compute angle for each axis
    angles = [pi * i / n for i in range(n)]
    angles += angles[:1]  # close the polygon
    values_plot = values + values[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    ax.plot(angles, values_plot, color=COLORS["primary"], linewidth=2,
            linestyle="-")
    ax.fill(angles, values_plot, color=COLORS["primary"], alpha=0.15)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_ylim(0, max(max(values) * 1.2, 1))
    ax.set_title(f"Domain Profile — {team_name}", fontsize=12,
                 fontweight="bold", color=COLORS["text"], pad=20)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight",
                facecolor=COLORS["bg"])
    plt.close(fig)


# ---------------------------------------------------------------------------
# Chart 7: Domain Weights
# ---------------------------------------------------------------------------

def chart_domain_weights(output_path):
    """
    Horizontal bar chart of scoring methodology weights from weights.yaml.
    Static — same for every team/run.
    """
    _ensure_dir(output_path)

    weights_path = os.path.join(SYSTEM_DIR, "calculation", "weights.yaml")
    try:
        with open(weights_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
    except (yaml.YAMLError, OSError):
        return

    domains_cfg = cfg.get("domains", {})
    if not domains_cfg:
        return

    names = list(domains_cfg.keys())
    weights = [domains_cfg[n]["weight"] for n in names]

    # Sort by weight descending
    paired = sorted(zip(weights, names), reverse=True)
    weights_sorted = [p[0] for p in paired]
    names_sorted = [p[1] for p in paired]

    fig, ax = plt.subplots(figsize=(7, max(3, len(names) * 0.5)))

    y_pos = range(len(names_sorted))
    bars = ax.barh(y_pos, weights_sorted, color=COLORS["primary"],
                   edgecolor="white", linewidth=0.5, height=0.6)

    for bar, w in zip(bars, weights_sorted):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                str(w), va="center", fontsize=9, color=COLORS["text"])

    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(names_sorted, fontsize=9)
    ax.set_xlabel("Weight (of 100)")
    ax.set_title("Scoring Methodology — Domain Weights", fontsize=11,
                 fontweight="bold", color=COLORS["text"])
    _apply_style(ax)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight",
                facecolor=COLORS["bg"])
    plt.close(fig)


# ---------------------------------------------------------------------------
# CLI entrypoint — generate charts from a JSON spec
# ---------------------------------------------------------------------------

def generate_charts(spec, output_dir):
    """
    Generate charts based on a specification dict.

    spec keys:
      - domain_charts: {"{participant}_{domain}": {team_score, global_mean, ...}}
      - rank_charts: {domain_name: {teams_data}} — once per domain
      - team_charts: {team_name: {domain_scores_list}}
    """
    os.makedirs(output_dir, exist_ok=True)

    # Rank distribution — once per domain (chart 2)
    for domain_name, data in spec.get("rank_charts", {}).items():
        if "teams_data" in data:
            chart_rank_distribution(
                data["teams_data"],
                domain_name,
                os.path.join(output_dir, f"{domain_name}-rank-distribution.png"),
            )

    # Domain-specific charts (1, 3-5), keyed by "{participant}_{domain}"
    for chart_key, data in spec.get("domain_charts", {}).items():
        parts = chart_key.split("_", 1)
        pname = parts[0] if len(parts) > 1 else "unknown"
        domain_name = parts[1] if len(parts) > 1 else chart_key
        safe_key = chart_key.replace("_", "-")

        # 1. Field distribution
        if "team_score" in data:
            chart_field_distribution(
                data["team_score"],
                data.get("global_mean", 0),
                data.get("global_stdev", 0),
                f"{pname} — {domain_name}",
                os.path.join(output_dir, f"{safe_key}-field-distribution.png"),
            )

        # 3. Det vs sem contribution
        if "det_score" in data and "sem_score" in data:
            chart_det_sem_contribution(
                data["det_score"],
                data["sem_score"],
                data.get("det_weight", 0.6),
                data.get("sem_weight", 0.4),
                f"{pname} — {domain_name}",
                os.path.join(output_dir, f"{safe_key}-det-sem-contribution.png"),
            )

        # 4. Rule pass rate
        if "rules" in data:
            chart_rule_pass_rate(
                data["rules"],
                domain_name,
                os.path.join(output_dir, f"{safe_key}-rule-pass-rate.png"),
            )

        # 5. Model spread
        if "model_results" in data:
            chart_model_spread(
                data["model_results"],
                domain_name,
                os.path.join(output_dir, f"{safe_key}-model-spread.png"),
                mean_score=data.get("mean_score", 0),
            )

    # 6. Team radar charts
    for team_name, data in spec.get("team_charts", {}).items():
        if "domain_scores_list" in data:
            chart_team_radar(
                data["domain_scores_list"],
                team_name,
                os.path.join(output_dir, f"{team_name}-radar.png"),
            )

    # 7. Domain weights (static, once)
    chart_domain_weights(os.path.join(output_dir, "domain-weights.png"))

    print(f"Charts written to {output_dir}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate report charts")
    parser.add_argument("--spec", required=True,
                        help="Path to chart specification JSON")
    parser.add_argument("--output", required=True,
                        help="Output directory for PNG files")
    args = parser.parse_args()

    with open(args.spec, "r", encoding="utf-8") as f:
        spec = json.load(f)

    generate_charts(spec, args.output)
