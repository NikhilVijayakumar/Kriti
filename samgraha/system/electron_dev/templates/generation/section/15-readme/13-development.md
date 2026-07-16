# Development — Generation Template

> **Domain:** readme
> **Section:** development
> **Source:** `documentation-standards/15-readme-standards.md` §Development
> **Relationships:** `audit/deterministic/document/15-readme-relationships.yaml`

Generate the Development section for a README document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | engineering / code_standards | Development workflow must reference Engineering(07) code standards |

## Template

```markdown
## Development

### Local Setup

[Development environment setup steps]

### Running Tests

[Test commands with expected output]

### Workflow

[Development workflow description]
[Reference coding standards]
```

**Required subsections:** Local Setup, Running Tests
**Optional subsections:** Workflow

## Examples

**Correct:**
> ### Local Setup
>
> ```bash
> git clone https://github.com/acme/scheduler.git
> cd scheduler
> npm install
> ```
>
> ### Running Tests
>
> ```bash
> npm test
> ```
>
> ### Workflow
>
> Create a feature branch, make changes, run tests, and open a pull request. See [Coding Standards](../engineering/coding-standards.md) for style guidelines.

**Incorrect:**
> To develop, clone the repo and start coding. Write tests for your changes.
> *Why wrong: Development must provide specific setup steps, test commands, and workflow description, not assume the reader knows the toolchain or contribution process.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Describe development environment setup with specific commands; explain how to run tests; reference coding standards
- **Don't:** Assume prior knowledge of the toolchain; omit test commands; skip workflow description or coding standard references

**Minimum content:** 1 subsection
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Contributing, Getting Started, Repository Structure

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
