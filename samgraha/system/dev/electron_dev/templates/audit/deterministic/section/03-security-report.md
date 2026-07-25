# Deterministic Section Report — Security

**Document:** {{ document_path }}
**Standard:** `documentation-standards/03-security-standards.md`
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Deterministic Section Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
overall = average of the 8 section scores below
section_score = 100 × (Σ weight of passed rules in that section) / (Σ weight of all rules in that section)
# calculation: deterministic_section_v1
```

### Score History

| Revision | Date | Score | vs. Previous | vs. Baseline |
|---:|---|---:|---|---|
{% for r in revision_history -%}
| {{ r.revision }} | {{ r.date }} | {{ r.score }} / 100 | {{ r.delta_previous_display }} | {{ r.delta_baseline_display }} |
{% endfor -%}
| {{ revision_number }} (current) | {{ created_at }} | {{ score }} / 100 | {{ delta_previous_display }} | {{ delta_baseline_display }} |

{% if not previous_score %}No prior runs — this revision is the baseline every future run is compared against.{% endif %}

### Section Scores

| # | Section | Required | Weight | Score | Previous | Trend |
|---:|---|:---:|---:|---:|---:|---|
| 1 | Threat Model | **required** | 5.0 | {{ sections.threat_model.score }} / 100 | {{ sections.threat_model.previous_score | default('—') }} | {{ sections.threat_model.trend_display }} |
| 2 | Data Classification | **required** | 5.5 | {{ sections.data_classification.score }} / 100 | {{ sections.data_classification.previous_score | default('—') }} | {{ sections.data_classification.trend_display }} |
| 3 | Security Principles | **required** | 5.5 | {{ sections.security_principles.score }} / 100 | {{ sections.security_principles.previous_score | default('—') }} | {{ sections.security_principles.trend_display }} |
| 4 | Purpose | **required** | 4.0 | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 5 | Constraints | **required** | 4.5 | {{ sections.constraints.score }} / 100 | {{ sections.constraints.previous_score | default('—') }} | {{ sections.constraints.trend_display }} |
| 6 | Traceability | **required** | 4.5 | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |
| 7 | Compliance | optional | 3.0 | {{ sections.compliance.score }} / 100 | {{ sections.compliance.previous_score | default('—') }} | {{ sections.compliance.trend_display }} |
| 8 | Incident Response | optional | 3.0 | {{ sections.incident_response.score }} / 100 | {{ sections.incident_response.previous_score | default('—') }} | {{ sections.incident_response.trend_display }} |

The 6 required sections carry 29.0 of the document's 35.0 total rule weight — a document can only pass if those six are both present and internally sound; the remaining two are recommended-quality signal, not gating.

---

## 1. Threat Model — `section/03-security/01-threat_model.yaml` — weight 5.0 — **required**

**Why this matters:** Threat Model is the security posture's central artifact — it defines what can go wrong and how it's mitigated. A missing or empty threat model leaves downstream Architecture with no verifiable security boundary to enforce.

**Section Score: {{ sections.threat_model.score }} / 100** ({{ sections.threat_model.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| sec-sec-tm-001 | Threat Model section exists | error (mandatory) | 1.5 | {{ results['sec-sec-tm-001'].previous_status \| default('—') }} | {{ results['sec-sec-tm-001'].status }} | {{ results['sec-sec-tm-001'].trend_display }} | {{ results['sec-sec-tm-001'].evidence \| default('—') }} |
| sec-sec-tm-002 | Each identified threat includes a corresponding mitigation or countermeasure | error (mandatory) | 1.0 | {{ results['sec-sec-tm-002'].previous_status \| default('—') }} | {{ results['sec-sec-tm-002'].status }} | {{ results['sec-sec-tm-002'].trend_display }} | {{ results['sec-sec-tm-002'].evidence \| default('—') }} |
| sec-sec-tm-003 | No specific security libraries, frameworks, or tooling referenced | error (mandatory) | 1.0 | {{ results['sec-sec-tm-003'].previous_status \| default('—') }} | {{ results['sec-sec-tm-003'].status }} | {{ results['sec-sec-tm-003'].trend_display }} | {{ results['sec-sec-tm-003'].evidence \| default('—') }} |
| sec-sec-tm-004 | Threats organized by category, severity, or attack vector — not an unstructured paragraph | warning (recommended) | 0.5 | {{ results['sec-sec-tm-004'].previous_status \| default('—') }} | {{ results['sec-sec-tm-004'].status }} | {{ results['sec-sec-tm-004'].trend_display }} | {{ results['sec-sec-tm-004'].evidence \| default('—') }} |
| sec-sec-tm-005 | Threats identify which data classifications they affect | warning (recommended) | 0.5 | {{ results['sec-sec-tm-005'].previous_status \| default('—') }} | {{ results['sec-sec-tm-005'].status }} | {{ results['sec-sec-tm-005'].trend_display }} | {{ results['sec-sec-tm-005'].evidence \| default('—') }} |
| sec-sec-tm-006 | At least two distinct threats documented | warning (recommended) | 0.5 | {{ results['sec-sec-tm-006'].previous_status \| default('—') }} | {{ results['sec-sec-tm-006'].status }} | {{ results['sec-sec-tm-006'].trend_display }} | {{ results['sec-sec-tm-006'].evidence \| default('—') }} |

## 2. Data Classification — `02-data_classification.yaml` — weight 5.5 — **required**

**Why this matters:** Data Classification defines how sensitive data is categorized and handled. Without it, every data-handling decision is ad-hoc — the system may protect some data while silently leaking other data that deserves equal or greater protection.

**Section Score: {{ sections.data_classification.score }} / 100** ({{ sections.data_classification.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| sec-sec-dc-001 | Data Classification section exists | error (mandatory) | 1.5 | {{ results['sec-sec-dc-001'].previous_status \| default('—') }} | {{ results['sec-sec-dc-001'].status }} | {{ results['sec-sec-dc-001'].trend_display }} | {{ results['sec-sec-dc-001'].evidence \| default('—') }} |
| sec-sec-dc-002 | Distinct data types identified and classified | error (mandatory) | 1.0 | {{ results['sec-sec-dc-002'].previous_status \| default('—') }} | {{ results['sec-sec-dc-002'].status }} | {{ results['sec-sec-dc-002'].trend_display }} | {{ results['sec-sec-dc-002'].evidence \| default('—') }} |
| sec-sec-dc-003 | Each classification level includes specific handling requirements | error (mandatory) | 1.0 | {{ results['sec-sec-dc-003'].previous_status \| default('—') }} | {{ results['sec-sec-dc-003'].status }} | {{ results['sec-sec-dc-003'].trend_display }} | {{ results['sec-sec-dc-003'].evidence \| default('—') }} |
| sec-sec-dc-004 | No implementation technology references | error (mandatory) | 1.0 | {{ results['sec-sec-dc-004'].previous_status \| default('—') }} | {{ results['sec-sec-dc-004'].status }} | {{ results['sec-sec-dc-004'].trend_display }} | {{ results['sec-sec-dc-004'].evidence \| default('—') }} |
| sec-sec-dc-005 | Classification addresses data at rest, in transit, and in use | warning (recommended) | 0.5 | {{ results['sec-sec-dc-005'].previous_status \| default('—') }} | {{ results['sec-sec-dc-005'].status }} | {{ results['sec-sec-dc-005'].trend_display }} | {{ results['sec-sec-dc-005'].evidence \| default('—') }} |
| sec-sec-dc-006 | At least two distinct classification levels defined | warning (recommended) | 0.5 | {{ results['sec-sec-dc-006'].previous_status \| default('—') }} | {{ results['sec-sec-dc-006'].status }} | {{ results['sec-sec-dc-006'].trend_display }} | {{ results['sec-sec-dc-006'].evidence \| default('—') }} |

## 3. Security Principles — `03-security_principles.yaml` — weight 5.5 — **required**

**Why this matters:** Security Principles are the system's non-negotiable security rules — they constrain every downstream decision. Without them, every security decision is a one-off judgment call, and there's no consistent basis for reviewing whether the system is actually secure.

**Section Score: {{ sections.security_principles.score }} / 100** ({{ sections.security_principles.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| sec-sec-sp-001 | Security Principles section exists | error (mandatory) | 1.5 | {{ results['sec-sec-sp-001'].previous_status \| default('—') }} | {{ results['sec-sec-sp-001'].status }} | {{ results['sec-sec-sp-001'].trend_display }} | {{ results['sec-sec-sp-001'].evidence \| default('—') }} |
| sec-sec-sp-002 | Each principle is a discrete, numbered or bulleted statement with a clear directive | error (mandatory) | 1.0 | {{ results['sec-sec-sp-002'].previous_status \| default('—') }} | {{ results['sec-sec-sp-002'].status }} | {{ results['sec-sec-sp-002'].trend_display }} | {{ results['sec-sec-sp-002'].evidence \| default('—') }} |
| sec-sec-sp-003 | No specific security technologies, libraries, frameworks, or implementation details referenced | error (mandatory) | 1.0 | {{ results['sec-sec-sp-003'].previous_status \| default('—') }} | {{ results['sec-sec-sp-003'].status }} | {{ results['sec-sec-sp-003'].trend_display }} | {{ results['sec-sec-sp-003'].evidence \| default('—') }} |
| sec-sec-sp-004 | Each principle uses imperative language directing security decisions rather than describing current state | error (mandatory) | 1.0 | {{ results['sec-sec-sp-004'].previous_status \| default('—') }} | {{ results['sec-sec-sp-004'].status }} | {{ results['sec-sec-sp-004'].trend_display }} | {{ results['sec-sec-sp-004'].evidence \| default('—') }} |
| sec-sec-sp-005 | Security principles do not contradict the project philosophy guiding principles | warning (recommended) | 0.5 | {{ results['sec-sec-sp-005'].previous_status \| default('—') }} | {{ results['sec-sec-sp-005'].status }} | {{ results['sec-sec-sp-005'].trend_display }} | {{ results['sec-sec-sp-005'].evidence \| default('—') }} |
| sec-sec-sp-006 | At least three distinct security principles defined | warning (recommended) | 0.5 | {{ results['sec-sec-sp-006'].previous_status \| default('—') }} | {{ results['sec-sec-sp-006'].status }} | {{ results['sec-sec-sp-006'].trend_display }} | {{ results['sec-sec-sp-006'].evidence \| default('—') }} |

## 4. Purpose — `04-purpose.yaml` — weight 4.0 — **required**

**Why this matters:** Purpose tells a reader why Security Documentation exists before they read a single threat. A Purpose section that's missing, vague, or technology-leaking undermines every section that follows it.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| sec-sec-purpose-001 | Purpose section exists | error (mandatory) | 1.5 | {{ results['sec-sec-purpose-001'].previous_status \| default('—') }} | {{ results['sec-sec-purpose-001'].status }} | {{ results['sec-sec-purpose-001'].trend_display }} | {{ results['sec-sec-purpose-001'].evidence \| default('—') }} |
| sec-sec-purpose-002 | States security intent — why this documentation exists | error (mandatory) | 1.0 | {{ results['sec-sec-purpose-002'].previous_status \| default('—') }} | {{ results['sec-sec-purpose-002'].status }} | {{ results['sec-sec-purpose-002'].trend_display }} | {{ results['sec-sec-purpose-002'].evidence \| default('—') }} |
| sec-sec-purpose-003 | Technology-independent — no specific technologies, frameworks, or implementation details | error (mandatory) | 1.0 | {{ results['sec-sec-purpose-003'].previous_status \| default('—') }} | {{ results['sec-sec-purpose-003'].status }} | {{ results['sec-sec-purpose-003'].trend_display }} | {{ results['sec-sec-purpose-003'].evidence \| default('—') }} |
| sec-sec-purpose-004 | Scope boundaries defined — what the documentation is and is not | warning (recommended) | 0.5 | {{ results['sec-sec-purpose-004'].previous_status \| default('—') }} | {{ results['sec-sec-purpose-004'].status }} | {{ results['sec-sec-purpose-004'].trend_display }} | {{ results['sec-sec-purpose-004'].evidence \| default('—') }} |

## 5. Constraints — `05-constraints.yaml` — weight 4.5 — **required**

**Why this matters:** Constraints capture the boundaries on security decisions — what must be true regardless of design. Without them, every security constraint is discovered late, during Architecture review or, worse, in production.

**Section Score: {{ sections.constraints.score }} / 100** ({{ sections.constraints.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| sec-sec-con-001 | Constraints section exists | error (mandatory) | 1.5 | {{ results['sec-sec-con-001'].previous_status \| default('—') }} | {{ results['sec-sec-con-001'].status }} | {{ results['sec-sec-con-001'].trend_display }} | {{ results['sec-sec-con-001'].evidence \| default('—') }} |
| sec-sec-con-002 | Each constraint is a discrete statement defining a boundary or limitation on security decisions | error (mandatory) | 1.0 | {{ results['sec-sec-con-002'].previous_status \| default('—') }} | {{ results['sec-sec-con-002'].status }} | {{ results['sec-sec-con-002'].trend_display }} | {{ results['sec-sec-con-002'].evidence \| default('—') }} |
| sec-sec-con-003 | No implementation technology references | error (mandatory) | 1.0 | {{ results['sec-sec-con-003'].previous_status \| default('—') }} | {{ results['sec-sec-con-003'].status }} | {{ results['sec-sec-con-003'].trend_display }} | {{ results['sec-sec-con-003'].evidence \| default('—') }} |
| sec-sec-con-004 | Each constraint identifies its source (regulatory, organizational, technical, or philosophical) | warning (recommended) | 0.5 | {{ results['sec-sec-con-004'].previous_status \| default('—') }} | {{ results['sec-sec-con-004'].status }} | {{ results['sec-sec-con-004'].trend_display }} | {{ results['sec-sec-con-004'].evidence \| default('—') }} |
| sec-sec-con-005 | Constraints are stated in a way that allows verification of compliance | warning (recommended) | 0.5 | {{ results['sec-sec-con-005'].previous_status \| default('—') }} | {{ results['sec-sec-con-005'].status }} | {{ results['sec-sec-con-005'].trend_display }} | {{ results['sec-sec-con-005'].evidence \| default('—') }} |

## 6. Traceability — `06-traceability.yaml` — weight 4.5 — **required**

**Why this matters:** Traceability maps security decisions back to vision-level goals and forward to Architecture and Engineering. Without it, every security claim is unverifiable — you can't tell whether the system actually implements what the threat model requires.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| sec-sec-tr-001 | Traceability section exists | error (mandatory) | 1.5 | {{ results['sec-sec-tr-001'].previous_status \| default('—') }} | {{ results['sec-sec-tr-001'].status }} | {{ results['sec-sec-tr-001'].trend_display }} | {{ results['sec-sec-tr-001'].evidence \| default('—') }} |
| sec-sec-tr-002 | Threats traceable to vision-level security goals or concerns | error (mandatory) | 1.0 | {{ results['sec-sec-tr-002'].previous_status \| default('—') }} | {{ results['sec-sec-tr-002'].status }} | {{ results['sec-sec-tr-002'].trend_display }} | {{ results['sec-sec-tr-002'].evidence \| default('—') }} |
| sec-sec-tr-003 | Data classifications linked to threats and mitigations | warning (recommended) | 0.5 | {{ results['sec-sec-tr-003'].previous_status \| default('—') }} | {{ results['sec-sec-tr-003'].status }} | {{ results['sec-sec-tr-003'].trend_display }} | {{ results['sec-sec-tr-003'].evidence \| default('—') }} |
| sec-sec-tr-004 | No implementation technology references | error (mandatory) | 1.0 | {{ results['sec-sec-tr-004'].previous_status \| default('—') }} | {{ results['sec-sec-tr-004'].status }} | {{ results['sec-sec-tr-004'].trend_display }} | {{ results['sec-sec-tr-004'].evidence \| default('—') }} |
| sec-sec-tr-005 | Traceability maps both upstream (to vision/philosophy) and downstream (to architecture/engineering) | warning (recommended) | 0.5 | {{ results['sec-sec-tr-005'].previous_status \| default('—') }} | {{ results['sec-sec-tr-005'].status }} | {{ results['sec-sec-tr-005'].trend_display }} | {{ results['sec-sec-tr-005'].evidence \| default('—') }} |

## 7. Compliance — `07-compliance.yaml` — weight 3.0 — optional

**Why this matters:** Compliance Requirements names the regulatory regimes the system must satisfy, their scope of applicability, and traces each obligation to the control that satisfies it. It exists so "we're compliant" is a checkable claim, not an assertion.

**Section Score: {{ sections.compliance.score }} / 100** ({{ sections.compliance.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| security-sec-compliance-001 | Compliance section exists | error (mandatory) | 1.5 | {{ results['security-sec-compliance-001'].previous_status \| default('—') }} | {{ results['security-sec-compliance-001'].status }} | {{ results['security-sec-compliance-001'].trend_display }} | {{ results['security-sec-compliance-001'].evidence \| default('—') }} |
| security-sec-compliance-002 | Has substantive content — not empty or placeholder only | error (mandatory) | 1.0 | {{ results['security-sec-compliance-002'].previous_status \| default('—') }} | {{ results['security-sec-compliance-002'].status }} | {{ results['security-sec-compliance-002'].trend_display }} | {{ results['security-sec-compliance-002'].evidence \| default('—') }} |
| security-sec-compliance-003 | Specific to this project — not generic boilerplate | warning (recommended) | 0.5 | {{ results['security-sec-compliance-003'].previous_status \| default('—') }} | {{ results['security-sec-compliance-003'].status }} | {{ results['security-sec-compliance-003'].trend_display }} | {{ results['security-sec-compliance-003'].evidence \| default('—') }} |

## 8. Incident Response — `08-incident_response.yaml` — weight 3.0 — optional

**Why this matters:** Incident Response defines how a security incident is detected, escalated, communicated, and recovered from — at the outcome level, not a tooling mandate. It exists so a real incident has a known process instead of improvisation.

**Section Score: {{ sections.incident_response.score }} / 100** ({{ sections.incident_response.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| security-sec-incident_response-001 | Incident Response section exists | error (mandatory) | 1.5 | {{ results['security-sec-incident_response-001'].previous_status \| default('—') }} | {{ results['security-sec-incident_response-001'].status }} | {{ results['security-sec-incident_response-001'].trend_display }} | {{ results['security-sec-incident_response-001'].evidence \| default('—') }} |
| security-sec-incident_response-002 | Has substantive content — not empty or placeholder only | error (mandatory) | 1.0 | {{ results['security-sec-incident_response-002'].previous_status \| default('—') }} | {{ results['security-sec-incident_response-002'].status }} | {{ results['security-sec-incident_response-002'].trend_display }} | {{ results['security-sec-incident_response-002'].evidence \| default('—') }} |
| security-sec-incident_response-003 | Specific to this project — not generic boilerplate | warning (recommended) | 0.5 | {{ results['security-sec-incident_response-003'].previous_status \| default('—') }} | {{ results['security-sec-incident_response-003'].status }} | {{ results['security-sec-incident_response-003'].trend_display }} | {{ results['security-sec-incident_response-003'].evidence \| default('—') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Section | Rule | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.section_type }} | {{ r.id }} | {{ r.message }} | {{ r.evidence | default('—') }} | {{ 'Yes — regression' if r.is_new_failure else 'No — carried over' }} |
{% endfor %}
{% else %}
No failures across all 8 sections.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | security |
| Standard | documentation-standards |
| Section Rule Files | `audit/deterministic/section/03-security/*.yaml` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
