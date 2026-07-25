# Documentation Analysis Prompt

Guides the per-team analysis for the Documentation domain — read by
whichever agent runs it via MCP, after scoring has completed. Explains
why a team got their documentation score. Not parsed by a script — this
is a prompt.

## Version
1.0.0

## Analysis Intent
Documentation scores (weight: 5) measure README quality — the primary
communication artifact for hackathon submissions. Though lowest weight,
a missing or broken README is a foundational failure. This step
interprets README analysis results into actionable narrative.

## Inputs
- `standard_domain_scores` DB table — all teams' documentation domain
  scores (queried via MCP)
- Per-team deterministic findings: `README.md` presence, installation
  section with executable code blocks, link resolution (404 checks)
- Semantic findings: README completeness, clarity of problem
  statement, vision description

## Narrative Guidance
The Documentation narrative must cover:
1. **Score Overview** — team's documentation score out of 5, with
   competition average comparison. Note whether this low-weight domain
   still cost them points.
2. **README Presence** — does `README.md` exist at root? This is a
   binary gate — missing README is an immediate failure.
3. **Installation Instructions** — does the README contain a dedicated
   installation/setup section with executable code blocks (bash/sh)?
   Vague instructions like "install dependencies" without code blocks
   score poorly.
4. **Link Integrity** — were internal and external links checked? Any
   404s? Broken links in a README are a concrete, fixable finding.
5. **Semantic Quality** — does the README communicate the problem
   statement and vision clearly? Is the writing quality adequate for
   a hackathon submission?
6. **Strengths** — complete README with clear setup steps, working
   links, good problem statement, usage examples.
7. **Weaknesses** — missing README, no installation section, broken
   links, vague setup instructions, no problem statement.
8. **Recommendations** — "add a 'Getting Started' section with
   `pip install -r requirements.txt` code block", "fix 3 broken
   links to external docs", "add a problem statement paragraph".

## Visualization Guidance
- `domain_scores` — always include.
- `checklist_coverage` — include: presence/installation/links status
  per team.

## Output Schema
```json
{
  "domain": "04-documentation",
  "sections": [
    {"heading": "Score Overview", "text": "..."},
    {"heading": "README Presence", "text": "..."},
    {"heading": "Installation Instructions", "text": "..."},
    {"heading": "Link Integrity", "text": "..."},
    {"heading": "Semantic Quality", "text": "..."},
    {"heading": "Strengths", "text": "..."},
    {"heading": "Weaknesses", "text": "..."},
    {"heading": "Recommendations", "text": "..."}
  ]
}
```
