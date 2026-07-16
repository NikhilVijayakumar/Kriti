## API Versioning

> *Structural rules: `audit/deterministic/section/07-engineering/09-versioning.yaml`*

### Template

> **minimum_content:** 1 paragraph
> **length_guidance:** concise
> **diagram_requirements:** none

```markdown
This repository uses [URL Path / Header / Query] versioning for all public API endpoints.

[Describe the versioning strategy, e.g., `/v1/`, `/v2/`.]

## Deprecation Policy

[Describe the timeline and strategy for deprecating older API versions.]
```

**Required subsections:** Deprecation Policy
**Optional subsections:** none
**Required diagrams:** none
**Required cross-references:** none

### Examples

**Correct:**
> All external APIs are versioned in the URL path (e.g., `/api/v1/users`). Deprecated endpoints return a `Warning` header and are supported for 6 months post-deprecation.

**Incorrect:**
> We version our APIs when breaking changes occur.
> *Why wrong: Too vague. Doesn't specify how versioning is implemented.*

### Writing Guidance

- **Tone:** authoritative
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** backend engineer
- **Do:** Define the exact mechanism for versioning.
- **Don't:** Leave ambiguity about when a new version is required.
