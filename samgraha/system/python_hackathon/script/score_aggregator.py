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
import statistics
import argparse

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

DET_WEIGHT = 0.60
SEM_WEIGHT = 0.40


def aggregate_team(team_path):
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
        sem_mean = statistics.mean(sem_scores) if sem_scores else 0.0
        raw_score = round(DET_WEIGHT * det_score + SEM_WEIGHT * sem_mean, 2)

        domain_results[domain] = {
            "deterministic_score": det_score,
            "semantic_mean": round(sem_mean, 2),
            "model_breakdown": model_breakdown,
            "raw_score": raw_score,
        }

    return domain_results


def aggregate_all_teams(results_dir):
    """
    Iterates over all team subdirectories and aggregates domain scores.
    """
    output = {}
    for team_name in sorted(os.listdir(results_dir)):
        team_path = os.path.join(results_dir, team_name)
        if not os.path.isdir(team_path):
            continue
        output[team_name] = aggregate_team(team_path)
        print(f"  Aggregated: {team_name}")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Phase 1: Aggregate per-team, per-model domain scores into raw domain means"
    )
    parser.add_argument("--results", required=True, help="Path to results/ directory")
    parser.add_argument("--output", default="aggregated_scores.json", help="Output JSON file")
    args = parser.parse_args()

    print(f"Aggregating scores from {args.results} ...")
    aggregated = aggregate_all_teams(args.results)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(aggregated, f, indent=2)

    print(f"\nDone. {len(aggregated)} teams written to {args.output}")
