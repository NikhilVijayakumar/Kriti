# Implementation Document — Generation Template

> **Domain:** implementation
> **Source standard:** `documentation-standards/13-implementation-standards.md`
> **Coherence source:** `audit/semantic/document/13-implementation.md`
> **Relationships:** `audit/deterministic/document/13-implementation-relationships.yaml`

Generate a complete Implementation Plan document for a system. The document must satisfy every required section below, in the order defined by the standard.

## Required Sections

| # | Section | semantic_type | Required | Content Requirements |
|---|---------|--------------|----------|---------------------|
| 1 | Purpose | `purpose` | | Scope definition, out-of-scope boundaries, document relationships and responsibilities |
| 2 | Generation Plan | `generation_plan` | ✓ | Step-by-step generation sequence, verification checkpoints, deviation recording process |
| 3 | Refactor Plan | `refactor_plan` | | Target architecture, behavior preservation strategy, before/after test verification |
| 4 | Change Request Plan | `change_request_plan` | | Impact analysis, rollback strategy, test update identification |
| 5 | Enhancement Plan | `enhancement_plan` | | Measurable improvement targets, regression verification, no core behavior changes |
| 6 | Security Fix Plan | `security_fix_plan` | ✓ | Fix approach, vulnerability verification, security re-test requirements |

## Cross-Section Coherence Constraint

> Sourced from `audit/semantic/document/13-implementation.md` Engineering Intent.

Sections within an Implementation Plan must describe the same system without contradicting each other. Specifically:

- The Purpose section must define scope that encompasses every plan type included in the document
- The Generation Plan must align with every Refactor, Change Request, Enhancement, and Security Fix Plan in scope — no plan may contradict the generation sequence
- If multiple plan types exist (e.g., Generation Plan + Security Fix Plan), they must reference the same upstream documents and describe the same system boundaries
- Component names and feature names must be used identically across all plan sections
- The Security Fix Plan must not introduce features or components absent from the Generation Plan

If any section would introduce a component, feature, or boundary not present in another section, reconcile before outputting.

## Sections

---

### 1. Purpose

**Template:**

```markdown
## Purpose

This Implementation Plan documents the as-built record for [feature/system name]. It defines [scope], establishes boundaries via [out of scope], and traces implementation decisions back to [upstream documents].

> **Upstream sources:**
> - Feature(04): [what this plan builds from]
> - Architecture(05): [structural constraints applied]
> - Engineering(07): [code standards followed]
> - Security(03): [security requirements addressed]

> **Out of scope:**
> - [domain or concern not covered, with reason]
```

> **Generation note:** When generating for a specific system, fill this template with *that system's* implementation purpose: what was built, what boundaries apply, and which upstream documents drove the decisions. The meta-level "This document defines the standard for Implementation Plans..." language belongs in the standard itself, not in a generated document.

**Correct example:**
> This Implementation Plan documents the as-built record for the payment processing feature. It covers the payment flow from checkout to confirmation, excludes currency conversion and subscription billing, and traces every implementation decision back to Feature(04) payment requirements and Security(03) PCI-DSS constraints.

**Incorrect example:**
> This section describes the purpose of the project and how we plan to build it.
> *Why wrong: Describes project intent rather than recording what was actually built; confuses Implementation Purpose with Vision or Feature documentation.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** State the feature name and scope explicitly; link every relationship to its upstream document number; define boundaries by listing what is excluded
- **Don't:** Describe project vision or strategy; use vague phrases like "various aspects"; conflate purpose with goals or success criteria

---

### 2. Generation Plan

**Template:**

```markdown
## Generation Plan

### Inputs

| Upstream Document | Section | What It Provides |
|---|---|---|
| [Feature(04)] | [requirements section] | [what this plan extracts] |
| [Architecture(05)] | [constraints section] | [structural constraints applied] |
| [Engineering(07)] | [code standards] | [standards followed] |
| [Security(03)] | [requirements section] | [security requirements addressed] |

### Generation Sequence

1. [Step: verify/validate against upstream doc X]
2. [Step: implement component Y per Architecture(05)]
3. [Step: apply security constraint per Security(03)]
4. [Step: verify coding standards per Engineering(07)]

### Verification Checkpoints

| After Step | Check | Criteria | Source |
|---|---|---|---|
| [step number] | [what is verified] | [pass/fail criteria] | [upstream doc] |

### Deviation Recording

| Deviation | Upstream Source | Rationale | Impact |
|---|---|---|---|
| [what was deviated from] | [which upstream doc] | [why the deviation was made] | [effect on other components] |
```

**Correct example:**
> **Inputs:** Feature(04) notification requirements, Feature Technical(10) message producer runtime behavior, Architecture(05) message queue topology, Engineering(07) async processing standards, Security(03) data-at-rest encryption.
> **Generation Sequence:** 1) Verify notification requirements against Feature(04). 2) Validate runtime behavior against Feature Technical(10). 3) Implement message producer per Architecture(05) queue topology. 4) Apply encryption per Security(03). 5) Verify coding standards per Engineering(07).
> **Verification Checkpoints:** After step 2 — UX matches mockups. After step 5 — all unit tests pass, encryption verified.
> **Deviation Recording:** Deviated from Architecture(05) by using a persistent queue instead of in-memory; rationale: notification delivery must survive process restarts.

**Incorrect example:**
> **Inputs:** None listed.
> **Generation Sequence:** Write code, test it, deploy it.
> **Verification Checkpoints:** None.
> **Deviation Recording:** None needed.
> *Why wrong: No upstream documents referenced, generation sequence lacks tier ordering, no verification checkpoints defined, and deviation recording is dismissed rather than established as a process.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** List every upstream document consumed in the Inputs subsection; number the generation sequence steps in tier order; specify exact verification criteria at each checkpoint
- **Don't:** Omit upstream document references; skip verification checkpoints; write generation steps without referencing which standard each satisfies

---

### 3. Refactor Plan

**Template:**

```markdown
## Refactor Plan

### Target Architecture

[1-2 paragraphs: the desired structure after refactoring, referencing Architecture(05)]

### Behavior to Preserve

| Behavior | Current Contract | Verification Method |
|---|---|---|
| [behavior name] | [current guarantee — e.g., latency, response format] | [how to verify it still works] |

### Verification Strategy

[Description of before/after test comparison — test suite must pass identically]
```

**Correct example:**
> **Target Architecture:** Consolidate the three notification modules (email, sms, push) into a single notification service with a strategy pattern dispatcher, per Architecture(05) service consolidation directive.
> **Behavior to Preserve:** All existing notification delivery contracts — email must arrive within 5 seconds, SMS within 10 seconds, push within 2 seconds. API request/response shapes remain identical.
> **Verification Strategy:** Run full integration test suite (42 tests) before and after refactor. Both runs must produce identical pass/fail results. Benchmark delivery latency for each channel.

**Incorrect example:**
> **Target Architecture:** Rewrite the notification system in a new framework.
> **Behavior to Preserve:** None — this is a full rewrite.
> **Verification Strategy:** Manual testing after deployment.
> *Why wrong: Refactor must preserve existing behavior explicitly, not discard it; target architecture lacks specificity; verification strategy relies on manual testing rather than automated regression.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Specify the target architecture by referencing Architecture(05); enumerate every behavior contract that must be preserved with measurable criteria; require automated test suite pass/fail comparison before and after
- **Don't:** Introduce new features or behavior changes in a refactor; rely on manual testing for verification; omit the before/after test comparison

---

### 4. Change Request Plan

**Template:**

```markdown
## Change Request Plan

### Change Description

**Before:** [current behavior]
**After:** [desired behavior]
**Trigger:** [stakeholder request, updated requirement, or discovered issue]

### Impact Analysis

| Affected Area | Upstream Doc | Impact | Action Required |
|---|---|---|---|
| [module/component] | [Feature(04), Feature Technical(10), etc.] | [what changes] | [what to update] |

### Rollback Strategy

[How to revert the change if verification fails — including database migrations, feature flags, and deployment steps]
```

**Correct example:**
> **Change Description:** The checkout API response must now include a loyalty points balance field. Stakeholder request per updated Feature(04) requirements.
> **Impact Analysis:** Affects checkout API response schema, three downstream crates consuming the response, QA(12) integration tests (8 tests need new assertions), and Feature Technical(10) API documentation.
> **Rollback Strategy:** Deploy with feature flag disabled. If verification fails, toggle flag off — old response schema is restored with zero downtime. Database migration is additive only (new column), safe to leave in place.

**Incorrect example:**
> **Change Description:** Add loyalty points to checkout.
> **Impact Analysis:** Should be straightforward.
> **Rollback Strategy:** Revert the commit.
> *Why wrong: Change description lacks specificity about what and why; impact analysis is vague with no affected modules or tests identified; rollback strategy does not account for database migrations or frontend deployments.*

**Writing guidance:**
- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Describe the exact behavior change with before/after state; list every affected module, API endpoint, and test case in impact analysis; define a rollback strategy that accounts for database migrations and feature flags
- **Don't:** Write vague change descriptions like "improve X"; skip the impact analysis or list no affected components; assume rollback is just "revert the commit"

---

### 5. Enhancement Plan

**Template:**

```markdown
## Enhancement Plan

### Improvement Targets

| Metric | Baseline | Target | Measurement |
|---|---|---|---|
| [metric name] | [current value] | [target value] | [how to measure] |

### Enhancement Approach

[1-2 paragraphs: how the improvement is achieved without changing core behavior, referencing Architecture(05)]

### Regression Verification

| Test Suite | Count | Pass Criteria | Before | After |
|---|---|---|---|---|
| [suite name] | [number of tests] | [all pass] | [result] | [result] |
```

**Correct example:**
> **Improvement Targets:** Reduce search query latency from 800ms to under 200ms at P95. Current baseline measured via Engineering(07) performance benchmarks.
> **Enhancement Approach:** Add a read-through cache layer between the search controller and database, per Architecture(05) caching patterns. No changes to the search algorithm or response format.
> **Regression Verification:** Run the full search integration test suite (23 tests) to confirm identical results. Verify cache invalidation works correctly on data updates. Confirm no change in API response schema.

**Incorrect example:**
> **Improvement Targets:** Make search faster.
> **Enhancement Approach:** Rewrite the search engine from scratch.
> **Regression Verification:** None — performance improvement is the only goal.
> *Why wrong: Improvement targets are not measurable; enhancement approach changes core behavior rather than improving existing functionality; regression verification is absent, risking broken existing features.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Define improvement targets as measurable metrics with baseline and target values; describe the enhancement approach as additive layers that do not alter core behavior; specify the regression test suite that must pass unchanged
- **Don't:** Set improvement targets without measurable criteria; rewrite core components instead of layering improvements; skip regression verification or assume no breakage

---

### 6. Security Fix Plan

**Template:**

```markdown
## Security Fix Plan

### Vulnerability Description

- **Location:** [endpoint, parameter, file path]
- **Severity:** [critical | high | medium | low]
- **Threat model reference:** Security(03) [threat ID or entry]
- **Description:** [what was found and how it was discovered]

### Fix Approach

[1-2 paragraphs: how the vulnerability is addressed, referencing Engineering(07) secure coding standards]

### Verification

[Concrete steps to confirm the fix resolves the vulnerability — include specific test payloads]

### Re-test Requirements

| Test Suite | Category | Count | Source |
|---|---|---|---|
| [suite name] | [security category] | [number of tests] | QA(12) |
```

**Correct example:**
> **Vulnerability Description:** SQL injection vulnerability in the user search endpoint (GET /api/users?name=). User-supplied `name` parameter is interpolated directly into a SQL query string without parameterization. Identified in Security(03) threat model as high-severity for data exfiltration.
> **Fix Approach:** Replace string interpolation with parameterized queries using the database driver's prepared statement API, per Engineering(07) secure coding standards. Apply fix to all three search endpoints (users, products, orders).
> **Verification:** Confirm parameterized queries reject injected payloads — test with `'; DROP TABLE users; --` and `1' OR '1'='1`. Verify legitimate search results are unchanged.
> **Re-test Requirements:** Run QA(12) full security test suite (15 tests). specifically the SQL injection test category (5 tests). Verify no new injection vectors introduced in affected endpoints.

**Incorrect example:**
> **Vulnerability Description:** Security bug in search.
> **Fix Approach:** Add input validation.
> **Verification:** Tested manually.
> **Re-test Requirements:** None specified.
> *Why wrong: Vulnerability description lacks location, severity, and upstream reference; fix approach is vague without specifying the exact remediation technique; verification is manual rather than reproducible; re-test requirements are missing entirely.*

**Writing guidance:**
- **Tone:** technical
- **Voice:** imperative
- **Structure:** bullet lists
- **Audience:** engineer
- **Do:** Specify the exact vulnerability location (endpoint, parameter, file path) and its severity; reference the Security(03) threat model entry; define reproducible verification steps with specific attack payloads; list the QA(12) security test suite and category counts
- **Don't:** Write vague descriptions like "security issue in search"; use manual testing as the sole verification method; omit re-test requirements or skip checking for new vulnerability introduction

---

## Output Contract

Output a single complete markdown document containing all 6 sections above, in the order listed. Each section must:

1. Use the template skeleton as its structural basis
2. Fill every placeholder with domain-appropriate content (not lorem ipsum)
3. Satisfy the Writing Guidance for its section
4. Be consistent with every other section (cross-section coherence constraint above)
5. Include diagrams where Required diagrams are specified
6. Omit implementation details (technology names, library versions, configuration values, code snippets)
