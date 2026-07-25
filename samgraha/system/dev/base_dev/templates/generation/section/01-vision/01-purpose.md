# Purpose — Generation Template

> **Domain:** vision
> **Section:** purpose
> **Source:** `documentation-standards/01-vision-standards.md` §Purpose
> **Relationships:** `audit/deterministic/document/01-vision-relationships.yaml`

Generate the Purpose section for a Vision document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | philosophy / purpose | Purpose's statement of why the product exists must inspire Philosophy's purpose section |
| `derives_from` | vision_statement (self) | Purpose must be consistent with the Vision Statement — same product, same identity |

## Template

```markdown
[One sentence stating why the product exists and the problem it addresses]
[One sentence stating the intended value or outcome for users]
[One sentence reinforcing the core identity of the product]
```

## Examples

**Correct:**
> DataSync exists to help teams move information between systems without manual intervention, eliminating hours of repetitive data entry each week. DataSync is the bridge that turns fragmented data into a single source of truth.

**Incorrect:**
> DataSync is a Python-based ETL pipeline using Apache Airflow that runs daily cron jobs to sync PostgreSQL databases via REST APIs.
> *Why wrong: Contains implementation details (technology stack, scheduling mechanism, protocol) that belong in downstream documentation, not in the Purpose section.*

## Writing Guidance

- **Tone:** inspirational
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** new contributor
- **Do:** Write from the user's world, not the engineer's; anchor the purpose in the problem space; keep the language stable enough to survive technology changes
- **Don't:** Name programming languages, frameworks, or infrastructure; describe what the product does or how it works; use jargon that requires domain expertise to understand

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
