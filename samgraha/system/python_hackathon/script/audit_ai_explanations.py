import json
import argparse
import os
import re
import glob as globmod


LLM_DEPENDENCIES = (
    "openai", "anthropic", "google-generativeai", "google-genai",
    "cohere", "huggingface", "transformers", "langchain",
    "llama-index", "ollama", "together", "mistralai",
)

PROMPT_FILE_PATTERNS = (
    "*prompt*", "*instruction*", "*system_prompt*", "*system_instruction*",
    "*persona*", "*template_prompt*",
)


def run_ai_explanations_audit(repo_path):
    """
    Checks for AI/LLM integration: dependencies, prompt files, and configuration.
    """
    result = {
        "llm_dependencies_found": [],
        "llm_dependency_count": 0,
        "prompt_files_found": [],
        "prompt_file_count": 0,
        "ai_config_detected": False,
        "api_key_env_refs": [],
    }

    # 1. Scan dependency files for LLM-related packages
    dep_files = []
    for name in ("requirements.txt", "requirements-dev.txt", "pyproject.toml",
                  "setup.py", "setup.cfg", "Pipfile", "poetry.lock"):
        dep_files.extend(globmod.glob(os.path.join(repo_path, name)))

    # Also check nested requirements files
    dep_files.extend(globmod.glob(os.path.join(repo_path, "**", "requirements*.txt"), recursive=True))

    all_deps_text = ""
    for dep_file in dep_files:
        try:
            with open(dep_file, "r", encoding="utf-8", errors="ignore") as f:
                all_deps_text += f.read().lower() + "\n"
        except OSError:
            continue

    for dep in LLM_DEPENDENCIES:
        if dep in all_deps_text:
            result["llm_dependencies_found"].append(dep)
    result["llm_dependency_count"] = len(result["llm_dependencies_found"])

    # 2. Glob for prompt/instruction files
    for pattern in PROMPT_FILE_PATTERNS:
        matches = globmod.glob(os.path.join(repo_path, pattern), recursive=True)
        for m in matches:
            if os.path.isfile(m):
                rel = os.path.relpath(m, repo_path)
                if rel not in result["prompt_files_found"]:
                    result["prompt_files_found"].append(rel)
    result["prompt_file_count"] = len(result["prompt_files_found"])

    # 3. Check for AI config patterns in Python files
    ai_config_patterns = [
        re.compile(r"(?i)openai\.api_key|anthropic\.api_key|GOOGLE_API_KEY"),
        re.compile(r"(?i)client\s*=\s*OpenAI\(|client\s*=\s*Anthropic\("),
        re.compile(r"(?i)genai\.configure|ChatGoogleGenerativeAI"),
    ]
    py_files = globmod.glob(os.path.join(repo_path, "*.py"))
    py_files.extend(globmod.glob(os.path.join(repo_path, "**", "*.py"), recursive=True))

    for py_file in py_files[:50]:  # cap to avoid slow walks
        try:
            with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except OSError:
            continue

        for pat in ai_config_patterns:
            if pat.search(content):
                result["ai_config_detected"] = True
                break

        # Check for env var references to API keys
        env_refs = re.findall(r"os\.environ\.get\([\"']([A-Z_]*API_KEY[A-Z_]*)", content)
        env_refs += re.findall(r"os\.environ\[[\"']([A-Z_]*API_KEY[A-Z_]*)", content)
        for ref in env_refs:
            if ref not in result["api_key_env_refs"]:
                result["api_key_env_refs"].append(ref)

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="Path to the repository")
    args = parser.parse_args()

    audit_results = run_ai_explanations_audit(args.repo)
    print(json.dumps(audit_results, indent=2))
