"""_common.py — shared runner for every generated per-domain verify script.
One implementation, ~108 one-line callers (script/schema/
generate_per_domain_usecases.py) — avoids duplicating this logic in each
generated file. Not itself a usecase verify script.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_args  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "common"))
import academic_schema  # noqa: E402


def verify_main(usecase_name):
    args = parse_args(description=f"Verify {usecase_name} completion")
    conn = academic_schema.get_conn(args.db_path)
    try:
        complete, detail = academic_schema.usecase_status(conn, args.paper_id, usecase_name)
        status = "PASS" if complete else "FAIL"
        print(f"{usecase_name}: {status}")
        for d in detail:
            print(f"  - {d}")
        sys.exit(0 if complete else 1)
    finally:
        conn.close()
