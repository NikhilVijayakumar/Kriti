"""Shared phase-to-domain mapping for propose-* pipeline scripts.

Both persist_proposal.py and link_proposal_scope.py need to know which
domains each proposal phase covers.  This module is the single source
of truth for that mapping.  seed_standard.py builds its phase data from
the same constant set (see standard.yaml generate/audit/report/fix
usecases), but those live in YAML and can't be imported by scripts.

Phase → usecase suffix convention (standard.yaml):
  propose-{phase}          — gather/persist/render/approve
  persist-proposal-{phase} — same script for all phases
  approve-proposal-{phase} — same script for all phases

The generic `proposal` table uses `phase` = usecase suffix
(generation/audit/report/fix).
"""

PHASE_DOMAIN_USECASE_SUFFIXES = {
    "generation": [
        "title-and-metadata", "introduction", "methodology",
        "findings", "conclusion", "references",
    ],
    "audit": [
        "title-and-metadata", "introduction", "methodology",
        "findings", "conclusion", "references",
        "novelty", "gaps", "mathematics", "reviewer-simulation",
    ],
    "report": ["paper"],
    "fix": [],  # scoped by scope_domain_id, not phase-wide
}

PHASE_STANDARD_SUFFIXES = {
    "generation": "generation",
    "audit": "audit",
    "report": "report",
    "fix": "fix",
}


def get_phase_domain_keys(phase):
    """Return the domain key list for a proposal phase."""
    return list(PHASE_DOMAIN_USECASE_SUFFIXES.get(phase, []))


def get_standard_suffix(phase):
    """Return the DB-standard suffix for a phase."""
    return PHASE_STANDARD_SUFFIXES.get(phase, phase)
