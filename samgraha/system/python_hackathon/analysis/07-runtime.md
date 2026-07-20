# Runtime Analysis Prompt

Guides the per-team analysis for the Runtime domain — read by whichever
agent runs it via MCP, after scoring has completed. This is the highest-
weight domain (15 points) — it determines whether the model actually
works. Not parsed by a script — this is a prompt.

## Version
1.0.0

## Analysis Intent
Runtime scores (weight: 15) measure whether the final execution
artifact runs within constraints (12GB VRAM, 30s inference) and
exposes a clear API contract. This is the make-or-break domain — a
team with great code but a non-functional submission scores poorly.

## Inputs
- `standard_domain_scores` DB table — all teams' runtime domain scores
  (queried via MCP)
- Per-team deterministic findings: entrypoint script presence (`main.py`,
  `app.py`, `run.py`), model artifact format, VRAM usage measurement,
  inference timing
- Semantic findings: API contract clarity, error handling quality,
  response format compliance

## Narrative Guidance
The Runtime narrative must cover:
1. **Score Overview** — team's runtime score out of 15, with competition
   average. Emphasize this is the heaviest-weighted domain.
2. **Entrypoint Identification** — is there an obvious execution script
   at root (`main.py`, `app.py`, `run.py`)? Judges need to know how
   to run it. Ambiguous entrypoints are a common failure.
3. **Model Artifact Format** — what format is the model saved in?
   (pickle, ONNX, PyTorch `.pt`, HuggingFace `.bin`, joblib). Is the
   format appropriate for the model type?
4. **VRAM Constraints** — did the model fit within 12GB VRAM? If
   measured, report actual usage. OOM errors or exceeding the limit
   are hard failures.
5. **Inference Speed** — how long does a single prediction take?
   Must be under 30 seconds. Report actual timing if available.
6. **API Contract** — does the submission expose a clear input/output
   contract? Are request/response formats well-defined?
7. **Strengths** — clean entrypoint, appropriate artifact format,
   fast inference, well-documented API contract, proper error handling.
8. **Weaknesses** — no obvious entrypoint, pickle format for complex
   models, VRAM exceeded, slow inference, unclear input/output format.
9. **Recommendations** — "rename `experiment.py` to `main.py` or add
   an entrypoint wrapper", "convert model to ONNX for 3x faster
   inference", "add input validation to reduce OOM risk".

## Visualization Guidance
- `domain_scores` — always include.
- `vram_usage` — include if measured: bar chart of VRAM per team vs
  12GB limit.
- `inference_speed` — include if measured: bar chart of inference time
  per team vs 30s limit.

## Output Schema
```json
{
  "domain": "07-runtime",
  "sections": [
    {"heading": "Score Overview", "text": "..."},
    {"heading": "Entrypoint Identification", "text": "..."},
    {"heading": "Model Artifact Format", "text": "..."},
    {"heading": "VRAM Constraints", "text": "..."},
    {"heading": "Inference Speed", "text": "..."},
    {"heading": "API Contract", "text": "..."},
    {"heading": "Strengths", "text": "..."},
    {"heading": "Weaknesses", "text": "..."},
    {"heading": "Recommendations", "text": "..."}
  ]
}
```
