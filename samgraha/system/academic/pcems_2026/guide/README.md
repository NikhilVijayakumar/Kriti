# PCEMS Publication Knowledge Base

## Purpose

This knowledge base provides comprehensive guidance for writing, formatting, and submitting manuscripts to the PCEMS 2026 conference. It serves as a single source of truth for authors, reviewers, and AI writing assistants.

## Scope

Covers the complete manuscript lifecycle:
- Understanding conference requirements
- Structuring and writing each section
- Formatting figures, tables, and equations
- Avoiding common mistakes
- Preparing for review and submission

## Target Audience

- **Authors**: Researchers preparing PCEMS 2026 submissions
- **Reviewers**: Evaluating manuscript quality and compliance
- **AI Systems**: Writing assistants generating or reviewing manuscript content

## Knowledge Base Organization

```
guide/
├── README.md                          # This file
├── Conference Guidelines/             # Template requirements (extracted from PDF)
├── Philosophy/                        # Writing philosophy and principles
├── Writing Guide/                     # Per-section writing guidance
├── Figures/                           # Figure standards, types, examples
├── Tables/                            # Table standards, types, examples
├── Mathematics/                       # Equation formatting, notation
├── Reviewer Expectations/             # What reviewers evaluate
├── Examples/                          # Annotated excerpts from sample papers
├── Checklists/                        # Pre-submission verification
├── Common Mistakes/                   # Anti-patterns with corrections
└── Assets/                            # Quick reference cards
```

## Document Categories

### Philosophy
Core writing methodology and principles. Read this first to understand the approach.

### Conference Guidelines
Extracted from the PCEMS 2026 template PDF. Contains formatting specifications, submission requirements, and manuscript structure rules. These are mandatory.

### Writing Guide
Section-by-section guidance for writing each part of the manuscript. Includes word count targets, structural templates, and quality criteria.

### Figures
Standards for creating, labeling, and placing figures. Covers block diagrams, charts, photographs, and flowcharts.

### Tables
Standards for creating and formatting tables. Emphasizes Word-native tables over images.

### Mathematics
Equation formatting, notation conventions, and mathematical writing guidance.

### Reviewer Expectations
What reviewers evaluate, common rejection reasons, and strategies for strengthening papers.

### Examples
Annotated excerpts from 11 accepted PCEMS 2026 sample papers. Shows effective patterns with analysis.

### Checklists
Pre-submission, per-domain, and final review checklists. Complete every item before submission.

### Common Mistakes
Anti-patterns in formatting, content, citations, and language. Each mistake includes a correction.

### Assets
Quick reference cards for fonts, spacing, and overall style. Print and keep visible while writing.

## Recommended Workflow

1. **Read Philosophy** (15 minutes): Understand the writing approach
2. **Review Conference Guidelines** (10 minutes): Know the requirements
3. **Consult Writing Guide** (as needed): Write each section
4. **Use Figures/Tables/Mathematics** (as needed): Format visual elements
5. **Check Examples** (as needed): See effective patterns from accepted papers
6. **Avoid Common Mistakes** (as needed): Prevent known anti-patterns
7. **Complete Checklists** (before submission): Verify compliance
8. **Review Style Card** (final pass): Quick compliance check

## Design Principles

### Source Attribution
Every document traces its content to a source:
- Conference Guidelines → PCEMS 2026 Template
- Philosophy → PCEMS Publication Philosophy
- Writing Guide → Template + Sample Paper Analysis
- Examples → Accepted Sample Papers
- Checklists → Template + Conference Guidelines

### Evidence-Based
Recommendations are grounded in analysis of 11 accepted PCEMS 2026 sample papers, not assumptions.

### Actionable
Every document provides specific, implementable guidance rather than abstract advice.

### Cross-Referenced
Documents reference each other where content overlaps or depends.

## Relationship with Research Projects

This knowledge base is a **writing resource**, not a research resource. It organizes publication knowledge, not research knowledge. Research projects use this guide when preparing manuscripts for submission.

## Relationship with AI Systems

AI writing assistants should:
1. Load relevant guide sections before generating content
2. Follow formatting specifications from Assets/
3. Avoid anti-patterns from Common Mistakes/
4. Verify compliance using Checklists/

## Extensibility

New sections can be added as:
- Additional sample papers are analyzed
- New domains are added to the conference
- Template requirements change
- Reviewer feedback identifies new patterns

## System Registration

pcems_2026 is a samgraha knowledge standard. To use it with samgraha:

### Prerequisites
- samgraha installed (`pip install samgraha` or from source)
- A target repo with documentation (the paper source)

### Two-Stage Activation

```bash
# 1. Register the standard globally (one-time, per machine)
samgraha register-standard-global /path/to/pcems_2026

# 2. Activate in a target repo (creates .samgraha/knowledge.db)
samgraha register-standard /path/to/target-repo pcems_2026
```

### Key Files
- `script/schema/standard.yaml` — machine-readable manifest (samgraha reads this)
- `script/seeder.py` — populates knowledge.db with domains, scripts, prompts, usecases
- `standard.metadata.json` — declares 22 custom academic_* tables
- `script/smoke_test.py` — structural validation (no API keys needed)

### Verification
```bash
# Run smoke test
python script/smoke_test.py --repo-root /path/to/pcems_2026

# Run seeder against a test repo
samgraha run-script /path/to/target-repo pcems_2026 schema-init
```

## Summary

This knowledge base contains 30+ documents covering every aspect of PCEMS manuscript preparation. Use it systematically to produce publication-ready manuscripts that meet all conference requirements.
