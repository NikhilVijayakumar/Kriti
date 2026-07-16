# Product Context — Generation Template

> **Domain:** product-guide
> **Section:** product_context
> **Source:** `documentation-standards/16-product-guide-standards.md` §Product Context
> **Relationships:** `audit/deterministic/document/16-product-guide-relationships.yaml`

Generate the Product Context section for a Product Guide document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / purpose | Product Context must align with Vision(01) product purpose and version history |

## Template

```markdown
## Product Context

[Prerequisites, default behavior, and version-specific context the reader needs before using this feature.]

- **Prerequisites:** [What must already be installed or configured]
- **Default behavior:** [What happens if the user doesn't specify options]
- **Version:** [Applicable product version, if version-specific]
```

## Examples

**Correct:**
> - **Prerequisites:** App Server v2.0 or later must be installed
> - **Default behavior:** Backups run daily at 02:00 to the default directory
> - **Version:** Behavior changed in v2.3 — earlier versions require manual scheduling

**Incorrect:**
> Backup is a useful feature that helps protect your data. It was introduced in v1.0 and has been improved many times since then.
> *Why wrong: Reads like marketing copy — does not state prerequisites, defaults, or version-specific context the reader needs before using the feature.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** new contributor
- **Do:** List prerequisites as explicit bullet points with exact version numbers; state the default behavior concisely so the reader knows what happens without intervention; note any version-specific behavioral changes
- **Don't:** Write promotional or historical prose ("has been improved many times"); omit minimum version requirements; mix aspirational language with factual prerequisites

**Minimum content:** 1 paragraph
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** none

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
