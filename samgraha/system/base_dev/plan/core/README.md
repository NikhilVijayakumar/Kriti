# Documentation Plan

Orchestration layer for tier-by-tier documentation generation, audit, and fix. Ties together the existing layers without adding new judging or producing logic.

## How it works

1. **Two entry paths** — generate from scratch (Path A) or audit existing docs and fix (Path B)
2. **Tier gate** — domains in a tier run in parallel; no tier advances until every domain in it clears the score threshold (the Acceptable band minimum, resolved at runtime from `score_bands`)
3. **Fix loop** — failing sections get regenerated via the `## Audit Fix` slot in generation templates, re-audited, repeated up to 5 times before flagging for human review

## Files

| File | Purpose |
|------|---------|
| `tiers.yaml` | Domain→tier assignments, relationships, relationship type enum. Transcribed from `00-domain-relationships.md`. |
| `loop.yaml` | Per-domain procedure: path selection, scoring, fix loop, tier gate, special cases. |

## Source of truth

`tiers.yaml` is a transcription of `00-domain-relationships.md` (prose for humans, YAML for the engine). If that file changes, this file changes with it — not independently maintained.

## Scoring

Uses the same `calculation/summary/` formulas and bands as every other layer. Tier gate threshold: **the Acceptable band minimum** (resolved at runtime from `score_bands`). No per-bucket sub-gate.

## Iterations

Max 5 per domain. After 5: flag for human review, gate stays hard (domain doesn't clear until human resolves).

## Within-tier ordering

All domains in a tier run in parallel, except: **External Context completes before Engineering** in Tier 2 (External Context informs Engineering — Engineering's generation needs it as input context).
