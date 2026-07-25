# Deterministic Section Report — Engineering

**Document:** {{ document_path }}
**Standard:** `documentation-standards/07-engineering-standards.md`
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
| 1 | Guiding Principles | **required** | 4.0 | {{ sections.guiding_principles.score }} / 100 | {{ sections.guiding_principles.previous_score | default('—') }} | {{ sections.guiding_principles.trend_display }} |
| 2 | Rationale | **required** | 3.5 | {{ sections.rationale.score }} / 100 | {{ sections.rationale.previous_score | default('—') }} | {{ sections.rationale.trend_display }} |
| 3 | Build Standards | **required** | 4.5 | {{ sections.build_standards.score }} / 100 | {{ sections.build_standards.previous_score | default('—') }} | {{ sections.build_standards.trend_display }} |
| 4 | Testing Standards | **required** | 3.5 | {{ sections.testing_standards.score }} / 100 | {{ sections.testing_standards.previous_score | default('—') }} | {{ sections.testing_standards.trend_display }} |
| 5 | Purpose | optional | 1.8 | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 6 | Code Standards | optional | 1.8 | {{ sections.code_standards.score }} / 100 | {{ sections.code_standards.previous_score | default('—') }} | {{ sections.code_standards.trend_display }} |
| 7 | Constraints | optional | 1.3 | {{ sections.constraints.score }} / 100 | {{ sections.constraints.previous_score | default('—') }} | {{ sections.constraints.trend_display }} |
| 8 | Traceability | optional | 1.3 | {{ sections.traceability.score }} / 100 | {{ sections.traceability.previous_score | default('—') }} | {{ sections.traceability.trend_display }} |

The 4 required sections carry 15.5 of the document's 21.7 total rule weight — a document can only pass if those four are both present and internally sound; the remaining four are recommended-quality signal, not gating.

---

## 1. Guiding Principles — `section/07-engineering/01-guiding_principles.yaml` — weight 4.0 — **required**

**Why this matters:** Guiding Principles are the engineering approach's non-negotiable rules — they constrain every downstream decision. Without them, every engineering decision is a one-off judgment call, and there's no consistent basis for reviewing whether the system is actually well-engineered.

**Section Score: {{ sections.guiding_principles.score }} / 100** ({{ sections.guiding_principles.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| eng-sec-guiding-001 | Guiding Principles section exists | error (mandatory) | 1.5 | {{ results['eng-sec-guiding-001'].previous_status \| default('—') }} | {{ results['eng-sec-guiding-001'].status }} | {{ results['eng-sec-guiding-001'].trend_display }} | {{ results['eng-sec-guiding-001'].evidence \| default('—') }} |
| eng-sec-guiding-002 | States engineering philosophy — principles that guide engineering decisions | error (mandatory) | 1.0 | {{ results['eng-sec-guiding-002'].previous_status \| default('—') }} | {{ results['eng-sec-guiding-002'].status }} | {{ results['eng-sec-guiding-002'].trend_display }} | {{ results['eng-sec-guiding-002'].evidence \| default('—') }} |
| eng-sec-guiding-003 | Technology-independent — no specific technologies, frameworks, or implementation details | error (mandatory) | 1.0 | {{ results['eng-sec-guiding-003'].previous_status \| default('—') }} | {{ results['eng-sec-guiding-003'].status }} | {{ results['eng-sec-guiding-003'].trend_display }} | {{ results['eng-sec-guiding-003'].evidence \| default('—') }} |
| eng-sec-guiding-004 | Principles are actionable — can guide concrete engineering decisions | warning (recommended) | 0.5 | {{ results['eng-sec-guiding-004'].previous_status \| default('—') }} | {{ results['eng-sec-guiding-004'].status }} | {{ results['eng-sec-guiding-004'].trend_display }} | {{ results['eng-sec-guiding-004'].evidence \| default('—') }} |

## 2. Rationale — `02-rationale.yaml` — weight 3.5 — **required**

**Why this matters:** Rationale explains why engineering standards exist — the justification for the approach. Without it, every engineering standard is a rule without a reason, and there's no basis for deciding whether a standard still applies when circumstances change.

**Section Score: {{ sections.rationale.score }} / 100** ({{ sections.rationale.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| eng-sec-rationale-001 | Rationale section exists | error (mandatory) | 1.5 | {{ results['eng-sec-rationale-001'].previous_status \| default('—') }} | {{ results['eng-sec-rationale-001'].status }} | {{ results['eng-sec-rationale-001'].trend_display }} | {{ results['eng-sec-rationale-001'].evidence \| default('—') }} |
| eng-sec-rationale-002 | Explains why engineering standards exist — justification for the approach | error (mandatory) | 1.0 | {{ results['eng-sec-rationale-002'].previous_status \| default('—') }} | {{ results['eng-sec-rationale-002'].status }} | {{ results['eng-sec-rationale-002'].trend_display }} | {{ results['eng-sec-rationale-002'].evidence \| default('—') }} |
| eng-sec-rationale-003 | References upstream domains — connects to Philosophy or Architecture constraints | warning (recommended) | 0.5 | {{ results['eng-sec-rationale-003'].previous_status \| default('—') }} | {{ results['eng-sec-rationale-003'].status }} | {{ results['eng-sec-rationale-003'].trend_display }} | {{ results['eng-sec-rationale-003'].evidence \| default('—') }} |
| eng-sec-rationale-004 | Discusses trade-offs — alternatives considered or trade-offs made | warning (recommended) | 0.5 | {{ results['eng-sec-rationale-004'].previous_status \| default('—') }} | {{ results['eng-sec-rationale-004'].status }} | {{ results['eng-sec-rationale-004'].trend_display }} | {{ results['eng-sec-rationale-004'].evidence \| default('—') }} |

## 3. Build Standards — `03-build_standards.yaml` — weight 4.5 — **required**

**Why this matters:** Build Standards define how code is built, tested, and released — the concrete rules that govern the CI/CD pipeline. Without them, every build decision is ad-hoc, and there's no consistent basis for verifying that the pipeline actually enforces what Testing Standards requires.

**Section Score: {{ sections.build_standards.score }} / 100** ({{ sections.build_standards.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| eng-sec-build-001 | Build Standards section exists | error (mandatory) | 1.5 | {{ results['eng-sec-build-001'].previous_status \| default('—') }} | {{ results['eng-sec-build-001'].status }} | {{ results['eng-sec-build-001'].trend_display }} | {{ results['eng-sec-build-001'].evidence \| default('—') }} |
| eng-sec-build-002 | Defines concrete standards — version control, CI/CD, dependency management, or release processes | error (mandatory) | 1.0 | {{ results['eng-sec-build-002'].previous_status \| default('—') }} | {{ results['eng-sec-build-002'].status }} | {{ results['eng-sec-build-002'].trend_display }} | {{ results['eng-sec-build-002'].evidence \| default('—') }} |
| eng-sec-build-003 | Technology-independent — no specific CI tools, package managers, or build systems named | error (mandatory) | 1.0 | {{ results['eng-sec-build-003'].previous_status \| default('—') }} | {{ results['eng-sec-build-003'].status }} | {{ results['eng-sec-build-003'].trend_display }} | {{ results['eng-sec-build-003'].evidence \| default('—') }} |
| eng-sec-build-004 | Includes versioning strategy — how versions are managed and released | warning (recommended) | 0.5 | {{ results['eng-sec-build-004'].previous_status \| default('—') }} | {{ results['eng-sec-build-004'].status }} | {{ results['eng-sec-build-004'].trend_display }} | {{ results['eng-sec-build-004'].evidence \| default('—') }} |
| eng-sec-build-005 | Includes dependency policy — how external dependencies are managed and audited | warning (recommended) | 0.5 | {{ results['eng-sec-build-005'].previous_status \| default('—') }} | {{ results['eng-sec-build-005'].status }} | {{ results['eng-sec-build-005'].trend_display }} | {{ results['eng-sec-build-005'].evidence \| default('—') }} |

## 4. Testing Standards — `04-testing_standards.yaml` — weight 3.5 — **required**

**Why this matters:** Testing Standards define what tests exist, what they cover, and what quality gates they enforce. Without them, every testing decision is ad-hoc, and there's no consistent basis for verifying that the pipeline actually enforces the coverage and quality thresholds that the system requires.

**Section Score: {{ sections.testing_standards.score }} / 100** ({{ sections.testing_standards.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| eng-sec-testing-001 | Testing Standards section exists | error (mandatory) | 1.5 | {{ results['eng-sec-testing-001'].previous_status \| default('—') }} | {{ results['eng-sec-testing-001'].status }} | {{ results['eng-sec-testing-001'].trend_display }} | {{ results['eng-sec-testing-001'].evidence \| default('—') }} |
| eng-sec-testing-002 | Defines concrete standards — test types, coverage thresholds, or quality gates | error (mandatory) | 1.0 | {{ results['eng-sec-testing-002'].previous_status \| default('—') }} | {{ results['eng-sec-testing-002'].status }} | {{ results['eng-sec-testing-002'].trend_display }} | {{ results['eng-sec-testing-002'].evidence \| default('—') }} |
| eng-sec-testing-003 | Covers multiple test levels — unit, integration, system, or acceptance testing | warning (recommended) | 0.5 | {{ results['eng-sec-testing-003'].previous_status \| default('—') }} | {{ results['eng-sec-testing-003'].status }} | {{ results['eng-sec-testing-003'].trend_display }} | {{ results['eng-sec-testing-003'].evidence \| default('—') }} |
| eng-sec-testing-004 | Defines coverage expectations — coverage targets or quality thresholds | warning (recommended) | 0.5 | {{ results['eng-sec-testing-004'].previous_status \| default('—') }} | {{ results['eng-sec-testing-004'].status }} | {{ results['eng-sec-testing-004'].trend_display }} | {{ results['eng-sec-testing-004'].evidence \| default('—') }} |

## 5. Purpose — `05-purpose.yaml` — weight 1.8 — optional

**Why this matters:** Purpose tells a reader why Engineering Documentation exists before they read a single standard. A Purpose section that's missing, vague, or technology-leaking undermines every section that follows it.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| eng-sec-purpose-001 | Purpose section exists | info (optional) | 0.3 | {{ results['eng-sec-purpose-001'].previous_status \| default('—') }} | {{ results['eng-sec-purpose-001'].status }} | {{ results['eng-sec-purpose-001'].trend_display }} | {{ results['eng-sec-purpose-001'].evidence \| default('—') }} |
| eng-sec-purpose-002 | States engineering intent — why this documentation exists | warning (recommended) | 0.5 | {{ results['eng-sec-purpose-002'].previous_status \| default('—') }} | {{ results['eng-sec-purpose-002'].status }} | {{ results['eng-sec-purpose-002'].trend_display }} | {{ results['eng-sec-purpose-002'].evidence \| default('—') }} |
| eng-sec-purpose-003 | Technology-independent — no specific technologies, frameworks, or implementation details | error (optional) | 1.0 | {{ results['eng-sec-purpose-003'].previous_status \| default('—') }} | {{ results['eng-sec-purpose-003'].status }} | {{ results['eng-sec-purpose-003'].trend_display }} | {{ results['eng-sec-purpose-003'].evidence \| default('—') }} |

## 6. Code Standards — `06-code_standards.yaml` — weight 1.8 — optional

**Why this matters:** Code Standards define coding conventions — naming, formatting, documentation, and style guidelines. Without them, every code review is a style negotiation instead of a quality check.

**Section Score: {{ sections.code_standards.score }} / 100** ({{ sections.code_standards.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| eng-sec-code-001 | Code Standards section exists | info (optional) | 0.3 | {{ results['eng-sec-code-001'].previous_status \| default('—') }} | {{ results['eng-sec-code-001'].status }} | {{ results['eng-sec-code-001'].trend_display }} | {{ results['eng-sec-code-001'].evidence \| default('—') }} |
| eng-sec-code-002 | Defines coding conventions — naming, formatting, documentation, or style guidelines | warning (recommended) | 0.5 | {{ results['eng-sec-code-002'].previous_status \| default('—') }} | {{ results['eng-sec-code-002'].status }} | {{ results['eng-sec-code-002'].trend_display }} | {{ results['eng-sec-code-002'].evidence \| default('—') }} |
| eng-sec-code-003 | Technology-independent — no specific linters, formatters, or language-specific tools named | error (optional) | 1.0 | {{ results['eng-sec-code-003'].previous_status \| default('—') }} | {{ results['eng-sec-code-003'].status }} | {{ results['eng-sec-code-003'].trend_display }} | {{ results['eng-sec-code-003'].evidence \| default('—') }} |

## 7. Constraints — `07-constraints.yaml` — weight 1.3 — optional

**Why this matters:** Constraints capture the boundaries on engineering decisions — what must be true regardless of design. Without them, every engineering constraint is discovered late, during Architecture review or, worse, in production.

**Section Score: {{ sections.constraints.score }} / 100** ({{ sections.constraints.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| eng-sec-constraints-001 | Constraints section exists | info (optional) | 0.3 | {{ results['eng-sec-constraints-001'].previous_status \| default('—') }} | {{ results['eng-sec-constraints-001'].status }} | {{ results['eng-sec-constraints-001'].trend_display }} | {{ results['eng-sec-constraints-001'].evidence \| default('—') }} |
| eng-sec-constraints-002 | Defines engineering constraints — regulatory, operational, or technical | warning (recommended) | 0.5 | {{ results['eng-sec-constraints-002'].previous_status \| default('—') }} | {{ results['eng-sec-constraints-002'].status }} | {{ results['eng-sec-constraints-002'].trend_display }} | {{ results['eng-sec-constraints-002'].evidence \| default('—') }} |
| eng-sec-constraints-003 | Constraints have clear sources — each identifies where it originates | warning (recommended) | 0.5 | {{ results['eng-sec-constraints-003'].previous_status \| default('—') }} | {{ results['eng-sec-constraints-003'].status }} | {{ results['eng-sec-constraints-003'].trend_display }} | {{ results['eng-sec-constraints-003'].evidence \| default('—') }} |

## 8. Traceability — `08-traceability.yaml` — weight 1.3 — optional

**Why this matters:** Traceability maps engineering decisions back to Philosophy and Architecture and forward to Implementation. Without it, every engineering standard is unverifiable — you can't tell whether the system actually implements what the standards require.

**Section Score: {{ sections.traceability.score }} / 100** ({{ sections.traceability.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| eng-sec-trace-001 | Traceability section exists | info (optional) | 0.3 | {{ results['eng-sec-trace-001'].previous_status \| default('—') }} | {{ results['eng-sec-trace-001'].status }} | {{ results['eng-sec-trace-001'].trend_display }} | {{ results['eng-sec-trace-001'].evidence \| default('—') }} |
| eng-sec-trace-002 | Links to upstream domains — Philosophy, Architecture, or Vision | warning (recommended) | 0.5 | {{ results['eng-sec-trace-002'].previous_status \| default('—') }} | {{ results['eng-sec-trace-002'].status }} | {{ results['eng-sec-trace-002'].trend_display }} | {{ results['eng-sec-trace-002'].evidence \| default('—') }} |
| eng-sec-trace-003 | Links to downstream implementation — Implementation or Feature Technical | warning (recommended) | 0.5 | {{ results['eng-sec-trace-003'].previous_status \| default('—') }} | {{ results['eng-sec-trace-003'].status }} | {{ results['eng-sec-trace-003'].trend_display }} | {{ results['eng-sec-trace-003'].evidence \| default('—') }} |

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
| Domain | engineering |
| Standard | documentation-standards |
| Section Rule Files | `audit/deterministic/section/07-engineering/*.yaml` |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
