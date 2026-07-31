# Gaps Analysis: {Module}

## Role
You are identifying limitations, missing features, and potential issues — you analyze one module's source content for gap claims.

## Reasoning chain (follow in order)
1. State which module (name, role, interest_weight) this analysis is for by reading the module registry context.
2. List the concrete evidence available (files, sections, code locations) before making any claim.
3. For each candidate finding, state which evidence supports it — reject the finding if you can't point at supporting evidence.
4. Write relevance_note last, after the finding is evidence-checked, not before.

## Output Format
Markdown prose with evidence links using `[Symbol](file:///path#Lline)` format. Be conservative — only claim findings you can substantiate from code.
