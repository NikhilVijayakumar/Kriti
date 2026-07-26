# pcems_2026 — PCEMS 2026 Conference Paper System

Concrete samgraha system for generating IEEE-style academic papers from
code repositories, following the PCEMS 2026 conference template.

## Domains

**6 structural (scored):** title-and-metadata, introduction, methodology,
findings, conclusion, references

**5 cross-cutting (audit-only):** novelty, gaps, mathematics, tables, figures

## Shared vs. Owned

| Component | Source |
|-----------|--------|
| Scripts (schema-init through render-paper) | `base_academic/script/` |
| Verify scripts | `base_academic/script/verify/_common.py` |
| Content rules | `base_academic/script/common/content_rules.py` |
| Generation prompts (per-domain) | `pcems_2026/prompt/generation/` |
| Audit prompts | `pcems_2026/prompt/audit/` |
| Propose prompts | `pcems_2026/prompt/propose/` |
| Deterministic rules | `pcems_2026/calculation/` |
| Semantic rubrics | `pcems_2026/audit/semantic/document/` |
| Templates (markdown + HTML) | `pcems_2026/templates/` |
| Guide + reference | `pcems_2026/guide/` + `pcems_2026/reference/` |

## Registration

When registering a repository for analysis, `repo_root` must point at
the **code root** (where top-level packages live), not at a docs folder.
`discover_modules.py` walks source code structure and explicitly skips
`docs/`, `tests/`, and similar non-source directories. Pointing
`repo_root` at a docs-only folder will return zero modules and starve
the analysis usecases.

## External Bibliography

The system collates in-repo citation markers by default. To include
external literature, supply a bibliography file and register its path
in the paper's metadata:

```python
academic_schema.set_paper_metadata(conn, paper_id, "bibliography_path",
    str(Path("reference/external_references.txt").resolve()))
```

File format: one citation per line (plain text) or BibTeX
(`@article{...}`, `@inproceedings{...}`). External citations are merged
with in-repo citations during `collate-references`, deduplicated, and
numbered sequentially.

## Template

The PCEMS 2026 template specifies APA reference style, but all 11
accepted sample papers use IEEE numbered style. The guide documents
this discrepancy (`Writing Guide/07-references.md`,
`Examples/06-reference-examples.md`). Follow the sample papers'
convention: IEEE numbered citations `[1], [2]`.

## Rendering

DOCX/PDF rendering lives in `pcems_2026/script/render/`:
- `assemble-final-document.py` — concatenates domain drafts per
  `_master-schema.yaml` (reading each domain's `stage='polish'` narrative,
  falling back to `budget-fit` then `cite`), weaves cross-cutting content
  from `academic_cross_module_analysis` into its target section, fills
  each domain's HTML fragment template
- `extract-mermaid-images.py` — rasterizes mermaid diagrams via `mmdc`
- `render-docx.py` — pandoc conversion with reference doc
- `render-pdf.py` — playwright (adapted from `hackathon/.../export_team_pdfs.py`)
