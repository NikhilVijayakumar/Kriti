CREATE TABLE IF NOT EXISTS academic_table_map (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id        INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id       INTEGER NOT NULL REFERENCES academic_domains(id),
    map_key         TEXT    NOT NULL,
    number          INTEGER,
    caption         TEXT    NOT NULL,
    table_type      TEXT,
    target_section  TEXT,
    columns_json    TEXT    NOT NULL,
    rows_json       TEXT    NOT NULL,
    module_id       INTEGER REFERENCES academic_modules(id),
    source_evidence TEXT    NOT NULL DEFAULT '',
    relevance_note  TEXT    NOT NULL DEFAULT '',
    created_at      TEXT    NOT NULL,
    UNIQUE(paper_id, map_key)
);
