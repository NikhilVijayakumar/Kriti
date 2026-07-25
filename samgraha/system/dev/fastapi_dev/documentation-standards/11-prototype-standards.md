# Prototype Standard

## Table of Contents

> *Deterministic rules for this domain: `audit/deterministic/document/11-prototype.yaml`*

- [Purpose](#purpose)
- [Plan Scenarios](#plan-scenarios)
- [Mock APIs](#mock-apis)
- [Data Model](#data-model)
- [Constraints](#constraints)
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
- [Generation Rules](#generation-rules)
- [Enhancement Rules](#enhancement-rules)
- [Audit Rules](#audit-rules)
- [Validation Rules](#validation-rules)
- [Summary](#summary)
- [Common Mistakes](#common-mistakes)
- [Documentation Folder](#documentation-folder)
- [Usage](#usage)
- [Related](#related)
- [Prohibited Content](#prohibited-content)
- [Quality Requirements](#quality-requirements)
- [Prototype Endpoints](#prototype-endpoints)


---


## Purpose

> *Structural rules: `audit/deterministic/section/11-prototype/04-purpose.yaml`*

### Template

> **minimum_content:** 2 paragraphs
> **length_guidance:** concise
> **diagram_requirements:** none

[State the falsifiable question this prototype answers]
[Explain that this is a disposable simulation, not production code]
[State which upstream documents this prototype validates]

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Feature Design(09), Feature Technical Design(10)

### Examples

**Correct:**
> This prototype answers whether a real-time search interface can return results within 200ms on a 3G connection. It is a disposable simulation — not production code — and validates the interaction flow defined in Feature Design(09) and the data access pattern proposed in Feature Technical Design(10).

**Incorrect:**
> This document covers the Order Tracking feature and describes the system architecture.
> *Why wrong: No falsifiable question is stated, the prototype is not identified as disposable, and no upstream documents are referenced.*

### Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Lead with the falsifiable question in one sentence; state explicitly that the prototype is disposable; name the upstream documents by title and number
- **Don't:** Describe production architecture or implementation details; omit the falsifiable question or leave it vague; present the prototype as permanent or reusable

This document defines the standard for Prototype Documentation within the engineering documentation ecosystem.

A Prototype is an executable simulation of the application built to answer a specific falsifiable question or de-risk a specific unknown before production engineering commits to an approach.

A Prototype is **not** production implementation.

It is a disposable artifact scoped to one question, evaluated once, and discarded or replaced.

Prototype validates Feature Design and Feature Technical Design by exercising them against real interaction before Engineering builds the production version.

---

## Plan Scenarios

Not every prototype plan covers the entire project. The plan type depends on what is being prototyped and why.

### Full Generation

> **scenario:** New project or major feature set — prototype all uncertain features before implementation begins
> **scope:** Entire project or feature set
> **inputs:** Feature(04) requirements, Architecture(05) system boundaries, Design(06) UX direction
> **outputs:** Complete prototype plan covering all features, with separate frontend and backend prototypes per feature

Use Full Generation when:
- Starting a new project with significant unknowns
- Multiple features have technical uncertainty
- The team needs to validate the overall approach before committing

Full Generation produces a per-feature prototype plan. Each feature gets its own prototype with separate frontend and backend scopes.

### Enhancement

> **scenario:** Existing project — prototype a specific new feature or improve an existing one
> **scope:** Per feature or per section (UI only, backend only)
> **inputs:** Feature(04) for the specific feature, relevant upstream docs
> **outputs:** Targeted prototype plan for the specific feature or section

Use Enhancement when:
- Adding a new feature that has technical uncertainty
- Improving an existing feature's approach
- Prototyping a specific section (UI interaction, API contract, data flow)

Enhancement produces a focused prototype plan. Scope is limited to the feature or section being prototyped.

### Scope Options

| Scope | When to Use | Required Inputs |
|-------|-------------|-----------------|
| Entire project | New project with multiple unknowns | All upstream docs |
| Per feature | New uncertain feature | Feature(04) + relevant upstream |
| Frontend only | UI/UX uncertainty | Feature Design(09) + Design(06) |
| Backend only | API/data uncertainty | Architecture(05) + Engineering(07) |
| Per section | Specific component uncertainty | Component-specific upstream docs |

---

## Required Sections

Every Prototype document must contain the following sections.
Sections are identified by heading text; the compiler maps each to a semantic type.

| Section | semantic_type | Required | Aliases | Content Requirements |
|---------|--------------|----------|---------|---------------------|
| Scope | `scope` | ✓ | Coverage, What Is Covered | In-scope and out-of-scope lists with fidelity levels per item |
| Mock APIs | `mock_apis` | ✓ | Mocked APIs, API Contracts, Simulated APIs | Each mocked dependency with request/response contract and fidelity indicator |
| Data Model | `data_model` | ✓ | Data Structures, Schema | Minimal data structures and seed data; no PII or production data |
| Constraints | `constraints` | | Limitations, Non-Functional Requirements | Each constraint with type (hard/known-shortcoming) and impact |
| Traceability | `traceability` | | Traces To, Derived From | Text diagram showing upstream sources and downstream consumers |
| Purpose | `purpose` | | Overview, Summary | Falsifiable question, disposable nature, relationship to upstream documents |

Section headings are case-insensitive. Sections not listed here are stored as `generic` type — preserved but not queryable by type.

---

## Mock APIs

> *Structural rules: `audit/deterministic/section/11-prototype/02-mock_apis.yaml`*

### Template

> **minimum_content:** 1 paragraph + 1 table per mock
> **length_guidance:** moderate
> **diagram_requirements:** none

[List all mocked dependencies]

| Dependency | Fidelity | Request Contract | Response Contract |
|------------|----------|------------------|-------------------|
| [name] | [low|medium|high] | [request structure] | [response structure] |

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Scope, Data Model

### Examples

**Correct:**
> | Dependency | Fidelity | Request Contract | Response Contract |
> |------------|----------|------------------|-------------------|
> | Payment Gateway | low | POST /charge {amount, currency} | {status: "approved", id: "ch_123"} |
> | Inventory Service | medium | GET /stock/{sku} | {sku: "WIDGET-01", quantity: 42} |
>
> Payment Gateway is low fidelity because the prototype only tests the happy path. Inventory Service is medium fidelity because it returns realistic stock levels for the scenario.

**Incorrect:**
> | Dependency | Request Contract | Response Contract |
> |------------|------------------|-------------------|
> | Payment Gateway | POST /charge | {status: "approved"} |
> *Why wrong: The fidelity indicator column is missing. Without knowing whether the mock is low, medium, or high fidelity, reviewers cannot assess what the prototype actually simulates versus what is faked.*

### Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** List every mocked dependency in a table with a fidelity column; explain the fidelity choice for each mock in a sentence after the table; use concrete request/response examples with realistic field names
- **Don't:** Omit the fidelity indicator for any dependency; use vague descriptions like "some mock data"; include real production endpoints or credentials in the contract

> **⚠️ IMPORTANT:** This section is required by the Prototype standard but does not yet exist as a heading. Please add it when drafting a real Prototype document.

---

## Data Model

> *Structural rules: `audit/deterministic/section/11-prototype/03-data_model.yaml`*

### Template

> **minimum_content:** 1 paragraph + schema or table
> **length_guidance:** moderate
> **diagram_requirements:** none

[Data structures needed for the scenario]

```json
{
  "entity_name": {
    "field": "type — description"
  }
}
```

**Seed data:** [realistic but fake data, no PII or production values]

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Mock APIs

### Examples

**Correct:**
> ```json
> {
>   "order": {
>     "id": "string — unique order identifier",
>     "status": "string — pending | confirmed | shipped",
>     "total": "number — order total in cents"
>   }
> }
> ```
>
> **Seed data:** `{ "id": "ORD-001", "status": "pending", "total": 4999 }`
>
> Minimal structure exercises the checkout flow. No PII — customer name is not included because the prototype does not test profile management.

**Incorrect:**
> ```json
> {
>   "customer": {
>     "id": "string — unique identifier",
>     "name": "string — full legal name",
>     "email": "string — personal email address",
>     "ssn": "string — social security number"
>   }
> }
> ```
>
> **Seed data:** `{ "name": "John Smith", "email": "john@example.com", "ssn": "123-45-6789" }`
> *Why wrong: Contains PII fields (name, email, SSN) and seed data uses realistic personal information. The data model is not minimal — it includes fields irrelevant to the prototype scenario.*

### Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Define only the fields the prototype scenario exercises; provide seed data that is realistic but entirely fake; explain why excluded fields are not in scope
- **Don't:** Include PII, real email addresses, or production identifiers; replicate the full production schema; add fields that do not serve the falsifiable question

> **⚠️ IMPORTANT:** This section is required by the Prototype standard but does not yet exist as a heading. Please add it when drafting a real Prototype document.

---

## Constraints

> *Structural rules: `audit/deterministic/section/11-prototype/05-constraints.yaml`*

### Template

> **minimum_content:** 1 constraint list
> **length_guidance:** concise
> **diagram_requirements:** none

| Constraint | Type | Impact |
|------------|------|--------|
| [constraint] | [hard|known-shortcoming] | [effect on prototype] |

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Scope

### Examples

**Correct:**
> | Constraint | Type | Impact |
> |------------|------|--------|
> | No network access | hard | All external services must be mocked locally |
> | Response time not measured | known-shortcoming | Prototype does not validate latency — that is deferred to Engineering |
>
> The hard constraint shapes the entire mock strategy. The known-shortcoming is honest about what the prototype does not prove.

**Incorrect:**
> | Constraint | Type | Impact |
> |------------|------|--------|
> | API latency under 200ms | hard | Response time must meet production SLA |
>
> *Why wrong: This is a production performance requirement, not a prototype constraint. The prototype does not validate production latency — that belongs in Engineering(07) or Feature Technical Design(10).*

### Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** Classify each constraint as either hard or known-shortcoming; describe the concrete impact on the prototype for each entry; keep constraints specific to the prototype's simulation scope
- **Don't:** List production performance targets or SLAs as prototype constraints; describe preferences or nice-to-haves as constraints; leave the Impact column blank or vague

## Goals

Prototype aims to:

* Answer one falsifiable question before production engineering commits.
* Keep the simulation scoped and disposable.
* Give stakeholders something to react to before real cost is spent.

---

## Non-Goals

Prototype does not define:

* Product Vision
* Architecture
* Production Engineering Decisions
* Long-term Data Governance

These responsibilities belong to other documentation standards.

---

## Success Criteria

Prototype is successful when:

* Stakeholders can evaluate the falsifiable question the prototype was built to answer.
* Feature Design and/or Feature Technical Design gain (or lose) confidence as a direct result.
* The prototype is discarded or explicitly promoted, not left to rot as accidental production code.

---

## Responsibilities

Prototype is responsible for defining:

* The falsifiable question the simulation answers
* Success and failure thresholds for that question
* What is simulated versus what is real
* Mock or stubbed external dependencies
* A minimal data model sufficient to exercise the scenario
* Known limitations and assumptions

Prototype turns a Feature Design or Feature Technical Design into something a stakeholder can react to before it's built for real.

---

## Scope

> *Structural rules: `audit/deterministic/section/11-prototype/01-scope.yaml`*

### Template

> **minimum_content:** 2 lists (in-scope + out-of-scope)
> **length_guidance:** moderate
> **diagram_requirements:** none

**Falsifiable question:** [the question this prototype answers]

**In-scope:**
- [item] — fidelity: [mocked|stubbed|partial|full]

**Out-of-scope:**
- [item] — reason: [why excluded]

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Goals, Success Criteria

### Examples

**Correct:**
> **Falsifiable question:** Can a search-as-you-type interface return results within 200ms on a 3G connection?
>
> **In-scope:**
> - Search input field — fidelity: full
> - Results list rendering — fidelity: mocked
> - Network latency simulation — fidelity: partial
>
> **Out-of-scope:**
> - User authentication — reason: not relevant to the search interaction
> - Result ranking algorithm — reason: deferred to Feature Technical Design(10)
>
> Each item has a fidelity level, and out-of-scope items explain why they are excluded.

**Incorrect:**
> **Falsifiable question:** Can the search feature work?
>
> **In-scope:**
> - Search
> - Results
> - Filters
>
> **Out-of-scope:**
> - Nothing — the prototype covers everything
> *Why wrong: The question is not falsifiable ("can it work" has no pass/fail threshold), no fidelity levels are assigned to scope items, and nothing is excluded — the prototype has no boundaries.*

### Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** State the falsifiable question before listing scope; assign a fidelity level to every in-scope item; provide a reason for every out-of-scope exclusion
- **Don't:** Leave the falsifiable question vague or untestable; list items without fidelity levels; claim "nothing is out of scope" — a prototype without boundaries is not a prototype

Prototype may describe:

* In-scope and out-of-scope behavior
* Fidelity level per scope item (mocked, stubbed, partial, full)
* Simulated interaction flows
* Mocked external dependencies
* Minimal data model and seed data
* Known limitations and assumptions

Every Prototype should remain scoped to one falsifiable question.

---

## Out of Scope

Prototype must not describe:

* Product Vision
* Design Philosophy
* Architecture
* Production data governance
* Production security posture
* Production performance targets
* Long-term maintainability

Production concerns belong to Feature Technical Design and Engineering. A Prototype that tries to be production-ready has stopped being a prototype.

---

## Inputs

Prototype derives from:

* Feature Design — the UX it validates
* Feature Technical Design — the technical plan it validates

Prototype should not derive from Implementation — it comes before Implementation, not after.

---

## Outputs

Prototype provides:

* Confidence (or lack of it) that Feature Design and Feature Technical Design are viable
* A validated approach that Implementation may follow

Prototype code itself is not an output — it's discarded once the question is answered.

---

## Traceability

> *Structural rules: `audit/deterministic/section/11-prototype/06-traceability.yaml`*

### Template

> **minimum_content:** 1 text diagram
> **length_guidance:** concise
> **diagram_requirements:** flowchart

```text
[Upstream Doc A] ──┐
                    ├──> Prototype ── validates ──> [downstream impact]
[Upstream Doc B] ┘
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** traceability flowchart
**Required cross-references:** Feature Design(09), Feature Technical Design(10)

### Examples

**Correct:**
> ```text
> Feature Design(09)     ──┐
>                            ├──> Prototype ── validates ──> confidence to proceed with Implementation(13)
> Feature Technical(10)  ──┘
> ```
>
> Both upstream documents are named. The downstream impact — confidence for Implementation — is explicit.

**Incorrect:**
> ```text
> Some Docs ──┐
>              ├──> Prototype ──> ??? 
> More Docs ──┘
> ```
> *Why wrong: Upstream documents are not identified by name or number. The downstream impact is unclear. This diagram could belong to any prototype and provides no traceable lineage.*

### Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** diagrams
- **Audience:** architect
- **Do:** Name each upstream document by title and number in the diagram; show the validation direction from Prototype to downstream impact; keep the diagram minimal with one arrow per relationship
- **Don't:** Use generic labels like "some docs" or "more docs"; omit the downstream impact of the prototype; include unrelated documents or internal section-level traceability

```text
Feature Design ──┐
                  ├──> Prototype ── validates ──> confidence to proceed
Feature Technical ┘
```

Every Prototype should trace to the Feature Design and/or Feature Technical document it validates.

---

## Relationships

| Document          | Relationship                    |
| ------------------ | -------------------------------- |
| Feature Design     | Prototype validates it            |
| Feature Technical   | Prototype validates it            |

---

## Required Characteristics

Prototype should be:

* Scoped to one falsifiable question
* Disposable
* Independently runnable without external network
* Free of production credentials or PII
* Honest about fidelity level per scope item

---

## Generation Rules

When generating Prototype documentation:

* State the falsifiable question the prototype answers.
* Define success criteria before building the prototype.
* Document scope boundaries and excluded areas.
* Record the decision made from prototype results.
* Mark the prototype as disposable — not production code.

---

## Enhancement Rules

When enhancing Prototype documentation:

* Verify the original question was answered.
* Update results if the prototype is re-executed.
* Ensure the disposition (adopt/reject/iterate) is recorded.
* Remove or archive prototypes that are no longer relevant.
* Preserve the reasoning behind go/no-go decisions.

---

## Audit Rules

An audit should verify:

* Scope is present (error if missing).
* Mock APIs are documented (warning if missing).
* The prototype is disposable — no production implementation claims (warning if violated).

---

## Validation Rules

Prototype is considered valid when:

* Scope is documented with in-scope and out-of-scope lists.
* Every external dependency has a mock or stub.
* The data model is minimal and free of production data or PII.
* The question the prototype answers has explicit success and failure thresholds.
* No production implementation is presented as final.

---

## Summary

Prototype Documentation is a disposable, executable simulation scoped to one falsifiable question, built to validate a Feature Design or Feature Technical Design before Engineering commits to production implementation.

---

## Common Mistakes

Examples include:

* Building a prototype with no stated question ("see if it works").
* Letting scope grow into a second production effort.
* Mocks that silently call real production endpoints.
* Treating the prototype's disposable code as reusable.
* Embedding production credentials in mock configuration.

These should be reported during audits.

---

## Documentation Folder

Prototype documents live under:

```text
docs/raw/prototype/
```

---

## Usage

Written when a Feature Design or Feature Technical decision carries enough risk to warrant proof before production engineering starts. Use `samgraha audit --domain prototype` to confirm scope and mock APIs are documented and no production implementation leaked in.

## Related

- [Feature Technical Standard](10-feature-technical-standards.md) — the other document this standard validates
- [Standards Reference Standard](standards.md) — how this standard itself is documented

## Prohibited Content

A Prototype document must not contain:

* Production implementation

Prototype code is disposable by definition; presenting it as production-ready is a documentation defect, not a strength.

---

## Quality Requirements

Prototype should be:

* Scoped to one falsifiable question
* Explicit about success/failure thresholds
* Disposable
* Independently runnable without external network
* Free of production credentials or PII

---


## Prototype Endpoints

> *Structural rules: `audit/deterministic/section/11-prototype/03-prototype-endpoints.yaml`*

### Template

> **minimum_content:** 1 endpoint description
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
When prototyping backend features:

* **OpenAPI Specs:** Prototyping often involves defining and validating the API contract first (e.g., using Swagger/ReDoc).
* **Mock Responses:** Create endpoints that return static mock data matching the proposed schema to unblock frontend development.
* **Falsifiability:** The prototype should prove the data contract can satisfy the business requirement before writing the full implementation.

### [Endpoint Name]

[Method] [Path]
[Describe the static response model and any query parameters supported in the prototype.]
```

**Required subsections:** Endpoint Name
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> ### Get Users
> `GET /api/v1/users`
> Returns a static list of 3 `UserResponse` objects. Supports the `?role=admin` filter for testing.

**Incorrect:**
> We will have a mock server running.
> *Why wrong: Lacks specifics about which endpoints are mocked and their contracts.*

### Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** subsections per endpoint
- **Audience:** frontend engineers
- **Do:** Define the exact HTTP method, path, and response schema.
- **Don't:** Rely on generic mock servers; prototype using the actual backend app with mocked returns.
