# Deterministic Section Report — Prototype

**Document:** {{ document_path }}
**Standard:** `documentation-standards/11-prototype-standards.md`
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Deterministic Section Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
overall = average of the 6 section scores below
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
| 1 | Scope | **required** | 3.5 | {{ sections.scope.score }} / 100 | {{ sections.scope.previous_score | default('—') }} | {{ sections.scope.trend_display }} |
| 2 | Mock APIs | **required** | 3.5 | {{ sections.mock_apis.score }} / 100 | {{ sections.mock_apis.previous_score | default('—') }} | {{ sections.mock_apis.trend_display }} |
| 3 | Data Model | **required** | 3.5 | {{ sections.data_model.score }} / 100 | {{ sections.data_model.previous_score | default('—') }} | {{ sections.data_model.trend_display }} |
| 4 | Purpose | optional | 1.5 | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 5 | Constraints | optional | 1.5 | {{ sections.constraints.score }} / 100 | {{ sections.constraints.previous_score | default('—') }} | {{ sections.constraints.trend_display }} |
| 6 | Traceability | optional | 2.0 | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |

The 3 required sections carry 10.5 of the document's 15.5 total rule weight — a document can only pass if those three are both present and internally sound; the remaining three are recommended-quality signal, not gating.

---

## 1. Scope — `section/11-prototype/01-scope.yaml` — weight 3.5 — **required**

**Why this matters:** Scope defines the boundary between what the prototype simulates and what it ignores. Over-scoping inflates cost and delays answers; under-scoping produces misleading results. Scope must explicitly state inclusion and exclusion boundaries relative to the prototype purpose.

**Section Score: {{ sections.scope.score }} / 100** ({{ sections.scope.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| proto-sec-scope-001 | Scope section exists | error (mandatory) | 1.5 | {{ results['proto-sec-scope-001'].previous_status \| default('—') }} | {{ results['proto-sec-scope-001'].status }} | {{ results['proto-sec-scope-001'].trend_display }} | {{ results['proto-sec-scope-001'].evidence \| default('—') }} |
| proto-sec-scope-002 | Defines prototype boundaries — covers what's in scope and what's excluded | error (mandatory) | 1.0 | {{ results['proto-sec-scope-002'].previous_status \| default('—') }} | {{ results['proto-sec-scope-002'].status }} | {{ results['proto-sec-scope-002'].trend_display }} | {{ results['proto-sec-scope-002'].evidence \| default('—') }} |
| proto-sec-scope-003 | References upstream Feature Design document | warning (recommended) | 0.5 | {{ results['proto-sec-scope-003'].previous_status \| default('—') }} | {{ results['proto-sec-scope-003'].status }} | {{ results['proto-sec-scope-003'].trend_display }} | {{ results['proto-sec-scope-003'].evidence \| default('—') }} |
| proto-sec-scope-004 | References upstream Feature Technical document | warning (recommended) | 0.5 | {{ results['proto-sec-scope-004'].previous_status \| default('—') }} | {{ results['proto-sec-scope-004'].status }} | {{ results['proto-sec-scope-004'].trend_display }} | {{ results['proto-sec-scope-004'].evidence \| default('—') }} |

## 2. Mock APIs — `02-mock_apis.yaml` — weight 3.5 — **required**

**Why this matters:** Mock APIs are the prototype's simulation surface — they must faithfully represent the real interface contract without implementing production logic. Mismatched mocks produce false confidence or false negatives, and mocks referencing undefined types create gaps between what's simulated and what's modeled.

**Section Score: {{ sections.mock_apis.score }} / 100** ({{ sections.mock_apis.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| proto-sec-mock-001 | Mock APIs section exists | error (mandatory) | 1.5 | {{ results['proto-sec-mock-001'].previous_status \| default('—') }} | {{ results['proto-sec-mock-001'].status }} | {{ results['proto-sec-mock-001'].trend_display }} | {{ results['proto-sec-mock-001'].evidence \| default('—') }} |
| proto-sec-mock-002 | Defines at least one mock API endpoint | error (mandatory) | 1.0 | {{ results['proto-sec-mock-002'].previous_status \| default('—') }} | {{ results['proto-sec-mock-002'].status }} | {{ results['proto-sec-mock-002'].trend_display }} | {{ results['proto-sec-mock-002'].evidence \| default('—') }} |
| proto-sec-mock-003 | Each endpoint defines request and response data shapes | warning (recommended) | 0.5 | {{ results['proto-sec-mock-003'].previous_status \| default('—') }} | {{ results['proto-sec-mock-003'].status }} | {{ results['proto-sec-mock-003'].trend_display }} | {{ results['proto-sec-mock-003'].evidence \| default('—') }} |
| proto-sec-mock-004 | Endpoint types reference types defined in Data Model section | warning (recommended) | 0.5 | {{ results['proto-sec-mock-004'].previous_status \| default('—') }} | {{ results['proto-sec-mock-004'].status }} | {{ results['proto-sec-mock-004'].trend_display }} | {{ results['proto-sec-mock-004'].evidence \| default('—') }} |

## 3. Data Model — `03-data_model.yaml` — weight 3.5 — **required**

**Why this matters:** The data model is the prototype's entity vocabulary — it defines what types exist, what fields they have, and how they relate. A data model missing fields that mock APIs reference, or defining types never used, creates a mismatch between simulation and documentation that invalidates prototype results.

**Section Score: {{ sections.data_model.score }} / 100** ({{ sections.data_model.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| proto-sec-data-001 | Data Model section exists | error (mandatory) | 1.5 | {{ results['proto-sec-data-001'].previous_status \| default('—') }} | {{ results['proto-sec-data-001'].status }} | {{ results['proto-sec-data-001'].trend_display }} | {{ results['proto-sec-data-001'].evidence \| default('—') }} |
| proto-sec-data-002 | Defines at least one type or schema | error (mandatory) | 1.0 | {{ results['proto-sec-data-002'].previous_status \| default('—') }} | {{ results['proto-sec-data-002'].status }} | {{ results['proto-sec-data-002'].trend_display }} | {{ results['proto-sec-data-002'].evidence \| default('—') }} |
| proto-sec-data-003 | Each defined type has at least one field or property | warning (recommended) | 0.5 | {{ results['proto-sec-data-003'].previous_status \| default('—') }} | {{ results['proto-sec-data-003'].status }} | {{ results['proto-sec-data-003'].trend_display }} | {{ results['proto-sec-data-003'].evidence \| default('—') }} |
| proto-sec-data-004 | References upstream Feature Technical data structures | warning (recommended) | 0.5 | {{ results['proto-sec-data-004'].previous_status \| default('—') }} | {{ results['proto-sec-data-004'].status }} | {{ results['proto-sec-data-004'].trend_display }} | {{ results['proto-sec-data-004'].evidence \| default('—') }} |

## 4. Purpose — `04-purpose.yaml` — weight 1.5 — optional

**Why this matters:** A prototype must have a clearly stated purpose that defines what question it answers or what risk it mitigates. Without an explicit purpose, a prototype cannot be evaluated for fitness — the evaluator doesn't know what "success" means.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| proto-sec-purpose-001 | Purpose section exists | warning (recommended) | 0.5 | {{ results['proto-sec-purpose-001'].previous_status \| default('—') }} | {{ results['proto-sec-purpose-001'].status }} | {{ results['proto-sec-purpose-001'].trend_display }} | {{ results['proto-sec-purpose-001'].evidence \| default('—') }} |
| proto-sec-purpose-002 | States prototype intent — why this prototype exists | warning (recommended) | 0.5 | {{ results['proto-sec-purpose-002'].previous_status \| default('—') }} | {{ results['proto-sec-purpose-002'].status }} | {{ results['proto-sec-purpose-002'].trend_display }} | {{ results['proto-sec-purpose-002'].evidence \| default('—') }} |
| proto-sec-purpose-003 | Defines scope boundaries — what the prototype is and is not | warning (recommended) | 0.5 | {{ results['proto-sec-purpose-003'].previous_status \| default('—') }} | {{ results['proto-sec-purpose-003'].status }} | {{ results['proto-sec-purpose-003'].trend_display }} | {{ results['proto-sec-purpose-003'].evidence \| default('—') }} |

## 5. Constraints — `05-constraints.yaml` — weight 1.5 — optional

**Why this matters:** Constraints capture the known limitations, assumptions, and guardrails of a prototype. Every prototype operates under artificial conditions; undisclosed constraints mislead evaluators into overgeneralizing results. Constraints must be surfaced, documented, and traceable to their source.

**Section Score: {{ sections.constraints.score }} / 100** ({{ sections.constraints.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| proto-sec-constraints-001 | Constraints section exists | warning (recommended) | 0.5 | {{ results['proto-sec-constraints-001'].previous_status \| default('—') }} | {{ results['proto-sec-constraints-001'].status }} | {{ results['proto-sec-constraints-001'].trend_display }} | {{ results['proto-sec-constraints-001'].evidence \| default('—') }} |
| proto-sec-constraints-002 | Lists at least one constraint or limitation | warning (recommended) | 0.5 | {{ results['proto-sec-constraints-002'].previous_status \| default('—') }} | {{ results['proto-sec-constraints-002'].status }} | {{ results['proto-sec-constraints-002'].trend_display }} | {{ results['proto-sec-constraints-002'].evidence \| default('—') }} |
| proto-sec-constraints-003 | Constraints trace to their source (architecture, security, or engineering standards) | warning (recommended) | 0.5 | {{ results['proto-sec-constraints-003'].previous_status \| default('—') }} | {{ results['proto-sec-constraints-003'].status }} | {{ results['proto-sec-constraints-003'].trend_display }} | {{ results['proto-sec-constraints-003'].evidence \| default('—') }} |

## 6. Traceability — `06-traceability.yaml` — weight 2.0 — optional

**Why this matters:** Traceability connects prototype artifacts — purpose, scope, mocks, data model, constraints — into a coherent chain. Every design decision should be traceable back to the prototype purpose and forward to the code or configuration that implements it. Broken traceability means broken auditability.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| proto-sec-trace-001 | Traceability section exists | warning (recommended) | 0.5 | {{ results['proto-sec-trace-001'].previous_status \| default('—') }} | {{ results['proto-sec-trace-001'].status }} | {{ results['proto-sec-trace-001'].trend_display }} | {{ results['proto-sec-trace-001'].evidence \| default('—') }} |
| proto-sec-trace-002 | Links to originating Feature Design document | warning (recommended) | 0.5 | {{ results['proto-sec-trace-002'].previous_status \| default('—') }} | {{ results['proto-sec-trace-002'].status }} | {{ results['proto-sec-trace-002'].trend_display }} | {{ results['proto-sec-trace-002'].evidence \| default('—') }} |
| proto-sec-trace-003 | Links to originating Feature Technical document | warning (recommended) | 0.5 | {{ results['proto-sec-trace-003'].previous_status \| default('—') }} | {{ results['proto-sec-trace-003'].status }} | {{ results['proto-sec-trace-003'].trend_display }} | {{ results['proto-sec-trace-003'].evidence \| default('—') }} |
| proto-sec-trace-004 | Traces prototype back to vision statement | warning (recommended) | 0.5 | {{ results['proto-sec-trace-004'].previous_status \| default('—') }} | {{ results['proto-sec-trace-004'].status }} | {{ results['proto-sec-trace-004'].trend_display }} | {{ results['proto-sec-trace-004'].evidence \| default('—') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Section | Rule | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.section_type }} | {{ r.id }} | {{ r.message }} | {{ r.evidence | default('—') }} | {{ 'Yes — regression' if r.is_new_failure else 'No — carried over' }} |
{% endfor %}
{% else %}
No failures across all 6 sections.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | prototype |
| Standard | documentation-standards |
| Section Rule Files | `audit/deterministic/section/11-prototype/*.yaml` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
