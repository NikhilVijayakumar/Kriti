# Use-case 5e — Document Semantic Audit

**Depends on**: `cross-section-semantic-audit` (PASS)

**Script**: `gather-document-evidence` (det — concatenates all sections per
`_master-schema.yaml` order) → `document-semantic-audit` (prompt) →
`persist-domain-semantic-score` (extended, `scope='document'`, `domain_id=NULL`)

**Inputs**:
- Full concatenated document text
- New rubric: `calculation/semantic/document-review.yaml` — reads as one
  document: does the introduction's stated gap get closed by the
  conclusion, does methodology actually support the results shown, overall
  readability/flow a per-section score can't capture

**Action**: One holistic pass over the whole assembled document — the
"full document review" step, distinct from both per-section audit (5/5a)
and cross-section consistency (5d).

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_semantic_runs WHERE paper_id=? AND scope='document'` >= 1

**Verify script**: `script/verify/uc5e_document_audit.py --paper-id <id>`

**Rule**: Runs after 5d PASS. Gates `render-paper` — this is the last
check before `assemble-final-document.py`'s scaffolding.
