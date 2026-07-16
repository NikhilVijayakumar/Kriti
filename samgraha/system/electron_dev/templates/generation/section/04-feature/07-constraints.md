# Constraints — Generation Template

> **Domain:** feature
> **Section:** constraints
> **Source:** `documentation-standards/04-feature-standards.md` §Constraints
> **Relationships:** `audit/deterministic/document/04-feature-relationships.yaml`

Generate the Constraints section for a Feature document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `constrains` | philosophy / guiding_principles | Constraints must be consistent with Philosophy — constraints narrow scope without contradicting guiding principles |

## Template

```markdown
## Constraints

> **semantic_type:** `constraints`
> **scope:** [Limitations the feature must operate within]
> **out_of_scope:** [Implementation details excluded]
> **contributes:** [How this feeds downstream design]
> **relationships:** [Upstream and downstream connections]
> **responsibilities:** [What this section must capture]
> **generation_rules:** [Rules for authoring this section]
> **enhancement_rules:** [Rules for improving this section]
> **validation_rules:** [Criteria for section completeness]
> **audit_rules:** [Audit expectations]

### Regulatory
- [C-001] [Regulatory constraint and its impact on the feature]

### Business
- [C-002] [Business constraint and its impact on the feature]

### Technical
- [C-003] [Technical constraint and its impact on the feature]
```

## Examples

**Correct:**
> ### Regulatory
> - [C-001] CloudBridge must comply with data residency requirements that restrict cross-border data transfer.
>
> ### Business
> - [C-002] CloudBridge must complete synchronization within the agreed maintenance window of 4 hours.

**Incorrect:**
> ### Regulatory
> - [C-001] CloudBridge must use AES-256 encryption at rest and TLS 1.3 in transit per compliance requirements.
>
> ### Technical
> - [C-002] CloudBridge must run on Kubernetes pods with a minimum of 2 GB memory and 1 CPU core.
> *Why wrong: The first constraint specifies a particular encryption standard rather than stating the regulatory requirement it serves. The second constraint specifies infrastructure requirements that belong in Architecture or Engineering Documentation.*

## Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Categorize each constraint by type (Regulatory, Business, Technical); state the limitation clearly without prescribing a solution; reference the regulatory or business origin of each constraint
- **Don't:** Specify particular technologies, frameworks, or vendor solutions; describe infrastructure requirements or performance benchmarks; include implementation workarounds or mitigation strategies

**Required subsections:** none
**Optional subsections:** Regulatory, Business, Technical
**Required diagrams:** none
**Required cross-references:** External Context, Acceptance Criteria

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
