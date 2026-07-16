import subprocess
import json
import argparse
import os
import re

# Conventional Commit pattern: type(scope): description
CONVENTIONAL_COMMIT_RE = re.compile(
    r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+?\))?: .+$"
)

GITFLOW_BRANCH_RE = re.compile(
    r"^(main|master|develop|release/.+|hotfix/.+|feature/.+)$"
)

def run_git_audit(repo_path):
    """
    Analyzes the git history for the Team Workflow domain.
    Extracts total commits, unique authors, commit message quality, and branch structure.
    """
    if not os.path.exists(os.path.join(repo_path, ".git")):
        return {"error": "Not a git repository", "total_commits": 0, "unique_authors": 0}

    try:
        # Total commits
        commit_count = int(subprocess.check_output(
            ["git", "-C", repo_path, "rev-list", "--count", "HEAD"],
            text=True
        ).strip())

        # Unique authors via shortlog
        shortlog_out = subprocess.check_output(
            ["git", "-C", repo_path, "shortlog", "-s", "-n", "HEAD"],
            text=True
        ).strip().splitlines()
        author_count = len(shortlog_out)

        # Commit messages for quality analysis
        messages = subprocess.check_output(
            ["git", "-C", repo_path, "log", "--format=%s", "-n", "50"],
            text=True
        ).strip().splitlines()

        conventional_count = sum(
            1 for m in messages if CONVENTIONAL_COMMIT_RE.match(m.strip())
        )
        conventional_rate = round(conventional_count / max(len(messages), 1) * 100, 1)

        # Branches
        branches = subprocess.check_output(
            ["git", "-C", repo_path, "branch", "-a", "--format=%(refname:short)"],
            text=True
        ).strip().splitlines()
        gitflow_branches = [b for b in branches if GITFLOW_BRANCH_RE.match(b.strip())]

        # PR/merge commit evidence (looks for Merge pull request patterns)
        merge_msgs = [m for m in messages if "Merge pull request" in m or "pull request" in m.lower()]

        return {
            "total_commits": commit_count,
            "unique_authors": author_count,
            "meets_minimum_commits": commit_count >= 5,
            "meets_multiple_authors": author_count > 1,
            "commit_message_quality": {
                "total_analyzed": len(messages),
                "conventional_commits": conventional_count,
                "conventional_rate_pct": conventional_rate,
                "passes_threshold": conventional_rate >= 50,
            },
            "git_workflow": {
                "branches_found": branches,
                "gitflow_branches": gitflow_branches,
                "pull_request_evidence": len(merge_msgs) > 0,
                "pr_merge_count": len(merge_msgs),
            }
        }

    except subprocess.CalledProcessError as e:
        return {"error": str(e), "total_commits": 0, "unique_authors": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="Path to the git repository")
    args = parser.parse_args()

    result = run_git_audit(args.repo)
    print(json.dumps(result, indent=2))
