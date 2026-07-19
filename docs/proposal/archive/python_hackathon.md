# Python Hackathon Audit Standard

Version: 1.0.0

Status: Draft

---

# 1. Purpose

The Python Hackathon Audit Standard defines the engineering audit methodology, workflow, scoring model, reporting structure, and supporting artifacts required to evaluate Python-based hackathon submissions.

The standard provides a reproducible, evidence-driven evaluation framework that combines deterministic engineering audits with semantic assessments to produce transparent and explainable technical scores.

This standard is intended to be executed by a standards execution platform but remains implementation independent.

---

# 2. Design Principles

The standard is built around the following principles.

## Evidence First

Every engineering decision shall be supported by collected evidence.

No score shall be assigned without traceable findings.

---

## Deterministic Before Semantic

Objective engineering measurements are always evaluated before semantic analysis.

Semantic evaluation supplements engineering evidence but never replaces deterministic verification.

---

## Independent Engineering Domains

Each engineering domain is evaluated independently.

Strength in one engineering domain shall never compensate for weakness in another.

---

## Reproducible Evaluation

Repeated execution of the same audit against the same repository shall produce identical deterministic results.

Semantic evaluations shall record execution metadata to ensure traceability.

---

## Explainable Scoring

Every awarded or deducted point shall reference the engineering evidence that produced it.

---

## Declarative Configuration

Audit behaviour, calculations, weights, workflows, and reporting are defined by the standard rather than hardcoded into the execution platform.

---

# 3. Scope

This standard evaluates Python hackathon submissions.

It defines

- engineering domains
- audit workflow
- deterministic audits
- semantic audits
- scoring methodology
- statistical grading
- reporting templates
- remediation guidance

This standard does not define

- compilation
- execution engine
- scheduling
- orchestration
- runtime lifecycle

---

# 4. Engineering Domains

The audit evaluates ten independent engineering domains.

| Domain | Purpose |
|---------|----------|
| Infrastructure | Environment, packaging, Docker, local execution, offline capability |
| Engineering Quality | Code quality, maintainability, complexity |
| Testing | Automated validation and coverage |
| Documentation | Repository documentation and project communication |
| Security | Secure engineering practices |
| MLOps | Experiment reproducibility and model lifecycle |
| Runtime | Performance characteristics during execution |
| Team Workflow | Self-organization, smooth division of tasks, and clear Git workflow (e.g. peer-reviewed PRs, multiple contributors). |
| Data Quality | Quality of data sources, verification, and explanation of data collection methods. |
| AI Explanations | Quality, contextual reasoning, and clarity of automated AI text explanations. |

Each domain contains its own

- deterministic audit
- semantic audit
- scoring rules
- statistical grading
- report templates

---

# 5. Standard Structure

```text
python-hackathon-audit-standard/

├── standard.yaml

├── pillars/

├── audit/
│   ├── deterministic/
│   └── semantic/

├── calculation/
│   ├── deterministic/
│   ├── semantic/
│   ├── aggregation/
│   ├── relative/
│   ├── normalization/
│   └── validation/

├── templates/
│   ├── prompts/
│   └── reports/

├── fixes/

├── generation/

├── scripts/
```

---

# 6. Audit Workflow

The audit lifecycle consists of nine sequential stages.

Repository

↓

Deterministic Audit

↓

Semantic Audit

↓

Deterministic Scoring

↓

Semantic Scoring

↓

Pillar Aggregation

↓

Relative Grading

↓

Normalization

↓

Validation

↓

Report Generation

Each stage consumes only the artifacts produced by the preceding stage.

---

# 7. Deterministic Audit

Purpose

Collect objective engineering evidence.

Characteristics

- Repeatable
- Rule-based
- Non-probabilistic
- Independent of AI models

Outputs

- findings
- metrics
- evidence
- raw measurements

Examples

Documentation

- Required files
- Broken links
- Markdown validity

Testing

- Coverage
- Test execution
- Failed tests

Security

- Secrets
- Unsafe serialization
- Dependency vulnerabilities

---

# 8. Semantic Audit

Purpose

Evaluate engineering quality that cannot be reliably measured through deterministic rules.

Semantic audits shall never modify deterministic findings.

---

## Model Independence

Every semantic evaluator executes independently.

Each evaluator produces

- score
- reasoning
- evidence
- execution metadata

No evaluator has knowledge of the output produced by another evaluator.

---

## Semantic Ensemble

Multiple semantic evaluators may execute.

Example

- Gemini Flash
- Gemini Pro
- Claude
- GPT
- Local Models

The standard treats each evaluation as an independent observation.

---

## Semantic Metadata

Every semantic result shall include

- model identifier
- provider
- prompt version
- execution timestamp
- standard version

This metadata becomes part of the evidence.

---

# 9. Scoring

Scoring transforms audit evidence into engineering scores across a 4-phase pipeline.

---

## Phase 1: Domain Aggregation
Each engineering domain combines deterministic and semantic scores.
Deterministic scores are taken directly. Semantic scores are averaged across all models that evaluated that domain.
The raw domain score is calculated as: `(0.60 * Deterministic) + (0.40 * Semantic Mean)`.

---

## Phase 2: Relative Grading & Z-Score
For each domain independently, the population median and Median Absolute Deviation (MAD) are calculated.
A robust Z-score is generated for each team. A soft-bounded sigmoid function (`tanh`) converts the Z-score into a domain bonus/penalty (capped at ±10 points).

---

## Phase 3: Weighted Scoring
The adjusted domain scores are multiplied by their specific domain weight (totaling 100 points):
- Runtime (15)
- Engineering (12), Testing (12)
- Security (10), MLOps (10), Data Quality (10), AI Explanations (10)
- Infrastructure (8), Team Workflow (8)
- Documentation (5)

---

## Phase 4: Semantic Agreement & Normalization
A semantic agreement bonus is calculated based on inter-model standard deviation. High LLM agreement yields up to +15 bonus points. 
The final raw score (out of 115) is then mathematically normalized to the competition's final scale of **150 points**.

---

# 10. Blank (Merged into Section 9)
# 11. Blank (Merged into Section 9)

---

# 12. Validation

Every scoring stage shall validate

- weight totals
- statistical calculations
- normalization
- bonus calculations

Validation failures invalidate the audit.

---

# 13. Templates

Templates define presentation resources. The reporting architecture operates in 3 tiers:

## Tier 1: Domain Reports (30 templates)
Each of the 10 domains contains 3 distinct reports:
- `[domain]-deterministic.md`
- `[domain]-semantic.md`
- `[domain]-summary.md` (Contains the relative Z-score grading for the domain)

## Tier 2: Team Final Summary
A single report per team aggregating all 10 domain marks and displaying the LLM model bias breakdown.

## Tier 3: Global Leaderboard
The final competition report ranking all teams, featuring section-by-section mark breakdowns and the final normalized 150-point score.

---

# 14. Fix Guidance

Fix guidance provides structured engineering recommendations for every audit finding.

Recommendations are generated from deterministic evidence and semantic observations.

---

# 15. Generation Guidance

Generation artifacts provide reusable engineering templates for documentation and project improvements.

Generation guidance never affects scoring.

---

# 16. Developer & Execution Scripts

The declarative YAML rules are backed by specialized execution scripts that extract objective evidence from the repositories:

- `audit_git.py`: Analyzes git history, commit message quality (Conventional Commits), and GitFlow branches.
- `audit_testing.py`: Runs pytest and parses JSON coverage reports.
- `audit_security.py`: Executes bandit SAST and scans for hardcoded secrets via regex.
- `audit_infrastructure.py`: Validates Docker, docker-compose, and uv.lock setups.
- `audit_mlops.py`: Detects DVC and MLflow configurations.
- `audit_model_artifact.py`: Enforces the Section 17 rules (12GB VRAM limit, 30s speed, format constraints) in an offline sandbox.
- `statistics.py` & `leaderboard.py`: Executes Phase 2-4 of the scoring pipeline.

# 17. Rules & Restrictions. 
Since your goal is learning and ensuring compatibility with standard infrastructure (like a free/low-tier Google Colab T4 GPU with 12GB VRAM), these rules will act as the "guardrails" for your innovation teams.
Here is a comprehensive list of rules and restrictions to add to your challenge blueprint:
## 17.1. Infrastructure & Model Environment Rules
Hardware Ceiling: Both training and inference pipelines must run successfully on a machine with a maximum of 12GB VRAM (equivalent to a standard Google Colab T4 instance) without running out of memory (OOM).
Deliverable Formats: Models must be serialized and submitted as either a PyTorch checkpoint file (.pt / .pth) or a Python pickle (.pkl) file. No external cloud-hosted inference APIs (like custom fine-tuned OpenAI endpoints) can be used for the core prediction engine; everything must execute locally on the 12GB VRAM environment.
Inference Speed Constraint: To ensure the code is optimized, a single match inference loop (generating all team and player predictions) must run in under 30 seconds on the 12GB VRAM system.
## 17.2. Input Data & Forecasting Restrictions
The Strict Input Boundary: The live prediction engine API must accept only the two competing countries as input (e.g., team_A: "Argentina", team_B: "Brazil"). No human intervention or manual data-tweaking is allowed on match 


## 17.3.  The "Living Model" Update Rules
## 17.3.1 The Model Registry & Submission Deadline
The "One-Model" Constraint: Only one serialized model file (e.g., production_model.pt) per team can be active at any given time.
The Match-Day Freeze: Teams can update their model as often as they want during the week, but the version sitting in the submission repository exactly 2 hours before kickoff of any match is the one that will be locked and executed for that match. No updates are accepted mid-game.


## 17.3.2 . Input Integrity (The Automation Sandbox)
Your evaluation script will run the models blindly. The script will simply feed the model the two countries: predict(Team_A, Team_B).
The Restriction: If a team wants their model to know about a new player injury or a shift in squad form, they must bake that logic into their pipeline. They cannot pass a manual text note to you saying "Hey, manually reduce Messi's rating by 10% for this match." The model itself must ingest the updated data file or scrape it programmatically during execution.


## 17.3.3 Backwards Compatibility Rule (The "Don't Break the Script" Rule)
Even if a team completely changes their underlying machine learning algorithm (e.g., switching from an XGBoost model to a PyTorch Neural Network mid-tournament), the input arguments and output JSON format must never change. * If a team pushes a new model version that throws an error or breaks your evaluation script on match day, they get a Base Score of 0 for that match. This teaches them the critical engineering value of regression testing and API contracts.
