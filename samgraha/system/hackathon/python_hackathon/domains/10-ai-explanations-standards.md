# 10. AI Explanations Standards

**Domain:** AI Explanations
**Audit Target:** `README.md`

## Standard Definition
The submission must document *why* its predictions are trustworthy — not by using an LLM to narrate them, but by describing a concrete interpretability method applied to the model itself (feature importance, SHAP/LIME, coefficient inspection for linear models, attention visualization for transformers, or an equivalent technique appropriate to the model class used). This is a documentation-quality and methodology-presence check — it does not require LLM SDKs, and does not evaluate prediction accuracy.

### Expected Evidence
1. **Interpretability Method:** README documents a recognized interpretability technique (SHAP, LIME, feature importance, attention visualization, etc.).
2. **Prediction Capabilities:** README describes specific prediction capabilities:
   - Match predictions: match winner, win/draw probabilities, scoreline, first team to score, total goals, both teams scoring probability.
   - Player predictions: goal scoring probability, expected goals, assist probability, goalkeeper clean sheet probability.
3. **Methodology:** README explains how predictions are generated (model type, features, training approach, algorithm used).
