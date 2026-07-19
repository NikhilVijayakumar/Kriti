"""mock-api-runs — Category A check for domain 11-prototype.

Probes for mock server config, starts it, and checks if it responds.
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import check_result, write_check_result


MOCK_CONFIGS = [
    "mock-server.js", "mock-server.ts", "mock-server.py",
    "mockapi.config.js", "mockapi.config.ts",
    "mock_routes.json", "mock.json",
    "msw/handlers.js", "msw/handlers.ts",
    "mock/handlers.js", "mock/handlers.ts",
]

MOCK_PORT = 3099


def run_check(repo_root: Path, fingerprint: str) -> dict:
    if not repo_root.is_dir():
        return check_result(
            check="mock-api-runs", domain="11-prototype", category="A",
            status="error",
            metrics={"server_started": False, "responds": False},
            evidence=[f"Cannot access repo-root: {repo_root}"],
            repo_fingerprint=fingerprint,
        )

    # Probe for mock server config
    config_found = None
    for config in MOCK_CONFIGS:
        if (repo_root / config).exists():
            config_found = config
            break

    if not config_found:
        return check_result(
            check="mock-api-runs", domain="11-prototype", category="A",
            status="not_applicable",
            metrics={"server_started": False, "responds": False},
            evidence=["No mock server configuration found"],
            repo_fingerprint=fingerprint,
        )

    # Try to start mock server
    process = None
    try:
        if config_found.endswith(".py"):
            cmd = [sys.executable, str(repo_root / config_found)]
        else:
            cmd = ["node", str(repo_root / config_found)]

        process = subprocess.Popen(
            cmd, cwd=str(repo_root),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )

        # Wait for server to start
        time.sleep(3)

        # Check if process is still running
        if process.poll() is not None:
            return check_result(
                check="mock-api-runs", domain="11-prototype", category="A",
                status="fail",
                metrics={"server_started": False, "responds": False},
                evidence=[f"Mock server exited immediately (code: {process.returncode})"],
                repo_fingerprint=fingerprint,
            )

        # Try to connect
        import urllib.request
        try:
            req = urllib.request.Request(f"http://localhost:{MOCK_PORT}/")
            with urllib.request.urlopen(req, timeout=5) as resp:
                status_code = resp.status
                return check_result(
                    check="mock-api-runs", domain="11-prototype", category="A",
                    status="pass",
                    metrics={"server_started": True, "responds": True},
                    evidence=[f"Mock server responded with status {status_code}"],
                    repo_fingerprint=fingerprint,
                )
        except Exception:
            return check_result(
                check="mock-api-runs", domain="11-prototype", category="A",
                status="fail",
                metrics={"server_started": True, "responds": False},
                evidence=["Mock server started but not reachable on port " + str(MOCK_PORT)],
                repo_fingerprint=fingerprint,
            )

    except FileNotFoundError:
        return check_result(
            check="mock-api-runs", domain="11-prototype", category="A",
            status="error",
            metrics={"server_started": False, "responds": False},
            evidence=["Could not start mock server — runtime not available"],
            repo_fingerprint=fingerprint,
        )
    except Exception as e:
        return check_result(
            check="mock-api-runs", domain="11-prototype", category="A",
            status="error",
            metrics={"server_started": False, "responds": False},
            evidence=[f"Error starting mock server: {e}"],
            repo_fingerprint=fingerprint,
        )
    finally:
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--repo-fingerprint", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    result = run_check(Path(args.repo_root), args.repo_fingerprint)
    write_check_result(Path(args.out), result)


if __name__ == "__main__":
    main()
