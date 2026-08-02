# rust_dev — Code/Test/Build Generation Layer (Proposal)

## 0. Status

**Approved; scripts now functionally verified.** The owner reviewed the
retroactive proposal and locked the scope decisions in §5/§6 (feature-
technical tension accepted; generator deferred; samgraha wiring deferred).
The planned fixes from review were applied: all six scripts rewritten to
the shared deterministic-script contract, the tarpaulin hardcode removed
from the profile layer, and the minor inconsistencies in §4 fixed. Unlike
the initial submission, the scripts are now executed end-to-end against
fixture crates on both ubuntu (bash/WSL) and windows (PowerShell) — see
§7. Going forward, proposals for this line of work land here *before*
implementation, not after.

## 1. What prompted this

Owner's original ask (paraphrased): for each of `rust_dev`'s 16 (confirmed
live: 13, see §2) domains, define a section map + section profile the way
`E:\Python\Bodha\.bodha-structure\section\` does for a research paper —
what sections exist, why, mandatory/optional, how to validate — plus, for
the three domains that touch code specifically, something deeper: *"when
it comes to code test and build in documentation it is same however the
implementation should be actual code test and build so in that we need to
define how the code should be, what are considerations, how test should
be, what are considerations, how to use other documentation like
architecture engineering external context feature feature-technical to
generate the code and test and how to build it."*

Two rounds of scoping (this session) narrowed that to one deliverable:
design the layer that turns Implementation(13)/QA(12)/Build(14)'s
planning-document content into actual `.rs` code, test files, and CI
execution — because everything else in the original ask already exists.

## 2. What exists today (confirmed live, this session)

- `rust_dev/domain/` has **13** domains, not 16 — files `01`-`16` with
  `06`/`09`/`11` reserved and unused for dropped domains (design,
  feature-design, prototype). Confirmed against
  `00-domain-relationships.md`.
- `domain/12-qa.md`, `13-implementation.md`, `14-build.md` are already
  fully specified doc-standards (700-1150 lines each — Purpose, per-section
  templates with writing guidance and correct/incorrect examples, Required
  Sections table, Audit/Validation/Generation rules). `common/tier5/`
  (implementation), `tier6/` (qa), `tier7/` (build) each already have the
  full audit scaffolding — `audit/{deterministic,semantic}/{document,
  section}/*`, `script/{schema,ubuntu,windows}/*`, `templates/*` — same
  shape as `tier1`/`tier2`. **Nothing to design there** — this proposal
  does not touch `tier5`/`tier6`/`tier7`.
- But those three domains only govern **planning documents about**
  implementation/testing/building, not the real `.rs` code, test files, or
  CI execution. `feature-technical.md`'s "Crate Implementation"/"Error
  Implementation" sections name real trait/struct/error identifiers in
  prose, but the same document's own "Out of Scope"/"Technology
  Independence" rules explicitly forbid real Rust syntax — a live internal
  tension, not resolved by this proposal (see §5). `engineering.md`'s Code
  Standards section body is literally `(To be written by the domain
  expert.)`.
- Repo-wide search (this session, 3 Explore agents) found **zero existing
  precedent** anywhere in Kriti for a profile that drives code generation
  — not in `rust_dev`'s siblings (`base_dev`, `electron_dev`, `fastapi_dev`,
  `react_dev`, all doc-only pipelines), not in `python_hackathon` (which
  *audits* already-written team code via `.pylintrc`/`mypy.ini`/etc., but
  doesn't drive generation). No `crates/` or `.rs` file exists anywhere
  under `rust_dev/`.

So this is new design, not a port of an existing rust_dev pattern — though
the *shape* is a direct port of two patterns that do exist: Bodha's
`section/{map,profile-default,profile}` and rust_dev's own `tier1..8`
build-out discipline (prove the pattern on one tier, then repeat it).

## 3. Proposed design

New sibling directory, parallel to `common/tier1..8`, not itself a
numbered tier because it produces no document:

```
common/codegen/
├── code/    — governs .rs source generation
├── test/    — governs test-file generation
└── build/   — governs CI/CD execution
```

Each branch reuses the exact three-layer pattern Bodha proved for
document sections, applied to a **code/test/build unit** instead of a doc
section:

- **`{branch}/map/{branch}-map.yaml`** — same fields as Bodha's
  `section-map.yaml` (`id/title/parent_id/level/order/required/generated/
  profile/purpose`), with `source` renamed to **`upstream`**: which doc
  section this unit is generated from (e.g. `feature-technical.
  error_implementation`, `qa.unit_testing`, `build.cicd_validation`).
- **`{branch}/profile-default/*.yaml`** — reusable categories
  (error-handling, ownership-pattern, unit, lint-stage, ...), each
  **transcribing already-written policy** from `engineering.md`/`qa.md`/
  `build.md` rather than inventing new rules, with Bodha's
  `inheritance.allow_override`/`prohibit_override` contract.
- **`{branch}/profile/*.yaml`** — concrete per-unit instances that
  `inherits:` a default category and add `generation_sequence`,
  `completion.checklist`, `review.questions`, `validation.rules` — same
  shape as Bodha's `abstract.yaml`/`methodology.yaml`.
- **`audit/{deterministic,semantic}/{branch}/*`** — deterministic checks
  extend `tier5`'s existing 3 scripts (`lint-pass.ps1` already runs
  `cargo clippy`) with 3 new ones; semantic rubrics follow the exact
  `rubric.md` + generic `{{ unit }}`-templated prompt pattern already
  found at `.samgraha/pcems_2026/step1-draft-for-completeness/audit/` in
  Bodha.
- **`script/schema/{branch}/*.manifest.yaml` + `.schema.json` +
  `script/{ubuntu,windows}/{branch}/*.{sh,ps1}`** — same dual-OS pattern
  `tier5`'s `lint-pass`/`folder-structure`/`dependency-manifest` already
  use, including the fixed shared deterministic-script contract: named
  args `--repo-root/--repo-fingerprint/--out` (sh) or
  `$RepoRoot/$RepoFingerprint/$Out` (ps1), a JSON result envelope written
  to `$Out` (never stdout) with keys
  `repo_fingerprint/check/domain/category/status/metrics/evidence/
  executed_at`, `exit 1` only on internal error, `exit 0` on
  pass/fail/not_applicable. Manifests declare `requires_tools` and a
  `runs:` list per OS. Scripts may name a tool as implementation detail;
  profiles keep policy tool-agnostic (e.g. `unit.yaml` carries a generic
  `[Tool]` slot, not a hardcoded coverage tool).

**Scope discipline applied**: only one profile per branch is fully worked
end-to-end (`error-enum`, `unit-test`, `lint-stage`) — proving the vertical
slice rather than fleshing out every unit type on faith. The remaining
unit types are stubbed in each `map.yaml` with `generated: false` so the
taxonomy is visible without being built speculatively.

## 4. Files created (confirmed live, `find` run this session)

```
common/codegen/
├── code/
│   ├── map/code-map.yaml                          (5 units: error-enum[live], trait-definition, struct-impl, service-impl, module — 4 stubs)
│   ├── profile-default/{error-handling,ownership-pattern,async-pattern,trait-definition,struct-impl}.yaml
│   └── profile/error-enum.yaml                     (worked instance)
├── test/
│   ├── map/test-map.yaml                          (5 units: unit-test[live], integration-test, e2e-test, property-test, benchmark-test — 4 stubs)
│   ├── profile-default/{unit,integration,e2e,property,benchmark}.yaml
│   └── profile/unit-test.yaml                      (worked instance)
├── build/
│   ├── map/build-map.yaml                          (5 units: lint-stage[live], test-stage, security-stage, package-stage, versioning-stage — 4 stubs)
│   ├── profile-default/{lint-stage,test-stage,security-stage,package-stage,versioning-stage}.yaml
│   └── profile/lint-stage.yaml                     (worked instance)
├── audit/
│   ├── deterministic/{code/error-enum.yaml, test/unit-test.yaml, build/lint-stage.yaml}
│   └── semantic/{code/error-enum.md, test/unit-test.md, build/lint-stage.md, prompt/semantic-audit.md}
└── script/
    ├── schema/{code/unsafe-usage-scan, test/coverage-threshold, build/rustfmt-check}.{manifest.yaml,schema.json}
    ├── ubuntu/{code/unsafe-usage-scan.sh, test/coverage-threshold.sh, build/rustfmt-check.sh}
    └── windows/{code/unsafe-usage-scan.ps1, test/coverage-threshold.ps1, build/rustfmt-check.ps1}
```

40 files total (27 YAML, 3 JSON schemas, 6 scripts, 4 semantic-rubric
docs). Plus a short addendum in `00-domain-relationships.md`
(new "Code/Test/Build Generation Layer" section, inserted before "##
Rust-Specific Cross-Domain Relationships") documenting why `codegen/`
isn't a numbered tier and pointing at this proposal.

## 5. Known open issue — resolved by owner

`feature-technical.md`'s "Crate Implementation"/"Error Implementation"
sections name real trait/struct/error identifiers in prose, while the
same document's "Out of Scope"/"Technology Independence" rules forbid
real Rust syntax. **Owner accepted this proposal's resolution**: don't
edit `feature-technical.md`. Its sections stay the *naming* source (which
traits/structs/errors exist); `codegen/`'s profiles are what expand those
names into actual syntax. Flag closed.

## 6. Explicitly deferred (owner's own prioritization this round)

Not touched by this proposal or its files:

- DB schema extension — commit-hash linkage, dedicated `model_details`
  table, formal `script_result` table.
- The missing `python_hackathon/calculation/validation/
  scoring_validation.yaml` runner script (12 rules defined, no runner
  found).
- docx/pdf report export (only markdown/html exist today).
- The **generator** itself: the step that turns profile/map content into
  actual `.rs`, test, and CI files. This layer only produces the maps,
  profiles, audits, and executable check scripts a generator would
  consume; no generation engine is written.
- The 4 stub units per branch (`trait-definition`, `struct-impl`,
  `service-impl`, `module` for code; `integration-test`, `e2e-test`,
  `property-test`, `benchmark-test` for test; `test-stage`,
  `security-stage`, `package-stage`, `versioning-stage` for build) — map
  entries exist as a visible taxonomy, but no `profile/*.yaml` is written
  for any of them yet.

## 6a. Wiring explicitly deferred

`common/codegen/` is **not registered** as a samgraha standard:
`standard.yaml`, `mapping.yaml`, and the `seeder.py` were deliberately
left untouched. The layer is untracked content on disk — its scripts run
standalone (proven in §7) but nothing in the samgraha wiring invokes them
yet. Registration is a separate follow-up.

## 7. Verification performed this session

1. All 27 YAML files parse (`python -c "yaml.safe_load(...)"` over
   every file under `common/codegen/`, 0 errors) and all 3 new JSON schema
   files parse (0 errors).
2. `profile/error-enum.yaml`'s `inherits: [error-handling]` resolves
   against `profile-default/error-handling.yaml`'s `applies_to` list and
   does not touch anything in that file's `prohibit_override`.
3. Every `upstream:`/`source:` reference in the map and profile-default
   files names a section that was read in full this session from
   `engineering.md`, `feature-technical.md`, `qa.md`, `build.md`'s own
   Required Sections tables — no invented upstream section name.
4. `error-handling.yaml`'s policy (thiserror/anyhow split, `unwrap()` ban,
   `// SAFETY:` requirement) was checked against `engineering.md`'s
   directly-quoted Rust Engineering Practices text — no contradiction.
5. **All six scripts were executed end-to-end** (this session) against
   fixture crates on both OSes, not just parse-checked:
   - `unsafe-usage-scan.{sh,ps1}` — flags SAFETY-less `unsafe`
     blocks/items and `unwrap()`/`expect()` outside test scope on the
     fixture's expected lines (4, 6, 12, 18); ignores SAFETY-guarded and
     `#[cfg(test)]`-scoped cases; clean crate → `pass`, empty crate →
     `not_applicable`, bad repo-root → `error` + `exit 1`. sh and ps1
     produce identical findings.
   - `coverage-threshold.{sh,ps1}` — reads tarpaulin's top-level
     `coverage` string and aggregates `files[].coverage` arrays
     (covered/total lines, nulls skipped); honors `--threshold`/`-Threshold`;
     pass/fail/error paths all verified on both OSes with matching numbers.
   - `rustfmt-check.{sh,ps1}` — pass (`cargo fmt --check` exit 0),
     fail-with-diff-excerpt, `not_applicable` (no `Cargo.toml`), and
     `error`/`exit 1` (bad root, missing cargo) all verified on both OSes.
   - Every run wrote a contract-shaped envelope to `$Out` (never stdout)
     and returned the documented exit code.
6. The `pipefail` bug class was caught and fixed during testing: a
   `head`/no-match `grep` in a `set -euo pipefail` pipeline killed
   `coverage-threshold.sh` before it could write its envelope — now all
   pipelines are `|| true`-guarded and `head`-free (see script comments).
7. No `jq`/`bc` in any `.sh`; no hardcoded coverage tool remains in the
   profile layer (`unit.yaml` uses a generic `[Tool]` slot); audit
   deterministic checks carry `mandatory:` flags consistent with tier5.

**Not verified**: real tarpaulin execution (cargo-tarpaulin is not
installed on either OS — paths exercised via JSON fixtures/mocks),
clippy invocation (lint-stage-002), and any live crate. Wiring to
samgraha is intentionally not exercised (see §6a).
