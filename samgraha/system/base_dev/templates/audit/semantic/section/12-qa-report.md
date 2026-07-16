# Semantic Section Report — QA

**Document:** {{ document_path }}
**Standard:** `documentation-standards/12-qa-standards.md`
**Rubric Files:** `audit/semantic/section/12-qa/*.md`
**Auditor:** LLM ({{ model_name }})
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Semantic Section Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
overall = average of the section scores below, for sections actually present in the document
section_score = sum of passed criterion points in that section, capped at 100
# calculation: semantic_section_v1
```

### Score History

| Revision | Date | Score | vs. Previous | vs. Baseline |
|---:|---|---:|---|---|
{% for r in revision_history -%}
| {{ r.revision }} | {{ r.date }} | {{ r.score }} / 100 | {{ r.delta_previous_display }} | {{ r.delta_baseline_display }} |
{% endfor -%}
| {{ revision_number }} (current) | {{ created_at }} | {{ score }} / 100 | {{ delta_previous_display }} | {{ delta_baseline_display }} |

{% if not previous_score %}No prior runs — this revision is the baseline every future run is compared against.{% endif %}

### Score by Model

| Model | Runs | Avg Score | Min | Max |
|---|---:|---:|---:|---|
{% for m in model_scores -%}
| {{ m.model_name }} | {{ m.run_count }} | {{ m.avg_score }} / 100 | {{ m.min_score }} / 100 | {{ m.max_score }} / 100 |
{% endfor %}

### Section Scores

| # | Section | Required | Score | Previous | Trend |
|---:|---|:---:|---:|---:|---|
| 1 | Test Strategy | **required** | {{ sections.test_strategy.score }} / 100 | {{ sections.test_strategy.previous_score | default('—') }} | {{ sections.test_strategy.trend_display }} |
| 2 | Unit Testing | **required** | {{ sections.unit_testing.score }} / 100 | {{ sections.unit_testing.previous_score | default('—') }} | {{ sections.unit_testing.trend_display }} |
| 3 | Integration Testing | **required** | {{ sections.integration_testing.score }} / 100 | {{ sections.integration_testing.previous_score | default('—') }} | {{ sections.integration_testing.trend_display }} |
| 4 | Security Testing | **required** | {{ sections.security_testing.score }} / 100 | {{ sections.security_testing.previous_score | default('—') }} | {{ sections.security_testing.trend_display }} |
| 5 | Purpose | optional | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 6 | E2E Testing | **required** | {{ sections.e2e_testing.score }} / 100 | {{ sections.e2e_testing.previous_score | default('—') }} | {{ sections.e2e_testing.trend_display }} |
| 7 | Smoke Testing | **required** | {{ sections.smoke_testing.score }} / 100 | {{ sections.smoke_testing.previous_score | default('—') }} | {{ sections.smoke_testing.trend_display }} |
| 8 | Load Testing | **required** | {{ sections.load_testing.score }} / 100 | {{ sections.load_testing.previous_score | default('—') }} | {{ sections.load_testing.trend_display }} |
| 9 | Scalability Testing | **required** | {{ sections.scalability_testing.score }} / 100 | {{ sections.scalability_testing.previous_score | default('—') }} | {{ sections.scalability_testing.trend_display }} |
| — | Generic (unmatched sections) | n/a | {{ sections.generic.score }} / 100 | {{ sections.generic.previous_score | default('—') }} | {{ sections.generic.trend_display }} |

A section absent from the document (among the optional ones) isn't scored at all here — it's a deterministic presence check, not a semantic quality judgment on nothing.

---

## 1. Test Strategy — `section/12-qa/01-test_strategy.md` — **required**

**Why this matters:** Test Strategy defines the overall testing philosophy and approach that every other test type section derives from. A missing or vague strategy gives the individual test sections no coherence.

**Section Score: {{ sections.test_strategy.score }} / 100** ({{ sections.test_strategy.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['test_strategy.C1'].previous_passed_display | default('—') }} | {{ results['test_strategy.C1'].passed_display }} | {{ results['test_strategy.C1'].trend_display }} | {{ results['test_strategy.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['test_strategy.C2'].previous_passed_display | default('—') }} | {{ results['test_strategy.C2'].passed_display }} | {{ results['test_strategy.C2'].trend_display }} | {{ results['test_strategy.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['test_strategy.C3'].previous_passed_display | default('—') }} | {{ results['test_strategy.C3'].passed_display }} | {{ results['test_strategy.C3'].trend_display }} | {{ results['test_strategy.C3'].evidence.excerpt | default('—') }} |

C1: section exists with substantive content specific to this project. C2: internally consistent, does not contradict other sections. C3: includes concrete examples, evidence, or project-specific detail.

## 2. Unit Testing — `02-unit_testing.md` — **required**

**Why this matters:** Unit Testing is the foundation of the test pyramid. A section that's missing or generic gives developers no guidance on how to structure their tests or what coverage is expected.

**Section Score: {{ sections.unit_testing.score }} / 100** ({{ sections.unit_testing.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['unit_testing.C1'].previous_passed_display | default('—') }} | {{ results['unit_testing.C1'].passed_display }} | {{ results['unit_testing.C1'].trend_display }} | {{ results['unit_testing.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['unit_testing.C2'].previous_passed_display | default('—') }} | {{ results['unit_testing.C2'].passed_display }} | {{ results['unit_testing.C2'].trend_display }} | {{ results['unit_testing.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['unit_testing.C3'].previous_passed_display | default('—') }} | {{ results['unit_testing.C3'].passed_display }} | {{ results['unit_testing.C3'].trend_display }} | {{ results['unit_testing.C3'].evidence.excerpt | default('—') }} |

C1: section exists with substantive content specific to this project. C2: internally consistent, does not contradict other sections. C3: includes concrete examples, evidence, or project-specific detail.

## 3. Integration Testing — `03-integration_testing.md` — **required**

**Why this matters:** Integration Testing verifies component boundaries work as designed. Without it, individual units may pass in isolation while the system fails at every seam.

**Section Score: {{ sections.integration_testing.score }} / 100** ({{ sections.integration_testing.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['integration_testing.C1'].previous_passed_display | default('—') }} | {{ results['integration_testing.C1'].passed_display }} | {{ results['integration_testing.C1'].trend_display }} | {{ results['integration_testing.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['integration_testing.C2'].previous_passed_display | default('—') }} | {{ results['integration_testing.C2'].passed_display }} | {{ results['integration_testing.C2'].trend_display }} | {{ results['integration_testing.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['integration_testing.C3'].previous_passed_display | default('—') }} | {{ results['integration_testing.C3'].passed_display }} | {{ results['integration_testing.C3'].trend_display }} | {{ results['integration_testing.C3'].evidence.excerpt | default('—') }} |

C1: section exists with substantive content specific to this project. C2: internally consistent, does not contradict other sections. C3: includes concrete examples, evidence, or project-specific detail.

## 4. Security Testing — `04-security_testing.md` — **required**

**Why this matters:** Security Testing ensures threats are validated against, not just documented. A missing or shallow section means the Security domain's threat model goes untested.

**Section Score: {{ sections.security_testing.score }} / 100** ({{ sections.security_testing.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['security_testing.C1'].previous_passed_display | default('—') }} | {{ results['security_testing.C1'].passed_display }} | {{ results['security_testing.C1'].trend_display }} | {{ results['security_testing.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['security_testing.C2'].previous_passed_display | default('—') }} | {{ results['security_testing.C2'].passed_display }} | {{ results['security_testing.C2'].trend_display }} | {{ results['security_testing.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['security_testing.C3'].previous_passed_display | default('—') }} | {{ results['security_testing.C3'].passed_display }} | {{ results['security_testing.C3'].trend_display }} | {{ results['security_testing.C3'].evidence.excerpt | default('—') }} |

C1: section exists with substantive content specific to this project. C2: internally consistent, does not contradict other sections. C3: includes concrete examples, evidence, or project-specific detail.

## 5. Purpose — `05-purpose.md` — optional

**Why this matters:** Purpose defines why QA Documentation exists before a reader examines a single test type. A missing Purpose section means readers must infer the document's intent from its content.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['purpose.C1'].previous_passed_display | default('—') }} | {{ results['purpose.C1'].passed_display }} | {{ results['purpose.C1'].trend_display }} | {{ results['purpose.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['purpose.C2'].previous_passed_display | default('—') }} | {{ results['purpose.C2'].passed_display }} | {{ results['purpose.C2'].trend_display }} | {{ results['purpose.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['purpose.C3'].previous_passed_display | default('—') }} | {{ results['purpose.C3'].passed_display }} | {{ results['purpose.C3'].trend_display }} | {{ results['purpose.C3'].evidence.excerpt | default('—') }} |

C1: section exists with substantive content specific to this project. C2: internally consistent, does not contradict other sections. C3: includes concrete examples, evidence, or project-specific detail.

## 6. E2E Testing — `06-e2e_testing.md` — **required**

**Why this matters:** E2E Testing verifies critical user journeys work through the full system. It catches integration failures that unit and integration tests, scoped to individual components, can't see.

**Section Score: {{ sections.e2e_testing.score }} / 100** ({{ sections.e2e_testing.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 35 | {{ results['e2e_testing.C1'].previous_passed_display | default('—') }} | {{ results['e2e_testing.C1'].passed_display }} | {{ results['e2e_testing.C1'].trend_display }} | {{ results['e2e_testing.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 35 | {{ results['e2e_testing.C2'].previous_passed_display | default('—') }} | {{ results['e2e_testing.C2'].passed_display }} | {{ results['e2e_testing.C2'].trend_display }} | {{ results['e2e_testing.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['e2e_testing.C3'].previous_passed_display | default('—') }} | {{ results['e2e_testing.C3'].passed_display }} | {{ results['e2e_testing.C3'].trend_display }} | {{ results['e2e_testing.C3'].evidence.excerpt | default('—') }} |

C1: critical user journeys named specifically, not "test the app". C2: expected outcomes and acceptance criteria stated per journey. C3: journeys map to Design(06)'s documented workflows.

## 7. Smoke Testing — `07-smoke_testing.md` — **required**

**Why this matters:** Smoke Testing is a fast, minimal check that the core system is functioning after a deploy — not full verification, just "is it alive and basically working."

**Section Score: {{ sections.smoke_testing.score }} / 100** ({{ sections.smoke_testing.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['smoke_testing.C1'].previous_passed_display | default('—') }} | {{ results['smoke_testing.C1'].passed_display }} | {{ results['smoke_testing.C1'].trend_display }} | {{ results['smoke_testing.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['smoke_testing.C2'].previous_passed_display | default('—') }} | {{ results['smoke_testing.C2'].passed_display }} | {{ results['smoke_testing.C2'].trend_display }} | {{ results['smoke_testing.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['smoke_testing.C3'].previous_passed_display | default('—') }} | {{ results['smoke_testing.C3'].passed_display }} | {{ results['smoke_testing.C3'].trend_display }} | {{ results['smoke_testing.C3'].evidence.excerpt | default('—') }} |

C1: core function scope defined narrowly and explicitly. C2: pass/fail criteria stated explicitly. C3: execution timing and maximum duration threshold specified.

## 8. Load Testing — `08-load_testing.md` — **required**

**Why this matters:** Load Testing verifies the system behaves acceptably under expected and peak traffic. Performance targets are validated against a defined load profile, not assumed from production experience.

**Section Score: {{ sections.load_testing.score }} / 100** ({{ sections.load_testing.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['load_testing.C1'].previous_passed_display | default('—') }} | {{ results['load_testing.C1'].passed_display }} | {{ results['load_testing.C1'].trend_display }} | {{ results['load_testing.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['load_testing.C2'].previous_passed_display | default('—') }} | {{ results['load_testing.C2'].passed_display }} | {{ results['load_testing.C2'].trend_display }} | {{ results['load_testing.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['load_testing.C3'].previous_passed_display | default('—') }} | {{ results['load_testing.C3'].passed_display }} | {{ results['load_testing.C3'].trend_display }} | {{ results['load_testing.C3'].evidence.excerpt | default('—') }} |

C1: load profiles defined with concrete numbers (expected, peak, stress). C2: performance targets stated per profile (latency, throughput). C3: acceptable degradation thresholds specified.

## 9. Scalability Testing — `09-scalability_testing.md` — **required**

**Why this matters:** Scalability Testing characterizes how the system behaves as load grows well beyond current levels — where it breaks and how it degrades. Unlike Load Testing, it explores the growth curve itself.

**Section Score: {{ sections.scalability_testing.score }} / 100** ({{ sections.scalability_testing.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 35 | {{ results['scalability_testing.C1'].previous_passed_display | default('—') }} | {{ results['scalability_testing.C1'].passed_display }} | {{ results['scalability_testing.C1'].trend_display }} | {{ results['scalability_testing.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 35 | {{ results['scalability_testing.C2'].previous_passed_display | default('—') }} | {{ results['scalability_testing.C2'].passed_display }} | {{ results['scalability_testing.C2'].trend_display }} | {{ results['scalability_testing.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['scalability_testing.C3'].previous_passed_display | default('—') }} | {{ results['scalability_testing.C3'].passed_display }} | {{ results['scalability_testing.C3'].trend_display }} | {{ results['scalability_testing.C3'].evidence.excerpt | default('—') }} |

C1: growth scenarios defined as concrete multiples of baseline (2x, 5x, 10x). C2: breaking points identified with specific thresholds. C3: scaling behavior characterized (linear/sub-linear/cliff).

## Generic — `generic.md` (sections with no matching semantic_type)

**Why this matters:** Catches QA-relevant content an author wrote under a heading that doesn't match any of the 9 named section types above — still judged for relevance and non-duplication, not given a free pass for being unclassified.

**Section Score: {{ sections.generic.score }} / 100** ({{ sections.generic.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['generic.C1'].previous_passed_display | default('—') }} | {{ results['generic.C1'].passed_display }} | {{ results['generic.C1'].trend_display }} | {{ results['generic.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['generic.C2'].previous_passed_display | default('—') }} | {{ results['generic.C2'].passed_display }} | {{ results['generic.C2'].trend_display }} | {{ results['generic.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['generic.C3'].previous_passed_display | default('—') }} | {{ results['generic.C3'].passed_display }} | {{ results['generic.C3'].trend_display }} | {{ results['generic.C3'].evidence.excerpt | default('—') }} |

C1: content is QA-relevant, not implementation-specific. C2: claims and assertions are justified by evidence or reasoning. C3: no duplication of content from other QA section types.

---

## All Findings

{% if findings | length > 0 %}
| Section | Criterion | Severity | Evidence | Message | New This Run? |
|---|---|---|---|---|---|
{% for f in findings -%}
| {{ f.section_type }} | {{ f.criterion_id }} | {{ f.severity }} | {{ f.evidence.excerpt | default('—') }} | {{ f.message }} | {{ 'Yes — regression' if f.is_new_finding else 'No — carried over' }} |
{% endfor %}
{% else %}
No findings.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | qa |
| Standard | documentation-standards |
| Section Rubric Files | `audit/semantic/section/12-qa/*.md` |
| Auditor | LLM ({{ model_name }}) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
