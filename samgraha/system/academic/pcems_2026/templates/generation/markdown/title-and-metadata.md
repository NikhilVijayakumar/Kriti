# {{ title }}

{{#authors}}
{{ name }}<sup>{{ affiliation_number }}</sup>
{{/authors}}

**Corresponding Author:** {{ corresponding_author_email }}

## Affiliations
{{#affiliations}}
<sup>{{ number }}</sup> {{ name }}
{{/affiliations}}

## Keywords
{{#keywords}}
{{ . }}{{^last}}, {{/last}}
{{/keywords}}

## Abstract
{{ abstract }}
