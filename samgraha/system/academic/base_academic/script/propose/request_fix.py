"""request_fix.py — CLI entry point for ad-hoc 'fix X' user requests.

Not part of run_full_workflow.py's linear sequence; invoked directly
(e.g. by a human operator or an interactive agent) whenever a user
asks to fix something.

Usage:
  request_fix.py --mcp-bin <path> --repo-root <path> --user-comment "..." [--domain <key>]

Resolves the paper_id and target domain, then stages the propose-fix
chain via MCP. The interactive agent completes the semantic step and
persists the result (§7e/§8).
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from _adapter import write_envelope  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "common"))
import academic_schema  # noqa: E402


def _parse():
    p = argparse.ArgumentParser(
        description="Stage a fix proposal from a user comment")
    p.add_argument("--mcp-bin", required=True,
                   help="Path to the samgraha MCP binary")
    p.add_argument("--repo-root", required=True,
                   help="Repository root path")
    p.add_argument("--user-comment", required=True,
                   help="User's free-text fix request")
    p.add_argument("--domain", default=None,
                   help="Target domain key (optional)")
    p.add_argument("--out", default=None,
                   help="Output envelope path (optional)")
    return p.parse_args()


def _resolve_current_paper(conn, repo_root):
    """Resolve paper_id from repo_root for the current standard."""
    return academic_schema.resolve_paper_id(conn, repo_root)


def _resolve_domain(conn, domain_arg):
    """Exact match against academic_domains.key. No fuzzy fallback —
    a wrong guess means the wrong section gets a fix proposal."""
    if domain_arg:
        row = conn.execute("SELECT id FROM academic_domains WHERE key=?",
                           (domain_arg,)).fetchone()
        if row:
            return row["id"]
        available = [r["key"] for r in conn.execute(
            "SELECT key FROM academic_domains ORDER BY sort_order")]
        raise ValueError(
            f"unknown domain '{domain_arg}', available: {available}")
    return None  # whole-paper-scoped fix proposal


def main():
    args = _parse()
    conn = academic_schema.get_conn(academic_schema.db_path(args.repo_root))
    try:
        paper_id = _resolve_current_paper(conn, args.repo_root)
        if not paper_id:
            print("ERROR: no paper registered for this repo", file=sys.stderr)
            sys.exit(1)
        try:
            domain_id = _resolve_domain(conn, args.domain)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
    finally:
        conn.close()

    # Build the input payload for the propose-fix chain's first step
    gather_input = {
        "paper_id": paper_id,
        "phase": "fix",
        "scope_domain_id": domain_id,
        "user_comment": args.user_comment,
    }

    if args.out:
        # Write envelope for samgraha step contract
        write_envelope(Path(args.out), status="ok",
                       message="fix proposal context resolved",
                       gather_input=gather_input)
    else:
        # CLI mode — print the resolved context
        print(json.dumps(gather_input, indent=2))
        print("\nTo complete the propose-fix chain, run the MCP steps:")
        print("  1. run_script_step (gather-proposal-context)")
        print("  2. prepare_semantic_step (fix-proposal prompt)")
        print("  3. complete_semantic_step (agent reasoning)")
        print("  4. run_script_step (persist-proposal)")
        print("  5. run_script_step (render-proposal)")


if __name__ == "__main__":
    main()
