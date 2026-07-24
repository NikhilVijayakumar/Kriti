# Use-case 00 — Schema Init

**Depends on**: nothing (first usecase in pipeline)

**Script**: `init-schema` — runs `init_schema.py`

**Inputs**:
- `schema/*.sql` files (20 academic_* tables)
- Concrete system's domain list (from payload)
- `templates/` directory tree (seeded into `academic_templates`)

**Action**: Create base_academic's own tables in `knowledge.db` if they don't
exist, seed domains from the concrete system's payload, and scan `prompt/`
and `templates/` to populate the `academic_templates` catalog.

**Completion criteria** (checked by verify script):
- All 20 `academic_*` tables exist in `sqlite_master`
- `academic_domains` has rows (0 in base_academic, N in concrete systems)
- `academic_templates` has rows (scanned from disk)

**Verify script**: `script/verify/uc0_schema_init.py`

**Rule**: Idempotent — safe to run more than once. `CREATE TABLE IF NOT EXISTS`
for every table, `INSERT ... ON CONFLICT` for seeds.
