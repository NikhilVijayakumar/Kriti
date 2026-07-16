# Visual Testing — Generation Template

> **Domain:** qa
> **Section:** visual_testing
> **Source:** `documentation-standards/12-qa-standards.md` §Visual Testing
> **Relationships:** `audit/deterministic/document/qa-relationships.yaml`

Generates visual testing configuration including screenshot baselines, Storybook visual diffs, and CI gate setup.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| validates | implementation/component_output | Visual regressions must be caught before merge |

## Template

```markdown
# Visual Testing: [FeatureName]

## Screenshot Testing Setup

- [ ] Storybook visual diff configured
- [ ] Baseline screenshots generated
- [ ] Viewport sizes defined: mobile (375px), tablet (768px), desktop (1280px)
- [ ] Color scheme variants: light, dark

## Storybook Visual Diff

```bash
npx storybook:visual-detect --baseline-dir ./screenshots/baseline
```

- [ ] Per-component screenshot comparison
- [ ] Pixel threshold set (max 0.1% diff)
- [ ] Anti-aliasing tolerance configured

## CI Gate Configuration

```yaml
visual-test:
  stage: verification
  script:
    - npm run test:visual
    - npm run test:visual:compare
  artifacts:
    paths:
      - screenshots/diff/
  allow_failure: false
```

## Baseline Management

- [ ] Baselines stored in version control
- [ ] Update script: `npm run test:visual:update`
- [ ] Review workflow for baseline changes documented
```

## Examples

**Correct:**
> `Button` component has visual baselines for all 5 variants across 3 viewports, CI rejects diffs >0.1%, and baseline updates require PR review.

**Incorrect:**
> Visual tests run only on desktop viewport with a 5% threshold and no baseline review process.
> *Why wrong: Insufficient viewport coverage, threshold too permissive, no governance on baseline updates.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** configuration-driven
- **Audience:** QA engineer
- **Do:** Define exact viewport sizes, set strict pixel thresholds, version-control baselines.
- **Don't:** Allow large diff thresholds, skip mobile/tablet viewports, auto-merge baseline changes.

**Required subsections:** Screenshot Testing Setup, Storybook Visual Diff, CI Gate Configuration, Baseline Management
**Optional subsections:** Animation Testing, Responsive Breakpoints
**Required diagrams:** none
**Required cross-references:** implementation/component_output

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
