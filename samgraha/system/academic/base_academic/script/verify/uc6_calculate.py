"""Verify script for calculate — checks usecase completion criteria."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_args
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "common"))
import academic_schema


def main():
    args = parse_args(description="Verify calculate completion")
    conn = academic_schema.get_conn(args.db_path)
    try:
        complete, detail = academic_schema.usecase_status(
            conn, args.paper_id, "calculate")
        status = "PASS" if complete else "FAIL"
        print(f"calculate: {status}")
        for d in detail:
            print(f"  - {d}")
        sys.exit(0 if complete else 1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
