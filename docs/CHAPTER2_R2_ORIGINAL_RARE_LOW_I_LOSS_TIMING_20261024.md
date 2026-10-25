# R2: rare low-I alleles can disappear despite positive expected transmission in every segregating generation

**2026-10-24 — retrospective, exact-source original Model 3 result; not a new experiment, general fixation-frequency threshold, or causal selection/drift decomposition.** This follows the original SHA-verified 384 histories and original full-genome technical replays (#630–#636). Existing registered R1–R5 evidence ranks, R4 G/S, and independently founded four-setting R2 overall **INCONCLUSIVE** status remain unchanged.

## Question

The earlier native parentage audit found that in **all 22 strong historical pollen-limitation source populations** with A and M monomorphic and I polymorphic at original census 30, the visitor-activity decline increased the expected next-generation frequency of the *lowest numerical I allele*, conditional on the exact original census30 diploid genotype. Yet the lowest available I allele disappeared from the original **two rare-copy exception populations** by update 80, leaving a higher I allele fixed in both treatment futures. Was the low allele already disfavored during the actual trajectory, or did it disappear despite positive conditional expected transmission?

## Original-genome admissibility and reconstruction

The archived original pollen experiment is [Actions run 39233450099](https://github.com/zuizui0223/izu-core/actions/runs/39233450099), artifact `12178257738`, immutable original ZIP SHA256 `10bb8bdd52b53b32429e350c2f392ed2aeaa791683ede1d563ae6627c5ecb35e`.

An independently executed native replay of the **same original 24 census30 source states and 48 finite future paths** passed exact full diploid source-genome SHA256 checks in [Actions run 40057254260](https://github.com/zuizui0223/izu-core/actions/runs/40057254260) (artifact `12546400082`, exact pathwise source JSON SHA256 `794a23aca8e56f8e74f4d5497fa221cbba9432a20170917163fe117dd7fddccc`). These files are original already generated histories, **not** independent biological replications.

The two exception source populations had *exactly two numerical I allele values*, with allele difference 0.25 and no mutation, seed immigration, or adult survival. Therefore, at each original census t, the low-I numerical allele frequency is determined directly from the original population-mean I:

[
p_{\mathrm{low},t} = \frac{I_{\mathrm{high}}-\bar I_t}{I_{\mathrm{high}}-I_{\mathrm{low}}}.
]

The exact low-I diploid copy count equals `2N(t) × p_low(t)` and is verified to be an integer for every original census. Likewise, the source conditional expected one-generation frequency change in the lowest-I allele equals

[
\mathbb{E}[\Delta p_{\mathrm{low}}\mid \text{realized genotype state at }t]
=\frac{-S_{I,t}}{I_{\mathrm{high}}-I_{\mathrm{low}}},
]

where `S_I,t` is the full original native **father + mother + viable self** expected newborn I sorting, and the realized residual is the corresponding `-epsilon_I,t / (I_high-I_low)`. This is an algebraic transformation valid for these **biallelic** original states only, not an extrapolation to the two triallelic sources in the broader 22-cell group.

## Source-exact result: actual loss census and expected versus realized increments

| Original source | Treatment | Low-I copies at census30 | Census at which low-I first absent | Number of segregating future years | Cumulative expected low-I frequency change | Cumulative realization residual |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| A0=.3, founder 810102 / repeat 4 | Maintained | **6/96** | **45** | 15 | **+0.006402** | **−0.068902** |
| Same original source | Visitor decline | 6/96 | **35** | 5 | **+0.031675** | **−0.094175** |
| A0=.5, founder 810110 / repeat 3 | Maintained | **4/96** | **42** | 12 | **+0.004053** | **−0.045720** |
| Same original source | Visitor decline | 4/96 | **51** | 21 | **+0.100839** | **−0.142506** |

**Every one of the 53 original segregating annual states across these four treatment futures had a positive conditional expected change in the low-I allele frequency**, even though the low-I allele was eventually lost in *all four*. Once the allele had disappeared, the original zero-mutation, zero-immigration Model 3 made its expected frequency change zero.

The expected and realized-residual sums recover the exact source outcomes, not merely an approximate correlation:

- Founder 810102 / repeat4, visitor decline: `+0.031675−0.094175 = −0.062500`, corresponding to loss of **6/96** initial copies.
- Founder 810110 / repeat3, visitor decline: `+0.100839−0.142506 = −0.041667`, corresponding to loss of **4/96** initial copies.

For the first source, the low-I allele disappeared **10 updates earlier** in the decline future than in control (35 vs 45). For the second source, the low-I allele disappeared **9 updates later** in the decline future (51 vs 42). Thus **the visitor decline did not universally accelerate loss of these lower-I alleles**; the paths have different inherited frequencies and stochastic realizations. The direction of conditional expected genetic sorting stayed positive for the low allele throughout each segregating period, including the 21-year decline future in the second source.

## Scientific meaning and strict boundaries

This is a strong **within-original-model counterexample to deterministic inference from a selection-like directional expectation**: a rare inherited I allele can vanish in a finite population even when its immediate native expected parental transmission is positive at every visited state before disappearance. Reproductive contributions and offspring/parent sampling vary across generations. The residual records this difference between expected and realized native source reproduction, but **does not isolate pure neutral genetic drift or provide a uniquely identified causal "drift share"**. Repeated generations are serially dependent within two original founder identities, not 53 independent experiments.

It also illustrates that the window for floral simplification depends on two components that should be investigated separately: **what allele values are still genetically reachable after prior history**, and **how long that segregating genetic variation survives under a changed visitor community**. These are model-specific ecological/evolutionary hypotheses, **not established natural-island laws**. Neither these two rare-copy examples nor the 22 post-selected source cells establish a real frequency threshold, independent 50-year fixation probability, or general evidence that genetic drift overcame natural selection.

The original source-independent four-setting R2 **overall INCONCLUSIVE** result and the registered R1–R5 manuscript claims are not changed. Prospective causal separation would require independent source genotypes and matched demographic repetitions with a predeclared protocol and effect criteria.

## Reproduce

- Original full-path hash-verifying reader: `scripts/audit_chapter2_r2_original_pathwise_I_accounting_20261024.py`
- This biallelic loss chronology: `scripts/audit_chapter2_r2_rare_low_I_loss_chronology_20261024.py`
- Compact numeric result and source-provenance receipt: `docs/audits/CHAPTER2_R2_RARE_LOW_I_LOSS_CHRONOLOGY_20261024.json`
- Dedicated analytic and negative-control tests: `tests/test_chapter2_r2_rare_low_I_loss_chronology_20261024.py`

```bash
python -m scripts.audit_chapter2_r2_rare_low_I_loss_chronology_20261024 > /tmp/R2_ORIGINAL_RARE_LOW_I_LOSS_CHRONOLOGY.json
python -m pytest -q tests/test_chapter2_r2_rare_low_I_loss_chronology_20261024.py
```

This reader recomputes only original saved source trajectories and requires the exact original census30/t80 full-genome SHA. No new experiment cases, new stochastic seeds, biological parameter changes, or preregistration claim are introduced.
