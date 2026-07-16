# Audit Summary — Feature Technical

**Document:** {{ document_path }}
**Standard:** `documentation-standards/10-feature-technical-standards.md`
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

Deterministic and semantic judge different things at the document level — deterministic checks structural rule groupings, semantic checks judgment criteria. They aren't the same categories and don't map row-to-row, so they get separate tables rather than being forced side by side.

### Deterministic — Whole (`audit/deterministic/document/10-feature-technical.yaml`)

| Category | Score | Previous | Trend |
|---|---:|---:|---|
| Collection Completeness | {{ categories.collection_completeness.score }} / 100 | {{ categories.collection_completeness.previous_score | default('—') }} | {{ categories.collection_completeness.trend_display }} |
| Modularity | {{ categories.modularity.score }} / 100 | {{ categories.modularity.previous_score | default('—') }} | {{ categories.modularity.trend_display }} |
| Technology Independence | {{ categories.technology_independence.score }} / 100 | {{ categories.technology_independence.previous_score | default('—') }} | {{ categories.technology_independence.trend_display }} |
| Cross-References | {{ categories.cross_references.score }} / 100 | {{ categories.cross_references.previous_score | default('—') }} | {{ categories.cross_references.trend_display }} |
| Duplicate Content | {{ categories.duplicate_content.score }} / 100 | {{ categories.duplicate_content.previous_score | default('—') }} | {{ categories.duplicate_content.trend_display }} |
| Tier 3 Positioning | {{ categories.tier_3_positioning.score }} / 100 | {{ categories.tier_3_positioning.previous_score | default('—') }} | {{ categories.tier_3_positioning.trend_display }} |
| Validation & Derivation Markers | {{ categories.validation_derivation_markers.score }} / 100 | {{ categories.validation_derivation_markers.previous_score | default('—') }} | {{ categories.validation_derivation_markers.trend_display }} |

### Semantic — Whole (`audit/semantic/document/10-feature-technical.md`)

| Criterion | Result | Previous | Trend |
|---|---|---|---|
| C1 — Cross-section consistency | {{ doc_semantic.c1_display }} | {{ doc_semantic.c1_previous_display | default('—') }} | {{ doc_semantic.c1_trend_display }} |
| C2 — Terminology consistency | {{ doc_semantic.c2_display }} | {{ doc_semantic.c2_previous_display | default('—') }} | {{ doc_semantic.c2_trend_display }} |
| C3 — Cross-document coherence | {{ doc_semantic.c3_display }} | {{ doc_semantic.c3_previous_display | default('—') }} | {{ doc_semantic.c3_trend_display }} |

Full detail, including per-rule/per-criterion evidence: see the Deterministic — Whole and Semantic — Whole reports linked below.

## Section-Level Breakdown

Same reasoning as above, extended per section: a section's deterministic score and its semantic score aren't guaranteed to check the same things (a section can be structurally complete but semantically weak, or vice versa) — two separate tables, not one merged table with a false row-by-row correspondence.

### Deterministic — Section (`audit/deterministic/section/10-feature-technical/*.yaml`)

| # | Section | Required | Score | Previous | Trend |
|---:|---|:---:|---:|---:|---|
| 1 | Purpose | **required** | {{ sections.purpose.det_score }} / 100 | {{ sections.purpose.det_previous_score | default('—') }} | {{ sections.purpose.det_trend_display }} |
| 2 | Participating Components | **required** | {{ sections.participating_components.det_score }} / 100 | {{ sections.participating_components.det_previous_score | default('—') }} | {{ sections.participating_components.det_trend_display }} |
| 3 | Component Interactions | **required** | {{ sections.component_interactions.det_score }} / 100 | {{ sections.component_interactions.det_previous_score | default('—') }} | {{ sections.component_interactions.det_trend_display }} |
| 4 | Data Ownership | **required** | {{ sections.data_ownership.det_score }} / 100 | {{ sections.data_ownership.det_previous_score | default('—') }} | {{ sections.data_ownership.det_trend_display }} |
| 5 | Feature Specification | optional | {{ sections.feature_specification.det_score }} / 100 | {{ sections.feature_specification.det_previous_score | default('—') }} | {{ sections.feature_specification.det_trend_display }} |
| 6 | Component Responsibilities | optional | {{ sections.component_responsibilities.det_score }} / 100 | {{ sections.component_responsibilities.det_previous_score | default('—') }} | {{ sections.component_responsibilities.det_trend_display }} |
| 7 | Runtime Behavior | optional | {{ sections.runtime_behavior.det_score }} / 100 | {{ sections.runtime_behavior.det_previous_score | default('—') }} | {{ sections.runtime_behavior.det_trend_display }} |
| 8 | Communication Paths | optional | {{ sections.communication_paths.det_score }} / 100 | {{ sections.communication_paths.det_previous_score | default('—') }} | {{ sections.communication_paths.det_trend_display }} |
| 9 | Integration Points | optional | {{ sections.integration_points.det_score }} / 100 | {{ sections.integration_points.det_previous_score | default('—') }} | {{ sections.integration_points.det_trend_display }} |
| 10 | External Dependencies | optional | {{ sections.external_dependencies.det_score }} / 100 | {{ sections.external_dependencies.det_previous_score | default('—') }} | {{ sections.external_dependencies.det_trend_display }} |
| 11 | Runtime Constraints | optional | {{ sections.runtime_constraints.det_score }} / 100 | {{ sections.runtime_constraints.det_previous_score | default('—') }} | {{ sections.runtime_constraints.det_trend_display }} |
| 12 | Architectural Constraints | optional | {{ sections.architectural_constraints.det_score }} / 100 | {{ sections.architectural_constraints.det_previous_score | default('—') }} | {{ sections.architectural_constraints.det_trend_display }} |
| 13 | Security Considerations | optional | {{ sections.security_considerations.det_score }} / 100 | {{ sections.security_considerations.det_previous_score | default('—') }} | {{ sections.security_considerations.det_trend_display }} |
| 14 | Performance Considerations | optional | {{ sections.performance_considerations.det_score }} / 100 | {{ sections.performance_considerations.det_previous_score | default('—') }} | {{ sections.performance_considerations.det_trend_display }} |
| 15 | Failure Handling | optional | {{ sections.failure_handling.det_score }} / 100 | {{ sections.failure_handling.det_previous_score | default('—') }} | {{ sections.failure_handling.det_trend_display }} |
| 16 | Extension Points | optional | {{ sections.extension_points.det_score }} / 100 | {{ sections.extension_points.det_previous_score | default('—') }} | {{ sections.extension_points.det_trend_display }} |
| 17 | Traceability | optional | {{ sections.traceability.det_score }} / 100 | {{ sections.traceability.det_previous_score | default('—') }} | {{ sections.traceability.det_trend_display }} |

### Semantic — Section (`audit/semantic/section/10-feature-technical/*.md`)

| # | Section | Required | Score | Previous | Trend |
|---:|---|:---:|---:|---:|---|
| 1 | Purpose | **required** | {{ sections.purpose.sem_score }} / 100 | {{ sections.purpose.sem_previous_score | default('—') }} | {{ sections.purpose.sem_trend_display }} |
| 2 | Participating Components | **required** | {{ sections.participating_components.sem_score }} / 100 | {{ sections.participating_components.sem_previous_score | default('—') }} | {{ sections.participating_components.sem_trend_display }} |
| 3 | Component Interactions | **required** | {{ sections.component_interactions.sem_score }} / 100 | {{ sections.component_interactions.sem_previous_score | default('—') }} | {{ sections.component_interactions.sem_trend_display }} |
| 4 | Data Ownership | **required** | {{ sections.data_ownership.sem_score }} / 100 | {{ sections.data_ownership.sem_previous_score | default('—') }} | {{ sections.data_ownership.sem_trend_display }} |
| 5 | Feature Specification | optional | {{ sections.feature_specification.sem_score }} / 100 | {{ sections.feature_specification.sem_previous_score | default('—') }} | {{ sections.feature_specification.sem_trend_display }} |
| 6 | Component Responsibilities | optional | {{ sections.component_responsibilities.sem_score }} / 100 | {{ sections.component_responsibilities.sem_previous_score | default('—') }} | {{ sections.component_responsibilities.sem_trend_display }} |
| 7 | Runtime Behavior | optional | {{ sections.runtime_behavior.sem_score }} / 100 | {{ sections.runtime_behavior.sem_previous_score | default('—') }} | {{ sections.runtime_behavior.sem_trend_display }} |
| 8 | Communication Paths | optional | {{ sections.communication_paths.sem_score }} / 100 | {{ sections.communication_paths.sem_previous_score | default('—') }} | {{ sections.communication_paths.sem_trend_display }} |
| 9 | Integration Points | optional | {{ sections.integration_points.sem_score }} / 100 | {{ sections.integration_points.sem_previous_score | default('—') }} | {{ sections.integration_points.sem_trend_display }} |
| 10 | External Dependencies | optional | {{ sections.external_dependencies.sem_score }} / 100 | {{ sections.external_dependencies.sem_previous_score | default('—') }} | {{ sections.external_dependencies.sem_trend_display }} |
| 11 | Runtime Constraints | optional | {{ sections.runtime_constraints.sem_score }} / 100 | {{ sections.runtime_constraints.sem_previous_score | default('—') }} | {{ sections.runtime_constraints.sem_trend_display }} |
| 12 | Architectural Constraints | optional | {{ sections.architectural_constraints.sem_score }} / 100 | {{ sections.architectural_constraints.sem_previous_score | default('—') }} | {{ sections.architectural_constraints.sem_trend_display }} |
| 13 | Security Considerations | optional | {{ sections.security_considerations.sem_score }} / 100 | {{ sections.security_considerations.sem_previous_score | default('—') }} | {{ sections.security_considerations.sem_trend_display }} |
| 14 | Performance Considerations | optional | {{ sections.performance_considerations.sem_score }} / 100 | {{ sections.performance_considerations.sem_previous_score | default('—') }} | {{ sections.performance_considerations.sem_trend_display }} |
| 15 | Failure Handling | optional | {{ sections.failure_handling.sem_score }} / 100 | {{ sections.failure_handling.sem_previous_score | default('—') }} | {{ sections.failure_handling.sem_trend_display }} |
| 16 | Extension Points | optional | {{ sections.extension_points.sem_score }} / 100 | {{ sections.extension_points.sem_previous_score | default('—') }} | {{ sections.extension_points.sem_trend_display }} |
| 17 | Traceability | optional | {{ sections.traceability.sem_score }} / 100 | {{ sections.traceability.sem_previous_score | default('—') }} | {{ sections.traceability.sem_trend_display }} |
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
| Deterministic — Whole | `{{ det_whole_report_path }}` (`audit/deterministic/document/10-feature-technical.yaml`) |
| Deterministic — Section | `{{ det_section_report_path }}` (`audit/deterministic/section/10-feature-technical/*.yaml`) |
| Semantic — Whole | `{{ sem_whole_report_path }}` (`audit/semantic/document/10-feature-technical.md`) |
| Semantic — Section | `{{ sem_section_report_path }}` (`audit/semantic/section/10-feature-technical/*.md`) |

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
| Domain | feature-technical |
| Standard | documentation-standards |
| Document | {{ document_path }} |
| Auditor | System (deterministic engine) + LLM ({{ model_name }}) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
| Reports | 4 detail + 1 summary |
