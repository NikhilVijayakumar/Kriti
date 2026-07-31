import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
from _adapter import parse_step_args, write_envelope

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "common" / "script"))
import academic_schema

import yaml

_METADATA_PATH = os.path.normpath(os.path.join(
    os.path.dirname(__file__), "..", "templates", "metadata.yaml"))

def main():
    repo_root, db_path, payload, out_path = parse_step_args()
    paper_id = payload["paper_id"]
    conn = academic_schema.get_conn(db_path)
    try:
        row = conn.execute(
            "SELECT 1 FROM academic_proposal_review "
            "WHERE paper_id=? AND phase='input' AND is_latest=1 AND review_status='approved' "
            "LIMIT 1", (paper_id,)).fetchone()
        if not row:
            write_envelope(out_path, status="error",
                           message="no approved input proposal — run propose-input + approve first")
            return

        if not os.path.isfile(_METADATA_PATH):
            write_envelope(out_path, status="error",
                           message=f"metadata file not found: {_METADATA_PATH}")
            return

        with open(_METADATA_PATH, encoding="utf-8") as f:
            meta = yaml.safe_load(f)
        if not isinstance(meta, dict):
            write_envelope(out_path, status="error",
                           message="metadata.yaml is empty or invalid")
            return

        modules = meta.get("modules", {})
        registered = []
        sort_order = 0

        primary = modules.get("primary", {})
        if isinstance(primary, dict) and primary.get("name"):
            mod = academic_schema.upsert_module(
                conn, paper_id,
                module_name=primary["name"],
                module_path=primary.get("path", ""),
                sort_order=sort_order,
                role="primary",
                interest_weight=primary.get("interest_weight", 1.0),
                existing_draft_publisher=primary.get("existing_draft", {}).get("publisher", ""),
                existing_draft_status=primary.get("existing_draft", {}).get("status", "draft"),
                existing_draft_path=primary.get("existing_draft", {}).get("draft", ""),
            )
            registered.append(primary["name"])
            sort_order += 1

        dependent = modules.get("dependent", [])
        if isinstance(dependent, list):
            for dep in dependent:
                if not isinstance(dep, dict) or not dep.get("name"):
                    continue
                mod = academic_schema.upsert_module(
                    conn, paper_id,
                    module_name=dep["name"],
                    module_path=dep.get("path", ""),
                    sort_order=sort_order,
                    role="dependent",
                    interest_weight=dep.get("interest_weight", 0.5),
                    reason=dep.get("reason", ""),
                )
                registered.append(dep["name"])
                sort_order += 1

        cross_library = modules.get("cross_library", "")
        if cross_library:
            mod = academic_schema.upsert_module(
                conn, paper_id,
                module_name="cross_library",
                module_path=cross_library,
                sort_order=sort_order,
                role="cross_library",
            )
            registered.append("cross_library")
            sort_order += 1

    finally:
        conn.close()

    write_envelope(out_path, status="ok",
                   message=f"committed {len(registered)} modules from metadata.yaml: {', '.join(registered)}",
                   modules=registered, count=len(registered))

if __name__ == "__main__":
    main()
