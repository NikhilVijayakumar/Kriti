# Deterministic Section Report — Product Guide

**Document:** {{ document_path }}
**Standard:** `documentation-standards/16-product-guide-standards.md`
**Rule Files:** `audit/deterministic/section/16-product-guide/*.yaml`
**Auditor:** System (deterministic engine)
**Audit Date:** {{ created_at }}
**Revision:** {{ revision_number }}

---

## Score

**Deterministic Section Score: {{ score }} / 100**
{% if previous_score %}({{ '↑ Improved' if score > previous_score else '↓ Regressed' if score < previous_score else '→ Unchanged' }} vs. previous run){% else %}(baseline — first audit of this document){% endif %}

```
overall = average of the 8 section scores below
section_score = 100 × (Σ weight of passed rules in that section) / (Σ weight of all rules in that section)
# calculation: deterministic_section_v1
```

### Score History

| Revision | Date | Score | vs. Previous | vs. Baseline |
|---:|---|---:|---|---|
{% for r in revision_history -%}
| {{ r.revision }} | {{ r.date }} | {{ r.score }} / 100 | {{ r.delta_previous_display }} | {{ r.delta_baseline_display }} |
{% endfor -%}
| {{ revision_number }} (current) | {{ created_at }} | {{ score }} / 100 | {{ delta_previous_display }} | {{ delta_baseline_display }} |

{% if not previous_score %}No prior runs — this revision is the baseline every future run is compared against.{% endif %}

### Section Scores

| # | Section | Required | Weight | Score | Previous | Trend |
|---:|---|:---:|---:|---:|---:|---|
| 1 | Title | **required** | 3.0 | {{ sections.title.score }} / 100 | {{ sections.title.previous_score | default('—') }} | {{ sections.title.trend_display }} |
| 2 | Body | **required** | 3.5 | {{ sections.body.score }} / 100 | {{ sections.body.previous_score | default('—') }} | {{ sections.body.trend_display }} |
| 3 | Purpose | optional | 1.5 | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 4 | Product Context (early) | optional | 1.5 | {{ sections.product_context_early.score }} / 100 | {{ sections.product_context_early.previous_score | default('—') }} | {{ sections.product_context_early.trend_display }} |
| 5 | Public Contract (early) | optional | 1.5 | {{ sections.public_contract_early.score }} / 100 | {{ sections.public_contract_early.previous_score | default('—') }} | {{ sections.public_contract_early.trend_display }} |
| 6 | Related | optional | 1.5 | {{ sections.related.score }} / 100 | {{ sections.related.previous_score | default('—') }} | {{ sections.related.trend_display }} |
| 7 | Product Context | **required** | 3.0 | {{ sections.product_context.score }} / 100 | {{ sections.product_context.previous_score | default('—') }} | {{ sections.product_context.trend_display }} |
| 8 | Public Contract | **required** | 3.0 | {{ sections.public_contract.score }} / 100 | {{ sections.public_contract.previous_score | default('—') }} | {{ sections.public_contract.trend_display }} |

The 4 required sections carry 12.5 of the document's 15.5 total rule weight — a document can only pass if those four are both present and internally sound; the remaining four are recommended-quality signal, not gating.

---

## 1. Title — weight 3.0 — **required**

**Why this matters:** Title is what a reader sees first — it must identify the product guide topic accurately. A missing or non-descriptive title gives readers no way to know what the guide covers.

**Section Score: {{ sections.title.score }} / 100** ({{ sections.title.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| pg-sec-title-001 | Title section exists | error (mandatory) | 1.5 | {{ results['pg-sec-title-001'].previous_status \| default('—') }} | {{ results['pg-sec-title-001'].status }} | {{ results['pg-sec-title-001'].trend_display }} | {{ results['pg-sec-title-001'].evidence \| default('—') }} |
| pg-sec-title-002 | Title is descriptive — contains keywords identifying the product guide topic | error (mandatory) | 1.0 | {{ results['pg-sec-title-002'].previous_status \| default('—') }} | {{ results['pg-sec-title-002'].status }} | {{ results['pg-sec-title-002'].trend_display }} | {{ results['pg-sec-title-002'].evidence \| default('—') }} |
| pg-sec-title-003 | Title matches document focus | warning (recommended) | 0.5 | {{ results['pg-sec-title-003'].previous_status \| default('—') }} | {{ results['pg-sec-title-003'].status }} | {{ results['pg-sec-title-003'].trend_display }} | {{ results['pg-sec-title-003'].evidence \| default('—') }} |

## 2. Body — weight 3.5 — **required**

**Why this matters:** Body is the core of any Product Guide — the actual instructions, steps, or explanations readers came for. A body that's empty, thin, or unstructured fails the guide's primary purpose.

**Section Score: {{ sections.body.score }} / 100** ({{ sections.body.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| pg-sec-body-001 | Body section exists | error (mandatory) | 1.5 | {{ results['pg-sec-body-001'].previous_status \| default('—') }} | {{ results['pg-sec-body-001'].status }} | {{ results['pg-sec-body-001'].trend_display }} | {{ results['pg-sec-body-001'].evidence \| default('—') }} |
| pg-sec-body-002 | Body has substantive content (minimum 50 words) | error (mandatory) | 1.0 | {{ results['pg-sec-body-002'].previous_status \| default('—') }} | {{ results['pg-sec-body-002'].status }} | {{ results['pg-sec-body-002'].trend_display }} | {{ results['pg-sec-body-002'].evidence \| default('—') }} |
| pg-sec-body-003 | Body has clear structure (headings, lists, or code blocks) | warning (recommended) | 0.5 | {{ results['pg-sec-body-003'].previous_status \| default('—') }} | {{ results['pg-sec-body-003'].status }} | {{ results['pg-sec-body-003'].trend_display }} | {{ results['pg-sec-body-003'].evidence \| default('—') }} |
| pg-sec-body-004 | Body contains actionable content (steps, instructions, explanations) | warning (recommended) | 0.5 | {{ results['pg-sec-body-004'].previous_status \| default('—') }} | {{ results['pg-sec-body-004'].status }} | {{ results['pg-sec-body-004'].trend_display }} | {{ results['pg-sec-body-004'].evidence \| default('—') }} |

## 3. Purpose — weight 1.5 — optional

**Why this matters:** Purpose states why this Product Guide exists and who it's for. Without it, readers can't quickly assess whether this guide is relevant to them.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| pg-sec-purpose-001 | Purpose section exists | warning (recommended) | 0.5 | {{ results['pg-sec-purpose-001'].previous_status \| default('—') }} | {{ results['pg-sec-purpose-001'].status }} | {{ results['pg-sec-purpose-001'].trend_display }} | {{ results['pg-sec-purpose-001'].evidence \| default('—') }} |
| pg-sec-purpose-002 | Purpose states guide intent | warning (recommended) | 0.5 | {{ results['pg-sec-purpose-002'].previous_status \| default('—') }} | {{ results['pg-sec-purpose-002'].status }} | {{ results['pg-sec-purpose-002'].trend_display }} | {{ results['pg-sec-purpose-002'].evidence \| default('—') }} |
| pg-sec-purpose-003 | Purpose defines target audience | warning (recommended) | 0.5 | {{ results['pg-sec-purpose-003'].previous_status \| default('—') }} | {{ results['pg-sec-purpose-003'].status }} | {{ results['pg-sec-purpose-003'].trend_display }} | {{ results['pg-sec-purpose-003'].evidence \| default('—') }} |

## 4. Product Context (early) — weight 1.5 — optional

**Why this matters:** Product Context provides background information about the product and its positioning, grounding the guide in what's actually true for this product version.

**Section Score: {{ sections.product_context_early.score }} / 100** ({{ sections.product_context_early.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| pg-sec-context-001 | Product context section exists | warning (recommended) | 0.5 | {{ results['pg-sec-context-001'].previous_status \| default('—') }} | {{ results['pg-sec-context-001'].status }} | {{ results['pg-sec-context-001'].trend_display }} | {{ results['pg-sec-context-001'].evidence \| default('—') }} |
| pg-sec-context-002 | Product context provides background information | warning (recommended) | 0.5 | {{ results['pg-sec-context-002'].previous_status \| default('—') }} | {{ results['pg-sec-context-002'].status }} | {{ results['pg-sec-context-002'].trend_display }} | {{ results['pg-sec-context-002'].evidence \| default('—') }} |
| pg-sec-context-003 | Product context references Vision Documentation | warning (recommended) | 0.5 | {{ results['pg-sec-context-003'].previous_status \| default('—') }} | {{ results['pg-sec-context-003'].status }} | {{ results['pg-sec-context-003'].trend_display }} | {{ results['pg-sec-context-003'].evidence \| default('—') }} |

## 5. Public Contract (early) — weight 1.5 — optional

**Why this matters:** Public Contract defines the public API or interface exposed to users, including stability guarantees. Without it, readers have no reference for what's stable and what's subject to change.

**Section Score: {{ sections.public_contract_early.score }} / 100** ({{ sections.public_contract_early.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| pg-sec-contract-001 | Public contract section exists | warning (recommended) | 0.5 | {{ results['pg-sec-contract-001'].previous_status \| default('—') }} | {{ results['pg-sec-contract-001'].status }} | {{ results['pg-sec-contract-001'].trend_display }} | {{ results['pg-sec-contract-001'].evidence \| default('—') }} |
| pg-sec-contract-002 | Public contract defines the public interface | warning (recommended) | 0.5 | {{ results['pg-sec-contract-002'].previous_status \| default('—') }} | {{ results['pg-sec-contract-002'].status }} | {{ results['pg-sec-contract-002'].trend_display }} | {{ results['pg-sec-contract-002'].evidence \| default('—') }} |
| pg-sec-contract-003 | Public contract defines stability or versioning guarantees | warning (recommended) | 0.5 | {{ results['pg-sec-contract-003'].previous_status \| default('—') }} | {{ results['pg-sec-contract-003'].status }} | {{ results['pg-sec-contract-003'].trend_display }} | {{ results['pg-sec-contract-003'].evidence \| default('—') }} |

## 6. Related — weight 1.5 — optional

**Why this matters:** Related links connect this Product Guide to other guides or documentation. Without them, readers can't discover adjacent content that might be relevant to their task.

**Section Score: {{ sections.related.score }} / 100** ({{ sections.related.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| pg-sec-related-001 | Related section exists | warning (recommended) | 0.5 | {{ results['pg-sec-related-001'].previous_status \| default('—') }} | {{ results['pg-sec-related-001'].status }} | {{ results['pg-sec-related-001'].trend_display }} | {{ results['pg-sec-related-001'].evidence \| default('—') }} |
| pg-sec-related-002 | Related lists at least one related guide or documentation | warning (recommended) | 0.5 | {{ results['pg-sec-related-002'].previous_status \| default('—') }} | {{ results['pg-sec-related-002'].status }} | {{ results['pg-sec-related-002'].trend_display }} | {{ results['pg-sec-related-002'].evidence \| default('—') }} |
| pg-sec-related-003 | All links resolve to existing documents | warning (recommended) | 0.5 | {{ results['pg-sec-related-003'].previous_status \| default('—') }} | {{ results['pg-sec-related-003'].status }} | {{ results['pg-sec-related-003'].trend_display }} | {{ results['pg-sec-related-003'].evidence \| default('—') }} |

## 7. Product Context — weight 3.0 — **required**

**Why this matters:** Product Context states the prerequisites, default behavior, and version-specific context a reader needs before using a feature — grounding the guide in what's actually true for this product version, not generic assumptions.

**Section Score: {{ sections.product_context.score }} / 100** ({{ sections.product_context.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| product-guide-sec-product_context-001 | Product Context section exists | error (mandatory) | 1.5 | {{ results['product-guide-sec-product_context-001'].previous_status \| default('—') }} | {{ results['product-guide-sec-product_context-001'].status }} | {{ results['product-guide-sec-product_context-001'].trend_display }} | {{ results['product-guide-sec-product_context-001'].evidence \| default('—') }} |
| product-guide-sec-product_context-002 | Product Context has substantive content (≥ 100 chars) | error (mandatory) | 1.0 | {{ results['product-guide-sec-product_context-002'].previous_status \| default('—') }} | {{ results['product-guide-sec-product_context-002'].status }} | {{ results['product-guide-sec-product_context-002'].trend_display }} | {{ results['product-guide-sec-product_context-002'].evidence \| default('—') }} |
| product-guide-sec-product_context-003 | Product Context is project-specific, not generic boilerplate | warning (recommended) | 0.5 | {{ results['product-guide-sec-product_context-003'].previous_status \| default('—') }} | {{ results['product-guide-sec-product_context-003'].status }} | {{ results['product-guide-sec-product_context-003'].trend_display }} | {{ results['product-guide-sec-product_context-003'].evidence \| default('—') }} |

## 8. Public Contract — weight 3.0 — **required**

**Why this matters:** Public Contract is the exhaustive, tabular reference for every input, output, flag, config key, and error condition a user can hit. It exists as the ground truth a user checks instead of reading source code.

**Section Score: {{ sections.public_contract.score }} / 100** ({{ sections.public_contract.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| product-guide-sec-public_contract-001 | Public Contract section exists | error (mandatory) | 1.5 | {{ results['product-guide-sec-public_contract-001'].previous_status \| default('—') }} | {{ results['product-guide-sec-public_contract-001'].status }} | {{ results['product-guide-sec-public_contract-001'].trend_display }} | {{ results['product-guide-sec-public_contract-001'].evidence \| default('—') }} |
| product-guide-sec-public_contract-002 | Public Contract has substantive content (≥ 100 chars) | error (mandatory) | 1.0 | {{ results['product-guide-sec-public_contract-002'].previous_status \| default('—') }} | {{ results['product-guide-sec-public_contract-002'].status }} | {{ results['product-guide-sec-public_contract-002'].trend_display }} | {{ results['product-guide-sec-public_contract-002'].evidence \| default('—') }} |
| product-guide-sec-public_contract-003 | Public Contract is project-specific, not generic boilerplate | warning (recommended) | 0.5 | {{ results['product-guide-sec-public_contract-003'].previous_status \| default('—') }} | {{ results['product-guide-sec-public_contract-003'].status }} | {{ results['product-guide-sec-public_contract-003'].trend_display }} | {{ results['product-guide-sec-public_contract-003'].evidence \| default('—') }} |

---

## Failures Requiring Attention

{% if failed_rules | length > 0 %}
| Section | Rule | Message | Evidence | New This Run? |
|---|---|---|---|---|
{% for r in failed_rules -%}
| {{ r.section_type }} | {{ r.id }} | {{ r.message }} | {{ r.evidence | default('—') }} | {{ 'Yes — regression' if r.is_new_failure else 'No — carried over' }} |
{% endfor %}
{% else %}
No failures across all 8 sections.
{% endif %}

---

## Metadata

| Field | Value |
|---|---|
| Domain | product-guide |
| Standard | documentation-standards |
| Section Rule Files | `audit/deterministic/section/16-product-guide/*.yaml` |
| Auditor | System (deterministic engine) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
