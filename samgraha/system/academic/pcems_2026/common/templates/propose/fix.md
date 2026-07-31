# Fix Proposal

{{title}}

**Phase**: {{phase}}  
**Target domain**: {{target_domain}}  
**Iteration**: {{iteration}}  

{{#user_comment}}
**User comment**: {{user_comment}}
{{/user_comment}}

{{#summary}}
{{summary}}
{{/summary}}

## Triggering Findings

{{#triggering_findings}}
- {{#name}}**{{name}}**: {{/name}}{{message}}(severity={{severity}})
{{/triggering_findings}}

{{^triggering_findings}}
No triggering findings &mdash; user-requested fix.
{{/triggering_findings}}

{{#redraft_of}}
> Redraft of iteration {{redraft_of.iteration}}
{{/redraft_of}}
