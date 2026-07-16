# Deterministic Whole-Document Report — Product Guide

**Document:** {{ document_path }}
**Standard:** `documentation-standards/16-product-guide-standards.md`
**Rule File:** `audit/deterministic/document/16-product-guide.yaml`
**Auditor:** System (deterministic engine)
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Deterministic Whole Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
score = 100 × (Σ weight of passed rules) / (Σ weight of all rules)
# calculation: deterministic_document_v1
      = 100 × {{ passed_weight }} / 4.5
```

Total possible weight across all 5 document-level rules is fixed at **4.5** (pg-doc-001 1.5, 002 1.0, 003 0.5, 004 1.0, 005 0.5 — see `audit/deterministic/document/16-product-guide.yaml`). Mandatory rules (001, 002, 004 — combined weight 3.5 of 4.5) carry most of the score; a single mandatory failure is a heavier hit than any one recommended failure, by design.

### Score History

| Revision | Date | Score | vs. Previous | vs. Baseline |
|---:|---|---:|---|---|
{% for r in revision_history -%}
| {{ r.revision }} | {{ r.date }} | {{ r.score }} / 100 | {{ r.delta_previous_display }} | {{ r.delta_baseline_display }} |
{% endfor -%}
| {{ revision_number }} (current) | {{ created_at }} | {{ score }} / 100 | {{ delta_previous_display }} | {{ delta_baseline_display }} |

{% if not previous_score %}No prior runs — this revision is the baseline every future run is compared against.{% endif %}

### Category Scores

| Category | Score | Previous | Trend | Rules |
|---|---:|---:|---|---|
| Collection Completeness | {{ categories.collection_completeness.score }} / 100 | {{ categories.collection_completeness.previous_score | default('—') }} | {{ categories.collection_completeness.trend_display }} | pg-doc-001, 002 |
| Modularity | {{ categories.modularity.score }} / 100 | {{ categories.modularity.previous_score | default('—') }} | {{ categories.modularity.trend_display }} | pg-doc-003 |
| Content Richness | {{ categories.content_richness.score }} / 100 | {{ categories.content_richness.previous_score | default('—') }} | {{ categories.content_richness.trend_display }} | pg-doc-004 |
| Duplicate Content | {{ categories.duplicate_content.score }} / 100 | {{ categories.duplicate_content.previous_score | default('—') }} | {{ categories.duplicate_content.trend_display }} | pg-doc-005 |

---

## 1. Collection Completeness — weight 2.5 of 4.5

**Why this matters:** Product Guide is meant to be read as one coherent how-to document. A document missing a required section, or one with a required section that's present but empty, gives readers nothing actionable for that concern — the gap propagates downstream instead of being caught here.

**Category Score: {{ categories.collection_completeness.score }} / 100** ({{ categories.collection_completeness.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| pg-doc-001 | Required sections present (title, body) | error (mandatory) | 1.5 | {{ results['pg-doc-001'].previous_status \| default('—') }} | {{ results['pg-doc-001'].status }} | {{ results['pg-doc-001'].trend_display }} | {{ results['pg-doc-001'].evidence \| default('—') }} |
| pg-doc-002 | No empty required sections — a heading alone doesn't satisfy the requirement | error (mandatory) | 1.0 | {{ results['pg-doc-002'].previous_status \| default('—') }} | {{ results['pg-doc-002'].status }} | {{ results['pg-doc-002'].trend_display }} | {{ results['pg-doc-002'].evidence \| default('—') }} |

## 2. Modularity — weight 0.5 of 4.5

**Why this matters:** Product Guide is meant to be a focused document — one product topic per file. A document that mixes unrelated product guides is harder to keep consistent as either topic evolves, and harder for a reader to know which document is authoritative for what.

**Category Score: {{ categories.modularity.score }} / 100** ({{ categories.modularity.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| pg-doc-003 | Document has a single primary focus — does not mix unrelated product guides | warning (recommended) | 0.5 | {{ results['pg-doc-003'].previous_status \| default('—') }} | {{ results['pg-doc-003'].status }} | {{ results['pg-doc-003'].trend_display }} | {{ results['pg-doc-003'].evidence \| default('—') }} |

## 3. Content Richness — weight 1.0 of 4.5

**Why this matters:** A Product Guide body that's just links or references without substantive explanation gives readers no actual guidance. The body must contain actionable content — steps, instructions, or explanations — to fulfill the guide's purpose.

**Category Score: {{ categories.content_richness.score }} / 100** ({{ categories.content_richness.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| pg-doc-004 | Body section contains substantive content (minimum 50 words, not just links or references) | error (mandatory) | 1.0 | {{ results['pg-doc-004'].previous_status \| default('—') }} | {{ results['pg-doc-004'].status }} | {{ results['pg-doc-004'].trend_display }} | {{ results['pg-doc-004'].evidence \| default('—') }} |

## 4. Duplicate Content — weight 0.5 of 4.5

**Why this matters:** Every Product Guide concept should be defined exactly once. Duplication is how two sections quietly drift apart over time — one gets updated, the copy doesn't, and now the document contradicts itself.

**Category Score: {{ categories.duplicate_content.score }} / 100** ({{ categories.duplicate_content.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| pg-doc-005 | No section repeats information already stated in another section | warning (recommended) | 0.5 | {{ results['pg-doc-005'].previous_status \| default('—') }} | {{ results['pg-doc-005'].status }} | {{ results['pg-doc-005'].trend_display }} | {{ results['pg-doc-005'].evidence \| default('—') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Rule | Category | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.id }} | {{ r.category }} | {{ r.message }} | {{ r.evidence | default('—') }} | {{ 'Yes — regression' if r.is_new_failure else 'No — carried over' }} |
{% endfor %}
{% else %}
No failures — all 5 document-level rules pass.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | product-guide |
| Standard | documentation-standards |
| Rule File | `audit/deterministic/document/16-product-guide.yaml` |
| Auditor | System (deterministic engine) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
