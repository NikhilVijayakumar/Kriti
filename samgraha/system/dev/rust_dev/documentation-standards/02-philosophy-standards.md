# Philosophy Standard

> *Deterministic rules for this domain: `audit/deterministic/document/02-philosophy.yaml`*

## Table of Contents
- [Purpose](#purpose)
- [Systems Philosophy Addendum](#systems-philosophy-addendum)
- [Principles](#principles)
- [Values](#values)
- [Trade-offs](#trade-offs)
- [Required Sections](#required-sections)
- [Goals](#goals)
- [Non-Goals](#non-goals)
- [Success Criteria](#success-criteria)
- [Responsibilities](#responsibilities)
- [Scope](#scope)
- [Out of Scope](#out-of-scope)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [Traceability](#traceability)
- [Relationships](#relationships)
- [Required Characteristics](#required-characteristics)
- [Audit Rules](#audit-rules)
- [Validation Rules](#validation-rules)
- [Generation Rules](#generation-rules)
- [Enhancement Rules](#enhancement-rules)
- [Summary](#summary)
- [Common Mistakes](#common-mistakes)
- [Documentation Folder](#documentation-folder)
- [Usage](#usage)
- [Related](#related)
- [Quality Requirements](#quality-requirements)

---


## Purpose

> *Structural rules: `audit/deterministic/section/02-philosophy/04-purpose.yaml`*

### Template

> **minimum_content:** 2 paragraphs
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
## Purpose

This document defines the standard for [Domain] documentation within the engineering documentation ecosystem.

[One paragraph explaining what this documentation type does and why it exists.]

[One paragraph distinguishing it from related standards — what it covers that others do not.]
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Vision(01)

### Examples

**Correct:**
> This document defines the standard for Project Horizon documentation within the engineering documentation ecosystem.
>
> Project Horizon Documentation establishes the product's guiding principles, values, and the deliberate trade-offs that shape every downstream decision.
>
> Unlike Vision, which explains **why** the product exists, Philosophy explains **how the people building it choose to think and decide**.

**Incorrect:**
> This document defines the Philosophy for the React frontend and PostgreSQL backend of Project Horizon.
> *Why wrong: Technology-specific — references concrete technologies instead of describing Philosophy's role in the ecosystem.*

### Writing Guidance

- **Tone:** inspirational
- **Voice:** first person plural
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** State Philosophy's role before listing contents; distinguish it from Vision using a clear contrast; use language that endures across technology changes
- **Don't:** Mention specific technologies or frameworks; describe features or architecture; use implementation-level vocabulary

This document defines the standard for Philosophy documentation within the engineering documentation ecosystem.

Philosophy Documentation establishes the product's guiding principles, values, and the deliberate trade-offs that shape every downstream decision.

Unlike Vision, which explains **why** the product exists, Philosophy explains **how the people building it choose to think and decide**.

It does not describe features, architecture, or engineering decisions.

It shapes the judgment that produces them.

---

## Principles

> *Structural rules: `audit/deterministic/section/02-philosophy/01-guiding_principles.yaml`*

### Template

> **minimum_content:** 3 subsections
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
## Principles

### [Principle Name 1]

[One to two sentences stating the principle as a stable, technology-independent decision rule.]

[One example of how this principle resolves an ambiguous decision.]

### [Principle Name 2]

[One to two sentences stating the principle.]

[One example of application.]

### [Principle Name 3]

[One to two sentences stating the principle.]

[One example of application.]
```

**Required subsections:** 3-5 named principles
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Values, Vision(01)

### Examples

**Correct:**
> ### Simplicity First
>
> When two designs solve the same problem, choose the simpler one. Complexity is a cost, not a feature.
>
> If adding a framework means the team must learn a new paradigm, it must clearly reduce complexity in the rest of the system to justify itself.

**Incorrect:**
> ### Use REST Over GraphQL
>
> We prefer REST because it is easier to implement with Express.js and integrates well with our React frontend.
> *Why wrong: Technology-specific — names concrete frameworks and technologies instead of expressing a stable, technology-independent decision rule.*

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** architect
- **Do:** State each principle as a decision rule that resolves ambiguity; include a concrete example of the principle in action; keep phrasing memorable enough to cite in Architecture or Design
- **Don't:** Name specific frameworks, languages, or libraries; write principles as aspirations without a decision outcome; list more than five principles

*(To be written by the product owner. This section defines the guiding principles of the product.)*

---

## Values

> *Structural rules: `audit/deterministic/section/02-philosophy/02-values.yaml`*

### Template

> **minimum_content:** 2 subsections
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
## Values

### [Value Name 1]

[One to two sentences naming the value and why it is prioritized.]

[One sentence explaining what this value costs or what it sacrifices.]

### [Value Name 2]

[One to two sentences naming the value and why it is prioritized.]

[One sentence explaining what this value costs or what it sacrifices.]

### [Value Name 3]

[One to two sentences naming the value and why it is prioritized.]

[One sentence explaining what this value costs or what it sacrifices.]
```

**Required subsections:** 2-4 named values
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Principles, Vision(01)

### Examples

**Correct:**
> ### Developer Productivity
>
> We optimize for how quickly a developer can understand, modify, and ship a change. Fast iteration beats perfect architecture.
>
> This sometimes means choosing a straightforward solution over a more elegant one that takes longer to implement.

**Incorrect:**
> ### Use TypeScript
>
> We value TypeScript because it catches bugs at compile time and is the industry standard for modern frontend development.
> *Why wrong: Names a specific technology instead of expressing an underlying value. The value is correctness, not a language choice.*

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** first person plural
- **Structure:** mixed
- **Audience:** product owner
- **Do:** Name the value explicitly in the heading; state what the value costs or what it sacrifices; make trade-offs between values visible so downstream standards can reference them
- **Don't:** Use aspirational platitudes without substance; conflate values with feature priorities; name technologies as values

*(To be written by the product owner. This section defines the core values of the product.)*

---

## Trade-offs

> *Structural rules: `audit/deterministic/section/02-philosophy/03-tradeoffs.yaml`*

### Template

> **minimum_content:** 1 subsection per trade-off
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
## Trade-offs

### [Trade-off Name 1]

**Chosen:** [What the product deliberately optimizes for.]
**Sacrificed:** [What the product deliberately does not optimize for.]
**Reason:** [Why this trade-off was made — tied to a value or principle.]

### [Trade-off Name 2]

**Chosen:** [What is optimized for.]
**Sacrificed:** [What is given up.]
**Reason:** [Why.]
```

**Required subsections:** at least one trade-off per named value
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Values, Principles, Architecture(05)

### Examples

**Correct:**
> ### Speed vs. Completeness
>
> **Chosen:** Fast iteration and rapid delivery of working features.
> **Sacrificed:** Comprehensive documentation and exhaustive test coverage at launch.
> **Reason:** Our value of Developer Productivity demands we ship early; documentation and coverage catch up after the feature is validated.

**Incorrect:**
> ### React vs. Vue
>
> **Chosen:** React for the frontend.
> **Sacrificed:** Vue's smaller bundle size.
> **Reason:** The team already knows React so it is faster to build with.
> *Why wrong: Describes a technology selection, not a deliberate trade-off in product values. This belongs in Architecture or Engineering, not Philosophy.*

### Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** tables
- **Audience:** architect
- **Do:** Use the Chosen / Sacrificed / Reason format consistently; tie each trade-off back to a named value; explain the reasoning so downstream standards can cite it
- **Don't:** Describe technology selections as trade-offs; list accidental constraints as deliberate choices; omit the reason or tie it to a named value

*(To be written by the product owner. This section defines the deliberate trade-offs the product makes.)*

---

## Required Sections

Every Philosophy document must contain the following sections.
Sections are identified by heading text; the compiler maps each to a semantic type.

| Section | semantic_type | Required | Aliases | Content Requirements |
|---------|--------------|----------|---------|----------------------|
| Principles | `guiding_principles` | ✓ | Core Principles, Design Principles | 3-5 named principles; each stated as a stable, technology-independent decision rule |
| Values | `values` | ✓ | Core Values, What We Value | 2-4 named values; each explicitly prioritized with rationale for why it outranks alternatives |
| Trade-offs | `tradeoffs` | ✓ | Trade offs, Tradeoffs, Deliberate Trade-offs | At least one trade-off per value; each names what is chosen and what is deliberately sacrificed |
| Purpose | `purpose` | | Overview, Summary | One to two paragraphs defining Philosophy's role and its distinction from Vision |

Section headings are case-insensitive. Sections not listed here are stored as `generic` type — preserved but not queryable by type.

---

## Goals

Philosophy Documentation aims to:

* Give the team a shared way to resolve ambiguous decisions.
* Make trade-offs explicit rather than implicit.
* Keep Architecture and Design principled rather than arbitrary.
* Remain true across many features and technology changes.

---

## Non-Goals

Philosophy Documentation does not define:

* Product vision or direction
* Feature specifications
* Architecture
* Technology selection

These responsibilities belong to other documentation standards.

---

## Success Criteria

Philosophy Documentation is successful when:

* Engineers can resolve an ambiguous design decision by referring back to it.
* Architecture and Design documents can cite it to justify a principle.
* It remains true even as specific features and technologies change.

---

## Responsibilities

Philosophy Documentation is responsible for defining:

* Guiding principles
* Core values
* Deliberate trade-offs
* Decision-making posture
* What the product optimizes for
* What the product deliberately does not optimize for

Philosophy provides the reasoning framework every other standard is judged against.

---

## Scope

Philosophy Documentation may describe:

* Engineering philosophy
* Product philosophy
* Design philosophy
* Trade-offs between competing goods (e.g. simplicity vs. flexibility)
* Values that resolve ambiguous decisions
* Postures toward risk, speed, and correctness

Philosophy should remain abstract enough to outlive any single feature or technology choice.

---

## Out of Scope

Philosophy Documentation must not describe:

* Product vision or long-term direction
* Feature specifications
* Architecture
* Technology selection
* Source code
* Specific technology choices

These belong to other documentation standards.

---

## Inputs

Philosophy Documentation derives from:

* Vision
* Organizational values
* Prior engineering experience and lessons learned

Philosophy should not derive from implementation details.

---

## Outputs

Philosophy Documentation provides direction for:

* Architecture
* Design
* Engineering decisions

Every architectural or design principle should be traceable to a value or trade-off documented here.

---

## Traceability

```text
Vision
    ↓
Philosophy
    │
    ├──────────────┐
    ↓              ↓
Architecture     Design
```

Philosophy guides Architecture and Design without dictating their specifics.

---

## Relationships

| Document     | Relationship                               |
| ------------ | ------------------------------------------ |
| Vision       | Inspired by Vision                          |
| Feature      | Shapes feature decision-making              |
| Architecture | Guides architectural principles              |
| Design       | Guides design principles                     |
| Security     | Shapes security decision-making              |
| Engineering  | Shapes engineering principles and trade-offs |

---

## Required Characteristics

Philosophy Documentation should be:

* Stable
* Abstract
* Honest about trade-offs
* Memorable
* Technology-independent
* Actionable when a decision is ambiguous

---

## Audit Rules

An audit should verify:

* Principles are documented (`phil-001`, error).
* Values are documented (`phil-002`, warning).
* Trade-offs are documented (`phil-003`, suggestion).

---

## Validation Rules

Philosophy Documentation is considered valid when:

* Principles are documented and distinguishable from Vision.
* Values are explicit.
* Trade-offs are named honestly, including what is deliberately sacrificed.
* No implementation or technology-specific content appears.

---

## Generation Rules

When generating Philosophy Documentation:

* Start from Vision, then ask "how do we decide when two good options conflict?"
* Name the trade-off explicitly — what is chosen, and what is deliberately given up.
* Keep principles technology-independent.

---

## Enhancement Rules

When enhancing Philosophy Documentation:

* Replace aspirational statements with named trade-offs.
* Remove content that duplicates Vision.
* Keep principles few and memorable rather than exhaustive.

---

## Summary

Philosophy is the decision-making posture behind the product: the principles, values, and named trade-offs that Architecture and Design are built on. It stays stable while features and technology change underneath it.

---

## Common Mistakes

Examples of incorrect Philosophy content include:

* Restating Vision instead of explaining decision-making posture.
* Listing aspirational values with no named trade-off.
* Describing specific technology choices.
* Describing features instead of the reasoning behind them.

---

## Documentation Folder

Philosophy documents live under:

```text
docs/raw/philosophy/
```

---

## Usage

Written rarely, revisited when a recurring disagreement reveals the team lacks a shared principle to resolve it. Use `samgraha audit --domain philosophy` to confirm Principles, Values, and Trade-offs are all present — a Philosophy doc missing a Trade-offs section is usually just restated Vision.

## Related

- [Vision Standard](01-vision-standards.md) — Philosophy is inspired by Vision
- [Architecture Standard](05-architecture-standards.md) — guided by Philosophy


## Quality Requirements

Philosophy Documentation should be:

* Stable
* Abstract enough to survive technology changes
* Concrete enough to resolve real disagreements
* Honest about trade-offs (not aspirational marketing)

---

## Systems Philosophy Addendum

> *Structural rules: `audit/deterministic/section/02-philosophy/05-systems_philosophy.yaml`*

### Template

> **minimum_content:** 1 list
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
The rust_dev system adds the following philosophical principles:

* **Ownership over Garbage Collection:** We leverage Rust's ownership system as a design tool, not just a compiler requirement. Ownership makes resource lifecycles explicit and eliminates an entire class of bugs at compile time.
* **Safety as Default:** Zero `unsafe` in business logic; all edge cases encoded in the type system.
* **Performance Matters:** Mechanical sympathy with the hardware, predictable latency.
* **Explicit Over Implicit:** We prefer explicit lifetimes, explicit errors (`Result`), and explicit dependencies.
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples
**Correct:**
> We return `Result<T, AppError>` instead of panicking.

**Incorrect:**
> We just use `.unwrap()`.

### Writing Guidance
- **Tone:** philosophical
- **Voice:** first person plural ("We")
- **Structure:** list
- **Audience:** all engineers
- **Do:** Emphasize safety and performance.
