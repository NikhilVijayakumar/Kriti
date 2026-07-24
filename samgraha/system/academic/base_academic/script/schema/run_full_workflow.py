#!/usr/bin/env python3
"""
run_full_workflow.py — master orchestrator for base_academic's samgraha
standard. Drives every step through the REAL MCP protocol (spawns the built
`mcp` binary, speaks JSON-RPC over stdio).

Execution order:
  1. register_standard — (re)registers standard.yaml
  2. schema-init — creates academic_* tables, seeds domains/templates
  3. classify-repo — determines repo state (2-state: NO_DOCS / HAS_DOCS)
  4. expand_triads — inserts domain-expanded steps into knowledge.db
  5. novelty-analysis → gap-analysis → mathematics-and-diagrams (§2.1-2.3)
  6. assemble-paper-structure (§2.4)
  7. deterministic-audit → semantic-audit → fix-loop (§2.5)
  8. plagiarism-forensic-audit → humanize (loop until PASS or max_iterations)
  9. calculate / render-audit-report / render-paper (§4, §7)
"""
import argparse
import json
import sqlite3
import subprocess
import sys
from pathlib import Path


# Domains that receive literature-review enrichment (conditional 4th step
# in assemble-paper-structure, gated by _master-schema.yaml's cite_context:).
CITE_CONTEXT_DOMAINS = {"related-work", "introduction", "discussion"}


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
# that have steps: [] in standard.yaml.
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
    """Delete steps with step_order > max_order for a usecase."""
    con.execute(
        "DELETE FROM step WHERE usecase_id=? AND step_order>?",
        (usecase_id, max_order),
    )
    con.commit()


def expand_triads(db_path, standard, domains, module_names=None,
                  cite_context_domains=None):
    """Insert expanded triad steps into knowledge.db for usecases that have
    steps: [] in standard.yaml.

    New usecase sequence (per proposal §2):
      0. classify-repo (single step, not expanded)
      1. novelty-analysis
      2. gap-analysis
      3. mathematics-and-diagrams
      4. assemble-paper-structure (+ conditional literature-review step)
      5. deterministic-audit
      6. semantic-audit
      7. plagiarism-forensic-audit (5-step: det pre-screen + sem + conditional Pass 2)
      8. humanize
      9. deterministic-fingerprint-check (standalone, used by plagiarism)
    """
    if module_names is None:
        module_names = []
    if cite_context_domains is None:
        cite_context_domains = CITE_CONTEXT_DOMAINS

    con = sqlite3.connect(db_path)
    con.row_factory = sqlite3.Row
    count = 0

    gather_mod_script = _lookup_script_id(con, "gather-module-evidence")
    persist_mod_script = _lookup_script_id(con, "persist-module-analysis")
    gather_xmod_script = _lookup_script_id(con, "gather-cross-module-evidence")
    persist_xmod_script = _lookup_script_id(con, "persist-cross-module-analysis")
    gather_domain_script = _lookup_script_id(con, "gather-domain-evidence")
    persist_domain_script = _lookup_script_id(con, "persist-section-draft")

    # --- 1. novelty-analysis: per-module + cross-module triads ---
    uc_id = _lookup_usecase_id(con, standard, "novelty-analysis")
    if uc_id and module_names:
        # 1 discover-modules + (modules * 3) + (1 cross-module * 3)
        expected = 1 + len(module_names) * 3 + 3
        _truncate_usecase_steps(con, uc_id, expected)
        discover_script = _lookup_script_id(con, "discover-modules")
        novelty_prompt = _lookup_prompt_id(con, "module-analysis-novelty")
        xnovelty_prompt = _lookup_prompt_id(con, "cross-module-analysis-novelty")
        order = 1
        _insert_step(con, uc_id, order, "deterministic",
                     "Discover module boundaries", script_id=discover_script)
        order += 1
        for mod_name in module_names:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather evidence for {mod_name}", script_id=gather_mod_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"Write novelty analysis for {mod_name}", prompt_id=novelty_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist novelty for {mod_name}", script_id=persist_mod_script)
            count += 3
            order += 3
        # Cross-module novelty
        _insert_step(con, uc_id, order, "deterministic",
                     "Pre: gather cross-module evidence for novelty",
                     script_id=gather_xmod_script)
        _insert_step(con, uc_id, order + 1, "semantic",
                     "Write cross-module novelty", prompt_id=xnovelty_prompt)
        _insert_step(con, uc_id, order + 2, "deterministic",
                     "Post: persist cross-module novelty",
                     script_id=persist_xmod_script)
        count += 3

    # --- 2. gap-analysis: per-module + cross-module triads ---
    uc_id = _lookup_usecase_id(con, standard, "gap-analysis")
    if uc_id and module_names:
        expected = 1 + len(module_names) * 3 + 3
        _truncate_usecase_steps(con, uc_id, expected)
        discover_script = _lookup_script_id(con, "discover-modules")
        gaps_prompt = _lookup_prompt_id(con, "module-analysis-gaps")
        xgaps_prompt = _lookup_prompt_id(con, "cross-module-analysis-gaps")
        order = 1
        _insert_step(con, uc_id, order, "deterministic",
                     "Discover module boundaries", script_id=discover_script)
        order += 1
        for mod_name in module_names:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather evidence for {mod_name}", script_id=gather_mod_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"Write gap analysis for {mod_name}", prompt_id=gaps_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist gaps for {mod_name}", script_id=persist_mod_script)
            count += 3
            order += 3
        _insert_step(con, uc_id, order, "deterministic",
                     "Pre: gather cross-module evidence for gaps",
                     script_id=gather_xmod_script)
        _insert_step(con, uc_id, order + 1, "semantic",
                     "Write cross-module gaps", prompt_id=xgaps_prompt)
        _insert_step(con, uc_id, order + 2, "deterministic",
                     "Post: persist cross-module gaps",
                     script_id=persist_xmod_script)
        count += 3

    # --- 3. mathematics-and-diagrams: per-module (math + architecture) + cross-module ---
    uc_id = _lookup_usecase_id(con, standard, "mathematics-and-diagrams")
    if uc_id and module_names:
        # Per module: math prompt + architecture prompt (2 semantic per module)
        # Cross-module: architecture + dependencies + interactions (3 semantic)
        mod_triads = len(module_names) * 2 * 3  # 2 prompts per module
        xmod_triads = 3 * 3  # 3 cross-module prompts
        expected = 1 + mod_triads + xmod_triads
        _truncate_usecase_steps(con, uc_id, expected)
        discover_script = _lookup_script_id(con, "discover-modules")
        math_prompt = _lookup_prompt_id(con, "module-analysis-mathematics")
        arch_prompt = _lookup_prompt_id(con, "module-analysis-architecture")
        xarch_prompt = _lookup_prompt_id(con, "cross-module-analysis-architecture")
        xdeps_prompt = _lookup_prompt_id(con, "cross-module-analysis-dependencies")
        xinter_prompt = _lookup_prompt_id(con, "cross-module-analysis-interactions")
        order = 1
        _insert_step(con, uc_id, order, "deterministic",
                     "Discover module boundaries", script_id=discover_script)
        order += 1
        for mod_name in module_names:
            # Mathematics
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather evidence for {mod_name}", script_id=gather_mod_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"Formalize mathematics for {mod_name}", prompt_id=math_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist math for {mod_name}", script_id=persist_mod_script)
            count += 3
            order += 3
            # Architecture diagrams
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather evidence for {mod_name}", script_id=gather_mod_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"Write architecture diagram for {mod_name}", prompt_id=arch_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist architecture for {mod_name}", script_id=persist_mod_script)
            count += 3
            order += 3
        # Cross-module: architecture, dependencies, interactions
        for kind_prompt, kind_label in [
            (xarch_prompt, "architecture"), (xdeps_prompt, "dependencies"),
            (xinter_prompt, "interactions"),
        ]:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather cross-module evidence for {kind_label}",
                         script_id=gather_xmod_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"Write cross-module {kind_label}", prompt_id=kind_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist cross-module {kind_label}",
                         script_id=persist_xmod_script)
            count += 3
            order += 3

    # --- 4. assemble-paper-structure: per-domain triads + conditional literature-review ---
    uc_id = _lookup_usecase_id(con, standard, "assemble-paper-structure")
    if uc_id:
        # Base: 3 steps per domain
        # Plus 1 conditional step per domain in cite_context
        cite_count = sum(1 for d in domains if d in cite_context_domains)
        expected = 3 * len(domains) + cite_count
        _truncate_usecase_steps(con, uc_id, expected)
        lit_prompt = _lookup_prompt_id(con, "literature-review-pass")
        order = 1
        for domain in domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather docs + analysis for {domain}",
                         script_id=gather_domain_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"Generate {domain}", prompt_id=_lookup_prompt_id(con, "generate-section"))
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist {domain} draft", script_id=persist_domain_script)
            count += 3
            order += 3
            # Conditional literature-review step for cite_context domains
            if domain in cite_context_domains and lit_prompt:
                _insert_step(con, uc_id, order, "semantic",
                             f"Literature-review pass for {domain}",
                             prompt_id=lit_prompt)
                count += 1
                order += 1

    # --- 5. deterministic-audit: per-domain triads ---
    uc_id = _lookup_usecase_id(con, standard, "deterministic-audit")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 3 * len(domains))
        det_audit_script = _lookup_script_id(con, "deterministic-audit")
        order = 1
        for domain in domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Gather + check deterministic rules for {domain}",
                         script_id=det_audit_script)
            # Persist is done inside deterministic-audit.py directly
            count += 1
            order += 1

    # --- 6. semantic-audit: per-domain triads (unchanged shape) ---
    uc_id = _lookup_usecase_id(con, standard, "semantic-audit")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 3 * len(domains))
        sem_prompt = _lookup_prompt_id(con, "semantic-audit")
        persist_sem_script = _lookup_script_id(con, "persist-domain-semantic-score")
        order = 1
        for domain in domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather draft + rubric for {domain}",
                         script_id=gather_domain_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"Score {domain} against rubric",
                         prompt_id=sem_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist {domain} score",
                         script_id=persist_sem_script)
            count += 3
            order += 3

    # --- 7. plagiarism-forensic-audit: 5 steps per domain ---
    # Step 1: gather context (det)
    # Step 2: deterministic fingerprint pre-screen (det)
    # Step 3: semantic fingerprint audit (sem)
    # Step 4: targeted rewrite — conditional on step 2 or 3 flags (sem)
    # Step 5: persist findings (det)
    uc_id = _lookup_usecase_id(con, standard, "plagiarism-forensic-audit")
    if uc_id:
        # Max possible: 5 steps per domain (step 4 always inserted; orchestrator
        # skips it if no flags)
        _truncate_usecase_steps(con, uc_id, 5 * len(domains))
        gather_plag_script = _lookup_script_id(con, "gather-plagiarism-context")
        det_fp_script = _lookup_script_id(con, "deterministic-fingerprint-check")
        forensic_prompt = _lookup_prompt_id(con, "plagiarism-fingerprint-audit")
        targeted_prompt = _lookup_prompt_id(con, "targeted-rewrite")
        persist_plag_script = _lookup_script_id(con, "persist-plagiarism-findings")
        order = 1
        for domain in domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Gather plagiarism context for {domain}",
                         script_id=gather_plag_script)
            _insert_step(con, uc_id, order + 1, "deterministic",
                         f"Deterministic fingerprint check for {domain}",
                         script_id=det_fp_script)
            _insert_step(con, uc_id, order + 2, "semantic",
                         f"Forensic audit {domain}",
                         prompt_id=forensic_prompt)
            _insert_step(con, uc_id, order + 3, "semantic",
                         f"Targeted rewrite {domain} (conditional)",
                         prompt_id=targeted_prompt)
            _insert_step(con, uc_id, order + 4, "deterministic",
                         f"Persist plagiarism findings for {domain}",
                         script_id=persist_plag_script)
            count += 5
            order += 5

    # --- 8. humanize: per-domain triads (unchanged shape) ---
    uc_id = _lookup_usecase_id(con, standard, "humanize")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 3 * len(domains))
        gather_hum_script = _lookup_script_id(con, "gather-humanize-context")
        hum_prompt = _lookup_prompt_id(con, "humanize-section")
        persist_hum_script = _lookup_script_id(con, "persist-humanize-pass")
        order = 1
        for domain in domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Gather humanize context for {domain}",
                         script_id=gather_hum_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"3-layer humanize rewrite {domain}",
                         prompt_id=hum_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Persist humanized {domain}",
                         script_id=persist_hum_script)
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
                           input_fn, report, label_prefix, steps_per_domain=3):
    """Run pre/semantic/post triads for a usecase, one per domain."""
    uc_steps = steps_of(steps, usecase)
    if not uc_steps:
        print(f"  WARNING: no steps for {usecase} — skipping")
        return
    triads = len(uc_steps) // steps_per_domain
    for i, domain in enumerate(domains):
        if i >= triads:
            break
        base = steps_per_domain * i
        pre, sem, post = uc_steps[base], uc_steps[base + 1], uc_steps[base + 2]
        pre_input = input_fn(domain)
        stage_semantic_triad(session, repo_root, pre, sem, post, pre_input, report,
                             label=f"{label_prefix}/{domain}")


def run_deterministic_triads_for_usecase(session, repo_root, steps, usecase,
                                         domains, input_fn, report, label_prefix):
    """Run single-step deterministic triads for a usecase (e.g. deterministic-audit)."""
    uc_steps = steps_of(steps, usecase)
    if not uc_steps:
        print(f"  WARNING: no steps for {usecase} — skipping")
        return
    for i, domain in enumerate(domains):
        if i >= len(uc_steps):
            break
        step = uc_steps[i]
        step_input = input_fn(domain)
        try:
            r = session.call("run_script_step", {
                "step_id": step["id"], "repo_path": repo_root, "input": step_input,
            })
            status = r.get("status", "error")
            report["ran"].append({"step": f"{label_prefix}/{domain}", "status": status,
                                  "message": r.get("message", "")[:500]})
            if status != "ok":
                report["failed"].append({"label": f"{label_prefix}/{domain}",
                                         "stage": "run", "message": r.get("message", "")})
        except Exception as e:
            report["failed"].append({"label": f"{label_prefix}/{domain}",
                                     "stage": "run", "message": str(e)})


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

        # --- Phase 2: Classify (2-state gate) ---
        print("\n== classify-repo ==")
        classify_step = steps_of(steps, "classify-repo")[0]
        r = session.call("run_script_step", {"step_id": classify_step["id"], "repo_path": repo_root})
        report["ran"].append({"step": "classify-repo", "status": r.get("status")})

        classification = get_repo_classification(db_path, args.standard, repo_root)
        paper_id = get_paper_id(db_path, args.standard, repo_root)
        domains = args.domains or domain_keys(db_path)
        modules = modules_for_paper(db_path, paper_id) if paper_id else []
        print(f"  classification={classification}, domains={len(domains)}, modules={len(modules)}")

        # --- Phase 3: Expand triads into DB ---
        print(f"\n== expand_triads ({len(domains)} domains, {len(modules)} modules) ==")
        insert_count = expand_triads(db_path, args.standard, domains,
                                     module_names=modules)
        print(f"  inserted {insert_count} steps")

        # Reload steps after expansion
        steps = load_steps(db_path, args.standard)

        # --- Gate: refuse if NO_DOCS ---
        if classification == "NO_DOCS":
            print("\n== REFUSED: no documentation — pipeline requires author-supplied docs ==")
            report["failed"].append({"label": "entry", "stage": "refuse",
                                     "message": "NO_DOCS: no author-supplied documentation found"})
        else:
            # --- Phase 4: Analysis usecases (novelty, gap, math+diagrams) ---
            if modules:
                for analysis_usecase in ("novelty-analysis", "gap-analysis",
                                         "mathematics-and-diagrams"):
                    print(f"\n== {analysis_usecase} ({len(modules)} modules) ==")
                    uc_steps = steps_of(steps, analysis_usecase)
                    if not uc_steps:
                        print(f"  WARNING: no steps for {analysis_usecase} — skipping")
                        continue
                    # Step 1 is always discover-modules (single step)
                    first_step = uc_steps[0]
                    try:
                        r = session.call("run_script_step",
                                         {"step_id": first_step["id"], "repo_path": repo_root})
                        report["ran"].append({"step": f"{analysis_usecase}/discover-modules",
                                              "status": r.get("status")})
                    except Exception as e:
                        report["failed"].append({"label": f"{analysis_usecase}/discover-modules",
                                                 "stage": "run", "message": str(e)})

            # --- Phase 5: Assemble paper structure ---
            print(f"\n== assemble-paper-structure ({len(domains)} domains) ==")

            def assemble_input(domain):
                return {"paper_id": paper_id, "domain": domain, "mode": "generate"}

            run_triads_for_usecase(session, repo_root, steps, "assemble-paper-structure",
                                   domains, assemble_input, report,
                                   label_prefix="assemble-paper-structure")

            # --- Phase 6: Deterministic audit (cheap fail-fast) ---
            print(f"\n== deterministic-audit ({len(domains)} domains) ==")

            det_failed_domains = set()

            def det_audit_input(domain):
                return {"paper_id": paper_id, "domain": domain}

            run_deterministic_triads_for_usecase(session, repo_root, steps,
                                                 "deterministic-audit", domains,
                                                 det_audit_input, report,
                                                 "deterministic-audit")

            # Check which domains failed deterministic audit
            for step_entry in report["ran"]:
                if (step_entry["step"].startswith("deterministic-audit/")
                        and step_entry.get("status") != "ok"):
                    domain_key = step_entry["step"].split("/", 1)[1]
                    det_failed_domains.add(domain_key)

            # --- Phase 7: Semantic audit (only for deterministic-PASS domains) ---
            sem_domains = [d for d in domains if d not in det_failed_domains]
            skipped_domains = [d for d in domains if d in det_failed_domains]

            if skipped_domains:
                print(f"\n== skipping semantic-audit for {len(skipped_domains)} domains "
                      f"(deterministic FAIL): {skipped_domains} ==")
                for d in skipped_domains:
                    report["ran"].append({
                        "step": f"semantic-audit/{d}",
                        "status": "skipped",
                        "message": "skipped: deterministic audit FAIL — fix mechanical gaps first",
                    })

            if sem_domains:
                print(f"\n== semantic-audit ({len(sem_domains)} domains) ==")

                def audit_input(domain):
                    return {"paper_id": paper_id, "domain": domain, "mode": "audit"}

                run_triads_for_usecase(session, repo_root, steps, "semantic-audit",
                                       sem_domains, audit_input, report,
                                       label_prefix="semantic-audit")

            # --- Phase 8: Plagiarism forensic + targeted rewrite loop ---
            max_humanize_iterations = 5
            print(f"\n== plagiarism-forensic-audit ({len(domains)} domains) ==")

            def plagiarism_input(domain):
                return {"paper_id": paper_id, "domain": domain}

            run_triads_for_usecase(session, repo_root, steps,
                                   "plagiarism-forensic-audit",
                                   domains, plagiarism_input, report,
                                   label_prefix="plagiarism-forensic-audit",
                                   steps_per_domain=5)

            print(f"\n== humanize (loop up to {max_humanize_iterations} iterations) ==")
            # Humanize loop is driven by an agent reading the workflow report
            # and calling prepare/complete_semantic_step for FAIL domains.

        # --- Phase 9: Calculate + Render ---
        for usecase in ("calculate", "render-audit-report", "render-paper"):
            uc_steps = steps_of(steps, usecase)
            if uc_steps:
                step = uc_steps[0]
                try:
                    r = session.call("run_script_step",
                                     {"step_id": step["id"], "repo_path": repo_root, "input": {}},
                                     timeout_secs=300)
                    report["ran"].append({"step": usecase, "status": r.get("status"),
                                          "message": r.get("message", "")[:500]})
                except Exception as e:
                    report["failed"].append({"label": usecase, "stage": "run",
                                             "message": str(e)})

    finally:
        session.close()

    report_path = args.report_out or str(Path(repo_root) / ".samgraha" / "workflow-report.json")
    Path(report_path).write_text(json.dumps(report, indent=2))

    print(f"\n== summary ==")
    print(f"ran: {len(report['ran'])}, failed: {len(report['failed'])}, "
          f"pending semantic: {len(report['pending_semantic'])}")
    print(f"full report: {report_path}")
    if report["pending_semantic"]:
        print(f"\n{len(report['pending_semantic'])} semantic steps staged but NOT completed "
              f"— need an agent to:")
        print("  1. prepare_semantic_step(semantic_step_id) to re-fetch the prompt")
        print("  2. reason over it, then complete_semantic_step(semantic_step_id)")
        print("  3. run_script_step(persist_step_id, input={..., result/sections: <the model's answer>})")
        print(f"  (see {report_path} for every domain -> step_id mapping)")

    sys.exit(1 if report["failed"] else 0)


if __name__ == "__main__":
    main()
