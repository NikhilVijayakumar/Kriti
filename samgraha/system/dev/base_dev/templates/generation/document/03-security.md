# Security Document — Generation Template

> **Domain:** security
> **Source standard:** `documentation-standards/03-security-standards.md`
> **Coherence source:** `audit/semantic/document/03-security.md`
> **Relationships:** `audit/deterministic/document/03-security-relationships.yaml`

Generate a complete Security document for a system. The document must satisfy every required section below, in the order defined by the standard.

## Required Sections

| # | Section | semantic_type | Required | Content Requirements |
|---|---------|--------------|----------|---------------------|
| 1 | Purpose | `purpose` | | Security's role as project-wide authority; scope boundary with per-domain sections; derivation from Vision/Philosophy |
| 2 | Threat Model | `threat_model` | ✓ | Named methodology (STRIDE, PASTA, or OWASP); adversary profiles; threat enumeration with severity; attack surfaces; downstream mitigation expectations |
| 3 | Data Classification | `data_classification` | ✓ | At least two distinct sensitivity levels; one concrete example per level; handling expectations per level; technology-independent |
| 4 | Security Principles | `security_principles` | ✓ | At least one principle; specific enough to constrain a concrete design decision; no generic platitudes; technology-independent |
| 5 | Compliance Requirements | `compliance` | | Named compliance regimes (e.g. GDPR, HIPAA); scope and applicability per regime; obligation-to-downstream-control traceability |
| 6 | Incident Response | `incident_response` | | Detection expectations; escalation paths; communication requirements; recovery objectives; outcome-level framing (no tooling mandates) |
| 7 | Constraints | `constraints` | | Non-negotiable limitations from regulatory, contractual, or organizational sources; each evaluable as pass/fail against a proposed design |

## Cross-Section Coherence Constraint

> Sourced from `audit/semantic/document/03-security.md` Engineering Intent.

All sections must cohere as a single security posture. Threat Model must reference Data Classification — threats are enumerated against classified assets. Security Principles must specialize Philosophy's guiding principles for the security context. Compliance Requirements must map obligations to threats or data classes. Incident Response must address the threats enumerated in Threat Model. Constraints must derive from Compliance Requirements or Philosophy trade-offs. No section may contain specific tooling, library names, or implementation controls — Security defines *what must be defended against*, not *which tool does the defending*. Terminology must be consistent across all sections.

## Sections

---

### 1. Purpose

**Template:**

```markdown
<!-- One paragraph: what Security defines and its role in the documentation hierarchy -->
<!-- One paragraph: what Security does not define, and where enforcement lives -->
```

**Correct example:**
> Security(03) establishes the project-wide threat model, data classification scheme, and security principles. It is the single source of truth for what the project defends against and why — every downstream domain's Security Considerations or Security Standards section derives from this document rather than re-deriving its own posture.

**Incorrect example:**
> Security(03) defines the authentication middleware, rate-limiting configuration, and WAF rule set used across all services.
> *Why wrong: Describes specific control implementations — those belong in Engineering's Security Standards, not in the project-wide Security document.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** new contributor
- **Do:** State Security's role as the single project-wide authority; define the boundary between Security and per-domain sections explicitly; reference derivation from Vision(01) and Philosophy(02)
- **Don't:** Name specific controls, libraries, or tooling; use imperative voice; embed implementation details that belong in downstream domains

---

### 2. Threat Model

**Template:**

```markdown
<!-- Methodology: state which threat-modeling methodology is used (STRIDE, PASTA, or OWASP) -->
<!-- Adversary Profiles: enumerate likely adversaries with motivation and capability -->
<!-- Threat Enumeration: list threats with category, severity, and affected assets -->
<!-- Attack Surfaces: identify external and internal surfaces -->
<!-- Downstream Expectations: map each threat to at least one domain that must address it -->
```

**Correct example:**
> **Methodology:** STRIDE
> **Adversary Profile — External Attacker:** Motivated by financial gain; capability includes automated scanning, phishing, and exploiting known vulnerabilities. Target: user authentication flows and data export endpoints.
> **Threat — Tampering (STRIDE):** An attacker modifies payment amount during transit between checkout and billing. Severity: High. Affected asset: transaction integrity. Downstream expectation: Engineering must implement request signing or integrity checks.

**Incorrect example:**
> Threat: Hackers might try to break in. Mitigation: We will use OWASP Top 10 and add WAF rules in the deployment pipeline.
> *Why wrong: No named methodology is used, the adversary profile is missing, severity is absent, and the mitigation embeds specific tooling.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** third person
- **Structure:** tables
- **Audience:** architect
- **Do:** Use a named methodology (STRIDE, PASTA, or OWASP Threat Modeling) consistently; link each threat to at least one downstream mitigation expectation; assign severity to every enumerated threat
- **Don't:** List specific tooling or library mitigations; enumerate per-component trust boundaries that belong in Architecture; use vague severity labels without justification

---

### 3. Data Classification

**Template:**

```markdown
<!-- Sensitivity Levels: define each level (e.g. Public, Internal, Confidential, Restricted) -->
<!--   For each level: description, one concrete example, handling expectations -->
<!-- Handling Expectations: cross-cutting rules (access control, encryption at rest/transit, retention) -->
<!-- Application: how downstream domains map their data to these levels -->
```

**Correct example:**
> **Internal:** Data intended for project members only — internal documentation, architecture diagrams, meeting notes.
> **Handling:** Access restricted to authenticated project members; no external sharing without approval.
> **Confidential:** Data whose unauthorized disclosure would cause material harm — user PII, financial records, authentication secrets.
> **Handling:** Encrypted at rest and in transit; access logged and auditable; retention policy enforced.

**Incorrect example:**
> Sensitive data goes in PostgreSQL with row-level security. Non-sensitive data goes in Elasticsearch.
> *Why wrong: Classifies data by storage technology rather than by sensitivity level.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** third person
- **Structure:** tables
- **Audience:** engineer
- **Do:** Provide one concrete example per sensitivity level; state handling expectations (access control, encryption, retention) per level; keep classification technology-independent
- **Don't:** Classify data by storage location or database; embed encryption library or access-control implementation; omit handling expectations for any defined level

---

### 4. Security Principles

**Template:**

```markdown
<!-- State each security principle with: -->
<!--   - Name: memorable, stable phrase -->
<!--   - Rationale: why this principle constrains design decisions -->
<!--   - Example decision it would constrain (optional but recommended) -->
<!-- Link principles back to Philosophy(02) guiding principles they specialize -->
```

**Correct example:**
> **Principle:** Least Privilege by Default
> **Rationale:** Every component, service, and user must start with the minimum permissions required for its function — no more.
> **Decision it constrains:** Architecture's service-to-service communication design must not grant blanket access between services.

**Incorrect example:**
> Security Principle: Be Secure. All code must follow security best practices.
> *Why wrong: This is a generic platitude that cannot constrain any concrete design decision.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** architect
- **Do:** State each principle with name, rationale, and at least one example decision it constrains; specialize Philosophy(02) guiding principles for the security context; ensure every principle is evaluable against a concrete design
- **Don't:** Write generic platitudes ("be secure", "follow best practices"); embed specific technology choices or library recommendations; list more than seven principles

---

### 5. Compliance Requirements

**Template:**

```markdown
<!-- For each compliance regime: -->
<!--   - Name: regulatory or contractual body (e.g. GDPR, HIPAA, PCI-DSS, SOC 2) -->
<!--   - Scope: what parts of the project it applies to -->
<!--   - Key obligations: what the project must do or avoid -->
<!--   - Downstream expectations: which domain(s) must implement controls for this obligation -->
<!-- Traceability matrix: obligation → downstream control expectation -->
```

**Correct example:**
> **Regime:** GDPR (General Data Protection Regulation)
> **Scope:** All user personal data collected and processed by the platform, regardless of storage location.
> **Key obligations:** Data minimization, right to erasure, breach notification within 72 hours, data protection impact assessment for high-risk processing.
> **Downstream expectations:** Architecture must design for erasure capability; Engineering must implement audit logging for data access; Feature Technical must scope consent flows per feature.

**Incorrect example:**
> We need to comply with GDPR. We'll use a consent management platform and encrypt all personal data at rest with AES-256.
> *Why wrong: Jumps straight to implementation solutions instead of stating obligations and downstream control expectations.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** third person
- **Structure:** tables
- **Audience:** architect
- **Do:** Name each compliance regime (GDPR, HIPAA, PCI-DSS, SOC 2) explicitly; define scope and applicability per regime; trace every obligation to at least one downstream control expectation
- **Don't:** Prescribe specific implementation controls (tooling, libraries, configurations); skip the obligation-to-control traceability; lump all regimes into a single undifferentiated paragraph

---

### 6. Incident Response

**Template:**

```markdown
<!-- Detection Expectations: what signals indicate a security incident -->
<!-- Response Escalation: who is notified, in what order, within what timeframe -->
<!-- Communication Requirements: internal and external notification expectations -->
<!-- Recovery Objectives: expected time-to-contain, time-to-restore -->
```

**Correct example:**
> **Detection Expectations:** Unauthorized access attempts to restricted data stores must be detected within 15 minutes.
> **Response Escalation:** Security lead notified first; project lead notified within 1 hour; external counsel notified if data breach is confirmed.
> **Recovery Objectives:** Containment within 4 hours; full restoration within 24 hours.

**Incorrect example:**
> We use Splunk for SIEM monitoring and PagerDuty for on-call alerting. The SOC team runs a weekly scan using Nessus.
> *Why wrong: Mandates specific tooling and operational cadences — those belong in Engineering's Security Standards.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** State detection and response expectations as outcomes, not tooling; define escalation paths with timeframes and notification order; specify recovery objectives (time-to-contain, time-to-restore)
- **Don't:** Mandate specific SIEM, alerting, or scanning tools; embed on-call rotation details or shift schedules; define post-mortem templates or review formats

---

### 7. Constraints

**Template:**

```markdown
<!-- For each constraint: -->
<!--   - Source: regulatory, contractual, infrastructure, or organizational -->
<!--   - Statement: hard boundary expressed as pass/fail evaluable condition -->
<!--   - Impact: which downstream domains are affected -->
<!-- Avoid embedding solutions — state the boundary, not how to satisfy it -->
```

**Correct example:**
> **Source:** Regulatory (data residency law)
> **Statement:** All user personal data must be stored and processed within the European Economic Area.
> **Impact:** Architecture (data storage design), Engineering (database deployment region), Feature Technical (data flow design)

**Incorrect example:**
> We should use a European cloud provider because it's closer to our users and reduces latency.
> *Why wrong: This is a soft preference disguised as a constraint — latency is not a hard boundary, and it embeds a solution.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** State each constraint as a hard boundary expressed as a pass/fail condition; identify which downstream domains are affected by each constraint; attribute each constraint to its source (regulatory, contractual, infrastructure, organizational)
- **Don't:** Embed implementation solutions within constraint statements; state soft preferences (performance, convenience) as hard constraints; omit source attribution for any listed constraint

---

## Output Contract

Output a single complete markdown document containing all 7 sections above, in the order listed. Each section must:

1. Use the template skeleton as its structural basis
2. Fill every placeholder with domain-appropriate content (not lorem ipsum)
3. Satisfy the Writing Guidance for its section
4. Be consistent with every other section (cross-section coherence constraint above)
5. Include diagrams where Required diagrams are specified (as markdown image references or Mermaid code blocks)
6. Omit implementation details (technology names, library versions, configuration values, code snippets)
