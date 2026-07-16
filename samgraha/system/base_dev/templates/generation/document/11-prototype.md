# Prototype Document — Generation Template

> **Domain:** prototype
> **Source standard:** `documentation-standards/11-prototype-standards.md`
> **Coherence source:** `audit/semantic/document/11-prototype.md`
> **Relationships:** `audit/deterministic/document/11-prototype-relationships.yaml`

Generate a complete Prototype document for a system. The document must satisfy every required section below, in the order defined by the standard.

## Required Sections

| # | Section | semantic_type | Required | Content Requirements |
|---|---------|--------------|----------|---------------------|
| 1 | Purpose | `purpose` | | Falsifiable question, disposable nature, relationship to upstream documents |
| 2 | Scope | `scope` | ✓ | In-scope and out-of-scope lists with fidelity levels per item |
| 3 | Mock APIs | `mock_apis` | ✓ | Each mocked dependency with request/response contract and fidelity indicator |
| 4 | Data Model | `data_model` | ✓ | Minimal data structures and seed data; no PII or production data |
| 5 | Constraints | `constraints` | | Each constraint with type (hard/known-shortcoming) and impact |

## Cross-Section Coherence Constraint

> Sourced from `audit/semantic/document/11-prototype.md` Engineering Intent.

Scope, Mock APIs, and Data Model must describe the same prototype simulation without contradicting each other. Specifically:

- Every in-scope item with mocked fidelity must have a corresponding entry in Mock APIs
- The Data Model must contain only fields exercised by in-scope items
- Out-of-scope items must not appear in Mock APIs or Data Model
- The falsifiable question stated in Scope must be answerable by the combination of Mock APIs and Data Model
- The collection as a whole must read as one prototype plan, not several independent descriptions

If any section would introduce a dependency, data field, or scope item not present in another section, reconcile before outputting.

## Sections

---

### 1. Purpose

**Template:**

```markdown
## Purpose

> **Falsifiable question:** [the specific question this prototype answers]

> **Disposable nature:** This is a disposable simulation — not production code. It is evaluated once and discarded or replaced.

> **Upstream validation:** This prototype validates [upstream document 1] and [upstream document 2].
```

> **Generation note:** When generating for a specific system, fill this template with *that prototype's* purpose: the falsifiable question it answers and which upstream documents it validates. The meta-level "This document defines the standard for Prototype Documentation..." language belongs in the standard itself, not in a generated document.

**Correct example:**
> **Falsifiable question:** Can a real-time search interface return results within 200ms on a 3G connection?
>
> **Disposable nature:** This is a disposable simulation — not production code. It is evaluated once and discarded or replaced.
>
> **Upstream validation:** This prototype validates Feature Design(09) §Search UX and Feature Technical Design(10) §Search Component Interactions.

**Incorrect example:**
> This document covers the Order Tracking feature and describes the system architecture.
> *Why wrong: no falsifiable question is stated, the prototype is not identified as disposable, and no upstream documents are referenced.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Lead with the falsifiable question in one sentence; state explicitly that the prototype is disposable; name the upstream documents by title and number
- **Don't:** Describe production architecture or implementation details; omit the falsifiable question; present the prototype as permanent or reusable

---

### 2. Scope

**Template:**

```markdown
## Scope

**Falsifiable question:** [the question this prototype answers]

**In-scope:**
- [item] — fidelity: [mocked|stubbed|partial|full]

**Out-of-scope:**
- [item] — reason: [why excluded]
```

**Correct example:**
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

**Incorrect example:**
> **Falsifiable question:** Can the search feature work?
>
> **In-scope:**
> - Search
> - Results
> - Filters
>
> **Out-of-scope:**
> - Nothing — the prototype covers everything
> *Why wrong: the question is not falsifiable, no fidelity levels are assigned, and nothing is excluded.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** State the falsifiable question before listing scope; assign a fidelity level to every in-scope item; provide a reason for every out-of-scope exclusion
- **Don't:** Leave the question vague or untestable; list items without fidelity levels; claim "nothing is out of scope"

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Goals, Success Criteria

---

### 3. Mock APIs

**Template:**

```markdown
## Mock APIs

[List all mocked dependencies]

| Dependency | Fidelity | Request Contract | Response Contract |
|------------|----------|------------------|-------------------|
| [name] | [low|medium|high] | [request structure] | [response structure] |

[Fidelity justification for each mock]
```

**Correct example:**
> | Dependency | Fidelity | Request Contract | Response Contract |
> |------------|----------|------------------|-------------------|
> | Payment Gateway | low | POST /charge {amount, currency} | {status: "approved", id: "ch_123"} |
> | Inventory Service | medium | GET /stock/{sku} | {sku: "WIDGET-01", quantity: 42} |
>
> Payment Gateway is low fidelity because the prototype only tests the happy path. Inventory Service is medium fidelity because it returns realistic stock levels for the scenario.

**Incorrect example:**
> | Dependency | Request Contract | Response Contract |
> |------------|------------------|-------------------|
> | Payment Gateway | POST /charge | {status: "approved"} |
> *Why wrong: the fidelity indicator column is missing. Without knowing fidelity level, reviewers cannot assess what the prototype actually simulates.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** List every mocked dependency with a fidelity column; explain the fidelity choice after the table; use concrete request/response examples with realistic field names
- **Don't:** Omit the fidelity indicator; use vague descriptions; include real production endpoints or credentials

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Scope, Data Model

---

### 4. Data Model

**Template:**

```markdown
## Data Model

[Data structures needed for the scenario]

```json
{
  "entity_name": {
    "field": "type — description"
  }
}
```

**Seed data:** [realistic but fake data, no PII or production values]

[Justification for included and excluded fields]
```

**Correct example:**
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

**Incorrect example:**
> ```json
> {
>   "customer": {
>     "name": "string — full legal name",
>     "email": "string — personal email address",
>     "ssn": "string — social security number"
>   }
> }
> ```
>
> **Seed data:** `{ "name": "John Smith", "email": "john@example.com", "ssn": "123-45-6789" }`
> *Why wrong: contains PII fields and seed data uses realistic personal information. The data model is not minimal.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Define only the fields the prototype scenario exercises; provide seed data that is realistic but entirely fake; explain why excluded fields are not in scope
- **Don't:** Include PII, real email addresses, or production identifiers; replicate the full production schema; add fields that do not serve the falsifiable question

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Mock APIs

---

### 5. Constraints

**Template:**

```markdown
## Constraints

| Constraint | Type | Impact |
|------------|------|--------|
| [constraint] | [hard|known-shortcoming] | [effect on prototype] |
```

**Correct example:**
> | Constraint | Type | Impact |
> |------------|------|--------|
> | No network access | hard | All external services must be mocked locally |
> | Response time not measured | known-shortcoming | Prototype does not validate latency — that is deferred to Engineering |
>
> The hard constraint shapes the entire mock strategy. The known-shortcoming is honest about what the prototype does not prove.

**Incorrect example:**
> | Constraint | Type | Impact |
> |------------|------|--------|
> | API latency under 200ms | hard | Response time must meet production SLA |
> *Why wrong: this is a production performance requirement, not a prototype constraint.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** engineer
- **Do:** Classify each constraint as either hard or known-shortcoming; describe the concrete impact on the prototype; keep constraints specific to the prototype's simulation scope
- **Don't:** List production performance targets as prototype constraints; describe preferences as constraints; leave the Impact column blank

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Scope

## Output Contract

Output a single complete markdown document containing all 5 sections above, in the order listed. Each section must:

1. Use the template skeleton as its structural basis
2. Fill every placeholder with domain-appropriate content (not lorem ipsum)
3. Satisfy the Writing Guidance for its section
4. Be consistent with every other section (cross-section coherence constraint above)
5. Omit implementation details (technology names, library versions, configuration values, code snippets)
6. Remain disposable — no production implementation claims
