# Model3 implementation and execution audit

Scope: the user's later instruction makes Q1 inspiration only. This audit covers
the independent life-history evolutionary model and its declared experiments;
it does not certify universal island ecology or complete the poster project.
The original frozen plan retains unchecked boxes because it is a hashed input.
This document records their disposition without editing the frozen plan.

|Requirement|Authoritative evidence|Disposition|
|Visitor-mediated pollen transfer and finite effective doses|`scripts/model3_evolution.py`, pollen-budget and empty-visitor tests|Implemented and verified|
|Viable reproduction, male/female contributions, selfing and depression|`scripts/model3_reproduction.py`, conservation tests, robustness reproductive ledgers|Implemented and verified; depression fixed, no purging claim|
|Mendelian inheritance and overlapping adult cohorts|Evolution module; genotype, survival and extinction tests|Implemented and verified|
|Drift/neutral, fixed-trait, activity and community controls|Baseline frozen case list and verified160artifacts|All28,672cases executed; no dropped failures/extinctions|
|Prospective numerical freeze|Three design JSONs, canonical source hashes, recorded source commits and terminal manifests|All source/design checks pass after reporting changes|
|Explicit time and replication rationale|Natural-history note and frozen plan;256/64/16seed designs and Monte Carlo uncertainty|Reported; no geological calibration or rare-event precision claim|
|Duration and loss of standing variation|Full trajectories, checkpoint tables, Figure5 and integrated report|Reported, including monomorphic populations and visitor transients|
|Convergence/divergence/no-change and failure|`between_start_distance.csv`, joint direction columns, extinction records|Reported with undefined extinct traits and paired denominators|
|Pollen limitation and inbreeding robustness|30,720cases;120exact replays; assurance/effort contrast tables|Executed and interpreted, including persistence failure|
|Distribution/PDE question|Derived discrete inheritance operator;2,560matched pairs;64exact replays|Executed as a discrete distribution comparison, not a PDE; grid sensitivity retained|
|Q1 four-region concordance|Explicit later user scope amendment, recorded in frozen implementation plan|Not performed by instruction; no regional reconstruction claimed|
|Scientific figures and usable results|Five visually inspected PNG/PDF/SVG figures, integrated report, hashed CSV/gzip tables|Delivered|
|Independent review|Implementation/reproduction reviews and report/table reconciliation|Actionable findings corrected; no remaining review blocker|
|Local regression tests|`model3-integrated-tests.log`:1,780passed,1skipped,380.59seconds|Full suite passed; later figure edits executed and visually checked|
|GitHub integration|Authorized `codex/simulation-integrity-factorial` branch, current-head push and CI checked in task closeout|Requires exact-head remote/CI check after this commit; no PR or main merge requested|

Whole-artifact verification totals61,952cases/pairs,344exact sampled replays.
Raw arrays are locally retained and hashed in manifests; compressed endpoint
tables, compact summaries, figures and receipts are versioned. A journal raw-data
repository deposit remains a separate publication action and is not claimed.

Scientific sufficiency is bounded: the computational experiment answers its
declared conditional question. It does not establish robustness to all founder
supports, source-pool geometries, fitness costs, discounting mechanisms or
spatial/age structures. Those suggested extensions are required before stronger
claims, not silently passed gates. The integrated report explicitly withholds
those stronger claims. No favorable result was used to retune frozen parameters.
