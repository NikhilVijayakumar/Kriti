"""archive_proposal.py — moves a rendered proposal out of the active
proposal output tree once its implementation is complete.

Expected --in payload: {paper_id: int, phase: str}
(phase is generation/audit/fix/report — the proposal category)

Matches render_proposal.py's Proposal 17 step-named output layout:
source: .samgraha/output/{step}/proposal/{phase}/paper-{id}/
dest:   .samgraha/output/{step}/proposal/archive/{phase}/paper-{id}/
"""
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _adapter import parse_step_args, write_envelope  # noqa: E402


_PHASE_TO_STEP_DIR = {
    "input": "step0-extract",
    "map": "step0-extract",
    "section": "step1-draft-for-completeness",
    "audit": "step1-draft-for-completeness",
    "fix": "step1-draft-for-completeness",
    "report": "step4-final-render",
}


def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    phase = payload["phase"]
    step_dir = _PHASE_TO_STEP_DIR.get(phase, "step1-draft-for-completeness")

    src = repo_root / ".samgraha" / "output" / step_dir / "proposal" / phase / f"paper-{paper_id}"
    if not src.is_dir():
        write_envelope(out_path, status="error",
                       message=f"no proposal output at {src}")
        return

    dest_parent = repo_root / ".samgraha" / "output" / step_dir / "proposal" / "archive" / phase
    dest_parent.mkdir(parents=True, exist_ok=True)
    dest = dest_parent / f"paper-{paper_id}"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.move(str(src), str(dest))

    write_envelope(out_path, status="ok",
                   message=f"archived {phase} proposal for paper {paper_id}",
                   archived_to=str(dest))


if __name__ == "__main__":
    main()
