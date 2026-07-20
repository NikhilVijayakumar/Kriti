# python_hackathon — Domain Strengthening Proposal

Every one of the 10 domains' actual audit content — `domains/*-standards.md`
(the human-readable "what good looks like" doc), the deterministic
YAML rules, and where relevant the semantic rubric — is thinner than
the competition rules it's meant to enforce. This proposal is grounded
in reading every one of those files directly, not assumed from the
domain names. No code changes made — proposal only.

**Two different kinds of gap found, not one**, and they need different
fixes:

1. **Computed-but-unused data** — the exact "stranded evidence"
   pattern already fixed once this conversation for `detail`/
   `severity` (visualization-and-detail-templates-proposal.md). Found
   again here: `audit_mlops.py` and `audit_python.py` already compute
   richer signals than their YAML rules check.
2. **Genuinely missing scope** — checks that don't exist at all, in
   script or rule, because the domain's own `domains/*-standards.md`
   never asked for them. This is most of what you listed.

---

## 0. Ground truth — what's actually in each file today

`domains/*-standards.md` is the shallowest layer in the whole system —
most files are 1-3 bullet points under "Expected Evidence." Quoted in
full where short enough to show exactly how thin:

| Domain | `domains/*-standards.md` (verbatim, abbreviated where long) | Deterministic rules | Gap vs. your message |
|---|---|---|---|
| `06-mlops` | "Data Versioning: presence of DVC configuration files" — **one sentence, no mention of MLflow, drift, or CI/CD at all** despite the semantic rubric asking about all three | `mlp-001`/`mlp-002`: DVC/MLflow file-presence only | Confirmed: no drift check, no CI/CD check, "doesn't check mlflow" is literally true — `mlflow_run_count` is computed by `audit_mlops.py` (already deepened earlier this conversation) but **no rule reads it** |
| `08-team-workflow` | Covers commits/authors/task-division — closest to complete of the 10 | `tw-001`–`tw-004`: commit count, author count, conventional-commit rate, PR-merge evidence | Your "reliability, speed, clean structuring" and "did they divide tasks smoothly" phrasing isn't in the current semantic prompt at all — it asks about self-organization generically, not the specific reliability/speed/structure framing you want |
| `10-ai-explanations` | "Inclusion of known LLM SDKs... Prompt Engineering... Output Quality" | `ai-001`/`ai-002`: LLM SDK dependency presence, prompt-file presence | **Structural mismatch, not just thinness** — see §2, this is the significant one |
| `07-runtime` | "The final execution artifact must be clearly identifiable" — **one sentence**, doesn't mention VRAM/format/timing/input-boundary at all, despite `run-002`–`run-005` already enforcing most of them | `run-001`–`run-005`: entrypoint, format, VRAM, 30s timing, output-contract schema | VRAM/format/30s/output-contract are **already built** (confirmed by direct read) — only the *input*-boundary half of your ask is missing, see §3 |
| `02-engineering` | "Automated complexity checks and static type analysis" | `eng-001`–`eng-005`: config presence + (per earlier work this conversation) actual radon/mypy execution | `radon_high_complexity_count`/`mypy_error_count` already computed by `audit_python.py`, **no rule reads them** — same stranded-data pattern as mlops |
| `09-data-quality` | "Identifiable local datasets... sourcing... methodology" | `dq-001`/`dq-002`: file presence, README source-link regex | Zero coverage of splits/overfitting/leakage/feature-engineering — see §4, this doesn't fit here as-is |

## 1. mlops — wire up already-computed data, then add what's still missing

**Wire-up (no new computation, same pattern as the earlier `detail`/
`severity` fix)**: `audit_mlops.py` already returns `dvc_stage_count`
and `mlflow_run_count` — real usage signals, not just "the tool is
configured." Two new rules using data that already exists:

```yaml
  - id: mlp-003
    description: "DVC pipeline has real stages, not an empty/placeholder file"
    condition: "dvc.yaml declares at least 1 pipeline stage"
    severity: warning
    weight: 1.0
    mandatory: false
    evidence: {type: tool_execution, target: dvc_stage_count, threshold: 1, op: gte}

  - id: mlp-004
    description: "MLflow has recorded at least one real run"
    condition: "mlruns/ contains at least 1 run directory"
    severity: warning
    weight: 1.0
    mandatory: false
    evidence: {type: tool_execution, target: mlflow_run_count, threshold: 1, op: gte}
```

**Genuinely missing — data/artifact versioning, drift, CI/CD**, none
of which exist in script or rule today:

- **Data/artifact versioning beyond DVC presence**: check `dvc.yaml`
  for `outs:` entries referencing model artifact paths specifically
  (not just any pipeline stage) — distinguishes "we version our data"
  from "we version our model," both currently invisible.
- **Drift analysis**: this is the one item on your list that's
  genuinely hard to check *deterministically* — drift is a property of
  two datasets compared over time, not a static file. Two honest
  options: (a) deterministic proxy — check for a `data/` directory
  with more than one dated/versioned subfolder or DVC-tracked file
  revision history (weak signal, but real and checkable without
  running anything), or (b) semantic-only — ask the rubric whether the
  README documents a drift-monitoring plan (methodology, not
  execution). Recommend **(b)**, consistent with your "no performance
  check expected" instruction elsewhere — actual drift measurement
  would require running the model against held-out data, which is
  explicitly out of scope.
- **CI/CD**: currently checked nowhere in this system at all, not just
  mlops. New rule, deterministic, cheap: presence of `.github/workflows/*.yml`
  or `.gitlab-ci.yml` with content matching a real pipeline (`on:`
  triggers, `jobs:` — not just an empty stub file). Arguably belongs
  in `engineering` (§ below) rather than `mlops` — flagged as an open
  question (§7) since CI/CD spans both "is the code tested
  automatically" (engineering) and "is the ML pipeline reproducible"
  (mlops) concerns.

## 2. ai-explanations — reframe, not just add rules

**This is the most consequential finding, not a small fix.** Your
message: *"ai explainability mainly should look for readme not in
model... these changes are expected to solve without using llm, no
performance check expected."*

Read against the current rubric, this identifies a real conceptual
mismatch, not just missing depth. The current domain (`ai-001`/
`ai-002` + the semantic prompt) is built around **the submission using
an LLM to generate human-readable text explanations** — it checks for
`openai`/`anthropic`/`langchain` SDK dependencies and prompt-template
files, and its semantic rubric asks a judge-model to rate "the quality
... of the automated AI text explanations generated by their system."

That's a different concept from **ML explainability** (SHAP, feature
importance, attention weights, LIME, permutation importance — the
actual technique that explains *why the model predicted what it
predicted*), which is what "AI explanations" more naturally means for
a prediction-model hackathon and what your message is pointing at:
audit whether the team **documented** their explainability
methodology in the README, structurally, without requiring an LLM to
exist in the stack at all and without running the model to check
prediction quality.

**Proposed reframe** (new `domains/10-ai-explanations-standards.md`
content — prose first, since that's the layer everything else should
derive from and it's currently the thinnest):

> The submission must document *why* its predictions are trustworthy
> — not by using an LLM to narrate them, but by describing a concrete
> interpretability method applied to the model itself (feature
> importance, SHAP/LIME, coefficient inspection for linear models,
> attention visualization for transformers, or an equivalent
> technique appropriate to the model class used). This is a
> documentation-quality and methodology-presence check — it does not
> require the LLM SDKs previously assumed, and does not evaluate
> prediction accuracy.

**Deterministic rules — replacing `ai-001`/`ai-002`, not additive**:

```yaml
  - id: ai-001
    description: "README documents an explainability/interpretability method"
    condition: "README.md mentions a recognized interpretability technique"
    severity: warning
    weight: 1.0
    mandatory: false
    evidence:
      type: regex_match
      target: README.md
      patterns: ["SHAP", "LIME", "feature importance", "permutation importance",
                 "attention weight", "interpretab", "explainab"]

  - id: ai-002
    description: "README documents specific prediction capabilities"
    condition: "README.md mentions match prediction or player prediction capabilities"
    severity: warning
    weight: 1.0
    mandatory: false
    evidence:
      type: regex_match
      target: README.md
      patterns: ["match winner", "win probability", "draw probability",
                 "scoreline", "first team to score", "total goals",
                 "both teams score", "goal scoring", "expected goals",
                 "assist probability", "clean sheet", "player predict"]

  - id: ai-003
    description: "Prediction methodology documented in README"
    condition: "README.md explains how predictions are generated (model type, features, or approach)"
    severity: warning
    weight: 1.0
    mandatory: false
    evidence:
      type: regex_match
      target: README.md
      patterns: ["prediction method", "model approach", "feature set",
                 "training data", "algorithm", "ensemble", "regression",
                 "classification", "neural network", "random forest",
                 "gradient boost", "xgboost", "lightgbm"]
```

**Decision on ai-002 evidence type**: Changed from `file_presence` with
`patterns` (unsupported by `evaluate_rules.py`'s `file_presence`
implementation) to `regex_match` on `README.md`. This checks the
documented prediction capabilities, not file-level artifacts —
consistent with the "README-only, no model execution" constraint.

The old LLM-SDK-presence check (`ai-001` today) doesn't disappear from
the system — it's simply not what *this* domain should measure. If
a team genuinely does use an LLM as part of their product (not
unreasonable for some hackathon entries), that's better captured as
an `engineering`-domain dependency-presence note, not the
explainability domain's core signal.

**Semantic rubric — rewritten to match**, README-only, explicitly no
model execution, now covers prediction capabilities:

```
Analyze the README.md only. Do not evaluate model outputs or run any
code. Does the team document a concrete interpretability method
(e.g. SHAP, feature importance, attention visualization) applied to
their model? Does the README describe specific prediction capabilities
(match winner, scoreline, goal probabilities, player predictions)?
Is the explanation of *why* the model makes its predictions clear
enough that a non-expert judge could follow the reasoning? Score based
on documentation clarity and methodological soundness — not on whether
the underlying prediction is accurate.
```

## 3. runtime — input-boundary is the one real gap left

Confirmed by direct read (§0): `run-002` (format), `run-003` (VRAM),
`run-004` (30s), `run-005` (output-contract schema) already exist and
already work — your hardware-ceiling/format/speed/output items are
**not missing**, they were built earlier this conversation. What's
new in your message and genuinely absent: **the input side of the API
contract** — "must accept only the two competing countries as input...
no human intervention or manual data-tweaking allowed on match day."

`run-005` checks predict()'s *output* shape; nothing checks its
*input* shape. New rule:

```yaml
  - id: run-006
    description: "predict() signature accepts only team_a/team_b, no other params"
    condition: "predict() function signature has exactly the params team_a, team_b (no extra required args, no config/override params)"
    severity: error
    weight: 2.0
    mandatory: true
    evidence:
      type: script_output
      script: script/audit_model_artifact.py
      check: inference.input_contract_valid
      expected: true
```

Requires extending `audit_model_artifact.py`'s existing sandboxed
inference call (`_run_inference_sandbox`, already built) to introspect
`predict()`'s signature via `inspect.signature()` before invoking it —
same script, same sandbox, one more check alongside the existing
output-contract validation, not a new mechanism.

## 4. Feature engineering / overfitting / data-split — doesn't fit any existing domain, decide before building

**No domain covers this today**, confirmed — `data-quality` (09) is
about data *sourcing*, not modeling *methodology*. Your list (feature
engineering, overloading, overfitting, underfitting, data split) is a
coherent, real category: **model-development-methodology**, distinct
from data-quality, distinct from runtime.

**Constraint from your message, taken seriously**: "no performance
check expected" — this rules out the obvious approach (actually
re-run the model against a held-out split and measure the
train/test gap, which is how you'd *really* detect overfitting). What
remains is **documentation and structural evidence of good practice**,
same shape as the ai-explanations reframe above:

- Deterministic: does a `train_test_split` call (or equivalent
  `sklearn.model_selection`/manual split logic) appear anywhere in the
  codebase — a grep-able structural signal, not a performance
  measurement.
- Deterministic: does the README or a notebook document validation
  methodology (cross-validation, held-out set size, etc.) — regex
  against known terms (`cross-validation`, `k-fold`, `validation set`,
  `train/test split`).
- Semantic: does the README's methodology section describe feature
  engineering decisions (why these features, any engineered/derived
  features, any features explicitly dropped to avoid leakage) —
  judged from prose, never from running anything.

**Placement — decided: extend `data-quality` (09)**. Rationale: avoids
the full cascade of adding an 11th domain (`weights.yaml`,
`DOMAIN_KEY_MAP`, leaderboard columns, `tiers.yaml`, all aggregation
YAMLs would need a new entry each). "Data quality" already implicitly
covers "was this data used correctly," and the cascade cost of a new
domain is real, not just paperwork.

## 5. engineering — wire up already-computed data, then structure check

**Wire-up**: same pattern as §1 — `audit_python.py` already computes
`radon_high_complexity_count` and `mypy_error_count`; no rule reads
either. Two new rules:

```yaml
  - id: eng-006
    description: "No high-complexity functions (radon grade C or worse)"
    condition: "radon_high_complexity_count == 0"
    severity: warning
    weight: 1.0
    mandatory: false
    evidence: {type: tool_execution, target: radon_high_complexity_count, threshold: 0, op: eq}

  - id: eng-007
    description: "No mypy type errors"
    condition: "mypy_error_count == 0"
    severity: warning
    weight: 1.0
    mandatory: false
    evidence: {type: tool_execution, target: mypy_error_count, threshold: 0, op: eq}
```

**Genuinely missing — "code structure" (your term)**: separation of
concerns at the folder level (e.g. `data/`, `model/`, `api/` or
equivalent — not literally these names, but *some* evident separation
rather than one flat script). Deterministic proxy: count top-level
Python-containing directories (excluding `tests/`, `.venv`, etc.) —
1 directory is a flag (everything in one place), 2+ is a pass. Weak
signal, same honesty standard as the drift-analysis note in §1 — this
can't detect *good* structure, only detect the complete absence of any
structure, which is still worth catching.

## 6. team-workflow — closest to complete, still needs the reframe you asked for

Deterministic side (`tw-001`–`tw-004`) is already the most solid
domain in the system — real `git log` analysis, not file-presence
checks. What's missing is specifically your framing: **"reliability,
speed, and clean structuring"** as the semantic judgment criteria,
which the current prompt doesn't use at all (it asks generically about
self-organization). Rewrite the semantic prompt to match your exact
framing:

```
Analyze the README.md, commit history, and project structure.
Evaluate three things explicitly: (1) Reliability — does the project
run without manual intervention, are dependencies pinned and
reproducible; (2) Speed — is there evidence the team worked
efficiently (steady commit cadence rather than one late burst); (3)
Clean structuring — is the codebase organized into clear separations
(data collection, model training, API serving) rather than one
monolithic script. Did the team divide tasks smoothly, and is there
evidence of peer-reviewed pull requests rather than one person doing
all the work? Score based on all three dimensions.
```

No deterministic change needed here — `tw-001`–`tw-004` already back
the "did multiple people contribute, is there PR evidence" half; this
is purely a semantic-rubric rewrite to match your exact language.

## 7. Decisions recorded

1. **§4 placement** — extend `data-quality` (09), not an 11th domain.
2. **§1 CI/CD check** — lives in `engineering` (CI is a code-quality practice first, ML-reproducibility second).
3. **§2 reframe** — replaces `ai-001`/`ai-002` entirely (old LLM-SDK check stops being this domain's signal).
4. **§1 drift approach** — semantic-only (matches "no performance check" constraint).
5. **§2 ai-002 evidence type** — changed from `file_presence` with `patterns` to `regex_match` on `README.md` (checks documented prediction capabilities, not file artifacts).
6. **§2 prediction scope** — added match predictions (winner, scoreline, goals) and player predictions (goals, assists, clean sheets) to ai-explanations domain.

## 8. Verification checklist

- [ ] §1 — `mlp-003`/`mlp-004` exist and read `dvc_stage_count`/
      `mlflow_run_count` (already-computed fields, confirmed present
      in `audit_mlops.py`'s current output — no script change needed
      for these two rules specifically).
- [ ] §1 — CI/CD presence rule exists in `engineering` (§7 decision),
      checking real workflow content, not just file presence.
- [ ] §2 — `domains/10-ai-explanations-standards.md`,
      `audit/deterministic/document/10-ai-explanations.yaml`, and
      `audit/semantic/document/10-ai-explanations.yaml` all describe
      the same concept (documented interpretability methodology +
      prediction capabilities) — no file still describes the old
      LLM-SDK/prompt-quality framing.
- [ ] §2 — `ai-002` uses `regex_match` on README for prediction
      capabilities (match winner, scoreline, goals, player predictions),
      not `file_presence` with `patterns`.
- [ ] §3 — `run-006` exists; `audit_model_artifact.py`'s sandboxed
      inference call introspects `predict()`'s signature before
      calling it, not just its output after.
- [ ] §4 — new rules exist in `09-data-quality.yaml` for
      train/test-split detection and methodology-documentation
      regex (extending data-quality, not adding 11th domain).
- [ ] §5 — `eng-006`/`eng-007` exist and read `radon_high_complexity_count`/
      `mypy_error_count`; a folder-structure proxy rule exists.
- [ ] §6 — `08-team-workflow.yaml`'s semantic prompt explicitly names
      reliability/speed/clean-structuring as scored dimensions, not
      the old generic self-organization phrasing.
- [ ] All `domains/*-standards.md` files touched by this proposal are
      updated to match their rule files — the prose stays the source
      of truth other files derive from, not left stale while the YAML
      changes underneath it.
