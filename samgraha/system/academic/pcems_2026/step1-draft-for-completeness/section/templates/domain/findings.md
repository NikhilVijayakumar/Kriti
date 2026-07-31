# III. FINDINGS

## Experimental Setup
{{ experimental_setup }}

## Results
{{! Tables render inline inside this field, each placed immediately after
    the sentence that first references it — table_created_with_word_tools
    layout, "Table I: ..." caption above, per guide/Tables/01-table-standards.md.
    The generation prompt embeds them at point of reference; this template
    does not — a trailing {{#tables}} loop here would put every table after
    all Results/Analysis prose regardless of where it's cited, the exact
    "collected at the end" anti-pattern Common Mistakes/01 and
    Reviewer Expectations/02 (11/11 sample papers) flag. }}
{{ results }}

## Analysis
{{! Figures render inline inside this field, same reasoning as tables
    above — each placed immediately after its first reference, caption
    below per guide/Figures/01-figure-standards.md. }}
{{ analysis }}
