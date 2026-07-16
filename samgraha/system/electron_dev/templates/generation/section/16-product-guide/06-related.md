# Related — Generation Template

> **Domain:** product-guide
> **Section:** related
> **Source:** `documentation-standards/16-product-guide-standards.md` §Related
> **Relationships:** `audit/deterministic/document/16-product-guide-relationships.yaml`

Generate the Related section for a Product Guide document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| (none) | — | Related provides cross-references to adjacent topics — no formal derivation relationships |

## Template

```markdown
## Related

- [Topic Name](link) — brief label explaining why this is relevant
```

## Examples

**Correct:**
> - [Scheduled Backups](scheduled-backups.md) — how to change the backup schedule
> - [Restore From Backup](restore-backup.md) — recovering data from a saved snapshot

**Incorrect:**
> - [Some Other Topic](broken-link.md)
> *Why wrong: Link target does not resolve, and the label gives no indication of why the reader should follow it.*

## Writing Guidance

- **Tone:** conversational
- **Voice:** second person
- **Structure:** bullet lists
- **Audience:** AI agent
- **Do:** Provide at least one cross-reference with a brief label explaining relevance; link to adjacent Product Guide topics the reader is likely to need next; keep labels descriptive enough to stand alone without context
- **Don't:** Include links without labels or with vague labels ("see also"); link to topics outside the Product Guide domain without clear relevance; duplicate content from the linked topic in the description

**Minimum content:** 1 link
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** at least one valid link with descriptive label

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
