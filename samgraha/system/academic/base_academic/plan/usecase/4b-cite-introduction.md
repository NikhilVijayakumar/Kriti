# Use-case 4b-introduction — Section Citations — introduction

**Depends on**: `generate-section-draft-introduction` (4a)

**Script**: `gather-domain-evidence` (mode=citation, domain=introduction) -> `persist-section-citations` (source_kind=in-repo) + `literature-review-pass` (prompt, external lit search) -> `persist-section-citations` (source_kind=literature) -> `persist-section-draft` (stage=cite)

**Inputs**: `introduction`'s stage='generate' draft + external literature corpus

**Action**: Extract in-repo grounding markers already present in `introduction`'s draft, persist them as real, queryable citations (previously silently dropped). `introduction` is also a `CITE_CONTEXT_DOMAINS` member — runs an external-literature search pass on top of the in-repo citations.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_section_citations WHERE domain_id=(SELECT id FROM academic_domains WHERE key='introduction')` >= 1

**Verify script**: `script/verify/uc4b_cite_introduction.py --paper-id <id>`

**Rule**: Runs after this domain's own 4a. Independent of every other domain's citation usecase.
