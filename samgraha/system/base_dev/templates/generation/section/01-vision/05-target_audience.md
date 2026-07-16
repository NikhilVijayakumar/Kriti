# Target Audience — Generation Template

> **Domain:** vision
> **Section:** target_audience
> **Source:** `documentation-standards/01-vision-standards.md` §Target Audience
> **Relationships:** `audit/deterministic/document/01-vision-relationships.yaml`

Generate the Target Audience section for a Vision document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `informs` | philosophy / user_model | Target Audience's description of users by goals and needs must inform Philosophy's understanding of who the product serves |

## Template

```markdown
[Description of the intended users or consumers by their goals and needs]
[Who benefits from the product and who makes adoption decisions]
[What the audience expects or requires from the product]
```

## Examples

**Correct:**
> CloudBridge serves operations teams who need to consolidate data from multiple sources into a single, reliable view. These teams prioritize accuracy and speed over technical flexibility, and their managers make adoption decisions based on time savings and error reduction.

**Incorrect:**
> CloudBridge is used by Python developers with 5+ years of experience who write pandas scripts and prefer CLI tools with YAML configuration.
> *Why wrong: Describes the audience by technical profile and specific skill requirements instead of goals and needs. The audience section should be understandable without code knowledge.*

## Writing Guidance

- **Tone:** conversational
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** Describe audiences by their goals, pain points, and decision-making criteria; distinguish between end users and decision-makers; include what each audience expects from the product
- **Don't:** List programming skills, tool proficiencies, or job titles as the defining trait; write user stories or persona cards; conflate technical users with the primary audience

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Purpose

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
