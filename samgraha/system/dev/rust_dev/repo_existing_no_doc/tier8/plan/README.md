# tier8 Plan — Shared with repo_existing

`repo_existing_no_doc` reuses `repo_existing`'s plan files unchanged after its one-time `bootstrap-readme` usecase completes (proposal 8 §5/§6 — not a third copy). See `repo_existing/tier8/plan/` for `01-audit.md` and `02-fix.md`.

The only difference from `repo_existing`: a `bootstrap` step runs first (`bootstrap/plan/01-bootstrap-readme.md`), so by the time tier 8 starts, a README exists at the repo root for the `readme` domain to audit — and tier 8's `readme` domain audits/finalizes exactly that bootstrap README rather than one drafted here.
