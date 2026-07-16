# Semantic Section Report — Philosophy

**Document:** {{ document_path }}
**Standard:** `documentation-standards/02-philosophy-standards.md`
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
| 1 | Guiding Principles | **required** | {{ sections.guiding_principles.score }} / 100 | {{ sections.guiding_principles.previous_score | default('—') }} | {{ sections.guiding_principles.trend_display }} |
| 2 | Values | **required** | {{ sections.values.score }} / 100 | {{ sections.values.previous_score | default('—') }} | {{ sections.values.trend_display }} |
| 3 | Trade-offs | **required** | {{ sections.tradeoffs.score }} / 100 | {{ sections.tradeoffs.previous_score | default('—') }} | {{ sections.tradeoffs.trend_display }} |
| 4 | Purpose | optional | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |

A section absent from the document (among the optional ones) isn't scored at all here — it's a deterministic presence check, not a semantic quality judgment on nothing.

---

## 1. Guiding Principles — `section/02-philosophy/01-guiding_principles.md`

**Why this matters:** Guiding principles are the durable design tenets that shape how the product is built. They must be actionable, prioritizable, and falsifiable — not platitudes. Principles resolve ambiguity when user needs or technical constraints conflict.

**Section Score: {{ sections.guiding_principles.score }} / 100** ({{ sections.guiding_principles.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['guiding_principles.C1'].previous_passed_display \| default('—') }} | {{ results['guiding_principles.C1'].passed_display }} | {{ results['guiding_principles.C1'].trend_display }} | {{ results['guiding_principles.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['guiding_principles.C2'].previous_passed_display \| default('—') }} | {{ results['guiding_principles.C2'].passed_display }} | {{ results['guiding_principles.C2'].trend_display }} | {{ results['guiding_principles.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 20 | {{ results['guiding_principles.C3'].previous_passed_display \| default('—') }} | {{ results['guiding_principles.C3'].passed_display }} | {{ results['guiding_principles.C3'].trend_display }} | {{ results['guiding_principles.C3'].evidence.excerpt \| default('—') }} |
| C4 | recommended | 20 | {{ results['guiding_principles.C4'].previous_passed_display \| default('—') }} | {{ results['guiding_principles.C4'].passed_display }} | {{ results['guiding_principles.C4'].trend_display }} | {{ results['guiding_principles.C4'].evidence.excerpt \| default('—') }} |

C1: guiding principles are documented with rationale. C2: each principle is actionable and falsifiable. C3: conflict resolution rule documented for when two principles oppose. C4: principles are consistently referenced in decision records.

## 2. Values — `02-values.md`

**Why this matters:** Values define what the product team prioritizes when trade-offs arise — simplicity over features, reliability over speed, accessibility over novelty. Values must be ranked or weighted so they produce consistent decisions across the team.

**Section Score: {{ sections.values.score }} / 100** ({{ sections.values.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['values.C1'].previous_passed_display \| default('—') }} | {{ results['values.C1'].passed_display }} | {{ results['values.C1'].trend_display }} | {{ results['values.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['values.C2'].previous_passed_display \| default('—') }} | {{ results['values.C2'].passed_display }} | {{ results['values.C2'].trend_display }} | {{ results['values.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['values.C3'].previous_passed_display \| default('—') }} | {{ results['values.C3'].passed_display }} | {{ results['values.C3'].trend_display }} | {{ results['values.C3'].evidence.excerpt \| default('—') }} |

C1: values are documented and ranked by priority. C2: each value has a concrete definition and example. C3: values demonstrably influence product decisions.

## 3. Trade-offs — `03-tradeoffs.md`

**Why this matters:** Trade-offs document conscious decisions where one quality was sacrificed for another. They must capture the alternatives considered, the rationale for the choice, and the expected cost. Trade-off records prevent re-litigation and surface accumulated debt.

**Section Score: {{ sections.tradeoffs.score }} / 100** ({{ sections.tradeoffs.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 35 | {{ results['tradeoffs.C1'].previous_passed_display \| default('—') }} | {{ results['tradeoffs.C1'].passed_display }} | {{ results['tradeoffs.C1'].trend_display }} | {{ results['tradeoffs.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 35 | {{ results['tradeoffs.C2'].previous_passed_display \| default('—') }} | {{ results['tradeoffs.C2'].passed_display }} | {{ results['tradeoffs.C2'].trend_display }} | {{ results['tradeoffs.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['tradeoffs.C3'].previous_passed_display \| default('—') }} | {{ results['tradeoffs.C3'].passed_display }} | {{ results['tradeoffs.C3'].trend_display }} | {{ results['tradeoffs.C3'].evidence.excerpt \| default('—') }} |

C1: trade-offs are documented with alternatives and rationale. C2: each trade-off includes explicit cost or downside. C3: trade-offs are linked to decisions and reviewed periodically.

## 4. Purpose — `04-purpose.md`

**Why this matters:** Purpose articulates the core reason the product exists — grounded in user need, durable across strategy shifts, and distinct from implementation goals. Every feature decision should trace back to purpose.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['purpose.C1'].previous_passed_display \| default('—') }} | {{ results['purpose.C1'].passed_display }} | {{ results['purpose.C1'].trend_display }} | {{ results['purpose.C1'].evidence.excerpt \| default('—') }} |
| C2 | mandatory | 30 | {{ results['purpose.C2'].previous_passed_display \| default('—') }} | {{ results['purpose.C2'].passed_display }} | {{ results['purpose.C2'].trend_display }} | {{ results['purpose.C2'].evidence.excerpt \| default('—') }} |
| C3 | recommended | 30 | {{ results['purpose.C3'].previous_passed_display \| default('—') }} | {{ results['purpose.C3'].passed_display }} | {{ results['purpose.C3'].trend_display }} | {{ results['purpose.C3'].evidence.excerpt \| default('—') }} |

C1: purpose is documented in a single coherent statement. C2: purpose is distinct from business goals and implementation. C3: purpose is referenced in feature or roadmap decisions.

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
| Domain | philosophy |
| Standard | documentation-standards |
| Section Rubric Files | `audit/semantic/section/02-philosophy/*.md` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
