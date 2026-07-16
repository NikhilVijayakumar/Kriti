# Change Request Plan — Generation Template

> **Domain:** implementation
> **Section:** change_request_plan
> **Source:** `documentation-standards/13-implementation-standards.md` §Change Request Plan
> **Relationships:** `audit/deterministic/document/13-implementation-relationships.yaml`

Generate the Change Request Plan section for an Implementation Plan document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature / purpose | Change must align with updated Feature(04) requirements |
| `derives_from` | feature-design / purpose | Change must align with updated Feature Design(09) UX |
| `traces_to` | qa / test_strategy | Impact analysis must reference QA(12) test updates |

## Template

```markdown
## Change Request Plan

### Change Description

**Before:** [current behavior]
**After:** [desired behavior]
**Trigger:** [stakeholder request, updated requirement, or discovered issue]

### Impact Analysis

| Affected Area | Upstream Doc | Impact | Action Required |
|---|---|---|---|
| [module/component] | [Feature(04), Feature Design(09), etc.] | [what changes] | [what to update] |

### Rollback Strategy

[How to revert the change if verification fails — including database migrations, feature flags, and deployment steps]
```

## Examples

**Correct:**
> **Change Description:** The checkout API response must now include a loyalty points balance field. Stakeholder request per updated Feature(04) requirements.
> **Impact Analysis:** Affects checkout API response schema, three frontend components consuming the response, QA(12) integration tests (8 tests need new assertions), and Feature Design(09) API documentation.
> **Rollback Strategy:** Deploy with feature flag disabled. If verification fails, toggle flag off — old response schema is restored with zero downtime. Database migration is additive only (new column), safe to leave in place.

**Incorrect:**
> **Change Description:** Add loyalty points to checkout.
> **Impact Analysis:** Should be straightforward.
> **Rollback Strategy:** Revert the commit.
> *Why wrong: Change description lacks specificity about what and why; impact analysis is vague with no affected modules or tests identified; rollback strategy does not account for database migrations or frontend deployments.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Describe the exact behavior change with before/after state; list every affected module, API endpoint, and test case in impact analysis; define a rollback strategy that accounts for database migrations and feature flags
- **Don't:** Write vague change descriptions like "improve X"; skip the impact analysis or list no affected components; assume rollback is just "revert the commit"

**Minimum content:** 3 subsections (Change Description, Impact Analysis, Rollback Strategy)
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Feature(04), Feature Design(09), QA(12)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
