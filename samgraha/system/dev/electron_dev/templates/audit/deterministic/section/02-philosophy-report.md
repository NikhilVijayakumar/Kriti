# Deterministic Section Report — Philosophy

**Document:** {{ document_path }}
**Standard:** `documentation-standards/02-philosophy-standards.md`
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Deterministic Section Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
overall = average of the 4 section scores below
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
| 1 | Guiding Principles | **required** | 5.5 | {{ sections.guiding_principles.score }} / 100 | {{ sections.guiding_principles.previous_score | default('—') }} | {{ sections.guiding_principles.trend_display }} |
| 2 | Values | **required** | 5.5 | {{ sections.values.score }} / 100 | {{ sections.values.previous_score | default('—') }} | {{ sections.values.trend_display }} |
| 3 | Trade-offs | **required** | 5.5 | {{ sections.tradeoffs.score }} / 100 | {{ sections.tradeoffs.previous_score | default('—') }} | {{ sections.tradeoffs.trend_display }} |
| 4 | Purpose | optional | 4.0 | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |

The 3 required sections carry 16.5 of the document's 20.5 total rule weight — a document can only pass if those three are both present and internally sound; Purpose is recommended-quality signal, not gating.

---

## 1. Guiding Principles — `section/02-philosophy/01-guiding_principles.yaml` — weight 5.5 — **required**

**Why this matters:** Guiding principles are the durable design tenets that shape how the product is built. They must be actionable, prioritizable, and falsifiable — not platitudes. Principles resolve ambiguity when user needs or technical constraints conflict. Without them, every downstream design decision is made on ad-hoc judgment with no shared foundation.

**Section Score: {{ sections.guiding_principles.score }} / 100** ({{ sections.guiding_principles.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| phil-sec-gp-001 | Guiding principles section exists | error (mandatory) | 1.5 | {{ results['phil-sec-gp-001'].previous_status \| default('—') }} | {{ results['phil-sec-gp-001'].status }} | {{ results['phil-sec-gp-001'].trend_display }} | {{ results['phil-sec-gp-001'].evidence \| default('—') }} |
| phil-sec-gp-002 | Principles stated as clear discrete directives | error (mandatory) | 1.0 | {{ results['phil-sec-gp-002'].previous_status \| default('—') }} | {{ results['phil-sec-gp-002'].status }} | {{ results['phil-sec-gp-002'].trend_display }} | {{ results['phil-sec-gp-002'].evidence \| default('—') }} |
| phil-sec-gp-003 | No implementation technology references | error (mandatory) | 1.0 | {{ results['phil-sec-gp-003'].previous_status \| default('—') }} | {{ results['phil-sec-gp-003'].status }} | {{ results['phil-sec-gp-003'].trend_display }} | {{ results['phil-sec-gp-003'].evidence \| default('—') }} |
| phil-sec-gp-004 | Principles are prescriptive, not descriptive | error (mandatory) | 1.0 | {{ results['phil-sec-gp-004'].previous_status \| default('—') }} | {{ results['phil-sec-gp-004'].status }} | {{ results['phil-sec-gp-004'].trend_display }} | {{ results['phil-sec-gp-004'].evidence \| default('—') }} |
| phil-sec-gp-005 | At least three principles defined | warning (recommended) | 0.5 | {{ results['phil-sec-gp-005'].previous_status \| default('—') }} | {{ results['phil-sec-gp-005'].status }} | {{ results['phil-sec-gp-005'].trend_display }} | {{ results['phil-sec-gp-005'].evidence \| default('—') }} |
| phil-sec-gp-006 | Principles are technology-independent | warning (recommended) | 0.5 | {{ results['phil-sec-gp-006'].previous_status \| default('—') }} | {{ results['phil-sec-gp-006'].status }} | {{ results['phil-sec-gp-006'].trend_display }} | {{ results['phil-sec-gp-006'].evidence \| default('—') }} |

## 2. Values — `02-values.yaml` — weight 5.5 — **required**

**Why this matters:** Values define what the product team prioritizes when trade-offs arise — simplicity over features, reliability over speed, accessibility over novelty. Without ranked values, every conflict is resolved by whoever argues loudest, not by shared priorities.

**Section Score: {{ sections.values.score }} / 100** ({{ sections.values.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| phil-sec-val-001 | Values section exists | error (mandatory) | 1.5 | {{ results['phil-sec-val-001'].previous_status \| default('—') }} | {{ results['phil-sec-val-001'].status }} | {{ results['phil-sec-val-001'].trend_display }} | {{ results['phil-sec-val-001'].evidence \| default('—') }} |
| phil-sec-val-002 | Core values defined as discrete named entities | error (mandatory) | 1.0 | {{ results['phil-sec-val-002'].previous_status \| default('—') }} | {{ results['phil-sec-val-002'].status }} | {{ results['phil-sec-val-002'].trend_display }} | {{ results['phil-sec-val-002'].evidence \| default('—') }} |
| phil-sec-val-003 | Values are specific, not vague platitudes | error (mandatory) | 1.0 | {{ results['phil-sec-val-003'].previous_status \| default('—') }} | {{ results['phil-sec-val-003'].status }} | {{ results['phil-sec-val-003'].trend_display }} | {{ results['phil-sec-val-003'].evidence \| default('—') }} |
| phil-sec-val-004 | No implementation technology references | error (mandatory) | 1.0 | {{ results['phil-sec-val-004'].previous_status \| default('—') }} | {{ results['phil-sec-val-004'].status }} | {{ results['phil-sec-val-004'].trend_display }} | {{ results['phil-sec-val-004'].evidence \| default('—') }} |
| phil-sec-val-005 | Values are ordered or include conflict resolution guidance | warning (recommended) | 0.5 | {{ results['phil-sec-val-005'].previous_status \| default('—') }} | {{ results['phil-sec-val-005'].status }} | {{ results['phil-sec-val-005'].trend_display }} | {{ results['phil-sec-val-005'].evidence \| default('—') }} |
| phil-sec-val-006 | At least two values defined | warning (recommended) | 0.5 | {{ results['phil-sec-val-006'].previous_status \| default('—') }} | {{ results['phil-sec-val-006'].status }} | {{ results['phil-sec-val-006'].trend_display }} | {{ results['phil-sec-val-006'].evidence \| default('—') }} |

## 3. Trade-offs — `03-tradeoffs.yaml` — weight 5.5 — **required**

**Why this matters:** Trade-offs document conscious decisions where one quality was sacrificed for another. Without them, every design decision looks equally negotiable, including the ones that aren't — and the same trade-offs get re-litigated repeatedly instead of being resolved once.

**Section Score: {{ sections.tradeoffs.score }} / 100** ({{ sections.tradeoffs.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| phil-sec-to-001 | Trade-offs section exists | error (mandatory) | 1.5 | {{ results['phil-sec-to-001'].previous_status \| default('—') }} | {{ results['phil-sec-to-001'].status }} | {{ results['phil-sec-to-001'].trend_display }} | {{ results['phil-sec-to-001'].evidence \| default('—') }} |
| phil-sec-to-002 | Trade-offs documented with reasoning | error (mandatory) | 1.0 | {{ results['phil-sec-to-002'].previous_status \| default('—') }} | {{ results['phil-sec-to-002'].status }} | {{ results['phil-sec-to-002'].trend_display }} | {{ results['phil-sec-to-002'].evidence \| default('—') }} |
| phil-sec-to-003 | Competing concerns identified per trade-off | error (mandatory) | 1.0 | {{ results['phil-sec-to-003'].previous_status \| default('—') }} | {{ results['phil-sec-to-003'].status }} | {{ results['phil-sec-to-003'].trend_display }} | {{ results['phil-sec-to-003'].evidence \| default('—') }} |
| phil-sec-to-004 | No implementation technology references | error (mandatory) | 1.0 | {{ results['phil-sec-to-004'].previous_status \| default('—') }} | {{ results['phil-sec-to-004'].status }} | {{ results['phil-sec-to-004'].trend_display }} | {{ results['phil-sec-to-004'].evidence \| default('—') }} |
| phil-sec-to-005 | Trade-offs are not one-sided — acknowledges what is lost | warning (recommended) | 0.5 | {{ results['phil-sec-to-005'].previous_status \| default('—') }} | {{ results['phil-sec-to-005'].status }} | {{ results['phil-sec-to-005'].trend_display }} | {{ results['phil-sec-to-005'].evidence \| default('—') }} |
| phil-sec-to-006 | At least one trade-off documented | warning (recommended) | 0.5 | {{ results['phil-sec-to-006'].previous_status \| default('—') }} | {{ results['phil-sec-to-006'].status }} | {{ results['phil-sec-to-006'].trend_display }} | {{ results['phil-sec-to-006'].evidence \| default('—') }} |

## 4. Purpose — `04-purpose.yaml` — weight 4.0 — optional

**Why this matters:** Purpose is what tells a reader why Philosophy Documentation exists at all before they read a single principle. A Purpose section that's missing, vague, or technology-leaking undermines every section that follows it.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| phil-sec-purpose-001 | Purpose section exists | error (mandatory) | 1.5 | {{ results['phil-sec-purpose-001'].previous_status \| default('—') }} | {{ results['phil-sec-purpose-001'].status }} | {{ results['phil-sec-purpose-001'].trend_display }} | {{ results['phil-sec-purpose-001'].evidence \| default('—') }} |
| phil-sec-purpose-002 | States philosophical intent | error (mandatory) | 1.0 | {{ results['phil-sec-purpose-002'].previous_status \| default('—') }} | {{ results['phil-sec-purpose-002'].status }} | {{ results['phil-sec-purpose-002'].trend_display }} | {{ results['phil-sec-purpose-002'].evidence \| default('—') }} |
| phil-sec-purpose-003 | Technology-independent | error (mandatory) | 1.0 | {{ results['phil-sec-purpose-003'].previous_status \| default('—') }} | {{ results['phil-sec-purpose-003'].status }} | {{ results['phil-sec-purpose-003'].trend_display }} | {{ results['phil-sec-purpose-003'].evidence \| default('—') }} |
| phil-sec-purpose-004 | Scope boundaries defined | warning (recommended) | 0.5 | {{ results['phil-sec-purpose-004'].previous_status \| default('—') }} | {{ results['phil-sec-purpose-004'].status }} | {{ results['phil-sec-purpose-004'].trend_display }} | {{ results['phil-sec-purpose-004'].evidence \| default('—') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Section | Rule | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.section_type }} | {{ r.id }} | {{ r.message }} | {{ r.evidence | default('—') }} | {{ 'Yes — regression' if r.is_new_failure else 'No — carried over' }} |
{% endfor %}
{% else %}
No failures across all 4 sections.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | philosophy |
| Standard | documentation-standards |
| Section Rule Files | `audit/deterministic/section/02-philosophy/*.yaml` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
