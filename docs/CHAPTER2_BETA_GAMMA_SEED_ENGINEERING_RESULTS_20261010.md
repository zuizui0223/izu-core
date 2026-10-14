# Chapter 2 finite focal reproductive selection vs group viable-seed response: executed engineering map

**2026-10-10. Post-outcome EXPLORATORY source-model diagnostic. Not a preregistered ecological test.**
**Scientific inference:** In the declared finite synthetic grid, a *one-individual* reproductive gradient sometimes opposes the aggregate viable-seed-production response. This does **not** establish a change in population survival or evolutionary suicide.

## Purpose and source lock

Implements the central beta/Gamma decomposition proposed in `docs/CHAPTER2_INDIVIDUAL_SELECTION_POPULATION_PERSISTENCE_DISCORDANCE_PROTOCOL_20261010.md` for the **immediate `Gamma_seed` component only**. The complete 384-cell engineering grid was declared before its execution in `data/design/chapter2_beta_gamma_seed_engineering_grid_20261010.json`. It was designed after earlier post-outcome investigations of this same source model and is **not an independently preregistered confirmation**.

- Executed scientific source SHA `fd543b821460820e63144b99c37162de644c560a`.
- [GitHub Actions #38013728388](https://github.com/zuizui0223/izu-core/actions/runs/38013728388), focused regression tests and 384-cell runner **PASS**, artifact preservation **PASS** (broader repository CI tracked separately).
- [Original complete JSON artifact #11654822692](https://github.com/zuizui0223/izu-core/actions/runs/38013728388/artifacts/11654822692). Original JSON SHA256 `8dd7d5be4fd0366827d230990b757d04d3eea5b4fc179852e62c5f53ff49ca7b`, ZIP SHA256 `fb9eae1cc2264b4a9d823f3ed9a4c7ec7e4268be440e741119cd331428dc8d92`.
- Source-preserved compact result: `data/results/chapter2_beta_gamma_seed_engineering_receipt_20261010.json`; computation: `scripts/audit_chapter2_beta_gamma_seed_map.py`; dedicated checks: `tests/test_chapter2_beta_gamma_seed_map.py`.
- 384 synthetic cells = four original reproductive settings × three hand-authored static visitor states (none/matched4/shifted4) × K{8,48} at constant pollen-background B48 × matching{0.2,0.5} × investment{0.35,0.65} × assurance{0.35,0.65} × perturbed locus{investment,assurance}. Ovule budget=8. ZERO independently sampled visitor histories.

## Two *different* source quantities

At every finite diploid monomorphic parental census, perturb **one** individual's diploid allele-based trait around the resident state, with all other parent genotypes fixed. Read that individual's complete native Model3 reproductive ledger:

```text
W_0 = 0.5 * F_0 + 0.5 * P_0 + S_0
beta_N(z) = [log W_0(z+h; others fixed) - log W_0(z-h; others fixed)]/(2h)
```

This is a **finite-one-individual gradient**. At K=8 it perturbs 1/8 = 12.5% of parental plants, not a mathematically rare mutant; K48 is also finite. Do not relabel it the previously published/frozen infinite-resident analytic `invasion_gradient`.

In a **distinct** collective expression perturbation, shift the same locus in *all* N parent genotypes:

```text
T_N(z) = sum F_i(z) + sum S_i(z) = viable outcross + viable self seeds
Gamma_seed,N(z) = [log T_N(z+h) - log T_N(z-h)]/(2h)
```

The source ledger conserves `sum_i F_i = sum_i P_i`. Its focal `beta_N` is additively decomposed into **half maternal F**, **half paternal P** and **viable self S** via the exact symmetric log-mean denominator, with no unexplained remainder. The two log-derivatives are compared only if they exceed a predeclared absolute 0.02 numerical deadband and remain directionally stable at both central difference widths 0.005 and 0.0025. No independent ecological sampling error is estimated.

## Actual complete-grid outcomes

| Classification | Count out of 384 |
|---|---:|
| Same local sign (beta and Gamma_seed) | **362** |
| **beta negative, Gamma_seed positive** | **14** |
| beta positive, Gamma_seed negative | **0** |
| Inconclusive (deadband/numeric stability) | **8** |

**All 14 resolved discordances concern increasing floral-investment trait values.** Reproductive-assurance perturbations show 190 aligned and 2 inconclusive cases; no resolved assurance discordance in this grid. Four setting-specific discordance counts: delayed_control 3, prior_selfing 5, pollen_discount 3, assurance_cost 3. No-visitor controls give exactly zero maternal and paternal outcross source contributions, and every no-visitor row is aligned.

For example, delayed selfing, a matching=0.2/investment=0.35/assurance=0.35 resident, four hand-authored matched visitors, K8, B48, investment perturbation:

| Derived source quantity | Signed log-gradient |
|---|---:|
| `beta_one_individual` | **−0.063174** |
| `Gamma_group_seed` | **+0.158229** |
| `beta_F` | +0.134346 |
| `beta_P` | +0.156951 |
| `beta_S` | −0.354470 |
| `beta_F + beta_P + beta_S` | −0.063174 |

**Mechanistic reading:** increasing investment improves the focal individual's maternal/paternal outcross components but reduces its own viable selfed contribution enough to make its total relative genetic contribution decline. Yet changing investment in the entire population can increase total viable seeds. The positive paternal term *does not* imply that pollen competition alone caused the mismatch, and the negative self term is a derivative with respect to investment, not evidence that selecting for higher assurance is harmful.

Across all 384 cells, the maximum absolute change when halving finite-difference width was approximately **0.000146** for each beta/Gamma target; the exact ledger mass and F/P/S additive identities passed regression tests. This is numerical stability **within declared model assumptions**, not cross-model ecological validity.

## Negative and alternative explanations retained

The proposed most provocative direction (beta positive but **group seed production negative**) was **not observed** in this declared grid. No positive selection against group seed output, let alone evolutionary suicide, should be asserted. That outcome could appear at other biologically specified parameter settings, but searching for such cells after seeing this result would be post-outcome exploration, **not independent confirmation**.

For the 14 opposite-direction cells, one must not call the signal a conflict with **population persistence**, because `Gamma_seed` precedes finite recruitment, density regulation and extinction. The experiment has no evolving trait trajectories; it is not evidence of a trait actually spreading against group benefit. Indeed, gamma_seed may change positively while gamma_persist remains negligible when K is saturated. There is no genetic load, mutational meltdown or ecological field calibration here.

## Next experimental branch (still blocked)

1. Lock a biologically motivated prospective parameter surface across mating rules, visit supply, K/B, depression, resource cost and mutation before looking at any new trajectories. Retain both observed and unobserved-sign predictions, including zero/inconclusive regions.
2. Distinguish a genuinely *rare-mutant* gradient from `beta_N`: compare to the existing analytic source rare-mutant implementation under a matching source environment, or explicitly extrapolate N while controlling pollen dilution. Do not combine incompatible denominators.
3. Introduce `Gamma_persist(H)`: randomized *collective trait expression* shift and an independent evolution-allowed vs **genetic evolution frozen** contrast with unconditional occupancy at matched history/H/K/B. A true evolutionary-suicide hypothesis requires the latter evolutionary comparison, not just seed output or isolated local beta.
4. Only after source validation and prospective power design, generate genuinely unused independent visitor histories; the existing 384 hand-authored cells and prior engineering grids cannot count as confirmation. Keep #411's confirmed evolution letter, #451's fixed-B capacity companion and #420 stochastic-operator diagnostics distinct.

**Scope summary:** successfully established a *local* source-model genetic-contribution versus total viable-seed-production sign mismatch in 14 of 384 synthetic finite-N parameter cells. The population-persistence boundary remains unmeasured.

## Canonical analytic rare-mutant cross-check (post-outcome, 2026-10-10)

The finite-population focal-one-individual beta at K48 was checked against the existing analytic rare-mutant gradient from `scripts/model3_island/selection.py`. Its monomorphic, at-capacity pollen denominator assumes **B=K**, therefore comparisons were restricted to **K48/B48** and **K8/B48 was excluded** as not source-equivalent. Original exact-source `investment_invasion_terms` and `syndrome_thresholds` were used for the investment and assurance axes; no biological settings were modified. The analytic gradient is not assumed numerically identical to a mutant occupying 1/48 of parents.

- Executed full 192 K48-cell original-source check: [CI #38014053216](https://github.com/zuizui0223/izu-core/actions/runs/38014053216), focused unit tests, computation and archive upload **PASS**; [full original artifact #11655438178](https://github.com/zuizui0223/izu-core/actions/runs/38014053216/artifacts/11655438178), original JSON SHA256 `d3dc89b702233c00be29ee1f0a6f36148d87ca7533a53271a621275178f2d3e6`. Reproducible `scripts/audit_chapter2_beta_gamma_rare_limit.py`, tests `tests/test_chapter2_beta_gamma_rare_limit.py`, source-locked `data/results/chapter2_beta_gamma_rare_limit_receipt_20261010.json`.
- **All six finite K48 discordances remained discordant using canonical analytical rare-mutant beta**. Finite versus rare signed-beta signs did not reverse in any of the 192 cells. Analytic rare-beta × group Gamma_seed classification: **178 aligned, 6 beta-negative/Gamma-positive, 0 beta-positive/Gamma-negative, 8 inconclusive**. Maximum absolute difference between numeric finite beta and analytic rare beta was ~0.01958; sign agreement does not imply exactly equal magnitudes.
- This check strengthens the **local model-conditional** conclusion that florally invested *rare individual* selection can oppose population-wide viable-seed production in some original model states, rather than only because a focal individual constitutes a large portion of K48. It **does not** establish the corresponding Gamma_persist sign, evolutionarily driven frequency change or evolutionary suicide, and zero independent ecological visitor histories remain.
