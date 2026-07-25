# Semantic Whole-Document Report — Vision

**Document:** {{ document_path }}
**Standard:** `documentation-standards/02-vision-standards.md`
**Rubric:** `audit/semantic/document/01-vision.md`
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
| C1 — Problem-Solution-VS alignment | mandatory | 35 | {{ results['C1'].previous_passed_display | default('—') }} | {{ results['C1'].passed_display }} | {{ results['C1'].trend_display }} |
| C2 — Technology independence | mandatory | 35 | {{ results['C2'].previous_passed_display | default('—') }} | {{ results['C2'].passed_display }} | {{ results['C2'].trend_display }} |
| C3 — Terminology consistency | recommended | 30 | {{ results['C3'].previous_passed_display | default('—') }} | {{ results['C3'].passed_display }} | {{ results['C3'].trend_display }} |

C1 and C2 are mandatory — either one failing caps this score at 30 (only C3's points remain reachable). C3 alone failing still allows 70.

---

## Judgment

Verifies Vision Documentation coheres as one aspirational statement — Problem, Solution, and Vision Statement must describe the same aspiration without contradicting each other, and the collection as a whole must read as one vision, not several. Section-level quality (is each section well-written on its own) is a separate concern, owned by the Semantic Section report; this report only catches problems that only exist when sections or documents are read together.

## Scoring Criteria — Detail

### C1 — mandatory, 0 or 35: Problem, Solution, and Vision Statement align without contradiction

**What this catches:** a Solution that addresses a different problem than the one Problem describes; a Vision Statement that's an unrelated ambition disconnected from the actual problem-solution pair.

**Previous:** {{ results['C1'].previous_passed_display | default('—') }} → **Current:** {{ results['C1'].passed_display }} ({{ results['C1'].trend_display }})
**Evidence:** {{ results['C1'].evidence.excerpt | default('—') }}
{% if not results['C1'].passed %}**Finding:** {{ results['C1'].message }}{% endif %}

### C2 — mandatory, 0 or 35: No technology/implementation references anywhere in the document

**What this catches:** a technology reference split across two sentences in different sections is still a violation. Vision must remain technology-independent as a whole, not just section by section.

**Previous:** {{ results['C2'].previous_passed_display | default('—') }} → **Current:** {{ results['C2'].passed_display }} ({{ results['C2'].trend_display }})
**Evidence:** {{ results['C2'].evidence.excerpt | default('—') }}
{% if not results['C2'].passed %}**Finding:** {{ results['C2'].message }}{% endif %}

### C3 — recommended, 0 or 30: Terminology consistent and all Vision documents cohere as one system

**What this catches:** when the same value or goal is named differently across sections, readers cannot tell whether the difference is intentional or accidental.

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
No findings — document reads as one coherent vision.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | vision |
| Standard | documentation-standards |
| Rubric File | `audit/semantic/document/01-vision.md` |
| Auditor | LLM ({{ model_name }}) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
