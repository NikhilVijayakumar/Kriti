# Use-case 4 — Semantic Audit

**Script**: Per-domain triad — `gather-domain-evidence` (mode=`audit`) →
`semantic-audit` (prompt — a single generic prompt shared across all
domains, not a per-domain-named prompt; the domain's specific rubric
comes from `domains/{domain}.md` + `calculation/semantic/document.yaml`
passed as evidence, not from the prompt's registration name) →
`persist-domain-semantic-score`

**Inputs**:
- `domains/{domain}.md` golden-standard rules (this document set — see
  `domains/`)
- `calculation/semantic/document.yaml` rubric shape
- Current draft for the domain (deepened, if usecase 3 has run; generated,
  otherwise)

**Action**: Scores each domain against its golden-standard rules + rubric.
`persist-domain-semantic-score` (via `upsert_semantic_score`) inserts an
append-only row — `run_number` auto-increments per (paper, domain, model),
never overwrites. History is preserved by design (fixes the destroyed-
history bug documented in `base_academic-data-pipeline-proposal.md` §0/§5).

**Completion criteria**:
- Minimum bar (unblocks usecase 5): >= 1 semantic run per structural
  domain
- Full bar (informational, never blocks): every configured model has
  scored every domain

**Verify script**: `verify_usecase_4_semantic_audit.py --standard base_academic --paper-id <id>`
- Reports both tiers
- Exit code reflects minimum bar only

**Rule**: Accumulates indefinitely — no "complete" end-state, same as
`python_hackathon`'s 2b. Each re-run is a new `run_number`, feeding
`academic_score_history`'s trend tracking once `calculate` (usecase 6)
runs against it.
