# Use-case 5d — Cross-Section Semantic Audit

**Depends on**: `deterministic-audit` + `semantic-audit` (every structural
domain PASS — this is a review of already-individually-passing sections
for consistency, not a substitute for per-section scoring)

**Script**: `gather-cross-section-evidence` (det) → `cross-section-semantic-audit`
(prompt) → `persist-domain-semantic-score` (extended, `scope='cross-section'`,
`domain_id=NULL`)

**Inputs**:
- Every structural domain's latest `academic_narratives` draft, concatenated
  in `_master-schema.yaml` order
- New rubric: `calculation/semantic/cross-section.yaml` — terminology
  consistency, claim-vs-evidence alignment across sections, narrative-arc
  coherence

**Action**: Score the *set* of sections together for consistency issues no
single-domain audit can see — each domain already passed its own rubric;
this catches contradictions between domains.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE paper_id=? AND scope='cross-section'` >= 1

**Verify script**: `script/verify/uc5d_cross_section_audit.py --paper-id <id>`

**Rule**: Runs once all domains individually PASS. Re-runs on any domain's
content changing (a targeted rewrite or humanize pass invalidates the last
cross-section run — re-run before proceeding to 5e).
