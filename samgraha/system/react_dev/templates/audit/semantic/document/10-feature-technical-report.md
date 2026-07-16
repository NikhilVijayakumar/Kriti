# Semantic Whole-Document Report — Feature Technical

**Document:** {{ document_path }}
**Standard:** `documentation-standards/10-feature-technical-standards.md`
**Rubric:** `audit/semantic/document/10-feature-technical.md`
**Auditor:** LLM ({{ model_name }})
**Audit Date:** {{ created_at }}
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
| C1 — Cross-section consistency | mandatory | 40 | {{ results['C1'].previous_passed_display | default('—') }} | {{ results['C1'].passed_display }} | {{ results['C1'].trend_display }} |
| C2 — Terminology consistency | mandatory | 30 | {{ results['C2'].previous_passed_display | default('—') }} | {{ results['C2'].passed_display }} | {{ results['C2'].trend_display }} |
| C3 — Cross-document coherence | recommended | 30 | {{ results['C3'].previous_passed_display | default('—') }} | {{ results['C3'].passed_display }} | {{ results['C3'].trend_display }} |

C1 and C2 are mandatory — either one failing caps this score at 30 (only C3's points remain reachable). C3 alone failing still allows 70.

---

## Judgment

Verifies a Feature Technical Design document coheres internally — Participating Components, Component Interactions, Data Ownership, and Runtime Behavior must describe one consistent realization of the feature, not four independently-written sections. Section-level quality (is each section well-written on its own) is a separate concern, owned by the Semantic Section report; this report only catches problems that only exist when sections or documents are read together.

## Scoring Criteria — Detail

### C1 — mandatory, 0 or 40: Participating Components, Component Interactions, Data Ownership, and Runtime Behavior are mutually consistent

**What this catches:** a component in Component Interactions that Participating Components doesn't list; a data owner in Data Ownership that Runtime Behavior contradicts; a runtime sequence that implies a component not present in Participating Components.

**Previous:** {{ results['C1'].previous_passed_display | default('—') }} → **Current:** {{ results['C1'].passed_display }} ({{ results['C1'].trend_display }})
**Evidence:** {{ results['C1'].evidence.excerpt | default('—') }}
{% if not results['C1'].passed %}**Finding:** {{ results['C1'].message }}{% endif %}

### C2 — mandatory, 0 or 30: Terminology (component/data names) consistent across all sections and documents

**What this catches:** when the same component or data entity is named differently in different sections (e.g., "OrderValidator" in Component Interactions but "OrderChecker" in Data Ownership), readers cannot tell whether the difference is intentional or accidental.

**Previous:** {{ results['C2'].previous_passed_display | default('—') }} → **Current:** {{ results['C2'].passed_display }} ({{ results['C2'].trend_display }})
**Evidence:** {{ results['C2'].evidence.excerpt | default('—') }}
{% if not results['C2'].passed %}**Finding:** {{ results['C2'].message }}{% endif %}

### C3 — recommended, 0 or 30: All Feature Technical Design documents cohere as one system

**What this catches:** two Feature Technical Design documents that realize the same feature with contradictory component responsibilities, conflicting data ownership, or incompatible interaction models.

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
No findings — document reads as one coherent Feature Technical Design.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | feature-technical |
| Standard | documentation-standards |
| Rubric File | `audit/semantic/document/10-feature-technical.md` |
| Auditor | LLM ({{ model_name }}) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
