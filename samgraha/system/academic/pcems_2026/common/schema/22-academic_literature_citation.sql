CREATE TABLE IF NOT EXISTS academic_literature_citation (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id    INTEGER NOT NULL REFERENCES academic_papers(id) ON DELETE CASCADE,
    cite_key    TEXT    NOT NULL,          -- short handle, e.g. "drain2017"
    number      INTEGER,                   -- rendered [N] — assigned at collation, stable per cite_key
    authors     TEXT    NOT NULL,
    year        TEXT,
    title       TEXT    NOT NULL,
    venue       TEXT,
    volume      TEXT,
    issue       TEXT,
    pages       TEXT,
    doi         TEXT,
    raw_markdown TEXT   NOT NULL,           -- full "**[N]** Author..." line, source of truth for rendering
    created_at  TEXT    NOT NULL,
    UNIQUE(paper_id, cite_key)
);
