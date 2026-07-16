# Semantic Whole-Document Report — QA

**Document:** {{ document_path }}
**Standard:** `documentation-standards/12-qa-standards.md`
**Rubric:** `audit/semantic/document/12-qa.md`
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
| C1 — Test Strategy priorities reflected in section depth | mandatory | 40 | {{ results['C1'].previous_passed_display | default('—') }} | {{ results['C1'].passed_display }} | {{ results['C1'].trend_display }} |
| C2 — Integration Testing boundaries consistent with Architecture(05) | mandatory | 30 | {{ results['C2'].previous_passed_display | default('—') }} | {{ results['C2'].passed_display }} | {{ results['C2'].trend_display }} |
| C3 — E2E workflows traceable to Feature-Technical(10) runtime behavior | recommended | 30 | {{ results['C3'].previous_passed_display | default('—') }} | {{ results['C3'].passed_display }} | {{ results['C3'].trend_display }} |

C1 and C2 are mandatory — either one failing caps this score at 30 (only C3's points remain reachable). C3 alone failing still allows 70.

---

## Judgment

Verifies a QA document's test types cohere as one strategy — Test Strategy's priority mapping is actually reflected in Unit/Integration/E2E/Load/Scalability/Security Testing, not a plan that the rest of the document ignores. Section-level quality per test type is owned by the Semantic Section report; this report only catches problems that only exist when sections are read together.

## Scoring Criteria — Detail

### C1 — mandatory, 0 or 40: Test Strategy's priorities are reflected in the depth of each test type section

**What this catches:** Test Strategy marks Security Testing as highest priority, but the Security Testing section is one sentence. Or: a test type Test Strategy marks as deprioritized has more detail than one marked critical.

**Previous:** {{ results['C1'].previous_passed_display | default('—') }} → **Current:** {{ results['C1'].passed_display }} ({{ results['C1'].trend_display }})
**Evidence:** {{ results['C1'].evidence.excerpt | default('—') }}
{% if not results['C1'].passed %}**Finding:** {{ results['C1'].message }}{% endif %}

### C2 — mandatory, 0 or 30: Integration Testing boundaries consistent with Architecture(05)

**What this catches:** Integration Testing tests boundaries that don't exist in Architecture, or ignores boundaries Architecture defines. No tested boundary that Architecture doesn't define, no defined boundary left untested.

**Previous:** {{ results['C2'].previous_passed_display | default('—') }} → **Current:** {{ results['C2'].passed_display }} ({{ results['C2'].trend_display }})
**Evidence:** {{ results['C2'].evidence.excerpt | default('—') }}
{% if not results['C2'].passed %}**Finding:** {{ results['C2'].message }}{% endif %}

### C3 — recommended, 0 or 30: E2E workflows traceable to Feature-Technical(10) runtime behavior

**What this catches:** E2E Testing invents runtime workflows with no corresponding Feature-Technical runtime behavior. Workflows that exist in Feature-Technical but are absent from E2E testing.

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
No findings — document reads as one coherent test strategy.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | qa |
| Standard | documentation-standards |
| Rubric File | `audit/semantic/document/12-qa.md` |
| Auditor | LLM ({{ model_name }}) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
