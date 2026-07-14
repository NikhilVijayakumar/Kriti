# Philosophy Document — Generation Template

> **Domain:** philosophy
> **Source standard:** `documentation-standards/02-philosophy-standards.md`
> **Coherence source:** `audit/semantic/document/02-philosophy.md`
> **Relationships:** `audit/deterministic/document/02-philosophy-relationships.yaml`

Generate a complete Philosophy document for a system. The document must satisfy every required section below, in the order defined by the standard.

## Required Sections

| # | Section | semantic_type | Required | Content Requirements |
|---|---------|--------------|----------|---------------------|
| 1 | Purpose | `purpose` | | 1-2 paragraphs defining Philosophy's role and its distinction from Vision |
| 2 | Principles | `guiding_principles` | ✓ | 3-5 named principles; each stated as a stable, technology-independent decision rule |
| 3 | Values | `values` | ✓ | 2-4 named values; each explicitly prioritized with rationale for why it outranks alternatives |
| 4 | Trade-offs | `tradeoffs` | ✓ | At least one trade-off per value; each names what is chosen and what is deliberately sacrificed |

## Cross-Section Coherence Constraint

> Sourced from `audit/semantic/document/02-philosophy.md` Engineering Intent.

All sections must cohere as a single decision-making posture. Principles must be consistent with Values — a principle cannot advocate for something a value explicitly sacrifices. Trade-offs must name the values they serve — every chosen/sacrificed pair must trace to a named value. No section may contain technology choices, feature specifications, or architectural decisions. Philosophy explains *how the team decides*, not *what they build*. Terminology must be consistent across all sections — the same concept uses the same name everywhere.

## Sections

---

### 1. Purpose

**Template:**

```markdown
## Purpose

> **Philosophical purpose:** [1-2 sentences: what decision-making philosophy guides this team, what values it establishes]

> **Distinction from Vision:**
> - **Vision says:** [why the product exists — one sentence]
> - **Philosophy says:** [how the team chooses to think and decide — one sentence]

> **Scope boundaries:**
> - **In scope:** [principles, values, trade-offs this document defines]
> - **Out of scope:** [what this document does not define — features, architecture, engineering decisions]
```

> **Generation note:** When generating for a specific system, fill this template with *that system's* philosophy purpose: what Philosophy establishes and how it differs from Vision. The meta-level "This document defines the standard for Philosophy..." language belongs in the standard itself, not in a generated document.

**Correct example:**
> **Philosophical purpose:** This document establishes Project Horizon's decision-making philosophy — the principles, values, and trade-offs that guide every downstream choice.
>
> **Distinction from Vision:**
> - **Vision says:** Why Project Horizon exists and what problem it solves for users.
> - **Philosophy says:** How the team building it chooses to think, prioritize, and decide.
>
> **Scope boundaries:**
> - **In scope:** Guiding principles, named values with priority rankings, explicit trade-offs
> - **Out of scope:** Feature specifications, architectural decisions, implementation choices

**Incorrect example:**
> This document defines the Philosophy for the React frontend and PostgreSQL backend of Project Horizon.
> *Why wrong: Technology-specific — references concrete technologies instead of describing Philosophy's role in the ecosystem.*

**Writing guidance:**
- **Tone:** inspirational
- **Voice:** first person plural
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** State Philosophy's role before listing contents; distinguish it from Vision using a clear contrast; use language that endures across technology changes
- **Don't:** Mention specific technologies or frameworks; describe features or architecture; use implementation-level vocabulary

---

### 2. Principles

**Template:**

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

**Correct example:**
> ### Simplicity First
>
> When two designs solve the same problem, choose the simpler one. Complexity is a cost, not a feature.
>
> If adding a framework means the team must learn a new paradigm, it must clearly reduce complexity in the rest of the system to justify itself.

**Incorrect example:**
> ### Use REST Over GraphQL
>
> We prefer REST because it is easier to implement with Express.js and integrates well with our React frontend.
> *Why wrong: Technology-specific — names concrete frameworks instead of expressing a stable decision rule.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** architect
- **Do:** State each principle as a decision rule that resolves ambiguity; include a concrete example of the principle in action; keep phrasing memorable enough to cite in Architecture or Design
- **Don't:** Name specific frameworks, languages, or libraries; write principles as aspirations without a decision outcome; list more than five principles

---

### 3. Values

**Template:**

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

**Correct example:**
> ### Developer Productivity
>
> We optimize for how quickly a developer can understand, modify, and ship a change. Fast iteration beats perfect architecture.
>
> This sometimes means choosing a straightforward solution over a more elegant one that takes longer to implement.

**Incorrect example:**
> ### Use TypeScript
>
> We value TypeScript because it catches bugs at compile time and is the industry standard for modern frontend development.
> *Why wrong: Names a specific technology instead of expressing an underlying value.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** first person plural
- **Structure:** mixed
- **Audience:** product owner
- **Do:** Name the value explicitly in the heading; state what the value costs or what it sacrifices; make trade-offs between values visible so downstream standards can reference them
- **Don't:** Use aspirational platitudes without substance; conflate values with feature priorities; name technologies as values

---

### 4. Trade-offs

**Template:**

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

**Correct example:**
> ### Speed vs. Completeness
>
> **Chosen:** Fast iteration and rapid delivery of working features.
> **Sacrificed:** Comprehensive documentation and exhaustive test coverage at launch.
> **Reason:** Our value of Developer Productivity demands we ship early; documentation and coverage catch up after the feature is validated.

**Incorrect example:**
> ### React vs. Vue
>
> **Chosen:** React for the frontend.
> **Sacrificed:** Vue's smaller bundle size.
> **Reason:** The team already knows React so it is faster to build with.
> *Why wrong: Describes a technology selection, not a deliberate trade-off in product values.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** imperative
- **Structure:** tables
- **Audience:** architect
- **Do:** Use the Chosen / Sacrificed / Reason format consistently; tie each trade-off back to a named value; explain the reasoning so downstream standards can cite it
- **Don't:** Describe technology selections as trade-offs; list accidental constraints as deliberate choices; omit the reason or tie it to a named value

---

## Output Contract

Output a single complete markdown document containing all 4 sections above, in the order listed. Each section must:

1. Use the template skeleton as its structural basis
2. Fill every placeholder with domain-appropriate content (not lorem ipsum)
3. Satisfy the Writing Guidance for its section
4. Be consistent with every other section (cross-section coherence constraint above)
5. Include diagrams where Required diagrams are specified (as markdown image references or Mermaid code blocks)
6. Omit implementation details (technology names, library versions, configuration values, code snippets)
