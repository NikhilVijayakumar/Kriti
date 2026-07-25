-- knowledge.db — one row per (narrative, heading/text) section. Normalizes
-- the `sections` list every analysis/*.md's own "## Output Schema" declares
-- ([{"heading": ..., "text": ...}, ...]) instead of storing it as one JSON
-- blob column — lets a report template pull a single section (e.g. just
-- "Strengths") without re-parsing the whole narrative, and lets the
-- narrative be regenerated/backtraced section by section if needed.

CREATE TABLE IF NOT EXISTS hackathon_narrative_sections (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    narrative_id  INTEGER NOT NULL REFERENCES hackathon_narratives(id) ON DELETE CASCADE,
    heading       TEXT    NOT NULL,
    text          TEXT    NOT NULL,
    sort_order    INTEGER NOT NULL DEFAULT 0
);
