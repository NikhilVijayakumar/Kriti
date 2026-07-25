# Integration Contract — Generation Template

> **Domain:** external-context
> **Section:** integration_contract
> **Source:** `documentation-standards/08-external-context-standards.md` §Integration Contract
> **Relationships:** `audit/deterministic/document/08-external-context-relationships.yaml`

Generate the Integration Contract section for an External Context document.

## Relationships

This section has the following outgoing relationships that must be satisfied:

| Relationship | Target | Constraint |
|---|---|---|
| `informs` | engineering / build_standards | Integration Contract must describe the external system's interface in terms engineers can build against |
| `informs` | feature_technical / communication_paths | Integration Contract must define the communication surface that feature technical designs reference |

## Template

```markdown
## Integration Contract

[Integration surface overview — what the external system exposes]

### Endpoints / Protocols

| Endpoint / Protocol | Purpose | Method | Required | Authentication | Notes |
|--------------------|---------|--------|----------|---------------|-------|
| [Path or protocol name] | [what it does] | [HTTP method / protocol type] | [yes/no] | [auth type] | [constraints] |

### Data Formats

| Direction | Format | Content Type | Encoding | Constraints |
|-----------|--------|-------------|----------|-------------|
| Request | [format] | [MIME type] | [encoding] | [limits] |
| Response | [format] | [MIME type] | [encoding] | [limits] |

### Authentication

| Aspect | Detail |
|--------|--------|
| Mechanism | [OAuth 2.0, API key, mutual TLS, etc.] |
| Flow | [client credentials, authorization code, etc.] |
| Token type | [Bearer, MAC, etc.] |
| Token lifetime | [expiration duration] |
| Refresh | [supported / not supported] |
| Credential storage | [how credentials should be stored] |

### Error Handling

| Error Code / Status | Meaning | Retry | Backoff Strategy |
|---------------------|---------|-------|-----------------|
| [code] | [what it means] | [yes/no] | [strategy] |

### Versioning

| Aspect | Detail |
|--------|--------|
| Versioning scheme | [URL path, header, query parameter] |
| Current version | [version identifier] |
| Deprecation policy | [how deprecation is communicated] |
| Migration guidance | [how to upgrade between versions] |
```

## Examples

**Correct:**
> The external system exposes a REST API over HTTPS. Authentication uses OAuth 2.0 client credentials flow.
>
> | Endpoint / Protocol | Purpose | Method | Required | Authentication | Notes |
> |--------------------|---------|--------|----------|---------------|-------|
> | `/v1/data` | Submit data | POST | Yes | Bearer token | Max 1MB payload |
> | `/v1/data/{id}` | Retrieve data | GET | Yes | Bearer token | Returns 404 for deleted records |
>
> Authoritative documentation: `https://docs.externalsystem.example/api`.

**Incorrect:**
> Here is the code we use to call the API:
> ```python
> resp = requests.post("https://api.externalsystem.example/v1/data", ...)
> ```
> *Why wrong: Includes implementation code rather than describing the contract. The Integration Contract should define what the external system exposes, not how the repository calls it.*

## Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** mixed
- **Audience:** engineer
- **Do:** Describe contract surface in implementation-neutral terms; always include the authoritative documentation URL; distinguish required from optional endpoints; include ALL subsections (Endpoints/Protocols, Data Formats, Authentication, Error Handling, Versioning) as part of this one section
- **Don't:** Paste code snippets or client implementations; document internal request/response transformation logic; omit authentication mechanism details; treat subsections as standalone sections

**Minimum content:** 1 subsection
**Length guidance:** moderate
**Required diagrams:** none
**Required cross-references:** authoritative external documentation

**Required subsections:** Endpoints / Protocols, Authentication
**Optional subsections:** Data Formats, Error Handling, Versioning

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
