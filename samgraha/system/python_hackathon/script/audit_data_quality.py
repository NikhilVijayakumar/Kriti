import json
import argparse
import os
import re


DATAHUB_URL_PATTERNS = [
    re.compile(r"(?i)kaggle\.com"),
    re.compile(r"(?i)huggingface\.co"),
    re.compile(r"(?i)drive\.google\.com"),
    re.compile(r"(?i).dropbox\.com"),
    re.compile(r"(?i)zenodo\.org"),
    re.compile(r"(?i)figshare\.com"),
    re.compile(r"(?i)data\.gov"),
    re.compile(r"(?i)archive\.org"),
]

DATA_FILE_EXTENSIONS = (".csv", ".parquet", ".jsonl", ".json", ".tsv", ".h5", ".hdf5", ".npy", ".npz")


def run_data_quality_audit(repo_path):
    """
    Checks for data artifacts: data files, data directories, and data-hub URL references.
    """
    result = {
        "data_files_found": False,
        "data_file_count": 0,
        "data_file_extensions": {},
        "data_directory_present": False,
        "data_directory_names": [],
        "datahub_urls_in_readme": [],
        "datahub_url_count": 0,
    }

    # Check for data directories
    data_dir_names = ("data", "dataset", "datasets", "raw", "processed", "input")
    for name in data_dir_names:
        if os.path.isdir(os.path.join(repo_path, name)):
            result["data_directory_present"] = True
            result["data_directory_names"].append(name)

    # Walk the repo for data files (skip hidden dirs, venvs, __pycache__)
    data_files = []
    extensions = {}
    for root, dirs, files in os.walk(repo_path):
        # Skip hidden/venv directories
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("venv", ".venv", "__pycache__", "node_modules", ".git")]
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext in DATA_FILE_EXTENSIONS:
                data_files.append(os.path.join(root, fname))
                extensions[ext] = extensions.get(ext, 0) + 1

    if data_files:
        result["data_files_found"] = True
        result["data_file_count"] = len(data_files)
        result["data_file_extensions"] = extensions

    # Scan README for data-hub URLs
    for readme_name in ("README.md", "README.rst", "README.txt", "README"):
        readme_path = os.path.join(repo_path, readme_name)
        if not os.path.isfile(readme_path):
            continue
        try:
            with open(readme_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except OSError:
            continue

        for pat in DATAHUB_URL_PATTERNS:
            matches = pat.findall(content)
            if matches:
                result["datahub_url_count"] += len(matches)
                # Extract actual URLs
                url_pattern = re.compile(r"https?://[^\s\)\"]+")
                for url in url_pattern.findall(content):
                    if pat.search(url) and url not in result["datahub_urls_in_readme"]:
                        result["datahub_urls_in_readme"].append(url)
        break  # only check first README found

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="Path to the repository")
    args = parser.parse_args()

    audit_results = run_data_quality_audit(args.repo)
    print(json.dumps(audit_results, indent=2))
