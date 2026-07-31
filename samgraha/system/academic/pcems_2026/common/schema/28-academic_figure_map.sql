CREATE TABLE IF NOT EXISTS academic_figure_map (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id        INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    domain_id       INTEGER NOT NULL REFERENCES academic_domains(id),
    map_key         TEXT    NOT NULL,
    number          INTEGER,
    caption         TEXT    NOT NULL,
    figure_type     TEXT,
    target_section  TEXT,
    asset_path          TEXT,
    mermaid_source      TEXT,
    module_id               INTEGER REFERENCES academic_modules(id),
    source_evidence         TEXT    NOT NULL DEFAULT '',
    relevance_note      TEXT    NOT NULL DEFAULT '',
    data_table_map_key  TEXT,
    created_at      TEXT    NOT NULL,
    UNIQUE(paper_id, map_key)
);
