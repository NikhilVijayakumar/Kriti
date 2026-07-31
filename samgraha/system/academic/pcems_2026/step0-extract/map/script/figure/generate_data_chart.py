"""generate_data_chart.py — deterministic data-chart generation for figure_map
rows whose figure_type is comparison_chart or graph_plot and whose
data_table_map_key links to an academic_table_map row.

Reads the linked table's rows_json + columns_json, re-renders as a
matplotlib chart, writes to docs/paper/Bodha/drafts/visualizations/generated/,
and sets asset_path on the figure_map row.

Idempotent: skips rows where asset_path is already non-null.
--force flag in payload regenerates.

This is the data-chart analogue of the mermaid generation path, but fully
deterministic (no LLM call needed — data comes from the table_map entry).

Expected --in payload:
  {paper_id: int, force: bool (optional)}
"""
import json as _json
import sys
from pathlib import Path as _Path

sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent.parent / "common" / "script"))
import academic_schema

CHART_TYPES = ("comparison_chart", "graph_plot")

GENERATED_DIR = _Path(
    "docs/paper/Bodha/drafts/visualizations/generated"
)


def _render_chart(columns_json, rows_json, output_path):
    """Render a matplotlib chart from table_map columns+rows.

    Returns True on success, False on any error.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        return False

    try:
        cols = _json.loads(columns_json) if isinstance(columns_json, str) else columns_json
        rows = _json.loads(rows_json) if isinstance(rows_json, str) else rows_json
    except (_json.JSONDecodeError, TypeError):
        return False

    if not rows or not cols:
        return False

    n_cols = len(cols)
    n_rows = len(rows)

    # Auto-detect whether this is a grouped-bar or line-chart scenario
    # by checking if the first column has repeated values (grouped) or unique (flat).
    first_col_vals = [r[0] for r in rows if r]
    is_grouped = len(first_col_vals) != len(set(first_col_vals))

    fig, ax = plt.subplots(figsize=(10, 6))

    if is_grouped and n_cols >= 3:
        # Grouped bar chart: first column = groups, remaining = series
        groups = list(dict.fromkeys(first_col_vals))  # unique, ordered
        series_labels = [c["label"] for c in cols[1:]]
        x = np.arange(len(groups))
        n_series = len(series_labels)
        width = 0.8 / n_series

        for s_idx, s_label in enumerate(series_labels):
            s_vals = []
            for g in groups:
                matching = [r for r in rows if r and r[0] == g]
                if matching:
                    try:
                        s_vals.append(float(matching[0][s_idx + 1]))
                    except (ValueError, IndexError):
                        s_vals.append(0)
                else:
                    s_vals.append(0)
            ax.bar(x + s_idx * width, s_vals, width, label=s_label)

        ax.set_xticks(x + width * (n_series - 1) / 2)
        ax.set_xticklabels(groups, fontsize=10)
        ax.set_ylabel(cols[1]["label"] if len(cols) > 1 else "")
        ax.legend(fontsize=9)

    else:
        # Line chart or single-series bar: first column = x labels, rest = lines
        x_labels = [str(r[0]) for r in rows if r]

        for c_idx in range(1, n_cols):
            vals = []
            label = cols[c_idx]["label"]
            for r in rows:
                if r and c_idx < len(r):
                    try:
                        vals.append(float(r[c_idx]))
                    except (ValueError, TypeError):
                        vals.append(0)
            ax.plot(range(len(vals)), vals, "o-", label=label, linewidth=2)

        ax.set_xticks(range(len(x_labels)))
        ax.set_xticklabels(x_labels, fontsize=9, rotation=30, ha="right")
        ax.legend(fontsize=9)

    ax.grid(True, alpha=0.3)
    ax.set_title(cols[0]["label"] if len(cols) > 0 else "Chart", fontsize=13)
    plt.tight_layout()
    plt.savefig(str(output_path), dpi=300, bbox_inches="tight")
    plt.close()
    return True


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    import sqlite3
    conn = academic_schema.get_conn(db_path=db_path)
    conn.row_factory = sqlite3.Row

    paper_id = payload.get("paper_id")
    force = payload.get("force", False)

    if not paper_id:
        write_envelope(out_path, status="error",
                       message="paper_id required in payload")
        conn.close()
        return

    generated_dir = _Path(repo_root) / GENERATED_DIR
    generated_dir.mkdir(parents=True, exist_ok=True)

    # Gather rows: comparison_chart/graph_plot with data_table_map_key and no asset
    if force:
        rows = conn.execute(
            "SELECT * FROM academic_figure_map "
            "WHERE paper_id=? AND figure_type IN (?, ?) "
            "AND data_table_map_key IS NOT NULL",
            (paper_id,) + CHART_TYPES,
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM academic_figure_map "
            "WHERE paper_id=? AND figure_type IN (?, ?) "
            "AND data_table_map_key IS NOT NULL "
            "AND (asset_path IS NULL OR asset_path = '')",
            (paper_id,) + CHART_TYPES,
        ).fetchall()

    if not rows:
        write_envelope(out_path, status="ok",
                       message="no data-chart-eligible rows to process",
                       paper_id=paper_id, rows_checked=0)
        conn.close()
        return

    processed = 0
    rendered = 0
    failed = 0

    for row in rows:
        map_key = row["map_key"]
        row_id = row["id"]
        data_key = row.get("data_table_map_key")
        if not data_key:
            continue

        processed += 1

        # Read source table data
        table_entry = academic_schema.get_map_entry(
            conn, paper_id, "table", data_key)
        if not table_entry:
            failed += 1
            continue

        columns_json = table_entry.get("columns_json")
        rows_json = table_entry.get("rows_json")
        if not columns_json or not rows_json:
            failed += 1
            continue

        # Sanitize map_key for filename (max 80 chars, .png suffix)
        safe_name = map_key.replace("_", "-").replace(" ", "-").lower()
        safe_name = "".join(c for c in safe_name if c.isalnum() or c in "-.")
        safe_name = safe_name[:80] + ".png"
        png_path = generated_dir / safe_name

        ok = _render_chart(columns_json, rows_json, png_path)
        if not ok:
            failed += 1
            continue

        # Persist asset_path
        asset_rel = str(GENERATED_DIR / safe_name).replace("\\", "/")
        conn.execute(
            "UPDATE academic_figure_map SET asset_path=? WHERE id=?",
            (asset_rel, row_id),
        )
        rendered += 1

    conn.commit()
    conn.close()

    write_envelope(out_path, status="ok",
                   message=f"rendered {rendered}/{processed} data charts "
                           f"({failed} failed) for paper {paper_id}",
                   paper_id=paper_id,
                   rows_checked=len(rows),
                   processed=processed,
                   rendered=rendered,
                   failed=failed)


if __name__ == "__main__":
    main()
