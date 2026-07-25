# Deterministic Whole-Document Report — Feature Technical

**Document:** {{ document_path }}
**Standard:** `documentation-standards/10-feature-technical-standards.md`
**Rule File:** `audit/deterministic/document/10-feature-technical.yaml`
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
      = 100 × {{ passed_weight }} / 7.0
```

Total possible weight across all 9 document-level rules is fixed at **7.0** (ft-doc-001 1.5, 002 1.0, 003 0.5, 004 1.0, 005 0.5, 006 0.5, 007 1.0, 008 0.5, 009 0.5 — see `audit/deterministic/document/10-feature-technical.yaml`). Mandatory rules (001, 002, 004, 007 — combined weight 4.5 of 7.0) carry most of the score; a single mandatory failure is a heavier hit than any one recommended failure, by design.

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
| Collection Completeness | {{ categories.collection_completeness.score }} / 100 | {{ categories.collection_completeness.previous_score | default('—') }} | {{ categories.collection_completeness.trend_display }} | ft-doc-001, 002 |
| Modularity | {{ categories.modularity.score }} / 100 | {{ categories.modularity.previous_score | default('—') }} | {{ categories.modularity.trend_display }} | ft-doc-003 |
| Technology Independence | {{ categories.technology_independence.score }} / 100 | {{ categories.technology_independence.previous_score | default('—') }} | {{ categories.technology_independence.trend_display }} | ft-doc-004 |
| Cross-References | {{ categories.cross_references.score }} / 100 | {{ categories.cross_references.previous_score | default('—') }} | {{ categories.cross_references.trend_display }} | ft-doc-005 |
| Duplicate Content | {{ categories.duplicate_content.score }} / 100 | {{ categories.duplicate_content.previous_score | default('—') }} | {{ categories.duplicate_content.trend_display }} | ft-doc-006 |
| Tier 3 Positioning | {{ categories.tier_3_positioning.score }} / 100 | {{ categories.tier_3_positioning.previous_score | default('—') }} | {{ categories.tier_3_positioning.trend_display }} | ft-doc-007 |
| Validation & Derivation Markers | {{ categories.validation_derivation_markers.score }} / 100 | {{ categories.validation_derivation_markers.previous_score | default('—') }} | {{ categories.validation_derivation_markers.trend_display }} | ft-doc-008, 009 |

---

## 1. Collection Completeness — weight 2.5 of 7.0

**Why this matters:** Feature Technical Documentation must contain all required sections (Purpose, Participating Components, Component Interactions, Data Ownership) to give downstream Implementation a complete specification to build against. Missing or empty sections leave gaps that propagate silently into implementation.

**Category Score: {{ categories.collection_completeness.score }} / 100** ({{ categories.collection_completeness.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-doc-001 | Required sections present (Purpose, Participating Components, Component Interactions, Data Ownership) | error (mandatory) | 1.5 | {{ results['ft-doc-001'].previous_status \| default('—') }} | {{ results['ft-doc-001'].status }} | {{ results['ft-doc-001'].trend_display }} | {{ results['ft-doc-001'].evidence \| default('—') }} |
| ft-doc-002 | No empty required sections — a heading alone doesn't satisfy the requirement | error (mandatory) | 1.0 | {{ results['ft-doc-002'].previous_status \| default('—') }} | {{ results['ft-doc-002'].status }} | {{ results['ft-doc-002'].trend_display }} | {{ results['ft-doc-002'].evidence \| default('—') }} |

## 2. Modularity — weight 0.5 of 7.0

**Why this matters:** Feature Technical is meant to describe one technical concern — one feature's realization. A document mixing unrelated feature technical concerns is harder to keep consistent and harder for a reader to find the authoritative source for a given concern.

**Category Score: {{ categories.modularity.score }} / 100** ({{ categories.modularity.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-doc-003 | Document has a single primary focus — does not mix unrelated feature technical concerns | warning (recommended) | 0.5 | {{ results['ft-doc-003'].previous_status \| default('—') }} | {{ results['ft-doc-003'].status }} | {{ results['ft-doc-003'].trend_display }} | {{ results['ft-doc-003'].evidence \| default('—') }} |

## 3. Technology Independence — weight 1.0 of 7.0

**Why this matters:** Feature Technical describes *what* the feature does technically, not *how* it's built with specific tools. A technology reference here (a specific language, framework, library, or protocol) means the document becomes stale the moment that technology choice changes, and it crosses into Implementation territory.

**Category Score: {{ categories.technology_independence.score }} / 100** ({{ categories.technology_independence.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-doc-004 | No specific programming languages, frameworks, libraries, database schemas, or protocols named | error (mandatory) | 1.0 | {{ results['ft-doc-004'].previous_status \| default('—') }} | {{ results['ft-doc-004'].status }} | {{ results['ft-doc-004'].trend_display }} | {{ results['ft-doc-004'].evidence \| default('—') }} |

## 4. Cross-References — weight 0.5 of 7.0

**Why this matters:** Feature Technical derives from Feature, Engineering, and Architecture — without cross-references, readers cannot trace why this technical design exists or verify it hasn't drifted from its upstream intent.

**Category Score: {{ categories.cross_references.score }} / 100** ({{ categories.cross_references.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-doc-005 | References upstream domains (Feature — derives from, Engineering — derives from, Architecture — derives from) | warning (recommended) | 0.5 | {{ results['ft-doc-005'].previous_status \| default('—') }} | {{ results['ft-doc-005'].status }} | {{ results['ft-doc-005'].trend_display }} | {{ results['ft-doc-005'].evidence \| default('—') }} |

## 5. Duplicate Content — weight 0.5 of 7.0

**Why this matters:** Every feature technical concept should be defined exactly once. Duplication is how two sections quietly drift apart over time — one gets updated, the copy doesn't, and now the document contradicts itself.

**Category Score: {{ categories.duplicate_content.score }} / 100** ({{ categories.duplicate_content.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-doc-006 | No section repeats information already stated in another section | warning (recommended) | 0.5 | {{ results['ft-doc-006'].previous_status \| default('—') }} | {{ results['ft-doc-006'].status }} | {{ results['ft-doc-006'].trend_display }} | {{ results['ft-doc-006'].evidence \| default('—') }} |

## 6. Tier 3 Positioning — weight 1.0 of 7.0

**Why this matters:** Feature Technical is Tier 3 — it must not derive from Implementation or Prototype (lower tiers). A document that claims derivation from a lower tier inverts the hierarchy, making it impossible to tell whether the technical design was derived from requirements or retrofitted to match existing code.

**Category Score: {{ categories.tier_3_positioning.score }} / 100** ({{ categories.tier_3_positioning.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-doc-007 | Feature Technical is Tier 3 and must not derive from Implementation or Prototype | error (mandatory) | 1.0 | {{ results['ft-doc-007'].previous_status \| default('—') }} | {{ results['ft-doc-007'].status }} | {{ results['ft-doc-007'].trend_display }} | {{ results['ft-doc-007'].evidence \| default('—') }} |

## 7. Validation & Derivation Markers — weight 1.0 of 7.0

**Why this matters:** Feature Technical sits between Feature/Architecture (upstream) and Implementation (downstream). Markers for Prototype validation and Implementation derivation make the derivation chain explicit — without them, readers cannot tell whether the document has been validated or what it feeds.

**Category Score: {{ categories.validation_derivation_markers.score }} / 100** ({{ categories.validation_derivation_markers.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| ft-doc-008 | Document or relationships reference Prototype as validation gate | warning (recommended) | 0.5 | {{ results['ft-doc-008'].previous_status \| default('—') }} | {{ results['ft-doc-008'].status }} | {{ results['ft-doc-008'].trend_display }} | {{ results['ft-doc-008'].evidence \| default('—') }} |
| ft-doc-009 | Document or relationships reference Implementation as downstream consumer | warning (recommended) | 0.5 | {{ results['ft-doc-009'].previous_status \| default('—') }} | {{ results['ft-doc-009'].status }} | {{ results['ft-doc-009'].trend_display }} | {{ results['ft-doc-009'].evidence \| default('—') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Rule | Category | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.id }} | {{ r.category }} | {{ r.message }} | {{ r.evidence | default('—') }} | {{ 'Yes — regression' if r.is_new_failure else 'No — carried over' }} |
{% endfor %}
{% else %}
No failures — all 9 document-level rules pass.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | feature-technical |
| Standard | documentation-standards |
| Rule File | `audit/deterministic/document/10-feature-technical.yaml` |
| Auditor | System (deterministic engine) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
