# ML Artifact Management — Generation Template

> **Domain:** build
> **Section:** ml_artifact_management
> **Source:** `documentation-standards/14-build-standards.md` §ML Artifact Management
> **Relationships:** `audit/deterministic/document/14-build-relationships.yaml`

Generate the ML Artifact Management section for a Build Plan document.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| `derives_from` | feature / purpose | ML artifact management must align with Feature(04) ML requirements |

## Template

```markdown
## ML Artifact Management

[1-2 sentence description of what ML artifact management covers]
[Statement that this stage is conditional and applies to ML projects]

> **Versioning scheme:**
> - **Models:** [format — e.g., model-{major}.{minor}.{patch}]
> - **Data:** [format — e.g., DVC-tracked, data-v{hash}]
> - **Experiments:** [tool — e.g., MLflow with parameters, metrics, model hashes]

> **Reproducibility requirement:** [same data version → same model]
```

## Examples

**Correct:**
> ML artifacts are versioned using semantic versioning (model-1.2.3). Data versions are tracked with DVC. Experiments are logged in MLflow with parameters, metrics, and model hashes. Each build reproduces the same model from the same data version.

**Incorrect:**
> ML models are saved as model-latest.pkl and overwritten on each training run. Training data is stored locally without versioning.
> *Why wrong: Without versioning, model lineage is untraceable and reproducibility is impossible — this is the core problem ML artifact management solves.*

## Writing Guidance

- **Tone:** technical
- **Voice:** third person
- **Structure:** paragraphs
- **Audience:** engineer
- **Do:** Name specific tools (DVC, MLflow) and their roles; define the versioning scheme format explicitly; state reproducibility requirements (same data version → same model)
- **Don't:** Use generic terms like "version your models" without specifying the scheme; omit the tooling stack; conflate artifact management with model training

**Minimum content:** 2 paragraphs
**Length guidance:** concise
**Required diagrams:** none
**Required cross-references:** Feature(04)

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
