# Getting Started — Generation Template

> **Domain:** readme
> **Section:** getting_started
> **Source:** `documentation-standards/15-readme-standards.md` §Getting Started
> **Relationships:** `audit/deterministic/document/15-readme-relationships.yaml`

Generate the Getting Started section for a README document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | build / documentation_quality | Getting Started must produce a result that passes Build(14) documentation quality checks |

## Template

```markdown
## Getting Started

### Prerequisites

- [Required tools and versions]

### Quick Start

[Step-by-step from clone to running project]
[Prerequisites, install, build, first run in one place]
```

**Required subsections:** Prerequisites, Quick Start

## Examples

**Correct:**
> ### Prerequisites
>
> - Python 3.10+
> - Docker 24+
>
> ### Quick Start
>
> ```bash
> git clone https://github.com/acme/scheduler.git
> cd scheduler
> docker compose up
> curl http://localhost:8080/health
> # Expected: {"status":"ok"}
> ```

**Incorrect:**
> Clone the repo, install dependencies, and run the app. See Installation and Build sections for details.
> *Why wrong: Getting Started must provide a complete, linear zero-to-running path with prerequisites and working commands, not delegate the reader to other sections.*

## Writing Guidance

- **Tone:** conversational
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** new contributor
- **Do:** Provide a complete linear path from clone to running project; include all prerequisites and version numbers; verify each step works
- **Don't:** Delegate readers to other sections; omit prerequisites; skip verification steps or expected outcomes

**Minimum content:** 1 subsection
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Installation, Build, Usage, Development, Contributing

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
