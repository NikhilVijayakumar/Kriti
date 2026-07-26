# {{ title }}

{{#authors}}
{{ name }}<sup>{{ affiliation_number }}</sup>
{{/authors}}

## Affiliations
{{#affiliations}}
<sup>{{ number }}</sup> {{ name }}
{{/affiliations}}

**Corresponding Author:** {{ corresponding_author_email }}

## Abstract
{{ abstract }}

## Keywords
{{#keywords}}
{{ . }}{{^last}}, {{/last}}
{{/keywords}}
