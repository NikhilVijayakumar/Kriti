# Installation — Generation Template

> **Domain:** readme
> **Section:** installation
> **Source:** `documentation-standards/15-readme-standards.md` §Installation
> **Relationships:** `audit/deterministic/document/15-readme-relationships.yaml`

Generate the Installation section for a README document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | build / versioning_naming | Installation must use versioned artifact names per Build(14) naming conventions |

## Template

```markdown
## Installation

### Prerequisites

- [Required tool and version]

### Install

[Step-by-step commands with expected output]
```

**Required subsections:** Prerequisites, Install

## Examples

**Correct:**
> ### Prerequisites
>
> - Rust 1.75+ (via rustup)
>
> ### Install
>
> ```bash
> cargo install acme-scheduler
> ```
>
> Verify installation:
>
> ```bash
> acme-scheduler --version
> # Expected: acme-scheduler 2.1.0
> ```

**Incorrect:**
> Just clone the repo and it works. You might need to install some things first.
> *Why wrong: Installation must provide specific step-by-step commands with prerequisites listed, not vague instructions that leave the reader guessing what to install.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** List prerequisites with version numbers first; provide step-by-step commands with expected output; verify each step works
- **Don't:** Use vague instructions like "install dependencies"; omit version requirements; skip verification steps

**Minimum content:** 1 subsection
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Build, Getting Started, Development, Contributing

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
