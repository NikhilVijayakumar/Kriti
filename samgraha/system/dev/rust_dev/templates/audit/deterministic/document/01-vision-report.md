# Deterministic Whole-Document Report â€” Vision

**Document:** {{ document_path }}
**Standard:** `documentation-standards/01-vision-standards.md`
**Rule File:** `audit/deterministic/document/01-vision.yaml`
**Auditor:** System (deterministic engine)
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Deterministic Whole Score: {{ score }} / 100**
{% if previous_score %}({{ 'â†‘ Improved' if score > previous_score else 'â†“ Regressed' if score < previous_score else 'â†’ Unchanged' }} vs. previous run){% else %}(baseline â€” first audit of this document){% endif %}

```
score = 100 Ã— (Î£ weight of passed rules) / (Î£ weight of all rules)
# calculation: deterministic_document_v1
      = 100 Ã— {{ passed_weight }} / 5.5
```

Total possible weight across all 7 document-level rules is fixed at **5.5** (vis-doc-001 1.5, 002 1.0, 003 0.5, 004 1.0, 005 1.0, 006 0.5, 007 0.5 â€” see `audit/deterministic/document/01-vision.yaml`). Mandatory rules (001, 002, 004, 005 â€” combined weight 4.5 of 5.5) carry most of the score; a single mandatory failure is a heavier hit than any one recommended failure, by design.

### Score History

| Revision | Date | Score | vs. Previous | vs. Baseline |
|---:|---|---:|---|---|
{% for r in revision_history -%}
| {{ r.revision }} | {{ r.date }} | {{ r.score }} / 100 | {{ r.delta_previous_display }} | {{ r.delta_baseline_display }} |
{% endfor -%}
| {{ revision_number }} (current) | {{ created_at }} | {{ score }} / 100 | {{ delta_previous_display }} | {{ delta_baseline_display }} |

{% if not previous_score %}No prior runs â€” this revision is the baseline every future run is compared against.{% endif %}

### Category Scores

| Category | Score | Previous | Trend | Rules |
|---|---:|---:|---|---|
| Collection Completeness | {{ categories.collection_completeness.score }} / 100 | {{ categories.collection_completeness.previous_score | default('â€”') }} | {{ categories.collection_completeness.trend_display }} | vis-doc-001, 002 |
| Modularity | {{ categories.modularity.score }} / 100 | {{ categories.modularity.previous_score | default('â€”') }} | {{ categories.modularity.trend_display }} | vis-doc-003 |
| Technology Independence | {{ categories.technology_independence.score }} / 100 | {{ categories.technology_independence.previous_score | default('â€”') }} | {{ categories.technology_independence.trend_display }} | vis-doc-004 |
| Tier 1 Positioning | {{ categories.tier_1_positioning.score }} / 100 | {{ categories.tier_1_positioning.previous_score | default('â€”') }} | {{ categories.tier_1_positioning.trend_display }} | vis-doc-005 |
| Cross-References | {{ categories.cross_references.score }} / 100 | {{ categories.cross_references.previous_score | default('â€”') }} | {{ categories.cross_references.trend_display }} | vis-doc-006 |
| Duplicate Content | {{ categories.duplicate_content.score }} / 100 | {{ categories.duplicate_content.previous_score | default('â€”') }} | {{ categories.duplicate_content.trend_display }} | vis-doc-007 |

---

## 1. Collection Completeness â€” weight 2.5 of 5.5

**Why this matters:** Vision Documentation is meant to be read as one coherent aspirational statement. A document missing a required section, or one with a required section that's present but empty, gives Philosophy and Feature nothing to derive themselves against for that concern â€” the gap propagates downstream instead of being caught here.

**Category Score: {{ categories.collection_completeness.score }} / 100** ({{ categories.collection_completeness.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| vis-doc-001 | Required sections present (Purpose, Vision Statement, Problem, Solution, Target Audience) | error (mandatory) | 1.5 | {{ results['vis-doc-001'].previous_status \| default('â€”') }} | {{ results['vis-doc-001'].status }} | {{ results['vis-doc-001'].trend_display }} | {{ results['vis-doc-001'].evidence \| default('â€”') }} |
| vis-doc-002 | No empty required sections â€” a heading alone doesn't satisfy the requirement | error (mandatory) | 1.0 | {{ results['vis-doc-002'].previous_status \| default('â€”') }} | {{ results['vis-doc-002'].status }} | {{ results['vis-doc-002'].trend_display }} | {{ results['vis-doc-002'].evidence \| default('â€”') }} |

## 2. Modularity â€” weight 0.5 of 5.5

**Why this matters:** Vision is meant to be a focused document â€” one aspirational direction per file. A document that mixes unrelated product visions (e.g. two unrelated products in the same file) is harder to keep consistent as either vision evolves, and harder for a reader to know which document is authoritative for what.

**Category Score: {{ categories.modularity.score }} / 100** ({{ categories.modularity.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| vis-doc-003 | Document has a single primary focus â€” does not mix unrelated product visions | warning (recommended) | 0.5 | {{ results['vis-doc-003'].previous_status \| default('â€”') }} | {{ results['vis-doc-003'].status }} | {{ results['vis-doc-003'].trend_display }} | {{ results['vis-doc-003'].evidence \| default('â€”') }} |

## 3. Technology Independence â€” weight 1.0 of 5.5

**Why this matters:** Vision describes aspiration â€” where the product is going, not how it will be built. A technology reference here (a specific language, framework, or protocol) is a sign the document has drifted from aspirational concern into Engineering's territory, and it makes the document stale the moment that technology choice changes.

**Category Score: {{ categories.technology_independence.score }} / 100** ({{ categories.technology_independence.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| vis-doc-004 | No specific programming languages, frameworks, libraries, database schemas, or protocols named | error (mandatory) | 1.0 | {{ results['vis-doc-004'].previous_status \| default('â€”') }} | {{ results['vis-doc-004'].status }} | {{ results['vis-doc-004'].trend_display }} | {{ results['vis-doc-004'].evidence \| default('â€”') }} |

## 4. Tier 1 Positioning â€” weight 1.0 of 5.5

**Why this matters:** Vision is Tier 1 â€” the root of the derivation chain. A document with no trace back to anything reads as if it were designed in isolation from product intent, which makes it harder to justify why the vision looks the way it does when questioned later. Conversely, if it *does* derive from something, the entire documentation hierarchy has no anchor.

**Category Score: {{ categories.tier_1_positioning.score }} / 100** ({{ categories.tier_1_positioning.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| vis-doc-005 | Vision derives from no other domain â€” Vision is Tier 1, the root of the derivation chain | error (mandatory) | 1.0 | {{ results['vis-doc-005'].previous_status \| default('â€”') }} | {{ results['vis-doc-005'].status }} | {{ results['vis-doc-005'].trend_display }} | {{ results['vis-doc-005'].evidence \| default('â€”') }} |

## 5. Cross-References â€” weight 0.5 of 5.5

**Why this matters:** Vision without downstream references is an orphan â€” it inspires nothing and has no traceable impact. A Vision document that doesn't reference Philosophy, Feature, and Security as downstream consumers means those domains have no upstream source of truth to derive from.

**Category Score: {{ categories.cross_references.score }} / 100** ({{ categories.cross_references.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| vis-doc-006 | References downstream (Philosophy â€” inspires, Feature â€” inspires, Security â€” inspires) | warning (recommended) | 0.5 | {{ results['vis-doc-006'].previous_status \| default('â€”') }} | {{ results['vis-doc-006'].status }} | {{ results['vis-doc-006'].trend_display }} | {{ results['vis-doc-006'].evidence \| default('â€”') }} |

## 6. Duplicate Content â€” weight 0.5 of 5.5

**Why this matters:** Every vision concept should be defined exactly once. Duplication is how two sections quietly drift apart over time â€” one gets updated, the copy doesn't, and now the document contradicts itself.

**Category Score: {{ categories.duplicate_content.score }} / 100** ({{ categories.duplicate_content.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| vis-doc-007 | No section repeats information already stated in another section | warning (recommended) | 0.5 | {{ results['vis-doc-007'].previous_status \| default('â€”') }} | {{ results['vis-doc-007'].status }} | {{ results['vis-doc-007'].trend_display }} | {{ results['vis-doc-007'].evidence \| default('â€”') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Rule | Category | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.id }} | {{ r.category }} | {{ r.message }} | {{ r.evidence | default('â€”') }} | {{ 'Yes â€” regression' if r.is_new_failure else 'No â€” carried over' }} |
{% endfor %}
{% else %}
No failures â€” all 7 document-level rules pass.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | vision |
| Standard | documentation-standards |
| Rule File | `audit/deterministic/document/01-vision.yaml` |
| Auditor | System (deterministic engine) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
