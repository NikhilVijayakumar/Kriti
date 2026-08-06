```toml
[system]
id = "domain-system-evaluation"
concern = "domain-system-evaluation"
is_privileged_request = false
scenarios = ["verify-domain-system"]
```

# domain-system-evaluation — Agent System

Analyses a Domain System as an artifact. It verifies the Domain System end to
end — every domain, Section Map, Section Profile, Epic, Usecase, Task, and
Task-Step, plus the system as a whole. It reads Domain Systems;
it never writes to one.

## Scenarios

- **Scenario A — verify the Domain System.** Check and validate a Domain
  System as declared content. The job is bounded and enumerable: each element
  is checked against the model the Domain System must satisfy, and every
  verdict carries evidence. Output is a per-domain + system-level verification
  report that tags each failed check `defect` or `gap`.

## Skills policy

Every skill in this Agent System is analysis-only. The system produces
reports and finding lists; no skill is effect-capable and none
mutates the Domain System or an Agent System it analyses. No agent or skill
names a specific repository or Domain System.
