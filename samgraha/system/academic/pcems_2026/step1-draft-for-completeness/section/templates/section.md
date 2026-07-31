# Section Generation Proposal

{{title}}

**Phase**: {{phase}}  
**Domains**: {{domain_count}}  
**Iteration**: {{iteration}}

{{#summary}}
{{summary}}
{{/summary}}

{{#domains}}
---

### {{domain_key}}

**Existing draft**: {{#existing_draft}}yes{{/existing_draft}}{{^existing_draft}}no{{/existing_draft}}

**Map entries**:
{{#map_entries}}
- `{{map_key}}` ({{kind}}) — {{label}}
{{/map_entries}}
{{^map_entries}}
  None.
{{/map_entries}}

{{/domains}}

{{#content_md}}
{{{content_md}}}
{{/content_md}}

{{#redraft_of}}
> Redraft of iteration {{redraft_of.iteration}}
{{/redraft_of}}
