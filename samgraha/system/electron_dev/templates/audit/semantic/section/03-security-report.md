# Semantic Section Report — Security

**Document:** {{ document_path }}
**Standard:** `documentation-standards/03-security-standards.md`
**Audit Date:** {{ created_at }}
**Auditor:** LLM ({{ model_name }})
**Revision:** {{ revision_number }}

---

## Score

**Semantic Section Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
overall = average of the section scores below, for sections actually present in the document
section_score = sum of passed criterion points in that section, capped at 100
# calculation: semantic_section_v1
```

### Score History

| Revision | Date | Score | vs. Previous | vs. Baseline |
|---:|---|---:|---|---|
{% for r in revision_history -%}
| {{ r.revision }} | {{ r.date }} | {{ r.score }} / 100 | {{ r.delta_previous_display }} | {{ r.delta_baseline_display }} |
{% endfor -%}
| {{ revision_number }} (current) | {{ created_at }} | {{ score }} / 100 | {{ delta_previous_display }} | {{ delta_baseline_display }} |

{% if not previous_score %}No prior runs — this revision is the baseline every future run is compared against.{% endif %}

### Score by Model

| Model | Runs | Avg Score | Min | Max |
|---|---:|---:|---:|---|
{% for m in model_scores -%}
| {{ m.model_name }} | {{ m.run_count }} | {{ m.avg_score }} / 100 | {{ m.min_score }} / 100 | {{ m.max_score }} / 100 |
{% endfor %}

### Section Scores

| # | Section | Required | Score | Previous | Trend |
|---:|---|:---:|---:|---:|---|
| 1 | Threat Model | **required** | {{ sections.threat_model.score }} / 100 | {{ sections.threat_model.previous_score | default('—') }} | {{ sections.threat_model.trend_display }} |
| 2 | Data Classification | **required** | {{ sections.data_classification.score }} / 100 | {{ sections.data_classification.previous_score | default('—') }} | {{ sections.data_classification.trend_display }} |
| 3 | Security Principles | **required** | {{ sections.security_principles.score }} / 100 | {{ sections.security_principles.previous_score | default('—') }} | {{ sections.security_principles.trend_display }} |
| 4 | Purpose | **required** | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 5 | Constraints | **required** | {{ sections.constraints.score }} / 100 | {{ sections.constraints.previous_score | default('—') }} | {{ sections.constraints.trend_display }} |
| 6 | Traceability | **required** | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |
| 7 | Compliance | optional | {{ sections.compliance.score }} / 100 | {{ sections.compliance.previous_score | default('—') }} | {{ sections.compliance.trend_display }} |
| 8 | Incident Response | optional | {{ sections.incident_response.score }} / 100 | {{ sections.incident_response.previous_score | default('—') }} | {{ sections.incident_response.trend_display }} |

A section absent from the document (among the optional ones) isn't scored at all here — it's a deterministic presence check, not a semantic quality judgment on nothing.

---

## 1. Threat Model — `section/03-security/01-threat_model.md`

**Why this matters:** Threat model and attack surface analysis — defines what can go wrong, who the attackers are, and how it's mitigated.

**Section Score: {{ sections.threat_model.score }} / 100** ({{ sections.threat_model.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['threat_model.C1'].previous_passed_display \| default('—') }} | {{ results['threat_model.C1'].passed_display }} | {{ results['threat_model.C1'].trend_display }} | {{ results['threat_model.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['threat_model.C2'].previous_passed_display \| default('—') }} | {{ results['threat_model.C2'].passed_display }} | {{ results['threat_model.C2'].trend_display }} | {{ results['threat_model.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['threat_model.C3'].previous_passed_display \| default('—') }} | {{ results['threat_model.C3'].passed_display }} | {{ results['threat_model.C3'].trend_display }} | {{ results['threat_model.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

## 2. Data Classification — `02-data_classification.md`

**Why this matters:** Data classification and handling — defines how sensitive data is categorized and what protections apply at each tier.

**Section Score: {{ sections.data_classification.score }} / 100** ({{ sections.data_classification.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['data_classification.C1'].previous_passed_display \| default('—') }} | {{ results['data_classification.C1'].passed_display }} | {{ results['data_classification.C1'].trend_display }} | {{ results['data_classification.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['data_classification.C2'].previous_passed_display \| default('—') }} | {{ results['data_classification.C2'].passed_display }} | {{ results['data_classification.C2'].trend_display }} | {{ results['data_classification.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['data_classification.C3'].previous_passed_display \| default('—') }} | {{ results['data_classification.C3'].passed_display }} | {{ results['data_classification.C3'].trend_display }} | {{ results['data_classification.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

## 3. Security Principles — `03-security_principles.md`

**Why this matters:** Security principles and constraints — defines the non-negotiable rules that guide every security decision in the system.

**Section Score: {{ sections.security_principles.score }} / 100** ({{ sections.security_principles.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['security_principles.C1'].previous_passed_display \| default('—') }} | {{ results['security_principles.C1'].passed_display }} | {{ results['security_principles.C1'].trend_display }} | {{ results['security_principles.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['security_principles.C2'].previous_passed_display \| default('—') }} | {{ results['security_principles.C2'].passed_display }} | {{ results['security_principles.C2'].trend_display }} | {{ results['security_principles.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['security_principles.C3'].previous_passed_display \| default('—') }} | {{ results['security_principles.C3'].passed_display }} | {{ results['security_principles.C3'].trend_display }} | {{ results['security_principles.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

## 4. Purpose — `04-purpose.md`

**Why this matters:** Security purpose and compliance goals — defines why this security documentation exists and what it covers.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['purpose.C1'].previous_passed_display \| default('—') }} | {{ results['purpose.C1'].passed_display }} | {{ results['purpose.C1'].trend_display }} | {{ results['purpose.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['purpose.C2'].previous_passed_display \| default('—') }} | {{ results['purpose.C2'].passed_display }} | {{ results['purpose.C2'].trend_display }} | {{ results['purpose.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['purpose.C3'].previous_passed_display \| default('—') }} | {{ results['purpose.C3'].passed_display }} | {{ results['purpose.C3'].trend_display }} | {{ results['purpose.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

## 5. Constraints — `05-constraints.md`

**Why this matters:** Security constraints and requirements — defines the boundaries on security decisions that must hold regardless of design.

**Section Score: {{ sections.constraints.score }} / 100** ({{ sections.constraints.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['constraints.C1'].previous_passed_display \| default('—') }} | {{ results['constraints.C1'].passed_display }} | {{ results['constraints.C1'].trend_display }} | {{ results['constraints.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['constraints.C2'].previous_passed_display \| default('—') }} | {{ results['constraints.C2'].passed_display }} | {{ results['constraints.C2'].trend_display }} | {{ results['constraints.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['constraints.C3'].previous_passed_display \| default('—') }} | {{ results['constraints.C3'].passed_display }} | {{ results['constraints.C3'].trend_display }} | {{ results['constraints.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

## 6. Traceability — `06-traceability.md`

**Why this matters:** Security traceability to threats and requirements — maps security decisions back to vision-level goals and forward to Architecture and Engineering.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['traceability.C1'].previous_passed_display \| default('—') }} | {{ results['traceability.C1'].passed_display }} | {{ results['traceability.C1'].trend_display }} | {{ results['traceability.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['traceability.C2'].previous_passed_display \| default('—') }} | {{ results['traceability.C2'].passed_display }} | {{ results['traceability.C2'].trend_display }} | {{ results['traceability.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['traceability.C3'].previous_passed_display \| default('—') }} | {{ results['traceability.C3'].passed_display }} | {{ results['traceability.C3'].trend_display }} | {{ results['traceability.C3'].evidence.excerpt \| default('—') }} |

C1: section exists with substantive content specific to this project. C2: content is internally consistent and does not contradict other sections. C3: content includes concrete examples, evidence, or project-specific detail.

## 7. Compliance — `07-compliance.md`

**Why this matters:** Compliance Requirements names the regulatory regimes the system must satisfy, their scope of applicability, and traces each obligation to the control that satisfies it.

**Section Score: {{ sections.compliance.score }} / 100** ({{ sections.compliance.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['compliance.C1'].previous_passed_display \| default('—') }} | {{ results['compliance.C1'].passed_display }} | {{ results['compliance.C1'].trend_display }} | {{ results['compliance.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['compliance.C2'].previous_passed_display \| default('—') }} | {{ results['compliance.C2'].passed_display }} | {{ results['compliance.C2'].trend_display }} | {{ results['compliance.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['compliance.C3'].previous_passed_display \| default('—') }} | {{ results['compliance.C3'].passed_display }} | {{ results['compliance.C3'].trend_display }} | {{ results['compliance.C3'].evidence.excerpt \| default('—') }} |

C1: compliance regimes named specifically. C2: scope and applicability stated per regime. C3: obligation-to-downstream-control traceability shown.

## 8. Incident Response — `08-incident_response.md`

**Why this matters:** Incident Response defines how a security incident is detected, escalated, communicated, and recovered from — at the outcome level, not a tooling mandate.

**Section Score: {{ sections.incident_response.score }} / 100** ({{ sections.incident_response.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['incident_response.C1'].previous_passed_display \| default('—') }} | {{ results['incident_response.C1'].passed_display }} | {{ results['incident_response.C1'].trend_display }} | {{ results['incident_response.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['incident_response.C2'].previous_passed_display \| default('—') }} | {{ results['incident_response.C2'].passed_display }} | {{ results['incident_response.C2'].trend_display }} | {{ results['incident_response.C2'].evidence.excerpt \| default('—') }} |
| C3 | mandatory | 20 | {{ results['incident_response.C3'].previous_passed_display \| default('—') }} | {{ results['incident_response.C3'].passed_display }} | {{ results['incident_response.C3'].trend_display }} | {{ results['incident_response.C3'].evidence.excerpt \| default('—') }} |
| C4 | recommended | 20 | {{ results['incident_response.C4'].previous_passed_display \| default('—') }} | {{ results['incident_response.C4'].passed_display }} | {{ results['incident_response.C4'].trend_display }} | {{ results['incident_response.C4'].evidence.excerpt \| default('—') }} |

C1: detection expectations stated. C2: escalation paths defined with roles. C3: communication requirements specified. C4: recovery objectives are measurable.

---

## All Findings

{% if findings | length > 0 %}
| Section | Criterion | Severity | Evidence | Message | New This Run? |
|---|---|---|---|---|---|
{% for f in findings -%}
| {{ f.section_type }} | {{ f.criterion_id }} | {{ f.severity }} | {{ f.evidence.excerpt | default('—') }} | {{ f.message }} | {{ 'Yes — regression' if f.is_new_finding else 'No — carried over' }} |
{% endfor %}
{% else %}
No findings.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | security |
| Standard | documentation-standards |
| Section Rubric Files | `audit/semantic/section/03-security/*.md` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
