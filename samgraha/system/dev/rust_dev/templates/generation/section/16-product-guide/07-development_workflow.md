# Development Workflow — Generation Template

> **Domain:** product-guide
> **Section:** development_workflow
> **Source:** `documentation-standards/16-product-guide-standards.md` §DevelopmentWorkflow
> **Relationships:** `audit/deterministic/document/16-product-guide-relationships.yaml`

Generate the Development Workflow section for a Product-Guide document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | build / local_setup | Workflow derives from local environment setup |

> *Structural rules: `audit/deterministic/section/16-product-guide/07-development_workflow.yaml`*

### Template

> **minimum_content:** 1 list of commands
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
To develop within this repository, follow the standard Rust workflow:

### Local Setup

[Provide commands for installing rustup, cargo-make, and cloning the workspace.]

### Building and Running

[Provide commands for `cargo build`, `cargo run`, and managing features.]

### Testing and Linting

[Provide commands for `cargo test`, `cargo clippy`, and `cargo fmt`.]
```

**Required subsections:** Local Setup, Building and Running, Testing and Linting
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> Run `cargo clippy --all-targets --all-features -- -D warnings` to lint your code before committing.

**Incorrect:**
> Just figure it out.
> *Why wrong: The product guide must explicitly document the developer workflow.*

### Writing Guidance

- **Tone:** instructional
- **Voice:** second person
- **Structure:** code blocks and lists
- **Audience:** new developer
- **Do:** Provide exact, copy-pasteable Cargo commands.

> **Generation note:** When generating this section for a specific system, ensure that the output strictly adheres to the provided writing guidance and focuses on the concrete implementation details rather than meta-level documentation standards.

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
