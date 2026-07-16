# Audit Summary — Security

**Document:** {{ document_path }}
**Standard:** `documentation-standards/03-security-standards.md`
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

### Deterministic — Whole (`audit/deterministic/document/03-security.yaml`)

| Category | Score | Previous | Trend |
|---|---:|---:|---|
| Collection Completeness | {{ categories.collection_completeness.score }} / 100 | {{ categories.collection_completeness.previous_score | default('—') }} | {{ categories.collection_completeness.trend_display }} |
| Modularity | {{ categories.modularity.score }} / 100 | {{ categories.modularity.previous_score | default('—') }} | {{ categories.modularity.trend_display }} |
| Technology Independence | {{ categories.technology_independence.score }} / 100 | {{ categories.technology_independence.previous_score | default('—') }} | {{ categories.technology_independence.trend_display }} |
| Cross-References | {{ categories.cross_references.score }} / 100 | {{ categories.cross_references.previous_score | default('—') }} | {{ categories.cross_references.trend_display }} |
| Duplicate Content | {{ categories.duplicate_content.score }} / 100 | {{ categories.duplicate_content.previous_score | default('—') }} | {{ categories.duplicate_content.trend_display }} |

### Semantic — Whole (`audit/semantic/document/03-security.md`)

| Criterion | Result | Previous | Trend |
|---|---|---|---|
| C1 — Cross-section consistency | {{ doc_semantic.c1_display }} | {{ doc_semantic.c1_previous_display | default('—') }} | {{ doc_semantic.c1_trend_display }} |
| C2 — Data class/Protection alignment | {{ doc_semantic.c2_display }} | {{ doc_semantic.c2_previous_display | default('—') }} | {{ doc_semantic.c2_trend_display }} |
| C3 — Terminology consistency | {{ doc_semantic.c3_display }} | {{ doc_semantic.c3_previous_display | default('—') }} | {{ doc_semantic.c3_trend_display }} |

Full detail, including per-rule/per-criterion evidence: see the Deterministic — Whole and Semantic — Whole reports linked below.

## Section-Level Breakdown

Same reasoning as above, extended per section: a section's deterministic score and its semantic score aren't guaranteed to check the same things (a section can be structurally complete but semantically weak, or vice versa) — two separate tables, not one merged table with a false row-by-row correspondence.

### Deterministic — Section (`audit/deterministic/section/03-security/*.yaml`)

| # | Section | Required | Score | Previous | Trend |
|---:|---|:---:|---:|---:|---|
| 1 | Threat Model | **required** | {{ sections.threat_model.det_score }} / 100 | {{ sections.threat_model.det_previous_score | default('—') }} | {{ sections.threat_model.det_trend_display }} |
| 2 | Data Classification | **required** | {{ sections.data_classification.det_score }} / 100 | {{ sections.data_classification.det_previous_score | default('—') }} | {{ sections.data_classification.det_trend_display }} |
| 3 | Security Principles | **required** | {{ sections.security_principles.det_score }} / 100 | {{ sections.security_principles.det_previous_score | default('—') }} | {{ sections.security_principles.det_trend_display }} |
| 4 | Purpose | **required** | {{ sections.purpose.det_score }} / 100 | {{ sections.purpose.det_previous_score | default('—') }} | {{ sections.purpose.det_trend_display }} |
| 5 | Constraints | **required** | {{ sections.constraints.det_score }} / 100 | {{ sections.constraints.det_previous_score | default('—') }} | {{ sections.constraints.det_trend_display }} |
| 6 | Traceability | **required** | {{ sections.traceability.det_score }} / 100 | {{ sections.traceability.det_previous_score | default('—') }} | {{ sections.traceability.det_trend_display }} |
| 7 | Compliance | optional | {{ sections.compliance.det_score }} / 100 | {{ sections.compliance.det_previous_score | default('—') }} | {{ sections.compliance.det_trend_display }} |
| 8 | Incident Response | optional | {{ sections.incident_response.det_score }} / 100 | {{ sections.incident_response.det_previous_score | default('—') }} | {{ sections.incident_response.det_trend_display }} |

### Semantic — Section (`audit/semantic/section/03-security/*.md`)

| # | Section | Required | Score | Previous | Trend |
|---:|---|:---:|---:|---:|---|
| 1 | Threat Model | **required** | {{ sections.threat_model.sem_score }} / 100 | {{ sections.threat_model.sem_previous_score | default('—') }} | {{ sections.threat_model.sem_trend_display }} |
| 2 | Data Classification | **required** | {{ sections.data_classification.sem_score }} / 100 | {{ sections.data_classification.sem_previous_score | default('—') }} | {{ sections.data_classification.sem_trend_display }} |
| 3 | Security Principles | **required** | {{ sections.security_principles.sem_score }} / 100 | {{ sections.security_principles.sem_previous_score | default('—') }} | {{ sections.security_principles.sem_trend_display }} |
| 4 | Purpose | **required** | {{ sections.purpose.sem_score }} / 100 | {{ sections.purpose.sem_previous_score | default('—') }} | {{ sections.purpose.sem_trend_display }} |
| 5 | Constraints | **required** | {{ sections.constraints.sem_score }} / 100 | {{ sections.constraints.sem_previous_score | default('—') }} | {{ sections.constraints.sem_trend_display }} |
| 6 | Traceability | **required** | {{ sections.traceability.sem_score }} / 100 | {{ sections.traceability.sem_previous_score | default('—') }} | {{ sections.traceability.sem_trend_display }} |
| 7 | Compliance | optional | {{ sections.compliance.sem_score }} / 100 | {{ sections.compliance.sem_previous_score | default('—') }} | {{ sections.compliance.sem_trend_display }} |
| 8 | Incident Response | optional | {{ sections.incident_response.sem_score }} / 100 | {{ sections.incident_response.sem_previous_score | default('—') }} | {{ sections.incident_response.sem_trend_display }} |

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
| Deterministic — Whole | `{{ det_whole_report_path }}` (`audit/deterministic/document/03-security.yaml`) |
| Deterministic — Section | `{{ det_section_report_path }}` (`audit/deterministic/section/03-security/*.yaml`) |
| Semantic — Whole | `{{ sem_whole_report_path }}` (`audit/semantic/document/03-security.md`) |
| Semantic — Section | `{{ sem_section_report_path }}` (`audit/semantic/section/03-security/*.md`) |

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
| Domain | security |
| Standard | documentation-standards |
| Document | {{ document_path }} |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
| Reports | 4 detail + 1 summary |
