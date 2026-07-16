# Semantic Section Report — Product Guide

**Document:** {{ document_path }}
**Standard:** `documentation-standards/16-product-guide-standards.md`
**Rubric Files:** `audit/semantic/section/16-product-guide/*.md`
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
| 1 | Title | **required** | {{ sections.title.score }} / 100 | {{ sections.title.previous_score | default('—') }} | {{ sections.title.trend_display }} |
| 2 | Body | **required** | {{ sections.body.score }} / 100 | {{ sections.body.previous_score | default('—') }} | {{ sections.body.trend_display }} |
| 3 | Purpose | optional | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 4 | Product Context (early) | optional | {{ sections.product_context_early.score }} / 100 | {{ sections.product_context_early.previous_score | default('—') }} | {{ sections.product_context_early.trend_display }} |
| 5 | Public Contract (early) | optional | {{ sections.public_contract_early.score }} / 100 | {{ sections.public_contract_early.previous_score | default('—') }} | {{ sections.public_contract_early.trend_display }} |
| 6 | Related | optional | {{ sections.related.score }} / 100 | {{ sections.related.previous_score | default('—') }} | {{ sections.related.trend_display }} |
| 7 | Product Context | **required** | {{ sections.product_context.score }} / 100 | {{ sections.product_context.previous_score | default('—') }} | {{ sections.product_context.trend_display }} |
| 8 | Public Contract | **required** | {{ sections.public_contract.score }} / 100 | {{ sections.public_contract.previous_score | default('—') }} | {{ sections.public_contract.trend_display }} |
| — | Generic (unmatched sections) | n/a | {{ sections.generic.score }} / 100 | {{ sections.generic.previous_score | default('—') }} | {{ sections.generic.trend_display }} |

A section absent from the document (among the optional ones) isn't scored at all here — it's a deterministic presence check, not a semantic quality judgment on nothing.

---

## 1. Title — `section/16-product-guide/01-title.md` — **required**

**Why this matters:** Title is the first thing a reader sees — it must accurately describe what this Product Guide covers. A missing or misleading title undermines the entire guide's discoverability.

**Section Score: {{ sections.title.score }} / 100** ({{ sections.title.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['title.C1'].previous_passed_display \| default('—') }} | {{ results['title.C1'].passed_display }} | {{ results['title.C1'].trend_display }} | {{ results['title.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['title.C2'].previous_passed_display \| default('—') }} | {{ results['title.C2'].passed_display }} | {{ results['title.C2'].trend_display }} | {{ results['title.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['title.C3'].previous_passed_display \| default('—') }} | {{ results['title.C3'].passed_display }} | {{ results['title.C3'].trend_display }} | {{ results['title.C3'].evidence.excerpt | default('—') }} |

C1: section exists with substantive project-specific content. C2: internally consistent and does not contradict other sections. C3: includes concrete examples, evidence, or project-specific detail.

## 2. Body — `section/16-product-guide/02-body.md` — **required**

**Why this matters:** Body is the core content — the actual instructions or explanations readers came for. A body that's thin, unstructured, or missing actionable content fails the guide's primary purpose.

**Section Score: {{ sections.body.score }} / 100** ({{ sections.body.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['body.C1'].previous_passed_display \| default('—') }} | {{ results['body.C1'].passed_display }} | {{ results['body.C1'].trend_display }} | {{ results['body.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['body.C2'].previous_passed_display \| default('—') }} | {{ results['body.C2'].passed_display }} | {{ results['body.C2'].trend_display }} | {{ results['body.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['body.C3'].previous_passed_display \| default('—') }} | {{ results['body.C3'].passed_display }} | {{ results['body.C3'].trend_display }} | {{ results['body.C3'].evidence.excerpt | default('—') }} |

C1: section exists with substantive project-specific content. C2: internally consistent and does not contradict other sections. C3: includes concrete examples, evidence, or project-specific detail.

## 3. Purpose — `section/16-product-guide/03-purpose.md` — optional

**Why this matters:** Purpose states why this Product Guide exists and who it's for, giving readers a quick way to assess relevance.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['purpose.C1'].previous_passed_display \| default('—') }} | {{ results['purpose.C1'].passed_display }} | {{ results['purpose.C1'].trend_display }} | {{ results['purpose.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['purpose.C2'].previous_passed_display \| default('—') }} | {{ results['purpose.C2'].passed_display }} | {{ results['purpose.C2'].trend_display }} | {{ results['purpose.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['purpose.C3'].previous_passed_display \| default('—') }} | {{ results['purpose.C3'].passed_display }} | {{ results['purpose.C3'].trend_display }} | {{ results['purpose.C3'].evidence.excerpt | default('—') }} |

C1: section exists with substantive project-specific content. C2: internally consistent and does not contradict other sections. C3: includes concrete examples, evidence, or project-specific detail.

## 4. Product Context (early) — `section/16-product-guide/04-product_context.md` — optional

**Why this matters:** Product Context provides background information about the product and its positioning, grounding the guide in what's actually true.

**Section Score: {{ sections.product_context_early.score }} / 100** ({{ sections.product_context_early.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['product_context_early.C1'].previous_passed_display \| default('—') }} | {{ results['product_context_early.C1'].passed_display }} | {{ results['product_context_early.C1'].trend_display }} | {{ results['product_context_early.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['product_context_early.C2'].previous_passed_display \| default('—') }} | {{ results['product_context_early.C2'].passed_display }} | {{ results['product_context_early.C2'].trend_display }} | {{ results['product_context_early.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['product_context_early.C3'].previous_passed_display \| default('—') }} | {{ results['product_context_early.C3'].passed_display }} | {{ results['product_context_early.C3'].trend_display }} | {{ results['product_context_early.C3'].evidence.excerpt | default('—') }} |

C1: section exists with substantive project-specific content. C2: internally consistent and does not contradict other sections. C3: includes concrete examples, evidence, or project-specific detail.

## 5. Public Contract (early) — `section/16-product-guide/05-public_contract.md` — optional

**Why this matters:** Public Contract defines the public API or interface exposed to users, including stability guarantees.

**Section Score: {{ sections.public_contract_early.score }} / 100** ({{ sections.public_contract_early.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['public_contract_early.C1'].previous_passed_display \| default('—') }} | {{ results['public_contract_early.C1'].passed_display }} | {{ results['public_contract_early.C1'].trend_display }} | {{ results['public_contract_early.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['public_contract_early.C2'].previous_passed_display \| default('—') }} | {{ results['public_contract_early.C2'].passed_display }} | {{ results['public_contract_early.C2'].trend_display }} | {{ results['public_contract_early.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['public_contract_early.C3'].previous_passed_display \| default('—') }} | {{ results['public_contract_early.C3'].passed_display }} | {{ results['public_contract_early.C3'].trend_display }} | {{ results['public_contract_early.C3'].evidence.excerpt | default('—') }} |

C1: section exists with substantive project-specific content. C2: internally consistent and does not contradict other sections. C3: includes concrete examples, evidence, or project-specific detail.

## 6. Related — `section/16-product-guide/06-related.md` — optional

**Why this matters:** Related links connect this guide to adjacent content. Without them, readers can't discover related guides that might be relevant.

**Section Score: {{ sections.related.score }} / 100** ({{ sections.related.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['related.C1'].previous_passed_display \| default('—') }} | {{ results['related.C1'].passed_display }} | {{ results['related.C1'].trend_display }} | {{ results['related.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['related.C2'].previous_passed_display \| default('—') }} | {{ results['related.C2'].passed_display }} | {{ results['related.C2'].trend_display }} | {{ results['related.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['related.C3'].previous_passed_display \| default('—') }} | {{ results['related.C3'].passed_display }} | {{ results['related.C3'].trend_display }} | {{ results['related.C3'].evidence.excerpt | default('—') }} |

C1: section exists with substantive project-specific content. C2: internally consistent and does not contradict other sections. C3: includes concrete examples, evidence, or project-specific detail.

## 7. Product Context — `section/16-product-guide/07-product_context.md` — **required**

**Why this matters:** Product Context states the prerequisites, default behavior, and version-specific context a reader needs before using a feature — grounding the guide in what's actually true for this product version.

**Section Score: {{ sections.product_context.score }} / 100** ({{ sections.product_context.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['product_context.C1'].previous_passed_display \| default('—') }} | {{ results['product_context.C1'].passed_display }} | {{ results['product_context.C1'].trend_display }} | {{ results['product_context.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['product_context.C2'].previous_passed_display \| default('—') }} | {{ results['product_context.C2'].passed_display }} | {{ results['product_context.C2'].trend_display }} | {{ results['product_context.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['product_context.C3'].previous_passed_display \| default('—') }} | {{ results['product_context.C3'].passed_display }} | {{ results['product_context.C3'].trend_display }} | {{ results['product_context.C3'].evidence.excerpt | default('—') }} |

C1: prerequisites explicitly listed. C2: default behavior stated concretely. C3: version-specific context noted where applicable.

## 8. Public Contract — `section/16-product-guide/08-public_contract.md` — **required**

**Why this matters:** Public Contract is the exhaustive reference for every input, output, flag, config key, and error condition. It exists as the ground truth a user checks instead of reading source code.

**Section Score: {{ sections.public_contract.score }} / 100** ({{ sections.public_contract.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 30 | {{ results['public_contract.C1'].previous_passed_display \| default('—') }} | {{ results['public_contract.C1'].passed_display }} | {{ results['public_contract.C1'].trend_display }} | {{ results['public_contract.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['public_contract.C2'].previous_passed_display \| default('—') }} | {{ results['public_contract.C2'].passed_display }} | {{ results['public_contract.C2'].trend_display }} | {{ results['public_contract.C2'].evidence.excerpt | default('—') }} |
| C3 | mandatory | 20 | {{ results['public_contract.C3'].previous_passed_display \| default('—') }} | {{ results['public_contract.C3'].passed_display }} | {{ results['public_contract.C3'].trend_display }} | {{ results['public_contract.C3'].evidence.excerpt | default('—') }} |
| C4 | recommended | 20 | {{ results['public_contract.C4'].previous_passed_display \| default('—') }} | {{ results['public_contract.C4'].passed_display }} | {{ results['public_contract.C4'].trend_display }} | {{ results['public_contract.C4'].evidence.excerpt | default('—') }} |

C1: inputs (CLI/config/API) documented in table form with type, default, required. C2: error conditions present with cause and resolution. C3: outputs documented with type and description. C4: contract matches the actual current interface (no stale/missing entries).

## Generic — `generic.md` (sections with no matching semantic_type)

**Why this matters:** Catches Product Guide-relevant content an author wrote under a heading that doesn't match any of the 8 named section types above — still judged for relevance and non-duplication, not given a free pass for being unclassified.

**Section Score: {{ sections.generic.score }} / 100** ({{ sections.generic.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['generic.C1'].previous_passed_display \| default('—') }} | {{ results['generic.C1'].passed_display }} | {{ results['generic.C1'].trend_display }} | {{ results['generic.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['generic.C2'].previous_passed_display \| default('—') }} | {{ results['generic.C2'].passed_display }} | {{ results['generic.C2'].trend_display }} | {{ results['generic.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['generic.C3'].previous_passed_display \| default('—') }} | {{ results['generic.C3'].passed_display }} | {{ results['generic.C3'].trend_display }} | {{ results['generic.C3'].evidence.excerpt | default('—') }} |

C1: content is Product Guide-relevant, not generic. C2: claims and assertions are justified by evidence or reasoning. C3: no duplication of content from other section types.

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
| Domain | product-guide |
| Standard | documentation-standards |
| Section Rubric Files | `audit/semantic/section/16-product-guide/*.md` |
| Auditor | LLM ({{ model_name }}) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
