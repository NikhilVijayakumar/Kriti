"""visualize.py — Matplotlib visualizations for base_dev audit data.

Reads check result JSONs, deterministic audit YAMLs, semantic audit MDs,
and calculation scores to produce publication-quality PNG charts.

Usage:
  python visualize.py --results-dir <path> --out-dir <path>
  python visualize.py --results-dir <path> --out-dir <path> --scores-json <path>
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from _common import load_yaml, read_text, write_text, ALL_DOMAINS, DOMAIN_NUMS


# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------

COLORS = {
    "pass": "#2ecc71",
    "fail": "#e74c3c",
    "error": "#f39c12",
    "not_applicable": "#95a5a6",
    "Excellent": "#27ae60",
    "Very Good": "#2ecc71",
    "Good": "#f39c12",
    "Acceptable": "#e67e22",
    "Needs Improvement": "#e74c3c",
    "N/A": "#bdc3c7",
}

DOMAIN_COLORS = [
    "#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6",
    "#1abc9c", "#e67e22", "#34495e", "#e91e63", "#00bcd4",
    "#8bc34a", "#ff5722", "#607d8b", "#795548", "#cddc39",
    "#ff9800",
]


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_check_results(results_dir: Path) -> list[dict[str, Any]]:
    """Load all check result JSONs from a results directory."""
    results = []
    for json_file in results_dir.rglob("*.json"):
        if json_file.name == "results.json":
            continue
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "check" in data and "status" in data:
                results.append(data)
        except (json.JSONDecodeError, KeyError):
            continue
    return results


def load_deterministic_rules(system_root: Path) -> dict[str, list[dict]]:
    """Load all deterministic audit rules indexed by domain."""
    rules: dict[str, list[dict]] = {}
    audit_dir = system_root / "audit" / "deterministic"

    # Document-level rules
    doc_dir = audit_dir / "document"
    if doc_dir.is_dir():
        for yaml_file in sorted(doc_dir.glob("*.yaml")):
            if "-relationships" in yaml_file.name:
                continue
            data = load_yaml(yaml_file)
            domain = data.get("domain", yaml_file.stem.split("-")[0])
            rules.setdefault(domain, []).extend(data.get("rules", []))

    # Section-level rules
    sec_dir = audit_dir / "section"
    if sec_dir.is_dir():
        for domain_dir in sorted(sec_dir.iterdir()):
            if not domain_dir.is_dir():
                continue
            domain = domain_dir.name
            for yaml_file in sorted(domain_dir.glob("*.yaml")):
                data = load_yaml(yaml_file)
                rules.setdefault(domain, []).extend(data.get("rules", []))

    return rules


def load_semantic_criteria(system_root: Path) -> dict[str, list[dict]]:
    """Load semantic audit criteria from markdown files."""
    criteria: dict[str, list[dict]] = {}
    audit_dir = system_root / "audit" / "semantic"

    for md_file in sorted(audit_dir.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        # Extract domain from path
        parts = md_file.parts
        try:
            sec_idx = parts.index("semantic")
            domain = parts[sec_idx + 2] if len(parts) > sec_idx + 2 else "unknown"
        except ValueError:
            domain = "unknown"

        # Parse scoring criteria table
        in_table = False
        for line in content.split("\n"):
            if "| ID |" in line and "Weight |" in line:
                in_table = True
                continue
            if in_table and line.startswith("|---"):
                continue
            if in_table and line.startswith("| C"):
                cols = [c.strip() for c in line.split("|") if c.strip()]
                if len(cols) >= 4:
                    criteria.setdefault(domain, []).append({
                        "id": cols[0],
                        "weight": cols[1],
                        "score": cols[2],
                        "description": cols[3],
                    })
            elif in_table and not line.startswith("|"):
                in_table = False

    return criteria


def load_scores_json(scores_path: Path) -> dict[str, Any]:
    """Load a scores JSON file (from calculate.py output or results.json)."""
    if scores_path.exists():
        return json.loads(scores_path.read_text(encoding="utf-8"))
    return {}


# ---------------------------------------------------------------------------
# Chart generation
# ---------------------------------------------------------------------------

def chart_check_results_by_domain(
    check_results: list[dict[str, Any]],
    out_dir: Path,
) -> Path:
    """Bar chart: pass/fail/error counts per domain."""
    domain_stats: dict[str, dict[str, int]] = {}
    for r in check_results:
        domain = r.get("domain", "unknown")
        status = r.get("status", "error")
        domain_stats.setdefault(domain, {"pass": 0, "fail": 0, "error": 0, "not_applicable": 0})
        if status in domain_stats[domain]:
            domain_stats[domain][status] += 1

    if not domain_stats:
        return _empty_chart(out_dir, "check_results_by_domain", "No check results found")

    domains = sorted(domain_stats.keys())
    fig, ax = plt.subplots(figsize=(14, 7))

    x = np.arange(len(domains))
    width = 0.2
    statuses = ["pass", "fail", "error", "not_applicable"]

    for i, status in enumerate(statuses):
        counts = [domain_stats[d].get(status, 0) for d in domains]
        if any(c > 0 for c in counts):
            ax.bar(x + i * width, counts, width, label=status.replace("_", " ").title(),
                   color=COLORS[status], edgecolor="white", linewidth=0.5)

    ax.set_xlabel("Domain", fontsize=11)
    ax.set_ylabel("Check Count", fontsize=11)
    ax.set_title("Deterministic Check Results by Domain", fontsize=14, fontweight="bold")
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels([d.split("-", 1)[-1] if "-" in d else d for d in domains],
                       rotation=45, ha="right", fontsize=9)
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    out_path = out_dir / "check_results_by_domain.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def chart_category_breakdown(
    check_results: list[dict[str, Any]],
    out_dir: Path,
) -> Path:
    """Stacked bar: category A/B/C pass vs fail."""
    cat_stats: dict[str, dict[str, int]] = {}
    for r in check_results:
        cat = r.get("category", "unknown")
        status = r.get("status", "error")
        cat_stats.setdefault(cat, {"pass": 0, "fail": 0, "error": 0})
        if status in ("pass", "fail", "error"):
            cat_stats[cat][status] += 1

    if not cat_stats:
        return _empty_chart(out_dir, "category_breakdown", "No check results found")

    cats = sorted(cat_stats.keys())
    fig, ax = plt.subplots(figsize=(8, 6))

    pass_vals = [cat_stats[c].get("pass", 0) for c in cats]
    fail_vals = [cat_stats[c].get("fail", 0) for c in cats]
    error_vals = [cat_stats[c].get("error", 0) for c in cats]

    x = np.arange(len(cats))
    width = 0.5

    ax.bar(x, pass_vals, width, label="Pass", color=COLORS["pass"], edgecolor="white")
    ax.bar(x, fail_vals, width, bottom=pass_vals, label="Fail", color=COLORS["fail"], edgecolor="white")
    ax.bar(x, error_vals, width, bottom=[p + f for p, f in zip(pass_vals, fail_vals)],
           label="Error", color=COLORS["error"], edgecolor="white")

    cat_labels = {"A": "A — Automated", "B": "B — Semi-automated", "C": "C — Cross-domain"}
    ax.set_xticks(x)
    ax.set_xticklabels([cat_labels.get(c, c) for c in cats], fontsize=10)
    ax.set_ylabel("Check Count", fontsize=11)
    ax.set_title("Check Results by Category", fontsize=14, fontweight="bold")
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    out_path = out_dir / "category_breakdown.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def chart_rule_weights_heatmap(
    deterministic_rules: dict[str, list[dict]],
    out_dir: Path,
) -> Path:
    """Heatmap: rule weights by domain, colored by severity."""
    domains = sorted(deterministic_rules.keys())
    if not domains:
        return _empty_chart(out_dir, "rule_weights_heatmap", "No deterministic rules found")

    # Build matrix: max weight per domain
    max_weights = []
    rule_counts = []
    for d in domains:
        rules = deterministic_rules[d]
        weights = [r.get("weight", 0) for r in rules]
        max_weights.append(max(weights) if weights else 0)
        rule_counts.append(len(rules))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), gridspec_kw={"width_ratios": [3, 1]})

    # Left: heatmap-style bar chart of max weight per domain
    colors = []
    for w in max_weights:
        if w >= 2.0:
            colors.append("#e74c3c")
        elif w >= 1.5:
            colors.append("#f39c12")
        elif w >= 1.0:
            colors.append("#3498db")
        else:
            colors.append("#95a5a6")

    y = np.arange(len(domains))
    ax1.barh(y, max_weights, color=colors, edgecolor="white", height=0.7)
    ax1.set_yticks(y)
    ax1.set_yticklabels([d.split("-", 1)[-1] if "-" in d else d for d in domains], fontsize=9)
    ax1.set_xlabel("Max Rule Weight", fontsize=11)
    ax1.set_title("Rule Weight Severity by Domain", fontsize=13, fontweight="bold")
    ax1.grid(axis="x", alpha=0.3)

    # Right: rule count per domain
    ax2.barh(y, rule_counts, color="#3498db", alpha=0.6, height=0.7)
    ax2.set_yticks(y)
    ax2.set_yticklabels([], fontsize=9)
    ax2.set_xlabel("Rule Count", fontsize=11)
    ax2.set_title("Total Rules", fontsize=13, fontweight="bold")
    ax2.grid(axis="x", alpha=0.3)

    fig.suptitle("Deterministic Audit Rule Distribution", fontsize=15, fontweight="bold", y=1.02)
    fig.tight_layout()

    out_path = out_dir / "rule_weights_heatmap.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def chart_scoring_radar(
    scores: dict[str, Any],
    out_dir: Path,
) -> Path:
    """Radar/spider chart: 4-bucket score breakdown."""
    buckets = {
        "Det. Document": scores.get("deterministic_whole", {}).get("score", 0),
        "Det. Section": scores.get("deterministic_section", {}).get("score", 0),
        "Sem. Document": scores.get("semantic_whole", {}).get("score", 0),
        "Sem. Section": scores.get("semantic_section", {}).get("score", 0),
    }

    if all(v == 0 for v in buckets.values()):
        return _empty_chart(out_dir, "scoring_radar", "No scores data available")

    labels = list(buckets.keys())
    values = list(buckets.values())
    num_vars = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values_plot = values + [values[0]]
    angles_plot = angles + [angles[0]]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles_plot, values_plot, "o-", linewidth=2, color="#3498db")
    ax.fill(angles_plot, values_plot, alpha=0.25, color="#3498db")
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylim(0, 100)
    ax.set_title("4-Bucket Score Breakdown", fontsize=14, fontweight="bold", pad=20)

    # Add score labels
    for angle, value, label in zip(angles, values, labels):
        ax.annotate(f"{value:.0f}", xy=(angle, value), fontsize=9,
                    ha="center", va="bottom", fontweight="bold")

    fig.tight_layout()
    out_path = out_dir / "scoring_radar.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def chart_score_bands(
    all_domain_scores: dict[str, dict[str, Any]],
    out_dir: Path,
) -> Path:
    """Horizontal stacked bar: score band distribution across domains."""
    if not all_domain_scores:
        return _empty_chart(out_dir, "score_bands", "No domain scores available")

    bands = ["Excellent", "Very Good", "Good", "Acceptable", "Needs Improvement"]
    band_counts = {b: 0 for b in bands}
    domain_bands = {}

    for domain, score_data in all_domain_scores.items():
        rating = score_data.get("score_bands", {}).get("rating", "N/A")
        domain_bands[domain] = rating
        if rating in band_counts:
            band_counts[rating] += 1

    if not any(v > 0 for v in band_counts.values()):
        return _empty_chart(out_dir, "score_bands", "No valid ratings found")

    fig, ax = plt.subplots(figsize=(10, 6))

    # Pie chart of band distribution
    labels = [b for b in bands if band_counts[b] > 0]
    sizes = [band_counts[b] for b in labels]
    colors = [COLORS[b] for b in labels]

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors, autopct="%1.0f%%",
        startangle=90, textprops={"fontsize": 10},
    )
    for autotext in autotexts:
        autotext.set_fontweight("bold")

    ax.set_title("Score Band Distribution", fontsize=14, fontweight="bold")
    fig.tight_layout()

    out_path = out_dir / "score_bands.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def chart_domain_scores_bar(
    all_domain_scores: dict[str, dict[str, Any]],
    out_dir: Path,
) -> Path:
    """Bar chart: final score per domain with rating color coding."""
    if not all_domain_scores:
        return _empty_chart(out_dir, "domain_scores", "No domain scores available")

    domains = sorted(all_domain_scores.keys())
    scores_list = []
    colors_list = []

    for d in domains:
        s = all_domain_scores[d].get("final_score", {}).get("score", 0)
        r = all_domain_scores[d].get("score_bands", {}).get("rating", "N/A")
        scores_list.append(s)
        colors_list.append(COLORS.get(r, COLORS["N/A"]))

    fig, ax = plt.subplots(figsize=(14, 7))
    x = np.arange(len(domains))
    bars = ax.bar(x, scores_list, color=colors_list, edgecolor="white", linewidth=0.5)

    # Add score labels on bars
    for bar, score in zip(bars, scores_list):
        if score > 0:
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                    f"{score:.0f}", ha="center", va="bottom", fontsize=8, fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels([d.split("-", 1)[-1] if "-" in d else d for d in domains],
                       rotation=45, ha="right", fontsize=9)
    ax.set_ylabel("Final Score", fontsize=11)
    ax.set_title("Documentation Score by Domain", fontsize=14, fontweight="bold")
    ax.set_ylim(0, 105)
    ax.axhline(y=70, color="#e67e22", linestyle="--", alpha=0.5, label="Acceptable threshold (70)")
    ax.axhline(y=95, color="#27ae60", linestyle="--", alpha=0.5, label="Excellent threshold (95)")
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()

    out_path = out_dir / "domain_scores.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def chart_section_pass_rate_heatmap(
    check_results: list[dict[str, Any]],
    out_dir: Path,
) -> Path:
    """Heatmap: pass rate by domain × check, showing weakest areas."""
    # Build matrix
    domain_checks: dict[str, dict[str, str]] = {}
    for r in check_results:
        domain = r.get("domain", "unknown")
        check = r.get("check", "unknown")
        status = r.get("status", "error")
        domain_checks.setdefault(domain, {})[check] = status

    if not domain_checks:
        return _empty_chart(out_dir, "section_heatmap", "No check results found")

    domains = sorted(domain_checks.keys())
    all_checks = sorted(set(c for d in domain_checks.values() for c in d))

    # Build numeric matrix: 1=pass, 0=fail, 0.5=error, -1=N/A
    matrix = np.full((len(domains), len(all_checks)), np.nan)
    for i, d in enumerate(domains):
        for j, c in enumerate(all_checks):
            status = domain_checks[d].get(c, None)
            if status == "pass":
                matrix[i, j] = 1.0
            elif status == "fail":
                matrix[i, j] = 0.0
            elif status == "error":
                matrix[i, j] = 0.5
            elif status == "not_applicable":
                matrix[i, j] = -1.0

    fig, ax = plt.subplots(figsize=(max(12, len(all_checks) * 0.8), max(6, len(domains) * 0.5)))

    cmap = matplotlib.colors.ListedColormap(["#e74c3c", "#f39c12", "#2ecc71"])
    cmap.set_bad(color="#ecf0f1")

    im = ax.imshow(matrix, cmap=cmap, aspect="auto", vmin=0, vmax=1)

    ax.set_xticks(np.arange(len(all_checks)))
    ax.set_xticklabels([c[:20] for c in all_checks], rotation=60, ha="right", fontsize=7)
    ax.set_yticks(np.arange(len(domains)))
    ax.set_yticklabels([d.split("-", 1)[-1] if "-" in d else d for d in domains], fontsize=9)

    # Add text annotations
    for i in range(len(domains)):
        for j in range(len(all_checks)):
            val = matrix[i, j]
            if np.isnan(val):
                continue
            text = "OK" if val == 1.0 else ("FAIL" if val == 0.0 else ("!" if val == 0.5 else "-"))
            ax.text(j, i, text, ha="center", va="center", fontsize=8,
                    color="white" if val != 0.5 else "black", fontweight="bold")

    legend_elements = [
        mpatches.Patch(facecolor="#2ecc71", label="Pass"),
        mpatches.Patch(facecolor="#f39c12", label="Error"),
        mpatches.Patch(facecolor="#e74c3c", label="Fail"),
        mpatches.Patch(facecolor="#ecf0f1", label="N/A"),
    ]
    ax.legend(handles=legend_elements, loc="upper right", fontsize=8)
    ax.set_title("Check Results Heatmap (Domain × Check)", fontsize=13, fontweight="bold")
    fig.tight_layout()

    out_path = out_dir / "section_heatmap.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def chart_tier_progression(
    all_domain_scores: dict[str, dict[str, Any]],
    out_dir: Path,
) -> Path:
    """Line chart: score progression by tier (domains ordered by tier)."""
    tier_map = {}
    for tier_info in _load_tiers().get("tiers", []):
        for d in tier_info["domains"]:
            tier_map[d] = tier_info["tier"]

    if not tier_map or not all_domain_scores:
        return _empty_chart(out_dir, "tier_progression", "No tier/score data available")

    # Group by tier
    tier_scores: dict[int, list[float]] = {}
    for domain, score_data in all_domain_scores.items():
        tier = tier_map.get(domain, 99)
        score = score_data.get("final_score", {}).get("score", 0)
        tier_scores.setdefault(tier, []).append(score)

    if not tier_scores:
        return _empty_chart(out_dir, "tier_progression", "No tier-score mapping found")

    tiers = sorted(tier_scores.keys())
    avg_scores = [np.mean(tier_scores[t]) for t in tiers]
    min_scores = [min(tier_scores[t]) for t in tiers]
    max_scores = [max(tier_scores[t]) for t in tiers]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(tiers, avg_scores, "o-", linewidth=2, markersize=8, color="#3498db", label="Average")
    ax.fill_between(tiers, min_scores, max_scores, alpha=0.2, color="#3498db", label="Min–Max range")
    ax.axhline(y=70, color="#e67e22", linestyle="--", alpha=0.5, label="Acceptable (70)")

    for t, avg, mn, mx in zip(tiers, avg_scores, min_scores, max_scores):
        ax.annotate(f"{avg:.0f}", xy=(t, avg), fontsize=9, ha="center", va="bottom",
                    fontweight="bold")

    ax.set_xlabel("Tier", fontsize=11)
    ax.set_ylabel("Score", fontsize=11)
    ax.set_title("Score Progression by Tier", fontsize=14, fontweight="bold")
    ax.set_xticks(tiers)
    ax.set_xticklabels([f"Tier {t}" for t in tiers])
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()

    out_path = out_dir / "tier_progression.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def _load_tiers() -> dict:
    """Load tiers.yaml from the base_dev system."""
    tiers_path = Path(__file__).parent.parent / "plan" / "core" / "tiers.yaml"
    if tiers_path.exists():
        return load_yaml(tiers_path)
    return {"tiers": []}


def _empty_chart(out_dir: Path, name: str, message: str) -> Path:
    """Generate a placeholder chart with a message."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=14,
            color="#7f8c8d", style="italic", transform=ax.transAxes)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title(name.replace("_", " ").title(), fontsize=13, fontweight="bold")
    fig.tight_layout()

    out_path = out_dir / f"{name}.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def generate_all_charts(
    system_root: Path,
    results_dir: Path,
    out_dir: Path,
    scores_json: Path | None = None,
) -> list[Path]:
    """Generate all visualization charts. Returns list of output PNG paths."""
    out_dir.mkdir(parents=True, exist_ok=True)
    charts: list[Path] = []

    print("Loading data...")
    check_results = load_check_results(results_dir)
    det_rules = load_deterministic_rules(system_root)
    sem_criteria = load_semantic_criteria(system_root)

    scores = {}
    if scores_json and scores_json.exists():
        scores = load_scores_json(scores_json)

    # Also try to load per-domain scores from results.json
    results_json = results_dir / "results.json"
    all_domain_scores = {}
    if results_json.exists():
        results_data = json.loads(results_json.read_text(encoding="utf-8"))
        for tier_key, tier_data in results_data.get("tiers", {}).items():
            for domain, domain_score in tier_data.get("results", {}).items():
                if isinstance(domain_score, dict):
                    normalized = {
                        "final_score": {"score": domain_score.get("score", 0)},
                        "score_bands": {"rating": domain_score.get("rating", "N/A")},
                    }
                    all_domain_scores[domain] = normalized

    print(f"  Check results: {len(check_results)}")
    print(f"  Deterministic rules: {sum(len(v) for v in det_rules.values())}")
    print(f"  Semantic criteria: {sum(len(v) for v in sem_criteria.values())}")
    print(f"  Domain scores: {len(all_domain_scores)}")
    print()

    # Generate charts
    print("Generating charts...")
    charts.append(chart_check_results_by_domain(check_results, out_dir))
    print(f"  [OK] {charts[-1].name}")

    charts.append(chart_category_breakdown(check_results, out_dir))
    print(f"  [OK] {charts[-1].name}")

    charts.append(chart_rule_weights_heatmap(det_rules, out_dir))
    print(f"  [OK] {charts[-1].name}")

    charts.append(chart_scoring_radar(scores, out_dir))
    print(f"  [OK] {charts[-1].name}")

    charts.append(chart_score_bands(all_domain_scores, out_dir))
    print(f"  [OK] {charts[-1].name}")

    charts.append(chart_domain_scores_bar(all_domain_scores, out_dir))
    print(f"  [OK] {charts[-1].name}")

    charts.append(chart_section_pass_rate_heatmap(check_results, out_dir))
    print(f"  [OK] {charts[-1].name}")

    charts.append(chart_tier_progression(all_domain_scores, out_dir))
    print(f"  [OK] {charts[-1].name}")

    print(f"\n{len(charts)} charts written to {out_dir}")
    return charts


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate audit visualization charts")
    parser.add_argument("--system-root", required=True, help="Path to system directory")
    parser.add_argument("--results-dir", required=True, help="Directory with check result JSONs")
    parser.add_argument("--out-dir", required=True, help="Output directory for PNG charts")
    parser.add_argument("--scores-json", help="Path to scores JSON (optional)")
    args = parser.parse_args()

    system_root = Path(args.system_root)
    results_dir = Path(args.results_dir)
    out_dir = Path(args.out_dir)
    scores_json = Path(args.scores_json) if args.scores_json else None

    if not system_root.is_dir():
        print(f"Error: system-root not found: {system_root}", file=sys.stderr)
        sys.exit(1)

    generate_all_charts(system_root, results_dir, out_dir, scores_json)


if __name__ == "__main__":
    main()
