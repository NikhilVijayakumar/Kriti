# pcems_2026 Content-Ingestion Pipeline Proposal

**Problem**: The academic pipeline assumes code-first repos (source code → AST analysis → LLM analysis → DB). Documentation-first repos like Bodha (369 doc files, pre-built module analyses, complete draft sections) have no path to populate the DB tables the downstream pipeline depends on.

**Root cause**: `discover_modules.py:24` hardcodes `docs` in its skip set. `gather_module_evidence.py` only parses Python ASTs. No script loads pre-existing `docs/paper/{system}/` content into `academic_module_analysis` or `academic_cross_module_analysis`.

**Existing partial solution**: `gather_domain_evidence.py:57-71` already reads `docs/paper/**/*.md` from disk for the generation triads' raw evidence. But the structured DB layer (which cross-module evidence, audit, and scoring depend on) remains empty.

---

## §1 Design: Three New Scripts + Workflow Integration

### §1a. `discover_docs_modules.py` — Module discovery from docs structure

**Location**: `base_academic/script/_shared/analysis/discover_docs_modules.py`

**Input**: `{paper_id: int, standard: str}`

**Logic**:
1. Walk `docs/paper/{system}/modules/` (system from standard name)
2. Each subdirectory = one module (chunking, parsing, monitoring)
3. Register each via `academic_schema.upsert_module()`
4. Also register a `_cross_module` pseudo-module for cross-module analysis

**Output**: Envelope with `modules: ["chunking", "parsing", "monitoring", "_cross_module"]`

**Fallback**: If `docs/paper/{system}/modules/` doesn't exist, check `docs/paper/modules/` (system-agnostic layout).

### §1b. `load_docs_module_analysis.py` — Load per-module analysis from disk

**Location**: `base_academic/script/_shared/analysis/load_docs_module_analysis.py`

**Input**: `{paper_id: int}`

**Logic**:
1. Get all modules from `academic_modules` for this paper
2. For each module (skip `_cross_module`):
   - Walk `docs/paper/{system}/modules/{module_name}/`
   - Map filenames to `analysis_kind`: `{stem}.md → stem` (architecture.md → "architecture")
   - Call `academic_schema.upsert_module_analysis(module_id, kind, content, file_path=...)`
3. Report: `{loaded: int, modules: [...], kinds: [...]}`

**Mapping** (Bodha example):
| File | analysis_kind |
|------|--------------|
| `chunking/architecture.md` | architecture |
| `chunking/novelty.md` | novelty |
| `chunking/mathematics.md` | mathematics |
| `chunking/gaps.md` | gaps |
| `chunking/summary.md` | summary |

### §1c. `load_docs_cross_module_analysis.py` — Load cross-module analysis

**Location**: `base_academic/script/_shared/analysis/load_docs_cross_module_analysis.py`

**Input**: `{paper_id: int}`

**Logic**:
1. Walk `docs/paper/{system}/cross_module/`
2. For each `.md` file: map `{stem}.md → stem` as `analysis_kind`
3. Call `academic_schema.upsert_cross_module_analysis(paper_id, kind, content, file_path=...)`

**Mapping** (Bodha example):
| File | analysis_kind |
|------|--------------|
| `cross_module/novelty.md` | novelty |
| `cross_module/architecture.md` | architecture |
| `cross_module/interactions.md` | interactions |
| `cross_module/mathematics.md` | mathematics |
| `cross_module/patterns.md` | patterns |
| `cross_module/dependencies.md` | dependencies |
| `cross_module/gaps.md` | gaps |
| `cross_module/consistency_check.md` | consistency_check |

---

## §2 Schema Registration

Add to `pcems_2026/script/schema/standard.yaml` under `scripts:`:

```yaml
  # --- docs-first ingestion usecase ---
  - name: discover-docs-modules
    location: ../../../base_academic/script/_shared/analysis/discover_docs_modules.py
    purpose: "discover module boundaries from docs/paper/{system}/modules/ structure"
  - name: load-docs-module-analysis
    location: ../../../base_academic/script/_shared/analysis/load_docs_module_analysis.py
    purpose: "load pre-existing per-module analysis .md files into academic_module_analysis"
  - name: load-docs-cross-module-analysis
    location: ../../../base_academic/script/_shared/analysis/load_docs_cross_module_analysis.py
    purpose: "load pre-existing cross_module/*.md files into academic_cross_module_analysis"
```

Add under `usecases:`:

```yaml
  - name: docs-first-ingestion
    description: "discover module structure from docs and load pre-existing analysis into DB"
    steps: []
```

---

## §3 Workflow Integration (`run_full_workflow.py`)

Insert between Phase 2 (classify-repo) and Phase 3 (expand_triads):

```
# --- Phase 2b: Docs-first ingestion (if docs/paper/{system}/modules/ exists) ---
docs_system_dir = Path(repo_root) / "docs" / "paper" / args.standard / "modules"
if not docs_system_dir.is_dir():
    docs_system_dir = Path(repo_root) / "docs" / "paper" / "modules"

docs_modules = []
if docs_system_dir.is_dir():
    docs_modules = [d.name for d in docs_system_dir.iterdir()
                    if d.is_dir() and not d.name.startswith(".")]
    if docs_modules:
        # Run docs-first ingestion: discover + load analysis
        # Then re-query modules for paper (now includes docs modules)
        # Skip code-based analysis triads (they'd find nothing useful)
```

The workflow would:
1. Check if `docs/paper/{system}/modules/` exists
2. If yes: run `discover-docs-modules` → `load-docs-module-analysis` → `load-docs-cross-module-analysis`
3. Re-query `modules_for_paper()` (now returns docs modules)
4. **Skip** code-based analysis triads (novelty, gap, math, diagrams) — they'd produce nothing useful for docs modules
5. Proceed to generation triads (which use `gather_domain_evidence` reading from disk)

For mixed repos (both source code + docs): discover from both, load docs analysis, run code analysis for code modules only.

---

## §4 Blast Radius

- **New files**: 3 scripts (~150 lines each)
- **Modified files**: `standard.yaml` (+12 lines), `run_full_workflow.py` (~30 lines insertion)
- **No changes to**: `gather_domain_evidence.py`, `gather_cross_module_evidence.py`, `persist_section_draft.py`, or any existing audit/scoring scripts
- **Downstream impact**: None — the scripts write to existing DB tables using existing schema functions. The generation triads already read `docs/paper/**/*.md` from disk.

---

## §5 Open Questions

1. **Mixed repos**: Should code-based analysis triads still run for code modules when docs modules exist? (Currently: skip all code triads for simplicity.)
2. **Draft sections**: Bodha has `drafts/0. Abstract.md` through `8. Reference.md`. Should the pipeline also seed these as `stage='generate'` narratives, or just load analysis and let the LLM generate from raw docs? (User: generate from docs, not seed.)
3. **Cross-library analysis**: Bodha has `cross_library/` docs (cross-system analysis). Should `load_docs_cross_module_analysis` also scan `cross_library/`? Or leave that for a future proposal?
