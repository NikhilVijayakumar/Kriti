"""deterministic_fingerprint_check.py — mechanical plagiarism pre-screen.
Computes burstiness (sentence-length variance), n-gram repetition ratio,
and checks a banned-phrase list. Records deterministic findings in
academic_plagiarism_findings with check_kind='deterministic'.
"""
import json
import math
import os
import re
import sys
from collections import Counter
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402

# Default banned phrases — AI-fingerprint patterns
BANNED_PHRASES = [
    r"\bin this paper\b", r"\bwe propose\b", r"\bour approach\b",
    r"\bit is worth noting\b", r"\bin conclusion\b",
    r"\bfurthermore\b", r"\bmoreover\b", r"\bhowever\b",
    r"\bthe results demonstrate\b", r"\bas shown in\b",
    r"\bthis paper presents\b", r"\ba comprehensive\b",
    r"\bleveraging\b", r"\bseamlessly\b", r"\brobust\b",
    r"\bcutting.edge\b", r"\bstate.of.the.art\b",
    r"\bpivotal\b", r"\bunprecedented\b",
]

DEFAULT_MIN_BURSTINESS = 0.3
DEFAULT_MAX_NGRAM_REPEAT = 0.15
DEFAULT_MAX_BANNED_PHRASES = 3


def _split_sentences(text):
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]


def _compute_burstiness(text):
    """Compute burstiness as coefficient of variation of sentence lengths.
    Higher burstiness = more varied sentence lengths = more human-like."""
    sentences = _split_sentences(text)
    if len(sentences) < 3:
        return 0.0
    lengths = [len(re.findall(r'\S+', s)) for s in sentences]
    mean = sum(lengths) / len(lengths)
    if mean == 0:
        return 0.0
    variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
    return math.sqrt(variance) / mean


def _compute_ngram_repetition(text, n=3):
    """Compute ratio of repeated n-grams to total n-grams.
    Higher ratio = more repetitive = more AI-like."""
    words = re.findall(r'\S+', text.lower())
    if len(words) < n:
        return 0.0
    ngrams = [tuple(words[i:i+n]) for i in range(len(words) - n + 1)]
    counts = Counter(ngrams)
    repeated = sum(c for c in counts.values() if c > 1)
    return repeated / len(ngrams) if ngrams else 0.0


def _count_banned_phrases(text, phrases=None):
    """Count occurrences of banned AI-fingerprint phrases."""
    phrases = phrases or BANNED_PHRASES
    text_lower = text.lower()
    matches = []
    for phrase in phrases:
        found = re.findall(phrase, text_lower)
        if found:
            matches.append({"phrase": phrase, "count": len(found)})
    return matches


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload.get("paper_id")
    domain = payload.get("domain")

    if not paper_id or not domain:
        write_envelope(out_path, status="error",
                       message="missing paper_id or domain in input")
        return

    conn = academic_schema.get_conn(db_path)
    try:
        # Get the latest draft for this domain
        narrative = academic_schema.get_narrative(conn, paper_id, domain)
        if not narrative:
            write_envelope(out_path, status="error",
                           message=f"no draft found for {domain}")
            return

        text = "\n\n".join(s.get("text", "") for s in narrative)
        if not text.strip():
            write_envelope(out_path, status="error",
                           message=f"empty draft for {domain}")
            return

        # Compute metrics
        burstiness = _compute_burstiness(text)
        ngram_repeat = _compute_ngram_repetition(text)
        banned = _count_banned_phrases(text)

        # Determine pass/fail per check
        findings = []
        all_passed = True

        # Burstiness check
        burst_pass = burstiness >= DEFAULT_MIN_BURSTINESS
        findings.append({
            "check_id": "fp-burstiness",
            "rule": "burstiness",
            "passed": burst_pass,
            "detail": f"burstiness={burstiness:.3f} (min={DEFAULT_MIN_BURSTINESS})",
            "severity": "warning" if burst_pass else "critical",
            "value": burstiness,
        })
        if not burst_pass:
            all_passed = False

        # N-gram repetition check
        ngram_pass = ngram_repeat <= DEFAULT_MAX_NGRAM_REPEAT
        findings.append({
            "check_id": "fp-ngram-repeat",
            "rule": "ngram_repetition",
            "passed": ngram_pass,
            "detail": f"ngram_repeat={ngram_repeat:.3f} (max={DEFAULT_MAX_NGRAM_REPEAT})",
            "severity": "warning" if ngram_pass else "critical",
            "value": ngram_repeat,
        })
        if not ngram_pass:
            all_passed = False

        # Banned phrases check
        banned_count = sum(m["count"] for m in banned)
        banned_pass = banned_count <= DEFAULT_MAX_BANNED_PHRASES
        findings.append({
            "check_id": "fp-banned-phrases",
            "rule": "banned_phrases",
            "passed": banned_pass,
            "detail": f"{banned_count} banned phrases found (max={DEFAULT_MAX_BANNED_PHRASES})",
            "severity": "warning" if banned_pass else "critical",
            "matches": banned,
        })
        if not banned_pass:
            all_passed = False

        verdict = "PASS" if all_passed else "FAIL"

        # Get latest run number for this domain and increment
        domain_id = academic_schema.get_domain_id(conn, domain)
        max_run = conn.execute(
            "SELECT COALESCE(MAX(run_number), 0) FROM academic_plagiarism_findings "
            "WHERE paper_id=? AND domain_id=? AND pass_type='forensic'",
            (paper_id, domain_id),
        ).fetchone()[0]

        # Record deterministic fingerprint findings
        academic_schema.upsert_plagiarism_finding(
            conn, paper_id, domain, max_run + 1, verdict,
            flagged_spans=findings, model="deterministic-fingerprint",
            pass_type="forensic", check_kind="deterministic",
        )

        # Flag high-severity items as spans for semantic audit to examine
        flagged_spans = []
        for f in findings:
            if not f["passed"]:
                flagged_spans.append({
                    "check_id": f["check_id"],
                    "detail": f["detail"],
                    "severity": f["severity"],
                })

        write_envelope(out_path, status="ok",
                       message=f"fingerprint check {domain}: {verdict}",
                       verdict=verdict, findings=findings,
                       flagged_spans=flagged_spans,
                       burstiness=burstiness,
                       ngram_repetition=ngram_repeat,
                       banned_phrases=banned)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
