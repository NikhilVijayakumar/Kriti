#!/usr/bin/env python3
"""
run_full_workflow.py — master orchestrator for python_hackathon's samgraha
standard. Drives every step through the REAL MCP protocol (spawns the built
`mcp` binary, speaks JSON-RPC over stdio) — never subprocess-calls the
wrap_*.py/persist_*.py scripts directly, so every execution (deterministic
or semantic) gets tracked exactly the way any MCP client driving samgraha
normally would: run_script_step/complete_semantic_step both record an
`execution` row, the same as if an agent called them one at a time.

What it does, in order:
  1. register_standard  — (re)registers standard.yaml's usecases/steps/
     scripts/prompts into knowledge.db.
  2. schema-init         — creates hackathon_* tables, seeds hackathon_domains
     (weights.yaml), hackathon_templates (every file under templates/
     reports/{markdown,html}/), hackathon_visualization_types (render_charts.py's
     known chart kinds).
  3. init + deterministic-audit — run to completion (all teams).
  4. semantic-audit / narrative-analysis — the pre-script (evidence/context
     gathering) runs automatically per (team, domain); the semantic step is
     only STAGED (prepare_semantic_step called, prompt fetched) — completing
     it needs an actual model reasoning over that prompt, which is exactly
     why samgraha splits prepare/complete_semantic_step. This script cannot
     and does not fabricate that judgment. Every staged-but-incomplete item
     is written to the report below so an agent driving MCP directly knows
     exactly which step_id to call next (prepare_semantic_step again if
     needed, then run_script_step on the matching persist step with the
     model's real result).
  5. calculate / render-markdown / render-html / export-pdf — run once each;
     harmless to rerun later once semantic steps are actually completed.

Writes a JSON report (ran/failed/pending_semantic) next to knowledge.db so
progress survives between runs — rerunning is idempotent for everything
except re-staging semantic steps it already staged.

Usage:
  python run_full_workflow.py \\
      --mcp-bin /home/dell/PycharmProjects/samgraha/target/release/mcp \\
      --repo-root /home/dell/PycharmProjects/Heimdall \\
      --standard-path /home/dell/PycharmProjects/Heimdall/.samgraha/scripts/schema
"""
import argparse
import json
import sqlite3
import subprocess
import sys
from pathlib import Path


class McpSession:
    def __init__(self, mcp_bin):
        self.proc = subprocess.Popen(
            [mcp_bin], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, bufsize=1,
        )
        self._id = 0

    def call(self, name, arguments, timeout_secs=None):
        self._id += 1
        args = dict(arguments)
        if timeout_secs is not None:
            args["timeout_secs"] = timeout_secs
        req = {"jsonrpc": "2.0", "id": self._id, "method": "tools/call",
               "params": {"name": name, "arguments": args}}
        self.proc.stdin.write(json.dumps(req) + "\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        resp = json.loads(line)
        result = resp.get("result", {})
        text = result.get("content", [{}])[0].get("text", "{}")
        payload = json.loads(text)
        if result.get("isError"):
            raise RuntimeError(f"{name} {args}: {payload}")
        return payload

    def close(self):
        self.proc.stdin.close()
        try:
            self.proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.proc.kill()


def load_steps(db_path, standard):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT step.id, usecase.name AS usecase, step.step_order, step.kind, step.description "
        "FROM step JOIN usecase ON step.usecase_id = usecase.id "
        "WHERE usecase.standard = ? ORDER BY usecase.id, step.step_order",
        (standard,),
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]


def domain_keys(db_path):
    con = sqlite3.connect(db_path)
    rows = con.execute("SELECT key FROM hackathon_domains ORDER BY sort_order").fetchall()
    con.close()
    return [r[0] for r in rows]


def team_names(db_path, standard):
    con = sqlite3.connect(db_path)
    rows = con.execute("SELECT team_name FROM hackathon_teams WHERE standard=?", (standard,)).fetchall()
    con.close()
    return [r[0] for r in rows]


def steps_of(steps, usecase):
    return [s for s in steps if s["usecase"] == usecase]


def stage_semantic_triad(session, repo_root, pre, sem, post, pre_input, report, label):
    try:
        ev = session.call("run_script_step", {"step_id": pre["id"], "repo_path": repo_root, "input": pre_input})
        if ev.get("status") != "ok":
            report["failed"].append({"label": label, "stage": "pre", "message": ev.get("message")})
            return
    except Exception as e:
        report["failed"].append({"label": label, "stage": "pre", "message": str(e)})
        return

    try:
        prompt = session.call("prepare_semantic_step", {"step_id": sem["id"], "repo_path": repo_root})
    except Exception as e:
        report["failed"].append({"label": label, "stage": "prepare_semantic", "message": str(e)})
        return

    report["pending_semantic"].append({
        "label": label,
        "pre_input": pre_input,
        "evidence_step_id": pre["id"],
        "semantic_step_id": sem["id"],
        "persist_step_id": post["id"],
        "prompt_name": prompt["prompt_name"],
    })


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mcp-bin", required=True)
    p.add_argument("--repo-root", required=True)
    p.add_argument("--standard-path", required=True)
    p.add_argument("--standard", default="python_hackathon")
    p.add_argument("--report-out", default=None)
    args = p.parse_args()

    repo_root = args.repo_root
    db_path = str(Path(repo_root) / ".samgraha" / "knowledge.db")
    report = {"ran": [], "failed": [], "pending_semantic": []}

    session = McpSession(args.mcp_bin)
    try:
        print("== register_standard ==")
        result = session.call("register_standard", {"path": args.standard_path, "repo_path": repo_root})
        print(json.dumps(result))
        report["ran"].append({"step": "register_standard", "result": result})

        steps = load_steps(db_path, args.standard)

        print("\n== schema-init ==")
        schema_init = steps_of(steps, "schema-init")[0]
        r = session.call("run_script_step", {"step_id": schema_init["id"], "repo_path": repo_root})
        report["ran"].append({"step": "schema-init", "status": r.get("status")})

        print("\n== init (sync teams + first deterministic pass) ==")
        init_step = steps_of(steps, "init")[0]
        r = session.call("run_script_step", {"step_id": init_step["id"], "repo_path": repo_root, "input": {}}, timeout_secs=600)
        report["ran"].append({"step": "init", "status": r.get("status")})

        print("\n== deterministic-audit (all teams) ==")
        det_step = steps_of(steps, "deterministic-audit")[0]
        r = session.call("run_script_step", {"step_id": det_step["id"], "repo_path": repo_root, "input": {}}, timeout_secs=900)
        report["ran"].append({"step": "deterministic-audit", "status": r.get("status")})

        teams = team_names(db_path, args.standard)
        domains = domain_keys(db_path)
        print(f"\nteams: {teams}")
        print(f"domains: {domains}")

        print(f"\n== semantic-audit: staging {len(teams)} teams x {len(domains)} domains ==")
        sem_steps = steps_of(steps, "semantic-audit")
        for team in teams:
            for i, domain in enumerate(domains):
                pre, sem, post = sem_steps[3 * i], sem_steps[3 * i + 1], sem_steps[3 * i + 2]
                stage_semantic_triad(
                    session, repo_root, pre, sem, post,
                    {"team_name": team, "domain": domain}, report,
                    label=f"semantic-audit/{team}/{domain}",
                )

        print("\n== narrative-analysis: staging competition-wide + per-team-per-domain ==")
        narr_steps = steps_of(steps, "narrative-analysis")
        leaderboard_pre, leaderboard_sem, leaderboard_post = narr_steps[0], narr_steps[1], narr_steps[2]
        stage_semantic_triad(
            session, repo_root, leaderboard_pre, leaderboard_sem, leaderboard_post,
            {"team_name": None, "domain": None}, report,
            label="narrative-analysis/(competition-wide)",
        )
        for i, domain in enumerate(domains):
            pre, sem, post = narr_steps[3 * (i + 1)], narr_steps[3 * (i + 1) + 1], narr_steps[3 * (i + 1) + 2]
            for team in teams:
                stage_semantic_triad(
                    session, repo_root, pre, sem, post,
                    {"team_name": team, "domain": domain}, report,
                    label=f"narrative-analysis/{team}/{domain}",
                )

        print("\n== calculate / render-markdown / render-html / export-pdf ==")
        for usecase in ("calculate", "render-markdown", "render-html", "export-pdf"):
            step = steps_of(steps, usecase)[0]
            try:
                r = session.call("run_script_step", {"step_id": step["id"], "repo_path": repo_root, "input": {}}, timeout_secs=300)
                report["ran"].append({"step": usecase, "status": r.get("status"), "message": r.get("message", "")[:500]})
            except Exception as e:
                report["failed"].append({"label": usecase, "stage": "run", "message": str(e)})
    finally:
        session.close()

    report_path = args.report_out or str(Path(repo_root) / ".samgraha" / "workflow-report.json")
    Path(report_path).write_text(json.dumps(report, indent=2))

    print(f"\n== summary ==")
    print(f"ran: {len(report['ran'])}, failed: {len(report['failed'])}, pending semantic: {len(report['pending_semantic'])}")
    print(f"full report: {report_path}")
    if report["pending_semantic"]:
        print(f"\n{len(report['pending_semantic'])} semantic steps staged but NOT completed — need an agent to:")
        print("  1. prepare_semantic_step(semantic_step_id) to re-fetch the prompt")
        print("  2. reason over it, then complete_semantic_step(semantic_step_id)")
        print("  3. run_script_step(persist_step_id, input={..., result/sections: <the model's answer>})")
        print(f"  (see {report_path} for every {{team, domain}} -> step_id mapping)")

    sys.exit(1 if report["failed"] else 0)


if __name__ == "__main__":
    main()
