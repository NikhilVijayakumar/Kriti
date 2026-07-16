# Contributing — Generation Template

> **Domain:** readme
> **Section:** contributing
> **Source:** `documentation-standards/15-readme-standards.md` §Contributing
> **Relationships:** `audit/deterministic/document/15-readme-relationships.yaml`

Generate the Contributing section for a README document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | engineering / code_standards | Contributing must reference Engineering(07) code standards and quality requirements |

## Template

```markdown
## Contributing

### Contribution Process

[Step-by-step contribution workflow]

### Code Review

[Code review expectations and process]

### Quality Standards

[List quality standards for contributions]
[Reference development setup]
```

**Required subsections:** Contribution Process, Code Review, Quality Standards

## Examples

**Correct:**
> ### Contribution Process
>
> 1. Fork the repository
> 2. Create a feature branch from `main`
> 3. Make changes and add tests
> 4. Open a pull request against `main`
>
> ### Code Review
>
> All pull requests require one approval. Reviewers check for test coverage, code style, and documentation updates.
>
> ### Quality Standards
>
> - All new code must have tests
> - Documentation must be updated for user-facing changes
> - Commit messages follow Conventional Commits

**Incorrect:**
> Contributions welcome! Just open a PR.
> *Why wrong: Contributing must describe the full contribution workflow, code review process, and quality standards, not provide a one-line invitation with no actionable guidance.*

## Writing Guidance

- **Tone:** conversational
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** new contributor
- **Do:** Describe the full contribution workflow step by step; explain code review expectations; list quality standards for contributions
- **Don't:** Use vague invitations like "contributions welcome"; omit code review process; skip quality standards or testing requirements

**Minimum content:** 1 subsection
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Development, Related, Documentation Navigation

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
