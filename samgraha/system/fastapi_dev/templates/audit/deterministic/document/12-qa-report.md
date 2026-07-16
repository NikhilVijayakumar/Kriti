# Deterministic Whole-Document Report — QA

**Document:** {{ document_path }}
**Standard:** `documentation-standards/12-qa-standards.md`
**Rule File:** `audit/deterministic/document/12-qa.yaml`
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
      = 100 × {{ passed_weight }} / 5.0
```

Total possible weight across all 6 document-level rules is fixed at **5.0** (qa-doc-001 1.5, 002 1.0, 003 0.5, 004 1.0, 005 0.5, 006 0.5 — see `audit/deterministic/document/12-qa.yaml`). Mandatory rules (001, 002, 004 — combined weight 3.5 of 5.0) carry most of the score; a single mandatory failure is a heavier hit than any one recommended failure, by design.

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
| Collection Completeness | {{ categories.collection_completeness.score }} / 100 | {{ categories.collection_completeness.previous_score | default('—') }} | {{ categories.collection_completeness.trend_display }} | qa-doc-001, 002 |
| Modularity | {{ categories.modularity.score }} / 100 | {{ categories.modularity.previous_score | default('—') }} | {{ categories.modularity.trend_display }} | qa-doc-003 |
| Coverage Completeness | {{ categories.coverage_completeness.score }} / 100 | {{ categories.coverage_completeness.previous_score | default('—') }} | {{ categories.coverage_completeness.trend_display }} | qa-doc-004 |
| Cross-References | {{ categories.cross_references.score }} / 100 | {{ categories.cross_references.previous_score | default('—') }} | {{ categories.cross_references.trend_display }} | qa-doc-005 |
| Duplicate Content | {{ categories.duplicate_content.score }} / 100 | {{ categories.duplicate_content.previous_score | default('—') }} | {{ categories.duplicate_content.trend_display }} | qa-doc-006 |

---

## 1. Collection Completeness — weight 2.5 of 5.0

**Why this matters:** QA Documentation is meant to be read as one coherent test plan. A document missing a required section, or one with a required section that's present but empty, gives downstream consumers nothing to derive against for that concern — the gap propagates downstream instead of being caught here.

**Category Score: {{ categories.collection_completeness.score }} / 100** ({{ categories.collection_completeness.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| qa-doc-001 | Required sections present (Test Strategy, Unit Testing, Integration Testing, Security Testing) | error (mandatory) | 1.5 | {{ results['qa-doc-001'].previous_status \| default('—') }} | {{ results['qa-doc-001'].status }} | {{ results['qa-doc-001'].trend_display }} | {{ results['qa-doc-001'].evidence \| default('—') }} |
| qa-doc-002 | No empty required sections — a heading alone doesn't satisfy the requirement | error (mandatory) | 1.0 | {{ results['qa-doc-002'].previous_status \| default('—') }} | {{ results['qa-doc-002'].status }} | {{ results['qa-doc-002'].trend_display }} | {{ results['qa-doc-002'].evidence \| default('—') }} |

## 2. Modularity — weight 0.5 of 5.0

**Why this matters:** QA Documentation is meant to be a focused document — one testing strategy per file. A document that mixes unrelated testing concerns is harder to keep consistent as either evolves, and harder for a reader to know which document is authoritative for what.

**Category Score: {{ categories.modularity.score }} / 100** ({{ categories.modularity.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| qa-doc-003 | Document has a single primary focus — does not mix unrelated testing concerns | warning (recommended) | 0.5 | {{ results['qa-doc-003'].previous_status \| default('—') }} | {{ results['qa-doc-003'].status }} | {{ results['qa-doc-003'].trend_display }} | {{ results['qa-doc-003'].evidence \| default('—') }} |

## 3. Coverage Completeness — weight 1.0 of 5.0

**Why this matters:** A QA plan that only covers some testing levels — unit but not integration, or integration but not security — leaves blind spots that downstream Engineering and Security can't compensate for, because they don't know the gap exists.

**Category Score: {{ categories.coverage_completeness.score }} / 100** ({{ categories.coverage_completeness.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| qa-doc-004 | Test strategy covers all testing levels — unit, integration, and security testing addressed | error (mandatory) | 1.0 | {{ results['qa-doc-004'].previous_status \| default('—') }} | {{ results['qa-doc-004'].status }} | {{ results['qa-doc-004'].trend_display }} | {{ results['qa-doc-004'].evidence \| default('—') }} |

## 4. Cross-References — weight 0.5 of 5.0

**Why this matters:** QA Documentation without upstream references is an orphan — it tests against no defined standard. A QA document that doesn't reference Architecture, Engineering, and Security as upstream sources means the test plan isn't grounded in the systems it's meant to validate.

**Category Score: {{ categories.cross_references.score }} / 100** ({{ categories.cross_references.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| qa-doc-005 | References upstream (Architecture — derives_from, Engineering — derives_from, Security — derives_from) | warning (recommended) | 0.5 | {{ results['qa-doc-005'].previous_status \| default('—') }} | {{ results['qa-doc-005'].status }} | {{ results['qa-doc-005'].trend_display }} | {{ results['qa-doc-005'].evidence \| default('—') }} |

## 5. Duplicate Content — weight 0.5 of 5.0

**Why this matters:** Every QA concept should be defined exactly once. Duplication is how two sections quietly drift apart over time — one gets updated, the copy doesn't, and now the document contradicts itself.

**Category Score: {{ categories.duplicate_content.score }} / 100** ({{ categories.duplicate_content.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| qa-doc-006 | No section repeats information already stated in another section | warning (recommended) | 0.5 | {{ results['qa-doc-006'].previous_status \| default('—') }} | {{ results['qa-doc-006'].status }} | {{ results['qa-doc-006'].trend_display }} | {{ results['qa-doc-006'].evidence \| default('—') }} |

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
| Domain | qa |
| Standard | documentation-standards |
| Rule File | `audit/deterministic/document/12-qa.yaml` |
| Auditor | System (deterministic engine) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
