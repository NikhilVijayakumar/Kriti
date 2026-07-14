# Data Model — Generation Template

> **Domain:** prototype
> **Section:** data_model
> **Source:** `documentation-standards/11-prototype-standards.md` §Data Model
> **Relationships:** `audit/deterministic/document/11-prototype-relationships.yaml`

Generate the Data Model section for a Prototype document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature-technical / component_responsibilities | Data structures must align with the feature's component responsibilities |

## Template

```markdown
## Data Model

```json
{
  "entity_name": {
    "field": "type — description"
  }
}
```

**Seed data:** [realistic but fake data, no PII or production values]

[Justification for included and excluded fields]
```

## Examples

**Correct:**
> ```json
> {
>   "order": {
>     "id": "string — unique order identifier",
>     "status": "string — pending | confirmed | shipped",
>     "total": "number — order total in cents"
>   }
> }
> ```
>
> **Seed data:** `{ "id": "ORD-001", "status": "pending", "total": 4999 }`
>
> Minimal structure exercises the checkout flow. No PII — customer name is not included because the prototype does not test profile management.

**Incorrect:**
> ```json
> {
>   "customer": {
>     "name": "string — full legal name",
>     "email": "string — personal email address",
>     "ssn": "string — social security number"
>   }
> }
> ```
>
> **Seed data:** `{ "name": "John Smith", "email": "john@example.com", "ssn": "123-45-6789" }`
> *Why wrong: contains PII fields and seed data uses realistic personal information.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Define only the fields the prototype scenario exercises; provide seed data that is realistic but entirely fake; explain why excluded fields are not in scope
- **Don't:** Include PII, real email addresses, or production identifiers; replicate the full production schema

**Minimum content:** 1 paragraph + schema or table
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Mock APIs

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
