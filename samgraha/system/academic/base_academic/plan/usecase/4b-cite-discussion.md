# Use-case 4b-discussion — Section Citations — discussion

**Depends on**: `generate-section-draft-discussion` (4a)

**Script**: `gather-domain-evidence` (mode=citation, domain=discussion) -> `persist-section-citations` (source_kind=in-repo) + `literature-review-pass` (prompt, external lit search) -> `persist-section-citations` (source_kind=literature) -> `persist-section-draft` (stage=cite)

**Inputs**: `discussion`'s stage='generate' draft + external literature corpus

**Action**: Extract in-repo grounding markers already present in `discussion`'s draft, persist them as real, queryable citations (previously silently dropped). `discussion` is also a `CITE_CONTEXT_DOMAINS` member — runs an external-literature search pass on top of the in-repo citations.

**Completion criteria** (checked by verify script):
- `SELECT COUNT(*) FROM academic_section_citations WHERE domain_id=(SELECT id FROM academic_domains WHERE key='discussion')` >= 1

**Verify script**: `script/verify/uc4b_cite_discussion.py --paper-id <id>`

**Rule**: Runs after this domain's own 4a. Independent of every other domain's citation usecase.
