# Semantic Whole-Document Report — Prototype

**Document:** {{ document_path }}
**Standard:** `documentation-standards/11-prototype-standards.md`
**Rubric:** `audit/semantic/document/11-prototype.md`
**Audit Date:** {{ created_at }}
**Auditor:** LLM ({{ model_name }})
**Revision:** {{ revision_number }}

---

## Score

**Semantic Whole Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
score = sum of passed criterion scores, capped at 100
# calculation: semantic_document_v1
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

### Scoring Criteria

| Criterion | Weight | Points | Previous | Current | Trend |
|---|---|---:|---|---|---|
| C1 — Mock/Data Model consistency | mandatory | 40 | {{ results['C1'].previous_passed_display | default('—') }} | {{ results['C1'].passed_display }} | {{ results['C1'].trend_display }} |
| C2 — Scope/Mock coverage | mandatory | 30 | {{ results['C2'].previous_passed_display | default('—') }} | {{ results['C2'].passed_display }} | {{ results['C2'].trend_display }} |
| C3 — Traceability accuracy | recommended | 30 | {{ results['C3'].previous_passed_display | default('—') }} | {{ results['C3'].passed_display }} | {{ results['C3'].trend_display }} |

C1 and C2 are mandatory — either one failing caps this score at 30 (only C3's points remain reachable). C3 alone failing still allows 70.

---

## Judgment

Verifies a Prototype document coheres as one falsifiable experiment — Mock APIs match the Data Model, Scope's in-scope items are actually mocked, Traceability's upstream/downstream links hold. Section-level quality is owned by `audit/semantic/section/prototype/`; this file owns whether the pieces fit together as one coherent simulation.

## Scoring Criteria — Detail

### C1 — mandatory, 0 or 40: Mock APIs and Data Model use consistent entities/fields

**What this catches:** a mock API request/response referencing a field or entity absent from the Data Model section — the mock simulates something the data model doesn't define, creating a gap between simulation and documentation.

**Previous:** {{ results['C1'].previous_passed_display | default('—') }} → **Current:** {{ results['C1'].passed_display }} ({{ results['C1'].trend_display }})
**Evidence:** {{ results['C1'].evidence.excerpt | default('—') }}
{% if not results['C1'].passed %}**Finding:** {{ results['C1'].message }}{% endif %}

### C2 — mandatory, 0 or 30: Scope's in-scope items are actually covered by Mock APIs

**What this catches:** scope claims something is in-scope that has no corresponding mock — the prototype promises coverage it doesn't deliver, producing misleading evaluation results.

**Previous:** {{ results['C2'].previous_passed_display | default('—') }} → **Current:** {{ results['C2'].passed_display }} ({{ results['C2'].trend_display }})
**Evidence:** {{ results['C2'].evidence.excerpt | default('—') }}
{% if not results['C2'].passed %}**Finding:** {{ results['C2'].message }}{% endif %}

### C3 — recommended, 0 or 30: Traceability accurately reflects what's actually validated

**What this catches:** traceability claiming to validate a Feature Design the prototype doesn't actually touch — aspirational traceability that overstates the prototype's scope.

**Previous:** {{ results['C3'].previous_passed_display | default('—') }} → **Current:** {{ results['C3'].passed_display }} ({{ results['C3'].trend_display }})
**Evidence:** {{ results['C3'].evidence.excerpt | default('—') }}
{% if not results['C3'].passed %}**Finding:** {{ results['C3'].message }}{% endif %}

---

## All Findings

{% if findings | length > 0 %}
| Criterion | Severity | Evidence | Message | New This Run? |
|---|---|---|---|---|
{% for f in findings -%}
| {{ f.criterion_id }} | {{ f.severity }} | {{ f.evidence.excerpt | default('—') }} | {{ f.message }} | {{ 'Yes — regression' if f.is_new_finding else 'No — carried over' }} |
{% endfor %}
{% else %}
No findings — document reads as one coherent prototype experiment.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | prototype |
| Standard | documentation-standards |
| Rubric File | `audit/semantic/document/11-prototype.md` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
