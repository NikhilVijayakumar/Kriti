"""report_html.py — Generates a self-contained HTML report with embedded charts.

Reads chart PNGs from visualize.py output, check results, deterministic/semantic
audit rules, and calculation scores. Produces a single HTML file with:
- Embedded chart images (base64-encoded)
- Detailed tables for every check, rule, and criterion
- Score summary with band classification
- Tier-by-tier breakdown

Usage:
  python report_html.py --system-root <path> --results-dir <path> --charts-dir <path> --out <path>
  python report_html.py --system-root <path> --results-dir <path> --charts-dir <path> --out <path> --scores-json <path>
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from _common import load_yaml, read_text, write_text, ALL_DOMAINS, DOMAIN_NUMS


# ---------------------------------------------------------------------------
# HTML template
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
:root {{
    --bg: #0d1117;
    --surface: #161b22;
    --border: #30363d;
    --text: #c9d1d9;
    --text-muted: #8b949e;
    --accent: #58a6ff;
    --green: #3fb950;
    --red: #f85149;
    --orange: #d29922;
    --purple: #bc8cff;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    padding: 2rem;
}}
.container {{ max-width: 1200px; margin: 0 auto; }}
h1 {{
    font-size: 2rem;
    margin-bottom: 0.5rem;
    color: #fff;
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
}}
h2 {{
    font-size: 1.4rem;
    margin: 2rem 0 1rem;
    color: var(--accent);
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.3rem;
}}
h3 {{
    font-size: 1.1rem;
    margin: 1.5rem 0 0.5rem;
    color: var(--text);
}}
.meta {{
    color: var(--text-muted);
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}}
.chart-container {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem 0;
    text-align: center;
}}
.chart-container img {{
    max-width: 100%;
    height: auto;
    border-radius: 4px;
}}
.chart-caption {{
    color: var(--text-muted);
    font-size: 0.85rem;
    margin-top: 0.5rem;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    font-size: 0.9rem;
}}
th, td {{
    padding: 0.6rem 0.8rem;
    text-align: left;
    border-bottom: 1px solid var(--border);
}}
th {{
    background: var(--surface);
    color: var(--accent);
    font-weight: 600;
    position: sticky;
    top: 0;
}}
tr:hover {{ background: rgba(88, 166, 255, 0.05); }}
.status-pass {{ color: var(--green); font-weight: 600; }}
.status-fail {{ color: var(--red); font-weight: 600; }}
.status-error {{ color: var(--orange); font-weight: 600; }}
.status-na {{ color: var(--text-muted); }}
.badge {{
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
}}
.badge-a {{ background: rgba(63, 185, 80, 0.2); color: var(--green); }}
.badge-b {{ background: rgba(210, 153, 34, 0.2); color: var(--orange); }}
.badge-c {{ background: rgba(188, 140, 255, 0.2); color: var(--purple); }}
.score-box {{
    display: inline-block;
    padding: 1rem 2rem;
    border-radius: 8px;
    text-align: center;
    margin: 0.5rem;
}}
.score-value {{ font-size: 2rem; font-weight: 700; }}
.score-label {{ font-size: 0.85rem; color: var(--text-muted); }}
.score-excellent {{ background: rgba(63, 185, 80, 0.15); border: 1px solid var(--green); }}
.score-verygood {{ background: rgba(63, 185, 80, 0.1); border: 1px solid rgba(63, 185, 80, 0.5); }}
.score-good {{ background: rgba(210, 153, 34, 0.15); border: 1px solid var(--orange); }}
.score-acceptable {{ background: rgba(210, 153, 34, 0.1); border: 1px solid rgba(210, 153, 34, 0.5); }}
.score-needs {{ background: rgba(248, 81, 73, 0.15); border: 1px solid var(--red); }}
.score-na {{ background: rgba(139, 148, 158, 0.1); border: 1px solid var(--text-muted); }}
.toc {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin: 1rem 0;
}}
.toc a {{
    color: var(--accent);
    text-decoration: none;
}}
.toc a:hover {{ text-decoration: underline; }}
.toc ul {{ list-style: none; padding-left: 1rem; }}
.toc li {{ margin: 0.3rem 0; }}
.summary-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}}
.finding {{
    padding: 0.5rem 0.8rem;
    border-left: 3px solid var(--border);
    margin: 0.3rem 0;
    font-size: 0.85rem;
}}
.finding-error {{ border-color: var(--red); }}
.finding-warning {{ border-color: var(--orange); }}
.finding-info {{ border-color: var(--accent); }}
</style>
</head>
<body>
<div class="container">
<h1>{title}</h1>
<div class="meta">
    <p>Generated: {timestamp}</p>
    <p>System: {system_name} | Use Case: {use_case}</p>
    <p>Domains: {domain_count} | Checks: {check_count} | Rules: {rule_count}</p>
</div>

<div class="toc">
<strong>Contents</strong>
<ul>
{toc_items}
</ul>
</div>

{sections}
</div>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _img_to_base64(path: Path) -> str:
    """Convert an image file to a base64 data URI."""
    if not path.exists():
        return ""
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    ext = path.suffix.lower().lstrip(".")
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(ext, "image/png")
    return f"data:{mime};base64,{b64}"


def _status_class(status: str) -> str:
    return f"status-{status}" if status in ("pass", "fail", "error") else "status-na"


def _badge_class(category: str) -> str:
    return f"badge-{category.lower()}" if category in ("A", "B", "C") else ""


def _score_box_class(rating: str) -> str:
    mapping = {
        "Excellent": "score-excellent",
        "Very Good": "score-verygood",
        "Good": "score-good",
        "Acceptable": "score-acceptable",
        "Needs Improvement": "score-needs",
    }
    return mapping.get(rating, "score-na")


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_check_results(results_dir: Path) -> list[dict[str, Any]]:
    results = []
    for json_file in results_dir.rglob("*.json"):
        if json_file.name == "results.json":
            continue
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "check" in data and "status" in data:
                results.append(data)
        except (json.JSONDecodeError, KeyError):
            continue
    return results


def load_deterministic_rules(system_root: Path) -> dict[str, list[dict]]:
    rules: dict[str, list[dict]] = {}
    audit_dir = system_root / "audit" / "deterministic"

    doc_dir = audit_dir / "document"
    if doc_dir.is_dir():
        for yaml_file in sorted(doc_dir.glob("*.yaml")):
            if "-relationships" in yaml_file.name:
                continue
            data = load_yaml(yaml_file)
            domain = data.get("domain", yaml_file.stem.split("-")[0])
            rules.setdefault(domain, []).extend(data.get("rules", []))

    sec_dir = audit_dir / "section"
    if sec_dir.is_dir():
        for domain_dir in sorted(sec_dir.iterdir()):
            if not domain_dir.is_dir():
                continue
            domain = domain_dir.name
            for yaml_file in sorted(domain_dir.glob("*.yaml")):
                data = load_yaml(yaml_file)
                rules.setdefault(domain, []).extend(data.get("rules", []))

    return rules


def load_semantic_criteria(system_root: Path) -> dict[str, list[dict]]:
    criteria: dict[str, list[dict]] = {}
    audit_dir = system_root / "audit" / "semantic"

    for md_file in sorted(audit_dir.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        parts = md_file.parts
        try:
            sec_idx = parts.index("semantic")
            domain = parts[sec_idx + 2] if len(parts) > sec_idx + 2 else "unknown"
        except ValueError:
            domain = "unknown"

        in_table = False
        for line in content.split("\n"):
            if "| ID |" in line and "Weight |" in line:
                in_table = True
                continue
            if in_table and line.startswith("|---"):
                continue
            if in_table and line.startswith("| C"):
                cols = [c.strip() for c in line.split("|") if c.strip()]
                if len(cols) >= 4:
                    criteria.setdefault(domain, []).append({
                        "id": cols[0],
                        "weight": cols[1],
                        "score": cols[2],
                        "description": cols[3],
                    })
            elif in_table and not line.startswith("|"):
                in_table = False

    return criteria


def load_results_summary(results_dir: Path) -> dict[str, Any]:
    results_json = results_dir / "results.json"
    if results_json.exists():
        return json.loads(results_json.read_text(encoding="utf-8"))
    return {}


# ---------------------------------------------------------------------------
# Section builders
# ---------------------------------------------------------------------------

def build_overview_section(
    check_results: list[dict[str, Any]],
    det_rules: dict[str, list[dict]],
    sem_criteria: dict[str, list[dict]],
    all_domain_scores: dict[str, dict[str, Any]],
    charts_dir: Path,
) -> str:
    html = []

    # Score summary boxes
    html.append('<div class="summary-grid">')
    total_checks = len(check_results)
    pass_count = sum(1 for r in check_results if r["status"] == "pass")
    fail_count = sum(1 for r in check_results if r["status"] == "fail")
    error_count = sum(1 for r in check_results if r["status"] == "error")

    html.append(f'<div class="score-box score-excellent"><div class="score-value">{pass_count}</div><div class="score-label">Checks Passed</div></div>')
    html.append(f'<div class="score-box score-needs"><div class="score-value">{fail_count}</div><div class="score-label">Checks Failed</div></div>')
    html.append(f'<div class="score-box score-acceptable"><div class="score-value">{error_count}</div><div class="score-label">Errors</div></div>')
    html.append(f'<div class="score-box score-na"><div class="score-value">{total_checks}</div><div class="score-label">Total Checks</div></div>')
    html.append('</div>')

    # Charts
    chart_files = [
        ("check_results_by_domain.png", "Deterministic Check Results by Domain", "Pass/fail/error distribution across all 16 domains"),
        ("category_breakdown.png", "Check Results by Category", "A (automated), B (semi-automated), C (cross-domain) breakdown"),
        ("score_bands.png", "Score Band Distribution", "Overall rating distribution across domains"),
        ("domain_scores.png", "Documentation Score by Domain", "Final score per domain with Acceptable/Excellent thresholds"),
    ]

    for filename, title, caption in chart_files:
        chart_path = charts_dir / filename
        img_b64 = _img_to_base64(chart_path)
        if img_b64:
            html.append(f'<div class="chart-container">')
            html.append(f'<img src="{img_b64}" alt="{title}">')
            html.append(f'<div class="chart-caption">{caption}</div>')
            html.append(f'</div>')

    return "\n".join(html)


def build_deterministic_section(
    check_results: list[dict[str, Any]],
    det_rules: dict[str, list[dict]],
    charts_dir: Path,
) -> str:
    html = []

    # Heatmap chart
    chart_path = charts_dir / "rule_weights_heatmap.png"
    img_b64 = _img_to_base64(chart_path)
    if img_b64:
        html.append(f'<div class="chart-container">')
        html.append(f'<img src="{img_b64}" alt="Rule Weight Heatmap">')
        html.append(f'<div class="chart-caption">Deterministic rule weight distribution by domain — higher weights indicate critical rules</div>')
        html.append(f'</div>')

    # Heatmap
    heatmap_path = charts_dir / "section_heatmap.png"
    img_b64 = _img_to_base64(heatmap_path)
    if img_b64:
        html.append(f'<div class="chart-container">')
        html.append(f'<img src="{img_b64}" alt="Section Heatmap">')
        html.append(f'<div class="chart-caption">Check results heatmap — green=pass, red=fail, orange=error</div>')
        html.append(f'</div>')

    # Detailed check results table
    html.append('<h3>Check Results Detail</h3>')
    html.append('<table>')
    html.append('<tr><th>Check</th><th>Domain</th><th>Category</th><th>Status</th><th>Metrics</th></tr>')
    for r in sorted(check_results, key=lambda x: (x.get("domain", ""), x.get("check", ""))):
        metrics_str = json.dumps(r.get("metrics", {}), indent=None)
        if len(metrics_str) > 80:
            metrics_str = metrics_str[:80] + "..."
        html.append(f'<tr>'
                    f'<td>{r.get("check", "")}</td>'
                    f'<td>{r.get("domain", "")}</td>'
                    f'<td><span class="badge {_badge_class(r.get("category", ""))}">{r.get("category", "")}</span></td>'
                    f'<td class="{_status_class(r.get("status", ""))}">{r.get("status", "")}</td>'
                    f'<td><code>{metrics_str}</code></td>'
                    f'</tr>')
    html.append('</table>')

    # Rules per domain
    html.append('<h3>Deterministic Audit Rules by Domain</h3>')
    for domain in sorted(det_rules.keys()):
        rules = det_rules[domain]
        html.append(f'<h3>{domain} ({len(rules)} rules)</h3>')
        html.append('<table>')
        html.append('<tr><th>ID</th><th>Description</th><th>Severity</th><th>Weight</th><th>Mandatory</th></tr>')
        for rule in rules:
            html.append(f'<tr>'
                        f'<td><code>{rule.get("id", "")}</code></td>'
                        f'<td>{rule.get("description", "")}</td>'
                        f'<td>{rule.get("severity", "")}</td>'
                        f'<td>{rule.get("weight", 0)}</td>'
                        f'<td>{"Yes" if rule.get("mandatory") else "No"}</td>'
                        f'</tr>')
        html.append('</table>')

    return "\n".join(html)


def build_semantic_section(
    sem_criteria: dict[str, list[dict]],
    charts_dir: Path,
) -> str:
    html = []

    for domain in sorted(sem_criteria.keys()):
        criteria = sem_criteria[domain]
        html.append(f'<h3>{domain} ({len(criteria)} criteria)</h3>')
        html.append('<table>')
        html.append('<tr><th>ID</th><th>Weight</th><th>Max Score</th><th>Description</th></tr>')
        for c in criteria:
            html.append(f'<tr>'
                        f'<td><code>{c["id"]}</code></td>'
                        f'<td>{c["weight"]}</td>'
                        f'<td>{c["score"]}</td>'
                        f'<td>{c["description"]}</td>'
                        f'</tr>')
        html.append('</table>')

    return "\n".join(html)


def build_scores_section(
    all_domain_scores: dict[str, dict[str, Any]],
    charts_dir: Path,
) -> str:
    html = []

    # Radar chart
    radar_path = charts_dir / "scoring_radar.png"
    img_b64 = _img_to_base64(radar_path)
    if img_b64:
        html.append(f'<div class="chart-container">')
        html.append(f'<img src="{img_b64}" alt="Scoring Radar">')
        html.append(f'<div class="chart-caption">4-bucket score breakdown — Deterministic Document (25%), Deterministic Section (25%), Semantic Document (25%), Semantic Section (25%)</div>')
        html.append(f'</div>')

    # Tier progression
    tier_path = charts_dir / "tier_progression.png"
    img_b64 = _img_to_base64(tier_path)
    if img_b64:
        html.append(f'<div class="chart-container">')
        html.append(f'<img src="{img_b64}" alt="Tier Progression">')
        html.append(f'<div class="chart-caption">Average score progression across tiers with min–max range</div>')
        html.append(f'</div>')

    # Domain scores table
    if all_domain_scores:
        html.append('<h3>Domain Scores Detail</h3>')
        html.append('<table>')
        html.append('<tr><th>Domain</th><th>Final Score</th><th>Rating</th><th>Det. Doc</th><th>Det. Sec</th><th>Sem. Doc</th><th>Sem. Sec</th></tr>')
        for domain in sorted(all_domain_scores.keys()):
            s = all_domain_scores[domain]
            final = s.get("final_score", {}).get("score", 0)
            rating = s.get("score_bands", {}).get("rating", "N/A")
            d_doc = s.get("deterministic_whole", {}).get("score", "-")
            d_sec = s.get("deterministic_section", {}).get("score", "-")
            s_doc = s.get("semantic_whole", {}).get("score", "-")
            s_sec = s.get("semantic_section", {}).get("score", "-")
            html.append(f'<tr>'
                        f'<td>{domain}</td>'
                        f'<td><strong>{final}</strong></td>'
                        f'<td><span class="{_score_box_class(rating)}" style="padding:0.15rem 0.5rem;border-radius:4px;font-size:0.8rem;">{rating}</span></td>'
                        f'<td>{d_doc}</td>'
                        f'<td>{d_sec}</td>'
                        f'<td>{s_doc}</td>'
                        f'<td>{s_sec}</td>'
                        f'</tr>')
        html.append('</table>')

    return "\n".join(html)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def generate_html_report(
    system_root: Path,
    results_dir: Path,
    charts_dir: Path,
    out_path: Path,
    scores_json: Path | None = None,
) -> Path:
    """Generate the full HTML report."""
    print("Loading data...")
    check_results = load_check_results(results_dir)
    det_rules = load_deterministic_rules(system_root)
    sem_criteria = load_semantic_criteria(system_root)
    results_summary = load_results_summary(results_dir)

    all_domain_scores = {}
    for tier_key, tier_data in results_summary.get("tiers", {}).items():
        for domain, domain_score in tier_data.get("results", {}).items():
            if isinstance(domain_score, dict):
                normalized = {
                    "final_score": {"score": domain_score.get("score", 0)},
                    "score_bands": {"rating": domain_score.get("rating", "N/A")},
                }
                all_domain_scores[domain] = normalized

    if scores_json and scores_json.exists():
        extra = json.loads(scores_json.read_text(encoding="utf-8"))
        all_domain_scores.update(extra)

    use_case = results_summary.get("use_case", "unknown")
    system_name = system_root.name

    print(f"  Check results: {len(check_results)}")
    print(f"  Deterministic rules: {sum(len(v) for v in det_rules.values())}")
    print(f"  Semantic criteria: {sum(len(v) for v in sem_criteria.values())}")

    # Build sections
    print("Building report sections...")
    overview = build_overview_section(check_results, det_rules, sem_criteria, all_domain_scores, charts_dir)
    deterministic = build_deterministic_section(check_results, det_rules, charts_dir)
    semantic = build_semantic_section(sem_criteria, charts_dir)
    scores = build_scores_section(all_domain_scores, charts_dir)

    # TOC
    toc_items = [
        '<li><a href="#overview">1. Overview &amp; Charts</a></li>',
        '<li><a href="#deterministic">2. Deterministic Audit</a></li>',
        '<li><a href="#semantic">3. Semantic Audit</a></li>',
        '<li><a href="#scores">4. Scores &amp; Visualization</a></li>',
    ]

    sections_html = f"""
<h2 id="overview">1. Overview &amp; Charts</h2>
{overview}

<h2 id="deterministic">2. Deterministic Audit</h2>
{deterministic}

<h2 id="semantic">3. Semantic Audit</h2>
{semantic}

<h2 id="scores">4. Scores &amp; Visualization</h2>
{scores}
"""

    # Render
    html = HTML_TEMPLATE.format(
        title=f"{system_name} — Audit Report",
        timestamp=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        system_name=system_name,
        use_case=use_case,
        domain_count=len(all_domain_scores) or len(DOMAIN_NUMS),
        check_count=len(check_results),
        rule_count=sum(len(v) for v in det_rules.values()),
        toc_items="\n".join(toc_items),
        sections=sections_html,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"\nHTML report written to {out_path}")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate HTML audit report")
    parser.add_argument("--system-root", required=True, help="Path to system directory")
    parser.add_argument("--results-dir", required=True, help="Directory with check result JSONs")
    parser.add_argument("--charts-dir", required=True, help="Directory with chart PNGs from visualize.py")
    parser.add_argument("--out", required=True, help="Output HTML file path")
    parser.add_argument("--scores-json", help="Path to scores JSON (optional)")
    args = parser.parse_args()

    system_root = Path(args.system_root)
    results_dir = Path(args.results_dir)
    charts_dir = Path(args.charts_dir)
    out_path = Path(args.out)
    scores_json = Path(args.scores_json) if args.scores_json else None

    if not system_root.is_dir():
        print(f"Error: system-root not found: {system_root}", file=sys.stderr)
        sys.exit(1)

    generate_html_report(system_root, results_dir, charts_dir, out_path, scores_json)


if __name__ == "__main__":
    main()
