# PCEMS 2026 Guide — Full Implementation Proposal

## 0. Current State

### What Exists (complete)

| Section | Files | Status |
|---------|-------|--------|
| `guide/Conference Guidelines/` | 7 docs + README | Complete — extracted from template PDF |
| `guide/Philosophy/philosophy.md` | 378 lines | Complete |
| `documentation-standards/` | 6 domain standards | Complete |
| `audit/semantic/document/` | 6 rubrics | Complete |
| `calculation/` | 4 YAML configs | Complete |
| `plan/core/` | tiers.yaml, loop.yaml | Complete |

### What Exists but Empty/Skeleton

| Section | Status |
|---------|--------|
| `guide/README.md` | Skeleton — 35 headings, no body text |
| `templates/generation/` | Empty — loop.yaml references `templates/generation/document/{domain}.md` |
| `templates/audit/` | Empty — loop.yaml references `templates/audit/summary/{domain}-report.md` |

### What's Missing Entirely

| Section | Purpose |
|---------|---------|
| `guide/Writing Guide/` | Per-section writing guidance from template + samples |
| `guide/Figures/` | Figure standards, placement rules, examples |
| `guide/Tables/` | Table standards, Word-native rules, examples |
| `guide/Mathematics/` | Equation formatting, notation conventions |
| `guide/Reviewer Expectations/` | What reviewers look for, rejection reasons |
| `guide/Examples/` | Annotated excerpts from sample papers |
| `guide/Checklists/` | Per-domain and per-section checklists |
| `guide/Common Mistakes/` | Anti-patterns with corrections |
| `guide/Assets/` | Font specs, spacing tables, style reference cards |
| `audit/deterministic/document/` | 6 YAML files referenced by documentation-standards |

### Filename Anomalies

Two files have leading spaces: ` 02-manuscript-structure.md` and ` 06-pdf-compliance.md`

---

## 1. PDF Limitation

**Template PDF**: Already extracted into `Conference Guidelines/` — appears complete.

**Sample Papers** (11 PDFs): Not analyzed. These are the source for writing style, section length norms, citation density, figure/table usage, math conventions, and terminology patterns.

**Proposal**: Sample paper analysis must happen first (human or PDF-capable model). Guide is built from those findings.

---

## 2. Target Guide Structure (~30 new files)

```
guide/
├── README.md                          # Fill skeleton
├── Conference Guidelines/             # Fix filename spaces
├── Philosophy/                        # Exists
├── Writing Guide/                     # NEW (7 files)
│   ├── 01-writing-principles.md
│   ├── 02-title-and-metadata.md
│   ├── 03-introduction.md
│   ├── 04-methodology.md
│   ├── 05-findings.md
│   ├── 06-conclusion.md
│   └── 07-references.md
├── Figures/                           # NEW (3 files)
│   ├── 01-figure-standards.md
│   ├── 02-figure-types.md
│   └── 03-figure-examples.md
├── Tables/                            # NEW (3 files)
│   ├── 01-table-standards.md
│   ├── 02-table-types.md
│   └── 03-table-examples.md
├── Mathematics/                       # NEW (3 files)
│   ├── 01-equation-formatting.md
│   ├── 02-notation-conventions.md
│   └── 03-math-examples.md
├── Reviewer Expectations/             # NEW (3 files)
│   ├── 01-reviewer-criteria.md
│   ├── 02-rejection-patterns.md
│   └── 03-strengthening-paper.md
├── Examples/                          # NEW (6 files)
│   ├── 01-title-examples.md
│   ├── 02-introduction-examples.md
│   ├── 03-methodology-examples.md
│   ├── 04-findings-examples.md
│   ├── 05-conclusion-examples.md
│   └── 06-reference-examples.md
├── Checklists/                        # NEW (3 files)
│   ├── 01-pre-submission.md
│   ├── 02-per-domain.md
│   └── 03-final-review.md
├── Common Mistakes/                   # NEW (4 files)
│   ├── 01-formatting-mistakes.md
│   ├── 02-content-mistakes.md
│   ├── 03-citation-mistakes.md
│   └── 04-language-mistakes.md
└── Assets/                            # NEW (3 files)
    ├── 01-font-reference.md
    ├── 02-spacing-reference.md
    └── 03-style-card.md
```

---

## 3. Implementation Phases

**Phase 1**: Verify template extraction completeness (from existing `Conference Guidelines/`)
**Phase 2**: Analyze 11 sample papers (requires PDF reading — blocking step)
**Phase 3**: Write all 30 guide files (depends on Phases 1+2)
**Phase 4**: Fill `guide/README.md` skeleton
**Phase 5**: Fix 2 filename anomalies

Phases 1 & 2 are parallel. Phase 3 depends on both. Phases 4 & 5 are independent.

---

## 4. Source Attribution

Every guide file traces content to a source:
- `Conference Guidelines/` → "Source: PCEMS 2026 Template"
- `philosophy.md` → "Source: PCEMS Publication Philosophy"
- `documentation-standards/` → "Source: [Domain] Documentation Standard"
- `audit/semantic/document/` → "Source: [Domain] Semantic Audit Rubric"
- Sample papers → "Source: [Paper Title]"

---

## 5. Questions for User

1. **Sample papers**: Can you provide text extractions from the 11 PDFs, or should I try Python PDF libraries?
2. **Template completeness**: Is the existing `Conference Guidelines/` extraction complete?
3. **Writing tone**: Formal engineering (like `philosophy.md`) or instructional/approachable?
4. **Examples**: Only from sample papers, or can I construct illustrative examples?
5. **LaTeX**: Word-only or also cover LaTeX formatting?
