# Bundle Analysis — Generation Template

> **Domain:** build
> **Section:** bundle_analysis
> **Source:** `documentation-standards/14-build-standards.md` §Bundle Analysis
> **Relationships:** `audit/deterministic/document/build-relationships.yaml`

Generates bundle size budgets, analyzer configuration, treeshaking verification, and CI size gates.

## Relationships

| Relationship | Target | Constraint |
|---|---|---|
| derives_from | implementation/build_output | Budgets must align with build artifacts |
| references | qa/test_results | Size regressions must not break test gates |

## Template

```markdown
# Bundle Analysis: [FeatureName]

## Bundle Size Budgets

| Asset | Budget | Current | Status |
|---|---|---|---|
| Main bundle | < 250 KB gzipped | [size] | [pass/fail] |
| Route chunk | < 50 KB gzipped | [size] | [pass/fail] |
| Component chunk | < 15 KB gzipped | [size] | [pass/fail] |
| Shared vendor | < 100 KB gzipped | [size] | [pass/fail] |

## Webpack Bundle Analyzer

```javascript
// vite.config.ts or webpack.config.js
{
  plugin: 'webpack-bundle-analyzer',
  options: {
    analyzerMode: 'static',
    reportFilename: './bundle-report.html',
    openAnalyzer: false,
  }
}
```

- [ ] Run `npm run analyze` before merge
- [ ] Review report for unexpected dependencies
- [ ] Check for duplicate packages across chunks

## CI Size Gate

```yaml
size-check:
  stage: build
  script:
    - npm run build
    - npx size-limit
  rules:
    - if: '$CI_MERGE_REQUEST_ID'
```

## Treeshaking Verification

- [ ] Verify unused exports removed in production build
- [ ] Check sideEffects field in package.json of dependencies
- [ ] Confirm ES module format for library dependencies

## Dependency Audit

- [ ] No new dependencies > 10 KB gzipped without approval
- [ ] Bundlephobia check for every new dependency
- [ ] Peer dependency count <= 3
```

## Examples

**Correct:**
> Main bundle is 220 KB gzipped, `npm run analyze` reports no duplicate lodash, and `size-limit` CI gate passes for all routes.

**Incorrect:**
> Main bundle is 400 KB gzipped, duplicate `moment` appears in 3 chunks, and no size CI gate exists.
> *Why wrong: Over budget, duplicate dependencies, no automated size enforcement.*

## Writing Guidance

- **Tone:** prescriptive
- **Voice:** imperative
- **Structure:** table-driven
- **Audience:** DevOps engineer
- **Do:** Set hard budgets, run analyzer on every PR, audit every new dependency.
- **Don't:** Skip size CI gates, allow unreviewed large dependencies, ignore duplicate packages.

**Required subsections:** Bundle Size Budgets, Webpack Bundle Analyzer, CI Size Gate, Treeshaking Verification, Dependency Audit
**Optional subsections:** Lazy Loading Strategy, Code Splitting Rules
**Required diagrams:** none
**Required cross-references:** implementation/build_output, qa/test_results

## Audit Fix

<!-- Phase 5: populate with finding→generation handoff -->
