# Deterministic Whole-Document Report — Prototype

**Document:** {{ document_path }}
**Standard:** `documentation-standards/11-prototype-standards.md`
**Rule File:** `audit/deterministic/document/11-prototype.yaml`
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

Total possible weight across all 6 document-level rules is fixed at **4.5** (proto-doc-001 1.5, 002 1.0, 003 0.5, 004 0.5, 005 0.5, 006 0.5 — see `audit/deterministic/document/11-prototype.yaml`). Mandatory rules (001, 002 — combined weight 2.5 of 4.5) carry most of the score; a single mandatory failure is a heavier hit than any one recommended failure, by design.

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
| Collection Completeness | {{ categories.collection_completeness.score }} / 100 | {{ categories.collection_completeness.previous_score | default('—') }} | {{ categories.collection_completeness.trend_display }} | proto-doc-001, 002 |
| Modularity | {{ categories.modularity.score }} / 100 | {{ categories.modularity.previous_score | default('—') }} | {{ categories.modularity.trend_display }} | proto-doc-003 |
| Mock Fidelity | {{ categories.mock_fidelity.score }} / 100 | {{ categories.mock_fidelity.previous_score | default('—') }} | {{ categories.mock_fidelity.trend_display }} | proto-doc-004 |
| Cross-References | {{ categories.cross_references.score }} / 100 | {{ categories.cross_references.previous_score | default('—') }} | {{ categories.cross_references.trend_display }} | proto-doc-005 |
| Duplicate Content | {{ categories.duplicate_content.score }} / 100 | {{ categories.duplicate_content.previous_score | default('—') }} | {{ categories.duplicate_content.trend_display }} | proto-doc-006 |

---

## 1. Collection Completeness — weight 2.5 of 4.5

**Why this matters:** Prototype Documentation is meant to be read as one falsifiable experiment — scope defines boundaries, mock APIs simulate behavior, data model defines entities. A document missing a required section, or one with a required section that's present but empty, gives evaluators nothing to judge for that concern — the gap propagates into the prototype evaluation instead of being caught here.

**Category Score: {{ categories.collection_completeness.score }} / 100** ({{ categories.collection_completeness.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| proto-doc-001 | Required sections present (Scope, Mock APIs, Data Model) | error (mandatory) | 1.5 | {{ results['proto-doc-001'].previous_status \| default('—') }} | {{ results['proto-doc-001'].status }} | {{ results['proto-doc-001'].trend_display }} | {{ results['proto-doc-001'].evidence \| default('—') }} |
| proto-doc-002 | No empty required sections — a heading alone doesn't satisfy the requirement | error (mandatory) | 1.0 | {{ results['proto-doc-002'].previous_status \| default('—') }} | {{ results['proto-doc-002'].status }} | {{ results['proto-doc-002'].trend_display }} | {{ results['proto-doc-002'].evidence \| default('—') }} |

## 2. Modularity — weight 0.5 of 4.5

**Why this matters:** A prototype document is meant to be a focused experiment — one feature prototype per document. A document that mixes unrelated feature prototypes (e.g., authentication flow and data export in the same file) is harder to keep consistent as either prototype evolves, and harder for a reader to know which document is authoritative for what.

**Category Score: {{ categories.modularity.score }} / 100** ({{ categories.modularity.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| proto-doc-003 | Document covers one feature prototype — does not mix unrelated concerns | warning (recommended) | 0.5 | {{ results['proto-doc-003'].previous_status \| default('—') }} | {{ results['proto-doc-003'].status }} | {{ results['proto-doc-003'].trend_display }} | {{ results['proto-doc-003'].evidence \| default('—') }} |

## 3. Mock Fidelity — weight 0.5 of 4.5

**Why this matters:** Mock APIs are the prototype's simulation surface — they must reference the same entities defined in the Data Model. A mock referencing types absent from the data model produces false confidence: the prototype appears to exercise a real interface, but the underlying entities don't exist in the documented model.

**Category Score: {{ categories.mock_fidelity.score }} / 100** ({{ categories.mock_fidelity.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| proto-doc-004 | Mock APIs reference types or schemas defined in the Data Model section | warning (recommended) | 0.5 | {{ results['proto-doc-004'].previous_status \| default('—') }} | {{ results['proto-doc-004'].status }} | {{ results['proto-doc-004'].trend_display }} | {{ results['proto-doc-004'].evidence \| default('—') }} |

## 4. Cross-References — weight 0.5 of 4.5

**Why this matters:** Prototype Documentation derives from upstream Feature Design and Feature Technical standards — it simulates what those standards specify. A document with no trace to those upstream sources reads as if it were written in isolation from the features it prototypes, which makes it harder to justify why the prototype looks the way it does when questioned later.

**Category Score: {{ categories.cross_references.score }} / 100** ({{ categories.cross_references.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| proto-doc-005 | References upstream Feature Design and Feature Technical standards where applicable | warning (recommended) | 0.5 | {{ results['proto-doc-005'].previous_status \| default('—') }} | {{ results['proto-doc-005'].status }} | {{ results['proto-doc-005'].trend_display }} | {{ results['proto-doc-005'].evidence \| default('—') }} |

## 5. Duplicate Content — weight 0.5 of 4.5

**Why this matters:** Every prototype concept should be defined exactly once. Duplication is how two sections quietly drift apart over time — one gets updated, the copy doesn't, and now the document contradicts itself.

**Category Score: {{ categories.duplicate_content.score }} / 100** ({{ categories.duplicate_content.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| proto-doc-006 | No section repeats information already stated in another section | warning (recommended) | 0.5 | {{ results['proto-doc-006'].previous_status \| default('—') }} | {{ results['proto-doc-006'].status }} | {{ results['proto-doc-006'].trend_display }} | {{ results['proto-doc-006'].evidence \| default('—') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Rule | Category | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.id }} | {{ r.category }} | {{ r.message }} | {{ r.evidence | default('—') }} | {{ 'Yes — regression' if r.is_new_failure else 'No — carried over' }} |
{% endfor %}
{% else %}
No failures — all 6 document-level rules pass.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | prototype |
| Standard | documentation-standards |
| Rule File | `audit/deterministic/document/11-prototype.yaml` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
