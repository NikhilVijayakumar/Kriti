# Audit Proposal — Paper {{ paper_id }}

**Commit:** {{ commit_sha }}  **Status:** {{ status }}  **Source:** {{ source }}  **Iteration:** {{ iteration }}
{{#user_comment}}
**Prior rejection reason:** {{ user_comment }}
{{/user_comment}}

{{ summary }}

---

## What Will Be Audited (computed)

**Models this round:** {{#models}}{{ . }} {{/models}}

| Domain | Deterministic Checks | Rubric Criteria |
|---|---|---|
{{#domains}}
| {{ domain_key }} | {{ det_rule_count }} ({{ det_critical_count }} critical) | {{#rubric_found}}{{ rubric_criterion_count }}{{/rubric_found}}{{^rubric_found}}rubric not found{{/rubric_found}} |
{{/domains}}

---

{{{ content_md }}}

---

## Approve

Review the scope above. Run `approve_proposal.py --phase audit` after
review, or `--reject --reason "..."` to send back for a redraft.
