-- Per-narrative {heading, text} sections.
-- persist-section-draft writes one row per heading in the generated output.
-- sort_order preserves the order the semantic step returned.
-- FK to academic_narratives with ON DELETE CASCADE — deleting a narrative
-- deletes its sections.

CREATE TABLE IF NOT EXISTS academic_narrative_sections (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    narrative_id  INTEGER NOT NULL REFERENCES academic_narratives(id) ON DELETE CASCADE,
    heading       TEXT    NOT NULL,
    text          TEXT    NOT NULL,
    sort_order    INTEGER NOT NULL DEFAULT 0
);
