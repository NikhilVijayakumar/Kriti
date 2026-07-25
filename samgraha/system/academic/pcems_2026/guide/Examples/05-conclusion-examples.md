# Conclusion Examples

> *Source: PCEMS 2026 Sample Papers*

## Purpose

The conclusion summarizes the paper's contribution and results. This document shows effective and ineffective conclusion patterns from accepted sample papers.

## Example 1: Strong Conclusion (WVD Paper)

> "In summary, this paper presents a novel time and frequency windowing-based method to remove false-terms from the WVD of non-stationary multi-component signals. The proposed method effectively removes inner and outer false-terms between signal components even in situations where they overlap in the time-frequency domain. The proposed method segments the original signal with overlapping windows in time and frequency domain successively, computes the WVD of each windowed signals and adds all the WVDs together to form the false-term free TFR. The effectiveness of the proposed method has been tested using multiple synthetic signals as well as real ECG signals. Results of the performance evaluation indicate that the proposed method has the potential to be a useful tool in the time-frequency analysis of non-stationary multi-component signals."

**What works**:
- Restates contribution in first sentence
- Summarizes the method in 2-3 sentences
- Mentions what was tested (synthetic + real signals)
- Ends with broader significance
- Does NOT introduce new results or data
- Length is appropriate (~100 words)

## Example 2: Functional Conclusion (Credit Card Fraud Detection)

> "Credit card fraud detection was performed using machine learning algorithms. We calculated each method's accuracy and found the performance metrics like recall (sensitivity), F1-score, and precision, which helped select the best method among the different methods used. Random forest gave the best output among all the Machine Learning techniques."

**What works**:
- States what was done
- Identifies the best method
- References specific metrics

**What could improve**:
- Does not state quantitative results in the conclusion
- Does not mention limitations
- Does not discuss future work
- Could be more specific about the improvement margin

## Example 3: System Summary Conclusion (IoT Warehouse)

> "This paper shows how to build a monitoring system for a grain and food storage facility. It utilizes an IOT platform and low-cost components. The system can be used to detect temperature changes, monitor the grain level, and determine the moisture level in the warehouse. The system uses a gas sensor to detect CO2 in the warehouse, and a flame sensor to notify the user if a fire ignites. The data collected by the sensors can be displayed on the screen which is supported by Blynk app. Display unit, where users can easily access it. This approach aims to improve the efficiency of the warehouse management system by reducing food waste and financial loss."

**What works**:
- Summarizes the complete system
- Lists capabilities
- States the goal

**What could improve**:
- Does not quantify improvement
- Does not compare with existing systems
- Does not mention limitations
- Does not discuss future work
- Some sentences are awkward ("Display unit, where users can easily access it")

## Example 4: Technical Conclusion (Nanotube JLFET)

> "In this paper, the NT JLFETs having channel length of 5nm and below is discussed. The effect of quantum confinement especially the direct source to drain tunneling is analyzed in depth. Through analysis, it is concluded that the device performance degrades significantly below 7nm. The I_ON current is reduced to a value of 10^-7 and the I_OFF current increased as well owing to the parasitic BJT behavior in the device. The overall I_ON/I_OFF current ratio is ~10^4 which is insufficient for a reliable operation of the device. We have also shown that at device length below 7nm core gate can be modified to control the charge carriers having better performance. Heterojunctions such as Si-Ge can be an effective solution considering it introduces a discontinuity into the valence band which reduces the tunneling associated with the device. The effect of direct source to drain tunneling is studied along with the characteristic behavior of NT JLFETs at 5nm channel."

**What works**:
- States the specific finding (degradation below 7nm)
- Provides quantitative data (10^-7 current, 10^4 ratio)
- Explains the physical mechanism (parasitic BJT)
- Mentions mitigation strategies (core gate, Si-Ge heterojunctions)
- Specific and data-rich

## Conclusion Writing Template

```
Sentence 1: This paper [presented/proposed/investigated] [specific contribution].
Sentence 2: [Method/approach summary in 1-2 sentences].
Sentence 3: [Key quantitative result 1].
Sentence 4: [Key quantitative result 2].
Sentence 5: [Significance or implication].
Sentence 6: [Limitation, if applicable].
Sentence 7: [Future work direction].
```

## Common Conclusion Mistakes

### Introducing New Information
> "Future work will include expanding the dataset to include more categories..."

**Problem**: If future work wasn't discussed in the results, this feels disconnected. Future work should relate to limitations identified in the results.

### Repeating the Abstract
Copying the abstract word-for-word adds no value. The conclusion should synthesize, not repeat.

### Making Unsupported Claims
> "This method will revolutionize the field of fraud detection."

**Problem**: The results don't support claims about revolutionizing anything. State what the results actually show.

### Being Too Vague
> "The results were satisfactory and the method shows promise."

**Problem**: No quantitative grounding. Replace with specific numbers.

## Conclusion Checklist

- [ ] Contribution restated clearly
- [ ] Key quantitative results included
- [ ] No new data or results introduced
- [ ] Significance explained
- [ ] Limitations acknowledged (if applicable)
- [ ] Future work connected to limitations
- [ ] Length between 150-300 words
- [ ] Last sentence provides closure
