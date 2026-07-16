# Deterministic Section Report — External Context

**Document:** {{ document_path }}
**Standard:** `documentation-standards/08-external-context-standards.md`
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Deterministic Section Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
overall = average of the 5 section scores below
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
| 1 | Purpose | **required** | 4.0 | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 2 | Integration Contract | **required** | 4.0 | {{ sections.integration_contract.score }} / 100 | {{ sections.integration_contract.previous_score | default('—') }} | {{ sections.integration_contract.trend_display }} |
| 3 | Constraints | optional | 1.5 | {{ sections.constraints.score }} / 100 | {{ sections.constraints.previous_score | default('—') }} | {{ sections.constraints.trend_display }} |
| 4 | Dependencies | optional | 1.5 | {{ sections.dependencies.score }} / 100 | {{ sections.dependencies.previous_score | default('—') }} | {{ sections.dependencies.trend_display }} |
| 5 | Traceability | optional | 1.5 | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |

The 2 required sections carry 8.0 of the document's 12.5 total rule weight — a document can only pass if those two are both present and internally sound; the remaining three are recommended-quality signal, not gating.

---

## 1. Purpose — `section/08-external-context/01-purpose.yaml` — weight 4.0 — **required**

**Why this matters:** Purpose is what tells a reader why this external context documentation exists at all before they read a single integration contract. A Purpose section that's missing, vague, or technology-leaking undermines every section that follows it.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ext-sec-purpose-001 | Purpose section exists | error (mandatory) | 1.5 | {{ results['ext-sec-purpose-001'].previous_status \| default('—') }} | {{ results['ext-sec-purpose-001'].status }} | {{ results['ext-sec-purpose-001'].trend_display }} | {{ results['ext-sec-purpose-001'].evidence \| default('—') }} |
| ext-sec-purpose-002 | States external context intent | error (mandatory) | 1.0 | {{ results['ext-sec-purpose-002'].previous_status \| default('—') }} | {{ results['ext-sec-purpose-002'].status }} | {{ results['ext-sec-purpose-002'].trend_display }} | {{ results['ext-sec-purpose-002'].evidence \| default('—') }} |
| ext-sec-purpose-003 | Technology-independent | error (mandatory) | 1.0 | {{ results['ext-sec-purpose-003'].previous_status \| default('—') }} | {{ results['ext-sec-purpose-003'].status }} | {{ results['ext-sec-purpose-003'].trend_display }} | {{ results['ext-sec-purpose-003'].evidence \| default('—') }} |
| ext-sec-purpose-004 | Scope boundaries defined | warning (recommended) | 0.5 | {{ results['ext-sec-purpose-004'].previous_status \| default('—') }} | {{ results['ext-sec-purpose-004'].status }} | {{ results['ext-sec-purpose-004'].trend_display }} | {{ results['ext-sec-purpose-004'].evidence \| default('—') }} |

## 2. Integration Contract — `02-integration_contract.yaml` — weight 4.0 — **required**

**Why this matters:** Integration contracts define the formal interface between the system and external dependencies — API endpoints, data schemas, protocol versions, authentication mechanisms, and expected behaviors. Without them, every integration is reverse-engineered from code instead of designed upfront.

**Section Score: {{ sections.integration_contract.score }} / 100** ({{ sections.integration_contract.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ext-sec-ic-001 | Integration contract section exists | error (mandatory) | 1.5 | {{ results['ext-sec-ic-001'].previous_status \| default('—') }} | {{ results['ext-sec-ic-001'].status }} | {{ results['ext-sec-ic-001'].trend_display }} | {{ results['ext-sec-ic-001'].evidence \| default('—') }} |
| ext-sec-ic-002 | Defines interfaces, protocols, or data formats | error (mandatory) | 1.0 | {{ results['ext-sec-ic-002'].previous_status \| default('—') }} | {{ results['ext-sec-ic-002'].status }} | {{ results['ext-sec-ic-002'].trend_display }} | {{ results['ext-sec-ic-002'].evidence \| default('—') }} |
| ext-sec-ic-003 | Technology-independent | error (mandatory) | 1.0 | {{ results['ext-sec-ic-003'].previous_status \| default('—') }} | {{ results['ext-sec-ic-003'].status }} | {{ results['ext-sec-ic-003'].trend_display }} | {{ results['ext-sec-ic-003'].evidence \| default('—') }} |
| ext-sec-ic-004 | System boundaries defined | warning (recommended) | 0.5 | {{ results['ext-sec-ic-004'].previous_status \| default('—') }} | {{ results['ext-sec-ic-004'].status }} | {{ results['ext-sec-ic-004'].trend_display }} | {{ results['ext-sec-ic-004'].evidence \| default('—') }} |

## 3. Constraints — `03-constraints.yaml` — weight 1.5 — optional

**Why this matters:** Constraints capture the limitations, requirements, and boundaries imposed by external systems on the design and operation of the internal system. Without them, every external limitation is discovered late — during integration testing or, worse, in production.

**Section Score: {{ sections.constraints.score }} / 100** ({{ sections.constraints.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ext-sec-con-001 | Constraints section present | warning (recommended) | 0.5 | {{ results['ext-sec-con-001'].previous_status \| default('—') }} | {{ results['ext-sec-con-001'].status }} | {{ results['ext-sec-con-001'].trend_display }} | {{ results['ext-sec-con-001'].evidence \| default('—') }} |
| ext-sec-con-002 | Constraints are clearly stated as discrete restrictions | warning (recommended) | 0.5 | {{ results['ext-sec-con-002'].previous_status \| default('—') }} | {{ results['ext-sec-con-002'].status }} | {{ results['ext-sec-con-002'].trend_display }} | {{ results['ext-sec-con-002'].evidence \| default('—') }} |
| ext-sec-con-003 | Constraints trace to external realities (regulations, vendor limits, physical constraints) | warning (recommended) | 0.5 | {{ results['ext-sec-con-003'].previous_status \| default('—') }} | {{ results['ext-sec-con-003'].status }} | {{ results['ext-sec-con-003'].trend_display }} | {{ results['ext-sec-con-003'].evidence \| default('—') }} |

## 4. Dependencies — `04-dependencies.yaml` — weight 1.5 — optional

**Why this matters:** Dependencies document the external libraries, services, APIs, SDKs, and infrastructure that the system relies on at build time, deploy time, and runtime. Without them, every dependency is discovered through build failures or runtime errors, not through design.

**Section Score: {{ sections.dependencies.score }} / 100** ({{ sections.dependencies.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ext-sec-dep-001 | Dependencies section present | warning (recommended) | 0.5 | {{ results['ext-sec-dep-001'].previous_status \| default('—') }} | {{ results['ext-sec-dep-001'].status }} | {{ results['ext-sec-dep-001'].trend_display }} | {{ results['ext-sec-dep-001'].evidence \| default('—') }} |
| ext-sec-dep-002 | Dependencies are enumerated | warning (recommended) | 0.5 | {{ results['ext-sec-dep-002'].previous_status \| default('—') }} | {{ results['ext-sec-dep-002'].status }} | {{ results['ext-sec-dep-002'].trend_display }} | {{ results['ext-sec-dep-002'].evidence \| default('—') }} |
| ext-sec-dep-003 | Dependencies distinguish direction (inbound vs outbound) | warning (recommended) | 0.5 | {{ results['ext-sec-dep-003'].previous_status \| default('—') }} | {{ results['ext-sec-dep-003'].status }} | {{ results['ext-sec-dep-003'].trend_display }} | {{ results['ext-sec-dep-003'].evidence \| default('—') }} |

## 5. Traceability — `05-traceability.yaml` — weight 1.5 — optional

**Why this matters:** Traceability maps each external dependency and integration point back to its authoritative source — vendor documentation, SLA contracts, API specs, or configuration registries. Without it, every external-context claim is unverifiable.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ext-sec-trace-001 | Traceability section present | warning (recommended) | 0.5 | {{ results['ext-sec-trace-001'].previous_status \| default('—') }} | {{ results['ext-sec-trace-001'].status }} | {{ results['ext-sec-trace-001'].trend_display }} | {{ results['ext-sec-trace-001'].evidence \| default('—') }} |
| ext-sec-trace-002 | Links to internal artifacts (Engineering, Feature Design, Feature Technical) | warning (recommended) | 0.5 | {{ results['ext-sec-trace-002'].previous_status \| default('—') }} | {{ results['ext-sec-trace-002'].status }} | {{ results['ext-sec-trace-002'].trend_display }} | {{ results['ext-sec-trace-002'].evidence \| default('—') }} |
| ext-sec-trace-003 | Identifies external source or authority | warning (recommended) | 0.5 | {{ results['ext-sec-trace-003'].previous_status \| default('—') }} | {{ results['ext-sec-trace-003'].status }} | {{ results['ext-sec-trace-003'].trend_display }} | {{ results['ext-sec-trace-003'].evidence \| default('—') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Section | Rule | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.section_type }} | {{ r.id }} | {{ r.message }} | {{ r.evidence | default('—') }} | {{ 'Yes — regression' if r.is_new_failure else 'No — carried over' }} |
{% endfor %}
{% else %}
No failures across all 5 sections.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | external-context |
| Standard | documentation-standards |
| Section Rule Files | `audit/deterministic/section/08-external-context/*.yaml` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
