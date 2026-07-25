# Outputs — Generation Template

> **Domain:** feature
> **Section:** outputs
> **Source:** `documentation-standards/04-feature-standards.md` §Outputs
> **Relationships:** `audit/deterministic/document/04-feature-relationships.yaml`

Generate the Outputs section for a Feature document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature_technical / testing_strategy | Feature Technical Design acceptance criteria derive from Feature acceptance criteria |

## Template

```markdown
Feature Documentation provides direction for:

* [Consumer Name] — [nature of dependency]
* [Consumer Name] — [nature of dependency]
```

## Examples

**Correct:**
> Feature Documentation provides direction for:
> * Feature Design — derives user experience and interaction patterns from feature requirements
> * Feature Technical Design — derives technical specifications from functional requirements
> * Testing — derives test cases from acceptance criteria and business rules

**Incorrect:**
> Feature Documentation provides direction for:
> * Source code — the codebase reads feature docs to generate implementation
> * Deployment pipeline — CI/CD reads feature specs to configure infrastructure
> *Why wrong: Source code and deployment pipelines are not documentation standards. They are implementation artifacts that belong downstream of Feature Documentation, not consumers within the documentation ecosystem.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** List each downstream consumer by name and standard number; state what each consumer derives from Feature Documentation; include Testing and Validation as consumers when acceptance criteria exist
- **Don't:** List upstream standards as consumers; omit the nature of the dependency for each consumer; include implementation artifacts like source code or deployment pipelines as consumers

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Traceability

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
