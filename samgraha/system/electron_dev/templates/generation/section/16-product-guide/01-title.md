# Title — Generation Template

> **Domain:** product-guide
> **Section:** title
> **Source:** `documentation-standards/16-product-guide-standards.md` §Title
> **Relationships:** `audit/deterministic/document/16-product-guide-relationships.yaml`

Generate the Title section for a Product Guide document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| (none) | — | Title is self-contained — no outgoing relationships |

## Template

```markdown
# [Command or Concept Name]
```

## Examples

**Correct:**
> # Configure Automatic Backups

**Incorrect:**
> # The Backup System — Everything You Need To Know
> *Why wrong: Over 60 characters, uses marketing language, and tries to be a catch-all instead of naming the specific command or concept.*

## Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Use the exact command name or concept name as written in the shipped product; keep under 60 characters; describe the action, not the system
- **Don't:** Use marketing adjectives or superlatives ("Everything You Need To Know"); include parenthetical qualifiers or version numbers in the title; use "How to" prefix when the command name already implies action

**Minimum content:** 1 line
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** none

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
