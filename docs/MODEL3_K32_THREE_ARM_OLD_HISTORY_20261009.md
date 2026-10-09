# PR #420 — old-history fixed K32 three-arm comparison (2026-10-09)

## Aim and provenance

This is a **simulation-only engineering comparison**, not natural-island
observations, external empirical validation, an independent biological
confirmation, an Itô SDE, or a spatial SPDE. The source Model 3 mating,
pollen exclusion, Mendelian genotype inheritance, and capped-Poisson
recruitment are **unchanged**. Only existing restricted diagnostic
implementations are called. No frozen confirmatory visitor history
37110801–37110864 is used.

Primary fixed conditions: **capacity K=32, mutation u=0, generations=8,
adult survival=0, incoming seeds=0**, existing *prior_selfing* biological
setting with its source values, and archived **visitor seed 26110601,
near** for the first eight time-indexed visitor communities.
No new visitor history is assembled. This is **one** old visitor history,
with 256 independently seeded *nested demographic draws* in each
stochastic arm—not 256 ecological histories. Four pre-existing
engineered diploid founder genotypes are replicated to K=32, with
two possible alleles at each of three loci (27 joint diploid classes).
These are NOT the original continuously valued 48-founder cohort and
should never be described as a natural island genotype sample.

The optional labeled sensitivity changes *only* ovule budget
from the source-comparison value 8 to 3 to explore extinction; the
K, mutation, eight-generation, mating and visitor settings remain fixed.
No result from the resource stress substitutes for the primary setting.

## Comparison and fair separation of assumptions

* **Exact finite stochastic reference:** 
  `genotype_count_markov_step()` reconstructs every individual from complete
  joint diploid genotype counts, calls canonical `reproduce()` (including
  diagonal exclusion of self-pollen transfers), draws the canonical capped
  Poisson census and then exact Mendelian categorical offspring. No
  mutation, survival or immigration.
* **Deterministic expected-count plug-in:**
  `E[min(Poisson(R),32)] q` is the canonical **conditional next-child
  expectation** for the *current* representative census. To pass an
  individual census to the unchanged source mating operator in the
  subsequent generation, we round expected census to the nearest
  integer and allocate expected genotype counts by deterministic
  largest remainders. This **does not equal** the exact ensemble
  expectation `E[X_8]` of the nonlinear eight-generation source
  process and changes genotype-loss behavior. It has a single
  representative trajectory rather than a probability distribution.
  A product of source one-step survival probabilities evaluated along
  that trajectory is separately reported as a *plug-in heuristic*,
  not as the deterministic path's own extinction probability.
* **Projected Gaussian approximate stochastic counts:**
  `approximate_markov_step()` calls the very same canonical
  `reproduce()` for each rounded genotype state and samples the same
  capped-Poisson census. It replaces the exact categorical offspring
  step by the previously implemented tangent-Gaussian counts with the
  matching *pre-projection* multinomial covariance,
  nonnegative clipping, renormalization and largest-remainder
  integerization. After projection the law need not have matching
  moments, may lose rare genotype classes incorrectly, and is
  **not** a validated SDE/SPDE.

Deterministic rounding and Gaussian projection are disclosed as distinct
**numerical approximations**, not biological changes to Model 3.
The exact finite comparator alone is an alternate representation of
its restricted original finite-process transition law.

## Endpoints at generation 8

1. **Whole-population extinction:** probability over stochastic repeats;
   **no trait value imputed as zero** for extinct trajectories.
   Deterministic reports representative occupancy and its labeled
   survival-product heuristic, not an extinction frequency.
2. **Mean of each of three genetic traits:** average diploid trait
   value **conditional on surviving endpoints**, with Monte Carlo SE
   for stochastic arms.
3. **Genotype loss:** fraction of endpoint replicates lacking each
   **initially present joint diploid genotype class**. A genotype class
   can disappear and subsequently reappear via Mendelian segregation;
   this readout is *endpoint absence* and NOT irreversible allele loss
   or independent lineage extinction.
4. **Genetic diversity:** joint diploid class richness (extinct
   populations legitimately have zero classes) and Simpson
   `1 - sum(p_g^2)` **conditional on occupancy**. No imputed
   allele count or missing continuous-genotype support is allowed.
5. **Numerical accuracy:** source-consistent integer nonnegative
   census in `[0,32]`, exact genotype-law mass audit,
   stochastic Monte Carlo standard errors, differences from
   exact-reference summary estimates, and elapsed wall-clock time.
   Wall-clock time is CI-hardware dependent and is not an algorithmic
   complexity theorem. Approximation errors are not natural-data
   goodness-of-fit statistics.

The results intentionally avoid a posterior probability of model
truth. An old, fixed visitor history gives no generalization estimate
across new independent histories. The full nonzero-mutation genotype
support, large-population/diffusion scaling, and ecological field
calibration remain **outside scope**.

## Reproduce

```bash
python -m pytest -q tests/test_model3_three_arm_k32_old_history.py
python -m scripts.run_model3_three_arm_k32_old_history \
  --out model3-three-arm-k32-old-near-budget8.json --draws 256 --budget 8
python -m scripts.run_model3_three_arm_k32_old_history \
  --out model3-three-arm-k32-old-near-budget3.json --draws 256 --budget 3
```

Dedicated CI: `.github/workflows/model3-three-arm-k32.yml` archives
the machine-readable JSON receipts as
`model3-three-arm-k32-engineering` on a successful workflow. Source
result files are **not** populated with unexecuted, guessed numbers.
Numerical conclusions may be reported only after the actual CI
run is completed and checked. Keep PR #420 Draft until its broader
scientific gates are satisfied.
