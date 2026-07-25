#!/usr/bin/env python3
"""
run_full_workflow.py — master orchestrator for base_academic's samgraha
standard. Drives every step through the REAL MCP protocol (spawns the built
`mcp` binary, speaks JSON-RPC over stdio).

Execution order (base_academic-usecase-atomicity-proposal.md §2):
  1. register_standard — (re)registers standard.yaml
  2. schema-init — creates academic_* tables, seeds domains/templates
  3. classify-repo — determines repo state (2-state: NO_DOCS / HAS_DOCS)
  4. expand_triads — inserts domain-expanded steps into knowledge.db
  5. novelty-analysis / gap-analysis / mathematics-analysis (3a) /
     diagram-architecture-analysis (3b)
  6. generate-section-draft (4a) -> section-citations (4b) ->
     section-supplementary-content (4c) -> section-budget-fit (4d)
  7. deterministic-audit -> semantic-audit (fail-fast on deterministic FAIL)
  8. plagiarism-forensic-audit -> humanize-deterministic (5c) ->
     humanize-semantic (5d, agent-driven loop for still-flagged domains)
  9. document-narrative-polish (4e) -> cross-section-semantic-audit (5e) ->
     document-semantic-audit (5f)
  10. calculate -> render-charts -> render-audit-report -> render-paper
"""
import argparse
import json
import sqlite3
import subprocess
import sys
from pathlib import Path


# Domains that receive literature-review enrichment (conditional extra
# steps in section-citations / 4b, gated by _master-schema.yaml's
# cite_context:).
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


def _expand_module_triads(con, uc_id, module_names, gather_mod_script,
                          persist_mod_script, per_module_prompts,
                          gather_xmod_script, persist_xmod_script,
                          cross_module_prompts):
    """Shared shape for novelty-analysis / gap-analysis / mathematics-analysis /
    diagram-architecture-analysis: discover-modules (1) + per-module triads
    (one per prompt in per_module_prompts, per module) + cross-module triads
    (one per prompt in cross_module_prompts). Returns steps inserted."""
    count = 0
    discover_script = _lookup_script_id(con, "discover-modules")
    order = 1
    _insert_step(con, uc_id, order, "deterministic",
                 "Discover module boundaries", script_id=discover_script)
    order += 1
    for mod_name in module_names:
        for label, prompt_id in per_module_prompts:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather evidence for {mod_name}", script_id=gather_mod_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"{label} for {mod_name}", prompt_id=prompt_id)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist {label.lower()} for {mod_name}", script_id=persist_mod_script)
            count += 3
            order += 3
    for label, prompt_id in cross_module_prompts:
        _insert_step(con, uc_id, order, "deterministic",
                     f"Pre: gather cross-module evidence for {label.lower()}",
                     script_id=gather_xmod_script)
        _insert_step(con, uc_id, order + 1, "semantic",
                     f"Write cross-module {label.lower()}", prompt_id=prompt_id)
        _insert_step(con, uc_id, order + 2, "deterministic",
                     f"Post: persist cross-module {label.lower()}",
                     script_id=persist_xmod_script)
        count += 3
        order += 3
    return count


def expand_triads(db_path, standard, domains, module_names=None,
                  cite_context_domains=None):
    """Insert expanded triad steps into knowledge.db for usecases that have
    steps: [] in standard.yaml. Matches the current usecase split — see
    docs/proposal/base_academic-usecase-atomicity-proposal.md §2/§9.
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
        expected = 1 + len(module_names) * 3 + 3
        _truncate_usecase_steps(con, uc_id, expected)
        count += _expand_module_triads(
            con, uc_id, module_names, gather_mod_script, persist_mod_script,
            [("Write novelty analysis", _lookup_prompt_id(con, "module-analysis-novelty"))],
            gather_xmod_script, persist_xmod_script,
            [("Novelty", _lookup_prompt_id(con, "cross-module-analysis-novelty"))],
        )

    # --- 2. gap-analysis: per-module + cross-module triads ---
    uc_id = _lookup_usecase_id(con, standard, "gap-analysis")
    if uc_id and module_names:
        expected = 1 + len(module_names) * 3 + 3
        _truncate_usecase_steps(con, uc_id, expected)
        count += _expand_module_triads(
            con, uc_id, module_names, gather_mod_script, persist_mod_script,
            [("Write gap analysis", _lookup_prompt_id(con, "module-analysis-gaps"))],
            gather_xmod_script, persist_xmod_script,
            [("Gaps", _lookup_prompt_id(con, "cross-module-analysis-gaps"))],
        )

    # --- 3a. mathematics-analysis: per-module math + cross-module math ---
    uc_id = _lookup_usecase_id(con, standard, "mathematics-analysis")
    if uc_id and module_names:
        expected = 1 + len(module_names) * 3 + 3
        _truncate_usecase_steps(con, uc_id, expected)
        count += _expand_module_triads(
            con, uc_id, module_names, gather_mod_script, persist_mod_script,
            [("Formalize mathematics", _lookup_prompt_id(con, "module-analysis-mathematics"))],
            gather_xmod_script, persist_xmod_script,
            [("Mathematics", _lookup_prompt_id(con, "cross-module-analysis-mathematics"))],
        )

    # --- 3b. diagram-architecture-analysis: per-module architecture +
    #     cross-module architecture/dependencies/interactions ---
    uc_id = _lookup_usecase_id(con, standard, "diagram-architecture-analysis")
    if uc_id and module_names:
        expected = 1 + len(module_names) * 3 + 3 * 3
        _truncate_usecase_steps(con, uc_id, expected)
        count += _expand_module_triads(
            con, uc_id, module_names, gather_mod_script, persist_mod_script,
            [("Write architecture diagram", _lookup_prompt_id(con, "module-analysis-architecture"))],
            gather_xmod_script, persist_xmod_script,
            [("Architecture", _lookup_prompt_id(con, "cross-module-analysis-architecture")),
             ("Dependencies", _lookup_prompt_id(con, "cross-module-analysis-dependencies")),
             ("Interactions", _lookup_prompt_id(con, "cross-module-analysis-interactions"))],
        )

    # --- 4a. generate-section-draft: per-domain triad, excludes references ---
    uc_id = _lookup_usecase_id(con, standard, "generate-section-draft")
    gen_domains = [d for d in domains if d != "references"]
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 3 * len(gen_domains))
        gen_prompt = _lookup_prompt_id(con, "generate-section")
        order = 1
        for domain in gen_domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather docs + analysis for {domain}",
                         script_id=gather_domain_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"Generate {domain}", prompt_id=gen_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist {domain} draft", script_id=persist_domain_script)
            count += 3
            order += 3

    # --- 4b. section-citations: per-domain in-repo citations (det) +
    #     literature-review-pass for cite-context domains (sem) +
    #     collate-references (det, single, last) ---
    uc_id = _lookup_usecase_id(con, standard, "section-citations")
    if uc_id:
        expected = 0
        for d in gen_domains:
            expected += 4 if d in cite_context_domains else 2
        expected += 1  # collate-references
        _truncate_usecase_steps(con, uc_id, expected)
        persist_cite_script = _lookup_script_id(con, "persist-section-citations")
        lit_prompt = _lookup_prompt_id(con, "literature-review-pass")
        collate_script = _lookup_script_id(con, "collate-references")
        order = 1
        for domain in gen_domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: extract in-repo citation markers for {domain}",
                         script_id=gather_domain_script)
            _insert_step(con, uc_id, order + 1, "deterministic",
                         f"Post: persist in-repo citations for {domain}",
                         script_id=persist_cite_script)
            count += 2
            order += 2
            if domain in cite_context_domains and lit_prompt:
                _insert_step(con, uc_id, order, "semantic",
                             f"Literature-review pass for {domain}", prompt_id=lit_prompt)
                _insert_step(con, uc_id, order + 1, "deterministic",
                             f"Post: persist literature citations + draft for {domain}",
                             script_id=persist_cite_script)
                count += 2
                order += 2
        _insert_step(con, uc_id, order, "deterministic",
                     "Collate all citations into references domain draft",
                     script_id=collate_script)
        count += 1

    # --- 4c. section-supplementary-content: per-domain triad, all domains
    #     (references included — it has content by now via 4b) ---
    uc_id = _lookup_usecase_id(con, standard, "section-supplementary-content")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 3 * len(domains))
        enrich_prompt = _lookup_prompt_id(con, "section-enrichment")
        order = 1
        for domain in domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather math/architecture findings for {domain}",
                         script_id=gather_domain_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"Enrich {domain} with math/tables/diagrams", prompt_id=enrich_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist enriched {domain}", script_id=persist_domain_script)
            count += 3
            order += 3

    # --- 4d. section-budget-fit: per-domain check + conditional fit + persist ---
    uc_id = _lookup_usecase_id(con, standard, "section-budget-fit")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 3 * len(domains))
        check_script = _lookup_script_id(con, "check-word-budget")
        fit_prompt = _lookup_prompt_id(con, "fit-to-budget")
        order = 1
        for domain in domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Check word budget for {domain}", script_id=check_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"Fit {domain} to budget (conditional)", prompt_id=fit_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist budget-fit {domain}", script_id=persist_domain_script)
            count += 3
            order += 3

    # --- 5. deterministic-audit: per-domain single step ---
    uc_id = _lookup_usecase_id(con, standard, "deterministic-audit")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, len(domains))
        det_audit_script = _lookup_script_id(con, "deterministic-audit")
        order = 1
        for domain in domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Gather + check deterministic rules for {domain}",
                         script_id=det_audit_script)
            count += 1
            order += 1

    # --- 6. semantic-audit: per-domain triad ---
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
                         f"Score {domain} against rubric", prompt_id=sem_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Post: persist {domain} score", script_id=persist_sem_script)
            count += 3
            order += 3

    # --- 7. plagiarism-forensic-audit: 5 steps per domain (unchanged shape) ---
    uc_id = _lookup_usecase_id(con, standard, "plagiarism-forensic-audit")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 5 * len(domains))
        gather_plag_script = _lookup_script_id(con, "gather-plagiarism-context")
        det_fp_script = _lookup_script_id(con, "deterministic-fingerprint-check")
        forensic_prompt = _lookup_prompt_id(con, "plagiarism-fingerprint-audit")
        targeted_prompt = _lookup_prompt_id(con, "targeted-rewrite")
        persist_plag_script = _lookup_script_id(con, "persist-plagiarism-findings")
        order = 1
        for domain in domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Gather plagiarism context for {domain}", script_id=gather_plag_script)
            _insert_step(con, uc_id, order + 1, "deterministic",
                         f"Deterministic fingerprint check for {domain}", script_id=det_fp_script)
            _insert_step(con, uc_id, order + 2, "semantic",
                         f"Forensic audit {domain}", prompt_id=forensic_prompt)
            _insert_step(con, uc_id, order + 3, "semantic",
                         f"Targeted rewrite {domain} (conditional)", prompt_id=targeted_prompt)
            _insert_step(con, uc_id, order + 4, "deterministic",
                         f"Persist plagiarism findings for {domain}", script_id=persist_plag_script)
            count += 5
            order += 5

    # --- 5c. humanize-deterministic: gather + NLP mechanical fix, per domain ---
    uc_id = _lookup_usecase_id(con, standard, "humanize-deterministic")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 2 * len(domains))
        gather_hum_script = _lookup_script_id(con, "gather-humanize-context")
        nlp_fix_script = _lookup_script_id(con, "nlp-fingerprint-fix")
        order = 1
        for domain in domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Gather humanize context for {domain}", script_id=gather_hum_script)
            _insert_step(con, uc_id, order + 1, "deterministic",
                         f"NLP mechanical fix for {domain}", script_id=nlp_fix_script)
            count += 2
            order += 2

    # --- 5d. humanize-semantic: gather + LLM rewrite + persist, per domain ---
    uc_id = _lookup_usecase_id(con, standard, "humanize-semantic")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 3 * len(domains))
        gather_hum_script = _lookup_script_id(con, "gather-humanize-context")
        hum_prompt = _lookup_prompt_id(con, "humanize-section")
        persist_hum_script = _lookup_script_id(con, "persist-humanize-pass")
        order = 1
        for domain in domains:
            _insert_step(con, uc_id, order, "deterministic",
                         f"Gather humanize context for {domain}", script_id=gather_hum_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         f"Layers 2-3 humanize rewrite {domain}", prompt_id=hum_prompt)
            _insert_step(con, uc_id, order + 2, "deterministic",
                         f"Persist humanized {domain}", script_id=persist_hum_script)
            count += 3
            order += 3

    # --- 4e. document-narrative-polish: 3 sequential whole-document
    #     sub-passes (gather + prompt each) — persistence fan-out (one
    #     persist-section-draft call per domain the pass actually changed)
    #     is agent-driven, same deferred pattern the humanize loop uses. ---
    uc_id = _lookup_usecase_id(con, standard, "document-narrative-polish")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 6)
        gather_doc_script = _lookup_script_id(con, "gather-document-evidence")
        order = 1
        for label, prompt_name in (
            ("Structure polish", "structure-polish"),
            ("Narrative-style polish", "narrative-style-polish"),
            ("Content-detail polish", "content-detail-polish"),
        ):
            _insert_step(con, uc_id, order, "deterministic",
                         f"Pre: gather whole document for {label.lower()}",
                         script_id=gather_doc_script)
            _insert_step(con, uc_id, order + 1, "semantic",
                         label, prompt_id=_lookup_prompt_id(con, prompt_name))
            count += 2
            order += 2

    # --- 5e. cross-section-semantic-audit: single triad ---
    uc_id = _lookup_usecase_id(con, standard, "cross-section-semantic-audit")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 3)
        gather_xs_script = _lookup_script_id(con, "gather-cross-section-evidence")
        xs_prompt = _lookup_prompt_id(con, "cross-section-semantic-audit")
        persist_xs_script = _lookup_script_id(con, "persist-domain-semantic-score")
        order = 1
        _insert_step(con, uc_id, order, "deterministic",
                     "Gather cross-section evidence", script_id=gather_xs_script)
        _insert_step(con, uc_id, order + 1, "semantic",
                     "Cross-section consistency review", prompt_id=xs_prompt)
        _insert_step(con, uc_id, order + 2, "deterministic",
                     "Persist cross-section score", script_id=persist_xs_script)
        count += 3

    # --- 5f. document-semantic-audit: single triad ---
    uc_id = _lookup_usecase_id(con, standard, "document-semantic-audit")
    if uc_id:
        _truncate_usecase_steps(con, uc_id, 3)
        gather_doc_script = _lookup_script_id(con, "gather-document-evidence")
        doc_prompt = _lookup_prompt_id(con, "document-semantic-audit")
        persist_doc_script = _lookup_script_id(con, "persist-domain-semantic-score")
        order = 1
        _insert_step(con, uc_id, order, "deterministic",
                     "Gather document evidence", script_id=gather_doc_script)
        _insert_step(con, uc_id, order + 1, "semantic",
                     "Document holistic review", prompt_id=doc_prompt)
        _insert_step(con, uc_id, order + 2, "deterministic",
                     "Persist document score", script_id=persist_doc_script)
        count += 3

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
        "persist_step_id": post["id"] if post is not None else None,
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
                                         domains, input_fn, report, label_prefix,
                                         steps_per_domain=1):
    """Run all-deterministic steps for a usecase (e.g. deterministic-audit,
    humanize-deterministic). steps_per_domain > 1 runs each domain's whole
    step group sequentially, feeding each step the same input_fn(domain)."""
    uc_steps = steps_of(steps, usecase)
    if not uc_steps:
        print(f"  WARNING: no steps for {usecase} — skipping")
        return
    groups = len(uc_steps) // steps_per_domain
    for i, domain in enumerate(domains):
        if i >= groups:
            break
        step_input = input_fn(domain)
        for j in range(steps_per_domain):
            step = uc_steps[i * steps_per_domain + j]
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
            gen_domains = [d for d in domains if d != "references"]

            # --- Phase 4: Analysis usecases (novelty, gap, math, diagrams) ---
            if modules:
                for analysis_usecase in ("novelty-analysis", "gap-analysis",
                                         "mathematics-analysis",
                                         "diagram-architecture-analysis"):
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

            # --- Phase 5: Generate section drafts (4a) ---
            print(f"\n== generate-section-draft ({len(gen_domains)} domains) ==")

            def generate_input(domain):
                return {"paper_id": paper_id, "domain": domain, "mode": "generate"}

            run_triads_for_usecase(session, repo_root, steps, "generate-section-draft",
                                   gen_domains, generate_input, report,
                                   label_prefix="generate-section-draft")

            # --- Phase 5b: Section citations (4b) — det steps auto-run,
            # literature-review-pass semantic steps + collate-references
            # are staged/run by run_triads_for_usecase's mixed step shape;
            # left to the agent loop like other semantic steps. ---
            print(f"\n== section-citations ({len(gen_domains)} domains) ==")
            cite_steps = steps_of(steps, "section-citations")
            if cite_steps:
                # The det (gather-citation -> persist-citation) pairs run
                # inline; semantic literature-review steps are staged.
                for domain in gen_domains:
                    matches = [s for s in cite_steps if s["description"].endswith(f"for {domain}")]
                    i = 0
                    while i < len(matches):
                        s = matches[i]
                        if s["kind"] == "deterministic" and s["description"].startswith("Pre: extract"):
                            in_repo_input = {"paper_id": paper_id, "domain": domain, "mode": "citation"}
                            gather_r = session.call("run_script_step",
                                                    {"step_id": s["id"], "repo_path": repo_root,
                                                     "input": in_repo_input})
                            persist_input = {"paper_id": paper_id, "domain": domain,
                                             "source_kind": "in-repo",
                                             "citations": gather_r.get("evidence", {}).get("citations", [])}
                            i += 1
                            if i < len(matches):
                                p_r = session.call("run_script_step",
                                                   {"step_id": matches[i]["id"], "repo_path": repo_root,
                                                    "input": persist_input})
                                report["ran"].append({"step": f"section-citations/{domain}",
                                                      "status": p_r.get("status")})
                            i += 1
                        elif s["kind"] == "semantic":
                            # Literature-review pass — stage for the agent loop.
                            try:
                                prompt = session.call("prepare_semantic_step",
                                                      {"step_id": s["id"], "repo_path": repo_root})
                                report["pending_semantic"].append({
                                    "label": f"section-citations/{domain}/literature-review",
                                    "semantic_step_id": s["id"],
                                    "persist_step_id": matches[i + 1]["id"] if i + 1 < len(matches) else None,
                                    "prompt_name": prompt.get("prompt_name", ""),
                                })
                            except Exception as e:
                                report["failed"].append({"label": f"section-citations/{domain}",
                                                         "stage": "prepare_semantic", "message": str(e)})
                            i += 2
                        else:
                            i += 1
                collate_step = next((s for s in cite_steps if s["description"].startswith("Collate")), None)
                if collate_step:
                    r = session.call("run_script_step",
                                     {"step_id": collate_step["id"], "repo_path": repo_root,
                                      "input": {"paper_id": paper_id}})
                    report["ran"].append({"step": "section-citations/collate-references",
                                          "status": r.get("status")})

            # --- Phase 5c: Section supplementary content (4c) ---
            print(f"\n== section-supplementary-content ({len(domains)} domains) ==")

            def enrich_input(domain):
                return {"paper_id": paper_id, "domain": domain, "mode": "enrich"}

            run_triads_for_usecase(session, repo_root, steps, "section-supplementary-content",
                                   domains, enrich_input, report,
                                   label_prefix="section-supplementary-content")

            # --- Phase 5d: Section budget fit (4d) ---
            print(f"\n== section-budget-fit ({len(domains)} domains) ==")

            def budget_input(domain):
                return {"paper_id": paper_id, "domain": domain}

            run_triads_for_usecase(session, repo_root, steps, "section-budget-fit",
                                   domains, budget_input, report,
                                   label_prefix="section-budget-fit")

            # --- Phase 6: Deterministic audit (cheap fail-fast) ---
            print(f"\n== deterministic-audit ({len(domains)} domains) ==")

            det_failed_domains = set()

            def det_audit_input(domain):
                return {"paper_id": paper_id, "domain": domain}

            run_deterministic_triads_for_usecase(session, repo_root, steps,
                                                 "deterministic-audit", domains,
                                                 det_audit_input, report,
                                                 "deterministic-audit")

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

            # --- Phase 8: Plagiarism forensic + humanize split ---
            print(f"\n== plagiarism-forensic-audit ({len(domains)} domains) ==")

            def plagiarism_input(domain):
                return {"paper_id": paper_id, "domain": domain}

            run_triads_for_usecase(session, repo_root, steps,
                                   "plagiarism-forensic-audit",
                                   domains, plagiarism_input, report,
                                   label_prefix="plagiarism-forensic-audit",
                                   steps_per_domain=5)

            flagged_domains = set()
            for step_entry in report["ran"]:
                if (step_entry["step"].startswith("plagiarism-forensic-audit/")
                        and step_entry.get("status") != "ok"):
                    flagged_domains.add(step_entry["step"].split("/", 1)[1])

            if flagged_domains:
                print(f"\n== humanize-deterministic ({len(flagged_domains)} flagged domains) ==")

                def humanize_input(domain):
                    return {"paper_id": paper_id, "domain": domain, "iteration": 0}

                run_deterministic_triads_for_usecase(
                    session, repo_root, steps, "humanize-deterministic",
                    sorted(flagged_domains), humanize_input, report,
                    "humanize-deterministic", steps_per_domain=2,
                )

            print(f"\n== humanize-semantic (agent-driven loop for still-flagged domains) ==")
            # Still-flagged-after-deterministic domains are re-checked and
            # staged for the agent loop the same way other semantic steps
            # are — this script only stages, an agent completes them.

            # --- Phase 9: Document narrative polish + cross-section/document audit ---
            print("\n== document-narrative-polish ==")
            polish_steps = steps_of(steps, "document-narrative-polish")
            for i in range(0, len(polish_steps), 2):
                pre, sem = polish_steps[i], polish_steps[i + 1]
                stage_semantic_triad(session, repo_root, pre, sem, None,
                                     {"paper_id": paper_id}, report,
                                     label=f"document-narrative-polish/{sem['description']}")

            print("\n== cross-section-semantic-audit ==")
            xs_steps = steps_of(steps, "cross-section-semantic-audit")
            if xs_steps:
                xs_input = {"paper_id": paper_id, "scope": "cross-section"}
                stage_semantic_triad(session, repo_root,
                                     xs_steps[0], xs_steps[1], xs_steps[2],
                                     xs_input, report,
                                     label="cross-section-semantic-audit")

            print("\n== document-semantic-audit ==")
            doc_steps = steps_of(steps, "document-semantic-audit")
            if doc_steps:
                doc_input = {"paper_id": paper_id, "scope": "document"}
                stage_semantic_triad(session, repo_root,
                                     doc_steps[0], doc_steps[1], doc_steps[2],
                                     doc_input, report,
                                     label="document-semantic-audit")

        # --- Phase 10: Calculate + Render ---
        for usecase in ("calculate", "render-charts", "render-audit-report", "render-paper"):
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
        print("     (persist_step_id is null for document-narrative-polish's 3 sub-passes —")
        print("      the agent calls persist-section-draft once per domain the pass actually")
        print("      changed, since one polish call can touch multiple domains at once)")
        print(f"  (see {report_path} for every domain -> step_id mapping)")

    sys.exit(1 if report["failed"] else 0)


if __name__ == "__main__":
    main()
