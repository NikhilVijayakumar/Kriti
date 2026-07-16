# Deterministic Whole-Document Report — Feature

**Document:** {{ document_path }}
**Standard:** `documentation-standards/04-feature-standards.md`
**Rule File:** `audit/deterministic/document/04-feature.yaml`
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

Total possible weight across all 6 document-level rules is fixed at **5.0** (feat-doc-001 1.5, 002 1.0, 003 0.5, 004 1.0, 005 0.5, 006 0.5 — see `audit/deterministic/document/04-feature.yaml`). Mandatory rules (001, 002, 004 — combined weight 3.5 of 5.0) carry most of the score.

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
| Collection Completeness | {{ categories.collection_completeness.score }} / 100 | {{ categories.collection_completeness.previous_score | default('—') }} | {{ categories.collection_completeness.trend_display }} | feat-doc-001, 002 |
| Modularity | {{ categories.modularity.score }} / 100 | {{ categories.modularity.previous_score | default('—') }} | {{ categories.modularity.trend_display }} | feat-doc-003 |
| Technology Independence | {{ categories.technology_independence.score }} / 100 | {{ categories.technology_independence.previous_score | default('—') }} | {{ categories.technology_independence.trend_display }} | feat-doc-004 |
| Cross-References | {{ categories.cross_references.score }} / 100 | {{ categories.cross_references.previous_score | default('—') }} | {{ categories.cross_references.trend_display }} | feat-doc-005 |
| Duplicate Content | {{ categories.duplicate_content.score }} / 100 | {{ categories.duplicate_content.previous_score | default('—') }} | {{ categories.duplicate_content.trend_display }} | feat-doc-006 |

---

## 1. Collection Completeness — weight 2.5 of 5.0

**Why this matters:** Feature Documentation defines what the system must do. A document missing a required section, or one with a required section that's present but empty, gives Feature Design and Feature Technical nothing to derive against for that concern.

**Category Score: {{ categories.collection_completeness.score }} / 100** ({{ categories.collection_completeness.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| feat-doc-001 | Required sections present (Purpose, Functional Requirements, Acceptance Criteria) | error (mandatory) | 1.5 | {{ results['feat-doc-001'].previous_status | default('—') }} | {{ results['feat-doc-001'].status }} | {{ results['feat-doc-001'].trend_display }} | {{ results['feat-doc-001'].evidence | default('—') }} |
| feat-doc-002 | No empty required sections | error (mandatory) | 1.0 | {{ results['feat-doc-002'].previous_status | default('—') }} | {{ results['feat-doc-002'].status }} | {{ results['feat-doc-002'].trend_display }} | {{ results['feat-doc-002'].evidence | default('—') }} |

## 2. Modularity — weight 0.5 of 5.0

**Why this matters:** Feature is meant to be a focused document — one feature per file. A document that mixes unrelated features is harder to keep consistent and harder for a reader to know which document is authoritative for what.

**Category Score: {{ categories.modularity.score }} / 100** ({{ categories.modularity.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| feat-doc-003 | Document covers one feature | warning (recommended) | 0.5 | {{ results['feat-doc-003'].previous_status | default('—') }} | {{ results['feat-doc-003'].status }} | {{ results['feat-doc-003'].trend_display }} | {{ results['feat-doc-003'].evidence | default('—') }} |

## 3. Technology Independence — weight 1.0 of 5.0

**Why this matters:** Feature describes what, not how. A technology reference here is a sign the document has drifted into Feature Technical's territory.

**Category Score: {{ categories.technology_independence.score }} / 100** ({{ categories.technology_independence.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| feat-doc-004 | No specific programming languages, frameworks, libraries, APIs, database schemas, or protocols named | error (mandatory) | 1.0 | {{ results['feat-doc-004'].previous_status | default('—') }} | {{ results['feat-doc-004'].status }} | {{ results['feat-doc-004'].trend_display }} | {{ results['feat-doc-004'].evidence | default('—') }} |

## 4. Cross-References — weight 0.5 of 5.0

**Why this matters:** Feature without upstream references to Vision and Philosophy has no traceable product intent. Without downstream references to Feature Design and Feature Technical, it has no impact chain.

**Category Score: {{ categories.cross_references.score }} / 100** ({{ categories.cross_references.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| feat-doc-005 | References upstream (Vision — derives_from, Philosophy — guided_by) and downstream (Feature Design, Feature Technical) | warning (recommended) | 0.5 | {{ results['feat-doc-005'].previous_status | default('—') }} | {{ results['feat-doc-005'].status }} | {{ results['feat-doc-005'].trend_display }} | {{ results['feat-doc-005'].evidence | default('—') }} |

## 5. Duplicate Content — weight 0.5 of 5.0

**Why this matters:** Every feature concept should be defined exactly once. Duplication is how two sections quietly drift apart over time.

**Category Score: {{ categories.duplicate_content.score }} / 100** ({{ categories.duplicate_content.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| feat-doc-006 | No section repeats information already stated in another section | warning (recommended) | 0.5 | {{ results['feat-doc-006'].previous_status | default('—') }} | {{ results['feat-doc-006'].status }} | {{ results['feat-doc-006'].trend_display }} | {{ results['feat-doc-006'].evidence | default('—') }} |

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
| Domain | feature |
| Standard | documentation-standards |
| Rule File | `audit/deterministic/document/04-feature.yaml` |
| Auditor | System (deterministic engine) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
