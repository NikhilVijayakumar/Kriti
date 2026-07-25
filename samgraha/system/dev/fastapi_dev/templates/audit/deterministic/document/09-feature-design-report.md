# Deterministic Whole-Document Report — Feature Design

**Document:** {{ document_path }}
**Standard:** `documentation-standards/09-feature-design-standards.md`
**Rule File:** `audit/deterministic/document/09-feature-design.yaml`
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Deterministic Whole Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
score = 100 × (Σ weight of passed rules) / (Σ weight of all rules)
# calculation: deterministic_document_v1
      = 100 × {{ passed_weight }} / 6.5
```

Total possible weight across all 8 document-level rules is fixed at **6.5** (fd-doc-001 1.5, 002 1.0, 003 0.5, 004 1.0, 005 0.5, 006 0.5, 007 1.0, 008 0.5 — see `audit/deterministic/document/09-feature-design.yaml`). Mandatory rules (001, 002, 004, 007 — combined weight 4.5 of 6.5) carry most of the score; a single mandatory failure is a heavier hit than any one recommended failure, by design.

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
| Collection Completeness | {{ categories.collection_completeness.score }} / 100 | {{ categories.collection_completeness.previous_score | default('—') }} | {{ categories.collection_completeness.trend_display }} | fd-doc-001, 002 |
| Modularity | {{ categories.modularity.score }} / 100 | {{ categories.modularity.previous_score | default('—') }} | {{ categories.modularity.trend_display }} | fd-doc-003 |
| Technology Independence | {{ categories.technology_independence.score }} / 100 | {{ categories.technology_independence.previous_score | default('—') }} | {{ categories.technology_independence.trend_display }} | fd-doc-004 |
| Cross-References | {{ categories.cross_references.score }} / 100 | {{ categories.cross_references.previous_score | default('—') }} | {{ categories.cross_references.trend_display }} | fd-doc-005 |
| Duplicate Content | {{ categories.duplicate_content.score }} / 100 | {{ categories.duplicate_content.previous_score | default('—') }} | {{ categories.duplicate_content.trend_display }} | fd-doc-006 |
| Tier Enforcement | {{ categories.tier_enforcement.score }} / 100 | {{ categories.tier_enforcement.previous_score | default('—') }} | {{ categories.tier_enforcement.trend_display }} | fd-doc-007 |
| Validation Marker | {{ categories.validation_marker.score }} / 100 | {{ categories.validation_marker.previous_score | default('—') }} | {{ categories.validation_marker.trend_display }} | fd-doc-008 |

---

## 1. Collection Completeness — weight 2.5 of 6.5

**Why this matters:** Feature Design Documentation is meant to be read as one coherent feature specification. A document missing a required section, or one with a required section that's present but empty, gives downstream standards (Feature Technical) nothing to constrain themselves against for that concern — the gap propagates downstream instead of being caught here.

**Category Score: {{ categories.collection_completeness.score }} / 100** ({{ categories.collection_completeness.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| fd-doc-001 | Required sections present (User Experience, Workflow, States) | error (mandatory) | 1.5 | {{ results['fd-doc-001'].previous_status \| default('—') }} | {{ results['fd-doc-001'].status }} | {{ results['fd-doc-001'].trend_display }} | {{ results['fd-doc-001'].evidence \| default('—') }} |
| fd-doc-002 | No empty required sections — a heading alone doesn't satisfy the requirement | error (mandatory) | 1.0 | {{ results['fd-doc-002'].previous_status \| default('—') }} | {{ results['fd-doc-002'].status }} | {{ results['fd-doc-002'].trend_display }} | {{ results['fd-doc-002'].evidence \| default('—') }} |

## 2. Modularity — weight 0.5 of 6.5

**Why this matters:** Feature Design is meant to be a focused document — one feature concern per file. A document that mixes unrelated feature design concerns is harder to keep consistent as either concern evolves, and harder for a reader to know which document is authoritative for what.

**Category Score: {{ categories.modularity.score }} / 100** ({{ categories.modularity.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| fd-doc-003 | Document covers one feature design concern — does not mix unrelated concerns | warning (recommended) | 0.5 | {{ results['fd-doc-003'].previous_status \| default('—') }} | {{ results['fd-doc-003'].status }} | {{ results['fd-doc-003'].trend_display }} | {{ results['fd-doc-003'].evidence \| default('—') }} |

## 3. Technology Independence — weight 1.0 of 6.5

**Why this matters:** Feature Design describes user experience, workflows, and states — not implementation. A technology reference here is a sign the document has drifted from design concern into Feature Technical's territory, and it makes the document stale the moment that technology choice changes.

**Category Score: {{ categories.technology_independence.score }} / 100** ({{ categories.technology_independence.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| fd-doc-004 | No specific programming languages, frameworks, libraries, database schemas, or protocols named | error (mandatory) | 1.0 | {{ results['fd-doc-004'].previous_status \| default('—') }} | {{ results['fd-doc-004'].status }} | {{ results['fd-doc-004'].trend_display }} | {{ results['fd-doc-004'].evidence \| default('—') }} |

## 4. Cross-References — weight 0.5 of 6.5

**Why this matters:** Feature Design is Tier 3 — derived from Feature and Design. A document with no trace back to either reads as if it were designed in isolation, which makes it harder to justify why the design looks the way it does when questioned later.

**Category Score: {{ categories.cross_references.score }} / 100** ({{ categories.cross_references.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| fd-doc-005 | References upstream (Feature — derives_from, Design — derives_from) | warning (recommended) | 0.5 | {{ results['fd-doc-005'].previous_status \| default('—') }} | {{ results['fd-doc-005'].status }} | {{ results['fd-doc-005'].trend_display }} | {{ results['fd-doc-005'].evidence \| default('—') }} |

## 5. Duplicate Content — weight 0.5 of 6.5

**Why this matters:** Every feature design concept should be defined exactly once. Duplication is how two sections quietly drift apart over time — one gets updated, the copy doesn't, and now the document contradicts itself.

**Category Score: {{ categories.duplicate_content.score }} / 100** ({{ categories.duplicate_content.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| fd-doc-006 | No section repeats information already stated in another section | warning (recommended) | 0.5 | {{ results['fd-doc-006'].previous_status \| default('—') }} | {{ results['fd-doc-006'].status }} | {{ results['fd-doc-006'].trend_display }} | {{ results['fd-doc-006'].evidence \| default('—') }} |

## 6. Tier Enforcement — weight 1.0 of 6.5

**Why this matters:** Feature Design is Tier 3 — it derives from Feature and Design, not from Architecture, Engineering, or Vision. A document that claims derivation from a higher-tier domain violates the documentation hierarchy and makes the provenance chain unreliable.

**Category Score: {{ categories.tier_enforcement.score }} / 100** ({{ categories.tier_enforcement.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| fd-doc-007 | Does not claim derivation from Architecture, Engineering, or Vision | error (mandatory) | 1.0 | {{ results['fd-doc-007'].previous_status \| default('—') }} | {{ results['fd-doc-007'].status }} | {{ results['fd-doc-007'].trend_display }} | {{ results['fd-doc-007'].evidence \| default('—') }} |

## 7. Validation Marker — weight 0.5 of 6.5

**Why this matters:** Feature Design is validated by Prototype before it reaches Feature Technical. A document that doesn't mention Prototype validation has no signal that the design was tested against reality.

**Category Score: {{ categories.validation_marker.score }} / 100** ({{ categories.validation_marker.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| fd-doc-008 | Mentions Prototype as validation gate | warning (recommended) | 0.5 | {{ results['fd-doc-008'].previous_status \| default('—') }} | {{ results['fd-doc-008'].status }} | {{ results['fd-doc-008'].trend_display }} | {{ results['fd-doc-008'].evidence \| default('—') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Rule | Category | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.id }} | {{ r.category }} | {{ r.message }} | {{ r.evidence | default('—') }} | {{ 'Yes — regression' if r.is_new_failure else 'No — carried over' }} |
{% endfor %}
{% else %}
No failures — all 8 document-level rules pass.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | feature-design |
| Standard | documentation-standards |
| Rule File | `audit/deterministic/document/09-feature-design.yaml` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
