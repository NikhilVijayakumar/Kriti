# Report Proposal — Paper {{ paper_id }}

**Commit:** {{ commit_sha }}  **Status:** {{ status }}  **Source:** {{ source }}  **Iteration:** {{ iteration }}
{{#user_comment}}
**Prior rejection reason:** {{ user_comment }}
{{/user_comment}}

{{ summary }}

---

## What Will Render (computed)

**Current score:** {{ current_final_score }} ({{ current_score_band }})

**Per-domain reports:** {{ total_domain_reports }} ({{ domain_count }} domains × {{ per_domain_kind_count }} kinds)

**Whole-run reports:** {{#whole_run_reports}}{{ . }} {{/whole_run_reports}}

---

{{{ content_md }}}

---

## Approve

Review the render plan above. Run `approve_proposal.py --phase report`
after review, or `--reject --reason "..."` to send back for a redraft.
