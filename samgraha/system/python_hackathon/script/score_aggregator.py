"""
score_aggregator.py — Phase 1: Raw Domain Score Aggregation

INPUT: A directory of per-team, per-model, per-domain JSON result files.
       Expected structure:
         results/
           team_alpha/
             01-infrastructure/
               gemini-1.5-pro.json
               claude-3-5-sonnet.json
               gpt-4o.json
             02-engineering/
               gemini-1.5-pro.json
               ...
           team_beta/
             ...

OUTPUT: aggregated_scores.json — per team, per domain: raw mean score
        (mean of deterministic score across models for semantic,
         deterministic score is model-independent and taken directly.)

Schema of each model JSON file:
  {
    "deterministic": { "score": 82.5 },
    "semantic":      { "score": 78.0, "model": "gemini-1.5-pro" }
  }
"""
import os
import json
import math
import argparse
import yaml


def _mean(values):
    return sum(values) / len(values) if values else 0

WEIGHTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "calculation", "weights.yaml"
)

DOMAINS = [
    "01-infrastructure",
    "02-engineering",
    "03-testing",
    "04-documentation",
    "05-security",
    "06-mlops",
    "07-runtime",
    "08-team-workflow",
    "09-data-quality",
    "10-ai-explanations",
]


def _load_weights(weights_file=WEIGHTS_FILE):
    """Load weights.yaml and normalize domain keys to underscores."""
    with open(weights_file, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    cfg["domains"] = {k.replace("-", "_"): v for k, v in cfg["domains"].items()}
    return cfg


def _get_domain_weights(weights_cfg, domain):
    """Get (det_weight, sem_weight) for a domain from the aggregation YAML."""
    agg_dir = os.path.join(
        os.path.dirname(__file__), "..", "calculation", "aggregation", "domain"
    )
    # Map domain dir name (01-infrastructure) to agg yaml filename
    agg_file = os.path.join(agg_dir, f"{domain}.yaml")
    if os.path.isfile(agg_file):
        with open(agg_file, "r", encoding="utf-8") as f:
            agg = yaml.safe_load(f)
        weights = agg.get("weights", {})
        return weights.get("deterministic", 0.60), weights.get("semantic", 0.40)
    return 0.60, 0.40  # fallback


def aggregate_team(team_path, weights_cfg):
    """
    For one team directory, compute raw domain scores:
      - Deterministic score is model-independent (taken once per domain)
      - Semantic scores are averaged across all models that evaluated that domain
      - Domain raw score = 0.60 * det + 0.40 * mean(sem scores)
    """
    domain_results = {}
    for domain in DOMAINS:
        domain_path = os.path.join(team_path, domain)
        if not os.path.isdir(domain_path):
            domain_results[domain] = {"error": "domain directory missing", "raw_score": 0.0}
            continue

        det_score = None
        sem_scores = []
        model_breakdown = {}

        for fname in os.listdir(domain_path):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(domain_path, fname)
            model_name = fname.replace(".json", "")
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (json.JSONDecodeError, OSError):
                continue

            # Deterministic is the same regardless of model — take the first one found
            if det_score is None and "deterministic" in data:
                det_score = float(data["deterministic"].get("score", 0))

            if "semantic" in data:
                sem = float(data["semantic"].get("score", 0))
                sem_scores.append(sem)
                model_breakdown[model_name] = sem

        det_score = det_score if det_score is not None else 0.0
        sem_mean = _mean(sem_scores) if sem_scores else 0.0
        det_w, sem_w = _get_domain_weights(weights_cfg, domain)
        raw_score = round(det_w * det_score + sem_w * sem_mean, 2)

        domain_results[domain] = {
            "deterministic_score": det_score,
            "semantic_mean": round(sem_mean, 2),
            "model_breakdown": model_breakdown,
            "raw_score": raw_score,
        }

    return domain_results


def aggregate_all_teams(results_dir, weights_cfg):
    """
    Iterates over all team subdirectories and aggregates domain scores.
    """
    output = {}
    for team_name in sorted(os.listdir(results_dir)):
        team_path = os.path.join(results_dir, team_name)
        if not os.path.isdir(team_path):
            continue
        output[team_name] = aggregate_team(team_path, weights_cfg)
        print(f"  Aggregated: {team_name}")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Phase 1: Aggregate per-team, per-model domain scores into raw domain means"
    )
    parser.add_argument("--results", required=True, help="Path to results/ directory")
    parser.add_argument("--weights", default=WEIGHTS_FILE, help="Path to weights.yaml")
    parser.add_argument("--output", default="aggregated_scores.json", help="Output JSON file")
    args = parser.parse_args()

    weights_cfg = _load_weights(args.weights)
    print(f"Aggregating scores from {args.results} ...")
    aggregated = aggregate_all_teams(args.results, weights_cfg)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(aggregated, f, indent=2)

    print(f"\nDone. {len(aggregated)} teams written to {args.output}")
