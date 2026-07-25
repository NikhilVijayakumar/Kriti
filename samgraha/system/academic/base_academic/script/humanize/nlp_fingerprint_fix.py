"""nlp_fingerprint_fix.py — deterministic Layer 1 humanize pass.
Applies mechanical AI-fingerprint fixes using NLP-library-style rules:
sentence-length variance normalization, parallel-structure breaking,
paragraph-length variation.

Expected --in payload: {paper_id: int, domain: str, iteration: int,
  sections: [{heading: str, text: str}], model: str}
"""
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parent.parent / "common"))
from _adapter import parse_step_args, write_envelope, SCRIPTS_DIR
import sys
import re
import random

sys.path.insert(0, str(SCRIPTS_DIR / "common"))
import academic_schema  # noqa: E402


def _split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())


def _fix_sentence_variance(sentences):
    if len(sentences) < 3:
        return sentences
    lengths = [len(s.split()) for s in sentences]
    avg = sum(lengths) / len(lengths)
    result = []
    for i, s in enumerate(sentences):
        wc = lengths[i]
        if i % 3 == 0 and wc > avg * 1.5:
            words = s.split()
            mid = len(words) // 2
            s = " ".join(words[:mid]) + ". " + " ".join(words[mid:])
        result.append(s)
    return result


def _break_parallel_structure(text):
    patterns = [
        (r'\b(First|Second|Third|Fourth|Fifth)\b,', ''),
        (r'\b(It is .+ that\b)', ''),
        (r'\b(The .+ is .+\. The .+ is .+\. The .+ is)\b', ''),
    ]
    result = text
    for pattern, repl in patterns:
        if random.random() < 0.3:
            result = re.sub(pattern, repl, result, count=1)
    return result


def _vary_paragraph_length(paragraphs):
    if len(paragraphs) < 2:
        return paragraphs
    result = []
    for i, p in enumerate(paragraphs):
        sentences = _split_sentences(p)
        if len(sentences) > 4 and i % 2 == 0:
            mid = len(sentences) // 2
            result.append(" ".join(sentences[:mid]))
            result.append(" ".join(sentences[mid:]))
        else:
            result.append(p)
    return result


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    domain = payload["domain"]
    iteration = payload.get("iteration", 0)
    sections = payload.get("sections", [])
    model = payload.get("model", "nlp_fingerprint_fix")

    fixed_sections = []
    changes = []
    for sec in sections:
        text = sec.get("text", "")
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        new_paragraphs = _vary_paragraph_length(paragraphs)
        new_text_parts = []
        for p in new_paragraphs:
            sentences = _split_sentences(p)
            sentences = _fix_sentence_variance(sentences)
            p_joined = " ".join(sentences)
            p_joined = _break_parallel_structure(p_joined)
            new_text_parts.append(p_joined)

        new_text = "\n\n".join(new_text_parts)
        if new_text != text:
            changes.append(f"fixed structure in '{sec.get('heading', '')}'")
        fixed_sections.append({"heading": sec.get("heading", ""), "text": new_text})

    risk_flags = [] if not changes else [f"NLP mechanical fixes applied: {len(changes)} sections"]

    conn = academic_schema.get_conn(db_path)
    try:
        academic_schema.upsert_humanize_pass(
            conn, paper_id, domain, iteration,
            change_summary=f"Layer 1 NLP fixes: {len(changes)} sections modified",
            risk_flags=risk_flags, model=model, pass_kind="deterministic",
        )
        academic_schema.upsert_narrative(
            conn, paper_id, domain, fixed_sections,
            stage="humanize", iteration=iteration, model=model,
        )
    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"NLP fingerprint fix: {len(changes)} sections modified for {domain}",
                   paper_id=paper_id, domain=domain, iteration=iteration,
                   sections_changed=len(changes))


if __name__ == "__main__":
    main()
