# Security — Generation Template

> **Domain:** architecture
> **Section:** security_considerations
> **Source:** `documentation-standards/05-architecture-standards.md` §Security
> **Relationships:** `audit/deterministic/document/05-architecture-relationships.yaml`

Generate the Security section for an Architecture document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | security / purpose | Security section must align with the Security domain's Purpose (threat model, security principles) |

## Template

```markdown
## Security

### Trust Boundaries
[Description of where trust changes — external/internal, component-to-component]

### Threat Model
[Key threats, attack vectors, and mitigations at the architectural level]

### Security Controls
[Architectural security measures — access control model, data protection requirements]
```

## Examples

**Correct:**
> **Trust Boundaries**
> - **External → Ingestion:** Untrusted external systems submit data; Ingestion validates all inputs before internal processing.
> - **Ingestion → Transform:** Trusted boundary — both are internal components communicating over an internal network.
>
> **Threat Model**
> - **Spoofing:** External systems may impersonate legitimate data sources. Mitigation: authenticated submission with signed payloads.
> - **Data tampering:** Malicious payloads may attempt to exploit downstream processing. Mitigation: schema validation at the Ingestion boundary.

**Incorrect:**
> We use JWT tokens signed with RS256 via the `jsonwebtoken` library. Passwords are hashed with bcrypt (12 rounds). The API gateway uses Kong 3.4 with rate limiting of 100 req/min. All traffic is encrypted with TLS 1.3.
> *Why wrong: specifies concrete libraries, library versions, configuration values, and protocol versions — these are Engineering implementation details, not architectural security controls.*

## Writing Guidance

- **Tone:** technical
- **Voice:** imperative
- **Structure:** mixed
- **Audience:** architect
- **Do:** Define every trust boundary with source and destination; document the threat model before controls; tie each control to a specific threat
- **Don't:** Name specific security libraries or libraries' configuration values; describe implementation of encryption or authentication; omit a threat that has no documented mitigation

**Required subsections:** Trust Boundaries, Threat Model
**Optional subsections:** Security Controls, Access Control Model
**Required diagrams:** trust boundary diagram
**Required cross-references:** Component Model, Data Flow, Philosophy(02)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
