CREATE TABLE IF NOT EXISTS academic_equation_map (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id        INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id       INTEGER NOT NULL REFERENCES academic_domains(id),
    map_key         TEXT    NOT NULL,
    number          INTEGER,
    latex           TEXT    NOT NULL,
    variables_json  TEXT,
    explanation     TEXT    NOT NULL,
    target_section  TEXT,
    module_id       INTEGER REFERENCES academic_modules(id),
    source_evidence TEXT    NOT NULL DEFAULT '',
    relevance_note  TEXT    NOT NULL DEFAULT '',
    created_at      TEXT    NOT NULL,
    UNIQUE(paper_id, map_key)
);
