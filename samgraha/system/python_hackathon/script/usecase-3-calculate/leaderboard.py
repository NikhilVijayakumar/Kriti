"""
leaderboard.py — Phase 3: Weighted Scoring + Final Leaderboard

INPUT:  adjusted_scores.json  (Phase 2 output)
        calculation/weights.yaml

PIPELINE:
  Phase 3 — Weighted Score:
    For each team and domain:
      weighted_contribution = (adjusted_score / 100) * domain_weight
    Sum all weighted contributions -> base_weighted_score (out of 100)

  Final Score:
    final_normalized = round((base_weighted_score / 100) * FINAL_SCALE, 2)

OUTPUT: leaderboard.json + leaderboard.md
"""
import json
import yaml
import argparse
import os
from datetime import datetime

WEIGHTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "..", "calculation", "weights.yaml"
)

DOMAIN_KEY_MAP = {
    "01-infrastructure": "infrastructure",
    "02-engineering": "engineering",
    "03-testing": "testing",
    "04-documentation": "documentation",
    "05-security": "security",
    "06-mlops": "mlops",
    "07-runtime": "runtime",
    "08-team-workflow": "team_workflow",
    "09-data-quality": "data_quality",
    "10-ai-explanations": "ai_explanations",
}

DOMAIN_SHORT = {
    "01-infrastructure": "Infra",
    "02-engineering": "Eng",
    "03-testing": "Test",
    "04-documentation": "Docs",
    "05-security": "Sec",
    "06-mlops": "MLOps",
    "07-runtime": "Runtime",
    "08-team-workflow": "TeamWF",
    "09-data-quality": "DataQ",
    "10-ai-explanations": "AI-Expl",
}


def _load_weights(weights_file):
    with open(weights_file, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    # Normalize domain keys to underscores — Mustache templates use underscores,
    # weights.yaml uses hyphens. Normalize once at load time so consumers see one convention.
    cfg["domains"] = {k.replace("-", "_"): v for k, v in cfg["domains"].items()}
    return cfg


def build_leaderboard(adjusted_scores, weights_cfg):
    domain_weights = weights_cfg["domains"]
    total_weight = sum(d["weight"] for d in domain_weights.values())
    final_scale = weights_cfg["final_scale"]

    results = []
    for team in sorted(adjusted_scores.keys()):
        team_adj = adjusted_scores[team]

        # Phase 3: Weighted score
        weighted_total = 0.0
        domain_details = {}
        for domain, weight_key in DOMAIN_KEY_MAP.items():
            weight = domain_weights.get(weight_key, {}).get("weight", 0)
            adj_score = team_adj.get(domain, {}).get("adjusted_score", 0.0)
            contribution = round((adj_score / 100.0) * weight, 3)
            weighted_total += contribution
            domain_details[domain] = {
                "adjusted_score": adj_score,
                "weight": weight,
                "weighted_contribution": contribution,
                "z_score": team_adj.get(domain, {}).get("z_score", 0.0),
                "bonus_applied": team_adj.get(domain, {}).get("bonus_applied", 0.0),
            }

        # Final score: scaled weighted sum, no second bonus stage
        final_normalized = round((weighted_total / total_weight) * final_scale, 2)

        results.append({
            "team": team,
            "base_weighted_score": round(weighted_total, 2),
            "final_score": final_normalized,
            "domain_details": domain_details,
        })

    # Sort by final score descending
    results.sort(key=lambda x: x["final_score"], reverse=True)
    for i, r in enumerate(results):
        r["rank"] = i + 1

    return results


def render_leaderboard_md(results, weights_cfg):
    """Renders the leaderboard as a Markdown report."""
    scale = weights_cfg["final_scale"]
    domain_weights = weights_cfg["domains"]
    total_weight = sum(d["weight"] for d in domain_weights.values())
    now = datetime.now().strftime("%Y-%m-%d %H:%M UTC")

    header_cols = " | ".join(DOMAIN_SHORT.values())
    sep_cols = " | ".join(["---"] * len(DOMAIN_SHORT))

    lines = [
        f"# Hackathon Global Leaderboard",
        f"",
        f"**Generated:** {now}  ",
        f"**Total Teams:** {len(results)}  ",
        f"**Scoring Scale:** {scale} points  ",
        f"",
        f"---",
        f"",
        f"## Final Rankings",
        f"",
        f"| Rank | Team | Final Score | {header_cols} |",
        f"|------|------|-------------|{sep_cols}|",
    ]

    for r in results:
        domain_cols = []
        for domain in DOMAIN_KEY_MAP.keys():
            adj = r["domain_details"].get(domain, {}).get("adjusted_score", 0)
            domain_cols.append(f"{adj:.1f}")
        cols = " | ".join(domain_cols)
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(r["rank"], "")
        lines.append(
            f"| {medal} **{r['rank']}** | `{r['team']}` | **{r['final_score']}/{scale}** | {cols} |"
        )

    lines += [
        f"",
        f"---",
        f"",
        f"## Domain Weights",
        f"",
        f"| Domain | Weight |",
        f"|--------|--------|",
    ]
    for domain, weight_key in DOMAIN_KEY_MAP.items():
        w = weights_cfg["domains"].get(weight_key, {}).get("weight", 0)
        lines.append(f"| {DOMAIN_SHORT[domain]} | {w}/100 |")

    lines += [
        f"",
        f"## Scoring Notes",
        f"",
        f"- **Base Score**: Weighted sum of adjusted domain scores (max {total_weight} pts)",
        f"- **Z-Score Bonus**: Per-domain robust Z-score via MAD, soft-bounded by tanh (max ±10 pts per domain)",
        f"- **Final Scale**: Normalized to {scale} points",
    ]

    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Phase 3: Build the final weighted leaderboard"
    )
    parser.add_argument("--adjusted", required=True, help="Path to adjusted_scores.json")
    parser.add_argument("--weights", default=WEIGHTS_FILE, help="Path to weights.yaml")
    parser.add_argument("--json-out", default="leaderboard.json")
    parser.add_argument("--md-out", default="leaderboard.md")
    args = parser.parse_args()

    with open(args.adjusted, "r", encoding="utf-8") as f:
        adjusted = json.load(f)
    weights_cfg = _load_weights(args.weights)

    print(f"Building leaderboard for {len(adjusted)} teams ...")
    results = build_leaderboard(adjusted, weights_cfg)

    with open(args.json_out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    md = render_leaderboard_md(results, weights_cfg)
    with open(args.md_out, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"\n{'='*50}")
    print(f"{'RANK':<6} {'TEAM':<30} {'SCORE':>6}")
    print(f"{'='*50}")
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    for r in results:
        m = medals.get(r["rank"], "  ")
        print(f"{m} {r['rank']:<4} {r['team']:<30} {r['final_score']:>6}/{weights_cfg['final_scale']}")
    print(f"{'='*50}")
    print(f"\nJSON   -> {args.json_out}")
    print(f"Report -> {args.md_out}")
