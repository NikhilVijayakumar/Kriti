# Use-case 4 — Assemble Paper Structure

**Depends on**: `novelty-analysis` + `gap-analysis` + `mathematics-and-diagrams`

**Script**: Per-domain triads — `gather-domain-evidence` → `generate-section`
(prompt) → `persist-section-draft` + conditional `literature-review-pass`
(prompt) for domains in `CITE_CONTEXT_DOMAINS`

**Inputs**:
- Repo documentation, analysis docs, novelty/gap/math findings
- `templates/generation/markdown/{domain}.md` per structural domain

**Action**: Generate every structural domain from documentation, weaving
in novelty/gap/math findings. Conditional literature-review for cite-context
domains (introduction, related-work, discussion).

**Completion criteria** (checked by verify script):
- Every structural domain has >= 1 `academic_narratives` row:
  `SELECT key FROM academic_domains WHERE kind='structural'` — each must
  have `SELECT COUNT(*) FROM academic_narratives WHERE paper_id=? AND domain_key=?` >= 1

**Verify script**: `script/verify/uc4_assemble.py --paper-id <id>`

**Rule**: Runs after novelty + gap + math all have results. Per-domain
triads expanded at runtime by `expand_triads()`.
