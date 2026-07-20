# 07. Runtime Standards

**Domain:** Runtime
**Audit Target:** `main.py`, `app.py`, `run.py`, model artifacts

## Standard Definition
The final execution artifact must be clearly identifiable, use allowed formats, fit within hardware constraints, complete inference within time limits, satisfy the API contract, and accept only the prescribed input parameters.

### Expected Evidence
1. **Entrypoint:** The root directory must contain an obvious execution script (e.g., `main.py`).
2. **Format:** Model artifacts must use only `.pt`, `.pth`, or `.pkl` format.
3. **VRAM:** Largest model file must be under 12GB (Colab T4 compatibility).
4. **Speed:** Single `predict()` call must complete within 30 seconds.
5. **Output Contract:** `predict()` output must include `team_a_score` and `team_b_score`.
6. **Input Contract:** `predict()` must accept only `team_a` and `team_b` as required parameters — no extra required args, no config/override params. No human intervention or manual data-tweaking allowed on match day.
