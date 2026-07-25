# Build — Generation Template

> **Domain:** readme
> **Section:** build
> **Source:** `documentation-standards/15-readme-standards.md` §Build
> **Relationships:** `audit/deterministic/document/15-readme-relationships.yaml`

Generate the Build section for a README document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | build / documentation_quality | Build instructions must be accurate to the shipped Build(14) pipeline |

## Template

```markdown
## Build

### Prerequisites

- [Build tool and version]

### Build Commands

[Build commands with expected output]
[List common build targets]
```

**Required subsections:** Prerequisites, Build Commands

## Examples

**Correct:**
> ### Prerequisites
>
> - JDK 17
> - Gradle 8.2+
>
> ### Build Commands
>
> ```bash
> ./gradlew build
> ```
>
> Produces `build/libs/scheduler.jar`.

**Incorrect:**
> Run the build. It compiles everything and puts the output somewhere in the build directory.
> *Why wrong: Build must list prerequisites, provide specific commands, and describe expected output, not leave the reader guessing about tool versions and where artifacts appear.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** List build prerequisites with version numbers; provide specific build commands; describe expected output and artifact locations
- **Don't:** Omit prerequisite versions; use ambiguous build commands; skip expected output descriptions

**Minimum content:** 1 subsection
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** Installation, Getting Started, Development, Contributing

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
