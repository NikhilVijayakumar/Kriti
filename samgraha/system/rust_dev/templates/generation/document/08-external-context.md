# External Context Document — Generation Template

> **Domain:** external-context
> **Source standard:** `documentation-standards/08-external-context-standards.md`
> **Coherence source:** `audit/semantic/document/08-external-context.md`
> **Relationships:** `audit/deterministic/document/08-external-context-relationships.yaml`

Generate a complete External Context document for a single external dependency. The document must satisfy every required section below, in the order defined by the standard.

## Required Sections

| # | Section | semantic_type | Required | Content Requirements |
|---|---------|--------------|----------|---------------------|
| 1 | Purpose | `purpose` | ✓ | Why this external dependency exists, what knowledge it imposes, distinction from package dependency documentation; atomic-per-dependency principle |
| 2 | Integration Contract | `integration_contract` | ✓ | Endpoints, protocols, data formats, authentication, error behaviors, versioning; reference authoritative API docs; ALL subsections included in this one section |
| 3 | Constraints | `constraints` | | Categorized limitations (functional, performance, legal, compliance) sourced from the external system; ALL subsections included in this one section |
| 4 | Dependencies | `dependencies` | | Transitive requirements, platform prerequisites, companion systems; distinguish runtime from build-time; note criticality; ALL subsections included in this one section |
| 5 | Traceability | `traceability` | ✓ | Tier diagram showing External Context's lateral position; list of consuming standards; non-duplication rule stated |

## Cross-Section Coherence Constraint

> Sourced from `audit/semantic/document/08-external-context.md` Engineering Intent.

All sections must be mutually consistent — no contradictions between Integration Contract capabilities and Constraints limitations, between Dependencies and Integration Contract availability requirements, or between any two sections. If Integration Contract describes a rate-limited endpoint, Constraints must document the exact rate limit. If Dependencies lists a critical runtime service, Integration Contract must reflect its availability constraints. Terminology must be consistent across all sections: same concept, same name.

## Sections

---

### 1. Purpose

**Template:**

```markdown
## Purpose

[1 sentence: what this external dependency is and why it exists in this project's ecosystem]

[1 sentence: what knowledge contributors need about this dependency to implement integrations correctly]

[1 sentence: distinction from package dependency documentation — this documents knowledge, not package manifests]

[1 sentence: the atomic-per-dependency principle — one document per external dependency]
```

**Correct example:**
> Prana is the shared runtime that provides event-driven message routing for all Saṃgraha subsystems. Contributors need to understand Prana's subscription model, delivery guarantees, and retry semantics to implement integration points correctly. This document captures knowledge dependencies — the understanding contributors need about Prana — not package manifests or version management. Each External Context document describes a single external dependency, making the collection atomic and independently maintainable.

**Incorrect example:**
> External Context Documentation covers npm packages, pip dependencies, and Cargo crates required by the project.
> *Why wrong: Conflates External Context with package dependency documentation.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** State what the external dependency is. Draw clear boundary between knowledge and package dependencies. Reference atomic-per-dependency principle.
- **Don't:** Describe internal architecture. List package managers. Use motivational language.

---

### 2. Integration Contract

**Template:**

```markdown
## Integration Contract

[Integration surface overview — what the external system exposes]

### Endpoints / Protocols

| Endpoint / Protocol | Purpose | Method | Required | Authentication | Notes |
|--------------------|---------|--------|----------|---------------|-------|
| [Path or protocol name] | [what it does] | [HTTP method / protocol type] | [yes/no] | [auth type] | [constraints] |

### Data Formats

| Direction | Format | Content Type | Encoding | Constraints |
|-----------|--------|-------------|----------|-------------|
| Request | [format] | [MIME type] | [encoding] | [limits] |
| Response | [format] | [MIME type] | [encoding] | [limits] |

### Authentication

| Aspect | Detail |
|--------|--------|
| Mechanism | [OAuth 2.0, API key, mutual TLS, etc.] |
| Flow | [client credentials, authorization code, etc.] |
| Token type | [Bearer, MAC, etc.] |
| Token lifetime | [expiration duration] |
| Refresh | [supported / not supported] |
| Credential storage | [how credentials should be stored] |

### Error Handling

| Error Code / Status | Meaning | Retry | Backoff Strategy |
|---------------------|---------|-------|-----------------|
| [code] | [what it means] | [yes/no] | [strategy] |

### Versioning

| Aspect | Detail |
|--------|--------|
| Versioning scheme | [URL path, header, query parameter] |
| Current version | [version identifier] |
| Deprecation policy | [how deprecation is communicated] |
| Migration guidance | [how to upgrade between versions] |
```

**Correct example:**
> The external system exposes a REST API over HTTPS. Authentication uses OAuth 2.0 client credentials flow.
>
> | Endpoint / Protocol | Purpose | Method | Required | Authentication | Notes |
> |--------------------|---------|--------|----------|---------------|-------|
> | `/v1/data` | Submit data | POST | Yes | Bearer token | Max 1MB payload |
> | `/v1/data/{id}` | Retrieve data | GET | Yes | Bearer token | Returns 404 for deleted records |
>
> Authoritative documentation: `https://docs.externalsystem.example/api`.

**Incorrect example:**
> Here is the code we use to call the API:
> ```python
> resp = requests.post("https://api.externalsystem.example/v1/data", ...)
> ```
> *Why wrong: Includes implementation code rather than describing the contract.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** third person
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Describe contract surface in implementation-neutral terms. Always include authoritative documentation URL. Distinguish required from optional endpoints. Include ALL subsections (Endpoints/Protocols, Data Formats, Authentication, Error Handling, Versioning) as part of this one section.
- **Don't:** Paste code. Document internal transformation logic. Omit authentication details. Treat subsections as standalone sections.

---

### 3. Constraints

**Template:**

```markdown
## Constraints

[1 paragraph: overview of constraints the external system imposes on the repository]

### Functional Constraints

| Constraint | Limitation | Impact | Source |
|-----------|-----------|--------|--------|
| [Name] | [specific restriction] | [what this prevents] | [external source] |

### Performance Constraints

| Constraint | Limitation | Impact | Source |
|-----------|-----------|--------|--------|
| [Name] | [specific numeric limit] | [what this requires] | [external source] |

### Legal / Compliance Constraints

| Constraint | Requirement | Impact | Source |
|-----------|-------------|--------|--------|
| [Name] | [specific requirement] | [what this requires] | [external source] |
```

**Correct example:**
> ### Functional Constraints
> | Constraint | Limitation | Impact | Source |
> |-----------|-----------|--------|--------|
> | Max payload | 1 MB per request | Large file uploads must be chunked | Platform API documentation §3.2 |
>
> ### Performance Constraints
> | Constraint | Limitation | Impact | Source |
> |-----------|-----------|--------|--------|
> | Rate limit | 100 requests/minute | Request throttling needed for batch operations | Platform service limits |

**Incorrect example:**
> We decided to use connection pooling because our application needs high throughput.
> *Why wrong: Internal design decision, not a constraint imposed by the external system.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** third person
- **Structure:** bullet lists / tables
- **Audience:** architect
- **Do:** Categorize by type. Cite external source. State numeric limits where possible. Include ALL subsections as part of this one section.
- **Don't:** List internal decisions. Use vague qualifiers. Omit compliance constraints. Treat subsections as standalone sections.

---

### 4. Dependencies

**Template:**

```markdown
## Dependencies

[1 paragraph: overview of transitive requirements the external system itself needs]

### Runtime Dependencies

| Dependency | Purpose | Criticality | Behavior if Unavailable | Source |
|-----------|---------|-------------|------------------------|--------|
| [Name] | [what it provides] | [critical/nice-to-have] | [what fails] | [where documented] |

### Build-Time Dependencies

| Dependency | Purpose | Criticality | Behavior if Unavailable | Source |
|-----------|---------|-------------|------------------------|--------|
| [Name] | [what it provides] | [critical/nice-to-have] | [what fails] | [where documented] |
```

**Correct example:**
> ### Runtime Dependencies
> | Dependency | Purpose | Criticality | Behavior if Unavailable | Source |
> |-----------|---------|-------------|------------------------|--------|
> | Message broker | Webhook delivery | Critical | Webhooks fail silently | Platform documentation §6.2 |
>
> These are transitive requirements of the platform itself, not choices made by this repository.

**Incorrect example:**
> This project depends on Express.js for HTTP routing and Jest for testing.
> *Why wrong: Internal project dependencies, not transitive dependencies of the external system.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** third person
- **Structure:** tables
- **Audience:** architect
- **Do:** Distinguish runtime from build-time. Note criticality. Cross-reference other External Context documents for documented transitive dependencies. Include ALL subsections as part of this one section.
- **Don't:** List package.json entries. Include dev tooling. Omit companion systems. Treat subsections as standalone sections.

---

### 5. Traceability

**Template:**

```markdown
## Traceability

### Influence Diagram

```text
Vision
  ↓
Features
  ↓
Feature Design
  ↓
Architecture
  ↓
Feature Technical Design
  ↓
Engineering

         ↑

 External Context
```

External Context informs documentation. It does not redefine it.

### Consuming Standards

| Standard | How It References External Context |
|----------|-----------------------------------|
| Feature Technical Design (10) | [How this dependency's constraints and contract surface in technical designs] |
| Engineering (07) | [How this dependency's rationale and contract guide implementation] |
| Architecture (05) | [How this dependency's boundaries and platform requirements inform architecture] |
```

**Correct example:**
> External Context informs Feature Technical Design by surfacing integration constraints before implementation begins. It informs Architecture by revealing system boundaries and platform requirements. It informs Engineering by providing rationale for technology choices tied to the external dependency. Downstream standards **reference** External Context rather than duplicating its content.

**Incorrect example:**
> Traceability shows that External Context was last updated in March and is owned by the platform team.
> *Why wrong: Traceability means showing how External Context influences downstream standards, not tracking document metadata.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** third person
- **Structure:** diagrams + tables
- **Audience:** architect
- **Do:** Include a text-based tier diagram showing External Context's lateral position; list every downstream standard that consumes External Context by name; explicitly state the non-duplication rule (reference, don't copy).
- **Don't:** Include version history or changelog entries. Treat Traceability as document metadata. Omit a standard from the consuming list if it references External Context content.

---

## Output Contract

Output a single complete markdown document containing all 5 sections above, in the order listed. Each section must:

1. Use the template skeleton as its structural basis
2. Fill every placeholder with domain-appropriate content for the specific external dependency being documented (not lorem ipsum)
3. Satisfy the Writing Guidance for its section
4. Be consistent with every other section (cross-section coherence constraint above)
5. Include tables where template specifies them
6. Reference authoritative external documentation URLs throughout
7. Omit internal implementation details — describe what the external system exposes, not how the repository calls it
8. Keep subsections (Endpoints/Protocols, Data Formats, Authentication, Error Handling, Versioning under Integration Contract; Functional, Performance, Legal/Compliance under Constraints; Runtime, Build-Time under Dependencies) as part of their parent section, not as standalone sections
