# Use-case 4b-conclusion — Cite References — conclusion

**Depends on**: `4a-generate-conclusion`

**Script**: `gather-domain-evidence` (mode=cite, domain=conclusion) -> `enrich-with-citations` -> `persist-section-draft` (stage=cite)

**Inputs**: conclusion's stage='generate' draft, reference database

**Action**: Add citations if referencing prior work in future work directions. Verify no new citations introduced that aren't in references section.

**Completion criteria**:
- `SELECT COUNT(*) FROM academic_narratives WHERE domain_id=(SELECT id FROM academic_domains WHERE key='conclusion') AND stage='cite'` >= 1

**Verify script**: `script/verify/uc4b_cite_conclusion.py --paper-id <id>`

**Rule**: Re-runnable. Does not modify other domains.
