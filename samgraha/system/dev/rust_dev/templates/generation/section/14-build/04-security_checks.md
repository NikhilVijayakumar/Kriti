# Security Checks — Generation Template

> **Domain:** build
> **Section:** security_checks
> **Source:** `documentation-standards/14-build-standards.md` §Security Checks
> **Relationships:** `audit/deterministic/document/14-build-relationships.yaml`

Generate the Security Checks section for a Build Plan document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | security / mitigation_strategies | Security checks must map to Security(03) mitigation strategies and threat categories |

## Template

```markdown
## Security Checks

[1-2 sentence description of what security checks cover]
[Statement that checks are mandatory and map to Security(03) threat categories]

> **Checks performed:**
> - [check type] — maps to Security(03) [threat category]

> **Severity thresholds:**
> - **Critical:** [action — e.g., block build]
> - **High:** [action — e.g., block build]
> - **Medium:** [action — e.g., log warning]
> - **Low:** [action — e.g., log info]
```

## Examples

**Correct:**
> Security checks run dependency vulnerability scanning, SAST on source code, and secrets detection. All critical and high severity findings block the build. Checks map to the threat categories defined in Security(03).

**Incorrect:**
> Security checks run optional vulnerability scans and log warnings for critical findings without blocking the build.
> *Why wrong: Security checks must be mandatory with blocking thresholds for critical/high findings — logging warnings defeats the purpose of security validation.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Define concrete severity thresholds (critical/high block, low/medium log); map each check to a Security(03) threat category; specify what happens when a check fails
- **Don't:** Allow security checks to be optional; use vague terms like "thoroughly" instead of measurable thresholds; omit the blocking behavior for critical findings

**Minimum content:** 2 paragraphs
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** Security(03)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
