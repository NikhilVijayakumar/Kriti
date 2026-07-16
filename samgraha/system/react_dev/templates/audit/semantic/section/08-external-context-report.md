# Semantic Section Report — External Context

**Document:** {{ document_path }}
**Standard:** `documentation-standards/08-external-context-standards.md`
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
| 1 | Purpose | **required** | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 2 | Integration Contract | **required** | {{ sections.integration_contract.score }} / 100 | {{ sections.integration_contract.previous_score | default('—') }} | {{ sections.integration_contract.trend_display }} |
| 3 | Constraints | optional | {{ sections.constraints.score }} / 100 | {{ sections.constraints.previous_score | default('—') }} | {{ sections.constraints.trend_display }} |
| 4 | Dependencies | optional | {{ sections.dependencies.score }} / 100 | {{ sections.dependencies.previous_score | default('—') }} | {{ sections.dependencies.trend_display }} |
| 5 | Traceability | optional | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |

A section absent from the document (among the optional ones) isn't scored at all here — it's a deterministic presence check, not a semantic quality judgment on nothing.

---

## 1. Purpose — `section/08-external-context/01-purpose.md`

**Why this matters:** External context documents describe how the system depends on, integrates with, and is constrained by external systems. Purpose must clearly define why each external dependency exists and what role it plays.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 35 | {{ results['purpose.C1'].previous_passed_display \| default('—') }} | {{ results['purpose.C1'].passed_display }} | {{ results['purpose.C1'].trend_display }} | {{ results['purpose.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 35 | {{ results['purpose.C2'].previous_passed_display \| default('—') }} | {{ results['purpose.C2'].passed_display }} | {{ results['purpose.C2'].trend_display }} | {{ results['purpose.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['purpose.C3'].previous_passed_display \| default('—') }} | {{ results['purpose.C3'].passed_display }} | {{ results['purpose.C3'].trend_display }} | {{ results['purpose.C3'].evidence.excerpt \| default('—') }} |

C1: purpose stated for every external dependency. C2: business justification documented. C3: scope boundaries clearly defined.

## 2. Integration Contract — `02-integration_contract.md`

**Why this matters:** Integration contracts define the formal interface between the system and external dependencies — API endpoints, data schemas, protocol versions, authentication mechanisms, and expected behaviors. They serve as the source of truth for integration correctness.

**Section Score: {{ sections.integration_contract.score }} / 100** ({{ sections.integration_contract.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 25 | {{ results['integration_contract.C1'].previous_passed_display \| default('—') }} | {{ results['integration_contract.C1'].passed_display }} | {{ results['integration_contract.C1'].trend_display }} | {{ results['integration_contract.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 25 | {{ results['integration_contract.C2'].previous_passed_display \| default('—') }} | {{ results['integration_contract.C2'].passed_display }} | {{ results['integration_contract.C2'].trend_display }} | {{ results['integration_contract.C2'].evidence.excerpt \| default('—') }} |
| C3 | mandatory | 25 | {{ results['integration_contract.C3'].previous_passed_display \| default('—') }} | {{ results['integration_contract.C3'].passed_display }} | {{ results['integration_contract.C3'].trend_display }} | {{ results['integration_contract.C3'].evidence.excerpt \| default('—') }} |
| C4 | recommended | 25 | {{ results['integration_contract.C4'].previous_passed_display \| default('—') }} | {{ results['integration_contract.C4'].passed_display }} | {{ results['integration_contract.C4'].trend_display }} | {{ results['integration_contract.C4'].evidence.excerpt \| default('—') }} |

C1: contract exists for every external dependency. C2: API version or protocol version is pinned. C3: request/response schemas documented. C4: rate limits, retry, and error handling defined.

## 3. Constraints — `03-constraints.md`

**Why this matters:** Constraints capture the limitations, requirements, and boundaries imposed by external systems on the design and operation of the internal system — performance bounds, data volume limits, compliance requirements, and operational restrictions originating outside the system boundary.

**Section Score: {{ sections.constraints.score }} / 100** ({{ sections.constraints.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['constraints.C1'].previous_passed_display \| default('—') }} | {{ results['constraints.C1'].passed_display }} | {{ results['constraints.C1'].trend_display }} | {{ results['constraints.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['constraints.C2'].previous_passed_display \| default('—') }} | {{ results['constraints.C2'].passed_display }} | {{ results['constraints.C2'].trend_display }} | {{ results['constraints.C2'].evidence.excerpt \| default('—') }} |
| C3 | mandatory | 20 | {{ results['constraints.C3'].previous_passed_display \| default('—') }} | {{ results['constraints.C3'].passed_display }} | {{ results['constraints.C3'].trend_display }} | {{ results['constraints.C3'].evidence.excerpt \| default('—') }} |
| C4 | recommended | 20 | {{ results['constraints.C4'].previous_passed_display \| default('—') }} | {{ results['constraints.C4'].passed_display }} | {{ results['constraints.C4'].trend_display }} | {{ results['constraints.C4'].evidence.excerpt \| default('—') }} |

C1: constraints enumerated per external dependency. C2: each constraint has measurable threshold. C3: constraint source attributed. C4: design impact described for each constraint.

## 4. Dependencies — `04-dependencies.md`

**Why this matters:** Dependencies document the external libraries, services, APIs, SDKs, and infrastructure that the system relies on at build time, deploy time, and runtime. They must capture version pinning, license compatibility, upgrade cadence, and end-of-life risk for every dependency.

**Section Score: {{ sections.dependencies.score }} / 100** ({{ sections.dependencies.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 25 | {{ results['dependencies.C1'].previous_passed_display \| default('—') }} | {{ results['dependencies.C1'].passed_display }} | {{ results['dependencies.C1'].trend_display }} | {{ results['dependencies.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 25 | {{ results['dependencies.C2'].previous_passed_display \| default('—') }} | {{ results['dependencies.C2'].passed_display }} | {{ results['dependencies.C2'].trend_display }} | {{ results['dependencies.C2'].evidence.excerpt \| default('—') }} |
| C3 | mandatory | 25 | {{ results['dependencies.C3'].previous_passed_display \| default('—') }} | {{ results['dependencies.C3'].passed_display }} | {{ results['dependencies.C3'].trend_display }} | {{ results['dependencies.C3'].evidence.excerpt \| default('—') }} |
| C4 | recommended | 25 | {{ results['dependencies.C4'].previous_passed_display \| default('—') }} | {{ results['dependencies.C4'].passed_display }} | {{ results['dependencies.C4'].trend_display }} | {{ results['dependencies.C4'].evidence.excerpt \| default('—') }} |

C1: all dependencies cataloged with pinned versions. C2: dependency type and license recorded. C3: runtime vs build-time dependency separation. C4: upgrade cadence, deprecation tracking, and security patch velocity documented.

## 5. Traceability — `05-traceability.md`

**Why this matters:** Traceability maps each external dependency and integration point back to its authoritative source — vendor documentation, SLA contracts, API specs, or configuration registries. It ensures every external-context claim is verifiable against an upstream source.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['traceability.C1'].previous_passed_display \| default('—') }} | {{ results['traceability.C1'].passed_display }} | {{ results['traceability.C1'].trend_display }} | {{ results['traceability.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['traceability.C2'].previous_passed_display \| default('—') }} | {{ results['traceability.C2'].passed_display }} | {{ results['traceability.C2'].trend_display }} | {{ results['traceability.C2'].evidence.excerpt \| default('—') }} |
| C3 | mandatory | 20 | {{ results['traceability.C3'].previous_passed_display \| default('—') }} | {{ results['traceability.C3'].passed_display }} | {{ results['traceability.C3'].trend_display }} | {{ results['traceability.C3'].evidence.excerpt \| default('—') }} |
| C4 | recommended | 20 | {{ results['traceability.C4'].previous_passed_display \| default('—') }} | {{ results['traceability.C4'].passed_display }} | {{ results['traceability.C4'].trend_display }} | {{ results['traceability.C4'].evidence.excerpt \| default('—') }} |

C1: every dependency has link to authoritative source. C2: integration contracts have bidirectional traceability. C3: external changes logged with internal impact notes. C4: traceability verification date present on each entry.

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
| Domain | external-context |
| Standard | documentation-standards |
| Section Rubric Files | `audit/semantic/section/08-external-context/*.md` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
