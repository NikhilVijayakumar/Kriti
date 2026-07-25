# Deterministic Whole-Document Report — Build

**Document:** {{ document_path }}
**Standard:** `documentation-standards/14-build-standards.md`
**Rule File:** `audit/deterministic/document/14-build.yaml`
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

Total possible weight across all 6 document-level rules is fixed at **5.0** (build-doc-001 1.5, 002 1.0, 003 0.5, 004 1.0, 005 0.5, 006 0.5 — see `audit/deterministic/document/14-build.yaml`). Mandatory rules (001, 002, 004 — combined weight 3.5 of 5.0) carry most of the score; a single mandatory failure is heavier than any one recommended failure, by design.

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
| Collection Completeness | {{ categories.collection_completeness.score }} / 100 | {{ categories.collection_completeness.previous_score | default('—') }} | {{ categories.collection_completeness.trend_display }} | build-doc-001, 002 |
| Modularity | {{ categories.modularity.score }} / 100 | {{ categories.modularity.previous_score | default('—') }} | {{ categories.modularity.trend_display }} | build-doc-003 |
| Derivation Completeness | {{ categories.derivation_completeness.score }} / 100 | {{ categories.derivation_completeness.previous_score | default('—') }} | {{ categories.derivation_completeness.trend_display }} | build-doc-004 |
| Cross-References | {{ categories.cross_references.score }} / 100 | {{ categories.cross_references.previous_score | default('—') }} | {{ categories.cross_references.trend_display }} | build-doc-005 |
| Duplicate Content | {{ categories.duplicate_content.score }} / 100 | {{ categories.duplicate_content.previous_score | default('—') }} | {{ categories.duplicate_content.trend_display }} | build-doc-006 |

---

## 1. Collection Completeness — weight 2.5 of 5.0

**Why this matters:** Build Documentation is meant to read as one coherent packaging/distribution policy. A document missing a required section, or one with a required section that's present but empty, gives downstream Readme Documentation nothing to derive against for that concern — the gap propagates instead of being caught here.

**Category Score: {{ categories.collection_completeness.score }} / 100** ({{ categories.collection_completeness.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| build-doc-001 | Required sections present (Documentation Quality, Security Checks, Versioning & Naming) | error (mandatory) | 1.5 | {{ results['build-doc-001'].previous_status \| default('—') }} | {{ results['build-doc-001'].status }} | {{ results['build-doc-001'].trend_display }} | {{ results['build-doc-001'].evidence \| default('—') }} |
| build-doc-002 | No empty required sections — a heading alone doesn't satisfy the requirement | error (mandatory) | 1.0 | {{ results['build-doc-002'].previous_status \| default('—') }} | {{ results['build-doc-002'].status }} | {{ results['build-doc-002'].trend_display }} | {{ results['build-doc-002'].evidence \| default('—') }} |

## 2. Modularity — weight 0.5 of 5.0

**Why this matters:** Build Documentation is meant to be a focused document — one build concern per file. A document that mixes unrelated build configurations (e.g. two unrelated packaging strategies in the same file) is harder to keep consistent as either evolves, and harder for a reader to know which document is authoritative for what.

**Category Score: {{ categories.modularity.score }} / 100** ({{ categories.modularity.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| build-doc-003 | Document has a single primary focus — does not mix unrelated build concerns | warning (recommended) | 0.5 | {{ results['build-doc-003'].previous_status \| default('—') }} | {{ results['build-doc-003'].status }} | {{ results['build-doc-003'].trend_display }} | {{ results['build-doc-003'].evidence \| default('—') }} |

## 3. Derivation Completeness — weight 1.0 of 5.0

**Why this matters:** Build is derived from Implementation Documentation — a Build document with no upstream reference reads as if it were authored in isolation from what the code actually does. Without the derivation link, there's no way to verify Build's packaging claims match what was actually implemented.

**Category Score: {{ categories.derivation_completeness.score }} / 100** ({{ categories.derivation_completeness.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| build-doc-004 | Document references upstream Implementation Documentation | error (mandatory) | 1.0 | {{ results['build-doc-004'].previous_status \| default('—') }} | {{ results['build-doc-004'].status }} | {{ results['build-doc-004'].trend_display }} | {{ results['build-doc-004'].evidence \| default('—') }} |

## 4. Cross-References — weight 0.5 of 5.0

**Why this matters:** Build Documentation without downstream references is an orphan — it specifies packaging but has no traceable handoff to Readme Documentation that documents usage. Without cross-references, readers can't tell if downstream docs reflect the current build policy.

**Category Score: {{ categories.cross_references.score }} / 100** ({{ categories.cross_references.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| build-doc-005 | References downstream Readme Documentation where applicable | warning (recommended) | 0.5 | {{ results['build-doc-005'].previous_status \| default('—') }} | {{ results['build-doc-005'].status }} | {{ results['build-doc-005'].trend_display }} | {{ results['build-doc-005'].evidence \| default('—') }} |

## 5. Duplicate Content — weight 0.5 of 5.0

**Why this matters:** Every build concept should be defined exactly once. Duplication is how two sections quietly drift apart over time — one gets updated, the copy doesn't, and now the document contradicts itself.

**Category Score: {{ categories.duplicate_content.score }} / 100** ({{ categories.duplicate_content.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| build-doc-006 | No section repeats information already stated in another section | warning (recommended) | 0.5 | {{ results['build-doc-006'].previous_status \| default('—') }} | {{ results['build-doc-006'].status }} | {{ results['build-doc-006'].trend_display }} | {{ results['build-doc-006'].evidence \| default('—') }} |

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
| Domain | build |
| Standard | documentation-standards |
| Rule File | `audit/deterministic/document/14-build.yaml` |
| Auditor | System (deterministic engine) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
