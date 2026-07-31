-- One row per (repo_root, standard) classification result.
-- classify-repo writes this; the 2-state classification determines whether
-- the pipeline proceeds or refuses.
--
-- CHECK constraint uses the 2-state model:
--   NO_DOCS  — refuse: repo has no author-supplied documentation
--   HAS_DOCS — proceed: repo has documentation, pipeline runs
--
-- has_implementation is kept as metadata (useful for claim grounding later)
-- but no longer drives classification branching.

CREATE TABLE IF NOT EXISTS academic_repos (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    standard      TEXT    NOT NULL,
    repo_root     TEXT    NOT NULL,
    classification TEXT   NOT NULL CHECK (classification IN (
        'NO_DOCS', 'HAS_DOCS'
    )),
    has_implementation INTEGER NOT NULL DEFAULT 0,
    module_count  INTEGER NOT NULL DEFAULT 0,
    metadata      TEXT    NOT NULL DEFAULT '{}',
    created_at    TEXT    NOT NULL,
    updated_at    TEXT    NOT NULL,
    UNIQUE(standard, repo_root)
);
