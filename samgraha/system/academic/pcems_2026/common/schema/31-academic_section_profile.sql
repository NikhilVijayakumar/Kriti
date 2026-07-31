CREATE TABLE IF NOT EXISTS academic_section_profile (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id            INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id           INTEGER NOT NULL REFERENCES academic_domains(id),
    word_budget         INTEGER,
    source_analysis     TEXT    NOT NULL DEFAULT '',     -- JSON array of analysis_kind values
    profile_notes       TEXT    NOT NULL DEFAULT '',     -- free-form extraction notes
    created_at          TEXT    NOT NULL,
    updated_at          TEXT    NOT NULL,
    UNIQUE(paper_id, domain_id)
);
