# Success Criteria — Generation Template

> **Domain:** vision
> **Section:** success_criteria
> **Source:** `documentation-standards/01-vision-standards.md` §Success Criteria
> **Relationships:** `audit/deterministic/document/01-vision-relationships.yaml`

Generate the Success Criteria section for a Vision document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `traceable_to` | feature / acceptance_criteria | Vision success criteria must be traceable to Feature acceptance criteria — product-level outcomes map to feature-level verifications |

## Template

```markdown
* [Observable outcome tied to the Vision — what success looks like]
* [Observable outcome tied to the Vision — what success looks like]
* [Observable outcome tied to the Vision — what success looks like]
```

## Examples

**Correct:**
> * Teams report spending less than 2 hours per week on data reconciliation tasks.
> * At least 80% of new data flows are set up without engineering support.
> * Data delivered through the product is accurate 99.9% of the time as verified by audits.

**Incorrect:**
> * The API response time is under 200ms.
> * The test suite achieves 95% code coverage.
> * Deployment frequency increases to daily releases.
> *Why wrong: Describes implementation-level metrics (performance, test coverage, release cadence) rather than observable outcomes tied to the Vision and product purpose.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** bullet lists
- **Audience:** product owner
- **Do:** Write each criterion as a measurable or evaluable outcome; tie every criterion directly to the Vision statement; use concrete units of measure where possible
- **Don't:** Describe technical benchmarks like latency or throughput; include test coverage or deployment frequency; list more than six criteria

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Vision, Purpose

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
