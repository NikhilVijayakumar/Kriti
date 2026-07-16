# End-to-End Testing — Generation Template

> **Domain:** qa
> **Section:** e2e_testing
> **Source:** `documentation-standards/12-qa-standards.md` §End-to-End Testing
> **Relationships:** `audit/deterministic/document/12-qa-relationships.yaml`

Generate the End-to-End Testing section for a QA document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | design / workflow | Critical user journeys must map to Design workflows |
| `derives_from` | feature / purpose | Pass/fail criteria must trace to Feature requirements |

## Template

```markdown
## End-to-End Testing

### Critical User Journeys

| Journey | Design Reference | Expected Outcome | Pass/Fail Criteria |
|---------|-----------------|------------------|-------------------|
| [Journey 1] | Design(06) §[section] | [Expected result] | [Measurable criteria] |

### Journey Flowchart
[Flowchart showing happy path and critical edge cases]
```

## Examples

**Correct:**
> ### Critical User Journeys
>
> | Journey | Design Reference | Expected Outcome | Pass/Fail Criteria |
> |---------|-----------------|------------------|-------------------|
> | New user registration | Design(06) §Onboarding Flow | User receives confirmation email within 60s; profile created | HTTP 200 response; email sent; DB row exists |
> | Complete purchase | Design(06) §Checkout | Order created; payment processed; confirmation displayed | Order ID returned; payment status "success" |

**Incorrect:**
> Test that users can log in, add items to cart, and check out. Make sure the UI works.
> *Why wrong: critical user journeys must be mapped to specific Design(06) references with measurable pass/fail criteria.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** Link each journey to a specific Design(06) section; define expected outcomes as observable system states; write pass/fail criteria as automated assertions
- **Don't:** List journeys without a Design(06) reference; describe expected outcomes in user-emotion terms; leave pass/fail criteria implicit

**Required subsections:** Critical User Journeys table
**Optional subsections:** none
**Required diagrams:** flowchart of user journey paths
**Required cross-references:** Design(06), Feature(04), Implementation(13)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
