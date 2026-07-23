#!/usr/bin/env python3
"""
run_full_workflow.py — master orchestrator for base_academic's samgraha
standard. Drives every step through the REAL MCP protocol (spawns the built
`mcp` binary, speaks JSON-RPC over stdio).

Execution order:
  1. register_standard — (re)registers standard.yaml
  2. expand_triads — inserts domain-expanded steps into knowledge.db
  3. schema-init — creates academic_* tables, seeds domains/templates
  4. classify-repo — determines repo state (4-state: NO_DOCS_NO_IMPL,
     DOCS_ONLY, IMPL_NO_ANALYSIS, IMPL_WITH_ANALYSIS)
  5. [if IMPL_NO_ANALYSIS] generate-analysis-docs
  6. draft-from-docs-only OR generate-paper-draft (per classification)
  7. deepen-sections — literature review / mathematics / figures
  8. semantic-audit — score against rubric
  9. plagiarism-forensic-audit → humanize (loop until PASS or max_iterations)
  10. calculate / render — scoring + report assembly
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


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

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
    rows = con.execute("SELECT key FROM academic_domains ORDER BY sort_order").fetchall()
    con.close()
    return [r[0] for r in rows]


def get_repo_classification(db_path, standard, repo_root):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    row = con.execute(
        "SELECT classification FROM academic_repos WHERE standard=? AND repo_root=?",
        (standard, repo_root),
    ).fetchone()
    con.close()
    return row["classification"] if row else None


def modules_for_paper(db_path, paper_id):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        "SELECT module_name FROM academic_modules WHERE paper_id=? ORDER BY sort_order",
        (paper_id,),
    ).fetchall()
    con.close()
    return [r["module_name"] for r in rows]


def get_paper_id(db_path, standard, repo_root):
    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    row = con.execute(
        "SELECT id FROM academic_papers WHERE standard=? AND repo_root=?",
        (standard, repo_root),
    ).fetchone()
    con.close()
    return row["id"] if row else None


def steps_of(steps, usecase):
    return [s for s in steps if s["usecase"] == usecase]


# ---------------------------------------------------------------------------
# Dynamic triad expansion — inserts steps into knowledge.db for usecases
# that have steps: [] in standard.yaml. This is the fix for the "expanded
# at runtime" pattern: the orchestrator knows the domain list after
# classify-repo runs, so it inserts the concrete steps before trying to
# dispatch them.
# ---------------------------------------------------------------------------

def _lookup_script_id(con, name):
    row = con.execute("SELECT id FROM script WHERE name=?", (name,)).fetchone()
    return row["id"] if row else None


def _lookup_prompt_id(con, name):
    row = con.execute("SELECT id FROM prompt WHERE name=?", (name,)).fetchone()
    return row["id"] if row else None


def _lookup_usecase_id(con, standard, name):
    row = con.execute(
        "SELECT id FROM usecase WHERE standard=? AND name=?", (standard, name)
    ).fetchone()
    return row["id"] if row else None


def _insert_step(con, usecase_id, order, kind, description, script_id=None, prompt_id=None):
    existing = con.execute(
        "SELECT id FROM step WHERE usecase_id=? AND step_order=?",
        (usecase_id, order),
    ).fetchone()
    if existing:
        return existing["id"]
    cur = con.execute(
        "INSERT INTO step (usecase_id, step_order, kind, description) VALUES (?, ?, ?, ?)",
        (usecase_id, order, kind, description),
    )
    step_id = cur.lastrowid
    if script_id is not None:
        con.execute(
            "INSERT INTO step_script (step_id, script_id) VALUES (?, ?)",
            (step_id, script_id),
        )
    if prompt_id is not None:
        con.execute(
            "INSERT INTO step_prompt (step_id, prompt_id) VALUES (?, ?)",
            (step_id, prompt_id),
        )
    con.commit()
    return step_id


def _truncate_usecase_steps(con, usecase_id, max_order):
    """Delete steps with step_order > max_order for a usecase.
    Called before expand_triads inserts to handle shrinking domain/module sets."""
    con.execute(
        "DELETE FROM step WHERE usecase_id=? AND step_order>?",
        (usecase_id, max_order),
    )
    con.commit()


def expand_triads(db_path, standard, domains, module_names=None, enrichment_kinds=None):
    """Insert expanded triad steps into knowledge.db for usecases that have
    steps: [] in standard.yaml. Called after register_standard + schema-init
    so that script/prompt/usecase rows already exist.

    Truncates stale steps (orphan cleanup) before inserting, so shrinking
    domain/module sets don't leave orphaned rows.

    Returns the number of steps inserted.
    """
    if enrichment_kinds is None:
        enrichment_kinds = ["literature-review", "mathematics", "figures"]
    if module_names is None:
        module_names = []

    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    count = 0

    # --- draft-from-docs-only: 3 steps per domain ---
    uc_id = _lookup_usecase_id(con, standard, "draft-from-docs-only")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 3 * len(domains))
        pre_script = _lookup_script_id(con, "gather-domain-evidence")
        sem_prompt = _lookup_prompt_id(con, "generate-section-docs-only")
        post_script = _lookup_script_id(con, "persist-section-draft")
        order = 1
        for domain in domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather docs for {domain}", script_id=pre_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"Draft {domain} from docs only", prompt_id=sem_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist {domain} draft", script_id=post_script)
            count += 3
            order += 3

    # --- generate-paper-draft: 3 steps per domain ---
    uc_id = _lookup_usecase_id(con, standard, "generate-paper-draft")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 3 * len(domains))
        pre_script = _lookup_script_id(con, "gather-domain-evidence")
        sem_prompt = _lookup_prompt_id(con, "generate-section")
        post_script = _lookup_script_id(con, "persist-section-draft")
        order = 1
        for domain in domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather analysis docs for {domain}", script_id=pre_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"Generate {domain} from analysis docs", prompt_id=sem_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist {domain} draft", script_id=post_script)
            count += 3
            order += 3

    # --- deepen-sections: 3 steps per (domain, enrichment_kind) ---
    uc_id = _lookup_usecase_id(con, standard, "deepen-sections")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 3 * len(domains) * len(enrichment_kinds))
        pre_script = _lookup_script_id(con, "gather-enrichment-context")
        post_script = _lookup_script_id(con, "persist-section-draft")
        prompt_map = {
            "literature-review": _lookup_prompt_id(con, "literature-review-pass"),
            "mathematics": _lookup_prompt_id(con, "mathematics-pass"),
            "figures": _lookup_prompt_id(con, "figures-pass"),
        }
        order = 1
        for domain in domains:
            for kind in enrichment_kinds:
                sem_prompt = prompt_map.get(kind)
                _insert_step(con, uc_id, order, "deterministic",
                             f"Pre: gather enrichment context for {domain}/{kind}",
                             script_id=pre_script)
                _insert_step(con, uc_id, order + 1, "semantic",
                             f"{kind} pass over {domain}",
                             prompt_id=sem_prompt)
                _insert_step(con, uc_id, order + 2, "deterministic",
                             f"Post: persist enriched {domain}/{kind}",
                             script_id=post_script)
                count += 3
                order += 3

    # --- semantic-audit: 3 steps per domain ---
    uc_id = _lookup_usecase_id(con, standard, "semantic-audit")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 3 * len(domains))
        pre_script = _lookup_script_id(con, "gather-domain-evidence")
        sem_prompt = _lookup_prompt_id(con, "semantic-audit")
        post_script = _lookup_script_id(con, "persist-domain-semantic-score")
        order = 1
        for domain in domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather draft + rubric for {domain}",
                         script_id=pre_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"Score {domain} against rubric",
                         prompt_id=sem_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist {domain} score",
                         script_id=post_script)
            count += 3
            order += 3

    # --- 5a-plagiarism-forensic-audit: 3 steps per domain ---
    # Pass 1: forensic audit (flag spans). Pass 2: targeted rewrite (fix flagged spans).
    # Both run within the same usecase; the fix_loop decides if 5b is needed.
    uc_id = _lookup_usecase_id(con, standard, "plagiarism-forensic-audit")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 3 * len(domains))
        pre_script = _lookup_script_id(con, "gather-plagiarism-context")
        forensic_prompt = _lookup_prompt_id(con, "plagiarism-fingerprint-audit")
        targeted_prompt = _lookup_prompt_id(con, "targeted-rewrite")
        post_script = _lookup_script_id(con, "persist-plagiarism-findings")
        order = 1
        for domain in domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather draft for plagiarism check {domain}",
                         script_id=pre_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"Forensic audit {domain}",
                         prompt_id=forensic_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist forensic findings for {domain}",
                         script_id=post_script)
            count += 3
            order += 3

    # --- 5b-humanize: 3 steps per domain ---
    # Pass 3: full 3-layer humanize rewrite (triggered only if targeted rewrite
    # didn't bring section under risk threshold).
    uc_id = _lookup_usecase_id(con, standard, "humanize")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 3 * len(domains))
        pre_script = _lookup_script_id(con, "gather-humanize-context")
        sem_prompt = _lookup_prompt_id(con, "humanize-section")
        post_script = _lookup_script_id(con, "persist-humanize-pass")
        order = 1
        for domain in domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather humanize context for {domain}",
                         script_id=pre_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"3-layer humanize rewrite {domain}",
                         prompt_id=sem_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist humanized {domain}",
                         script_id=post_script)
            count += 3
            order += 3

    # --- generate-analysis-docs: discover-modules (step 1) + per-module triads ---
    uc_id = _lookup_usecase_id(con, standard, "generate-analysis-docs")
    if uc_id and module_names:
        module_kinds = ["summary", "architecture", "mathematics", "novelty", "gaps"]
        cross_kinds = ["architecture", "dependencies", "interactions", "patterns",
                        "gaps", "mathematics", "novelty"]
        # 1 discover-modules step + (modules * module_kinds * 3) + (cross_kinds * 3)
        expected_steps = 1 + len(module_names) * len(module_kinds) * 3 + len(cross_kinds) * 3
        _truncate_usecase_steps(con, uc_id, expected_steps)
        discover_script = _lookup_script_id(con, "discover-modules")
        gather_mod_script = _lookup_script_id(con, "gather-module-evidence")
        persist_mod_script = _lookup_script_id(con, "persist-module-analysis")
        gather_xmod_script = _lookup_script_id(con, "gather-cross-module-evidence")
        persist_xmod_script = _lookup_script_id(con, "persist-cross-module-analysis")

        module_kinds = ["summary", "architecture", "mathematics", "novelty", "gaps"]
        cross_kinds = ["architecture", "dependencies", "interactions", "patterns",
                        "gaps", "mathematics", "novelty"]

        order = 1
        # Step 1: discover-modules
        _insert_step(con, uc_id, order, "deterministic",
                     "Discover module boundaries", script_id=discover_script)
        order += 1

        # Per-module x per-kind triads
        for mod_name in module_names:
            for kind in module_kinds:
                prompt_name = f"module-analysis-{kind}"
                sem_prompt = _lookup_prompt_id(con, prompt_name)
                _insert_step(con, uc_id, order, "deterministic",
                             f"Pre: gather evidence for {mod_name}",
                             script_id=gather_mod_script)
                _insert_step(con, uc_id, order + 1, "semantic",
                             f"Write {kind} analysis for {mod_name}",
                             prompt_id=sem_prompt)
                _insert_step(con, uc_id, order + 2, "deterministic",
                             f"Post: persist {kind} for {mod_name}",
                             script_id=persist_mod_script)
                count += 3
                order += 3

        # Cross-module x per-kind triads
        for kind in cross_kinds:
            prompt_name = f"cross-module-analysis-{kind}"
            sem_prompt = _lookup_prompt_id(con, prompt_name)
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather cross-module evidence for {kind}",
                         script_id=gather_xmod_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"Write cross-module {kind}",
                         prompt_id=sem_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist cross-module {kind}",
                         script_id=persist_xmod_script)
            count += 3
            order += 3

    con.close()
    return count


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

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
        "prompt_name": prompt.get("prompt_name", ""),
    })


def run_triads_for_usecase(session, repo_root, steps, usecase, domains,
                           input_fn, report, label_prefix):
    """Run pre/semantic/post triads for a usecase, one per domain."""
    uc_steps = steps_of(steps, usecase)
    if not uc_steps:
        print(f"  WARNING: no steps for {usecase} — skipping")
        return
    triads = len(uc_steps) // 3
    for i, domain in enumerate(domains):
        if i >= triads:
            break
        pre, sem, post = uc_steps[3 * i], uc_steps[3 * i + 1], uc_steps[3 * i + 2]
        pre_input = input_fn(domain)
        stage_semantic_triad(session, repo_root, pre, sem, post, pre_input, report,
                             label=f"{label_prefix}/{domain}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mcp-bin", required=True)
    p.add_argument("--repo-root", required=True)
    p.add_argument("--standard-path", required=True)
    p.add_argument("--standard", default="base_academic")
    p.add_argument("--report-out", default=None)
    p.add_argument("--domains", nargs="*", help="Override domain list (space-separated keys)")
    args = p.parse_args()

    repo_root = args.repo_root
    db_path = str(Path(repo_root) / ".samgraha" / "knowledge.db")
    report = {"ran": [], "failed": [], "pending_semantic": []}

    session = McpSession(args.mcp_bin)
    try:
        # --- Phase 1: Registration + Schema ---
        print("== register_standard ==")
        result = session.call("register_standard", {"path": args.standard_path, "repo_path": repo_root})
        print(json.dumps(result))
        report["ran"].append({"step": "register_standard", "result": result})

        print("\n== schema-init ==")
        steps = load_steps(db_path, args.standard)
        schema_init = steps_of(steps, "schema-init")[0]
        r = session.call("run_script_step", {"step_id": schema_init["id"], "repo_path": repo_root})
        report["ran"].append({"step": "schema-init", "status": r.get("status")})

        # --- Phase 2: Classify ---
        print("\n== classify-repo ==")
        classify_step = steps_of(steps, "classify-repo")[0]
        r = session.call("run_script_step", {"step_id": classify_step["id"], "repo_path": repo_root})
        report["ran"].append({"step": "classify-repo", "status": r.get("status")})

        classification = get_repo_classification(db_path, args.standard, repo_root)
        paper_id = get_paper_id(db_path, args.standard, repo_root)
        domains = args.domains or domain_keys(db_path)
        modules = modules_for_paper(db_path, paper_id) if paper_id else []
        print(f"  classification={classification}, domains={domains}, modules={modules}")

        # --- Phase 2.5: Expand triads into DB ---
        print(f"\n== expand_triads ({len(domains)} domains) ==")
        insert_count = expand_triads(db_path, args.standard, domains,
                                     module_names=modules)
        print(f"  inserted {insert_count} steps")

        # Reload steps after expansion
        steps = load_steps(db_path, args.standard)

        # --- Phase 3: Analysis docs (if needed) ---
        if classification == "IMPL_NO_ANALYSIS" and modules:
            print(f"\n== generate-analysis-docs ({len(modules)} modules) ==")
            analysis_steps = steps_of(steps, "generate-analysis-docs")
            if analysis_steps:
                r = session.call("run_script_step", {"step_id": analysis_steps[0]["id"], "repo_path": repo_root})
                report["ran"].append({"step": "discover-modules", "status": r.get("status")})

        # --- Phase 4: Generate draft ---
        if classification == "NO_DOCS_NO_IMPL":
            print("\n== REFUSED: no docs, no implementation — nothing to draft from ==")
            report["failed"].append({"label": "entry", "stage": "refuse",
                                     "message": "NO_DOCS_NO_IMPL: no documentation and no implementation to analyze"})
        else:
            if classification == "DOCS_ONLY":
                entry_usecase = "draft-from-docs-only"
                mode = "draft"
            else:
                entry_usecase = "generate-paper-draft"
                mode = "generate"
            print(f"\n== {entry_usecase} ({len(domains)} domains) ==")

            def draft_input(domain):
                return {"paper_id": paper_id, "domain": domain, "mode": mode}

            run_triads_for_usecase(session, repo_root, steps, entry_usecase, domains,
                                   draft_input, report, label_prefix=entry_usecase)

            # --- Phase 5: Deepen ---
            enrichment_kinds = ["literature-review", "mathematics", "figures"]
            print(f"\n== deepen-sections ({len(domains)} domains x {len(enrichment_kinds)} kinds) ==")

            deepen_steps = steps_of(steps, "deepen-sections")
            if deepen_steps:
                idx = 0
                for domain in domains:
                    for kind in enrichment_kinds:
                        if idx + 2 >= len(deepen_steps):
                            break
                        pre, sem, post = deepen_steps[idx], deepen_steps[idx + 1], deepen_steps[idx + 2]
                        stage_semantic_triad(session, repo_root, pre, sem, post,
                                             {"paper_id": paper_id, "domain": domain, "enrichment_kind": kind},
                                             report, label=f"deepen-sections/{domain}/{kind}")
                        idx += 3

            # --- Phase 6: Semantic audit ---
            print(f"\n== semantic-audit ({len(domains)} domains) ==")

            def audit_input(domain):
                return {"paper_id": paper_id, "domain": domain, "mode": "audit"}

            run_triads_for_usecase(session, repo_root, steps, "semantic-audit", domains,
                                   audit_input, report, label_prefix="semantic-audit")

            # --- Phase 7: Plagiarism forensic + targeted rewrite loop ---
            max_humanize_iterations = 5
            print(f"\n== plagiarism-forensic-audit ({len(domains)} domains) ==")

            def plagiarism_input(domain):
                return {"paper_id": paper_id, "domain": domain}

            run_triads_for_usecase(session, repo_root, steps, "plagiarism-forensic-audit",
                                   domains, plagiarism_input, report,
                                   label_prefix="plagiarism-forensic-audit")

            print(f"\n== humanize (loop up to {max_humanize_iterations} iterations) ==")
            # Humanize loop is driven by an agent reading the workflow report
            # and calling prepare/complete_semantic_step for FAIL domains.

        # --- Phase 8: Calculate + Render (if available) ---
        for usecase in ("calculate", "render"):
            uc_steps = steps_of(steps, usecase)
            if uc_steps:
                step = uc_steps[0]
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
        print(f"  (see {report_path} for every domain -> step_id mapping)")

    sys.exit(1 if report["failed"] else 0)


if __name__ == "__main__":
    main()
