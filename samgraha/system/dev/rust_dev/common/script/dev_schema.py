"""
dev_schema.py -- rust_dev's own dev_* tables in knowledge.db, catalogued
via standard.metadata.json's custom_tables[]. DDL source of truth:
common/schema/*.sql, read in filename order by ensure_schema.

Kept deliberately small -- proposal 6 §1 found rust_dev does NOT need a
pcems-academic_schema.py-style typed-access-plus-allow-lists module for
samgraha's own generic usecase/step/script/prompt/domain tables (those are
samgraha's, not rust_dev's). This module only exists for the tables that
genuinely are rust_dev's own (proposal 6 §5, §7): dev_repo_domain_state,
dev_proposal_phase_scope, and the 8 findings/score/report tables. No
allow-lists, no metadata-key validation -- rust_dev has no
metadata.yaml-shaped input pcems's academic_papers.metadata does.
"""
import os
import sqlite3

_SCHEMA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "schema")


def ensure_schema(conn):
    """Read and execute every *.sql file in common/schema/, in filename
    order. Non-.sql files (the tierN check schema/manifest JSON+YAML pairs
    that also live in this directory, proposal 1 §3) are skipped -- same
    extension filter pcems_2026's own academic_schema.py uses, which
    already tolerates a mixed-purpose directory."""
    schema_dir = os.path.normpath(_SCHEMA_DIR)
    if not os.path.isdir(schema_dir):
        raise RuntimeError(f"schema directory not found: {schema_dir}")
    sql_files = sorted(f for f in os.listdir(schema_dir) if f.endswith(".sql"))
    for fname in sql_files:
        fpath = os.path.join(schema_dir, fname)
        with open(fpath, "r", encoding="utf-8") as fh:
            sql = fh.read()
        conn.executescript(sql)
    conn.commit()


def get_conn(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    ensure_schema(conn)
    return conn
