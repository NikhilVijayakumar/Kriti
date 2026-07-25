# Threat Model — Generation Template

> **Domain:** security
> **Section:** threat_model
> **Source:** `documentation-standards/03-security-standards.md` §Threat Model
> **Relationships:** `audit/deterministic/document/03-security-relationships.yaml`

Generate the Threat Model section for a Security document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | vision / vision_statement | Threat Model must derive from Vision — what the product is determines what adversaries target |
| `guided_by` | philosophy / guiding_principles | Threat Model must be guided by Philosophy — the team's values shape what they choose to defend against |
| `informs` | architecture / security_considerations | Threat Model must inform Architecture's security considerations — threats map to structural mitigations |
| `traceable_to` | security / data_classification (self) | Threat Model must reference Data Classification — threats are enumerated against classified assets |

## Template

```markdown
<!-- Methodology: state which threat-modeling methodology is used (STRIDE, PASTA, or OWASP) -->
<!-- Adversary Profiles: enumerate likely adversaries with motivation and capability -->
<!-- Threat Enumeration: list threats with category, severity, and affected assets -->
<!-- Attack Surfaces: identify external and internal surfaces -->
<!-- Downstream Expectations: map each threat to at least one domain that must address it -->
```

## Examples

**Correct:**
> **Methodology:** STRIDE
> **Adversary Profile — External Attacker:** Motivated by financial gain; capability includes automated scanning, phishing, and exploiting known vulnerabilities. Target: user authentication flows and data export endpoints.
> **Threat — Tampering (STRIDE):** An attacker modifies payment amount during transit between checkout and billing. Severity: High. Affected asset: transaction integrity. Downstream expectation: Engineering must implement request signing or integrity checks.

**Incorrect:**
> Threat: Hackers might try to break in. Mitigation: We will use OWASP Top 10 and add WAF rules in the deployment pipeline.
> *Why wrong: No named methodology is used ("OWASP Top 10" is a list, not a methodology), the adversary profile is missing, severity is absent, and the mitigation embeds specific tooling (WAF) that belongs in Engineering's Security Standards.*

## Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** tables
- **Audience:** architect
- **Do:** Use a named methodology (STRIDE, PASTA, or OWASP Threat Modeling) consistently; link each threat to at least one downstream mitigation expectation; assign severity to every enumerated threat
- **Don't:** List specific tooling or library mitigations; enumerate per-component trust boundaries that belong in Architecture; use vague severity labels without justification

**Required subsections:** methodology, adversary profiles, threat enumeration, attack surfaces, downstream expectations
**Optional subsections:** trust assumptions, risk scoring matrix
**Required diagrams:** threat landscape overview (flowchart or table)
**Required cross-references:** Data Classification, Security Principles

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
