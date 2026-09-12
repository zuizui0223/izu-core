# Chapter 2 Oikos submission checklist

Updated: 2026-09-12

## Active route

- Journal: **Oikos**
- Article type: **Research Paper**
- Scientific tier: **Tier B — synthetic conditional-response mechanism completed by source-audited metadata confrontation at a bounded empirical claim ceiling**
- Journal-facing story: **Conditional response geometry → exact realized-richness control → scale-dependent determinant ordering → downstream modifiers → metadata confrontation / empirical claim ceiling**
- Empirical role: **source-audited biological plausibility, adversarial secondary-data stress testing and identifiability boundary; not full natural validation**
- Izu E3/E4: **post-Chapter-2 future transport/falsification, not a submission gate**
- Fallback: **Journal of Ecology Research Article**

Active narrative contract: `docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md`.
Chapter-completion contract: `data/design/chapter2_simulation_metadata_completion_lock_20260912.json`.
Claim-by-claim evidence map: `docs/CHAPTER2_SIM_META_EVIDENCE_MATRIX_20260912.md`.
Historical three-result and four-act narrative locks are provenance only.

The scientific gate is closed. No additional simulation, world search, Izu same-block field measurement, NEE Stage-1 work or Chapter 3 result is required to complete the current Chapter 2 paper.

## Oikos initial-submission requirements implemented

- blinded main upload: **`MANUSCRIPT.rtf`**;
- separate supporting upload: **`SUPPORTING_INFORMATION.rtf`**;
- separate identity-bearing **`TITLE_PAGE.rtf`**;
- double-anonymous manuscript rendering;
- single-column, double-spaced main text;
- continuous line numbering and page numbering;
- Introduction forced to begin on page two;
- abstract capped at 300 words;
- renderer validates the mechanism-mainline contract rather than historical three-result/four-act routing;
- dedicated Significance statement;
- Data Availability / data-archiving statement;
- accepted-stage public repository fixed to **Dryad Digital Repository**;
- conflict-of-interest and ethics statement surfaces;
- author confirmation of the prefilled ethics statement remains fail-closed through `ethics_statement_confirmed`;
- reviewer-ready frozen data, code and audit materials in the anonymous review archive.

The active submission manifest is `data/design/chapter2_oikos_submission_manifest_20260831.json`.
The active metadata template is `data/design/island_ecology_submission_metadata_template.json`.
The machine-readable submission-closure preflight is `data/results/chapter2_submission_closure_audit_20260906.json` and is checked by `python scripts/audit_chapter2_submission_closure.py --check`.

## Scientific claim ceiling retained at submission

### 1. Conditional response geometry

- baseline 96 matched community realizations contain 41 mixed, 42 all-positive and 13 all-negative response worlds;
- partner loss and partner arrival are the largest sign-stable regime associations in the declared design;
- baseline variance decomposition is starting position 2.18%, community realization 80.17%, state × community non-additivity 17.64%;
- these are synthetic design quantities, not natural frequencies or calibrated ecological effect sizes.

### 2. Realized-richness control

- exact stepwise realized-richness matching makes the ensemble mean all-positive in **6/6** prespecified matching seeds;
- nevertheless **51–65/96** individual communities remain mixed-sign;
- community-realization share remains **50.04–55.92%**, state × community nonadditivity **42.72–48.51%**, and starting-position additive share **0.94–2.21%**;
- equalizing baseline partner-arrival/loss rates still yields **70/96** mixed realizations and **65.61%** nonadditivity.

### 3. Scale-dependent determinant hierarchy

- zero-adjustment pooling across `k={1,2,4,8,16}` reduces finite-community count variation while mixed branching persists through `k=16`;
- the deterministic mean-field kernel contrast is all-positive, so branching vanishes asymptotically when finite realized composition is averaged away;
- with active plant adjustment, median starting-position share rises **2.55 → 10.33 → 27.33 → 42.52 → 55.84%**;
- median community-realization share falls **72.98 → 48.03 → 23.52 → 18.26 → 12.72%**;
- starting position exceeds community realization in **0/6, 0/6, 6/6, 6/6, 6/6** seeds across the declared `k` sequence;
- mixed branching persists at `k=16` in **28–42/96** realizations;
- the supported conclusion is that **determinant ordering is regime dependent**;
- the numerical crossover near `k=4` is model-specific and must not be interpreted as a natural threshold.

### 4. Downstream modifiers

- local filtering reallocates branches bidirectionally but asymmetrically;
- at filtering strength 0.40, negative→non-negative transitions are 42/268 (15.67%) and positive→non-positive transitions 337/596 (56.54%);
- reproductive assurance attenuates magnitude but gives zero sign rescues among 580 eligible declines through 4× in the declared envelope.

### 5. Metadata confrontation and empirical claim ceiling

- formal source audit: direct responses 21/25, direct partner arrival/replacement 2/25, full outcome-independent contracts 0/25;
- formal external prediction remains `not_evaluable`;
- broader source-verified descriptive evidence reaches 42 research entries / 37 exact geographic labels and the declared geography-first saturation rule;
- Wanshan–Yongxing and Ogasawara provide large partner-turnover examples without licensing a pooled universal island effect;
- existing Izu secondary analyses retain both support and failure: functional exposure → corrected matching is robust, matching → pollen is not leave-one-island sign stable, the historical signed-position projection is unsupported after null correction, and the Oshima bridge is not independently identified as causal;
- these data constrain interpretation and biological plausibility but do **not** validate a universal synthetic determinant hierarchy or natural `k≈4` threshold;
- Chapter 3 phenotype divergence is not Chapter 2 validation;
- Izu visitor → effectiveness → dependency → mature-seed E3/E4 is a **post-Chapter-2** prospective transport/falsification programme.

## Author-supplied information still required

Populate the metadata template with final author order/affiliations, corresponding-author email/postal address/ORCID, significance prior-work context, acknowledgements, funding, inclusion/EDI statement, conflict-of-interest statement, ethics confirmation (`ethics_statement_confirmed=true` after author review), and explicit submission declarations.

**CRediT / author-contribution roles are not an initial-submission blocker.**

The public repository choice is already fixed to **Dryad Digital Repository**.

## Final build

Run the metadata validator, `python scripts/audit_chapter2_submission_closure.py --check`, and then `python scripts/build_island_ecology_submission_bundle.py --metadata data/design/island_ecology_submission_metadata_template.json`.

Expected bundle: `dist/chapter2_oikos_submission_bundle.zip`.

Until the author-supplied fields, ethics confirmation and declarations are complete, the builder remains fail-closed by design. Any non-metadata failure is a packaging/renderer problem, not a scientific reason to reopen simulation, metadata searching or field E3/E4.
