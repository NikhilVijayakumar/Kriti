"""Verify script for propose-fix — domain-scoped, unlike the other three
propose-* verify scripts. propose-fix has no academic_schema.py registry
entry (docs/proposal/base_academic-proposal-gate-workflow-proposal.md
§5): a fix proposal's scope_domain_id varies per invocation, so this
checks academic_proposals directly instead of going through
usecase_status() with a single whole-paper name.

Usage: uc_propose_fix.py --repo-root <path> --paper-id <id> [--domain <key>]
(omit --domain for a whole-paper-scoped fix proposal)
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "common"))
import academic_schema  # noqa: E402


def parse_args():
    p = argparse.ArgumentParser(description="Verify propose-fix completion")
    p.add_argument("--repo-root", required=True)
    p.add_argument("--paper-id", required=True, type=int)
    p.add_argument("--domain", default=None,
                   help="Domain key (omit for whole-paper-scoped fix)")
    args = p.parse_args()
    args.db_path = str(Path(args.repo_root) / ".samgraha" / "knowledge.db")
    return args


def main():
    args = parse_args()
    conn = academic_schema.get_conn(args.db_path)
    try:
        domain_id = None
        if args.domain:
            domain_id = academic_schema.get_domain_id(conn, args.domain)
            if domain_id is None:
                print("propose-fix: FAIL")
                print(f"  - unknown domain '{args.domain}'")
                sys.exit(1)
        row = conn.execute(
            "SELECT commit_sha FROM academic_proposals "
            "WHERE paper_id=? AND phase='fix' AND scope_domain_id IS ? "
            "AND status='approved' AND is_latest=1",
            (args.paper_id, domain_id)).fetchone()
        complete = row is not None
        status = "PASS" if complete else "FAIL"
        scope_label = args.domain or "(whole-paper)"
        print(f"propose-fix[{scope_label}]: {status}")
        if complete:
            print(f"  - fix proposal approved at {row['commit_sha'][:8] or '(no commit)'}")
        else:
            print(f"  - no approved fix proposal for {scope_label}")
        sys.exit(0 if complete else 1)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
