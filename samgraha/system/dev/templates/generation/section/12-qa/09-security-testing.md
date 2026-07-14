# Security Testing — Generation Template

> **Domain:** qa
> **Section:** security_testing
> **Source:** `documentation-standards/12-qa-standards.md` §Security Testing
> **Relationships:** `audit/deterministic/document/12-qa-relationships.yaml`

Generate the Security Testing section for a QA document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | security / threat_model | Security test types must map to Security(03) threat categories |

## Template

```markdown
## Security Testing

### Security Test Types

| Test Type | Threat Category Coverage | Tool | Frequency | Severity Threshold |
|-----------|------------------------|------|-----------|-------------------|
| SAST | [categories] | [Tool] | [frequency] | [Critical/High/Medium] |
| DAST | [categories] | [Tool] | [frequency] | [Critical/High/Medium] |
| Dependency scanning | [categories] | [Tool] | [frequency] | [Critical/High/Medium] |
| Secrets detection | [categories] | [Tool] | [frequency] | [Critical/High/Medium] |

### Severity Thresholds

| Severity | Fail Build? | Required Response Time | Examples |
|----------|------------|----------------------|----------|
| Critical | Yes | [X hours] | [Examples] |
| High | Yes | [X days] | [Examples] |
| Medium | No | [X days] | [Examples] |
| Low | No | [X sprints] | [Examples] |
```

## Examples

**Correct:**
> ### Security Test Types
>
> | Test Type | Threat Category Coverage | Tool | Frequency | Severity Threshold |
> |-----------|------------------------|------|-----------|-------------------|
> | SAST | Injection, XSS, insecure deserialization | Static analyzer | Every commit | Critical |
> | DAST | Authentication bypass, privilege escalation | DAST scanner | Nightly build | Critical |
> | Dependency scanning | Known CVEs in third-party packages | Dependency checker | Daily | High |
> | Secrets detection | Hardcoded credentials, API keys | Secret scanner | Every commit | Critical |
>
> ### Severity Thresholds
>
> | Severity | Fail Build? | Required Response Time | Examples |
> |----------|------------|----------------------|----------|
> | Critical | Yes | 4 hours | Remote code execution, SQL injection |
> | High | Yes | 24 hours | Authentication bypass, privilege escalation |
> | Medium | No | 7 days | Information disclosure, missing security headers |
> | Low | No | Next sprint | Verbose error messages, outdated TLS version |

**Incorrect:**
> Run security scans and fix any issues found. Use whatever security tools the team prefers.
> *Why wrong: security testing requires explicit test types mapped to threat categories, severity thresholds, and scan frequency.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** tables
- **Audience:** security engineer
- **Do:** Map each test type to Security(03) threat categories; define severity thresholds with explicit fail-build rules and response times; specify scan frequency for every test type
- **Don't:** List security tools without stating what threat categories they cover; use severity labels without defining build impact; omit scan frequency

**Required subsections:** Security Test Types table, Severity Thresholds table
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** Security(03), Engineering(07), Implementation(13)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
