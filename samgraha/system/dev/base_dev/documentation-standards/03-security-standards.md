# Security Standard

> *Deterministic rules for this domain: `audit/deterministic/document/03-security.yaml`*

## Table of Contents
- [Purpose](#purpose)
- [Threat Model](#threat-model)
- [Data Classification](#data-classification)
- [Security Principles](#security-principles)
- [Compliance Requirements](#compliance-requirements)
- [Incident Response](#incident-response)
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
- [Revision History](#revision-history)
- [Relationship to Per-Domain Security Sections](#relationship-to-per-domain-security-sections)
- [Quality Requirements](#quality-requirements)

---


## Purpose

> *Structural rules: `audit/deterministic/section/03-security/04-purpose.yaml`*

### Template

> **minimum_content:** 1–2 paragraphs
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
<!-- One paragraph: what Security defines and its role in the documentation hierarchy -->
<!-- One paragraph: what Security does not define, and where enforcement lives -->
```

**Required subsections:** none
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Vision(01), Philosophy(02)

### Examples

**Correct:**
> Security(03) establishes the project-wide threat model, data classification scheme, and security principles. It is the single source of truth for what the project defends against and why — every downstream domain's Security Considerations or Security Standards section derives from this document rather than re-deriving its own posture.

**Incorrect:**
> Security(03) defines the authentication middleware, rate-limiting configuration, and WAF rule set used across all services.
> *Why wrong: This describes specific control implementations (authentication middleware, rate limiting, WAF rules) — those belong in Engineering's Security Standards or Architecture's Security Considerations, not in the project-wide Security document.*

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** new contributor
- **Do:** State Security's role as the single project-wide authority; define the boundary between Security and per-domain sections explicitly; reference derivation from Vision(01) and Philosophy(02)
- **Don't:** Name specific controls, libraries, or tooling; use imperative voice; embed implementation details that belong in downstream domains

---

This document defines the standard for Security documentation within the engineering documentation ecosystem.

A Security document establishes the project-wide threat model, data classification scheme, security principles, and compliance posture that every other domain must operate within.

It defines **what the project is defending against and why**, once, at the project level — the same way Vision defines why the product exists and Philosophy defines the values guiding decisions.

It does not define how any single component enforces that posture. That belongs to each domain's own Security Considerations or Security Standards section.

---

## Threat Model

> *Structural rules: `audit/deterministic/section/03-security/01-threat_model.yaml`*

### Template

> **minimum_content:** 3–5 subsections
> **length_guidance:** extensive
> **diagram_requirements:** flowchart

```markdown
<!-- Methodology: state which threat-modeling methodology is used (STRIDE, PASTA, or OWASP) -->
<!-- Adversary Profiles: enumerate likely adversaries with motivation and capability -->
<!-- Threat Enumeration: list threats with category, severity, and affected assets -->
<!-- Attack Surfaces: identify external and internal surfaces -->
<!-- Downstream Expectations: map each threat to at least one domain that must address it -->
```

**Required subsections:** methodology, adversary profiles, threat enumeration, attack surfaces, downstream expectations
**Optional subsections:** trust assumptions, risk scoring matrix
**Required diagrams:** threat landscape overview (flowchart or table)
**Required cross-references:** Data Classification, Security Principles

### Examples

**Correct:**
> **Methodology:** STRIDE
> **Adversary Profile — External Attacker:** Motivated by financial gain; capability includes automated scanning, phishing, and exploiting known vulnerabilities. Target: user authentication flows and data export endpoints.
> **Threat — Tampering (STRIDE):** An attacker modifies payment amount during transit between checkout and billing. Severity: High. Affected asset: transaction integrity. Downstream expectation: Engineering must implement request signing or integrity checks.

**Incorrect:**
> Threat: Hackers might try to break in. Mitigation: We will use OWASP Top 10 and add WAF rules in the deployment pipeline.
> *Why wrong: No named methodology is used ("OWASP Top 10" is a list, not a methodology), the adversary profile is missing, severity is absent, and the mitigation embeds specific tooling (WAF) that belongs in Engineering's Security Standards.*

### Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** tables
- **Audience:** architect
- **Do:** Use a named methodology (STRIDE, PASTA, or OWASP Threat Modeling) consistently; link each threat to at least one downstream mitigation expectation; assign severity to every enumerated threat
- **Don't:** List specific tooling or library mitigations; enumerate per-component trust boundaries that belong in Architecture; use vague severity labels without justification

---

*(To be written by the domain expert. This section defines the project-wide threat model.)*

---

## Data Classification

> *Structural rules: `audit/deterministic/section/03-security/02-data_classification.yaml`*

### Template

> **minimum_content:** 2–3 subsections
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
<!-- Sensitivity Levels: define each level (e.g. Public, Internal, Confidential, Restricted) -->
<!--   For each level: description, one concrete example, handling expectations -->
<!-- Handling Expectations: cross-cutting rules (access control, encryption at rest/transit, retention) -->
<!-- Application: how downstream domains map their data to these levels -->
```

**Required subsections:** sensitivity levels, handling expectations
**Optional subsections:** data inventory examples, classification decision tree
**Required diagrams:** none
**Required cross-references:** Threat Model, Security Principles

### Examples

**Correct:**
> **Internal:** Data intended for project members only — internal documentation, architecture diagrams, meeting notes.
> **Handling:** Access restricted to authenticated project members; no external sharing without approval.
> **Confidential:** Data whose unauthorized disclosure would cause material harm — user PII, financial records, authentication secrets.
> **Handling:** Encrypted at rest and in transit; access logged and auditable; retention policy enforced.

**Incorrect:**
> Sensitive data goes in PostgreSQL with row-level security. Non-sensitive data goes in Elasticsearch.
> *Why wrong: This classifies data by storage technology rather than by sensitivity level — a new team member reading this cannot determine what "sensitive" means without knowing the infrastructure, and the classification is not technology-independent.*

### Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** tables
- **Audience:** engineer
- **Do:** Provide one concrete example per sensitivity level; state handling expectations (access control, encryption, retention) per level; keep classification technology-independent
- **Don't:** Classify data by storage location or database; embed encryption library or access-control implementation; omit handling expectations for any defined level

---

*(To be written by the domain expert. This section defines the data classification scheme.)*

---

## Security Principles

> *Structural rules: `audit/deterministic/section/03-security/03-security_principles.yaml`*

### Template

> **minimum_content:** 1–2 subsections
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
<!-- State each security principle with: -->
<!--   - Name: memorable, stable phrase -->
<!--   - Rationale: why this principle constrains design decisions -->
<!--   - Example decision it would constrain (optional but recommended) -->
<!-- Link principles back to Philosophy(02) guiding principles they specialize -->
```

**Required subsections:** none
**Optional subsections:** principle-to-decision examples, derivation from Philosophy
**Required diagrams:** none
**Required cross-references:** Philosophy(02), Threat Model

### Examples

**Correct:**
> **Principle:** Least Privilege by Default
> **Rationale:** Every component, service, and user must start with the minimum permissions required for its function — no more.
> **Decision it constrains:** Architecture's service-to-service communication design must not grant blanket access between services.

**Incorrect:**
> Security Principle: Be Secure. All code must follow security best practices.
> *Why wrong: This is a generic platitude that cannot constrain any concrete design decision — "best practices" is undefined, and "be secure" gives no evaluative criteria for a proposed design.*

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** State each principle with name, rationale, and at least one example decision it constrains; specialize Philosophy(02) guiding principles for the security context; ensure every principle is evaluable against a concrete design
- **Don't:** Write generic platitudes ("be secure", "follow best practices"); embed specific technology choices or library recommendations; list more than seven principles — keep the set focused and memorable

---

*(To be written by the domain expert. This section defines the project-wide security principles.)*

---

## Compliance Requirements

> *Structural rules: `audit/deterministic/section/03-security/07-compliance.yaml`*

### Template

> **minimum_content:** 2–3 subsections
> **length_guidance:** moderate
> **diagram_requirements:** none

```markdown
<!-- For each compliance regime: -->
<!--   - Name: regulatory or contractual body (e.g. GDPR, HIPAA, PCI-DSS, SOC 2) -->
<!--   - Scope: what parts of the project it applies to -->
<!--   - Key obligations: what the project must do or avoid -->
<!--   - Downstream expectations: which domain(s) must implement controls for this obligation -->
<!-- Traceability matrix: obligation → downstream control expectation -->
```

**Required subsections:** per-regime breakdown, obligation-to-control traceability
**Optional subsections:** compliance timeline, audit cadence
**Required diagrams:** none
**Required cross-references:** Threat Model, Vision(01)

### Examples

**Correct:**
> **Regime:** GDPR (General Data Protection Regulation)
> **Scope:** All user personal data collected and processed by the platform, regardless of storage location.
> **Key obligations:** Data minimization, right to erasure, breach notification within 72 hours, data protection impact assessment for high-risk processing.
> **Downstream expectations:** Architecture must design for erasure capability; Engineering must implement audit logging for data access; Feature Technical must scope consent flows per feature.

**Incorrect:**
> We need to comply with GDPR. We'll use a consent management platform and encrypt all personal data at rest with AES-256.
> *Why wrong: This skips the obligation-to-control traceability — it jumps straight to implementation solutions (CMP, AES-256) instead of stating what the project must do and which downstream domains must implement controls.*

### Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** tables
- **Audience:** architect
- **Do:** Name each compliance regime (GDPR, HIPAA, PCI-DSS, SOC 2) explicitly; define scope and applicability per regime; trace every obligation to at least one downstream control expectation
- **Don't:** Prescribe specific implementation controls (tooling, libraries, configurations); skip the obligation-to-control traceability; lump all regimes into a single undifferentiated paragraph

---

*(To be written by the domain expert. This section defines compliance obligations.)*

---

## Incident Response

> *Structural rules: `audit/deterministic/section/03-security/08-incident_response.yaml`*

### Template

> **minimum_content:** 2–3 subsections
> **length_guidance:** moderate
> **diagram_requirements:** flowchart

```markdown
<!-- Detection Expectations: what signals indicate a security incident -->
<!-- Response Escalation: who is notified, in what order, within what timeframe -->
<!-- Communication Requirements: internal and external notification expectations -->
<!-- Recovery Objectives: expected time-to-contain, time-to-restore -->
```

**Required subsections:** detection expectations, response escalation, recovery objectives
**Optional subsections:** communication templates, post-incident review expectations
**Required diagrams:** escalation flowchart
**Required cross-references:** Threat Model

### Examples

**Correct:**
> **Detection Expectations:** Unauthorized access attempts to restricted data stores must be detected within 15 minutes.
> **Response Escalation:** Security lead notified first; project lead notified within 1 hour; external counsel notified if data breach is confirmed.
> **Recovery Objectives:** Containment within 4 hours; full restoration within 24 hours.

**Incorrect:**
> We use Splunk for SIEM monitoring and PagerDuty for on-call alerting. The SOC team runs a weekly scan using Nessus.
> *Why wrong: This mandates specific tooling (Splunk, PagerDuty, Nessus) and operational cadences — those belong in Engineering's Security Standards, not at the project-wide incident response level.*

### Writing Guidance

- **Tone:** structural
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** State detection and response expectations as outcomes, not tooling; define escalation paths with timeframes and notification order; specify recovery objectives (time-to-contain, time-to-restore)
- **Don't:** Mandate specific SIEM, alerting, or scanning tools; embed on-call rotation details or shift schedules; define post-mortem templates or review formats

---

*(To be written by the domain expert. This section defines incident response expectations.)*

---

## Constraints

> *Structural rules: `audit/deterministic/section/03-security/05-constraints.yaml`*

### Template

> **minimum_content:** 1–2 subsections
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
<!-- For each constraint: -->
<!--   - Source: regulatory, contractual, infrastructure, or organizational -->
<!--   - Statement: hard boundary expressed as pass/fail evaluable condition -->
<!--   - Impact: which downstream domains are affected -->
<!-- Avoid embedding solutions — state the boundary, not how to satisfy it -->
```

**Required subsections:** none
**Optional subsections:** constraint-to-domain impact matrix
**Required diagrams:** none
**Required cross-references:** Vision(01), External Context

### Examples

**Correct:**
> **Source:** Regulatory (data residency law)
> **Statement:** All user personal data must be stored and processed within the European Economic Area.
> **Impact:** Architecture (data storage design), Engineering (database deployment region), Feature Technical (data flow design)

**Incorrect:**
> We should use a European cloud provider because it's closer to our users and reduces latency.
> *Why wrong: This is a soft preference disguised as a constraint — latency is not a hard boundary, and it embeds a solution (cloud provider selection) instead of stating the non-negotiable limitation (data must remain in the EEA).*

### Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** State each constraint as a hard boundary expressed as a pass/fail condition; identify which downstream domains are affected by each constraint; attribute each constraint to its source (regulatory, contractual, infrastructure, organizational)
- **Don't:** Embed implementation solutions within constraint statements; state soft preferences (performance, convenience) as hard constraints; omit source attribution for any listed constraint

---

*(To be written by the domain expert. This section defines hard security constraints.)*

---

## Required Sections

Every Security document must contain the following sections.
Sections are identified by heading text; the compiler maps each to a semantic type.

| Section | semantic_type | Required | Aliases | Content Requirements |
|---------|--------------|----------|---------|---------------------|
| Threat Model | `threat_model` | ✓ | Threats, Threat Modeling, Risk Assessment | Named methodology (STRIDE, PASTA, or OWASP); adversary profiles; threat enumeration with severity; attack surfaces; at least one downstream mitigation expectation per threat |
| Data Classification | `data_classification` | ✓ | Data Sensitivity, Data Classes | At least two distinct sensitivity levels; one concrete example per level; handling expectations per level; technology-independent classification |
| Security Principles | `security_principles` | ✓ | Security Posture, Guiding Security Principles | At least one principle; specific enough to constrain a concrete design decision; no generic platitudes; technology-independent |
| Compliance Requirements | `compliance` | | Regulatory Requirements, Compliance Obligations | Named compliance regimes (e.g. GDPR, HIPAA); scope and applicability per regime; obligation-to-downstream-control traceability |
| Incident Response | `incident_response` | | Incident Handling, Breach Response | Detection expectations; escalation paths; communication requirements; recovery objectives; outcome-level framing (no tooling mandates) |
| Purpose | `purpose` | | Overview, Summary | Security's role as project-wide authority; scope boundary with per-domain sections; derivation from Vision/Philosophy |
| Constraints | `constraints` | | Limitations | Non-negotiable limitations from regulatory, contractual, or organizational sources; each evaluable as pass/fail against a proposed design |
| Traceability | `traceability` | | Traces To, Derived From | Tier diagram showing derivation chain; list of downstream consumers; non-duplication rule stated |

Section headings are case-insensitive. Sections not listed here are stored as `generic` type — preserved but not queryable by type.

---

## Goals

Security aims to:

* Establish one authoritative threat model and data classification the whole project references.
* Prevent every domain from re-deriving its own security posture independently.
* Make compliance obligations traceable to specific downstream controls.
* Keep security a first-class constraint on Architecture and Engineering, not an afterthought.

---

## Non-Goals

Security(03) does not define:

* Specific authentication/authorization implementation
* Cryptographic algorithm or library selection
* CI/CD security tooling configuration
* Per-component trust boundaries
* Per-feature attack surface enumeration
* Source code

These responsibilities belong to Architecture, Engineering, and Feature Technical's own Security sections.

---

## Success Criteria

A Security document is successful when:

* Architecture, Engineering, and Feature Technical can each write their own Security Considerations/Standards sections by referencing this document instead of re-deriving a threat model from scratch.
* Data sensitivity is classified once and referenced consistently across the project.
* Compliance obligations are traceable to specific controls in downstream documents.
* A new contributor can read this document and understand what the project defends against before reading any implementation detail.

---

## Responsibilities

A Security document is responsible for defining:

* The project's threat model — what adversaries, threats, and failure modes are in scope
* Data classification — what data exists and how sensitive each class is
* Security principles that constrain every downstream design and implementation decision
* Compliance obligations the project must satisfy (regulatory, contractual, or self-imposed)
* Incident response expectations at a project level

Security provides the constraint every structural and implementation decision must satisfy — the same role Philosophy plays for values, applied specifically to threat and risk.

---

## Scope

A Security document should describe:

* Threats and adversaries the project defends against
* Data classification and sensitivity levels
* Project-wide security principles (e.g. least privilege, defense in depth, zero trust)
* Compliance regimes that apply (e.g. GDPR, HIPAA, PCI-DSS, SOC 2)
* Incident response expectations
* Security review or audit cadence

The Security document should remain stable, revisited when the threat landscape or compliance obligations change — not on every feature or release.

---

## Out of Scope

A Security document must not describe:

* Specific authentication or authorization implementations
* Cryptographic library or algorithm choices
* CI/CD security tooling (SAST, dependency scanning)
* Per-component trust boundaries
* Per-feature attack surface
* Source code

These belong to Architecture's Security Considerations, Engineering's Security Standards, and Feature Technical's Security Considerations respectively — see Relationship to Per-Domain Security Sections below.

---

## Inputs

Security derives from:

* Vision — what's being protected follows from what the product is
* Philosophy — security principles are a specialization of guiding principles

Security should not derive from implementation, architecture, or engineering decisions — it constrains those, not the other way around.

---

## Outputs

Security provides direction for:

* Architecture — Security Considerations
* Engineering — Security Standards
* Feature Technical Design — Security Considerations

Every per-domain Security section should be traceable to a threat, data class, or principle documented here.

---

## Traceability

> *Structural rules: `audit/deterministic/section/03-security/06-traceability.yaml`*

### Template

> **minimum_content:** 1–2 subsections
> **length_guidance:** concise
> **diagram_requirements:** flowchart

```markdown
<!-- Tier diagram: Vision/Philosophy → Security → downstream domains -->
<!-- Downstream consumers: list each domain that consumes Security and how -->
<!-- Non-duplication rule: downstream sections reference this document, do not restate -->
```

**Required subsections:** tier diagram, downstream consumers, non-duplication rule
**Optional subsections:** none
**Required diagrams:** tier derivation chain (flowchart or text diagram)
**Required cross-references:** Vision(01), Philosophy(02), Architecture(05), Engineering(07), Feature Technical(10)

### Examples

**Correct:**
> Vision, Philosophy
>        │
>        ↓
>    Security (03)
>        │
>        ├── guides ──> Architecture (05) ── Security Considerations
>        └── guides ──> Engineering (07) ── Security Standards
>                             │
>                             ↓
>                   Feature Technical (10) ── Security Considerations
>
> Every downstream Security section references this document's threat model, data classification, or principles — it does not restate them.

**Incorrect:**
> Security derives from Architecture's trust-boundary analysis, which feeds Engineering's SAST tooling choices, which then inform the threat model.
> *Why wrong: The derivation chain is inverted — Security must derive from Vision and Philosophy, not from downstream implementation decisions like Architecture or Engineering tooling.*

### Writing Guidance

- **Tone:** structural
- **Voice:** third person
- **Structure:** diagrams
- **Audience:** new contributor
- **Do:** Show the full derivation chain as a tier diagram; list every downstream domain that consumes Security and how it consumes it; state the non-duplication rule explicitly so downstream sections reference, not restate
- **Don't:** Omit the tier diagram; list downstream domains without explaining their consumption pattern; allow downstream sections to re-derive threat models or data classification independently

---

```text
Vision, Philosophy
       │
       ↓
   Security (03)
       │
       ├── guides ──> Architecture (05) ── Security Considerations realizes it structurally
       │
       └── guides ──> Engineering (07) ── Security Standards realizes it at the tooling/code level
                            │
                            ↓
                  Feature Technical (10) ── Security Considerations realizes it per feature
```

Every downstream Security Considerations or Security Standards section should trace back to this document's threat model, data classification, or principles — not restate them independently.

---

## Relationships

| Document | Relationship |
|---|---|
| Vision | Security derives from Vision (what's being protected follows from what the product is) |
| Philosophy | Security derives from Philosophy (security principles are a specialization of guiding principles) |
| Architecture | Security guides Architecture; Architecture's Security Considerations realizes it structurally |
| Engineering | Security guides Engineering; Engineering's Security Standards realizes it at the tooling/code level |
| Feature Technical | Security's threat model and data classification apply per feature via Feature Technical's own Security Considerations |

---

## Required Characteristics

A Security document should be:

* Specific about data classification, not just principles
* Traceable from every downstream Security section
* Stable across releases
* Technology-independent
* Compliance-aware
* Threat-focused rather than control-focused

---

## Generation Rules

When generating Security documentation:

* Define the threat model before listing controls.
* Classify data by sensitivity, not by storage location.
* Document security principles that apply across all domains.
* Reference compliance requirements by name and scope.
* Keep the project-wide security posture separate from per-domain enforcement.

---

## Enhancement Rules

When enhancing Security documentation:

* Verify the threat model reflects current attack surfaces.
* Update data classification when new data types are introduced.
* Add compliance requirements when regulations change.
* Ensure per-domain Security sections remain consistent with this standard.
* Preserve existing threat model structure while refining detail.

---

## Audit Rules

An audit should verify:

* Threat Model section exists and uses a named, structured methodology (error if missing).
* Data Classification section exists with at least one sensitivity level defined (error if missing).
* Security Principles are specific enough to be traceable to at least one downstream Security Considerations/Standards section (warning if too generic).
* No content duplicating what belongs in Architecture's, Engineering's, or Feature Technical's own Security sections (warning if found — see Relationship to Per-Domain Security Sections).

---

## Validation Rules

A Security document is considered valid when:

* A threat model is documented using a structured methodology (STRIDE, PASTA, or OWASP Threat Modeling).
* Data classification levels are defined with at least one example per level.
* Security principles are stated and are specific enough to guide a design decision, not generic ("be secure").
* No cryptographic algorithm, library, or CI tooling choice appears (that belongs to Engineering).
* No per-component trust boundary diagram appears (that belongs to Architecture).
* No per-feature attack surface appears (that belongs to Feature Technical).

---

## Summary

Security is the project-wide statement of what is being defended, against what, and why — the threat model, data classification, and security principles every structural and implementation decision must satisfy.

It sits beside Feature in Tier 2, guided by Vision and Philosophy, and guides Architecture and Engineering downstream the same way Philosophy does — without replacing the Security Considerations or Security Standards sections those domains, and Feature Technical, already own.

---

## Common Mistakes

Examples include:

* Restating the same threat model separately inside Architecture, Engineering, and Feature Technical instead of referencing this document.
* Listing cryptographic algorithms or SAST tools here instead of in Engineering's Security Standards.
* Treating "security will be handled later" as acceptable deferral.
* Defining principles too generically to constrain any actual decision (e.g. "we take security seriously").
* Omitting data classification and jumping straight to controls.

These should be reported during audits.

---

## Documentation Folder

Security documents live under:

```text
docs/raw/security/
```

---

## Usage

Written once per project, alongside or shortly after Vision and Philosophy, by whoever owns security/compliance for the project. Revisit on threat-landscape or compliance changes, not on every feature. Once registered in code, use `samgraha audit --domain security` to confirm Architecture, Engineering, and Feature Technical reference this document's threat model rather than duplicating it.

## Related

- [Vision Standard](01-vision-standards.md) — Security derives from Vision
- [Philosophy Standard](02-philosophy-standards.md) — Security derives from Philosophy
- [Architecture Standard](05-architecture-standards.md) — has its own Security Considerations section that realizes this one structurally
- [Engineering Standard](07-engineering-standards.md) — has its own Security Standards section that realizes this one at the tooling/code level
- [Feature Technical Standard](10-feature-technical-standards.md) — has its own Security Considerations section that realizes this one per feature

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| Draft | — | — | Initial proposal. No `StandardDefinition` for `security` exists in `crates/standards/src/builtin.rs` yet. Required Sections, audit rules, and relationships below are proposed. |

## Relationship to Per-Domain Security Sections

Architecture, Engineering, and Feature Technical each already have their own Security Considerations or Security Standards section. This document does not replace them — it is what they derive from, the same way Architecture and Design derive from Philosophy without Philosophy restating either.

| Layer | Owns | Derives From Security(03) |
|---|---|---|
| Security (03) | Threat model, data classification, security principles, compliance posture — once, project-wide | — |
| Architecture — Security Considerations | Trust boundaries between components, where threat-model mitigations map onto system structure | The threat model and principles this document defines |
| Engineering — Security Standards | Secrets management tooling, cryptographic library/algorithm choices, SAST/dependency-scanning enforcement in CI | The security principles and compliance obligations this document defines |
| Feature Technical — Security Considerations | Per-feature authentication/authorization flows, per-feature input validation, per-feature audit events | The threat model and data classification this document defines, scoped to one feature |

An audit finding a duplicated threat model or data classification scheme inside Architecture, Engineering, or Feature Technical should flag it as belonging here instead — those sections should reference Security(03), not restate it.

---

## Quality Requirements

A Security document should be:

* Written once per project, revised only when threat landscape or compliance obligations change
* Specific about data classification, not just principles
* Traceable — every downstream Security Considerations/Standards section should be able to cite which threat or principle it addresses
* Technology independent — it says what must be defended against, not which library does it
* Reviewed on a defined cadence, not left stale

---
