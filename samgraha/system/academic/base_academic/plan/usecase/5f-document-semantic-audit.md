# Use-case 5f — Document Semantic Audit

**Depends on**: `cross-section-semantic-audit` (5e, PASS)

**Script**: `gather-document-evidence` (det — concatenates all sections per
`_master-schema.yaml` order) → deterministic pre-check (total word count
against `calculation/summary/paper-budget.yaml`, written as `scope='document'`,
`domain_id=NULL` row in `academic_deterministic_findings`) →
`document-semantic-audit` (prompt) →
`persist-domain-semantic-score` (extended, `scope='document'`, `domain_id=NULL`)

**Inputs**:
- Full concatenated document text
- Rubric: `calculation/semantic/document-review.yaml` — reads as one
  document: does the introduction's stated gap get closed by the
  conclusion, does methodology actually support the results shown, overall
  readability/flow a per-section score can't capture

**Action**: One holistic pass over the whole assembled document — the
"full document review" step, distinct from both per-section audit (5/5a)
and cross-section consistency (5e).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE paper_id=? AND scope='document'` >= 1
- Total word count deterministic check PASS (scope='document', domain_id=NULL)

**Verify script**: `script/verify/uc5f_document_audit.py --paper-id <id>`

**Rule**: Runs after 5e PASS. Gates `render-paper` — this is the last
check before `assemble-final-document.py`'s scaffolding.
