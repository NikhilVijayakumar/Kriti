# Vision Statement — Generation Template

> **Domain:** vision
> **Section:** vision_statement
> **Source:** `documentation-standards/01-vision-standards.md` §Vision
> **Relationships:** `audit/deterministic/document/01-vision-relationships.yaml`

Generate the Vision Statement section for a Vision document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | philosophy / vision_alignment | Vision Statement must inspire Philosophy's alignment with product direction |
| `derives_from` | feature / purpose | Vision Statement must inspire each Feature's purpose — features derive from vision |
| `derives_from` | security / purpose | Vision Statement must inform what the product is, which determines what Security defends |

## Template

```markdown
[Aspirational statement describing the desired future state of the product]
[What the product will enable or become once fully realized]
```

## Examples

**Correct:**
> CloudBridge will become the trusted backbone for cross-organization data exchange, where any team can connect to any data source within minutes and trust that the information is accurate and current.

**Incorrect:**
> CloudBridge will migrate from REST to GraphQL by Q3, reaching 10,000 API calls per second with sub-50ms latency on AWS.
> *Why wrong: Describes a technology roadmap with specific implementation targets (latency, throughput, cloud provider) rather than an aspirational future state.*

## Writing Guidance

- **Tone:** inspirational
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** Paint a vivid picture of the fully realized product state; write in the future tense with aspirational language; tie the vision back to the Purpose section's "why"
- **Don't:** Mention specific technologies, release timelines, or implementation milestones; describe current product state or features; use metrics or benchmarks that belong in Success Criteria

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Purpose

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
