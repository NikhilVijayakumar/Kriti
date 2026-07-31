CREATE TABLE IF NOT EXISTS academic_keyword_map (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id        INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    module_id       INTEGER NOT NULL REFERENCES academic_modules(id) ON DELETE CASCADE,
    keyword         TEXT    NOT NULL,
    relevance_note  TEXT    NOT NULL DEFAULT '',
    source_evidence TEXT    NOT NULL DEFAULT '',
    created_at      TEXT    NOT NULL,
    UNIQUE(paper_id, module_id, keyword)
);
