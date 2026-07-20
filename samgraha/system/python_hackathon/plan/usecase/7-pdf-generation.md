# Use-case 7 — PDF Generation

**Script**: `export_team_pdfs.py`

**Inputs**:
- Use-case 6's HTML output (all of it, per team)

**Action**: One PDF per team, merging HTML pages in fixed domain order.

**Completion criteria**:
- One PDF file per registered team, non-zero size
- Page count matches expected count (31 per team: 30 domain pages + 1 team-summary; fewer if some domains have zero audit data)

**Verify script**: `verify_usecase_7_pdf_generation.py --standard python_hackathon`
- File existence/size check
- `pypdf.PdfReader(path).pages` count vs expected count (computed from same domain-data lookup as use-case 6)
