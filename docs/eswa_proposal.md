# Proposal: Integrating ESWA Journal System Standards into Samgraha

## 1. Executive Summary
This proposal outlines the creation of a dedicated Samgraha system standards domain for authoring and auditing papers targeted at the *Expert Systems with Applications (ESWA)* journal. By translating the ESWA reviewer guidelines, structural requirements, and AI plagiarism forensics into programmatic Samgraha audits, we can autonomously verify the quality, tone, and rigor of manuscripts prior to submission, ensuring the final output is highly technical, deeply empirical, and verifiably human-authored.

## 2. Motivation & Background
The current ESWA publication blueprint and the "ESWA Journal Publication Master Checklist" specify strict requirements for manuscript structure, statistical rigor, scalability analysis, and tone. Furthermore, AI-generated text introduces linguistic fingerprints—such as low burstiness, passive voice, and hollow technical claims—that reviewers increasingly flag as plagiarism or lack of empirical depth. Relying solely on manual review leaves room for inconsistencies. By integrating these rules into Samgraha as a new domain (`eswa_journal`), we introduce an "Antigravity Reviewer Persona" and an "AI Forensic Analyst" that deterministically and semantically audit paper drafts against Q1-ready standards and Humanification rules.

## 3. Proposed Samgraha Domain: `eswa_journal`
We propose creating a new domain at `samgraha/system/eswa_journal`. This domain treats the academic paper as a "system", where each section (Abstract, Introduction, etc.) is a component governed by documentation, semantic audit, and generation standards.

### 3.1 Directory Structure
The domain will follow standard Samgraha architecture:
```text
samgraha/system/eswa_journal/
├── 00-domain-relationships.md       # Maps the flow and dependencies of paper sections
├── audit/
│   └── semantic/
│       ├── document/                # Global persona rules (Tone, AI Plagiarism, Claims)
│       └── section/                 # Section-specific content rules (IMRaD, Baselines)
├── documentation-standards/         # The expected structure and template for each section
├── calculation/                     # Scoring mechanics for the audits
├── plan/
│   └── core/
│       └── tiers.yaml               # Hierarchy of the paper sections
└── templates/
    └── generation/                  # Humanification pipeline templates
```

## 4. Documentation Standards (Section-Level Rules)
We will create standards for each section of the ESWA paper dictating structure and mandatory sub-elements.

1. **`01-abstract-standards.md`**: Enforces IMRaD structure, numerical improvement mention (e.g., +8.4% F1), and strict 150-250 word limit. No citations.
2. **`02-introduction-standards.md`**: Requires explicit global problem, technical gap, limitations of prior systems, and a strict bulleted list of contributions.
3. **`03-related-work-standards.md`**: Enforces structured taxonomy, 15+ recent references, 2-4 ESWA citations, a summary comparison table, and a clear gap-closing narrative bridge.
4. **`04-problem-definition-standards.md`**: Requires mathematical notation, formal set definitions, explicit assumptions, and objective function (if optimization-based).
5. **`05-methodology-standards.md`**: Enforces visual hierarchy (logical vs physical), formal Big-O complexity analysis (Time/Space/Scalability), mathematical grounding, and algorithmic clarity (pseudocode).
6. **`06-experimental-setup-standards.md`**: Requires reproducibility checklist (hardware/software/seed), minimum 3 baselines (1 classical, 2 recent SOTA), ablation baselines, and rigorous statistical significance testing (e.g., paired t-test, Wilcoxon, p < 0.05).
7. **`07-results-standards.md`**: Enforces mandatory ablation studies, sensitivity/robustness analysis (e.g., noise injection), and a structured "Threats to Validity" subsection (Internal, External, Construct, Dataset bias).
8. **`08-implications-standards.md`**: Evaluates practical/managerial implications, ensuring realistic pathways to industry application.
9. **`09-limitations-standards.md`**: Ensures transparent scalability constraints and ethical considerations are documented.
10. **`10-conclusion-standards.md`**: Restates contributions and applied relevance without introducing new claims.
11. **`11-references-standards.md`**: Checks ratio of recent citations (60-70% from 2022-2026).

## 5. Semantic Audit Rules (Document-Level Persona)
To emulate a Q1 Journal Reviewer and an AI Forensic Analyst, we will implement global semantic audits across the `document` level:

### 5.1 Antigravity Reviewer Persona Audits
Derived directly from the master checklist, these audits ensure structural and scientific rigor:
- **Claim vs. Evidence Check**: Maps any claims of "stability" or "improvement" to corresponding empirical tables, metrics, or citations. Flags unsupported claims.
- **Citation Integrity Check**: Audits references to ensure no predatory journals or blogs are used. Cross-checks that all papers mentioned in "Related Work" exist in the References (e.g. Q1/Q2 Scopus, CORE A/A*).
- **Structural Coherence**: Ensures logical transitions (Introduction -> Related Work -> Methodology).
- **Validation & Baseline Checks**: Ensures at least 3 baselines, flags missing complexity analysis, and verifies the completeness of the reproducibility checklist.

### 5.2 AI Plagiarism & Fingerprint Audits
- **Linguistic Fingerprint Scan**: Flags AI tells such as uniform sentence lengths, predictable transition words at sentence starts ("Furthermore", "Moreover"), and passive voice ("It was observed").
- **Hollow Technical Claim Check (DNA Check)**: Flags generic precision language ("high accuracy", "significant improvement", "robust results") that lacks specific technical anchors (actual hardware, exact hyper-parameters, specific dataset nuances, actual F1 scores).
- **Algorithm/Math Sentence Check**: Flags mathematical explanations that only mechanically restate formulas without explaining the intuitive reasoning behind the architectural choice.

## 6. Generation Standards (Humanifier Workflow)
Because raw documentation generation often yields non-humanified content, we will implement a 3-layer generation and rewrite pipeline to ensure the text passes AI forensics:

1. **Layer 1: Structural Rhythm Fix**: 
   - Varies sentence length intentionally (combining short 5-8 word blunt statements with 25-30 word contextual explanations).
   - Relocates transition words to the middle of sentences.
   - Breaks strict grammatical parallelism in lists.
2. **Layer 2: Technical DNA Injection**: 
   - Replaces all abstract claims with concrete experimental anchors (e.g., swapping "The model was fast" with "The Bi-LSTM-CRF configuration parsed 1,583 unique templates on an RTX 4070 Ti").
3. **Layer 3: Voice Restoration**: 
   - Selectively applies active voice to experimental actions ("We observed...").
   - Restores a direct "explanation tone" for complex concepts rather than textbook definitions.
   - Outputs a three-block report format: Change Summary, Final Clean Section, and Remaining Risk Flags (to highlight where the author must insert personal experimental memory).

## 7. Domain Relationships & Tiers
The `00-domain-relationships.md` will define how sections support one another:
- **Tier 1 (Foundation)**: Problem Definition, Related Work
- **Tier 2 (Core)**: Methodology (requires Tier 1)
- **Tier 3 (Validation)**: Experimental Setup, Results (validates Tier 2)
- **Tier 4 (Synthesis)**: Introduction, Abstract, Conclusion (summarizes Tiers 1-3)

*Rule*: Methodology cannot introduce a solution to a problem not defined in the Problem Definition.

## 8. Execution Strategy
1. **Approval**: Review this proposal for completeness.
2. **Implementation**: Once approved, create the files in `samgraha/system/eswa_journal` as outlined above.
3. **Integration**: Run Samgraha's `compile` on the new domain to verify the structural and semantic audit rules.
4. **Testing**: Run a Samgraha `audit` against a draft ESWA paper to ensure both the Reviewer Persona and AI Forensic Analyst successfully catch violations and prompt the Humanifier workflow.
