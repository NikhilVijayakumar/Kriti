# python_hackathon — System Proposal

## 1. Class / Position in Taxonomy

Class `hackathon`, no subclass, no `extends`/base — standalone, single
member (per your instruction: hackathon needs no further
categorization). Proposed path `hackathon/python_hackathon/` (currently
flat at `samgraha/system/python_hackathon/`, no `system.yaml` exists
yet).

## 2. What It Has

10 domains: infrastructure, engineering, testing, documentation,
security, mlops, runtime, team-workflow, data-quality, ai-explanations.

**Tier structure** (`00-domain-relationships.md`):

| Tier | Domains |
|---|---|
| 1 | infrastructure, security, team-workflow |
| 2 | engineering, documentation |
| 3 | testing, data-quality, mlops |
| 4 | runtime, ai-explanations |

Edges: `infrastructure/security/team-workflow --guides--> engineering`
(all mandatory), `engineering --requires--> testing`, `testing
--validates--> runtime`, `documentation --informs--> engineering`
(non-mandatory), `mlops --requires--> infrastructure`, `data-quality
--informs--> mlops` (non-mandatory), `ai-explanations --validates-->
runtime` (non-mandatory). Same closed `relationship_types` vocabulary
as the academic systems (`guides`/`requires`/`validates`/`informs`).

**File inventory:**
- `documentation-standards/`: 10 files
- `audit/`: **both `deterministic/document/` (10 files) AND
  `semantic/document/` (10 files)** — this class has a real
  deterministic layer, unlike the academic class
- `calculation/`: the richest calculation structure of any system
  examined — `aggregation/domain/` (10 files), `deterministic/document.yaml`
  + `deterministic/document/` (10 files) + `deterministic/section.yaml`,
  `semantic/document.yaml` + `semantic/ensemble/` (10 files) +
  `semantic/section.yaml`, `summary/{final_score,score_bands,trend}.yaml`,
  `validation/scoring_validation.yaml`, plus a top-level `weights.yaml`
  (domain-weighted scoring with documented rationale per domain — e.g.
  `runtime: weight 15, "Highest weight: model must run within 12GB
  VRAM and 30s constraint"`)
- `plan/usecase/`: **does have `repo_new/{case_1_no_documentation,case_2_has_documentation}/tier_{1-4}/{01-generation,02-audit,03-fix}.md`**
  — but `01-generation.md` files are literal placeholder stubs, e.g.
  tier 1's reads in full: *"# Step 01-generation.md for Tier 1 /
  Placeholder content for case_1_no_documentation scenario."* Confirms
  LIM-001's "audit-only, no generation" characterization in spirit —
  the scaffolding exists but was never actually authored, unlike the
  dev class's real generation procedures.
- `templates/reports/`: `domain/{NN-name}-{deterministic,semantic,summary}.md`
  ×10 domains (30 files) + `global-leaderboard.md` + `team-final-summary.md`
- `script/`: **12 real Python scripts** (§3)

## 3. Existing Script Architecture — Reference Implementation

Organized around domain-specific audit scripts plus separate
aggregation scripts, **not** the author guide's 6-capability
(`init`/`validate`/`calculate`/`report`/`scaffold`/`plan_generation`)
file layout, and **not** the dev class's `mapping.yaml`/`policy.yaml`/
`schema/`/`windows`/`ubuntu` split — a third, genuinely different
organizational pattern:

| Script | What it does (read directly, not inferred) | Closest capability |
|---|---|---|
| `audit_git.py` | Git history analysis for team-workflow: conventional-commit regex, gitflow branch-name regex, commit/author counts | `validate` (one domain) |
| `audit_infrastructure.py` | Checks for `uv.lock`, `Dockerfile`, `docker-compose` presence | `validate` (one domain) |
| `audit_mlops.py` | Checks for DVC/MLflow config presence | `validate` (one domain) |
| `audit_model_artifact.py` | **The most sophisticated script in the system** — validates hackathon model artifacts against explicit competition rules: file format (`.pt`/`.pth`/`.pkl` only), 12GB VRAM load constraint, 30s inference-time constraint, JSON output-schema contract, and runs everything with network access blocked for the inference subprocess | `validate` (runtime/mlops) |
| `audit_python.py` | Static analysis config detection + execution (Radon, Bandit, Mypy) | `validate` (engineering) |
| `audit_security.py` | Runs `bandit` SAST, regex-based hardcoded-secret scanning (API keys, tokens, `sk-` prefixed strings) | `validate` (security) |
| `audit_testing.py` | Test discovery, `pytest`+coverage execution, result parsing | `validate` (testing) |
| `score_aggregator.py` | Phase 1: raw per-team/per-domain score aggregation from a directory of per-model JSON results (`results/{team}/{domain}/{model}.json`) | `calculate` (partial) |
| `statistics.py` | Phase 2: MAD-based robust z-score per domain across teams, `tanh`-bounded bonus/penalty (±~4.9 points at z=±2) | `calculate` (partial) |
| `leaderboard.py` | Phase 3-4: weighted score (domain weights from `weights.yaml`) + semantic quality bonus (inter-model agreement) + final leaderboard | `calculate` + `report` (partial) |
| `validate_scores.py` | Validates `weights.yaml` sums to 100, all weights positive, score bounds | pipeline pre-check, no direct author-guide equivalent |
| `verify_standard.py` | Cross-checks that every domain in `weights.yaml` has a matching file across `audit/deterministic`, `audit/semantic`, `calculation/aggregation/domain`, `calculation/deterministic/document`, `calculation/semantic/ensemble` | pipeline pre-check, no direct author-guide equivalent |

**None of the 12 scripts follow the `--repo-root`/`--in`/`--out`
argparse contract or write the standard `{status, message, written}`
envelope** — confirmed by reading each script's actual argument
handling (e.g. `audit_git.py` takes a positional `repo_path`,
`validate_scores.py`/`verify_standard.py` take explicit named paths,
`leaderboard.py` reads specific named JSON files like
`adjusted_scores.json`). They'd need a thin adapter layer to conform,
not a rewrite — the actual logic (git parsing, VRAM/timing checks,
z-score statistics, weighted aggregation) is real, tested-looking, and
substantially more sophisticated than any placeholder — this is
genuinely the most mature script layer of any system in this pass.

## 4. Use Cases

Audit-only per LIM-001, confirmed: the only real content in
`plan/usecase/` is under `repo_new/` (no `repo_existing/` directory
exists at all, unlike the dev class's 4-way split), and even
`repo_new`'s `01-generation.md` files are unauthored placeholders
(§2). The actual triggering use case is: **ingest a target repo
(competition submission), run full audit+scoring, add it to the
cross-repo leaderboard** — `case_1_no_documentation` vs.
`case_2_has_documentation` likely distinguishes whether the submission
already has docs to audit against vs. needs a baseline assumption, but
since both cases' `01-generation.md` are identical placeholders, this
isn't confirmable from content alone.

## 5. Workflow per Use Case (target `init.py` phase plan)

Full ordered phase table, following `plan/core/loop.yaml`'s 11 stages
directly (this is the canonical, correct `loop.yaml` — the one
LIM-001 says got mistakenly copy-pasted into the academic systems
before being caught):

```
repository-ingest        script    depends_on: []
audit-deterministic      script    depends_on: [repository-ingest]      # parallel, scope: document
audit-semantic           semantic  depends_on: [repository-ingest]      # parallel, scope: document
calculate-deterministic  script    depends_on: [audit-deterministic]    # scope: document
calculate-semantic       semantic  depends_on: [audit-semantic]         # scope: ensemble
aggregate-domain         script    depends_on: [calculate-deterministic, calculate-semantic]
calculate-relative       script    depends_on: [aggregate-domain]       # scope: competition — needs ALL teams' aggregate-domain output, not just this one
normalize-final          script    depends_on: [calculate-relative]     # cap: 20 — see §10 on the cap:20 vs weights.yaml's final_scale:150 discrepancy
validate-scoring         script    depends_on: [normalize-final]        # on_failure: abort
report-generation        script    depends_on: [validate-scoring]       # templates/reports
```

Almost entirely `script`-kind, one exception (`audit-semantic`, LLM
judgment) — the orchestration itself needs no LLM authorship even
though the audit has both deterministic AND semantic-judgment layers.
`calculate-relative`'s `depends_on` is structurally different from
every other system in this pass: it needs every competing team's
`aggregate-domain` output, not just this run's own — `init.py` for this
system needs a cross-repo dependency concept the dev/academic classes
never require.

## 6. Deterministic Audit via Script

Every one of the 10 domains has a deterministic backing script or
config-presence check (§3's table) — the most complete
deterministic-check coverage of any system in this pass, richer even
than `base_dev`'s 18 generic checks since these are domain-native
(git history parsing, VRAM/timing constraints, SAST) rather than
generic cross-document rules.

## 7. Generation via Script (`scaffold.py`)

Confirmed: no real generation exists (§2, §4) — `templates/generation/`
doesn't appear in this system's tree at all (only `templates/reports/`).
Per the author guide's own FAQ (*"if a capability doesn't apply,
implement it as a no-op that returns `status: ok, message: not
applicable`"*), `scaffold.py` should be exactly that — a no-op,
matching the class's actual shape rather than forcing a generation
capability this class was never designed to have.

## 8. Report & Calculation via Script (`calculate.py` + `report.py`)

The competitive scoring pipeline (§3, §5) is the most novel
`calculate`/`report` shape of any of the 9 systems — cross-repo
ranking, not single-repo scoring. Mapped to the 6-capability contract:
`score_aggregator.py` + `statistics.py` + `leaderboard.py` together
constitute `calculate.py`'s logic (raw aggregation → z-score adjustment
→ weighted+semantic-bonus final score), `validate_scores.py` +
`verify_standard.py` are pipeline integrity pre-checks with no direct
equivalent in the author guide's 6 capabilities (closest to `validate`,
but validating the *scoring pipeline's own configuration*, not a
target repo's documents) — worth keeping as a 7th, hackathon-specific
concern rather than force-fitting into `validate.py`. `report.py` would
render `templates/reports/global-leaderboard.md` +
`templates/reports/team-final-summary.md` from `leaderboard.py`'s
output.

## 9. Script Language Priority Applied

**This system is already 100% Python** — the positive baseline the
execution-model proposal's §3.5 explicitly cites. Remaining work per
this proposal's scope:
- **`init.py` doesn't exist** — needs authoring from scratch per §5's
  phase table, no base to inherit from
- **The 12 existing scripts need a thin adapter, not a rewrite** — none
  currently accept `--repo-root`/`--in`/`--out` or emit the standard
  envelope (§3). The actual domain logic in each (git parsing, VRAM
  checks, z-score math, weighted aggregation) is sound and shouldn't be
  touched; only the argument-parsing/output-envelope boundary needs
  wrapping to conform to the contract every other system's scripts
  would follow.

## 10. Open Questions / Risks Specific to `python_hackathon`

- **How much rework the 12 scripts need is the central open question.**
  My read: minimal — wrap each script's existing `main()`/entry logic
  behind a new `--repo-root`/`--in`/`--out` argument layer that
  translates to/from each script's current (different, per-script)
  argument shape, without touching the internal logic. A full rewrite
  isn't warranted given the logic's apparent maturity.
- `plan/usecase/repo_new/*/tier_*/01-generation.md` being placeholder
  stubs (§2) while `02-audit.md`/`03-fix.md` presumably have real
  content (not read in this pass — worth checking) suggests the
  generation stage was scaffolded structurally but deliberately left
  unauthored, consistent with "this class doesn't generate" — worth
  confirming these placeholder files should simply be deleted (since
  §7 concludes `scaffold.py` is a no-op) rather than filled in later.
- **`weights.yaml`'s `final_scale: 150` vs. `loop.yaml`'s
  `normalize: {type: final, cap: 20}`** — these two numbers (150 vs 20)
  read as inconsistent on their face; LIM-001 specifically calls out
  `cap: 20` as a real, intentional python_hackathon-specific
  normalization value (the same value that mistakenly leaked into the
  academic systems' copy-pasted `loop.yaml`), so it's presumably
  correct — but its relationship to `weights.yaml`'s separately-stated
  `final_scale: 150` isn't obvious from the files alone and is worth
  confirming with whoever owns the scoring formula rather than assumed
  here.

## 11. Explicitly Out of Scope

Actual rework of the 12 existing scripts to fit the standard contract
— this proposal specifies the target shape (§9), doesn't implement the
adapter. Resolving the `cap: 20` vs. `final_scale: 150` question (§10).
Any change to domain content, weights, or scoring rules themselves.
