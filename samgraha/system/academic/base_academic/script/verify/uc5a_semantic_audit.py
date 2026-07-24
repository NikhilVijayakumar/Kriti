"""Verify script for semantic-audit — checks usecase completion criteria."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_args
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "common"))
import academic_schema


def main():
    args = parse_args(description="Verify semantic-audit completion")
    conn = academic_schema.get_conn(args.db_path)
    try:
        complete, detail = academic_schema.usecase_status(
            conn, args.paper_id, "semantic-audit")
        status = "PASS" if complete else "FAIL"
        print(f"semantic-audit: {status}")
        for d in detail:
            print(f"  - {d}")
        sys.exit(0 if complete else 1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
