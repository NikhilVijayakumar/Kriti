# Deterministic Section Report — Build

**Document:** {{ document_path }}
**Standard:** `documentation-standards/14-build-standards.md`
**Rule Files:** `audit/deterministic/section/14-build/*.yaml`
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
| 1 | Documentation Quality | **required** | 3.5 | {{ sections.documentation_quality.score }} / 100 | {{ sections.documentation_quality.previous_score | default('—') }} | {{ sections.documentation_quality.trend_display }} |
| 2 | Security Checks | **required** | 3.5 | {{ sections.security_checks.score }} / 100 | {{ sections.security_checks.previous_score | default('—') }} | {{ sections.security_checks.trend_display }} |
| 3 | Versioning & Naming | **required** | 3.5 | {{ sections.versioning_naming.score }} / 100 | {{ sections.versioning_naming.previous_score | default('—') }} | {{ sections.versioning_naming.trend_display }} |
| 4 | Purpose | optional | 1.5 | {{ sections.purpose.score }} / 100 | {{ sections.purpose.previous_score | default('—') }} | {{ sections.purpose.trend_display }} |
| 5 | Size Checks | **required** | 3.0 | {{ sections.size_checks.score }} / 100 | {{ sections.size_checks.previous_score | default('—') }} | {{ sections.size_checks.trend_display }} |
| 6 | ML Artifact Management | **required** | 3.0 | {{ sections.ml_artifact_management.score }} / 100 | {{ sections.ml_artifact_management.previous_score | default('—') }} | {{ sections.ml_artifact_management.trend_display }} |
| 7 | CI/CD Validation | **required** | 3.0 | {{ sections.cicd_validation.score }} / 100 | {{ sections.cicd_validation.previous_score | default('—') }} | {{ sections.cicd_validation.trend_display }} |
| 8 | Obfuscation & Optimization | **required** | 3.0 | {{ sections.obfuscation_optimization.score }} / 100 | {{ sections.obfuscation_optimization.previous_score | default('—') }} | {{ sections.obfuscation_optimization.trend_display }} |

The 7 required sections carry 22.5 of the document's 24.0 total rule weight — a document can only pass if those seven are both present and internally sound; the remaining one is recommended-quality signal, not gating.

---

## 1. Documentation Quality — weight 3.5 — **required**

**Why this matters:** Documentation Quality is the gate that ensures build documentation meets minimum standards before it can be trusted. Without it, downstream consumers have no assurance that the build policy is complete or accurate.

**Section Score: {{ sections.documentation_quality.score }} / 100** ({{ sections.documentation_quality.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| build-sec-doc-quality-001 | Documentation Quality section exists | error (mandatory) | 1.5 | {{ results['build-sec-doc-quality-001'].previous_status \| default('—') }} | {{ results['build-sec-doc-quality-001'].status }} | {{ results['build-sec-doc-quality-001'].trend_display }} | {{ results['build-sec-doc-quality-001'].evidence \| default('—') }} |
| build-sec-doc-quality-002 | Defines documentation quality standards or requirements | error (mandatory) | 1.0 | {{ results['build-sec-doc-quality-002'].previous_status \| default('—') }} | {{ results['build-sec-doc-quality-002'].status }} | {{ results['build-sec-doc-quality-002'].trend_display }} | {{ results['build-sec-doc-quality-002'].evidence \| default('—') }} |
| build-sec-doc-quality-003 | Defines quality checks or validation steps | warning (recommended) | 0.5 | {{ results['build-sec-doc-quality-003'].previous_status \| default('—') }} | {{ results['build-sec-doc-quality-003'].status }} | {{ results['build-sec-doc-quality-003'].trend_display }} | {{ results['build-sec-doc-quality-003'].evidence \| default('—') }} |
| build-sec-doc-quality-004 | References Implementation Documentation generation plan | warning (recommended) | 0.5 | {{ results['build-sec-doc-quality-004'].previous_status \| default('—') }} | {{ results['build-sec-doc-quality-004'].status }} | {{ results['build-sec-doc-quality-004'].trend_display }} | {{ results['build-sec-doc-quality-004'].evidence \| default('—') }} |

## 2. Security Checks — weight 3.5 — **required**

**Why this matters:** Security Checks is the gate that prevents known vulnerabilities from shipping in a build. Without scan steps and failure criteria, "the build is secure" is an unverifiable claim.

**Section Score: {{ sections.security_checks.score }} / 100** ({{ sections.security_checks.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| build-sec-security-001 | Security Checks section exists | error (mandatory) | 1.5 | {{ results['build-sec-security-001'].previous_status \| default('—') }} | {{ results['build-sec-security-001'].status }} | {{ results['build-sec-security-001'].trend_display }} | {{ results['build-sec-security-001'].evidence \| default('—') }} |
| build-sec-security-002 | Defines security scan or audit steps to run during build | error (mandatory) | 1.0 | {{ results['build-sec-security-002'].previous_status \| default('—') }} | {{ results['build-sec-security-002'].status }} | {{ results['build-sec-security-002'].trend_display }} | {{ results['build-sec-security-002'].evidence \| default('—') }} |
| build-sec-security-003 | Defines failure criteria for security gates | warning (recommended) | 0.5 | {{ results['build-sec-security-003'].previous_status \| default('—') }} | {{ results['build-sec-security-003'].status }} | {{ results['build-sec-security-003'].trend_display }} | {{ results['build-sec-security-003'].evidence \| default('—') }} |
| build-sec-security-004 | References Security Documentation mitigation strategies | warning (recommended) | 0.5 | {{ results['build-sec-security-004'].previous_status \| default('—') }} | {{ results['build-sec-security-004'].status }} | {{ results['build-sec-security-004'].trend_display }} | {{ results['build-sec-security-004'].evidence \| default('—') }} |

## 3. Versioning & Naming — weight 3.5 — **required**

**Why this matters:** Versioning & Naming defines how artifacts are identified and differentiated. Without a clear scheme, consumers cannot tell which version they have or which version they need — the basis for reproducibility.

**Section Score: {{ sections.versioning_naming.score }} / 100** ({{ sections.versioning_naming.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| build-sec-version-001 | Versioning & Naming section exists | error (mandatory) | 1.5 | {{ results['build-sec-version-001'].previous_status \| default('—') }} | {{ results['build-sec-version-001'].status }} | {{ results['build-sec-version-001'].trend_display }} | {{ results['build-sec-version-001'].evidence \| default('—') }} |
| build-sec-version-002 | Defines versioning scheme (semver, calver, etc.) | error (mandatory) | 1.0 | {{ results['build-sec-version-002'].previous_status \| default('—') }} | {{ results['build-sec-version-002'].status }} | {{ results['build-sec-version-002'].trend_display }} | {{ results['build-sec-version-002'].evidence \| default('—') }} |
| build-sec-version-003 | Defines naming conventions for artifacts or releases | warning (recommended) | 0.5 | {{ results['build-sec-version-003'].previous_status \| default('—') }} | {{ results['build-sec-version-003'].status }} | {{ results['build-sec-version-003'].trend_display }} | {{ results['build-sec-version-003'].evidence \| default('—') }} |
| build-sec-version-004 | References Engineering Documentation build standards | warning (recommended) | 0.5 | {{ results['build-sec-version-004'].previous_status \| default('—') }} | {{ results['build-sec-version-004'].status }} | {{ results['build-sec-version-004'].trend_display }} | {{ results['build-sec-version-004'].evidence \| default('—') }} |

## 4. Purpose — weight 1.5 — optional

**Why this matters:** Purpose is what tells a reader why Build Documentation exists before they read a single rule. A Purpose section that's missing, vague, or incomplete undermines every section that follows it.

**Section Score: {{ sections.purpose.score }} / 100** ({{ sections.purpose.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| build-sec-purpose-001 | Purpose section exists | warning (recommended) | 0.5 | {{ results['build-sec-purpose-001'].previous_status \| default('—') }} | {{ results['build-sec-purpose-001'].status }} | {{ results['build-sec-purpose-001'].trend_display }} | {{ results['build-sec-purpose-001'].evidence \| default('—') }} |
| build-sec-purpose-002 | States build intent | warning (recommended) | 0.5 | {{ results['build-sec-purpose-002'].previous_status \| default('—') }} | {{ results['build-sec-purpose-002'].status }} | {{ results['build-sec-purpose-002'].trend_display }} | {{ results['build-sec-purpose-002'].evidence \| default('—') }} |
| build-sec-purpose-003 | Defines scope boundaries | warning (recommended) | 0.5 | {{ results['build-sec-purpose-003'].previous_status \| default('—') }} | {{ results['build-sec-purpose-003'].status }} | {{ results['build-sec-purpose-003'].trend_display }} | {{ results['build-sec-purpose-003'].evidence \| default('—') }} |

## 5. Size Checks — weight 3.0 — **required**

**Why this matters:** Size Checks defines measurable limits on artifact size — bundle, binary, image, package — and what happens when a build crosses them. Without it, bloat is caught by policy, not discovered in production.

**Section Score: {{ sections.size_checks.score }} / 100** ({{ sections.size_checks.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| build-sec-size_checks-001 | Size Checks section exists | error (mandatory) | 1.5 | {{ results['build-sec-size_checks-001'].previous_status \| default('—') }} | {{ results['build-sec-size_checks-001'].status }} | {{ results['build-sec-size_checks-001'].trend_display }} | {{ results['build-sec-size_checks-001'].evidence \| default('—') }} |
| build-sec-size_checks-002 | Has substantive content (≥ 100 chars of project-specific detail) | error (mandatory) | 1.0 | {{ results['build-sec-size_checks-002'].previous_status \| default('—') }} | {{ results['build-sec-size_checks-002'].status }} | {{ results['build-sec-size_checks-002'].trend_display }} | {{ results['build-sec-size_checks-002'].evidence \| default('—') }} |
| build-sec-size_checks-003 | Contains project-specific details, not generic boilerplate | warning (recommended) | 0.5 | {{ results['build-sec-size_checks-003'].previous_status \| default('—') }} | {{ results['build-sec-size_checks-003'].status }} | {{ results['build-sec-size_checks-003'].trend_display }} | {{ results['build-sec-size_checks-003'].evidence \| default('—') }} |

## 6. ML Artifact Management — weight 3.0 — **required**

**Why this matters:** ML Artifact Management defines how models and training data are versioned, tracked, and reproduced. Without it, a model in production cannot be traced back to the exact data and code that produced it.

**Section Score: {{ sections.ml_artifact_management.score }} / 100** ({{ sections.ml_artifact_management.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| build-sec-ml_artifact_management-001 | ML Artifact Management section exists | error (mandatory) | 1.5 | {{ results['build-sec-ml_artifact_management-001'].previous_status \| default('—') }} | {{ results['build-sec-ml_artifact_management-001'].status }} | {{ results['build-sec-ml_artifact_management-001'].trend_display }} | {{ results['build-sec-ml_artifact_management-001'].evidence \| default('—') }} |
| build-sec-ml_artifact_management-002 | Has substantive content (≥ 100 chars of project-specific detail) | error (mandatory) | 1.0 | {{ results['build-sec-ml_artifact_management-002'].previous_status \| default('—') }} | {{ results['build-sec-ml_artifact_management-002'].status }} | {{ results['build-sec-ml_artifact_management-002'].trend_display }} | {{ results['build-sec-ml_artifact_management-002'].evidence \| default('—') }} |
| build-sec-ml_artifact_management-003 | Contains project-specific details, not generic boilerplate | warning (recommended) | 0.5 | {{ results['build-sec-ml_artifact_management-003'].previous_status \| default('—') }} | {{ results['build-sec-ml_artifact_management-003'].status }} | {{ results['build-sec-ml_artifact_management-003'].trend_display }} | {{ results['build-sec-ml_artifact_management-003'].evidence \| default('—') }} |

## 7. CI/CD Validation — weight 3.0 — **required**

**Why this matters:** CI/CD Validation defines the gate sequence a build must pass and what happens when a gate fails. Without it, "the pipeline is green" has no precise, checkable meaning.

**Section Score: {{ sections.cicd_validation.score }} / 100** ({{ sections.cicd_validation.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| build-sec-cicd_validation-001 | CI/CD Validation section exists | error (mandatory) | 1.5 | {{ results['build-sec-cicd_validation-001'].previous_status \| default('—') }} | {{ results['build-sec-cicd_validation-001'].status }} | {{ results['build-sec-cicd_validation-001'].trend_display }} | {{ results['build-sec-cicd_validation-001'].evidence \| default('—') }} |
| build-sec-cicd_validation-002 | Has substantive content (≥ 100 chars of project-specific detail) | error (mandatory) | 1.0 | {{ results['build-sec-cicd_validation-002'].previous_status \| default('—') }} | {{ results['build-sec-cicd_validation-002'].status }} | {{ results['build-sec-cicd_validation-002'].trend_display }} | {{ results['build-sec-cicd_validation-002'].evidence \| default('—') }} |
| build-sec-cicd_validation-003 | Contains project-specific details, not generic boilerplate | warning (recommended) | 0.5 | {{ results['build-sec-cicd_validation-003'].previous_status \| default('—') }} | {{ results['build-sec-cicd_validation-003'].status }} | {{ results['build-sec-cicd_validation-003'].trend_display }} | {{ results['build-sec-cicd_validation-003'].evidence \| default('—') }} |

## 8. Obfuscation & Optimization — weight 3.0 — **required**

**Why this matters:** Obfuscation & Optimization defines which build-time transformations apply, under what configuration, and their cost to debuggability. Without it, a production stack trace problem is a mystery.

**Section Score: {{ sections.obfuscation_optimization.score }} / 100** ({{ sections.obfuscation_optimization.trend_display }})

| Rule | Check | Severity | Weight | Previous | Current | Trend | Evidence |
|---|---|---|---:|---|---|---|---|
| build-sec-obfuscation_optimization-001 | Obfuscation & Optimization section exists | error (mandatory) | 1.5 | {{ results['build-sec-obfuscation_optimization-001'].previous_status \| default('—') }} | {{ results['build-sec-obfuscation_optimization-001'].status }} | {{ results['build-sec-obfuscation_optimization-001'].trend_display }} | {{ results['build-sec-obfuscation_optimization-001'].evidence \| default('—') }} |
| build-sec-obfuscation_optimization-002 | Has substantive content (≥ 100 chars of project-specific detail) | error (mandatory) | 1.0 | {{ results['build-sec-obfuscation_optimization-002'].previous_status \| default('—') }} | {{ results['build-sec-obfuscation_optimization-002'].status }} | {{ results['build-sec-obfuscation_optimization-002'].trend_display }} | {{ results['build-sec-obfuscation_optimization-002'].evidence \| default('—') }} |
| build-sec-obfuscation_optimization-003 | Contains project-specific details, not generic boilerplate | warning (recommended) | 0.5 | {{ results['build-sec-obfuscation_optimization-003'].previous_status \| default('—') }} | {{ results['build-sec-obfuscation_optimization-003'].status }} | {{ results['build-sec-obfuscation_optimization-003'].trend_display }} | {{ results['build-sec-obfuscation_optimization-003'].evidence \| default('—') }} |

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
| Domain | build |
| Standard | documentation-standards |
| Section Rule Files | `audit/deterministic/section/14-build/*.yaml` |
| Auditor | System (deterministic engine) |
| Audit Date | {{ created_at }} |
| Revision | {{ revision_number }} |
| Session | {{ session_id }} |
