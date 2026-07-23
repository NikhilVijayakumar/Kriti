# Semantic Audit — data-quality

Semantic evaluation of data quality, dataset suitability, feature engineering, data preparation, validation methodology, and overall machine learning development practices.

## Evaluation Principles
- Evaluate data quality rather than dataset size.
- Evaluate only observable evidence.
- Do not assume undocumented data processing practices.
- Consider the scope and complexity expected for a hackathon project.
- Reward sound machine learning methodology over model performance.
- Focus on engineering rigor throughout the data lifecycle.

## Task
Analyze the repository documentation, README, notebooks, and source code
to evaluate the overall quality of the project's data engineering and
machine learning methodology.

Consider:

- Whether the data sources are clearly identified and appropriate for the problem.
- Whether the reliability, relevance, and quality of the datasets are discussed.
- Whether data collection, preprocessing, cleaning, and transformation are well documented.
- Whether feature engineering decisions are reasonable and well justified.
- Whether the dataset preparation pipeline is clearly explained.
- Whether training, validation, and testing strategies are appropriate.
- Whether the project demonstrates awareness of data leakage, bias, overfitting,
  class imbalance, and other common machine learning risks.
- Whether model evaluation methodology is appropriate for the prediction task.
- Whether evaluation metrics are justified and correctly interpreted.
- Whether limitations of the data or model are acknowledged.
- Whether the overall machine learning methodology demonstrates sound
  engineering practices appropriate for a hackathon project.

Do not reward projects solely for using larger datasets or more complex models.
Evaluate the quality of the data methodology, engineering decisions,
and machine learning practices.

Provide:

- Overall data quality score (0-100)
- Data engineering strengths
- Data engineering weaknesses
- Recommendations for improvement
- Supporting evidence from the repository

## Expected Output
Return exactly one JSON object matching this schema (this is what the post-script persists):
```json
{
  "overall_score": "number",
  "reasoning": "string",
  "evidence": "string",
  "strengths": [
    "string"
  ],
  "weaknesses": [
    "string"
  ],
  "recommendations": [
    "string"
  ]
}
```
