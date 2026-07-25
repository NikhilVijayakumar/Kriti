# Generation Plan — Generation Template

> **Domain:** implementation
> **Section:** generation_plan
> **Source:** `documentation-standards/13-implementation-standards.md` §Generation Plan
> **Relationships:** `audit/deterministic/document/13-implementation-relationships.yaml`

Generate the Generation Plan section for an Implementation Plan document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature-technical / component_responsibilities | Generation Plan must implement component responsibilities defined in Feature Technical(10) |
| `derives_from` | engineering / code_standards | Generation Plan must follow code standards defined in Engineering(07) |
| `derives_from` | prototype / scope | Generation Plan must account for prototyping findings from Prototype(11) |

## Template

```markdown
## Generation Plan

### Inputs

| Upstream Document | Section | What It Provides |
|---|---|---|
| [Feature(04)] | [requirements section] | [what this plan extracts] |
| [Architecture(05)] | [constraints section] | [structural constraints applied] |
| [Engineering(07)] | [code standards] | [standards followed] |
| [Security(03)] | [requirements section] | [security requirements addressed] |

### Generation Sequence

1. [Step: verify/validate against upstream doc X]
2. [Step: implement component Y per Architecture(05)]
3. [Step: apply security constraint per Security(03)]
4. [Step: verify coding standards per Engineering(07)]

### Verification Checkpoints

| After Step | Check | Criteria | Source |
|---|---|---|---|
| [step number] | [what is verified] | [pass/fail criteria] | [upstream doc] |

### Deviation Recording

| Deviation | Upstream Source | Rationale | Impact |
|---|---|---|---|
| [what was deviated from] | [which upstream doc] | [why the deviation was made] | [effect on other components] |
```

## Examples

**Correct:**
> **Inputs:** Feature(04) notification requirements, Feature Design(09) alert UX mockups, Architecture(05) message queue topology, Engineering(07) async processing standards, Security(03) data-at-rest encryption.
> **Generation Sequence:** 1) Verify notification requirements against Feature(04). 2) Validate UX against Feature Design(09). 3) Implement message producer per Architecture(05) queue topology. 4) Apply encryption per Security(03). 5) Verify coding standards per Engineering(07).
> **Verification Checkpoints:** After step 2 — UX matches mockups. After step 5 — all unit tests pass, encryption verified.
> **Deviation Recording:** Deviated from Architecture(05) by using a persistent queue instead of in-memory; rationale: notification delivery must survive process restarts.

**Incorrect:**
> **Inputs:** None listed.
> **Generation Sequence:** Write code, test it, deploy it.
> **Verification Checkpoints:** None.
> **Deviation Recording:** None needed.
> *Why wrong: No upstream documents referenced, generation sequence lacks tier ordering, no verification checkpoints defined, and deviation recording is dismissed rather than established as a process.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** List every upstream document consumed in the Inputs subsection; number the generation sequence steps in tier order; specify exact verification criteria at each checkpoint
- **Don't:** Omit upstream document references; skip verification checkpoints; write generation steps without referencing which standard each satisfies

**Minimum content:** 4 subsections (Inputs, Generation Sequence, Verification Checkpoints, Deviation Recording)
**Length guidance:** extensive
**Required diagrams:** none
**Required cross-references:** Feature(04), Feature Design(09), Prototype(11), Architecture(05), Design(06), Engineering(07), External Context(08), Security(03)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
