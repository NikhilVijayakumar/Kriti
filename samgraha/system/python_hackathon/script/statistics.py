"""
statistics.py — Phase 2: Z-Score & Statistical Adjustment

INPUT:  aggregated_scores.json (output of score_aggregator.py)
        calculation/weights.yaml

OUTPUT: adjusted_scores.json — per team, per domain: bonus/penalty applied score
        domain_stats.json     — global mean and std dev per domain

Algorithm:
  For each domain independently:
    1. Collect raw_scores across all teams
    2. Compute population mean and std dev (MAD-based robust z-score for small N)
    3. Compute z-score for each team
    4. Apply sigmoid-bounded bonus: bonus = MAX_BONUS * tanh(z * 0.5)
       - z = +2 => ~+4.9 points bonus on domain
       - z = -2 => ~-4.9 points penalty
       - Soft bounded to prevent outlier dominance
    5. domain_adjusted_score = raw_score + bonus (capped 0-100)
"""
import json
import statistics
import math
import argparse
import os

MAX_DOMAIN_BONUS = 10.0   # Max bonus/penalty per domain in raw points


def _robust_z(value, median_val, mad):
    """MAD-based robust Z-score (Hampel identifier). Falls back to 0 if MAD=0."""
    if mad == 0:
        return 0.0
    return 0.6745 * (value - median_val) / mad


def _sigmoid_bonus(z_score, max_bonus=MAX_DOMAIN_BONUS):
    """Soft-bounded bonus using tanh. Prevents extreme outliers dominating."""
    return round(max_bonus * math.tanh(z_score * 0.5), 3)


def calculate_domain_stats(aggregated_scores, domain):
    """Returns median, MAD, and per-team z-scores for one domain."""
    team_scores = {}
    for team, domains in aggregated_scores.items():
        if domain in domains and "raw_score" in domains[domain]:
            team_scores[team] = domains[domain]["raw_score"]

    if not team_scores:
        return {}, {}

    values = list(team_scores.values())
    median_val = statistics.median(values)
    mad = statistics.median([abs(v - median_val) for v in values])

    stats = {
        "global_median": median_val,
        "global_mad": mad,
        "global_mean": statistics.mean(values),
        "global_stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
        "team_count": len(values),
    }

    per_team = {}
    for team, score in team_scores.items():
        z = _robust_z(score, median_val, mad)
        bonus = _sigmoid_bonus(z)
        adjusted = min(100.0, max(0.0, round(score + bonus, 2)))
        per_team[team] = {
            "raw_score": score,
            "z_score": round(z, 4),
            "bonus_applied": bonus,
            "adjusted_score": adjusted,
        }

    return stats, per_team


def run_z_adjustment(aggregated_scores):
    """
    Runs Phase 2 for all domains. Returns domain_stats and adjusted_scores.
    """
    all_domains = set()
    for team_data in aggregated_scores.values():
        all_domains.update(team_data.keys())

    domain_stats = {}
    adjusted_scores = {team: {} for team in aggregated_scores}

    for domain in sorted(all_domains):
        stats, per_team = calculate_domain_stats(aggregated_scores, domain)
        domain_stats[domain] = stats
        for team, data in per_team.items():
            adjusted_scores[team][domain] = data

    return domain_stats, adjusted_scores


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Phase 2: Apply Z-score bonus/penalty to aggregated domain scores"
    )
    parser.add_argument("--aggregated", required=True, help="Path to aggregated_scores.json")
    parser.add_argument("--domain-stats-out", default="domain_stats.json")
    parser.add_argument("--adjusted-out", default="adjusted_scores.json")
    args = parser.parse_args()

    with open(args.aggregated, "r", encoding="utf-8") as f:
        aggregated = json.load(f)

    print(f"Running Z-score adjustment for {len(aggregated)} teams ...")
    domain_stats, adjusted = run_z_adjustment(aggregated)

    with open(args.domain_stats_out, "w", encoding="utf-8") as f:
        json.dump(domain_stats, f, indent=2)
    with open(args.adjusted_out, "w", encoding="utf-8") as f:
        json.dump(adjusted, f, indent=2)

    print(f"Domain statistics -> {args.domain_stats_out}")
    print(f"Adjusted scores   -> {args.adjusted_out}")
