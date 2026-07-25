# Generation Proposal — Paper {{ paper_id }}

**Commit:** {{ commit_sha }}  **Status:** {{ status }}  **Source:** {{ source }}  **Iteration:** {{ iteration }}
{{#user_comment}}
**Prior rejection reason:** {{ user_comment }}
{{/user_comment}}

{{ summary }}

---

## What Will Be Generated (computed)

| Domain | Stage | Word Range | Rule Checks (critical) |
|---|---|---|---|
{{#domains}}
| {{ domain_key }} | {{ stage }} | {{ word_min }}–{{ word_max }} | {{ check_count }} ({{ critical_count }}) |
{{/domains}}

---

{{{ content_md }}}

---

## Approve

Review the plan above. Run `approve_proposal.py --phase generation`
after review, or `--reject --reason "..."` to send back for a redraft —
the next draft will address the stated reason.
