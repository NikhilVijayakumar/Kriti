# rust_dev — Gap Analysis: Template Content Depth vs. Base_Dev Templates

**Category:** Gaps / Content Quality  
**Severity:** Medium  
**Date:** 2026-07-15

---

## Summary

While the 12 new Rust-specific generation templates are well-formed and far better than the single-line stubs that existed previously, they are structurally **thinner** than the mature base_dev templates in the same directories. The base_dev templates (e.g., `01-purpose.md` at 4,088 bytes with 70 lines) contain: a full YAML front-matter header, Relationship tables, an `## Audit Fix` block, and a Generation Note. The new Rust templates are missing ALL of these standard elements.

---

## Evidence — Structural Comparison

**Reference template (`01-purpose.md`, 4,088 bytes)** contains:
```markdown
# Purpose — Generation Template

> **Domain:** architecture
> **Section:** purpose
> **Source:** `documentation-standards/05-architecture-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/05-architecture-relationships.yaml`

Generate the Purpose section for an Architecture document.

## Relationships

This section has the following outgoing relationships...

## Template

...

> **Generation note:** [note for LLM agents]

## Examples

...

## Writing Guidance

...

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
```

**New Rust template (`12-crate_architecture.md`, 1,614 bytes)** contains:
```markdown
## Crate Architecture

> *Structural rules: `audit/deterministic/section/05-architecture/12-crate_architecture.yaml`*

### Template
...

### Examples
...

### Writing Guidance
...
```

---

## Gap 1 — Missing YAML Front-Matter Header Block

**Affected:** All 12 new Rust templates (`05-architecture/12-*`, `05-architecture/13-*`, `07-engineering/09-*` through `11-*`, `10-feature-technical/18-*`, `10-feature-technical/19-*`, `12-qa/10-*`, `12-qa/11-*`, `13-implementation/08-*`, `14-build/10-*`, `16-product-guide/07-*`)

All new templates are missing the header block that tells the generation agent what domain, section, and standard this template belongs to:
```markdown
> **Domain:** [domain]
> **Section:** [section_name]
> **Source:** `documentation-standards/NN-xxx-standards.md` §SectionName
> **Relationships:** `audit/deterministic/document/NN-xxx-relationships.yaml`
```

**Fix Required:**
- Add the header block to all 12 new Rust generation templates.

---

## Gap 2 — Missing `## Relationships` Table

**Affected:** All 12 new Rust templates

Base_dev templates include a `## Relationships` table that shows what each section derives from or must align with. This is important for generation agents that build documents in dependency order. None of the 12 new Rust templates declare their relationships.

**Fix Required:**
- Add a `## Relationships` table to each new Rust template, showing upstream dependencies (e.g., `Crate Architecture derives from Component Model(03)`).

---

## Gap 3 — Missing `> **Generation note:**` Block

**Affected:** All 12 new Rust templates

Some base_dev templates include a `Generation note` that provides important clarification to LLM agents about what context is system-specific vs. meta-level. The new templates have no such guidance.

**Fix Required:**
- Add a `Generation note` to templates where the section could be confused with a meta-level definition vs. a system-specific fill-in (e.g., `18-crate_implementation.md`).

---

## Gap 4 — Missing `## Audit Fix` Stub

**Affected:** All 12 new Rust templates

Base_dev templates end with:
```markdown
## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
```

This placeholder links the generation template back to the audit pipeline, enabling future auto-fix workflows. The new Rust templates are missing this integration hook.

**Fix Required:**
- Add the `## Audit Fix` stub to all 12 new Rust generation templates.

---

## Gap 5 — Top-Level H1 Heading Format Is Inconsistent

**Affected:** All 12 new Rust templates

Base_dev templates use:
```markdown
# [Section Name] — Generation Template
```

New Rust templates use:
```markdown
## [Section Name]
```

This uses an H2 instead of H1, making templates look like nested subsections rather than top-level documents when viewed in isolation.

**Fix Required:**
- Change the top-level heading in all 12 new Rust templates from `##` to `# [Section Name] — Generation Template`.
