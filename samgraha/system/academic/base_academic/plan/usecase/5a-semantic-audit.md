# Use-case 4 — Semantic Audit

**Script**: Per-domain triad — `gather-domain-evidence` (mode=`audit`) →
`semantic-audit` (prompt) → `persist-domain-semantic-score`

**Inputs**:
- `domains/{domain}.md` golden-standard rules
- `calculation/semantic/document.yaml` rubric shape
- Current draft for the domain (from assemble-paper-structure)

**Action**: Scores each domain against its golden-standard rules + rubric.
`persist-domain-semantic-score` inserts an append-only row with
auto-incrementing `run_number`.

**Completion criteria**:
- Minimum bar: >= 1 semantic run per structural domain
- Full bar: every configured model has scored every domain

**Rule**: Runs after deterministic-audit. Only runs for domains that
passed deterministic audit (deterministic FAIL short-circuits semantic —
§2.5 of proposal). Accumulates indefinitely.
