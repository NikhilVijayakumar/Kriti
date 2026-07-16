# Purpose — Generation Template

> **Domain:** design
> **Section:** purpose
> **Source:** `documentation-standards/06-design-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/06-design-relationships.yaml`

Generate the Purpose section for a Design document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `guided_by` | philosophy / guiding_principles | Design Purpose must align with the product's guiding philosophy |

## Template

```markdown
## Purpose

[1 paragraph: problem statement — what Design Documentation solves and why it exists]

[1 paragraph: scope — what it defines and what it does not; distinction from Feature Design]
```

## Examples

**Correct:**
> Design Documentation solves the problem of inconsistent design across features by establishing reusable design principles, interaction philosophy, and UX standards that govern an entire product ecosystem. It defines how products should be designed at the product level — not how individual features behave.

**Incorrect:**
> Design Documentation defines the checkout flow for the payment module, including screen layouts and button placement for the order form.
> *Why wrong: This describes a feature-specific workflow, not a product-level design standard. Design Documentation must not contain feature-specific content.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** State the problem Design Documentation solves before describing what it defines. Distinguish Design Documentation from Feature Design explicitly. Keep scope boundaries firm and technology-free.
- **Don't:** List specific features or products. Reference implementation technologies or frameworks. Describe how individual features behave.

**Generation Note:** When generating for a specific system, replace the generic problem statement with the specific design inconsistency this system faces. Do NOT write meta-level language about documentation types.

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Vision, Feature Design Standard

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
