# Gaps — base_dev

Things the plan/usecase layer implies (or requires to actually run) but does not specify or does not have built.

---

## GAP-001 — Audit stage never names the executor script
- **Severity:** HIGH
- **Status:** 🔴 **OPEN**

**Evidence:**
`plan/usecase/repo_existing/case_1_no_documentation/tier_1/02-audit.md:19-22`:
```
1. Deterministic document audit: Run `audit/deterministic/document/{domain}.yaml` against the document.
2. Deterministic section audit: Run `audit/deterministic/section/{domain}/*.yaml` against each section.
3. Semantic document audit: Run `audit/semantic/document/{domain}.md` against the whole document.
4. Semantic section audit: Run `audit/semantic/section/{domain}/*.md` against each section.
```
"Run \<yaml file\>" names data, not a command. This exact wording repeats identically across all 32 `02-audit.md` files (4 use cases × 8 tiers).

The executors already exist and work:
- `script/evaluate_rules.py` — dispatches on `evidence.type` (`section_presence`, `section_content`, `keyword_absence`, `relationship_absence`, `cross_reference`, `heading_analysis`, `content_deduplication`), reads `audit/deterministic/{document,section}/{domain}.yaml`, writes JSON. CLI: `--system-root --domain --doc --out`.
- `script/evaluate_semantic.py` — parses `audit/semantic/{document,section}/{domain}.md` rubric tables, heuristically scores criteria against document content. CLI: `--system-root --domain --doc --out [--context]`.

Neither script name nor invocation appears in any usecase `.md`. An agent executing `02-audit.md` literally has no instruction for how step 1-4 actually happens — it has to already know the codebase to guess `evaluate_rules.py` is the tool.

**Affected files:** 32× `plan/usecase/**/02-audit.md`

**Proposed fix:** Add executor line to steps 1-4 in each `02-audit.md`, e.g.:
```
1. Deterministic document audit: `python script/evaluate_rules.py --system-root <root> --domain {domain} --doc <doc-path> --out <out>/det-doc.json`, sourcing `audit/deterministic/document/{domain}.yaml`.
```
Since the wording is identical across all 32 files, this is one template edit propagated mechanically, not 32 independent edits — check if these `.md` files are rendered from a Jinja template (`render_usecase_docs.py` exists in `script/`) before hand-editing 32 copies.

---

## GAP-002 — Check-name scripts exist but are wired to nothing
- **Severity:** HIGH
- **Status:** 🔴 **OPEN** (not a doc fix — underlying wiring is unbuilt)

**Evidence:**
`script/mapping.yaml:1-11`:
```yaml
id: script_mapping_v1
generated_from: audit/**/*.{yaml,md}   # rule_ref / criterion_ref scan, not hand-maintained
note: |
  Placeholder version. The rule_ids listed below (qa-doc-014, sec-doc-009, etc.)
  are illustrative IDs from the proposal's examples, not real audit rules yet.
  No audit rule currently has a rule_ref pointing into script/schema/ — that
  wiring happens in Phase 6 (§8 retrofit), which adds script-sourced rules to
  audit/deterministic/* and audit/semantic/*. Once Phase 6 is done, regenerate
  this file by scanning all rule_ref values that resolve into script/schema/**.
```
20 check-name scripts exist in `script/` (`build-succeeds.py`, `artifact-exists.py`, `folder-structure.py`, `lint-pass.py`, `dependency-manifest.py`, `secret-scan.py`, `dependency-vuln-scan.py`, `module-boundary-diff.py`, `lint-standards.py`, `dependency-reachable.py`, `mock-api-runs.py`, `public-contract-diff.py`, `design-tokens-in-implementation.py`, `integration-points-exist.py`, `mitigation-present-at-boundary.py`, `unit-test-coverage.py`, `feature-family-mapping.py`, `traceability-refs-exist.py`), each listed in `mapping.yaml` against a `rule_id` (e.g. `qa-doc-014`, `build-doc-012`). None of those `rule_id`s exist in the real `audit/deterministic/**/*.yaml` files — confirmed against `audit/deterministic/document/01-vision.yaml`, whose real rule IDs are `vis-doc-001` through `vis-doc-007`, no `rule_ref` field anywhere.

Consequence: the "Scripts (check-name)" column in every `02-audit.md` step-0 table is correctly empty for every domain today (not a bug for tiers 1-2), but the column will **stay empty everywhere** — including QA, Build, Security, Implementation domains where these checks are clearly meant to run — until:
1. `audit/deterministic/**/*.yaml` rules get a `rule_ref` field pointing at a check name, and
2. `mapping.yaml` is regenerated from real rule scans instead of the placeholder table.

**Affected:** `script/mapping.yaml`, all `audit/deterministic/document/{04-feature,03-security,07-engineering,10-feature-technical,11-prototype,12-qa,13-implementation,14-build,16-product-guide}.yaml` (domains with check-name mappings per `mapping.yaml`'s `consumed_by` list).

**Proposed fix (build, not doc):** Add `rule_ref: <check-name>` to the specific rule in each target domain's deterministic yaml per `mapping.yaml`'s `consumed_by` mapping, then regenerate `mapping.yaml` from a real scan (this is "Phase 6" per the note — track as its own phase, not folded into the doc-wiring fix).

---

## GAP-003 — Fix mechanism is an unfilled template stub
- **Severity:** HIGH
- **Status:** 🔴 **OPEN** (not a doc fix — mechanism unbuilt)

**Evidence:**
`plan/core/loop.yaml:56-63`:
```yaml
fix_loop:
  trigger: Path B AND final_score < threshold.score
  mechanism: >
    For each failing section, feed the finding into
    templates/generation/section/{domain}/{section}.md's ## Audit Fix
    slot, regenerate, re-audit that section.
  max_iterations: 5
  fallback: human_review
```
`templates/generation/section/01-vision/01-purpose.md:48-50`:
```markdown
## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
```
The slot the fix loop is supposed to feed a finding into is a literal placeholder comment, not a template with variables/instructions for how a finding (from `evaluate_rules.py`/`evaluate_semantic.py` JSON output) turns into regeneration guidance. Spot-checked one file; the `<!-- Phase 5: ... -->` marker pattern suggests this is a known, deliberately deferred stub (i.e. self-admitted, like `mapping.yaml`'s Phase 6 note), not an oversight — but it means `03-fix.md`'s "apply" step has nothing concrete to execute against for section-level fixes.

**Affected:** likely all section-level generation templates across 16 domains (only `01-vision/01-purpose.md` confirmed directly; same `<!-- Phase 5 -->` marker pattern should be grepped across `templates/generation/section/**/*.md` to get an exact count before scoping the fix).

**Proposed fix (build, not doc):** Design and fill the `## Audit Fix` slot format (what a finding object looks like, how it's substituted into the regeneration prompt), track as "Phase 5" per the existing marker — separate work item from GAP-001/004.

---

## GAP-004 — No single doc states the full pipeline order + CLI chain
- **Severity:** MEDIUM
- **Status:** 🔴 **OPEN**

**Evidence:**
The real, working chain — confirmed by reading each script's CLI args — is:
```
evaluate_rules.py    --system-root --domain --doc --out            (deterministic)
evaluate_semantic.py --system-root --domain --doc --out [--context] (semantic)
calculate.py          --system-root --domain --out [--out-dir] [--previous-report]  (7 formulas incl. final_score, score_bands, trend_comparison)
report.py             --system-root --domain --scores --out [--type] [--scope]      (renders report from calculate.py's scores JSON)
```
`plan/core/loop.yaml:41-54` (`path_selection.audit`) names the *data* files (deterministic/semantic yaml + md, report templates) each stage draws on but never names the 4 scripts above or their order/data-flow (`evaluate_rules.py` output feeds `calculate.py --out-dir`, whose output feeds `report.py --scores`). `plan/core/README.md` describes the loop conceptually but also never lists the script chain.

**Affected:** `plan/core/loop.yaml`, `plan/core/README.md` (or a new file alongside them).

**Proposed fix:** Add a "Script Chain" section to `plan/core/README.md` (or a new `plan/core/scripts.yaml` mirroring `loop.yaml`'s style) listing the 4 scripts in order with their CLI args and what output feeds what input. This unblocks GAP-001's per-usecase edits — write this first, then GAP-001's `02-audit.md` edits can reference it instead of repeating full CLI args 32 times.

**Correction to scope (confirmed after re-checking `script/init.py`):** the "4 scripts" above are incomplete. `script/init.py` docstring: *"Orchestration engine for the base_dev documentation pipeline. Reads tiers.yaml and loop.yaml... executes the tier-by-tier pipeline: scaffold→structural→content→validate→calculate→report→fix."* This is a real, already-built single-command orchestrator covering the whole chain:

```
scaffold.py                      — document stub from templates/generation/document + section
generate_structural_sections.py  — deterministic-format section skeletons (constraints, dependencies, etc.)
(content: LLM fills TODO markers — no script, this is the generation-agent's job)
validate.py                      — runs the 18-20 check-name scripts per script/mapping.yaml, aggregates findings
evaluate_rules.py                — deterministic yaml rule evaluation (per domain, called per GAP-001)
evaluate_semantic.py             — semantic md rubric evaluation (per domain, called per GAP-001)
calculate.py                     — 7 scoring formulas (final_score, score_bands, trend_comparison, etc.)
analyze.py                       — reads calculate.py + validate.py output, produces {domain}-fix-plan.json
report.py                        — renders report template from calculate.py's scores JSON
visualize.py                     — matplotlib PNG charts from check-result JSONs + scores
report_html.py                   — self-contained HTML report embedding visualize.py's PNGs + all tables
```
`grep -rl "init.py\|scaffold.py\|validate.py\|analyze.py\|visualize.py\|report_html.py\|calculate.py" plan/` → **zero matches.** None of these 10 scripts, nor the fact that `init.py` already automates the entire chain as one command, appears anywhere in `plan/usecase` or `plan/core`. `03-fix.md`'s "apply" step (GAP-003) and the missing image/HTML rendering step were previously uninvestigated — `analyze.py` already does exactly what GAP-003 assumed was unbuilt (produces a fix plan, file-based JSON, not the `## Audit Fix` template-slot mechanism `loop.yaml` describes — these are two different, both-real fix-plan mechanisms and it's unclear from the docs which one is authoritative; needs a design decision, not just a doc fix).

**Revised proposed fix:** `plan/core/README.md` should state `init.py` is the canonical entry point and list what it orchestrates; `02-audit.md`/`03-fix.md` per-usecase docs should reference `init.py --use-case <case>` for the common path and only detail manual per-script invocation as the fallback/debug path.

---

## GAP-005 — DB schema alignment: `rules.script_check_id` never gets populated by either side
- **Severity:** MEDIUM
- **Status:** 🔴 **OPEN**

**Context:** `base_dev` itself is entirely file/JSON-based — confirmed zero `sqlite`/`database`/`db_path` references anywhere in `system/base_dev` (scripts write JSON/PNG/HTML/MD to disk only). The DB layer lives in a separate repo, `E:\Python\samgraha` (Rust engine, `crates/`), which has a real schema at `schema/knowledge-hub/*.sql` and a loader (`schema/knowledge-hub/knowledge-hub-loader.py`) that reads a system directory shaped exactly like `base_dev` (`audit/deterministic`, `audit/semantic`, `script/schema`, `calculation`, `templates`, `plan/core`, `plan/usecase`) and ingests it into that DB. This is the correct separation — `base_dev` is source-of-truth files, the loader populates the DB, not a gap by itself.

**Verified alignment issue:**
`schema/knowledge-hub/11-rules.sql:52-53` reserves a column exactly for the wiring GAP-002 described as missing:
```sql
script_check_id  INTEGER REFERENCES script_checks(id) ON DELETE CASCADE,
```
But `knowledge-hub-loader.py`'s `_insert_rule_and_params()` (loader repo, lines ~614-677) never receives or sets `script_check_id` — its `INSERT INTO rules` column list (line ~644-647) omits it entirely, and every call site (`pass_5`, line ~786) passes no such argument. Confirmed by reading the function signature and its one call site directly. So even after GAP-002 is fixed (a real `audit/deterministic/*.yaml` rule gets `evidence: {type: script_result, ...}` pointing at a check), the loader has no code path that resolves it to `script_checks.id` and writes it into `rules.script_check_id` — it would load with `evidence_type: script_result` but `script_check_id: NULL`, silently breaking the very link it exists to represent.

**Spot-check — what does line up:** `script/schema/03-security/secret-scan.schema.json` correctly has `properties.category.const: "A"`, which `pass_4` (loader) reads via `schema_data["properties"]["category"]["const"]` to populate `script_checks.category`. `manifest.yaml`'s `check`/`timeout_seconds`/`requires_network` fields also line up with what `pass_4` reads. Only spot-checked `secret-scan`; the other 19 check schemas should be verified the same way before assuming full alignment.

**Open question, not yet resolved:** MCP tools available in this environment (`store_document_report`, `store_section_report`, `store_generated_content`, `store_system_plan`, `get_document`, `get_section`) imply runtime data (actual generated document content, actual per-run audit scores, actual fix plans) gets persisted somewhere. `schema/knowledge-hub/*.sql` only models **static** definitions (rules, templates, script checks, workflow/tier structure) — no table for generated document content, per-run scores, or fix-plan instances. Either those MCP tools write to a schema not discovered in this session (only `schema/knowledge-hub/` exists under `E:\Python\samgraha\schema\`), or runtime persistence is itself unbuilt. Needs verification against `crates/services`/`crates/mcp` (out of scope for this pass — flagging, not asserting).

**Affected:** `E:\Python\samgraha\schema\knowledge-hub\knowledge-hub-loader.py` (cross-repo, not `base_dev`, tracked here for visibility since it blocks GAP-002 end-to-end); `system/base_dev/script/schema/**` (19 of 20 check schemas unverified against loader expectations).

**Proposed fix:** (1) In the loader repo, add `script_check_id` resolution to `_insert_rule_and_params`/`pass_5` — look up `script_checks` by `(standard_id, check_name)` when `evidence_type == 'script_result'` and a check name is present in the rule's evidence params, pass the resolved id through. (2) Verify remaining 19 `script/schema/**/*.schema.json` files have `properties.category.const` set. (3) Resolve the open question on runtime persistence before assuming the MCP store_* tools are backed by anything real.
