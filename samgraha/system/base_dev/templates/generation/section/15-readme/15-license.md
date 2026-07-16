# License — Generation Template

> **Domain:** readme
> **Section:** license
> **Source:** `documentation-standards/15-readme-standards.md` §License
> **Relationships:** `audit/deterministic/document/15-readme-relationships.yaml`

Generate the License section for a README document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | external-context / constraints | License must comply with External Context third-party license requirements |

## Template

```markdown
## License

[State the license name]
[Link to or include the full license text]
[Include copyright notices if applicable]
```

## Examples

**Correct:**
> This project is licensed under the [Apache License 2.0](LICENSE).
>
> Copyright 2025 Acme Corporation.

**Incorrect:**
> You can use this software however you want. See the license file for details.
> *Why wrong: License must state the specific license name and provide a direct link to the full license text, not use vague language that leaves the legal terms ambiguous.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** State the exact license name; link directly to the full license text; include copyright notices if applicable
- **Don't:** Use vague language like "see license file"; omit the license name; include legal advice or license comparisons

**Minimum content:** 1 paragraph
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** External Context for third-party licenses

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
