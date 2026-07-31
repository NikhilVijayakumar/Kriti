"""introspect_schema.py — DB introspection + ER diagram generator.

Connects to knowledge.db, enumerates academic_* tables and views,
emits a Mermaid erDiagram block and a human-readable text summary.

Usage:
    python .samgraha/pcems_2026/common/script/introspect_schema.py
    python .samgraha/pcems_2026/common/script/introspect_schema.py --db-path /custom/path/knowledge.db
    python .samgraha/pcems_2026/common/script/introspect_schema.py --out-dir /custom/path/output
"""

import argparse
import os
import sys
from academic_schema import get_conn

_TABLE_FILTER = "academic_%"


def _safe_name(name):
    if name and not name.replace("_", "").isalnum():
        return f"`{name}`"
    return name


def _fmt_type(col):
    t = col["type"] or ""
    pk = " PK" if col["pk"] else ""
    nn = " NOT NULL" if col["notnull"] and not col["pk"] else ""
    return f"{t}{pk}{nn}"


def introspect(conn):
    tables_raw = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE ? ORDER BY name",
        (_TABLE_FILTER,),
    ).fetchall()

    views_raw = conn.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='view' AND name LIKE ? ORDER BY name",
        (_TABLE_FILTER,),
    ).fetchall()

    tables = []
    for (tname,) in tables_raw:
        cols = conn.execute(f"PRAGMA table_info({tname})").fetchall()
        fks = conn.execute(f"PRAGMA foreign_key_list({tname})").fetchall()
        row_count = conn.execute(f"SELECT COUNT(*) FROM {tname}").fetchone()[0]
        tables.append({
            "name": tname,
            "row_count": row_count,
            "columns": [
                {"name": c["name"], "type": c["type"], "notnull": c["notnull"], "pk": c["pk"]}
                for c in cols
            ],
            "fks": [
                {"table": fk["table"], "from": fk["from"], "to": fk["to"]}
                for fk in fks
            ],
        })

    views = [{"name": v["name"], "sql": v["sql"]} for v in views_raw]

    return tables, views


def _mermaid_block(tables):
    lines = ["erDiagram"]
    for t in tables:
        safe = _safe_name(t["name"])
        lines.append(f"    {safe} {{")
        for c in t["columns"]:
            lines.append(f"        {c['name']} {_fmt_type(c)}")
        lines.append("    }")

    for t in tables:
        for fk in t["fks"]:
            lines.append(
                f"    {_safe_name(t['name'])} ||--o{{ {_safe_name(fk['table'])} : \"{fk['from']}\""
            )
    return "\n".join(lines) + "\n"


def _summary_block(tables, views):
    lines = ["# Schema Summary", ""]
    for t in tables:
        lines.append(f"## {t['name']}")
        lines.append("")
        lines.append(f"Row count: {t['row_count']}")
        lines.append("")
        lines.append("Columns:")
        for c in t["columns"]:
            flags = []
            if c["pk"]:
                flags.append("PK")
            if c["notnull"]:
                flags.append("NOT NULL")
            flag_str = f" ({', '.join(flags)})" if flags else ""
            lines.append(f"- {c['name']}: {c['type'] or 'N/A'}{flag_str}")
        if t["fks"]:
            lines.append("")
            lines.append("Foreign Keys:")
            for fk in t["fks"]:
                lines.append(f"- {fk['from']} -> {fk['table']}.{fk['to']}")
        lines.append("")

    if views:
        lines.append("## Views")
        lines.append("")
        for v in views:
            lines.append(f"### {v['name']}")
            lines.append("")
            sql = v["sql"] or "-- no sql stored in sqlite_master"
            lines.append(f"```sql\n{sql}\n```")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Introspect knowledge.db and emit ER diagram + schema summary"
    )
    parser.add_argument(
        "--db-path",
        default=os.path.join(".samgraha", "knowledge.db"),
        help="Path to knowledge.db (default: .samgraha/knowledge.db relative to cwd)",
    )
    parser.add_argument(
        "--out-dir",
        default=os.path.join(".samgraha", "output", "step4-final-render", "schema"),
        help="Output directory (default: .samgraha/output/step4-final-render/schema relative to cwd)",
    )
    args = parser.parse_args()

    db_path = os.path.abspath(args.db_path)
    out_dir = os.path.abspath(args.out_dir)

    if not os.path.isfile(db_path):
        print(f"Error: DB not found at {db_path}")
        sys.exit(1)

    conn = get_conn(db_path)
    tables, views = introspect(conn)
    conn.close()

    mermaid = _mermaid_block(tables)
    summary = _summary_block(tables, views)

    os.makedirs(out_dir, exist_ok=True)

    er_path = os.path.join(out_dir, "er-diagram.md")
    with open(er_path, "w", encoding="utf-8") as f:
        f.write("```mermaid\n")
        f.write(mermaid)
        f.write("```\n")
    print(f"Written: {er_path}")

    summary_path = os.path.join(out_dir, "schema-summary.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"Written: {summary_path}")


if __name__ == "__main__":
    main()
