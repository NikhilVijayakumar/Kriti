# Proposal: Integrating PCEMS 2026 Conference Standards into Samgraha

## 1. Executive Summary
This proposal outlines the creation of a dedicated Samgraha system standards domain for authoring and auditing papers targeted at the **PCEMS 2026** conference. By translating the PCEMS manuscript preparation guidelines (formatting, structure, and media rules) into programmatic Samgraha audits, we can autonomously verify the quality and formatting of manuscripts prior to CMT submission, avoiding desk-rejections due to layout or structural errors.

## 2. Motivation & Background
The PCEMS 2026 guidelines dictate strict typographic, structural, and media-handling rules (e.g., specific Arial font sizes for headings, single-column layout, and exact placement of tables/figures). It also strictly mandates APA style references and specific PDF export parameters. Integrating these into a Samgraha domain (`pcems_2026`) allows for rigorous, automated pre-submission compliance checks.

## 3. Proposed Samgraha Domain: `pcems_2026`
We propose creating a new domain at `samgraha/system/pcems_2026`. This domain will enforce both the structural sections and the exact typography/formatting rules defined in the guidelines.

### 3.1 Directory Structure
```text
samgraha/system/pcems_2026/
├── 00-domain-relationships.md       
├── audit/
│   ├── deterministic/               
│   │   └── document/                # Formatting audits (font sizes, table placement)
│   └── semantic/
│       ├── document/                # Global rules (Originality, PDF export constraints)
│       └── section/                 # Section-specific content rules
├── documentation-standards/         # Expected structure for the 5 mandatory sections
├── calculation/                     
└── plan/
    └── core/
        └── tiers.yaml               
```

## 4. Documentation Standards (Section-Level Rules)
We will create standards for the mandatory sections explicitly mentioned in the PCEMS guidelines.

1. **`01-title-and-metadata-standards.md`**: 
   - *Rules*: Enforces Title (Arial Bold 14pt centered), Authors (Arial 12pt Bold centered), Affiliations (Arial 11pt centered), Email, and 4-5 Keywords (Arial 12pt bold).
2. **`02-introduction-standards.md`**: 
   - *Rules*: Expected to introduce the research problem and objectives.
3. **`03-methodology-standards.md`**: 
   - *Rules*: Requires explanation of the research methodology.
4. **`04-findings-standards.md`**: 
   - *Rules*: Mandates that all images and tables (created via MS Word functions) are placed immediately after the first point of reference, not at the end.
5. **`05-conclusion-standards.md`**: 
   - *Rules*: Closing remarks.
6. **`06-references-standards.md`**: 
   - *Rules*: Enforces APA referencing style and 8pt font size.

## 5. Semantic & Formatting Audit Rules (Document-Level)
Since PCEMS heavily emphasizes formatting, we will implement specific audits alongside scientific rigor checks:

### 5.1 Formatting & Submission Integrity Audits
- **Formatting & Typography Check**: Audits the presence of single-column format, Arial 12pt Bold (Heading 1), Arial 12pt (Heading 2), Arial 12pt Italics (Heading 3), and Arial 11pt (Body text).
- **Media Placement Check**: Flags any document where tables or figures are aggregated at the end of the manuscript instead of inline.
- **PDF Export & Integrity Check**: Ensures the final PDF has scalable fonts embedded, contains NO transparent pixels (alpha-channels) in images, and has Adobe Document Security disabled.
- **Originality Check**: Enforces the guideline that the paper is not under review elsewhere.

### 5.2 Antigravity Reviewer Persona Audits
Derived directly from the master checklist, these audits ensure structural and scientific rigor:
- **Claim vs. Evidence Check**: Maps any claims of "stability" or "improvement" to corresponding empirical tables, metrics, or citations. Flags unsupported claims.
- **Citation Integrity Check**: Audits references to ensure no predatory journals or blogs are used. Cross-checks that all papers mentioned in "Related Work" exist in the References (e.g. Q1/Q2 Scopus, CORE A/A*).
- **Structural Coherence**: Ensures logical transitions (Introduction -> Methodology -> Findings).
- **Validation & Baseline Checks**: Ensures at least 3 baselines, flags missing complexity analysis, and verifies the completeness of the reproducibility checklist.

### 5.3 AI Plagiarism & Fingerprint Audits
- **Linguistic Fingerprint Scan**: Flags AI tells such as uniform sentence lengths, predictable transition words at sentence starts ("Furthermore", "Moreover"), and passive voice ("It was observed").
- **Hollow Technical Claim Check (DNA Check)**: Flags generic precision language ("high accuracy", "significant improvement", "robust results") that lacks specific technical anchors (actual hardware, exact hyper-parameters, specific dataset nuances, actual F1 scores).
- **Algorithm/Math Sentence Check**: Flags mathematical explanations that only mechanically restate formulas without explaining the intuitive reasoning behind the architectural choice.
## 6. Domain Relationships & Tiers
The `00-domain-relationships.md` will define the flow:
- **Tier 1**: Introduction, Methodology
- **Tier 2**: Findings (requires Methodology)
- **Tier 3**: Conclusion, References (validates Findings)
- **Tier 4**: Title & Metadata (summarizes the above)

## 7. Execution Strategy
1. **Approval**: Review this proposal for completeness.
2. **Implementation**: Once approved, create the files in `samgraha/system/pcems_2026` as outlined above.
3. **Integration**: Run Samgraha's `compile` on the new domain.
