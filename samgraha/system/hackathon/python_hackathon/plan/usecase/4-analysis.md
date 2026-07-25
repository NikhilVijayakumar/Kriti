# Use-case 4 — Analysis

**Script**: Agent-driven (writes `standard_narratives` rows)

**Inputs**:
- Use-case 3's output (aggregated scores + z-stats)
- `analysis/{domain}.md` x 10 + `analysis/00-leaderboard.md` rubrics

**Action**: Writes `standard_narratives` rows: per team+domain, plus one competition-wide row (`participant_id=NULL, domain=NULL`).

**Completion criteria**:
- Exactly one `standard_narratives` row for every (team, domain) pair that has any audit data
- Exactly one competition-wide row exists

**Verify script**: `verify_usecase_4_analysis.py --standard python_hackathon`
- Cross-references `standard_domain_scores` against `standard_narratives`
- Lists any combo with data but no narrative
- Checks competition-wide row exists and isn't duplicated
