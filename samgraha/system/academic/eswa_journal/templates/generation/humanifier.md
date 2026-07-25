# Humanifier Generation Workflow

## Purpose
Raw LLM text generation frequently produces linguistic fingerprints that will fail the AI Plagiarism & Fingerprint Audits. The Humanifier workflow is a post-processing generation standard designed to transform synthetic-sounding text into a rigorous, empirically grounded, and mathematically intuitive human voice.

## The 3-Layer Fix Strategy

When a section fails an `audit/semantic/document` check (e.g., Tone, Evidence Verification), the generation template must run this three-pass rewrite:

### Layer 1: Structural Rhythm Fix
**Goal:** Increase burstiness and remove mechanical predictability.
- **Rules:**
  1. Prevent any sequence of more than two sentences with similar lengths (15-20 words).
  2. Insert a blunt, short sentence (5-8 words) to state core points.
  3. Relocate predictable transition words ("Furthermore", "Moreover", "Additionally") from the start of the sentence to the middle.
  4. Break perfect grammatical parallelism in lists.

### Layer 2: Technical DNA Injection
**Goal:** Eliminate "hollow" claims and anchor the text in empirical reality.
- **Rules:**
  1. Replace generic subjective terms ("high accuracy", "significant improvement", "robust performance") with exact numbers derived from the experiment (e.g., "+8.4% F1").
  2. Map generic model statements to specific hardware (e.g., RTX 4070 Ti) and hyperparameter choices (e.g., 1,583 unique templates, window size of 5).

### Layer 3: Voice Restoration
**Goal:** Convert textbook perfection into direct experimental explanation.
- **Rules:**
  1. Selectively change passive voice to active voice ("It was observed" -> "We observed") only where natural.
  2. Replace mechanical algorithm definitions with "why" statements (e.g., instead of defining a CRF layer mechanically, explain *why* it was chosen over softmax for this specific dataset).
  3. Inject at least one direct experimental observation per section (a sentence reflecting a unique experimental memory that an AI couldn't hallucinate).

## Output Format
The Humanifier generation agent must produce its output in three blocks:
1. **Change Summary**: A markdown table tracking what was changed (Location, Change Type, What Changed).
2. **Final Clean Section**: The fully rewritten text preserving all LaTeX, citations, and section headings.
3. **Remaining Risk Flags**: A list of sentences tagged `[NEEDS AUTHOR INPUT]` where a specific empirical anchor is missing and only the human author can provide the real number or observation.
