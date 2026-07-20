# System Summary Analysis Prompt

Guides the system-scope semantic-analysis step — read by whichever agent
runs it via MCP, on-demand, after per-domain trend analysis has
completed. Produces the always-present Final Summary section in the
HTML report. Not parsed by a script — this is a prompt.

## Version
1.0.0

## Analysis Intent
The Final Summary answers: "across all 16 domains, what's the overall
documentation health, what improved, what declined, and what needs
attention next?" This step reads every domain's `{domain}-scores.json`
and `{domain}-trend.json`, plus the system-level `results.json`, and
writes a narrative that a human can scan in 60 seconds.

## Inputs
- `results.json` — system-level scores per tier
- `score_history.json` — full history for trend direction
- All `{domain}-scores.json` and `{domain}-trend.json` files across
  all tiers (read the latest entry per domain from history)
- `00-summary-narrative.json` — the output of this step

## Narrative Guidance
The Final Summary narrative must cover:
1. **Overall Health** — system-wide score (average or weighted across
   domains), band rating, and whether it's improving/declining vs the
   last run. Lead with the number.
2. **Tier Breakdown** — one line per tier: tier number, domains in that
   tier, aggregate score. Flag any tier where the aggregate dropped.
3. **Biggest Movers** — the 3 domains with the largest score deltas
   (positive or negative) since the last run. Name the domain, the
   delta, and the likely driver (which criterion moved).
4. **Mandatory Failures** — any domain with a mandatory criterion (C1
   or C2) failing. These block the tier gate. List each one.
5. **Recommended Warnings** — count of domains with C3 failures.
   Don't list each one; just the count and whether it's trending up or
   down.
6. **Next Steps** — 2-3 actionable items: which domains to fix first,
   which rubrics to author if missing, which charts to generate.

## Visualization Guidance
From the chart catalog:
- `tier_progression` — always include; this is the only step that
  generates it. Shows score progression across all tiers.
- `domain_scores` — always include; the full-domain bar chart with
  band coloring.
- `check_results` — include if any domain has a failing deterministic
  check. Skip if all checks pass (the chart would be all-green and
  uninformative).

## Fix-Plan Trigger Criteria
This is the system-level summary — it does NOT trigger individual
domain fix plans. The per-domain analysis steps (§5) handle that.
The Final Summary's role is to:
- Highlight which domains have open fix plans (read from
  `{domain}-fix-plan.json` files)
- Recommend priority order for human attention
- Flag domains where mandatory failures are recurring across runs

## Output Schema
```json
{
  "domain": "00-summary",
  "sections": [
    {"heading": "Overall Health", "text": "..."},
    {"heading": "Tier Breakdown", "text": "..."},
    {"heading": "Biggest Movers", "text": "..."},
    {"heading": "Mandatory Failures", "text": "..."},
    {"heading": "Recommended Warnings", "text": "..."},
    {"heading": "Next Steps", "text": "..."}
  ]
}
```
