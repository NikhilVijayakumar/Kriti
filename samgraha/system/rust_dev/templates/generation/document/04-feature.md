# Feature Document — Generation Template

> **Domain:** feature
> **Source standard:** `documentation-standards/04-feature-standards.md`
> **Coherence source:** `audit/semantic/document/04-feature.md`
> **Relationships:** `audit/deterministic/document/04-feature-relationships.yaml`

Generate a complete Feature document for a system. The document must satisfy every required section below, in the order defined by the standard. Each Feature document describes exactly one atomic capability.

## Required Sections

| # | Section | semantic_type | Required | Content Requirements |
|---|---------|--------------|----------|---------------------|
| 1 | Purpose | `purpose` | ✓ | 1-2 paragraphs defining what the feature is and why it exists |
| 2 | Functional Requirements | `functional_requirements` | ✓ | Atomic testable statements of what the product shall do |
| 3 | Business Rules | `business_rules` | | Conditional logic governing feature behavior |
| 4 | Constraints | `constraints` | | Regulatory, business, or technical limitations |
| 5 | Dependencies | `dependencies` | | Other features or systems the feature relies on |
| 6 | Acceptance Criteria | `acceptance_criteria` | ✓ | Verifiable conditions confirming feature completeness |
| 7 | Future Extensions | `future_extensions` | | Known deferred work with rationale |

## Cross-Section Coherence Constraint

> Sourced from `audit/semantic/document/04-feature.md` Engineering Intent.

All sections must cohere as a single atomic feature specification. Functional Requirements must be testable against Acceptance Criteria — every AC must trace to at least one FR. Business Rules must be consistent with Functional Requirements — rules cannot contradict requirements. Constraints must not contradict Functional Requirements — constraints narrow scope, they don't negate it. Dependencies must be listed honestly — missing a dependency produces an unimplementable feature. No section may contain technology names, library versions, API endpoints, or code snippets. Feature Documentation explains *what the product must do*, not *how it is implemented*. Terminology must be consistent across all sections.

## Sections

---

### 1. Purpose

**Template:**

```markdown
## Purpose

> **semantic_type:** `purpose`
> **scope:** [Why this feature exists — its role in the product]
> **out_of_scope:** [What this feature does not define]
> **contributes:** [How this section feeds downstream standards]
> **relationships:** [Upstream and downstream connections]
> **responsibilities:** [What this section must capture]
> **generation_rules:** [Rules for authoring this section]
> **enhancement_rules:** [Rules for improving this section]
> **validation_rules:** [Criteria for section completeness]
> **audit_rules:** [Audit expectations]

[1-2 paragraphs stating what the feature is and why it exists]
```

**Note:** When generating for a specific system, produce system-specific content — what THIS feature does for THIS system — not meta-level language about documentation types. The generation note above (semantic_type, scope, etc.) is structural metadata; the actual content is the paragraph(s) describing the feature's purpose.

**Correct example:**
> CloudBridge is a data synchronization feature that transfers datasets between distributed storage systems. It exists to ensure data consistency across environments without requiring manual intervention. CloudBridge focuses on the capability of synchronization, not the underlying protocol or transport mechanism.

**Incorrect example:**
> CloudBridge is a feature built with Python 3.12 using Apache Kafka for message streaming and PostgreSQL for state tracking. It exists to move data between clusters.
> *Why wrong: Contains implementation details (Python, Kafka, PostgreSQL) that belong in Engineering Documentation.*

**Writing guidance:**
- **Tone:** inspirational
- **Voice:** first person plural
- **Structure:** paragraphs
- **Audience:** product owner
- **Do:** State the feature's existence and value in business terms; explain what capability the feature provides to users; keep scope boundaries explicit and clear
- **Don't:** Mention specific technologies, frameworks, or implementation patterns; describe how the feature works internally; include lists of requirements or detailed specifications

---

### 2. Functional Requirements

**Template:**

```markdown
## Functional Requirements

> **semantic_type:** `functional_requirements`
> **scope:** [Functional behaviors the feature must exhibit]
> **out_of_scope:** [Implementation details excluded]
> **contributes:** [How this feeds downstream design]
> **relationships:** [Upstream and downstream connections]
> **responsibilities:** [What this section must capture]
> **generation_rules:** [Rules for authoring this section]
> **enhancement_rules:** [Rules for improving this section]
> **validation_rules:** [Criteria for section completeness]
> **audit_rules:** [Audit expectations]

- [FR-001] The feature shall [behavior] when [condition].
- [FR-002] The feature shall [behavior] when [condition].
- [FR-003] The feature shall [behavior] when [condition].
```

**Correct example:**
> - [FR-001] CloudBridge shall synchronize data between source and target systems when a sync request is initiated.
> - [FR-002] CloudBridge shall detect conflicting changes when both source and target contain modifications to the same record.
> - [FR-003] CloudBridge shall preserve data integrity when a partial failure occurs during synchronization.

**Incorrect example:**
> - [FR-001] CloudBridge shall use the Apache Kafka producer API to publish sync events to the broker topic.
> - [FR-002] CloudBridge shall query the PostgreSQL `sync_status` table using the SQLAlchemy ORM.
> *Why wrong: Each requirement describes a specific technology choice rather than the functional behavior.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Write one atomic requirement per bullet using shall/must language; make each requirement independently testable; describe the behavior the product must exhibit under specific conditions
- **Don't:** Reference specific technologies, APIs, or libraries; write compound requirements that combine multiple behaviors; use vague terms like "should" or "might" without a testable condition

---

### 3. Business Rules

**Template:**

```markdown
## Business Rules

> **semantic_type:** `business_rules`
> **scope:** [Business logic governing feature behavior]
> **out_of_scope:** [Technical constraints excluded]
> **contributes:** [How this feeds downstream design]
> **relationships:** [Upstream and downstream connections]
> **responsibilities:** [What this section must capture]
> **generation_rules:** [Rules for authoring this section]
> **enhancement_rules:** [Rules for improving this section]
> **validation_rules:** [Criteria for section completeness]
> **audit_rules:** [Audit expectations]

- [BR-001] When [condition], then [behavior].
- [BR-002] When [condition], then [behavior].

[Optional: flowchart showing rule decision logic]
```

**Correct example:**
> - [BR-001] When a record exists in both source and target with different values, then CloudBridge shall flag the conflict and pause synchronization for that record.
> - [BR-002] When the source dataset is empty, then CloudBridge shall complete with a no-op result and log the condition.

**Incorrect example:**
> - [BR-001] When a conflict is detected, then the system shall execute the `resolve_conflict()` method defined in `sync_engine.py`.
> *Why wrong: References implementation details (specific Python files and methods) instead of describing business logic in technology-independent terms.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** product owner
- **Do:** Express each rule as a conditional When/Then statement; capture domain-specific business logic that cannot be inferred from requirements alone; include edge cases and exception handling rules
- **Don't:** Describe technical validation, input sanitization, or database constraints; reference implementation code or system components; write rules that duplicate functional requirements

---

### 4. Constraints

**Template:**

```markdown
## Constraints

> **semantic_type:** `constraints`
> **scope:** [Limitations the feature must operate within]
> **out_of_scope:** [Implementation details excluded]
> **contributes:** [How this feeds downstream design]
> **relationships:** [Upstream and downstream connections]
> **responsibilities:** [What this section must capture]
> **generation_rules:** [Rules for authoring this section]
> **enhancement_rules:** [Rules for improving this section]
> **validation_rules:** [Criteria for section completeness]
> **audit_rules:** [Audit expectations]

### Regulatory
- [C-001] [Regulatory constraint and its impact on the feature]

### Business
- [C-002] [Business constraint and its impact on the feature]

### Technical
- [C-003] [Technical constraint and its impact on the feature]
```

**Correct example:**
> ### Regulatory
> - [C-001] CloudBridge must comply with data residency requirements that restrict cross-border data transfer.
>
> ### Business
> - [C-002] CloudBridge must complete synchronization within the agreed maintenance window of 4 hours.

**Incorrect example:**
> ### Regulatory
> - [C-001] CloudBridge must use AES-256 encryption at rest and TLS 1.3 in transit per compliance requirements.
> *Why wrong: Specifies a particular encryption standard rather than stating the regulatory requirement it serves.*

**Writing guidance:**
- **Tone:** structural
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** architect
- **Do:** Categorize each constraint by type (Regulatory, Business, Technical); state the limitation clearly without prescribing a solution; reference the regulatory or business origin of each constraint
- **Don't:** Specify particular technologies, frameworks, or vendor solutions; describe infrastructure requirements or performance benchmarks; include implementation workarounds or mitigation strategies

---

### 5. Dependencies

**Template:**

```markdown
## Dependencies

> **semantic_type:** `dependencies`
> **scope:** [Features or systems this feature relies on]
> **out_of_scope:** [Implementation dependencies excluded]
> **contributes:** [How this feeds downstream design]
> **relationships:** [Upstream and downstream connections]
> **responsibilities:** [What this section must capture]
> **generation_rules:** [Rules for authoring this section]
> **enhancement_rules:** [Rules for improving this section]
> **validation_rules:** [Criteria for section completeness]
> **audit_rules:** [Audit expectations]

| Dependency | Nature | Required |
|------------|--------|----------|
| [Feature/System Name] | [functional \| data] | [yes \| no] |
```

**Correct example:**
> | Dependency | Nature | Required |
> |------------|--------|----------|
> | User Authentication | functional | yes |
> | Data Encryption | functional | yes |
> | Audit Logging | data | no |

**Incorrect example:**
> | Dependency | Nature | Required |
> |------------|--------|----------|
> | Spring Security | functional | yes |
> | Apache Kafka 3.4 | data | yes |
> *Why wrong: Lists specific software libraries and version numbers rather than feature or system capabilities.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** tables
- **Audience:** architect
- **Do:** List each dependency by feature or system name; specify whether the dependency is functional or data-related; indicate whether each dependency is required or optional
- **Don't:** List software libraries, frameworks, or version-specific packages; include build dependencies or toolchain requirements; omit the nature or criticality of each dependency

---

### 6. Acceptance Criteria

**Template:**

```markdown
## Acceptance Criteria

> **semantic_type:** `acceptance_criteria`
> **scope:** [Verifiable conditions confirming feature completeness]
> **out_of_scope:** [Test implementation details excluded]
> **contributes:** [How this feeds downstream validation]
> **relationships:** [Upstream and downstream connections]
> **responsibilities:** [What this section must capture]
> **generation_rules:** [Rules for authoring this section]
> **enhancement_rules:** [Rules for improving this section]
> **validation_rules:** [Criteria for section completeness]
> **audit_rules:** [Audit expectations]

- [AC-001] Given [precondition], when [action], then [expected result].
- [AC-002] Given [precondition], when [action], then [expected result].
- [AC-003] Given [precondition], when [action], then [expected result].
```

**Correct example:**
> - [AC-001] Given a dataset in the source system, when a sync request is initiated, then CloudBridge shall transfer all records to the target system without data loss.
> - [AC-002] Given conflicting records in both systems, when sync encounters a conflict, then CloudBridge shall flag the conflicting records and preserve both versions for review.
> - [AC-003] Given a partial failure during synchronization, when the process is interrupted, then CloudBridge shall resume from the last successful checkpoint without duplicating records.

**Incorrect example:**
> - [AC-001] Given a sync request, when the `SyncManager.process()` method is called, then it should return a 200 status code within 500ms.
> *Why wrong: References specific code components and implementation mechanics rather than verifiable conditions.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Use Given/When/Then format for each criterion; derive every criterion from a specific functional requirement or business rule; make each criterion independently verifiable without code inspection
- **Don't:** Reference specific code components, database tables, or API endpoints; write criteria that require reading source code to verify; use vague pass/fail conditions without observable outcomes

---

### 7. Future Extensions

**Template:**

```markdown
## Future Extensions

> **semantic_type:** `future_extensions`
> **scope:** [Known deferred work for this feature]
> **out_of_scope:** [Current requirements excluded]
> **contributes:** [How this informs downstream planning]
> **relationships:** [Upstream and downstream connections]
> **responsibilities:** [What this section must capture]
> **generation_rules:** [Rules for authoring this section]
> **enhancement_rules:** [Rules for improving this section]
> **validation_rules:** [Criteria for section completeness]
> **audit_rules:** [Audit expectations]

| Extension | Rationale | Trigger |
|-----------|-----------|---------|
| [Description] | [Why deferred] | [When to revisit] |
```

**Correct example:**
> | Extension | Rationale | Trigger |
> |-----------|-----------|---------|
> | Multi-directional sync | Current scope limited to one-way transfer to reduce complexity | When bidirectional use cases are validated with users |
> | Incremental sync | Requires a change-detection mechanism not yet designed | When full-sync performance becomes a bottleneck |

**Incorrect example:**
> | Extension | Rationale | Trigger |
> |-----------|-----------|---------|
> | Add Redis caching layer | Performance optimization deferred to phase 2 | When database queries exceed 200ms |
> *Why wrong: Describes an implementation component rather than a functional capability.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables
- **Audience:** product owner
- **Do:** Describe deferred work as functional capabilities, not implementation tasks; include a clear rationale for why each item was deferred; specify the triggering condition that would prompt revisiting the item
- **Don't:** List implementation components or technical optimizations as extensions; defer items without a rationale; include current in-scope requirements disguised as future work

---

## Output Contract

Output a single complete markdown document containing all 7 sections above, in the order listed. Each section must:

1. Use the template skeleton as its structural basis
2. Fill every placeholder with domain-appropriate content (not lorem ipsum)
3. Satisfy the Writing Guidance for its section
4. Be consistent with every other section (cross-section coherence constraint above)
5. Include diagrams where Required diagrams are specified (as markdown image references or Mermaid code blocks)
6. Omit implementation details (technology names, library versions, configuration values, code snippets)
