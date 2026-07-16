# Semantic Section Report â€” Vision

**Document:** {{ document_path }}
**Standard:** `documentation-standards/01-vision-standards.md`
**Rubric Files:** `audit/semantic/section/01-vision/*.md`
**Auditor:** LLM ({{ model_name }})
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Semantic Section Score: {{ score }} / 100**
{% if previous_score %}({{ 'â†‘ Improved' if score > previous_score else 'â†“ Regressed' if score < previous_score else 'â†’ Unchanged' }} vs. previous run){% else %}(baseline â€” first audit of this document){% endif %}

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

{% if not previous_score %}No prior runs â€” this revision is the baseline every future run is compared against.{% endif %}

### Score by Model

| Model | Runs | Avg Score | Min | Max |
|---|---:|---:|---:|---|
{% for m in model_scores -%}
| {{ m.model_name }} | {{ m.run_count }} | {{ m.avg_score }} / 100 | {{ m.min_score }} / 100 | {{ m.max_score }} / 100 |
{% endfor %}

### Section Scores

| # | Section | Required | Score | Previous | Trend |
|---:|---|:---:|---:|---:|---|
| 1 | Purpose | **required** | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('â€”') }} | {{ sections.purpose.trend_display }} |
| 2 | Vision Statement | **required** | {{ sections.vision_statement.score }} / 100 | {{ sections.vision_statement.previous_score | default('â€”') }} | {{ sections.vision_statement.trend_display }} |
| 3 | Problem | **required** | {{ sections.problem.score }} / 100 | {{ sections.problem.previous_score | default('â€”') }} | {{ sections.problem.trend_display }} |
| 4 | Solution | **required** | {{ sections.solution.score }} / 100 | {{ sections.solution.previous_score | default('â€”') }} | {{ sections.solution.trend_display }} |
| 5 | Target Audience | **required** | {{ sections.target_audience.score }} / 100 | {{ sections.target_audience.previous_score | default('â€”') }} | {{ sections.target_audience.trend_display }} |
| 6 | Pillars | optional | {{ sections.pillars.score }} / 100 | {{ sections.pillars.previous_score | default('â€”') }} | {{ sections.pillars.trend_display }} |
| 7 | Philosophy | optional | {{ sections.philosophy.score }} / 100 | {{ sections.philosophy.previous_score | default('â€”') }} | {{ sections.philosophy.trend_display }} |
| 8 | Guiding Principles | optional | {{ sections.guiding_principles.score }} / 100 | {{ sections.guiding_principles.previous_score | default('â€”') }} | {{ sections.guiding_principles.trend_display }} |
| 9 | Success Criteria | optional | {{ sections.success_criteria.score }} / 100 | {{ sections.success_criteria.previous_score | default('â€”') }} | {{ sections.success_criteria.trend_display }} |
| 10 | Traceability | optional | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('â€”') }} | {{ sections.traceability.trend_display }} |
| â€” | Generic (unmatched sections) | n/a | {{ sections.generic.score }} / 100 | {{ sections.generic.previous_score | default('â€”') }} | {{ sections.generic.trend_display }} |

A section absent from the document (among the optional ones) isn't scored at all here â€” it's a deterministic presence check, not a semantic quality judgment on nothing.

---

## 1. Purpose â€” `section/01-vision/01-purpose.md` â€” **required**

**Why this matters:** Purpose defines why Vision Documentation exists before they read a single direction statement. A Purpose section that's missing, vague, or technology-leaking undermines every section that follows it.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['purpose.C1'].previous_passed_display | default('â€”') }} | {{ results['purpose.C1'].passed_display }} | {{ results['purpose.C1'].trend_display }} | {{ results['purpose.C1'].evidence.excerpt | default('â€”') }} |
| C2 | mandatory | 30 | {{ results['purpose.C2'].previous_passed_display | default('â€”') }} | {{ results['purpose.C2'].passed_display }} | {{ results['purpose.C2'].trend_display }} | {{ results['purpose.C2'].evidence.excerpt | default('â€”') }} |
| C3 | recommended | 30 | {{ results['purpose.C3'].previous_passed_display | default('â€”') }} | {{ results['purpose.C3'].passed_display }} | {{ results['purpose.C3'].trend_display }} | {{ results['purpose.C3'].evidence.excerpt | default('â€”') }} |

C1: purpose is clearly stated with scope boundaries. C2: primary vision goals and their priorities are defined. C3: purpose is consistent with requirements and downstream sections.

## 2. Vision Statement â€” `02-vision_statement.md` â€” **required**

**Why this matters:** Vision Statement is the core aspirational statement â€” where the product is going. A vague or technology-leaking vision gives Philosophy and Feature nothing concrete to derive against.

**Section Score: {{ sections.vision_statement.score }} / 100** ({{ sections.vision_statement.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['vision_statement.C1'].previous_passed_display | default('â€”') }} | {{ results['vision_statement.C1'].passed_display }} | {{ results['vision_statement.C1'].trend_display }} | {{ results['vision_statement.C1'].evidence.excerpt | default('â€”') }} |
| C2 | mandatory | 30 | {{ results['vision_statement.C2'].previous_passed_display | default('â€”') }} | {{ results['vision_statement.C2'].passed_display }} | {{ results['vision_statement.C2'].trend_display }} | {{ results['vision_statement.C2'].evidence.excerpt | default('â€”') }} |
| C3 | recommended | 30 | {{ results['vision_statement.C3'].previous_passed_display | default('â€”') }} | {{ results['vision_statement.C3'].passed_display }} | {{ results['vision_statement.C3'].trend_display }} | {{ results['vision_statement.C3'].evidence.excerpt | default('â€”') }} |

C1: vision describes a future state in 1-3 sentences. C2: free of implementation-specific language. C3: differentiates from current status quo or alternatives.

## 3. Problem â€” `03-problem.md` â€” **required**

**Why this matters:** Problem is what motivates the entire vision. A section that mixes problem and solution gives Philosophy and Feature no clean handoff.

**Section Score: {{ sections.problem.score }} / 100** ({{ sections.problem.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['problem.C1'].previous_passed_display | default('â€”') }} | {{ results['problem.C1'].passed_display }} | {{ results['problem.C1'].trend_display }} | {{ results['problem.C1'].evidence.excerpt | default('â€”') }} |
| C2 | mandatory | 30 | {{ results['problem.C2'].previous_passed_display | default('â€”') }} | {{ results['problem.C2'].passed_display }} | {{ results['problem.C2'].trend_display }} | {{ results['problem.C2'].evidence.excerpt | default('â€”') }} |
| C3 | recommended | 30 | {{ results['problem.C3'].previous_passed_display | default('â€”') }} | {{ results['problem.C3'].passed_display }} | {{ results['problem.C3'].trend_display }} | {{ results['problem.C3'].evidence.excerpt | default('â€”') }} |

C1: problem stated from user/stakeholder perspective with evidence. C2: affected parties identified and scope bounded. C3: current workarounds or alternatives acknowledged.

## 4. Solution â€” `04-solution.md` â€” **required**

**Why this matters:** Solution is the aspirational approach â€” what the product will do, not how. A section that leaks into implementation details crosses into Architecture's territory.

**Section Score: {{ sections.solution.score }} / 100** ({{ sections.solution.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['solution.C1'].previous_passed_display | default('â€”') }} | {{ results['solution.C1'].passed_display }} | {{ results['solution.C1'].trend_display }} | {{ results['solution.C1'].evidence.excerpt | default('â€”') }} |
| C2 | mandatory | 30 | {{ results['solution.C2'].previous_passed_display | default('â€”') }} | {{ results['solution.C2'].passed_display }} | {{ results['solution.C2'].trend_display }} | {{ results['solution.C2'].evidence.excerpt | default('â€”') }} |
| C3 | recommended | 30 | {{ results['solution.C3'].previous_passed_display | default('â€”') }} | {{ results['solution.C3'].passed_display }} | {{ results['solution.C3'].trend_display }} | {{ results['solution.C3'].evidence.excerpt | default('â€”') }} |

C1: solution addresses all aspects of the stated problem. C2: described at capability level without technology prescription. C3: constraints and feasibility considerations acknowledged.

## 5. Target Audience â€” `05-target_audience.md` â€” **required**

**Why this matters:** Target Audience tells Philosophy who the product serves. A missing or vague audience section gives Philosophy nothing to reason about.

**Section Score: {{ sections.target_audience.score }} / 100** ({{ sections.target_audience.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['target_audience.C1'].previous_passed_display | default('â€”') }} | {{ results['target_audience.C1'].passed_display }} | {{ results['target_audience.C1'].trend_display }} | {{ results['target_audience.C1'].evidence.excerpt | default('â€”') }} |
| C2 | mandatory | 30 | {{ results['target_audience.C2'].previous_passed_display | default('â€”') }} | {{ results['target_audience.C2'].passed_display }} | {{ results['target_audience.C2'].trend_display }} | {{ results['target_audience.C2'].evidence.excerpt | default('â€”') }} |
| C3 | recommended | 30 | {{ results['target_audience.C3'].previous_passed_display | default('â€”') }} | {{ results['target_audience.C3'].passed_display }} | {{ results['target_audience.C3'].trend_display }} | {{ results['target_audience.C3'].evidence.excerpt | default('â€”') }} |

C1: section exists with substantive project-specific content. C2: internally consistent, does not contradict other sections. C3: includes concrete examples or project-specific detail.

## 6. Pillars â€” `06-pillars.md` â€” optional

**Why this matters:** Pillars distill the vision into core values that guide every downstream decision. A document without them gives Philosophy no explicit anchor.

**Section Score: {{ sections.pillars.score }} / 100** ({{ sections.pillars.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['pillars.C1'].previous_passed_display | default('â€”') }} | {{ results['pillars.C1'].passed_display }} | {{ results['pillars.C1'].trend_display }} | {{ results['pillars.C1'].evidence.excerpt | default('â€”') }} |
| C2 | mandatory | 30 | {{ results['pillars.C2'].previous_passed_display | default('â€”') }} | {{ results['pillars.C2'].passed_display }} | {{ results['pillars.C2'].trend_display }} | {{ results['pillars.C2'].evidence.excerpt | default('â€”') }} |
| C3 | recommended | 30 | {{ results['pillars.C3'].previous_passed_display | default('â€”') }} | {{ results['pillars.C3'].passed_display }} | {{ results['pillars.C3'].trend_display }} | {{ results['pillars.C3'].evidence.excerpt | default('â€”') }} |

C1: section exists with substantive project-specific content. C2: internally consistent, does not contradict other sections. C3: includes concrete examples or project-specific detail.

## 7. Philosophy â€” `07-philosophy.md` â€” optional

**Why this matters:** Philosophy in Vision is a preview of what the dedicated Philosophy document will expand. Its absence means the vision has no explicit values layer.

**Section Score: {{ sections.philosophy.score }} / 100** ({{ sections.philosophy.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['philosophy.C1'].previous_passed_display | default('â€”') }} | {{ results['philosophy.C1'].passed_display }} | {{ results['philosophy.C1'].trend_display }} | {{ results['philosophy.C1'].evidence.excerpt | default('â€”') }} |
| C2 | mandatory | 30 | {{ results['philosophy.C2'].previous_passed_display | default('â€”') }} | {{ results['philosophy.C2'].passed_display }} | {{ results['philosophy.C2'].trend_display }} | {{ results['philosophy.C2'].evidence.excerpt | default('â€”') }} |
| C3 | recommended | 30 | {{ results['philosophy.C3'].previous_passed_display | default('â€”') }} | {{ results['philosophy.C3'].passed_display }} | {{ results['philosophy.C3'].trend_display }} | {{ results['philosophy.C3'].evidence.excerpt | default('â€”') }} |

C1: section exists with substantive project-specific content. C2: internally consistent, does not contradict other sections. C3: includes concrete examples or project-specific detail.

## 8. Guiding Principles â€” `08-guiding_principles.md` â€” optional

**Why this matters:** Guiding Principles in Vision are the seeds that Philosophy's Guiding Principles section expands. Without them, Philosophy has no explicit upstream to trace back to.

**Section Score: {{ sections.guiding_principles.score }} / 100** ({{ sections.guiding_principles.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['guiding_principles.C1'].previous_passed_display | default('â€”') }} | {{ results['guiding_principles.C1'].passed_display }} | {{ results['guiding_principles.C1'].trend_display }} | {{ results['guiding_principles.C1'].evidence.excerpt | default('â€”') }} |
| C2 | mandatory | 30 | {{ results['guiding_principles.C2'].previous_passed_display | default('â€”') }} | {{ results['guiding_principles.C2'].passed_display }} | {{ results['guiding_principles.C2'].trend_display }} | {{ results['guiding_principles.C2'].evidence.excerpt | default('â€”') }} |
| C3 | recommended | 30 | {{ results['guiding_principles.C3'].previous_passed_display | default('â€”') }} | {{ results['guiding_principles.C3'].passed_display }} | {{ results['guiding_principles.C3'].trend_display }} | {{ results['guiding_principles.C3'].evidence.excerpt | default('â€”') }} |

C1: section exists with substantive project-specific content. C2: internally consistent, does not contradict other sections. C3: includes concrete examples or project-specific detail.

## 9. Success Criteria â€” `09-success_criteria.md` â€” optional

**Why this matters:** Success Criteria in Vision are the seeds that Feature's Acceptance Criteria section expands. Without them, Feature has no explicit upstream success definition to trace.

**Section Score: {{ sections.success_criteria.score }} / 100** ({{ sections.success_criteria.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['success_criteria.C1'].previous_passed_display | default('â€”') }} | {{ results['success_criteria.C1'].passed_display }} | {{ results['success_criteria.C1'].trend_display }} | {{ results['success_criteria.C1'].evidence.excerpt | default('â€”') }} |
| C2 | mandatory | 30 | {{ results['success_criteria.C2'].previous_passed_display | default('â€”') }} | {{ results['success_criteria.C2'].passed_display }} | {{ results['success_criteria.C2'].trend_display }} | {{ results['success_criteria.C2'].evidence.excerpt | default('â€”') }} |
| C3 | recommended | 30 | {{ results['success_criteria.C3'].previous_passed_display | default('â€”') }} | {{ results['success_criteria.C3'].passed_display }} | {{ results['success_criteria.C3'].trend_display }} | {{ results['success_criteria.C3'].evidence.excerpt | default('â€”') }} |

C1: criteria are specific, measurable, and include clear targets. C2: span multiple dimensions (user, business, technical). C3: include timeframes and distinguish leading vs lagging indicators.

## 10. Traceability â€” `10-traceability.md` â€” optional

**Why this matters:** Traceability is what makes the derivation chain enforceable â€” without it, nothing stops a downstream domain from silently drifting away from what Vision actually says.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['traceability.C1'].previous_passed_display | default('â€”') }} | {{ results['traceability.C1'].passed_display }} | {{ results['traceability.C1'].trend_display }} | {{ results['traceability.C1'].evidence.excerpt | default('â€”') }} |
| C2 | mandatory | 30 | {{ results['traceability.C2'].previous_passed_display | default('â€”') }} | {{ results['traceability.C2'].passed_display }} | {{ results['traceability.C2'].trend_display }} | {{ results['traceability.C2'].evidence.excerpt | default('â€”') }} |
| C3 | recommended | 30 | {{ results['traceability.C3'].previous_passed_display | default('â€”') }} | {{ results['traceability.C3'].passed_display }} | {{ results['traceability.C3'].trend_display }} | {{ results['traceability.C3'].evidence.excerpt | default('â€”') }} |

C1: traceability links to upstream origins are present. C2: links to downstream consumers are present. C3: no contradictory or unresolvable links.

## Generic â€” `generic.md` (sections with no matching semantic_type)

**Why this matters:** Catches vision-relevant content an author wrote under a heading that doesn't match any of the 10 named section types above â€” still judged for relevance and non-duplication, not given a free pass for being unclassified.

**Section Score: {{ sections.generic.score }} / 100** ({{ sections.generic.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['generic.C1'].previous_passed_display | default('â€”') }} | {{ results['generic.C1'].passed_display }} | {{ results['generic.C1'].trend_display }} | {{ results['generic.C1'].evidence.excerpt | default('â€”') }} |
| C2 | mandatory | 30 | {{ results['generic.C2'].previous_passed_display | default('â€”') }} | {{ results['generic.C2'].passed_display }} | {{ results['generic.C2'].trend_display }} | {{ results['generic.C2'].evidence.excerpt | default('â€”') }} |
| C3 | recommended | 30 | {{ results['generic.C3'].previous_passed_display | default('â€”') }} | {{ results['generic.C3'].passed_display }} | {{ results['generic.C3'].trend_display }} | {{ results['generic.C3'].evidence.excerpt | default('â€”') }} |

C1: content is vision-relevant, not implementation-specific. C2: claims and assertions are justified by evidence or reasoning. C3: no duplication of content from other vision section types.

---

## All Findings

{% if findings | length > 0 %}
| Section | Criterion | Severity | Evidence | Message | New This Run? |
|---|---|---|---|---|---|
{% for f in findings -%}
| {{ f.section_type }} | {{ f.criterion_id }} | {{ f.severity }} | {{ f.evidence.excerpt | default('â€”') }} | {{ f.message }} | {{ 'Yes â€” regression' if f.is_new_finding else 'No â€” carried over' }} |
{% endfor %}
{% else %}
No findings.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | vision |
| Standard | documentation-standards |
| Section Rubric Files | `audit/semantic/section/01-vision/*.md` |
| Auditor | LLM ({{ model_name }}) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
