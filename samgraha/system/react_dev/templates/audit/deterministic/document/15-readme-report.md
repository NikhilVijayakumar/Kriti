# Deterministic Whole-Document Report — README

**Document:** {{ document_path }}
**Standard:** `documentation-standards/15-readme-standards.md`
**Rule File:** `audit/deterministic/document/15-readme.yaml`
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

Total possible weight across all 6 document-level rules is fixed at **5.0** (readme-doc-001 1.5, 002 1.0, 003 0.5, 004 1.0, 005 0.5, 006 0.5 — see `audit/deterministic/document/15-readme.yaml`). Mandatory rules (001, 002, 004 — combined weight 3.5 of 5.0) carry most of the score; a single mandatory failure is a heavier hit than any one recommended failure, by design.

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
| Collection Completeness | {{ categories.collection_completeness.score }} / 100 | {{ categories.collection_completeness.previous_score | default('—') }} | {{ categories.collection_completeness.trend_display }} | readme-doc-001, 002 |
| Modularity | {{ categories.modularity.score }} / 100 | {{ categories.modularity.previous_score | default('—') }} | {{ categories.modularity.trend_display }} | readme-doc-003 |
| Derivation Completeness | {{ categories.derivation_completeness.score }} / 100 | {{ categories.derivation_completeness.previous_score | default('—') }} | {{ categories.derivation_completeness.trend_display }} | readme-doc-004 |
| Section Ordering | {{ categories.section_ordering.score }} / 100 | {{ categories.section_ordering.previous_score | default('—') }} | {{ categories.section_ordering.trend_display }} | readme-doc-005 |
| Duplicate Content | {{ categories.duplicate_content.score }} / 100 | {{ categories.duplicate_content.previous_score | default('—') }} | {{ categories.duplicate_content.trend_display }} | readme-doc-006 |

---

## 1. Collection Completeness — weight 2.5 of 5.0

**Why this matters:** README is the single entry point for anyone encountering the project. Missing a required section — or having one that's present but empty — means a reader hits a dead end where they expected guidance. The gap propagates to every downstream section that assumes the missing content exists.

**Category Score: {{ categories.collection_completeness.score }} / 100** ({{ categories.collection_completeness.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-doc-001 | Required sections present (project_name, short_description, overview, purpose, key_capabilities, repository_structure, documentation_structure, getting_started, installation, build, usage, development, contributing) | error (mandatory) | 1.5 | {{ results['readme-doc-001'].previous_status \| default('—') }} | {{ results['readme-doc-001'].status }} | {{ results['readme-doc-001'].trend_display }} | {{ results['readme-doc-001'].evidence \| default('—') }} |
| readme-doc-002 | No empty required sections — a heading alone doesn't satisfy the requirement | error (mandatory) | 1.0 | {{ results['readme-doc-002'].previous_status \| default('—') }} | {{ results['readme-doc-002'].status }} | {{ results['readme-doc-002'].trend_display }} | {{ results['readme-doc-002'].evidence \| default('—') }} |

## 2. Modularity — weight 0.5 of 5.0

**Why this matters:** A README should cover one project — one cohesive entry point. A document that mixes unrelated project READMEs forces readers to determine which portions apply to them and makes consistency impossible to maintain as either project evolves.

**Category Score: {{ categories.modularity.score }} / 100** ({{ categories.modularity.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-doc-003 | Document has a single primary focus — does not mix unrelated project READMEs | warning (recommended) | 0.5 | {{ results['readme-doc-003'].previous_status \| default('—') }} | {{ results['readme-doc-003'].status }} | {{ results['readme-doc-003'].trend_display }} | {{ results['readme-doc-003'].evidence \| default('—') }} |

## 3. Derivation Completeness — weight 1.0 of 5.0

**Why this matters:** README derives from Build — the build process determines how the project is installed, run, and developed. A README that doesn't trace back to Build Documentation may contain stale or contradictory instructions that silently diverge from the actual build process.

**Category Score: {{ categories.derivation_completeness.score }} / 100** ({{ categories.derivation_completeness.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-doc-004 | Document references upstream Build Documentation | error (mandatory) | 1.0 | {{ results['readme-doc-004'].previous_status \| default('—') }} | {{ results['readme-doc-004'].status }} | {{ results['readme-doc-004'].trend_display }} | {{ results['readme-doc-004'].evidence \| default('—') }} |

## 4. Section Ordering — weight 0.5 of 5.0

**Why this matters:** Readers develop muscle memory for where information lives. Standard ordering (project_name → short_description → overview → purpose → key_capabilities → repository_structure → documentation_structure → getting_started → installation → build → usage → development → contributing) lets experienced users navigate without scanning headings. Non-standard ordering creates confusion for both readers and cross-references.

**Category Score: {{ categories.section_ordering.score }} / 100** ({{ categories.section_ordering.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-doc-005 | Sections follow the standard README ordering: project_name, short_description, overview, purpose, key_capabilities, repository_structure, documentation_structure, getting_started, installation, build, usage, development, contributing | warning (recommended) | 0.5 | {{ results['readme-doc-005'].previous_status \| default('—') }} | {{ results['readme-doc-005'].status }} | {{ results['readme-doc-005'].trend_display }} | {{ results['readme-doc-005'].evidence \| default('—') }} |

## 5. Duplicate Content — weight 0.5 of 5.0

**Why this matters:** Every README concept should be defined exactly once. Duplication is how two sections quietly drift apart over time — one gets updated, the copy doesn't, and now the document contradicts itself. This is especially dangerous in README where Usage, Installation, and Build can easily repeat overlapping instructions.

**Category Score: {{ categories.duplicate_content.score }} / 100** ({{ categories.duplicate_content.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| readme-doc-006 | No section repeats information already stated in another section | warning (recommended) | 0.5 | {{ results['readme-doc-006'].previous_status \| default('—') }} | {{ results['readme-doc-006'].status }} | {{ results['readme-doc-006'].trend_display }} | {{ results['readme-doc-006'].evidence \| default('—') }} |

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
| Domain | readme |
| Standard | documentation-standards |
| Rule File | `audit/deterministic/document/15-readme.yaml` |
| Auditor | System (deterministic engine) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
