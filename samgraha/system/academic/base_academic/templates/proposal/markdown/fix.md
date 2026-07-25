# Fix Proposal — Paper {{ paper_id }}

**Commit:** {{ commit_sha }}  **Status:** {{ status }}  **Source:** {{ source }}  **Iteration:** {{ iteration }}
**Target domain:** {{ target_domain }}
{{#user_comment}}
**User request / rejection reason:** {{ user_comment }}
{{/user_comment}}

{{ summary }}

---

## Failing Checks This Fix Addresses (computed)

{{#triggering_findings}}
- **{{ rule }}** ({{ check_id }}): {{ detail }}
{{/triggering_findings}}
{{^triggering_findings}}
(no deterministic findings — this fix is driven by `user_comment` alone)
{{/triggering_findings}}

---

{{{ content_md }}}

---

## Approve

Review the change above. Run `approve_proposal.py --phase fix
--domain {{ target_domain }}` after review, or `--reject --reason "..."`
to send back for a redraft.
