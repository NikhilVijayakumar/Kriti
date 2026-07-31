-- Per (paper, domain): citations attached to a structural domain's draft.
-- source_kind distinguishes in-repo evidence citations from external
-- literature citations.  Built by usecase 4b (section-citations) from
-- generate-section's previously-silently-dropped citations_used output
-- and from literature-review-pass results for CITE_CONTEXT_DOMAINS.

CREATE TABLE IF NOT EXISTS academic_section_citations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id    INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id   INTEGER REFERENCES academic_domains(id) ON DELETE CASCADE,
    source_kind TEXT    NOT NULL CHECK (source_kind IN ('in-repo','literature')),
    citation    TEXT    NOT NULL,
    created_at  TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_academic_section_citations_lookup
    ON academic_section_citations(paper_id, domain_id);
