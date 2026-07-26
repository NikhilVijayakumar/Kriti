# Use-case 5g — Reviewer Simulation

**Depends on**: 5e-cross-section-semantic-audit, 5f-document-semantic-audit

**Script**: (LLM-driven, no deterministic script)

**Prompt**: `prompt/audit/reviewer-simulation.md`

**Inputs**: Full assembled document text (all domain drafts concatenated)

**Action**:
1. Load the assembled document text
2. Present to LLM with the reviewer-simulation prompt
3. LLM produces three independent persona scores (1-10 each)
4. Combine scores: overall_score = sum of 3 scores (range 3-30)
5. Map to decision: 25-30=Accept, 18-24=Minor Revision, 10-17=Major Revision, 3-9=Reject
6. Store results in academic_semantic_runs with domain="reviewer-simulation"

**Completion criteria**:
- `SELECT * FROM academic_semantic_runs WHERE paper_id=<id> AND domain_id=(SELECT id FROM academic_domains WHERE key='reviewer-simulation')` returns a row
- The row's `scores` JSON contains `reviewers` array with 3 entries and `decision` field

**Verify script**: `script/verify/uc5g_reviewer_simulation.py --paper-id <id>`
