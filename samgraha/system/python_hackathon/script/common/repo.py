"""
repo.py — Helper to resolve the actual code root inside a cloned repo.

Some repos (e.g. Goal GPT) have all code inside a single subfolder:
  .heimdall/.hackathon/goal-gpt/GoalGPT/

Others have code at the root:
  .heimdall/.hackathon/bol/

This module detects the correct code root for audit scripts.
"""
import os


def resolve_code_root(repo_path):
    """
    Given a cloned repo path, return the path where the actual code lives.

    Rules:
    - If repo has a single non-hidden subfolder and no code files at root,
      return that subfolder.
    - Otherwise, return repo_path itself.

    Examples:
      resolve_code_root(".heimdall/.hackathon/goal-gpt") -> ".../goal-gpt/GoalGPT"
      resolve_code_root(".heimdall/.hackathon/bol") -> ".../bol"
    """
    if not os.path.isdir(repo_path):
        return repo_path

    entries = os.listdir(repo_path)
    non_hidden = [e for e in entries if not e.startswith(".")]

    # Count non-hidden directories and files
    dirs = [e for e in non_hidden if os.path.isdir(os.path.join(repo_path, e))]
    files = [e for e in non_hidden if os.path.isfile(os.path.join(repo_path, e))]

    # If exactly one subfolder and no files at root, dive into it
    if len(dirs) == 1 and len(files) == 0:
        return os.path.join(repo_path, dirs[0])

    return repo_path
