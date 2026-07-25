"""analyze_trend.py — Multi-window trend analysis (§6.5).

Extends the single-step trend that calculate.py already computes (via
phase_calculate in init.py) with two additional comparison windows:
  - vs_last_run:    recomputed here (keeps output self-contained)
  - vs_last_3_runs: compares against the entry 3 runs back
  - vs_baseline:    compares against the first entry in history

Reads the existing score_history.json (written by append_score_history
in init.py) — does not write it.

Usage:
  python analyze_trend.py --system-root <path> --domain <domain> \
    --scores <{domain}-scores.json> --history <score_history.json> \
    --out <{domain}-trend.json>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from _common import write_json, utc_now_iso


# ---------------------------------------------------------------------------
# Trend comparison (reuses calculate.py's logic unchanged)
# ---------------------------------------------------------------------------

def trend_comparison(
    current: float,
    previous: float | None,
    tolerance: float = 0.1,
) -> dict[str, Any]:
    """trend_v1 — direction from current vs previous with tolerance.

    Identical logic to calculate.py:trend_comparison(). Duplicated here
    so analyze_trend.py is self-contained (no cross-import at CLI level).
    """
    if previous is None:
        direction = "baseline"
        delta = 0.0
    elif abs(current - previous) <= tolerance:
        direction = "stable"
        delta = round(current - previous, 2)
    elif current > previous:
        direction = "improving"
        delta = round(current - previous, 2)
    else:
        direction = "declining"
        delta = round(current - previous, 2)

    return {
        "current": current,
        "previous": previous,
        "delta": delta,
        "direction": direction,
        "tolerance": tolerance,
    }


# ---------------------------------------------------------------------------
# History loading
# ---------------------------------------------------------------------------

def load_history(history_path: Path, domain: str) -> list[dict[str, Any]]:
    """Load score_history.json and filter to entries for this domain.

    Returns entries in chronological order (oldest first), matching the
    order append_score_history() writes them.
    """
    if not history_path.exists():
        return []

    try:
        raw = json.loads(history_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, KeyError):
        return []

    if not isinstance(raw, list):
        return []

    return [e for e in raw if e.get("domain") == domain]


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def analyze_trend(
    scores: dict[str, Any],
    history: list[dict[str, Any]],
) -> dict[str, Any]:
    """Compute multi-window trend from current scores and domain history.

    Three windows:
      vs_last_run    — current vs most recent prior entry (recomputed)
      vs_last_3_runs — current vs entry 3 runs back (not an average)
      vs_baseline    — current vs first entry in history

    Empty/short history → "baseline" direction (no prior data).
    """
    current_score = scores.get("final_score", {}).get("score", 0.0)
    run_timestamp = utc_now_iso()

    # Filter to entries before this run (history doesn't include the
    # current run yet — append_score_history fires after calculate, and
    # analyze_trend fires after that).
    prior = [e for e in history if e.get("final_score") is not None]

    # vs_last_run: most recent prior entry
    if prior:
        last_run = prior[-1]
        vs_last = trend_comparison(current_score, last_run.get("final_score"))
    else:
        vs_last = trend_comparison(current_score, None)

    # vs_last_3_runs: entry 3 runs back (not an average)
    if len(prior) >= 3:
        target = prior[-3]
        vs_3 = trend_comparison(current_score, target.get("final_score"))
        vs_3["runs_compared"] = 3
    elif prior:
        target = prior[0]
        vs_3 = trend_comparison(current_score, target.get("final_score"))
        vs_3["runs_compared"] = len(prior)
    else:
        vs_3 = trend_comparison(current_score, None)
        vs_3["runs_compared"] = 0

    # vs_baseline: first entry in history
    if prior:
        baseline = prior[0]
        vs_bl = trend_comparison(current_score, baseline.get("final_score"))
        vs_bl["baseline_timestamp"] = baseline.get("timestamp", "unknown")
    else:
        vs_bl = trend_comparison(current_score, None)
        vs_bl["baseline_timestamp"] = None

    return {
        "formula": "trend_v2",
        "domain": scores.get("domain", "unknown"),
        "run_timestamp": run_timestamp,
        "vs_last_run": {
            "delta": vs_last["delta"],
            "direction": vs_last["direction"],
        },
        "vs_last_3_runs": {
            "delta": vs_3["delta"],
            "direction": vs_3["direction"],
            "runs_compared": vs_3["runs_compared"],
        },
        "vs_baseline": {
            "delta": vs_bl["delta"],
            "direction": vs_bl["direction"],
            "baseline_timestamp": vs_bl.get("baseline_timestamp"),
        },
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Multi-window trend analysis for a domain"
    )
    parser.add_argument("--system-root", required=True, help="Path to system directory")
    parser.add_argument("--domain", required=True, help="Domain name (e.g. 01-vision)")
    parser.add_argument("--scores", required=True, help="Path to {domain}-scores.json")
    parser.add_argument("--history", required=True, help="Path to score_history.json")
    parser.add_argument("--out", required=True, help="Output path for {domain}-trend.json")
    args = parser.parse_args()

    scores_path = Path(args.scores)
    history_path = Path(args.history)

    if not scores_path.exists():
        print(f"Error: scores file not found: {scores_path}", file=sys.stderr)
        sys.exit(1)

    scores = json.loads(scores_path.read_text(encoding="utf-8"))
    history = load_history(history_path, args.domain)
    result = analyze_trend(scores, history)

    out_path = Path(args.out)
    write_json(out_path, result)

    # Summary
    domain = result["domain"]
    vs_last = result["vs_last_run"]
    vs_3 = result["vs_last_3_runs"]
    vs_bl = result["vs_baseline"]
    print(f"{domain}: trend_v2")
    print(f"  vs last run:    {vs_last['delta']:+.1f} ({vs_last['direction']})")
    runs = vs_3.get("runs_compared", 0)
    print(f"  vs last {runs} run(s): {vs_3['delta']:+.1f} ({vs_3['direction']})")
    bl_ts = vs_bl.get("baseline_timestamp")
    label = bl_ts if bl_ts else "N/A"
    print(f"  vs baseline:    {vs_bl['delta']:+.1f} ({vs_bl['direction']}) [since {label}]")

    # Sanity check: trend directions should be consistent or explainable
    directions = {vs_last["direction"], vs_3["direction"], vs_bl["direction"]}
    if "declining" in directions and "improving" in directions:
        print("  NOTE: mixed trend directions — short-term decline amid long-term improvement (or vice versa)")


if __name__ == "__main__":
    main()
