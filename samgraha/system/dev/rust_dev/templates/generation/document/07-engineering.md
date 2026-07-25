# Engineering Document — Generation Template

> **Domain:** engineering
> **Source standard:** `documentation-standards/07-engineering-standards.md`
> **Coherence source:** `audit/semantic/document/07-engineering.md`
> **Relationships:** `audit/deterministic/document/07-engineering-relationships.yaml`

Generate a complete Engineering document for a system. The document must satisfy every required section below, in the order defined by the standard.

## Required Sections

| # | Section | semantic_type | Required | Content Requirements |
|---|---------|--------------|----------|---------------------|
| 1 | Engineering Principles | `guiding_principles` | ✓ | Technology-independent values, stable across features, memorable phrasing |
| 2 | Technology Selection | `rationale` | ✓ | Rationale for each choice; not a bare list; connected to Architecture and External Context |
| 3 | Build Standards | `build_standards` | ✓ | Build system, pipeline stages, quality gates, rationale for each stage |
| 4 | Testing Standards | `testing_standards` | ✓ | Test types, coverage expectations, test tooling, rationale |
| 5 | Purpose | `purpose` | | Document's role in ecosystem, scope boundaries, relationship to adjacent standards |
| 6 | Code Standards | `code_standards` | | Style guide, linting configuration, naming conventions, rationale |
| 7 | Constraints | `constraints` | | Non-functional requirements categorized by type, verifiable, connected to source |
| 8 | Traceability | `traceability` | | Derivation diagram, upstream/downstream list, non-contradiction rule |

## Cross-Section Coherence Constraint

> Sourced from `audit/semantic/document/07-engineering.md` Engineering Intent.

All sections must be mutually consistent — no contradictions between Engineering Principles and Build Standards, between Testing Standards and Code Standards, between Constraints and any other section, or between any two sections. Technology rationale in Technology Selection must align with Build Standards and Code Standards tooling choices. Constraints must derive from Architecture and External Context, not from internal preferences. Terminology must be consistent across all sections: same concept, same name.

## Sections

---

### 1. Engineering Principles

**Template:**

```markdown
## Engineering Principles

> [metadata block]

[1 paragraph explaining how principles guide engineering decisions]

[bulleted list of principles, each as a memorable phrase with 1–sentence explanation]
```

**Correct example:**
> * **Minimal Dependencies:** We prefer fewer external dependencies to reduce maintenance burden and security surface. When a choice exists between a library and a self-contained implementation, the trade-off is evaluated against long-term maintenance cost.
> * **Explicit Configuration:** All configuration must be declared in version-controlled files. Environment-specific overrides use a documented override mechanism, not undocumented runtime state.

**Incorrect example:**
> * Use the fastest framework available.
> * Always use the latest version of every library.
> * Write clean code.
> * *Why wrong: Technology-dependent, unstable, and vague — none of these survive technology changes or guide engineering decisions when ambiguity arises.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Phrase each principle as a memorable, technology-independent value. Ensure every principle is actionable.
- **Don't:** Use technology-specific language. State vague platitudes. Add principles that change with technology.

---

### 2. Technology Selection

**Template:**

```markdown
## Technology Selection

> [metadata block]

### [Technology Category]

[1 paragraph: why this technology was chosen, connected to architectural constraints and external context]

[repeat for each technology category]
```

**Correct example:**
> **Language:** Project Alpha uses Rust 1.75+ (edition 2021) because the team has deep expertise, the ecosystem provides mature libraries for data processing, and the architecture requires rapid prototyping cycles. This choice is constrained by the organization's existing Rust infrastructure (External Context) and the need for readable, maintainable code (Architecture Section 2.1).

**Incorrect example:**
> **Language:** Python. **Framework:** Django. **Database:** PostgreSQL.
> *Why wrong: Bare list with no rationale, no connection to Architecture or External Context.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Connect every choice to an architectural constraint or External Context. Explain why, not just what.
- **Don't:** Present bare lists without rationale. Justify on business grounds rather than engineering grounds.

---

### 3. Build Standards

**Template:**

```markdown
## Build Standards

> [metadata block]

### Build System

[1–2 paragraphs: build tool, configuration, rationale]

### Pipeline Stages

> **diagram:** flowchart of pipeline stages

| Stage | Purpose | Inputs | Outputs | Quality Gate |
|-------|---------|--------|---------|-------------|
| [Stage name] | [what it does] | [what feeds it] | [what it produces] | [pass/fail criteria] |

### Quality Gates

[Optional: criteria that must pass before proceeding]
```

**Correct example:**
> **Build System:** The repository uses a task runner configured via `build.config.toml`. Each pipeline stage runs in an isolated container to ensure reproducibility. Rationale: deterministic builds ensure that any commit produces the same artifact regardless of the build environment.

**Incorrect example:**
> **Build System:** We use Jenkins. Our pipeline is: checkout → build → deploy to staging.
> *Why wrong: Missing rationale, missing quality gates, describes deployment which is out of scope.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Document each stage with purpose, inputs, outputs, quality gates. Explain rationale. Include a flowchart.
- **Don't:** Describe deployment. Omit quality gates. List stages without explaining why.

---

### 4. Testing Standards

**Template:**

```markdown
## Testing Standards

> [metadata block]

### Test Types

| Test Type | Purpose | Scope | Tooling | Execution |
|-----------|---------|-------|---------|-----------|
| [Type name] | [what it validates] | [what it covers] | [test runner, assertions] | [when it runs] |

### Coverage Expectations

| Metric | Target | Scope | Rationale |
|--------|--------|-------|-----------|
| [Metric name] | [threshold] | [what it covers] | [why this threshold] |

### Test Tooling

[Optional: test runner, assertion libraries, mocking frameworks]
```

**Correct example:**
> | Test Type | Purpose | Scope | Tooling | Execution |
> |-----------|---------|-------|---------|-----------|
> | Unit | Validate individual modules | Single module | Vitest | Every commit |
> | Integration | Verify module interactions | Cross-module | Vitest + supertest | Every commit |
> | E2E | Exercise critical user journeys | Full system | Playwright | Nightly |

**Incorrect example:**
> We have unit tests and some integration tests. Coverage is pretty good.
> *Why wrong: Vague, no specific test type definitions, no coverage targets, no rationale.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Define each test type with purpose, scope, tooling. Set measurable coverage targets.
- **Don't:** Use vague claims. Omit specific thresholds. Describe feature-specific tests.

---

### 5. Purpose

**Template:**

```markdown
## Purpose

[1–2 paragraphs: this document's role in the documentation ecosystem, scope boundaries, relationship to adjacent standards]
```

**Correct example:**
> This document defines Engineering Documentation's role in the documentation ecosystem. It establishes repository-wide engineering decisions, implementation standards, technology selection rationale, and development conventions. Unlike Feature Technical Design, Engineering Documentation is not feature-specific — it provides reusable knowledge that governs the entire repository.

**Incorrect example:**
> This document describes the login page implementation, including the OAuth2 flow and JWT token storage.
> *Why wrong: Feature-specific and describes implementation details, not the repository-wide role of Engineering Documentation.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** Define the document's role explicitly. Distinguish from adjacent standards. Set clear scope boundaries.
- **Don't:** Include implementation details. Blur boundaries with adjacent standards.

---

### 6. Code Standards

**Template:**

```markdown
## Code Standards

> [metadata block]

### Style Guide

[1 paragraph: language-specific style guide reference, key rules]

### Linting Configuration

[1 paragraph: linter tool, config file location, key rules]

| Rule Category | Description | Enforcement |
|--------------|-------------|-------------|
| [Category] | [what it checks] | [error/warning] |

### Naming Conventions

[Optional: naming patterns for files, modules, functions, variables]
```

**Correct example:**
> **Style Guide:** All modules follow the Rust Style Guide (rustfmt defaults). Functions are named with verb-noun convention. Files are named after the module they contain.
> **Linting Configuration:** cargo clippy is configured in `Cargo.toml` under `[lints]`. All CI builds must pass the linter before merge.

**Incorrect example:**
> We use tabs for indentation and camelCase for variables. Our linter catches some errors.
> *Why wrong: Missing rationale, missing configuration location, no connection to engineering principles.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Reference the specific style guide. Document linting config location and key rules. Explain non-obvious conventions.
- **Don't:** Assume universal knowledge. Omit config locations. Describe feature-specific patterns.

---

### 7. Constraints

**Template:**

```markdown
## Constraints

> [metadata block]

[1–2 paragraphs: overview of non-functional requirements and engineering limitations]

### Performance Constraints

| Constraint | Threshold | Source | Verifiability |
|-----------|-----------|--------|---------------|
| [Constraint name] | [specific value] | [where it comes from] | [how to verify] |

### Security Constraints

| Constraint | Requirement | Source | Verifiability |
|-----------|-------------|--------|---------------|
| [Constraint name] | [specific requirement] | [where it comes from] | [how to verify] |

### Compliance Constraints

[Optional: regulatory, organizational policy requirements]
```

**Correct example:**
> ### Performance Constraints
> | Constraint | Threshold | Source | Verifiability |
> |-----------|-----------|--------|---------------|
> | API response time | ≤200ms at p95 | Architecture Section 4.3 | Load testing |

**Incorrect example:**
> The application should be fast and secure. We follow industry best practices.
> *Why wrong: Not verifiable, no specific thresholds, no source attribution.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Categorize by type. Cite source. Make verifiable with specific thresholds.
- **Don't:** State vague requirements. Omit source attribution. List without categorization.

---

### 8. Traceability

**Template:**

```markdown
## Traceability

> [metadata block]

[1 paragraph: non-contradiction constraint and traceability principle]

> **diagram:** flowchart showing derivation chain

### Upstream Sources

[List of upstream documents that feed into Engineering]

### Downstream Consumers

[List of downstream documents that derive from Engineering]
```

**Correct example:**
> **Upstream Sources:** Architecture(05) provides system-wide design decisions. External Context provides compliance and platform constraints. **Downstream Consumers:** Implementation derives build, test, and code conventions from this document. Feature Technical Design references engineering standards for technology conformance. **Non-contradiction rule:** No downstream document may contradict a standard established here.

**Incorrect example:**
> This document traces to Architecture.
> *Why wrong: Missing downstream consumers, no non-contradiction rule, no derivation diagram.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** architect
- **Do:** Include a derivation diagram. List every upstream source and downstream consumer. State non-contradiction rule as enforceable.
- **Don't:** Leave derivation paths implicit. Omit downstream consumers. Use traceability as a summary rather than a verifiable chain.

---

## Output Contract

Output a single complete markdown document containing all 8 sections above, in the order listed. Each section must:

1. Use the template skeleton as its structural basis
2. Fill every placeholder with domain-appropriate content (not lorem ipsum)
3. Satisfy the Writing Guidance for its section
4. Be consistent with every other section (cross-section coherence constraint above)
5. Include diagrams where Required diagrams are specified
6. Omit implementation details — explain rationale, not code
