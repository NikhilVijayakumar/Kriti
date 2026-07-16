# Crate Folder Structure — Generation Template

> **Domain:** implementation
> **Section:** crate_folder_structure
> **Source:** `documentation-standards/13-implementation-standards.md` §CrateFolderStructure
> **Relationships:** `audit/deterministic/document/13-implementation-relationships.yaml`

Generate the Crate Folder Structure section for a Implementation document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | architecture / crate_architecture | Folder structure mirrors crate boundaries |

> *Structural rules: `audit/deterministic/section/13-implementation/08-crate_folder_structure.yaml`*

### Template

> **minimum_content:** 1 file tree
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
This feature is implemented using the standard Cargo crate structure:

```text
crate_name/
├── Cargo.toml
├── src/
│   ├── lib.rs
│   ├── models.rs
│   ├── error.rs
│   └── service.rs
└── tests/
    └── integration_test.rs
```

[Explain any deviations or additions to this standard structure for this specific feature.]
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> The `auth` crate follows the standard layout and adds a `benches/` directory for crypto benchmarks.

**Incorrect:**
> All code is in `lib.rs`.
> *Why wrong: Fails to structure the crate modularly.*

### Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** file tree blocks
- **Audience:** backend developer
- **Do:** Use the canonical Cargo layout.

> **Generation note:** When generating this section for a specific system, ensure that the output strictly adheres to the provided writing guidance and focuses on the concrete implementation details rather than meta-level documentation standards.

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
