# Tier 2 — Audit (Path B)

**Use case:** Existing repo, existing docs
**Path:** B (audit existing documentation — docs already present)

## Domains

- `security`
- `feature`
- `architecture`
- `design`
- `engineering`
- `external-context`

## Pipeline per Domain

Each domain in this tier follows the Path B pipeline (no scaffold/content phase):

1. **Pre-hook: staleness check** — skip if doc unchanged since last audit
2. **Evaluate rules** (`scripts/evaluate_rules.py`) — evaluate deterministic rules against existing docs
3. **Evaluate semantic** (`scripts/evaluate_semantic.py`) — heuristic semantic criteria evaluation
   - Pre-script: `scripts/gather_semantic_context.py` — gather check metrics as grounding evidence
4. **Validate** (`scripts/validate.py`) — run 18 deterministic check scripts
5. **Calculate** (`scripts/calculate.py`) — compute 4-bucket score from evaluated results
6. **Report** (`scripts/report.py`) — render markdown report
7. **Analyze** (`scripts/analyze.py`) — generate structured fix plan
8. **Visualize** (`scripts/visualize.py`) — generate 8 PNG charts
9. **Report HTML** (`scripts/report_html.py`) — render self-contained HTML report
10. **Fix** (semantic, conditional) — only if score < threshold; modify existing sections

## Upstream Dependencies

- `vision` —derives→ `feature` (tier-gating: strict)
- `philosophy` —derives→ `feature` (tier-gating: strict)
- `vision` —derives→ `security` (tier-gating: strict)
- `philosophy` —derives→ `security` (tier-gating: strict)
- `philosophy` —guides→ `architecture` (tier-gating: strict)
- `philosophy` —guides→ `design` (tier-gating: strict)
- `philosophy` —guides→ `engineering` (tier-gating: strict)
- `security` —guides→ `architecture` (tier-gating: strict)
- `security` —guides→ `engineering` (tier-gating: strict)
- `architecture` —soft_aligns_with→ `engineering` (tier-gating: none)
- `external-context` —informs→ `engineering` (tier-gating: none)

## Tier Gate

All domains in tier 2 must reach `Acceptable` before tier 3 starts.

## Domain-Specific Notes

### security

- Existing doc detected at `docs/security.md` or `security.md`
- Validate runs same checks as Path A but against existing content
- Fix phase modifies existing sections in-place (not full re-generation)

### feature

- Existing doc detected at `docs/feature.md` or `feature.md`
- Validate runs same checks as Path A but against existing content
- Fix phase modifies existing sections in-place (not full re-generation)

### architecture

- Existing doc detected at `docs/architecture.md` or `architecture.md`
- Validate runs same checks as Path A but against existing content
- Fix phase modifies existing sections in-place (not full re-generation)

### design

- Existing doc detected at `docs/design.md` or `design.md`
- Validate runs same checks as Path A but against existing content
- Fix phase modifies existing sections in-place (not full re-generation)

### engineering

- Existing doc detected at `docs/engineering.md` or `engineering.md`
- Validate runs same checks as Path A but against existing content
- Fix phase modifies existing sections in-place (not full re-generation)

### external-context

- Existing doc detected at `docs/external-context.md` or `external-context.md`
- Validate runs same checks as Path A but against existing content
- Fix phase modifies existing sections in-place (not full re-generation)
