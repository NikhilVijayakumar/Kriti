# rust_dev — Per-Tier Usecase Map: Generator + DB Persistence (Proposal 4 of 7)

## 0. Series

Part of a 7-proposal set — see
[`rust_dev-tier-directory-restructure-proposal.md`](1-rust_dev-tier-directory-restructure-proposal.md) §0.
Depends on proposal 2 (manifest + schema exist) and proposal 3 (real
per-tier usecases with non-empty `steps:` to enumerate — nothing to map
otherwise). Feeds proposal 5: every `propose-tierN-*` usecase's context
step reads this proposal's output as a required input, so a proposal can
never be drafted without its tier's usecase map attached.

**Correction notice**: this proposal's core design (§2's generator
algorithm, §5's "don't regenerate every time" caching principle) is
sound, but its persistence mechanism — a new `dev_tier_usecase_map` table
(§4) — is mostly redundant.
[`6-rust_dev-samgraha-schema-alignment-proposal.md`](6-rust_dev-samgraha-schema-alignment-proposal.md) §2-§3
found that samgraha's real `usecase.data` JSON column (already used in
production for `driver`/`depends_on`) can carry `tier` directly, making
the "usecase map" a query against generic tables rather than a
standard-specific table this proposal generates and persists separately —
**but not via a `standard.yaml`-level `data:` block** (proposal 6 checked
`register_standard.rs`'s actual struct fields directly and found no such
generic pass-through exists). Read §2 for the generator's algorithm —
redirected to live as logic inside `rust_dev`'s own `common/script/seeder.py`
(same file pcems's `seeder.py` already builds its domain-lookup data in),
computing `tier` at seed time and writing it into `usecase.data` itself,
not a script that "patches `standard.yaml`" ahead of some other generic
ingestion step — and §3 for why the caching principle still matters,
applied to a smaller thing.

**Status, checked against the live tree**: §2's standalone generator script
and §4's table/persist-script/usecase are all superseded — nothing in
either section should be built as written. What survives is smaller than
either section: the tier-computation *algorithm* (§2's steps 1-3), moved
into `rust_dev`'s own `common/script/seeder.py`. That file doesn't exist
yet (confirmed — `common/script/` today holds only proposal 1's relocated
`{ubuntu,windows}/_generic/` checks, no `seeder.py`), and per proposal 6
§1's caveat, `rust_dev` only has grounds to declare `seeder_script:` at
all once it has a custom table to seed — that's proposal 7's
`dev_repo_domain_state`, not this proposal's. Writing `seeder.py` now,
ahead of proposal 7, would mean guessing at a shape this proposal has no
basis for. Once `seeder.py` exists, "the usecase map" is just the query in
proposal 6 §3, run live — no generated file, no table, nothing this
proposal produces to hand off. This proposal's remaining content below is
kept as the design record for that future `seeder.py` logic, not as a
build list.

## 1. What "usecase map" means here, grounded in two existing precedents

Two real files already do a version of this, on the Bodha (target-repo)
side, not the standard-definition side:

- `E:\Python\Bodha\.bodha-structure\section\map\section-map.yaml` —
  Bodha's own document structure: a flat `sections:` list, each entry
  `{id, title, parent_id, level, order, required, generated, source,
  profile, purpose}`. This describes *what the finished paper looks like*,
  independent of how any section gets produced.
- `E:\Python\Bodha\.samgraha\pcems_2026\step0-extract\section-map.yaml` —
  same schema (`schema.id: bodha.step0.extraction-map`), but scoped to
  Step 0's extraction taxonomy only (`novelty`, `gaps`, `data`), with a
  header comment documenting a deliberate boundary: *"has no concept of
  manuscript sections... deciding where an extracted item lands... is a
  Step 1 (drafting) decision, not a Step 0 (extraction) one."* — i.e.
  pcems already keeps **one map per pipeline stage**, not one global map,
  precisely because a stage-scoped map stays honest about what that stage
  actually owns.

The user's ask maps directly onto this second pattern, generalized: one
usecase map **per tier**, generated (not hand-authored) from `standard.yaml`'s
`usecases:` block (proposal 3) + `plan/core/tiers.yaml`'s domain→tier
partition, saved under `rust_dev/plan/usecase-map/tierN.yaml`, and — the
part neither Bodha file does — also persisted to the samgraha DB so a
proposal-drafting script can read it with one query instead of re-deriving
it from `standard.yaml` every run.

## 2. Generator script — modeled on `generate_per_domain_usecases.py`

pcems's existing generator (`common/schema-manifest/generate_per_domain_usecases.py`)
is the closest real precedent: reads a fixed domain list, emits one file
per (prefix, domain) pair, explicit "do not hand-edit, edit the generator
and re-run" contract in every generated file's docstring. Same shape here,
different grouping key (tier instead of domain-prefix):

```
common/schema-manifest/generate_tier_usecase_map.py
```

```python
"""generate_tier_usecase_map.py — rust_dev's per-tier usecase-map
generator. Reads standard.yaml's usecases: block + plan/core/tiers.yaml's
domain->tier partition, emits plan/usecase-map/tier{N}.yaml.

Does not persist to DB directly — persist_usecase_map.py (a samgraha
deterministic step, see §4) reads this script's output and writes it via
the standard --in/write_envelope() contract, so the map generation logic
itself has no DB dependency and can run standalone for a dry-run diff.

Regenerate whenever standard.yaml's usecases: block changes. Content-hash
the block (see §5) so re-runs are no-ops when nothing changed — the user's
explicit requirement: "do not want to create it every time."
"""
```

Algorithm:
1. Load `standard.yaml`'s `usecases:` list.
2. Load `plan/core/tiers.yaml`'s `tiers:` list — build `domain -> tier`.
3. For each usecase, extract its domain from the name (usecase names carry
   the domain as a suffix, e.g. `deterministic-audit-{domain}` per
   proposal 3 §3 — same convention pcems already uses,
   e.g. `deterministic-audit-title-and-metadata` in the real `standard.yaml`).
   Usecases with no domain suffix (`calculate`, per proposal 3 §3) are
   cross-tier — excluded from every per-tier map, listed once in a
   `plan/usecase-map/_cross-tier.yaml` instead.
4. Group by tier, emit `plan/usecase-map/tier{N}.yaml`:

```yaml
schema:
  id: rust_dev.tier.usecase-map
  name: Tier Usecase Map Schema
  version: 1.0.0
  generated_by: common/schema-manifest/generate_tier_usecase_map.py
  generated_from_hash: "{sha256 of standard.yaml's usecases: block}"

tier: 2
domains: [security, feature, architecture, engineering, external-context]

usecases:
  - id: generate-document-security
    domain: security
    kind: mixed           # has both deterministic and semantic steps
    step_count: 2
    steps:
      - order: 1
        kind: deterministic
        script: gather-tier-context
      - order: 2
        kind: semantic
        prompt: generate-security
  - id: deterministic-audit-security
    domain: security
    kind: deterministic
    step_count: 3
    steps: [...]
  # ... one entry per usecase belonging to this tier's domains
```

## 3. Why per-tier, not one global map

Directly answers the user's framing ("each step can have its own usecase
map"): a global map would force every propose call to filter it down to
"usecases relevant to this tier" at read time — the exact anti-pattern
pcems's Step 0 `section-map.yaml` header comment (§1) already documents
avoiding. Scoping the map at generation time instead of filtering it at
read time means proposal 5's context-gathering step is a single indexed
DB query (`WHERE tier = ?`), not a filter-then-scan.

## 4. DB persistence — new table + step (dropped — see status note in §0)

Kept verbatim as the original design record; proposal 6 §3 found the table
below redundant with `usecase.data.tier` (§2's algorithm, relocated) plus a
plain SQL query. Do not build `dev_tier_usecase_map`, `persist_usecase_map.py`,
or the `generate-usecase-map` usecase below.

Proposal 2 §6 leaves the `dev_*` table prefix and tier-as-first-class-row
question open; this proposal assumes that decision resolves to tiers being
queryable (either `dev_tiers` as its own table or a `tier_number` column on
`dev_domains` — either way, a `tier_number` value must exist to key off).
New table:

```sql
CREATE TABLE dev_tier_usecase_map (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    tier_number         INTEGER NOT NULL,
    usecase_name        TEXT    NOT NULL,
    domain_key          TEXT    NOT NULL,
    kind                TEXT    NOT NULL CHECK (kind IN ('deterministic','semantic','mixed')),
    step_count          INTEGER NOT NULL,
    deterministic_steps INTEGER NOT NULL,
    semantic_steps      INTEGER NOT NULL,
    source_hash         TEXT    NOT NULL,  -- generated_from_hash, §2 step 4 — cache key
    generated_at         TEXT    NOT NULL,
    UNIQUE (tier_number, usecase_name)
);
```

New deterministic script `plan/script/persist_usecase_map.py` — reads
`generate_tier_usecase_map.py`'s YAML output (`--in` payload:
`{tier_number: int}`), `INSERT OR REPLACE`s rows keyed on
`(tier_number, usecase_name)` (same idempotent-upsert pattern
`ADDING-A-USECASE.md` §1 calls out generally: *"UNIQUE constraint covers
the right key — `INSERT OR REPLACE` matches on this"*).

New usecase, wired into `standard.yaml` (proposal 2's manifest):

```yaml
- name: generate-usecase-map
  description: "generate + persist this tier's usecase map from standard.yaml + tiers.yaml — cached by source_hash, regenerates only when standard.yaml's usecases: block changes"
  steps:
    - order: 1
      kind: deterministic
      description: "generate plan/usecase-map/tier{N}.yaml, skip if source_hash unchanged"
      script: generate-tier-usecase-map
    - order: 2
      kind: deterministic
      description: "persist rows to dev_tier_usecase_map"
      script: persist-usecase-map
```

## 5. "Don't regenerate every time" — cache mechanism

rust_dev already has exactly this pattern for a different resource:
`script/policy.yaml`'s `strategy: fingerprint` (default for all checks,
`max_age_seconds: null` — *"fingerprint match alone is enough"*). Reuse
the same idea here instead of inventing a second caching convention:
`generate-tier-usecase-map`'s step 1 hashes `standard.yaml`'s `usecases:`
block, compares against `dev_tier_usecase_map`'s stored `source_hash` for
that tier, and no-ops (skips file write + DB write) on a match. This is
the direct answer to *"donot want to create it everytime"* — generation is
idempotent and cheap to call unconditionally (e.g. from every
`propose-tierN-*` run, proposal 5 §3), because the common case is a
same-hash no-op, not a real regenerate.

## 6. What consumes this map (forward pointer to proposal 5)

Proposal 5's `gather-tier-proposal-context` step queries
`dev_tier_usecase_map WHERE tier_number = ?` as its first, mandatory read —
directly satisfying *"a script which take this usecase map to input so
that when creating proposal it always has this usecase map."* No propose
usecase in proposal 5 can run without this table populated for its tier —
that's the enforced dependency, not just a convention.

## 7. Open questions

1. ~~Domain-suffix extraction from usecase names is a naming convention,
   not a schema field~~ — **resolved by proposal 6**: read
   `register_standard.rs`'s `UsecaseDecl` struct directly — `domain:` is
   already a real, first-class top-level field the real samgraha engine
   parses and resolves to `usecase.domain_id` (not a pcems-style
   name-string-only convention as this question originally assumed).
   `rust_dev`'s `standard.yaml` usecase entries should declare
   `domain: {domain_key}` directly, no name-suffix parsing needed. See
   proposal 6 §2 for the full mechanism, including the caveat that
   `rust_dev`'s own `seeder.py` (not this generic field) is what actually
   fires once `seeder_script` is declared.
2. ~~`_cross-tier.yaml` (§2 step 3, for `calculate` and any future
   whole-run usecase) — does it get its own DB table row too
   (`tier_number = NULL`), or stay file-only~~ — **moot**: §4's table is
   dropped (see status note in §0), so there's no table row question left
   to answer. `calculate` (proposal 3 §3) already carries no `domain:`
   field in `standard.yaml`, which is enough for the proposal 6 §3 query
   to exclude it from any `tier = ?` filter — no `_cross-tier.yaml` file
   or extra row needed.

## 8. Explicitly out of scope

The tier-as-first-class-row schema decision (proposal 2 §6, inherited
open question). Proposal 5's actual propose-usecase wiring — this
proposal only guarantees the map exists and is queryable, not how it gets
consumed. Any manual/hand-authored `plan/usecase-map/*.yaml` content —
every file this proposal produces is generated, per the "do not hand-edit"
contract in §2.
