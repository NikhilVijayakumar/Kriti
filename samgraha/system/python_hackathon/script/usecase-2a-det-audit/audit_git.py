import subprocess
import json
import argparse
import os
import sys
import re

# Conventional Commit pattern: type(scope): description
CONVENTIONAL_COMMIT_RE = re.compile(
    r"^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+?\))?: .+$"
)

GITFLOW_BRANCH_RE = re.compile(
    r"^(main|master|develop|release/.+|hotfix/.+|feature/.+)$"
)

SHORTSTAT_RE = re.compile(
    r"(\d+) files? changed(?:, (\d+) insertions?\(\+\))?(?:, (\d+) deletions?\(-\))?"
)


def _analyze_commit_sizes(repo_path, limit=200):
    """Classify recent commits by lines-changed size (small/medium/large)."""
    raw = subprocess.check_output(
        ["git", "-C", repo_path, "log", "-n", str(limit),
         "--pretty=format:__COMMIT__", "--shortstat"],
        text=True
    )
    sizes = []
    for line in raw.splitlines():
        m = SHORTSTAT_RE.search(line)
        if m:
            insertions = int(m.group(2) or 0)
            deletions = int(m.group(3) or 0)
            sizes.append(insertions + deletions)

    n = len(sizes)
    buckets = {"small": 0, "medium": 0, "large": 0}
    for changed in sizes:
        if changed <= 30:
            buckets["small"] += 1
        elif changed <= 150:
            buckets["medium"] += 1
        else:
            buckets["large"] += 1

    large_rate = round(buckets["large"] / n * 100, 1) if n else 0.0
    return {
        "commits_analyzed": n,
        "avg_lines_changed": round(sum(sizes) / n, 1) if n else 0.0,
        "small_commits": buckets["small"],
        "medium_commits": buckets["medium"],
        "large_commits": buckets["large"],
        "large_commit_rate_pct": large_rate,
        "healthy_commit_size": n > 0 and large_rate <= 40.0,
    }


def _analyze_contributor_balance(shortlog_out):
    """Detect one author dominating the commit history (bulk solo work)."""
    counts = []
    for line in shortlog_out:
        parts = line.strip().split("\t", 1)
        if parts and parts[0].strip().isdigit():
            counts.append(int(parts[0].strip()))
    total = sum(counts)
    top_share = round(counts[0] / total * 100, 1) if counts and total else 0.0
    return {
        "commit_counts_by_author": counts,
        "top_contributor_share_pct": top_share,
        "balanced_contribution": len(counts) > 1 and top_share <= 80.0,
    }


def run_git_audit(repo_path):
    """
    Analyzes the git history for the Team Workflow domain.
    Extracts total commits, unique authors, commit message quality, and branch structure.
    """
    # Note: deliberately NOT using repo.resolve_code_root() here. That helper
    # descends into a repo's single code subfolder (e.g. goal-gpt/GoalGPT/)
    # for source-level audits, but git history lives at the repo root above
    # that subfolder — descending would make `git -C` fail to find `.git`.
    try:
        subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "--is-inside-work-tree"],
            check=True, capture_output=True, text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
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
            },
            "commit_size_analysis": _analyze_commit_sizes(repo_path),
            "contributor_balance": _analyze_contributor_balance(shortlog_out),
        }

    except subprocess.CalledProcessError as e:
        return {"error": str(e), "total_commits": 0, "unique_authors": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="Path to the git repository")
    args = parser.parse_args()

    result = run_git_audit(args.repo)
    print(json.dumps(result, indent=2))
