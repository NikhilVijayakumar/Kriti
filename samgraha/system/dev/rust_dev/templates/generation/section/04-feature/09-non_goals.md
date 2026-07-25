# Non-Goals — Generation Template

> **Domain:** feature
> **Section:** non_goals
> **Source:** `documentation-standards/04-feature-standards.md` §Non-Goals
> **Relationships:** `audit/deterministic/document/04-feature-relationships.yaml`

Generate the Non-Goals section for a Feature document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `constrains` | philosophy / guiding_principles | Non-goals must respect Philosophy guiding principles — exclusions must not contradict product values |

## Template

```markdown
## Non-Goals

> **semantic_type:** `non_goals`
> **scope:** [What this feature explicitly does not define]
> **out_of_scope:** [Positive framing of intent excluded]
> **contributes:** [How this prevents scope creep]
> **relationships:** [Upstream and downstream connections]
> **responsibilities:** [What this section must capture]
> **generation_rules:** [Rules for authoring this section]
> **enhancement_rules:** [Rules for improving this section]
> **validation_rules:** [Criteria for section completeness]
> **audit_rules:** [Audit expectations]

Feature Documentation does not define:

* [Non-goal] — belongs to [owning standard].
* [Non-goal] — belongs to [owning standard].
* [Non-goal] — belongs to [owning standard].
```

## Examples

**Correct:**
> Feature Documentation does not define:
> * How CloudBridge implements conflict resolution — belongs to Feature Technical Design.
> * Which programming language CloudBridge is built with — belongs to Engineering Documentation.
> * The API contract for CloudBridge endpoints — belongs to Feature Technical Design.

**Incorrect:**
> Feature Documentation does not define:
> * Database schema design — this is handled in the backend.
> * Deployment configuration — this is handled in DevOps.
> * Unit test implementation — this is handled by QA.
> *Why wrong: The exclusions fail to name the specific owning standard for each responsibility, making it unclear which documentation standard owns each excluded item. Vague attribution prevents traceability.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** product owner
- **Do:** Name the specific owning standard for each excluded responsibility; invert the Goals list to derive exclusions; state what Feature Documentation explicitly does not define
- **Don't:** Use vague ownership like "handled by the backend" or "handled by DevOps"; list exclusions without naming the owning standard; include items that actually belong within Feature Documentation scope

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Goals

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
