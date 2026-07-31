-- Lookup table replacing the hardcoded CHECK constraints that used to
-- live on academic_module_analysis/academic_cross_module_analysis.
-- Adding a new analysis kind is now an INSERT here, not a schema edit —
-- the exact bug class that caused figures/tables to be missing from
-- both CHECK constraints after Proposal 15 added them.
-- scope documents which table(s) a kind is valid for; not enforced by
-- a second constraint (would reintroduce the same rigidity problem at
-- one level down) — scripts are trusted to insert valid combinations,
-- same trust boundary the rest of this system already relies on.

CREATE TABLE IF NOT EXISTS analysis_kind (
    key         TEXT PRIMARY KEY,
    description TEXT NOT NULL DEFAULT '',
    scope       TEXT NOT NULL DEFAULT 'both' CHECK (scope IN ('module', 'cross-module', 'both'))
);

INSERT OR IGNORE INTO analysis_kind (key, description, scope) VALUES
    ('summary', 'Per-module summary', 'module'),
    ('architecture', 'Design patterns, component structure, data flow', 'both'),
    ('mathematics', 'Algorithm identification, complexity, formulas', 'both'),
    ('novelty', 'Falsifiable differentiation claims', 'both'),
    ('gaps', 'Field-level gaps', 'both'),
    ('figures', 'Figure candidates — diagrams, data charts', 'both'),
    ('tables', 'Table candidates — metrics, comparisons', 'both'),
    ('dependencies', 'Coupling graph, stability analysis', 'cross-module'),
    ('interactions', 'Runtime data/control flow', 'cross-module'),
    ('patterns', 'Cross-module shared patterns', 'cross-module'),
    ('consistency_check', 'Docs-first ingestion cross-module consistency review', 'cross-module');
