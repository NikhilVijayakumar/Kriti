# AI Explanations Analysis Prompt

Guides the per-team analysis for the AI Explanations domain — read by
whichever agent runs it via MCP, after scoring has completed. Explains
how well a team leverages LLMs for automated reasoning. Not parsed by
a script — this is a prompt.

## Version
1.0.0

## Analysis Intent
AI Explanations scores (weight: 10) measure the quality of automated
AI text explanations — the actual product output of hackathon
submissions. This domain evaluates LLM tooling, prompt engineering,
and output quality. It's what the end-user sees.

## Inputs
- `standard_domain_scores` DB table — all teams' ai-explanations domain
  scores (queried via MCP)
- Per-team deterministic findings: LLM SDK presence (openai, anthropic,
  langchain, gemini imports), prompt template files, AI configuration
  files
- Semantic findings: prompt quality, output clarity, contextual
  reasoning depth in AI-generated text

## Narrative Guidance
The AI Explanations narrative must cover:
1. **Score Overview** — team's AI explanations score out of 10, with
   competition average comparison. This domain measures the product
   output directly.
2. **LLM Tooling** — which LLM SDK is used? (OpenAI, Anthropic,
   Gemini, LangChain, local models). Is it imported in code? Name
   the specific SDK found.
3. **Prompt Engineering** — are prompts extracted into dedicated
   template files, or hardcoded in function calls? Prompt files
   (Jinja2, string templates, YAML) demonstrate deliberate prompt
   engineering vs ad-hoc strings.
4. **AI Configuration** — is there an AI config section (model name,
   temperature, max_tokens, system prompts)? Configuration signals
   intentional prompt design.
5. **Output Quality** — semantic assessment: do the AI-generated
   explanations demonstrate contextual reasoning? Are they clear,
   relevant, and well-structured? Or generic and template-like?
6. **Strengths** — dedicated prompt templates, configurable AI params,
   high-quality contextual outputs, multiple prompt strategies.
7. **Weaknesses** — no LLM SDK found, prompts hardcoded as inline
   strings, generic/template outputs, no configuration, API keys in
   source code.
8. **Recommendations** — "extract prompt from inline string to
   `prompts/explain.py` template", "add `temperature` and
   `max_tokens` config", "improve output specificity by including
   domain context in system prompt".

## Visualization Guidance
- `domain_scores` — always include.
- `sdk_adoption` — include: bar chart of LLM SDK usage across teams.
- `prompt_engineering` — include: stacked bar of template-based vs
  inline vs no prompts across teams.

## Output Schema
```json
{
  "domain": "10-ai-explanations",
  "sections": [
    {"heading": "Score Overview", "text": "..."},
    {"heading": "LLM Tooling", "text": "..."},
    {"heading": "Prompt Engineering", "text": "..."},
    {"heading": "AI Configuration", "text": "..."},
    {"heading": "Output Quality", "text": "..."},
    {"heading": "Strengths", "text": "..."},
    {"heading": "Weaknesses", "text": "..."},
    {"heading": "Recommendations", "text": "..."}
  ]
}
```
