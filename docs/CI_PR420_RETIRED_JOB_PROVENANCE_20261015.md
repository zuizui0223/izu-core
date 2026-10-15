# CI cleanup — retired PR #420-only jobs (2026-10-15)

## Decision and provenance

The existing `.github/workflows/ci.yml` contained one **general** test matrix and 20
auxiliary Model 3 K32 jobs, each guarded **exactly** by:

```yaml
if: github.event_name == 'pull_request' && github.event.pull_request.number == 420
```

[PR #420](https://github.com/zuizui0223/izu-core/pull/420) is **merged and
closed**. No later pull request can have number 420, and `push` events cannot
satisfy the guard. None of the retired blocks was a dependency of another
job (`needs:` absent). Thus all 20 definitions had become unreachable; they
showed only **skipped** on normal PRs while making the active CI file hard to
maintain. The 2026-10-15 cleanup removed their definitions from **current CI**
and did *not* remove the algorithms, tests, readouts, source manuscripts,
experimental receipts, release identities, or git history.

The full pre-cleanup **1,295-line** original workflow is retained by Git at
[commit `264ed7d` prior to retirement](https://github.com/zuizui0223/izu-core/blob/264ed7d7185d6c205b6f02c019dd15bddfee982b/.github/workflows/ci.yml)
(Git blob `ae91c6aaf66637b23db14067eb08d135cb9f4172`). Original
[#420 merged commit](https://github.com/zuizui0223/izu-core/commit/b4335ae90ecb0b0b76fe0341b2ec67c91df65697b)
and historical Actions run references in Model 3 K32 reports remain as
provenance. Artifact expiry or availability must be checked independently;
this documentation does not assert continued archive downloadability.

## Retired auxiliary job IDs (20)

| Group | Original PR #420 job names |
| --- | --- |
| Fundamental finite-process decompositions | `model3-k32-decomposition`, `model3-k32-pathwise`, `model3-k32-neutral-boundary`, `model3-k32-mean-matched-ceiling`, `model3-k32-demographic-holdout` |
| Parentage, selfing and outcrossing | `model3-k32-same-parent-moments`, `model3-k32-local-assurance-response`, `model3-k32-symmetric-assurance`, `model3-k32-self-outcross`, `model3-k32-outcross-factors`, `model3-k32-outcross-ablation`, `model3-k32-parental-marginals` |
| Larger conditional contrasts | `model3-k32-full-factorial`, `model3-k32-state-visitor-cross`, `model3-k32-locus-reassignment`, `model3-k32-fixed-allele-heterozygosity`, `model3-k32-heterozygosity-channels`, `model3-k32-self-transmission-curvature`, `model3-k32-new-visitor-history-stress`, `model3-k32-multihistory-state-visitor-cross` |

These are historical *engineering run names*, not 20 independent experimental
systems or an enlarged natural-history sample. The original work and exact
reproduction commands remain in the respective `docs/MODEL3_K32_*` records
and historical CI commit; do not reinterpret their claims or re-run large
biological campaigns merely because a job name was removed.

## Active CI contract after cleanup

Only `jobs.tests` runs in `.github/workflows/ci.yml`:

- Python **3.10**, **3.11**, **3.12**
- `python -m pip install -e '.[dev]'`
- `pytest -q`, preserving pipe-failure propagation and failure log upload
- unchanged workflow triggers (`main` pushes and pull requests) and concurrency

The separate [Chapter 2 scientific gate](../.github/workflows/chapter2-scientific-gate.yml)
remains unchanged and is still required when its path filters match. That gate
protects source-bound, original-result and reviewer-package checks.

**Preservation firewall:** this is CI *definition* hygiene. No original Model 3
math, independent-unit denominator, biological program, frozen experiment,
original reference, paper or data-deposit result is modified by the cleanup.
If a PR #420 audit ever needs to be rerun, reconstruct the exact historical
workflow checkout by SHA and follow its original source instructions rather
than restoring always-skipped blocks into the shared CI file.
