# Audit Proposal

{{title}}

**Phase**: {{phase}}  
**Model(s)**: {{models}}  
**Iteration**: {{iteration}}  

{{#summary}}
{{summary}}
{{/summary}}

## Domains Under Audit

{{#domains}}
- **{{domain_key}}**: {{det_rule_count}} det rules, {{rubric_criterion_count}} rubric criteria{{#rubric_found}} (rubric found){{/rubric_found}}{{^rubric_found}} (no rubric){{/rubric_found}}
{{/domains}}

{{^domains}}
No domain data available.
{{/domains}}

{{#redraft_of}}
> Redraft of iteration {{redraft_of.iteration}}
{{/redraft_of}}
