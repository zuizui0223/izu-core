# R2: floral investment I can sort and fix under visitor decline even with A and M genetically frozen

**2026-10-23 — authenticated original 384-path, exploratory, post-outcome source subset.** This is not a new population experiment, a prospectively registered result, or an empirical island-flora comparison. Preserve all registered R1–R5 endpoints and the fresh-founder four-setting R2 **overall INCONCLUSIVE** verdict.

## Question

Can floral investment evolve under changed pollinator service if *both* reproductive assurance (A) and plant-pollinator matching (M) are incapable of changing? The original archived 384-path comparison already allows a more discriminating response than inspecting just the final A mean, because it retains the **diploid A, M and I allele support at census30**, the moment visitor activity is experimentally reduced.

We selected every original matched future pair for which:
1. A is **monomorphic** at census30;
2. M is **monomorphic** at census30;
3. I remains **polymorphic** at census30.

The original frozen model has **zero mutation and no seed or visitor immigration**; hence all subsequent A and M expressed trait values remain invariant. Only I has segregating genetic support at the shock. In each pair, *exactly the same source population at census30* enters common-random-stream control (visitor activity .4) and activity decline (.04) futures for 50 reproductive updates, differing first in an imposed **90% activity reduction**. We verify the A/M fixation invariant against the original source records at both endpoints, rather than assuming that the absence of a final A contrast proves no A evolution.

## Confirmed original-source native paired endpoint pattern

The same 384-path original GitHub Actions ZIP (run 39233450099, artifact 12178257738, SHA256 `10bb8bdd52b53b32429e350c2f392ed2aeaa791683ede1d563ae6627c5ecb35e`) yields **24 eligible paired sources**, belonging to **11 distinct founder seeds**, with four demographic repeats and two nominal starting A strata nested within each founder source.

| Historical pollen limitation | Eligible matched source pairs | I fixed at update80, control | I fixed at update80, visitor decline | Additional visitor-decline I contrast negative / zero / positive |
|---|---:|---:|---:|---|
| **Strong** | **22** | **13/22** | **22/22** | **12 / 10 / 0** |
| Weak | 2 | 1/2 | 1/2 | 1 / 0 / 1 |

This is a precise finite-model result: **under strong prior pollen limitation all 22 A/M-frozen sources had fixed investment I after the additional activity decline, but nine maintained-activity controls still retained I polymorphism**. Among the same 22 pairs, **20** of the 22 decline futures ended with I below their own census30 I mean, versus **11** of 22 controls. The mean within-pair `I_decline − I_control` was **−0.089134** I units.

The *first future generation* after the identical census30 genetic state had mean outcross fertilization of available ovules (`q`, before autonomous selfing) **0.139210** under strong-history controls versus **0.016895** under the extra activity decline. These q readouts are original *model-expected fertilization fractions*, **not** field pollen-deposition measurements or directly measured natural pollinator abundance. The two weak-history pairs instead had q near 0.998304 vs 0.541484 and opposite-signed I responses. Thus a universal decrease of I under any visitor drop is **not** established.

## Source axes and genetic-fixation outcomes

Under strong limitation, these 22 paired source futures represent **11 distinct founder seeds**. Founder-average treatment contrasts in I were negative for **9/11 founders**, exactly zero for **2/11**, and positive for **0/11**. The four demographic repeats are nested: 22 pairs are *not* 22 biologically independent founders, and founder selection into this subcohort was post hoc.

Among those strong-history 22 pairs, the final I support split was:

| Genetic endpoint state | Number of paired sources |
|---|---:|
| Both futures fixed to the same numerical I allele value | 10 |
| Both futures fixed to **different** numerical I allele values | 3 |
| Maintained-activity control polymorphic, decline arm fixed | 9 |
| Both futures polymorphic | 0 |

The **12 pairs with nonzero treatment contrasts** are exactly the three `both fixed different` plus nine `control polymorphic, decline fixed` sources. The remaining 10 converge on equal fixed I alleles. Exact fixed allele *values* do not establish identical ancestral gene copies.

## Biological meaning and what is not identified

This is a **structural negative control of necessity**: the original genetic model admits an I response to contemporary visitor decline when A and M are genetically unable to evolve over that future interval. It is not a controlled, genome-identical *causal A/M intervention*: A/M fixation was produced by an earlier 30-update period and selected from the already exposed exploratory archive. All present A, M, I frequencies, covariances and mating backgrounds still vary across source founders. The 22 outcomes are correlated descendants of only 11 independent founder IDs.

Moreover, the comparison does not divide the I effect into **directional selection versus stochastic demographic/genetic sampling**. A strong pollen reduction affects both maternal outcrossing and paternal export via the native reproduction operator; realized survival/fixation depends on finite stochastic reproduction. No generational individual-genome checkpoint sequence is retained in these summary records, so exact first-fixation times or separate hazard/selection coefficients cannot be reconstructed.

The next genuinely discriminating experiment is independent source-genome and visitor-history sampling with **genetically clamped A/M**, matched founder-by-visitor cells, and multiple independent demographic continuations within *every* cell; log both fixed-resident parental-genome gradients and realized gene support at each census, and prespecify a meaningful I contrast and a source-level inference rule. The original 384 pilot cannot become confirmation merely by further slicing outcomes. The existing 2026-10-23 prospective proposal explicitly keeps new biological dispatch unapproved; this note does not change that gate.

## Source paths and reproduction

- Original source: GitHub Actions [run 39233450099](https://github.com/zuizui0223/izu-core/actions/runs/39233450099), ZIP artifact **12178257738**
- This exact-source audit: `scripts/audit_chapter2_r2_shock_frozen_AM_I_sorting_20261023.py`
- Compact receipt: `docs/audits/CHAPTER2_R2_FROZEN_AM_I_SORTING_20261023.json`
- Tests: `tests/test_chapter2_r2_shock_frozen_AM_I_sorting_20261023.py`
- Original pair and cross-locus validators remain in PR #630 and PR #631, respectively.

To rerun source analysis, download the authentic 1.86 MB ZIP and execute:

    python -m scripts.audit_chapter2_r2_shock_frozen_AM_I_sorting_20261023 --zip /path/to/original.zip
    CHAPTER2_R2_384_ORIGINAL_ZIP=/path/to/original.zip python -m pytest -q tests/test_chapter2_r2_shock_frozen_AM_I_sorting_20261023.py

All source/model genome and pollen-operator code remains untouched; **new biological population updates = 0**, statistical tests = 0, and results are descriptive for this original finite model only.
