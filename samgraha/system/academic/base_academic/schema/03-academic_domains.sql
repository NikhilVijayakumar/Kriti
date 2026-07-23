-- Lookup: scoring domains for the concrete system.
-- Seeded by init-schema from the concrete system's payload["domains"].
-- base_academic has domains:[] (abstract); concrete systems override.
-- weight is used by final_score calculation when domains have unequal
-- importance (most academic systems weight equally).

CREATE TABLE IF NOT EXISTS academic_domains (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    key           TEXT    NOT NULL UNIQUE,
    display_name  TEXT    NOT NULL,
    sort_order    INTEGER NOT NULL,
    weight        REAL    NOT NULL DEFAULT 0
);
