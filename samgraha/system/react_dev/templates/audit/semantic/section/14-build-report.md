# Semantic Section Report — Build

**Document:** {{ document_path }}
**Standard:** `documentation-standards/14-build-standards.md`
**Rubric Files:** `audit/semantic/section/14-build/*.md`
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
| 1 | Documentation Quality | **required** | {{ sections.documentation_quality.score }} / 100 | {{ sections.documentation_quality.previous_score | default('—') }} | {{ sections.documentation_quality.trend_display }} |
| 2 | Security Checks | **required** | {{ sections.security_checks.score }} / 100 | {{ sections.security_checks.previous_score | default('—') }} | {{ sections.security_checks.trend_display }} |
| 3 | Versioning & Naming | **required** | {{ sections.versioning_naming.score }} / 100 | {{ sections.versioning_naming.previous_score | default('—') }} | {{ sections.versioning_naming.trend_display }} |
| 4 | Purpose | optional | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 5 | Size Checks | **required** | {{ sections.size_checks.score }} / 100 | {{ sections.size_checks.previous_score | default('—') }} | {{ sections.size_checks.trend_display }} |
| 6 | ML Artifact Management | **required** | {{ sections.ml_artifact_management.score }} / 100 | {{ sections.ml_artifact_management.previous_score | default('—') }} | {{ sections.ml_artifact_management.trend_display }} |
| 7 | CI/CD Validation | **required** | {{ sections.cicd_validation.score }} / 100 | {{ sections.cicd_validation.previous_score | default('—') }} | {{ sections.cicd_validation.trend_display }} |
| 8 | Obfuscation & Optimization | **required** | {{ sections.obfuscation_optimization.score }} / 100 | {{ sections.obfuscation_optimization.previous_score | default('—') }} | {{ sections.obfuscation_optimization.trend_display }} |
| — | Generic (unmatched sections) | n/a | {{ sections.generic.score }} / 100 | {{ sections.generic.previous_score | default('—') }} | {{ sections.generic.trend_display }} |

A section absent from the document (among the optional ones) isn't scored at all here — it's a deterministic presence check, not a semantic quality judgment on nothing.

---

## 1. Documentation Quality — `section/14-build/01-documentation_quality.md` — **required**

**Why this matters:** Documentation Quality is the gate that ensures build documentation meets minimum standards before it can be trusted. Without it, downstream consumers have no assurance that the build policy is complete or accurate.

**Section Score: {{ sections.documentation_quality.score }} / 100** ({{ sections.documentation_quality.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['documentation_quality.C1'].previous_passed_display | default('—') }} | {{ results['documentation_quality.C1'].passed_display }} | {{ results['documentation_quality.C1'].trend_display }} | {{ results['documentation_quality.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['documentation_quality.C2'].previous_passed_display | default('—') }} | {{ results['documentation_quality.C2'].passed_display }} | {{ results['documentation_quality.C2'].trend_display }} | {{ results['documentation_quality.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['documentation_quality.C3'].previous_passed_display | default('—') }} | {{ results['documentation_quality.C3'].passed_display }} | {{ results['documentation_quality.C3'].trend_display }} | {{ results['documentation_quality.C3'].evidence.excerpt | default('—') }} |

C1: section exists with substantive content specific to this project. C2: internally consistent, does not contradict other sections. C3: includes concrete examples, evidence, or project-specific detail.

## 2. Security Checks — `section/14-build/02-security_checks.md` — **required**

**Why this matters:** Security Checks is the gate that prevents known vulnerabilities from shipping in a build. Without scan steps and failure criteria, "the build is secure" is an unverifiable claim.

**Section Score: {{ sections.security_checks.score }} / 100** ({{ sections.security_checks.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['security_checks.C1'].previous_passed_display | default('—') }} | {{ results['security_checks.C1'].passed_display }} | {{ results['security_checks.C1'].trend_display }} | {{ results['security_checks.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['security_checks.C2'].previous_passed_display | default('—') }} | {{ results['security_checks.C2'].passed_display }} | {{ results['security_checks.C2'].trend_display }} | {{ results['security_checks.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['security_checks.C3'].previous_passed_display | default('—') }} | {{ results['security_checks.C3'].passed_display }} | {{ results['security_checks.C3'].trend_display }} | {{ results['security_checks.C3'].evidence.excerpt | default('—') }} |

C1: section exists with substantive content specific to this project. C2: internally consistent, does not contradict other sections. C3: includes concrete examples, evidence, or project-specific detail.

## 3. Versioning & Naming — `section/14-build/03-versioning_naming.md` — **required**

**Why this matters:** Versioning & Naming defines how artifacts are identified and differentiated. Without a clear scheme, consumers cannot tell which version they have or which version they need.

**Section Score: {{ sections.versioning_naming.score }} / 100** ({{ sections.versioning_naming.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['versioning_naming.C1'].previous_passed_display | default('—') }} | {{ results['versioning_naming.C1'].passed_display }} | {{ results['versioning_naming.C1'].trend_display }} | {{ results['versioning_naming.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['versioning_naming.C2'].previous_passed_display | default('—') }} | {{ results['versioning_naming.C2'].passed_display }} | {{ results['versioning_naming.C2'].trend_display }} | {{ results['versioning_naming.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['versioning_naming.C3'].previous_passed_display | default('—') }} | {{ results['versioning_naming.C3'].passed_display }} | {{ results['versioning_naming.C3'].trend_display }} | {{ results['versioning_naming.C3'].evidence.excerpt | default('—') }} |

C1: section exists with substantive content specific to this project. C2: internally consistent, does not contradict other sections. C3: includes concrete examples, evidence, or project-specific detail.

## 4. Purpose — `section/14-build/04-purpose.md` — optional

**Why this matters:** Purpose tells a reader why Build Documentation exists before they read a single rule. A missing or vague Purpose section undermines every section that follows it.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['purpose.C1'].previous_passed_display | default('—') }} | {{ results['purpose.C1'].passed_display }} | {{ results['purpose.C1'].trend_display }} | {{ results['purpose.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['purpose.C2'].previous_passed_display | default('—') }} | {{ results['purpose.C2'].passed_display }} | {{ results['purpose.C2'].trend_display }} | {{ results['purpose.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['purpose.C3'].previous_passed_display | default('—') }} | {{ results['purpose.C3'].passed_display }} | {{ results['purpose.C3'].trend_display }} | {{ results['purpose.C3'].evidence.excerpt | default('—') }} |

C1: section exists with substantive content specific to this project. C2: internally consistent, does not contradict other sections. C3: includes concrete examples, evidence, or project-specific detail.

## 5. Size Checks — `section/14-build/05-size_checks.md` — **required**

**Why this matters:** Size Checks defines measurable limits on artifact size and what happens when a build crosses them. Without it, bloat is caught by policy, not discovered in production.

**Section Score: {{ sections.size_checks.score }} / 100** ({{ sections.size_checks.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['size_checks.C1'].previous_passed_display | default('—') }} | {{ results['size_checks.C1'].passed_display }} | {{ results['size_checks.C1'].trend_display }} | {{ results['size_checks.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['size_checks.C2'].previous_passed_display | default('—') }} | {{ results['size_checks.C2'].passed_display }} | {{ results['size_checks.C2'].trend_display }} | {{ results['size_checks.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['size_checks.C3'].previous_passed_display | default('—') }} | {{ results['size_checks.C3'].passed_display }} | {{ results['size_checks.C3'].trend_display }} | {{ results['size_checks.C3'].evidence.excerpt | default('—') }} |

C1: measurable size limit defined per artifact type. C2: measurement method specified. C3: enforcement action stated for a breach.

## 6. ML Artifact Management — `section/14-build/06-ml_artifact_management.md` — **required**

**Why this matters:** ML Artifact Management defines how models and training data are versioned, tracked, and reproduced. Without it, a model in production cannot be traced back to the exact data and code that produced it.

**Section Score: {{ sections.ml_artifact_management.score }} / 100** ({{ sections.ml_artifact_management.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['ml_artifact_management.C1'].previous_passed_display | default('—') }} | {{ results['ml_artifact_management.C1'].passed_display }} | {{ results['ml_artifact_management.C1'].trend_display }} | {{ results['ml_artifact_management.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['ml_artifact_management.C2'].previous_passed_display | default('—') }} | {{ results['ml_artifact_management.C2'].passed_display }} | {{ results['ml_artifact_management.C2'].trend_display }} | {{ results['ml_artifact_management.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['ml_artifact_management.C3'].previous_passed_display | default('—') }} | {{ results['ml_artifact_management.C3'].passed_display }} | {{ results['ml_artifact_management.C3'].trend_display }} | {{ results['ml_artifact_management.C3'].evidence.excerpt | default('—') }} |

C1: versioning scheme defined for models and data. C2: experiment tracking approach specified. C3: reproducibility requirements stated and falsifiable.

## 7. CI/CD Validation — `section/14-build/07-cicd_validation.md` — **required**

**Why this matters:** CI/CD Validation defines the gate sequence a build must pass and what happens when a gate fails. Without it, "the pipeline is green" has no precise, checkable meaning.

**Section Score: {{ sections.cicd_validation.score }} / 100** ({{ sections.cicd_validation.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['cicd_validation.C1'].previous_passed_display | default('—') }} | {{ results['cicd_validation.C1'].passed_display }} | {{ results['cicd_validation.C1'].trend_display }} | {{ results['cicd_validation.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['cicd_validation.C2'].previous_passed_display | default('—') }} | {{ results['cicd_validation.C2'].passed_display }} | {{ results['cicd_validation.C2'].trend_display }} | {{ results['cicd_validation.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['cicd_validation.C3'].previous_passed_display | default('—') }} | {{ results['cicd_validation.C3'].passed_display }} | {{ results['cicd_validation.C3'].trend_display }} | {{ results['cicd_validation.C3'].evidence.excerpt | default('—') }} |

C1: gate sequence defined in execution order. C2: failure handling policy stated. C3: deployment blockers explicitly named per gate.

## 8. Obfuscation & Optimization — `section/14-build/08-obfuscation_optimization.md` — **required**

**Why this matters:** Obfuscation & Optimization defines which build-time transformations apply, under what configuration, and their cost to debuggability. Without it, a production stack trace problem is a mystery.

**Section Score: {{ sections.obfuscation_optimization.score }} / 100** ({{ sections.obfuscation_optimization.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['obfuscation_optimization.C1'].previous_passed_display | default('—') }} | {{ results['obfuscation_optimization.C1'].passed_display }} | {{ results['obfuscation_optimization.C1'].trend_display }} | {{ results['obfuscation_optimization.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['obfuscation_optimization.C2'].previous_passed_display | default('—') }} | {{ results['obfuscation_optimization.C2'].passed_display }} | {{ results['obfuscation_optimization.C2'].trend_display }} | {{ results['obfuscation_optimization.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['obfuscation_optimization.C3'].previous_passed_display | default('—') }} | {{ results['obfuscation_optimization.C3'].passed_display }} | {{ results['obfuscation_optimization.C3'].trend_display }} | {{ results['obfuscation_optimization.C3'].evidence.excerpt | default('—') }} |

C1: transformations specified per build type. C2: configuration/tooling referenced. C3: debuggability impact addressed.

## Generic — `generic.md` (sections with no matching semantic_type)

**Why this matters:** Catches build-relevant content an author wrote under a heading that doesn't match any of the 8 named section types above — still judged for relevance and non-duplication, not given a free pass for being unclassified.

**Section Score: {{ sections.generic.score }} / 100** ({{ sections.generic.trend_display }})

| ID | Weight | Points | Previous | Current | Trend | Evidence |
|---|---|---:|---|---|---|---|
| C1 | mandatory | 40 | {{ results['generic.C1'].previous_passed_display | default('—') }} | {{ results['generic.C1'].passed_display }} | {{ results['generic.C1'].trend_display }} | {{ results['generic.C1'].evidence.excerpt | default('—') }} |
| C2 | mandatory | 30 | {{ results['generic.C2'].previous_passed_display | default('—') }} | {{ results['generic.C2'].passed_display }} | {{ results['generic.C2'].trend_display }} | {{ results['generic.C2'].evidence.excerpt | default('—') }} |
| C3 | recommended | 30 | {{ results['generic.C3'].previous_passed_display | default('—') }} | {{ results['generic.C3'].passed_display }} | {{ results['generic.C3'].trend_display }} | {{ results['generic.C3'].evidence.excerpt | default('—') }} |

C1: content is build-relevant, not implementation-specific. C2: claims and assertions are justified by evidence or reasoning. C3: no duplication of content from other build section types.

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
| Domain | build |
| Standard | documentation-standards |
| Section Rubric Files | `audit/semantic/section/14-build/*.md` |
| Auditor | LLM ({{ model_name }}) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
