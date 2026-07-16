# fastapi_dev — Gap Analysis: Backend Standards Appended, Not Integrated

**Category:** Gaps / Content Quality  
**Severity:** Medium  
**Date:** 2026-07-15

---

## Summary

The backend-specific content added to `documentation-standards/` files was appended to the **bottom** of each document as a new section. This means:

1. The table of contents at the top of each file **does not reference** the new sections.
2. The new backend sections do not reference any structural audit rules (no `> *Structural rules: ...*` directive).
3. The new sections are **not wired into templates** — the generation templates don't know about the backend-specific additions.
4. The backend sections feel "bolted on" rather than being integrated into the document's information architecture.

---

## Specific Examples

### `documentation-standards/05-architecture-standards.md`

The appended section at line 1035:
```markdown
## Backend Architecture Considerations
For backend systems, the architecture must explicitly address:
* **Layered Architecture:** ...
```

**Issues:**
- Not in the Table of Contents (which ends at line 42 with `Quality Requirements`)
- No structural rule reference (missing `> *Structural rules: ...*.yaml`)
- No template/examples/writing guidance subsections matching the pattern used in all other sections
- The content is written as prose bullets, not as the structured template+examples+guidance format used throughout the rest of the file

---

### `documentation-standards/07-engineering-standards.md`

The appended section at line 971:
```markdown
## Backend Engineering Practices
When engineering backend systems (particularly with Python/FastAPI), standards must dictate:
```

**Issues:**
- Not in the Table of Contents
- Says "particularly with Python/FastAPI" — this is a mild form of technology name leaking into the standard itself (acceptable but inconsistent with the proposal's principle of generalized standards)
- No structural rule reference
- No Correct/Incorrect examples
- No writing guidance block

---

### Pattern Violation Across All Appended Sections

Every other section in these files follows a consistent pattern:
```
## Section Name
> *Structural rules: `audit/deterministic/section/{domain}/{NN-name}.yaml`*

### Template
> **minimum_content:** ...
> **length_guidance:** ...
> **diagram_requirements:** ...
[template content]

### Examples
**Correct:** ...
**Incorrect:** ...

### Writing Guidance
- **Tone:** ...
- **Voice:** ...
```

None of the appended backend sections follow this pattern.

---

## Fix Required

For every appended backend section across all affected standards files:

1. Add the section to the **Table of Contents** at the top of the file.
2. Add a `> *Structural rules: ...*.yaml` directive (or create the corresponding deterministic rule file).
3. Replace the prose bullet list with the proper **Template + Examples + Writing Guidance** structure.
4. Remove direct technology name references where possible (e.g., "Python/FastAPI" → "the backend framework").
5. Cross-reference the corresponding generation template slot.

---

## Affected Files

- `documentation-standards/01-vision-standards.md` — Backend System Vision section
- `documentation-standards/03-security-standards.md` — API Security Considerations section
- `documentation-standards/04-feature-standards.md` — Backend Feature Definition section
- `documentation-standards/05-architecture-standards.md` — Backend Architecture Considerations section
- `documentation-standards/07-engineering-standards.md` — Backend Engineering Practices section
- `documentation-standards/08-external-context-standards.md` — Backend Technology Categories section
- `documentation-standards/10-feature-technical-standards.md` — Layer-Specific Implementation Guidance section
- `documentation-standards/11-prototype-standards.md` — API Prototyping section
- `documentation-standards/12-qa-standards.md` — API Testing Strategy section
- `documentation-standards/13-implementation-standards.md` — Layer Implementation Patterns section
- `documentation-standards/14-build-standards.md` — Backend Build and Packaging section
- `documentation-standards/15-readme-standards.md` — Backend README Conventions section
- `documentation-standards/16-product-guide-standards.md` — Backend Development Workflow section
