# Design Document — Generation Template

> **Domain:** design
> **Source standard:** `documentation-standards/06-design-standards.md`
> **Coherence source:** `audit/semantic/document/06-design.md`
> **Relationships:** `audit/deterministic/document/06-design-relationships.yaml`

Generate a complete Design document for a system. The document must satisfy every required section below, in the order defined by the standard.

## Required Sections

| # | Section | semantic_type | Required | Content Requirements |
|---|---------|--------------|----------|---------------------|
| 1 | Design Principles | `design_principles` | ✓ | 3+ named principles with rationale and product-level examples |
| 2 | UX Principles | `ux_principles` | ✓ | 3+ interaction principles covering navigation, feedback, and discoverability |
| 3 | Accessibility | `accessibility` | ✓ | Compliance target (e.g. WCAG level), inclusive design principles, assistive technology guidance |
| 4 | Purpose | `purpose` | | Problem statement, scope definition, distinction from Feature Design |
| 5 | Constraints | `constraints` | | Binding constraints with source (regulatory, platform, organizational) and enforcement scope |
| 6 | Traceability | `traceability` | | Tier diagram, upstream derivation paths, downstream consumers, non-contradiction rule |

## Cross-Section Coherence Constraint

> Sourced from `audit/semantic/document/06-design.md` Engineering Intent.

All sections must be mutually consistent — no contradictions between Design Principles and UX Principles, between Accessibility and any other section, between Constraints and UX Principles, or between any two sections. Terminology must be consistent across all sections: same concept, same name. Design principles must be reusable and technology-independent throughout. No feature-specific content may appear in any section.

## Sections

---

### 1. Design Principles

**Template:**

```markdown
## Design Principles

[1 paragraph: how design principles anchor the design language and guide decisions]

### [Principle Name]

> **definition:** [one-sentence definition of this principle]
> **scope:** [which design decisions this applies to]

[1 paragraph: why this principle matters]

[1–2 examples: how this principle applies across features]

[Contrast: what violating this principle looks like]

---

[Repeat for each principle — minimum 3]

### Principle Prioritization

[1 paragraph: how to resolve conflicts when principles compete]
```

**Correct example:**
> ### Consistency
> > **definition:** Every feature uses the same interaction patterns, visual language, and terminology for the same type of action.
> > **scope:** Navigation, feedback, input, error handling, and layout across all features.
>
> Consistency ensures users transfer learning between features. When one feature uses a swipe gesture for deletion, every feature should use the same gesture for the same action.
>
> *Contrast:* If one feature requires a long-press to delete and another requires a swipe, users must relearn the pattern — eroding trust and increasing cognitive load.

**Incorrect example:**
> Consistency means all buttons should use the same CSS class (`btn-primary`) and follow the design tokens defined in the component library's theme configuration.
> *Why wrong: This conflates design consistency with CSS implementation details. Design Principles must describe values and behaviors, not technology-specific styling rules.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** mixed
- **Audience:** new contributor
- **Do:** Define each principle with a one-sentence definition and explicit scope. Include cross-feature examples and contrast. Add Principle Prioritization.
- **Don't:** Reference CSS classes, frameworks, or design tokens. Leave principle conflicts unaddressed.

---

### 2. UX Principles

**Template:**

```markdown
## UX Principles

[1 paragraph: how UX principles connect to the product's design philosophy]

### [Principle Name]

[1 paragraph: what this principle means at the product level]

[1 cross-feature example]

---

[Repeat for each principle — minimum 3]
```

**Correct example:**
> ### Feedback Visibility
> Users should always receive immediate, clear feedback when they perform an action. Whether submitting a form, navigating to a new view, or encountering an error, the system confirms the action occurred and indicates the result.
>
> When a user submits a support ticket, they see a confirmation toast and are redirected to the ticket detail view. When a user updates their profile settings, the same confirmation pattern applies.

**Incorrect example:**
> When the user clicks the "Submit" button in React, the onClick handler should call the API endpoint and display a Material UI Snackbar component.
> *Why wrong: Technology-specific implementation guidance, not a product-level UX principle.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** mixed
- **Audience:** product owner
- **Do:** Frame each principle as product-level philosophy. Provide cross-feature examples. Ground in user outcomes.
- **Don't:** Reference UI frameworks or libraries. Describe feature-specific workflows.

---

### 3. Accessibility

**Template:**

```markdown
## Accessibility

[1 paragraph: accessibility philosophy]

### Compliance Targets

[1 paragraph: applicable standard, enforcement scope]

### Inclusive Design Principles

[1 principle per subsection — minimum 3]

### Assistive Technology Support

[1 paragraph: screen readers, keyboard navigation, voice control]
```

**Correct example:**
> ### Compliance Targets
> The product targets WCAG 2.1 Level AA conformance across all user-facing interfaces. Exceptions are documented per feature and must receive explicit approval.
>
> ### Inclusive Design Principles
> #### Perceivable Content
> All information and UI components must be presentable in ways users can perceive. Text alternatives for non-text content, captions for multimedia, and sufficient color contrast ratios of at least 4.5:1.

**Incorrect example:**
> All buttons must include `aria-label="Submit"` and use the `role="button"` attribute.
> *Why wrong: Component-level ARIA patterns belong to Engineering, not Design.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Reference specific compliance standards with enforcement scope. Define inclusive design principles at product level.
- **Don't:** Specify ARIA attributes or HTML patterns. Write testing scripts.

---

### 4. Purpose

**Template:**

```markdown
## Purpose

[1 paragraph: what problem this Design Documentation solves and why it exists]

[1 paragraph: scope — what it defines and what it does not; distinction from Feature Design]
```

**Correct example:**
> Design Documentation solves the problem of inconsistent design across features by establishing reusable design principles, interaction philosophy, and UX standards that govern an entire product ecosystem. It defines how products should be designed at the product level — not how individual features behave.

**Incorrect example:**
> Design Documentation defines the checkout flow for the payment module, including screen layouts and button placement.
> *Why wrong: Feature-specific workflow, not a product-level design standard.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** State the problem before describing scope. Distinguish from Feature Design.
- **Don't:** List specific features. Reference implementation technologies.

---

### 5. Constraints

**Template:**

```markdown
## Constraints

[1 paragraph: how constraints shape design decisions]

### [Constraint Category]

> **source:** [regulatory body, platform requirement, organizational mandate]
> **enforcement:** [binding / advisory]
> **scope:** [which features or capabilities this applies to]

[1 paragraph: what this constraint requires]

[Repeat for each constraint category — minimum 1]
```

**Correct example:**
> ### Regulatory
> > **source:** Federal accessibility regulation (Section 508)
> > **enforcement:** binding
> > **scope:** All user-facing interfaces
>
> The product must comply with federal accessibility requirements. This constraint is non-negotiable.

**Incorrect example:**
> We prefer using a specific CSS framework because the team knows it well.
> *Why wrong: Team preference, not a binding constraint.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** State each constraint with source, enforcement level, and scope. Distinguish binding from advisory.
- **Don't:** List team preferences. Omit source or enforcement level.

---

### 6. Traceability

**Template:**

```markdown
## Traceability

### Tier Diagram

[ASCII or Mermaid diagram showing Design Documentation's position in the hierarchy]

### Upstream Derivation

[1 paragraph per upstream source]

### Downstream Consumers

[1 paragraph per downstream consumer]

### Non-Contradiction Rule

[1 paragraph: downstream documents must not contradict design principles]
```

**Correct example:**
> ### Tier Diagram
> Vision → Design Documentation → Feature Design → Engineering → Implementation
>
> Design Documentation derives its principles from the product Vision and Philosophy. It feeds Feature Design, which applies those principles to specific features. No downstream document may contradict the design principles established here.

**Incorrect example:**
> Traceability shows that module A calls module B, which calls module C, through a dependency graph of the codebase.
> *Why wrong: Code-level implementation traceability, not documentation hierarchy traceability.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** third person
- **Structure:** diagrams
- **Audience:** AI agent
- **Do:** Include a visual tier diagram. List every upstream source and downstream consumer. State non-contradiction rule as binding.
- **Don't:** Describe code-level module dependencies. Leave non-contradiction rule implicit.

---

## Output Contract

Output a single complete markdown document containing all 6 sections above, in the order listed. Each section must:

1. Use the template skeleton as its structural basis
2. Fill every placeholder with domain-appropriate content (not lorem ipsum)
3. Satisfy the Writing Guidance for its section
4. Be consistent with every other section (cross-section coherence constraint above)
5. Omit implementation details
6. Remain technology-independent throughout
