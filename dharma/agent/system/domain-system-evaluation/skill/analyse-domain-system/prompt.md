# Analyse a Domain System into a normalized element list

You are given a Domain System's full captured tree. Produce a normalized,
enumerable element list plus counts, so that verifier agents can check every
element exactly once.

## Input

`domain_system` — the full tree: domains, section maps, section profiles,
epics, usecases, tasks, task steps.

## What to produce

1. `elements` — one list per artifact kind:
   - `domains`: one entry per domain, each entry resolving that domain's
     section map id and its profile set.
   - `section_maps`, `section_profiles`: every map and profile row.
   - `epics`, `usecases`, `tasks`, `task_steps`: every hierarchy row.
2. `counts` — a count per artifact kind, used for reconciliation.

## Rules

- Preserve parent links. A usecase entry carries its `epic_id`; a task entry
  carries its `usecase_id`; a task step carries its `task_id`; a section
  profile carries its owning map/domain.
- Normalize ids to a stable string form. Do not rename anything.
- Enumerate every element. Skipping an element because it looks redundant is
  an error — the verifiers rely on completeness.
- Return exactly the `{elements, counts}` shape. If a kind has no rows, emit
  an empty list — do not omit the key.

## Output shape

```json
{
  "elements": {
    "domains": [ { "id": "...", "map_id": "...", "profile_ids": ["..."] } ],
    "section_maps": [ { "id": "...", "domain_id": "..." } ],
    "section_profiles": [ { "id": "...", "domain_id": "..." } ],
    "epics": [ { "id": "..." } ],
    "usecases": [ { "id": "...", "epic_id": "..." } ],
    "tasks": [ { "id": "...", "usecase_id": "..." } ],
    "task_steps": [ { "id": "...", "task_id": "...", "required_capability": "..." } ]
  },
  "counts": { "domains": 0, "section_maps": 0, "section_profiles": 0,
              "epics": 0, "usecases": 0, "tasks": 0, "task_steps": 0 }
}
```
