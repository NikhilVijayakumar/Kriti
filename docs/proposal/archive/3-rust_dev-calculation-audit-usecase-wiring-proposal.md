# rust_dev — `calculation`/`audit` as Usecases-with-Steps (Proposal 3 of 7)

## 0. Series

Part of a 7-proposal set — see
[`rust_dev-tier-directory-restructure-proposal.md`](1-rust_dev-tier-directory-restructure-proposal.md) §0.
Depends on proposal 1 (layout) and proposal 2 (manifest + schema layer
existing to attach to). Feeds proposal 4 (usecase-map generation needs
real usecases with steps to enumerate — a usecase with `steps: []` has
nothing for a usecase map to point at).

## 1. The user's framing, restated precisely

Today `calculation/` and `audit/` are **data trees** — YAML rule files and
scoring formulas — not usecases. Nothing in rust_dev wires them into
samgraha's `usecase → step (deterministic|semantic) → script|prompt` model
the way pcems_2026's `deterministic-audit` and `semantic-audit` usecases
do. This proposal makes them real usecases, each expressed as a set of
steps, per tier.

## 2. How pcems_2026 does it (the pattern to port)

`standard.yaml`'s `deterministic-audit` usecase:

```yaml
- name: deterministic-audit
  description: "run deterministic checks against calculation/deterministic/{domain}.yaml rules"
  steps:
    - order: 1
      kind: deterministic
      description: "run deterministic checks against calculation/deterministic/{domain}.yaml rules"
      script: deterministic-audit
```

One script (`step1-draft-for-completeness/audit/script/deterministic_audit.py`)
reads `calculation/deterministic/{domain}.yaml`-style rule files, evaluates
them against the domain's draft, persists to `academic_deterministic_findings`.
Semantic audit is the same shape but `kind: semantic` with a `prompt:`
(`semantic-audit`), followed by a deterministic persist step
(`persist-domain-semantic-score`).

rust_dev's equivalent inputs already exist and are richer, not thinner:

- `audit/deterministic/{document,section}/{domain}.yaml` — same shape as
  pcems's rule files (confirmed: `03-security.yaml` has `id`, `condition`,
  `severity`, `weight`, `mandatory`, `evidence` — matches pcems's rule
  schema field-for-field)
- `audit/semantic/{document,section}/{domain}.md` — rubric prose, same role
  as pcems's `audit/semantic/document/{domain}.md`
- `calculation/{deterministic,semantic}/{document,section}.yaml` — the
  scoring **formulas** these rules feed (confirmed generic, see proposal 1
  §3) — pcems has no direct equivalent this explicit; pcems's scoring is
  folded into `calculate.py` rather than externalized as its own YAML layer.
  rust_dev's `calculation/` is more explicit and should stay that way.
- `script/schema/{domain}/{check}.schema.json` +
  `script/{ubuntu,windows}/{domain}/{check}.{sh,ps1}` — the **ground-truth**
  layer pcems's audit rules don't have at all for most domains. rust_dev's
  `sec-doc-015`/`sec-doc-016` rules (read in `03-security.yaml`) already
  reference `script_result` evidence pointing at
  `script/schema/03-security/secret-scan.schema.json#metrics.secrets_found` —
  this is a rule citing a script's output, exactly the shape pcems's
  `rule_ref` mechanism uses (confirmed by `script/mapping.yaml`'s own
  header comment: *"No audit rule currently has a rule_ref pointing into
  script/schema/ — that wiring happens in Phase 6 (§8 retrofit)"* — i.e.
  rust_dev's own prior proposal already flagged this exact gap and
  deferred it; this proposal is that deferred work, reframed as
  usecase/step wiring instead of a standalone "Phase 6").

## 3. Proposed usecase shape, per tier

Four usecases per tier (matching pcems's granularity: generate → audit-det
→ audit-sem → fix), all four scoped to that tier's domain(s):

```yaml
# tierN/'s slice of standard.yaml's usecases: block
- name: generate-document-{domain}
  description: "generate {domain}'s document from its domain/{domain}.md template"
  steps:
    - order: 1
      kind: deterministic
      description: "gather upstream tier context (per tiers.yaml relationships)"
      script: gather-tier-context
    - order: 2
      kind: semantic
      description: "generate the document from templates/generation/document/{domain}.md"
      prompt: generate-{domain}

- name: deterministic-audit-{domain}
  description: "run {domain}'s deterministic checks — rule file + script-sourced ground truth"
  steps:
    - order: 1
      kind: deterministic
      description: "run any script/schema/{domain}/*.schema.json-backed checks (secret-scan, cargo-audit, etc.)"
      script: run-domain-checks
    - order: 2
      kind: deterministic
      description: "evaluate audit/deterministic/{document,section}/{domain}.yaml rules, scoring script_result rules against step 1's output"
      script: deterministic-audit
    - order: 3
      kind: deterministic
      description: "persist verdict + findings"
      script: persist-deterministic-findings

- name: semantic-audit-{domain}
  description: "score {domain} against audit/semantic/{document,section}/{domain}.md rubric"
  steps:
    - order: 1
      kind: semantic
      description: "score against rubric"
      prompt: semantic-audit
    - order: 2
      kind: deterministic
      description: "persist score + findings"
      script: persist-semantic-score

- name: fix-{domain}
  description: "regenerate {domain} content for sections that failed deterministic or semantic audit"
  steps:
    - order: 1
      kind: deterministic
      description: "gather failing findings for this domain"
      script: gather-fix-context
    - order: 2
      kind: semantic
      description: "regenerate failing section(s)"
      prompt: fix-{domain}
    - order: 3
      kind: deterministic
      description: "persist regenerated content, re-queue for audit"
      script: persist-fix
```

`calculate` stays a single **cross-tier** usecase (not per-tier) — it reads
already-persisted findings across all tiers/domains and applies
`calculation/summary/final_score.yaml`'s `weighted_sum`, same as pcems's
single `calculate` usecase reading across all domains. No per-tier
duplication needed there; matches proposal 1 §3's reasoning for why
`calculation/` itself stays common.

## 4. The `run-domain-checks` script — the actual net-new work

This is the one genuinely new script family, not a port. rust_dev's checks
today are `.sh`/`.ps1` pairs (`script/ubuntu/{domain}/{check}.sh`,
`script/windows/{domain}/{check}.ps1`) producing output validated against
`script/schema/{domain}/{check}.schema.json`. A samgraha `deterministic`
step must be a Python script speaking `parse_step_args()`/`write_envelope()`
(per `ADDING-A-USECASE.md` §2). Two implementation options:

- **(a) Thin Python wrapper per check** — one `.py` per check that shells
  out to the existing `.sh`/`.ps1` (OS-detected) and reshapes its stdout
  into `write_envelope()`'s JSON contract, validated against the existing
  `.schema.json`. Minimal rewrite, keeps the shell/PowerShell logic as the
  actual implementation.
- **(b) Full Python port** — rewrite each check natively in Python,
  dropping the `.sh`/`.ps1` pair entirely. Matches the original
  `rust_dev-proposal.md` §9's stated intent (*"consolidate each `.ps1`+`.sh`
  pair into a single `.py`, same as the 16 inherited checks"*) — this
  proposal's predecessor already decided this direction; (a) would be a
  regression from that decision, not a neutral choice.

**Recommend (b)**, matching the already-decided direction in
`docs/proposal/archive/rust_dev-proposal.md` §9. One `run-{check}.py` per
check, `script/schema/{domain}/{check}.schema.json` becomes the contract
the Python script's `write_envelope()` output must satisfy, `.sh`/`.ps1`
retired once ported (or kept only where a check is inherently
shell-native — e.g. `cargo-audit` invoking the real `cargo audit` binary —
in which case the `.py` becomes a thin subprocess wrapper by necessity, not
by choice, which is a different case from (a)'s blanket approach).

## 5. `script/mapping.yaml`'s deferred wiring — now has a home

`mapping.yaml`'s header note (quoted in full in proposal 1 §5, table row 3)
says the `rule_id → script/schema/` wiring is deferred to a future "Phase 6."
This proposal *is* that phase: once §4's checks exist as
samgraha-registered scripts (`run-{check}` in `standard.yaml`'s `scripts:`
block) and §3's `deterministic-audit-{domain}` usecase's step 2 evaluates
`script_result`-type rules against step 1's persisted output, every
`rule_id` in `mapping.yaml` gets a real, resolvable `rule_ref`. Regenerating
`mapping.yaml` (its own header says it's `generated_from: audit/**/*.{yaml,md}`,
i.e. not hand-maintained) becomes possible once this lands — out of scope
to regenerate it here, but this proposal removes the blocker its header
describes.

## 6. Open questions

1. **Decided: net-new logic, lives inside `gather-tier-context` when
   written.** `gather-tier-context` (generation usecase step 1) needs to
   read `tiers.yaml`'s `relationships:` to assemble "already-completed
   upstream domains" the same way `loop.yaml`'s
   `path_selection.generate.context` describes — this logic doesn't exist
   as a script anywhere today, it's currently just prose in `loop.yaml`.
   Scoped to whoever writes `gather-tier-context.py`, not proposal 2's.
2. **Decided: branches internally, no separate step variant.**
   `product-guide`'s "full-context generation" special case
   (`loop.yaml`'s `special_cases.product-guide`, `context: all_domains`)
   is one script with domain-aware branching, matching how `loop.yaml`
   already documents it as an exception to the general rule rather than a
   separate procedure.
3. **Decided: one step, both scopes.** Section-scope audit
   (`audit/deterministic/section/{domain}/*.yaml` — plural) and
   document-scope (`audit/deterministic/document/{domain}.yaml` —
   singular) both run inside `deterministic-audit-{domain}`'s step 2 (rule
   file selection is already file-path-driven, no new branching needed) —
   not split into `deterministic-audit-{domain}-document` /
   `-section` as separate usecases. `standard.yaml`'s `usecases:` block
   reflects this: one `deterministic-audit-{domain}` per domain, not two.

## 7. Explicitly out of scope

Deciding (a) vs (b) for every individual check (§4 recommends (b) as
default, but `cargo-audit`-style OS/toolchain-native checks are called out
as exceptions needing case-by-case judgment during execution). Writing any
script content. Regenerating `script/mapping.yaml` (§5 — unblocked, not
executed here). The usecase-map generator that consumes this proposal's
usecases (proposal 4).
