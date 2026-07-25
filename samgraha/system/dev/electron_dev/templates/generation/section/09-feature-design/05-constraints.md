# Constraints — Generation Template

> **Domain:** feature-design
> **Section:** constraints
> **Source:** `documentation-standards/09-feature-design-standards.md` §Constraints
> **Relationships:** `audit/deterministic/document/09-feature-design-relationships.yaml`

Generate the Constraints section for a Feature Design document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `constrains` | feature-technical / runtime_constraints | Constraints defined here must be respected by Feature Technical Design's runtime constraints |
| `derives_from` | design / constraints | Constraints must apply Design Documentation's constraint principles |

## Template

```markdown
## Constraints

> **semantic_type:** `constraints`
> **scope:** [what constraint concerns this section covers]
> **out_of_scope:** [what constraint concerns are excluded]
> **contributes:** [how this section feeds downstream documents]
> **relationships:** [which upstream documents this derives from]
> **responsibilities:** [what this section is responsible for defining]
> **generation_rules:** [rules for generating this section]
> **enhancement_rules:** [rules for improving this section]
> **validation_rules:** [rules for validating this section]
> **audit_rules:** [rules for auditing this section]

| Constraint | Type | Source | Impact on Design |
|-----------|------|--------|-----------------|
| [description] | Hard/Advisory | [External Context source] | [what it prevents or requires] |
| ... | ... | ... | ... |
```

## Examples

**Correct:**
> | Constraint | Type | Source | Impact on Design |
> |-----------|------|--------|-----------------|
> | Maximum password length is 128 characters | Hard | Platform Security Policy | Input field must accept and display up to 128 characters without truncation |
> | Feature must support right-to-left text | Hard | Localization Requirements | Layout must mirror for RTL locales; labels and icons must flip alignment |
> | Dark mode support is preferred but not mandatory | Advisory | Design System Guidelines | Color choices should work in both themes if feasible |

**Incorrect:**
> | Constraint | Type | Source | Impact on Design |
> |-----------|------|--------|-----------------|
> | Use `maxlength="128"` on the input element | Hard | HTML spec | Input validation in the DOM layer |
> | Must use CSS `direction: rtl` for Arabic | Hard | W3C CSS spec | Stylesheet must set text direction |
> *Why wrong: describes implementation techniques (HTML attributes, CSS properties) rather than user-facing design constraints.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables
- **Audience:** architect
- **Do:** Cite the source of every constraint; distinguish hard constraints from advisory preferences; state the concrete impact on design decisions
- **Don't:** Describe implementation techniques (HTML attributes, CSS properties); omit source attribution; conflate constraints with implementation preferences

**Minimum content:** constraint list with sources
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** External Context, Platform requirements

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
