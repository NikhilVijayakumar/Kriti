# Adding a usecase / step / script / prompt — checklist

Run through in order. Each step guards a bug class hit repeatedly in earlier sessions.

## 1. Schema (if new tables or columns needed)

- [ ] Create or edit `.sql` file under `common/schema/` — numbered filename, no gaps
- [ ] CHECK constraints include every valid value (forgot a value = silent skip, not error)
- [ ] UNIQUE constraint covers the right key — `INSERT OR REPLACE` matches on this
- [ ] Add `model TEXT NOT NULL DEFAULT ''` if this table tracks LLM-generated content (multi-model comparison needs it)

## 2. Script (deterministic step)

- [ ] Create `.py` file under the appropriate `step*/` tree
- [ ] `sys.path.insert` depth is correct — count `..` from your file back to `common/script/`
- [ ] Import `_adapter` and `academic_schema` via that sys.path
- [ ] Signature follows `parse_step_args()` contract — reads `--in` payload, writes `write_envelope()` JSON
- [ ] Script name registered in `common/schema-manifest/standard.yaml` under `scripts:`
- [ ] If the script touches metadata keys, update `_ALLOWED_*_KEYS` sets in `common/script/academic_schema.py`

## 3. Prompt (semantic step)

- [ ] Create `.md` file under the appropriate `step*/prompt/` tree
- [ ] Prompt name registered in `standard.yaml` under `prompts:`
- [ ] Template variables (`{{var}}`) match what `gather-proposal-context` actually sends

## 4. Usecase (wires script + prompt steps together)

- [ ] Registered in `standard.yaml` under `usecases:` with correct step ordering
- [ ] Each deterministic step references a `script:` name (must exist in `scripts:`)
- [ ] Each semantic step references a `prompt:` name (must exist in `prompts:`)

## 5. Allow-lists (if metadata.yaml keys touched)

- [ ] `_ALLOWED_METADATA_KEYS` in `academic_schema.py` covers the new key
- [ ] `_ALLOWED_MODULE_PRIMARY_KEYS` / `_ALLOWED_MODULE_DEPENDENT_KEYS` if modules block changed
- [ ] `_ALLOWED_AUTHOR_KEYS` / `_ALLOWED_AFFILIATION_KEYS` if authors/affiliations changed
- [ ] `_walk_unknown_keys` sentinel `... (Ellipsis)` — only `custom:` gets this escape hatch

## 6. Smoke test

- [ ] Run `python common/script/smoke_test.py` — 7/7 PASS
- [ ] The new script actually imports without error: `python -c "import importlib.util; spec = importlib.util.spec_from_file_location('x', 'path/to/new_script.py'); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)"`
- [ ] (smoke_test.py's `import_check` will do this automatically for registered scripts, but run the import once manually before registering so the failure path is clear)

## 7. Integration (one real run)

- [ ] If this is a new propose-* gate: run propose → approve → commit cycle end-to-end
- [ ] If this is a new analysis step: run with real repo data, confirm rows written
- [ ] If this touches the verify pipeline: run with 2 models, confirm 2 rows per (claim, check_kind)
