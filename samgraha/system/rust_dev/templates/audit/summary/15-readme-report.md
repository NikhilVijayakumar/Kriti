# Audit Summary — README

**Document:** {{ document_path }}
**Standard:** `documentation-standards/15-readme-standards.md`
**Auditor:** System (deterministic engine) + LLM ({{ model_name }})
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Final Score

**{{ final_score }} / 100** — **{{ rating }}**
{% if previous_score %}({{ '↑ Improved' if final_score > previous_score else '↓ Regressed' if final_score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

*Trend computed per `calculation: trend_v1`.*

```
final_score = (deterministic_whole/100 × 25)
            + (deterministic_section/100 × 25)
            + (semantic_whole/100 × 25)
            + (semantic_section/100 × 25)
# calculation: final_score_v1
```

| Report | Score | Previous | Trend | Weight | Contribution |
|---|---:|---:|---|---|---|
| Deterministic — Whole | {{ deterministic_whole }} | {{ bucket_trend.det_whole.previous | default('—') }} | {{ bucket_trend.det_whole.trend_display }} | 25% | {{ (deterministic_whole / 100 * 25) | round(1) }} |
| Deterministic — Section | {{ deterministic_section }} | {{ bucket_trend.det_section.previous | default('—') }} | {{ bucket_trend.det_section.trend_display }} | 25% | {{ (deterministic_section / 100 * 25) | round(1) }} |
| Semantic — Whole | {{ semantic_whole }} | {{ bucket_trend.sem_whole.previous | default('—') }} | {{ bucket_trend.sem_whole.trend_display }} | 25% | {{ (semantic_whole / 100 * 25) | round(1) }} |
| Semantic — Section | {{ semantic_section }} | {{ bucket_trend.sem_section.previous | default('—') }} | {{ bucket_trend.sem_section.trend_display }} | 25% | {{ (semantic_section / 100 * 25) | round(1) }} |

Mandatory-criterion severity is absorbed inside each of the four reports' own scoring (see each report's Scoring Criteria table) — this rollup is a plain weighted sum, no additional gating here.

---

## Score History

Every run of this document's audit, oldest first, with this revision last:

| Revision | Date | Final Score | Rating | vs. Previous | vs. Baseline |
|---:|---|---:|---|---|---|
{% for r in revision_history -%}
| {{ r.revision }} | {{ r.date }} | {{ r.score }} / 100 | {{ r.rating }} | {{ r.delta_previous_display }} | {{ r.delta_baseline_display }} |
{% endfor -%}
| {{ revision_number }} (current) | {{ created_at }} | {{ final_score }} / 100 | {{ rating }} | {{ delta_previous_display }} | {{ delta_baseline_display }} |

{% if not previous_score %}No prior runs — this revision is the baseline every future run is compared against.{% else %}Baseline was revision {{ baseline_revision }} ({{ baseline_score }} / 100, {{ baseline_date }}).{% endif %}

---

## Document-Level Breakdown

Deterministic and semantic judge different things at the document level — deterministic checks structural rule groupings, semantic checks cross-section consistency. They aren't the same categories and don't map row-to-row, so they get separate tables rather than being forced side by side.

### Deterministic — Whole (`audit/deterministic/document/15-readme.yaml`)

| Category | Score | Previous | Trend |
|---|---:|---:|---|
| Collection Completeness | {{ categories.collection_completeness.score }} / 100 | {{ categories.collection_completeness.previous_score | default('—') }} | {{ categories.collection_completeness.trend_display }} |
| Modularity | {{ categories.modularity.score }} / 100 | {{ categories.modularity.previous_score | default('—') }} | {{ categories.modularity.trend_display }} |
| Derivation Completeness | {{ categories.derivation_completeness.score }} / 100 | {{ categories.derivation_completeness.previous_score | default('—') }} | {{ categories.derivation_completeness.trend_display }} |
| Section Ordering | {{ categories.section_ordering.score }} / 100 | {{ categories.section_ordering.previous_score | default('—') }} | {{ categories.section_ordering.trend_display }} |
| Duplicate Content | {{ categories.duplicate_content.score }} / 100 | {{ categories.duplicate_content.previous_score | default('—') }} | {{ categories.duplicate_content.trend_display }} |

### Semantic — Whole (`audit/semantic/document/15-readme.md`)

| Criterion | Result | Previous | Trend |
|---|---|---|---|
| C1 — Usage consistent with Build/Installation | {{ doc_semantic.c1_display }} | {{ doc_semantic.c1_previous_display | default('—') }} | {{ doc_semantic.c1_trend_display }} |
| C2 — Development and Contributing consistent | {{ doc_semantic.c2_display }} | {{ doc_semantic.c2_previous_display | default('—') }} | {{ doc_semantic.c2_trend_display }} |
| C3 — Terminology consistent throughout | {{ doc_semantic.c3_display }} | {{ doc_semantic.c3_previous_display | default('—') }} | {{ doc_semantic.c3_trend_display }} |

Full detail, including per-rule/per-criterion evidence: see the Deterministic — Whole and Semantic — Whole reports linked below.

## Section-Level Breakdown

Same reasoning as above, extended per section: a section's deterministic score and its semantic score aren't guaranteed to check the same things (a section can be structurally complete but semantically weak, or vice versa) — two separate tables, not one merged table with a false row-by-row correspondence.

### Deterministic — Section (`audit/deterministic/section/15-readme/*.yaml`)

| # | Section | Required | Score | Previous | Trend |
|---:|---|:---:|---:|---:|---|
| 1 | Project Name | **required** | {{ sections.project_name.det_score }} / 100 | {{ sections.project_name.det_previous_score | default('—') }} | {{ sections.project_name.det_trend_display }} |
| 2 | Short Description | **required** | {{ sections.short_description.det_score }} / 100 | {{ sections.short_description.det_previous_score | default('—') }} | {{ sections.short_description.det_trend_display }} |
| 3 | Overview | **required** | {{ sections.overview.det_score }} / 100 | {{ sections.overview.det_previous_score | default('—') }} | {{ sections.overview.det_trend_display }} |
| 4 | Purpose | **required** | {{ sections.purpose.det_score }} / 100 | {{ sections.purpose.det_previous_score | default('—') }} | {{ sections.purpose.det_trend_display }} |
| 5 | Key Capabilities | **required** | {{ sections.key_capabilities.det_score }} / 100 | {{ sections.key_capabilities.det_previous_score | default('—') }} | {{ sections.key_capabilities.det_trend_display }} |
| 6 | Repository Structure | **required** | {{ sections.repository_structure.det_score }} / 100 | {{ sections.repository_structure.det_previous_score | default('—') }} | {{ sections.repository_structure.det_trend_display }} |
| 7 | Documentation Structure | **required** | {{ sections.documentation_structure.det_score }} / 100 | {{ sections.documentation_structure.det_previous_score | default('—') }} | {{ sections.documentation_structure.det_trend_display }} |
| 8 | Getting Started | **required** | {{ sections.getting_started.det_score }} / 100 | {{ sections.getting_started.det_previous_score | default('—') }} | {{ sections.getting_started.det_trend_display }} |
| 9 | Installation | **required** | {{ sections.installation.det_score }} / 100 | {{ sections.installation.det_previous_score | default('—') }} | {{ sections.installation.det_trend_display }} |
| 10 | Build | **required** | {{ sections.build.det_score }} / 100 | {{ sections.build.det_previous_score | default('—') }} | {{ sections.build.det_trend_display }} |
| 11 | Usage | **required** | {{ sections.usage.det_score }} / 100 | {{ sections.usage.det_previous_score | default('—') }} | {{ sections.usage.det_trend_display }} |
| 12 | Development | **required** | {{ sections.development.det_score }} / 100 | {{ sections.development.det_previous_score | default('—') }} | {{ sections.development.det_trend_display }} |
| 13 | Contributing | **required** | {{ sections.contributing.det_score }} / 100 | {{ sections.contributing.det_previous_score | default('—') }} | {{ sections.contributing.det_trend_display }} |
| 14 | Configuration | optional | {{ sections.configuration.det_score }} / 100 | {{ sections.configuration.det_previous_score | default('—') }} | {{ sections.configuration.det_trend_display }} |
| 15 | License | optional | {{ sections.license.det_score }} / 100 | {{ sections.license.det_previous_score | default('—') }} | {{ sections.license.det_trend_display }} |

### Semantic — Section (`audit/semantic/section/15-readme/*.md`)

| # | Section | Required | Score | Previous | Trend |
|---:|---|:---:|---:|---:|---|
| 1 | Project Name | **required** | {{ sections.project_name.sem_score }} / 100 | {{ sections.project_name.sem_previous_score | default('—') }} | {{ sections.project_name.sem_trend_display }} |
| 2 | Short Description | **required** | {{ sections.short_description.sem_score }} / 100 | {{ sections.short_description.sem_previous_score | default('—') }} | {{ sections.short_description.sem_trend_display }} |
| 3 | Overview | **required** | {{ sections.overview.sem_score }} / 100 | {{ sections.overview.sem_previous_score | default('—') }} | {{ sections.overview.sem_trend_display }} |
| 4 | Purpose | **required** | {{ sections.purpose.sem_score }} / 100 | {{ sections.purpose.sem_previous_score | default('—') }} | {{ sections.purpose.sem_trend_display }} |
| 5 | Key Capabilities | **required** | {{ sections.key_capabilities.sem_score }} / 100 | {{ sections.key_capabilities.sem_previous_score | default('—') }} | {{ sections.key_capabilities.sem_trend_display }} |
| 6 | Repository Structure | **required** | {{ sections.repository_structure.sem_score }} / 100 | {{ sections.repository_structure.sem_previous_score | default('—') }} | {{ sections.repository_structure.sem_trend_display }} |
| 7 | Documentation Structure | **required** | {{ sections.documentation_structure.sem_score }} / 100 | {{ sections.documentation_structure.sem_previous_score | default('—') }} | {{ sections.documentation_structure.sem_trend_display }} |
| 8 | Getting Started | **required** | {{ sections.getting_started.sem_score }} / 100 | {{ sections.getting_started.sem_previous_score | default('—') }} | {{ sections.getting_started.sem_trend_display }} |
| 9 | Installation | **required** | {{ sections.installation.sem_score }} / 100 | {{ sections.installation.sem_previous_score | default('—') }} | {{ sections.installation.sem_trend_display }} |
| 10 | Build | **required** | {{ sections.build.sem_score }} / 100 | {{ sections.build.sem_previous_score | default('—') }} | {{ sections.build.sem_trend_display }} |
| 11 | Usage | **required** | {{ sections.usage.sem_score }} / 100 | {{ sections.usage.sem_previous_score | default('—') }} | {{ sections.usage.sem_trend_display }} |
| 12 | Development | **required** | {{ sections.development.sem_score }} / 100 | {{ sections.development.sem_previous_score | default('—') }} | {{ sections.development.sem_trend_display }} |
| 13 | Contributing | **required** | {{ sections.contributing.sem_score }} / 100 | {{ sections.contributing.sem_previous_score | default('—') }} | {{ sections.contributing.sem_trend_display }} |
| 14 | Configuration | optional | {{ sections.configuration.sem_score }} / 100 | {{ sections.configuration.sem_previous_score | default('—') }} | {{ sections.configuration.sem_trend_display }} |
| 15 | License | optional | {{ sections.license.sem_score }} / 100 | {{ sections.license.sem_previous_score | default('—') }} | {{ sections.license.sem_trend_display }} |
| — | Generic (unmatched sections) | n/a | {{ sections.generic.sem_score }} / 100 | {{ sections.generic.sem_previous_score | default('—') }} | {{ sections.generic.sem_trend_display }} |

Full detail, including per-rule/per-criterion evidence for every row above: see the Deterministic — Section and Semantic — Section reports linked below.

---

## Score Bands

| Range | Rating | Meaning |
|---|---|---|
| 95–100 | Excellent | Fully compliant, no reservations |
| 90–94 | Very Good | Minor gaps, safe to proceed |
| 80–89 | Good | Solid foundation, a few issues to resolve |
| 70–79 | Acceptable | Core present but gaps exist |
| Below 70 | Needs Improvement | Significant gaps, not ready |

*Ratings computed per `calculation: score_bands_v1`.*

---

## Report Links

| Report | File |
|---|---|
| Deterministic — Whole | `{{ det_whole_report_path }}` (`audit/deterministic/document/15-readme.yaml`) |
| Deterministic — Section | `{{ det_section_report_path }}` (`audit/deterministic/section/15-readme/*.yaml`) |
| Semantic — Whole | `{{ sem_whole_report_path }}` (`audit/semantic/document/15-readme.md`) |
| Semantic — Section | `{{ sem_section_report_path }}` (`audit/semantic/section/15-readme/*.md`) |

---

## Top Findings

{% if top_findings | length > 0 %}
| Severity | Source | Rule/Criterion | Message | New This Run? |
|---|---|---|---|---|
{% for f in top_findings -%}
| {{ f.severity }} | {{ f.report_type }} | {{ f.rule_id }} | {{ f.message }} | {{ 'Yes — regression' if f.is_new_finding else 'No — carried over' }} |
{% endfor %}
{% else %}
No findings.
{% endif %}

Full score-history and per-run trend detail lives in the Score History table above, and in each of the 4 linked detail reports (each carries its own Score History and per-row Previous/Trend columns) — this table only surfaces what's new since the last run.

---

## Metadata

| Field | Value |
|---|---|
| Domain | readme |
| Standard | documentation-standards |
| Document | {{ document_path }} |
| Auditor | System (deterministic engine) + LLM ({{ model_name }}) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
| Reports | 4 detail + 1 summary |
