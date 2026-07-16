# Compliance Requirements — Generation Template

> **Domain:** security
> **Section:** compliance
> **Source:** `documentation-standards/03-security-standards.md` §Compliance Requirements
> **Relationships:** `audit/deterministic/document/03-security-relationships.yaml`

Generate the Compliance Requirements section for a Security document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | threat_model (self-reference) | Compliance obligations must map to threats — regulatory requirements exist because specific threat categories need mitigation |
| `derives_from` | vision / vision_statement | Compliance must be consistent with Vision — the product's purpose determines which regulations apply |

## Template

```markdown
<!-- For each compliance regime: -->
<!--   - Name: regulatory or contractual body (e.g. GDPR, HIPAA, PCI-DSS, SOC 2) -->
<!--   - Scope: what parts of the project it applies to -->
<!--   - Key obligations: what the project must do or avoid -->
<!--   - Downstream expectations: which domain(s) must implement controls for this obligation -->
<!-- Traceability matrix: obligation → downstream control expectation -->
```

## Examples

**Correct:**
> **Regime:** GDPR (General Data Protection Regulation)
> **Scope:** All user personal data collected and processed by the platform, regardless of storage location.
> **Key obligations:** Data minimization, right to erasure, breach notification within 72 hours, data protection impact assessment for high-risk processing.
> **Downstream expectations:** Architecture must design for erasure capability; Engineering must implement audit logging for data access; Feature Technical must scope consent flows per feature.

**Incorrect:**
> We need to comply with GDPR. We'll use a consent management platform and encrypt all personal data at rest with AES-256.
> *Why wrong: This skips the obligation-to-control traceability — it jumps straight to implementation solutions (CMP, AES-256) instead of stating what the project must do and which downstream domains must implement controls.*

## Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** tables
- **Audience:** architect
- **Do:** Name each compliance regime (GDPR, HIPAA, PCI-DSS, SOC 2) explicitly; define scope and applicability per regime; trace every obligation to at least one downstream control expectation
- **Don't:** Prescribe specific implementation controls (tooling, libraries, configurations); skip the obligation-to-control traceability; lump all regimes into a single undifferentiated paragraph

**Required subsections:** per-regime breakdown, obligation-to-control traceability
**Optional subsections:** compliance timeline, audit cadence
**Required diagrams:** none
**Required cross-references:** Threat Model, Vision(01)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
