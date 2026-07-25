# Body — Generation Template

> **Domain:** product-guide
> **Section:** body
> **Source:** `documentation-standards/16-product-guide-standards.md` §Content
> **Relationships:** `audit/deterministic/document/16-product-guide-relationships.yaml`

Generate the Body section for a Product Guide document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| (none) | — | Body describes the shipped product — no formal derivation relationships |

## Template

```markdown
## [Feature or Workflow Name]

[1-2 sentences explaining what this feature does and when to use it.]

### How It Works

[Step-by-step instructions or explanation with concrete examples.]

### Examples

[Concrete usage examples showing expected input and output.]
```

**Required subsections:** How It Works, Examples
**Optional subsections:** Tips, Troubleshooting, Limitations

## Examples

**Correct:**
> ## Configure Automatic Backups
>
> Backups run daily at 02:00 by default. You can change the schedule or target directory.
>
> ### How It Works
>
> The backup service reads the `[backup]` section in your config file and writes compressed snapshots to the specified directory.
>
> ### Examples
>
> Run `app backup --now` to trigger an immediate backup. Output: `Backup saved to /data/backups/2026-07-11.snap`.

**Incorrect:**
> ## Backup
>
> The backup feature is very powerful and supports many use cases. See the source code for details on how it works internally.
> *Why wrong: No How It Works or Examples subsections, references source code instead of providing actionable user instructions, and lacks concrete examples.*

## Writing Guidance

- **Tone:** conversational
- **Voice:** second person
- **Structure:** mixed
- **Audience:** AI agent
- **Do:** Start with the user's goal in one sentence before explaining how; provide at least one concrete command or code example with expected output; use headers (How It Works, Examples) to make the content scannable
- **Don't:** Write long paragraphs without subheadings; reference source code, internal architecture, or implementation details; use passive constructions that obscure who performs the action

**Minimum content:** 2 subsections
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** none

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
