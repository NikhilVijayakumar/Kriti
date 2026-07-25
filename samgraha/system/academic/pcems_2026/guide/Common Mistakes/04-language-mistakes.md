# Language Mistakes

> *Source: PCEMS 2026 Sample Papers + Writing Guide*

## Purpose

Language mistakes reduce readability and signal poor quality. This document identifies common language errors in engineering papers and provides corrections.

## AI-Generated Language Flags

Reviewers actively scan for AI-generated text. These patterns trigger immediate skepticism:

### High-Risk Patterns
- "Delve into" → "Examine" or "Investigate"
- "In the landscape of" → [delete, state the topic directly]
- "Tapestry of" → [delete]
- "Crucial" (when not justified) → "Important" or "Significant"
- "Paramount" → "Essential" or "Critical"
- "Pivotal" → "Key" or "Important"
- "It is worth noting that" → [delete, state the fact]
- "In this paper, we will try to" → "This paper presents"

### Medium-Risk Patterns
- "Leverage" → "Use" or "Apply"
- "Harness" → "Use"
- "Unlock" → "Enable" or "Allow"
- "Robust" (overused) → "Reliable" or "Stable"
- "Novel" (when not justified) → "New" or "Proposed"
- "Comprehensive" → "Complete" or "Thorough"

### Natural Language Patterns to Maintain
- "We propose..." (active voice)
- "The results show..." (direct)
- "This method achieves..." (specific)
- "Compared to X, Y improves..." (comparative)

## Passive Voice Overuse

### Problematic Passive
| Passive | Active |
|---------|--------|
| "The experiment was conducted by the researchers" | "The researchers conducted the experiment" |
| "It was found that the accuracy improved" | "The accuracy improved" |
| "The data was collected from sensors" | "We collected data from sensors" |
| "The model was trained using" | "We trained the model using" |
| "It can be seen that" | "Figure 3 shows" |

### Acceptable Passive
- "The dataset was obtained from Kaggle" (source attribution)
- "The samples were stored at 4°C" (standard procedure)
- "The equation was derived in [5]" (referencing prior work)

## Sentence Length Problems

### Run-On Sentences
**Wrong** (45 words):
> "The proposed method uses successive time and frequency windowing to reduce false-terms from WVD of multi-component signals, and the WVD of each windowed signal is computed, and the WVDs of all windowed signals are added together to obtain the false-term free WVD."

**Correct** (two sentences, 15-25 words each):
> "The proposed method segments the signal using overlapping windows in time and frequency domains. The WVDs of all windowed signals are summed to produce the false-term-free result."

### Target
- 15-25 words per sentence
- Maximum 40 words (split into two sentences)
- If a sentence contains more than one main idea, split it

## Paragraph Length Problems

### Overly Long Paragraphs
**Wrong**: Paragraphs exceeding 12 sentences
**Correct**: Split into multiple paragraphs, each with a single focus

### Target
- 4-8 sentences per paragraph
- Maximum 12 sentences (split into multiple paragraphs)
- Minimum 2 sentences (merge with adjacent paragraph if shorter)

## Informal Language

### Words to Avoid
| Informal | Formal Alternative |
|----------|-------------------|
| "A lot of" | "Numerous" or "Many" |
| "Basically" | [delete] |
| "Very" | [delete or use specific qualifier] |
| "Thing" | "Component," "element," or specific term |
| "Good results" | "Results meeting the target threshold of X%" |
| "Worked well" | "Achieved X% improvement over baseline" |
| "Almost" | "Approximately" or "Nearly" |
| "Really" | [delete] |
| "Pretty" | [delete] |

## Hedging Language

### Excessive Hedging
**Wrong**: "It should be noted that it is worth mentioning that the results suggest that..."
**Correct**: "The results demonstrate..."

### Appropriate Hedging
- "The results suggest..." (when certainty is limited)
- "This may indicate..." (when interpretation is tentative)
- "Under these conditions..." (when scope is limited)

## Transition Problems

### Weak Transitions
**Wrong**: "Also. Another thing. Furthermore. Moreover."
**Correct**: Use logical connectors that show relationship:
- Cause: "Therefore," "As a result," "Consequently"
- Contrast: "However," "In contrast," "Nevertheless"
- Addition: "Additionally," "Building on this"
- Sequence: "First," "Next," "Finally"

### Missing Transitions
**Wrong**: Abrupt topic changes between paragraphs
**Correct**: Explicit transition sentences at section boundaries

## Redundancy

### Common Redundancies
| Redundant | Concise |
|-----------|---------|
| "Past history" | "History" |
| "Future plans" | "Plans" |
| "Free gift" | "Gift" |
| "Each and every" | "Each" or "Every" |
| "Final outcome" | "Outcome" or "Result" |
| "Basic fundamentals" | "Fundamentals" |
| "End result" | "Result" |

## Abbreviation Mistakes

### Mistake: Undefined Abbreviations
**Wrong**: "The LSTM model was used" (first mention)
**Correct**: "The Long Short-Term Memory (LSTM) model was used" (first mention), then "LSTM" throughout

### Mistake: Inconsistent Abbreviation
**Wrong**: "ML" in one place, "machine learning" in another, "M.L." in a third
**Correct**: Define once, use consistently

## Language Verification Process

1. Search for AI-flagged words (delve, landscape, tapestry, crucial, paramount)
2. Search for passive voice ("was conducted," "it was found")
3. Check sentence lengths (target: 15-25 words)
4. Check paragraph lengths (target: 4-8 sentences)
5. Search for informal words (a lot, basically, very, thing)
6. Search for redundancies
7. Verify all abbreviations defined at first use
8. Read aloud for natural flow
