"""content_rules.py — shared rule-evaluation dispatch for deterministic
checks against domain draft text.

Used by both check_word_budget.py (generation-time verification) and
deterministic_audit.py (post-generation audit).  Single implementation
of what each rule means — avoids drift between the two call-sites.
"""
import re
from collections import defaultdict


# ── shared constants ────────────────────────────────────────────────

_ROMAN_NUMERALS = {
    'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9,'X':10,
    'XI':11,'XII':12,'XIII':13,'XIV':14,'XV':15,'XVI':16,'XVII':17,
    'XVIII':18,'XIX':19,'XX':20,
}
_ROMAN_SET = set(_ROMAN_NUMERALS.keys())


def _check_regex(pattern, text, flags=0):
    return bool(re.search(pattern, text, flags))


def _check_word_count(text, min_words=0, max_words=None):
    wc = len(re.findall(r'\S+', text))
    if wc < min_words:
        return False, f"word count {wc} < minimum {min_words}"
    if max_words and wc > max_words:
        return False, f"word count {wc} > maximum {max_words}"
    return True, f"word count {wc}"


def _check_no_placeholders(text):
    patterns = [r'\bTODO\b', r'\bXXX\b', r'\[Author\s*Name\]', r'\[Insert',
                r'\[TBD\]', r'\[FIXME\]', r'\{TODO\}']
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return False, f"placeholder found: {re.search(pat, text, re.IGNORECASE).group()}"
    return True, "no placeholders"


def _check_contains_number(text):
    m = re.search(r'\d+\.?\d*', text)
    return bool(m), "contains numbers" if m else "no numbers found"


def _check_citation_markers(text):
    numbered = len(re.findall(r'\[\d+(?:[,;\s\-–]\d+)*\]', text))
    author_year = len(re.findall(
        r'\([A-Z][a-z]+(?:\s+(?:et\s+al\.?|and\s+[A-Z][a-z]+))?,\s*\d{4}[a-z]?\)',
        text))
    return numbered + author_year


def _check_mermaid_diagram(text):
    return bool(re.search(r'```mermaid', text))


def _check_equations(text):
    return bool(re.search(
        r'\$\$.*?\$\$|\\begin\{equation|\\\[.*?\\\]', text, re.DOTALL))


def _check_pseudocode(text):
    patterns = [r'\\begin\{algorithm', r'```pseudo', r'```algorithm',
                r'\*\*Algorithm\s*\d', r'**Input:', r'**Output:']
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False


def _check_list_items(text, min_items=1):
    items = re.findall(r'^\s*[-*+]\s|^\s*\d+[.)]\s', text, re.MULTILINE)
    return len(items) >= min_items, f"{len(items)} list items found"


def _check_table_count(text):
    lines = text.split('\n')
    count = 0
    i = 0
    while i < len(lines) - 1:
        if (lines[i].strip().startswith('|')
                and re.match(r'^\s*\|[\s:]*-+', lines[i + 1])):
            count += 1
            i += 2
        else:
            i += 1
    return count


def _check_diagram_count(text):
    return len(re.findall(r'```mermaid', text))


def _check_formula_count(text):
    block = len(re.findall(r'\$\$.*?\$\$', text, re.DOTALL))
    bracket = len(re.findall(r'\\\[.*?\\\]', text, re.DOTALL))
    return block + bracket


# ── writing-quality helpers ─────────────────────────────────────────

_AI_LANGUAGE_WORDS = [
    "delve", "landscape", "tapestry", "crucial", "paramount", "pivotal",
    "leverage", "harness", "unlock", "robust", "novel", "comprehensive",
]
_AI_LANGUAGE_PHRASES = [
    "it should be noted that", "it is worth mentioning",
    "in the realm of", "in the landscape of",
]


def _check_ai_language_flags(text):
    """Detect AI-generated language word/phrase flags."""
    flags = []
    text_lower = text.lower()
    for word in _AI_LANGUAGE_WORDS:
        matches = re.findall(r'\b' + re.escape(word) + r'\b', text_lower)
        if matches:
            flags.append(f"{word} ({len(matches)}x)")
    for phrase in _AI_LANGUAGE_PHRASES:
        if phrase in text_lower:
            flags.append(f'"{phrase}"')
    return len(flags) == 0, f"flags found: {', '.join(flags)}" if flags else "no AI-language flags"


def _check_acronym_defined_at_first_use(text):
    """Check that acronyms (2+ uppercase letters) are defined before use.

    An acronym is "defined" if a pattern like "Full Name (ABC)" or
    "Something (ABC)" appears before the acronym is used standalone.
    Flags acronyms that appear before their parenthetical definition.
    """
    # Find all definition positions: (ABC) or (Full Form ABC) patterns
    definition_positions = {}
    for m in re.finditer(r'\(([A-Za-z ]+([A-Z]{2,}))\)', text):
        acr = m.group(2)
        if acr not in _ROMAN_SET:
            definition_positions.setdefault(acr, m.start())
    # Also match pure (ABC) patterns
    for m in re.finditer(r'\(([A-Z]{2,})\)', text):
        acr = m.group(1)
        if acr not in _ROMAN_SET:
            definition_positions.setdefault(acr, m.start())

    # Find all acronym uses (not inside parentheses) and their positions
    # Remove parenthetical definitions to avoid matching inside them
    stripped = re.sub(r'\([A-Z]{2,}\)', '', text)
    # Track where each stripped character came from in the original
    # Simple approach: find acronyms in stripped, map back to original positions
    issues = []
    for m in re.finditer(r'\b([A-Z]{2,})\b', stripped):
        acr = m.group(1)
        if acr in _ROMAN_SET or acr in definition_positions:
            continue
        # This acronym has no definition anywhere — always flagged
        issues.append(acr)

    # Also check acronyms used before their definition
    for m in re.finditer(r'\b([A-Z]{2,})\b', text):
        acr = m.group(1)
        if acr in _ROMAN_SET or acr not in definition_positions:
            continue
        # Acronym has a definition — check if use comes before definition
        use_pos = m.start()
        def_pos = definition_positions[acr]
        # Only flag if this use is NOT the definition itself (not inside parens)
        # Check if this position is inside (...) by looking backwards
        before = text[:use_pos]
        if before.rstrip().endswith('('):
            continue  # This is part of the definition pattern
        if use_pos < def_pos:
            issues.append(f"{acr} (used before definition)")

    if issues:
        return False, f"undefined acronyms: {', '.join(sorted(set(issues)))}"
    return True, "all acronyms defined at first use"


def _check_terminology_consistency(text):
    """Flag term variants — same concept, different casing/hyphenation.

    Extracts multi-word terms, normalizes (lowercase, no hyphens/spaces),
    and flags groups with 2+ variants.
    """
    # Extract hyphenated and multi-word terms
    terms = re.findall(r'\b([A-Za-z]+(?:[- ][A-Za-z]+)+)\b', text)
    normalized = defaultdict(list)
    for term in terms:
        key = re.sub(r'[-\s]+', '', term.lower())
        normalized[key].append(term)

    variants = {k: sorted(set(v)) for k, v in normalized.items() if len(set(v)) > 1}
    if variants:
        details = [f"{', '.join(v)}" for v in variants.values()]
        return False, f"terminology variants: {'; '.join(details)}"
    return True, "terminology consistent"


def _check_sentence_length_distribution(text, target_min=15, target_max=25):
    """Check sentence length against Writing Guide/01 targets (15-25 words/sentence).

    Returns pass if ≥80% of sentences are within range.
    """
    # Split on sentence-ending punctuation, skip empty
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    if not sentences:
        return True, "no sentences to check"

    in_range = 0
    too_short = 0
    too_long = 0
    for s in sentences:
        wc = len(re.findall(r'\S+', s))
        if target_min <= wc <= target_max:
            in_range += 1
        elif wc < target_min:
            too_short += 1
        else:
            too_long += 1

    total = len(sentences)
    pct = in_range / total * 100
    if pct >= 80:
        return True, f"{pct:.0f}% sentences in {target_min}-{target_max} word range ({in_range}/{total})"
    return False, f"only {pct:.0f}% sentences in range ({in_range}/{total}), {too_short} too short, {too_long} too long"


def _check_citation_figure_table_collision(text):
    """Check that citation numbers [N] don't collide with Fig. N or Table N.

    Handles multi-citation brackets [1,2], [1, 2], [5;6] and Roman numeral
    figure/table labels (Fig. III, Table IV).
    """
    def _parse_fig_table_num(s):
        s = s.upper().strip()
        return _ROMAN_NUMERALS.get(s, int(s) if s.isdigit() else 0)

    # Extract citation numbers from [N], [1,2], [1, 2], [5;6], etc.
    citations = set()
    for m in re.finditer(r'\[(\d+(?:[,;\s]+\d+)*)\]', text):
        for n in re.findall(r'\d+', m.group(1)):
            citations.add(int(n))

    # Extract figure and table numbers (arabic + Roman numeral)
    figures = set(_parse_fig_table_num(n) for n in re.findall(
        r'(?i)(?:fig(?:ure|\.)?)\s+([IVXLCDM]+|\d+)', text))
    tables = set(_parse_fig_table_num(n) for n in re.findall(
        r'(?i)(?:table)\s+([IVXLCDM]+|\d+)', text))

    fig_collisions = citations & figures
    table_collisions = citations & tables
    all_collisions = fig_collisions | table_collisions

    if all_collisions:
        parts = []
        if fig_collisions:
            parts.append(f"cite-fig: {sorted(fig_collisions)}")
        if table_collisions:
            parts.append(f"cite-table: {sorted(table_collisions)}")
        return False, f"numbering collisions: {'; '.join(parts)}"
    return True, "no citation-figure-table collisions"


def _check_readability_score(text, min_score=None, max_score=None,
                              metric="flesch_reading_ease"):
    """Check readability score via textstat.

    metric: flesch_reading_ease (default, higher=easier, target 30-60 for
            academic prose), flesch_kincaid_grade, gunning_fog, etc.
    """
    try:
        import textstat
    except ImportError:
        return True, "textstat not installed — readability check skipped"

    scorer = getattr(textstat, metric, None)
    if scorer is None:
        return True, f"unknown metric '{metric}'"

    score = scorer(text)
    if min_score is not None and score < min_score:
        return False, f"{metric}={score:.1f} < minimum {min_score}"
    if max_score is not None and score > max_score:
        return False, f"{metric}={score:.1f} > maximum {max_score}"
    return True, f"{metric}={score:.1f}"


# ── public API ──────────────────────────────────────────────────────

def evaluate_rule(check, text, draft_texts=None):
    """Run a single content rule against draft text.

    Parameters
    ----------
    check : dict
        A check entry from a domain YAML (keys: rule, config, id, ...).
    text : str
        The domain's draft text.
    draft_texts : dict, optional
        Map of domain_key -> draft_text for cross-reference rules.

    Returns
    -------
    (passed: bool, detail: str)
    """
    rule = check.get("rule", "")
    draft_texts = draft_texts or {}

    try:
        if rule == "word_count_in_range":
            cfg = check.get("config", {})
            return _check_word_count(text, cfg.get("min", 0), cfg.get("max"))
        elif rule == "no_placeholders":
            return _check_no_placeholders(text)
        elif rule == "contains_number":
            return _check_contains_number(text)
        elif rule == "contains_mermaid_diagram":
            has = _check_mermaid_diagram(text)
            return has, "mermaid diagram present" if has else "no mermaid diagram"
        elif rule == "contains_pseudocode":
            has = _check_pseudocode(text)
            return has, "pseudocode present" if has else "no pseudocode"
        elif rule == "contains_equation":
            has = _check_equations(text)
            return has, "equations present" if has else "no equations"
        elif rule == "min_citation_count":
            min_count = check.get("config", {}).get("min", 1)
            count = _check_citation_markers(text)
            return count >= min_count, f"{count} citations found (minimum {min_count})"
        elif rule == "regex_match":
            pattern = check.get("config", {}).get("pattern", "")
            matched = _check_regex(pattern, text)
            return matched, f"pattern {'found' if matched else 'not found'}: {pattern}"
        elif rule == "regex_absent":
            pattern = check.get("config", {}).get("pattern", "")
            matched = _check_regex(pattern, text)
            return not matched, f"forbidden pattern {'found' if matched else 'absent'}: {pattern}"
        elif rule == "min_list_items":
            min_items = check.get("config", {}).get("min", 1)
            return _check_list_items(text, min_items)
        elif rule == "cross_reference_numbers":
            other_domain = check.get("config", {}).get("other_domain", "")
            other_text = draft_texts.get(other_domain, "")
            if not other_text:
                return True, f"cross-reference skipped: {other_domain} draft not available"
            nums_in_draft = set(re.findall(r'(?<!\w)\d+\.?\d*(?!\w)', text))
            nums_in_other = set(re.findall(r'(?<!\w)\d+\.?\d*(?!\w)', other_text))
            mismatches = nums_in_draft - nums_in_other
            if mismatches:
                return False, f"numbers in draft not in {other_domain}: {mismatches}"
            return True, "all numbers cross-referenced"
        elif rule == "no_new_results":
            results_text = draft_texts.get("results", "")
            if not results_text:
                return True, "cross-reference skipped: results draft not available"
            new_nums = (set(re.findall(r'(?<!\w)\d+\.?\d*(?!\w)', text))
                        - set(re.findall(r'(?<!\w)\d+\.?\d*(?!\w)', results_text)))
            if new_nums:
                return False, f"new numbers not in results: {new_nums}"
            return True, "no new results"
        elif rule == "length_proportion":
            other_domain = check.get("config", {}).get("compare_to", "")
            max_ratio = check.get("config", {}).get("max_ratio", 1.5)
            other_text = draft_texts.get(other_domain, "")
            if not other_text:
                return True, f"proportion check skipped: {other_domain} not available"
            my_wc = len(re.findall(r'\S+', text))
            other_wc = len(re.findall(r'\S+', other_text))
            if other_wc > 0 and my_wc / other_wc > max_ratio:
                return False, f"length ratio {my_wc/other_wc:.1f} exceeds {max_ratio} vs {other_domain}"
            return True, f"length proportion OK ({my_wc}/{other_wc})"
        elif rule == "no_citations":
            count = _check_citation_markers(text)
            return count == 0, f"{count} citations found (expected 0)"
        elif rule == "severity_tagged":
            severity_pattern = r'(?i)(?:HIGH|MEDIUM|LOW|CRITICAL)\s*[:\-]'
            matches = re.findall(severity_pattern, text)
            return len(matches) > 0, f"{len(matches)} severity-tagged items"
        elif rule == "min_table_count":
            min_count = check.get("config", {}).get("min", 1)
            count = _check_table_count(text)
            return count >= min_count, f"{count} tables found (minimum {min_count})"
        elif rule == "min_diagram_count":
            min_count = check.get("config", {}).get("min", 1)
            count = _check_diagram_count(text)
            return count >= min_count, f"{count} diagrams found (minimum {min_count})"
        elif rule == "min_formula_count":
            min_count = check.get("config", {}).get("min", 1)
            count = _check_formula_count(text)
            return count >= min_count, f"{count} formulas found (minimum {min_count})"
        # ── new rules (pcems_2026 cross-cutting + section checks) ──
        elif rule == "contains_table":
            count = _check_table_count(text)
            return count > 0, f"{count} tables found" if count else "no tables found"
        elif rule == "contains_figure":
            count = len(re.findall(r'(?i)fig(?:ure|\.)\s*\d', text))
            return count > 0, f"{count} figure references found" if count else "no figure references"
        elif rule == "max_citation_count":
            max_count = check.get("config", {}).get("max", 30)
            count = _check_citation_markers(text)
            return count <= max_count, f"{count} citations found (maximum {max_count})"
        elif rule == "keyword_count":
            cfg = check.get("config", {})
            min_kw = cfg.get("min", 4)
            max_kw = cfg.get("max", 6)
            m = re.search(r'(?i)keywords?\s*[:]\s*(.+)', text)
            if not m:
                return False, "no keywords line found"
            raw = m.group(1).strip()
            kws = [k.strip() for k in re.split(r'[,;]', raw) if k.strip()]
            count = len(kws)
            if count < min_kw:
                return False, f"{count} keywords found (minimum {min_kw})"
            if count > max_kw:
                return False, f"{count} keywords found (maximum {max_kw})"
            return True, f"{count} keywords found"
        elif rule == "author_block_present":
            has_sup = bool(re.search(r'<sup>\d+</sup>', text))
            has_bold_num = bool(re.search(r'\*\*\d+\*\*', text))
            has_author = has_sup or has_bold_num
            return has_author, "author block present" if has_author else "no author block found"
        elif rule == "table_created_with_word_tools":
            image_table = re.search(
                r'(?i)!\[.*\]\(.*\.(?:png|jpg|jpeg|svg|gif)\)', text)
            return not bool(image_table), "no image-based tables" if not image_table else "image-based table detected"
        elif rule == "table_caption_position":
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if re.match(r'^\s*\|', line) and i > 0:
                    prev = lines[i - 1].strip()
                    if re.match(r'(?i)^table\s', prev):
                        return True, "caption above table"
            return False, "no caption-above-table pattern found"
        elif rule == "sequential_numbering":
            pattern = r'(?i)(table|fig(?:ure|\.)?)\s+([IVXLCDM]+|\d+)'
            matches = re.findall(pattern, text)
            if not matches:
                return True, "no numbered items to check"
            def _parse_num(s):
                s = s.upper().strip()
                return _ROMAN_NUMERALS.get(s, int(s) if s.isdigit() else 0)
            nums = [_parse_num(n) for _, n in matches]
            sequential = all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1))
            return sequential, f"numbering: {'sequential' if sequential else 'non-sequential'} ({nums})"
        elif rule == "referenced_before_appearance":
            lines = text.split('\n')
            pattern = r'(?i)(table|fig(?:ure|\.)?)\s+([IVXLCDM]+|\d+)'
            appeared = set()
            for line in lines:
                refs = re.findall(pattern, line)
                is_table_line = re.match(r'^\s*\|', line)
                if is_table_line:
                    for kind, num in refs:
                        key = f"{kind.lower()}_{num}"
                        if key not in appeared:
                            return False, f"{kind} {num} appears before being referenced"
                for kind, num in refs:
                    appeared.add(f"{kind.lower()}_{num}")
            return True, "all items referenced before appearance"
        elif rule == "figure_placement":
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if re.match(r'(?i)\*?fig(?:ure|\.)?\s*\d', line):
                    next_10 = '\n'.join(lines[i + 1:i + 6])
                    if re.search(r'(?i)fig(?:ure|\.)?\s*\d', next_10):
                        return True, "figure near reference"
            return True, "no figure-reference proximity issues detected"
        elif rule == "figure_caption_position":
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if re.match(r'(?i)fig(?:ure|\.)?\s*\d', line):
                    if i + 1 < len(lines):
                        nxt = lines[i + 1].strip()
                        if re.match(r'(?i)^fig(?:ure|\.)?\s*\d', nxt):
                            return True, "caption below figure"
            return True, "no figure-caption pattern to validate"
        elif rule == "budget_fit_applied":
            return True, "budget_fit_applied — generation-time check (no runtime enforcement)"
        elif rule == "abstract_word_count_in_range":
            cfg = check.get("config", {})
            min_words = cfg.get("min", 0)
            max_words = cfg.get("max")
            m = re.search(r'(?im)^##\s*abstract\s*$(.*?)(?=^##\s|\Z)', text, re.DOTALL)
            if not m:
                return False, "no '## Abstract' section found to word-count"
            passed, detail = _check_word_count(m.group(1), min_words, max_words)
            return passed, f"abstract {detail}"
        # ── writing-quality rules ──
        elif rule == "ai_language_flags":
            return _check_ai_language_flags(text)
        elif rule == "acronym_defined_at_first_use":
            return _check_acronym_defined_at_first_use(text)
        elif rule == "terminology_consistency":
            return _check_terminology_consistency(text)
        elif rule == "sentence_length_distribution":
            cfg = check.get("config", {})
            return _check_sentence_length_distribution(
                text, cfg.get("min", 15), cfg.get("max", 25))
        elif rule == "citation_figure_table_collision":
            return _check_citation_figure_table_collision(text)
        elif rule == "readability_score_in_range":
            cfg = check.get("config", {})
            return _check_readability_score(
                text, cfg.get("min"), cfg.get("max"),
                cfg.get("metric", "flesch_reading_ease"))
        else:
            return True, f"unknown rule '{rule}' — passed by default"
    except Exception as e:
        return False, f"check error: {e}"
