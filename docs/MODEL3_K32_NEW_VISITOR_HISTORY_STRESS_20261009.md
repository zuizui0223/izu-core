# Model3 K32: New simulated visitor-history stress test of matching direction reversal

## Question

The original K32 old-history seed 26110601 gave a late sign reversal in the matching-high-allele expected one-generation reproductive direction under Chapter2 prior_selfing. Subsequent exact source accounting showed linear assurance seed output, quadratic allele dosage transmission, and strong genotype-state contributions. However, every numerical trajectory previously used ONE ecological visitor history.

This exploratory experiment checks whether the sign reversal reappears under EIGHT different original visit-history RNG seeds generated with the original visitor simulator, WITHOUT accessing the prospectively frozen confirmatory seeds.

## Strict prospective-origin distinction

**We chose these new simulation seeds after observing the sign reversal.** Their outcomes can constitute an out-of-source-seed *exploratory stress test*, NOT preregistered independent confirmation or unbiased evidence of novel evolution.

- Original discovery history: `26110601`, shown as an explicitly separate reference.
- Newly generated, predetermined follow-up histories: `26110602` through `26110609`, a contiguous eight-seed range. All eight are included whether or not they reproduce the sign reversal.
- Prospectively frozen Chapter2 histories `37110801..37110864`: **NOT used**.
- Each new history is a different RNG visitor trajectory from the **same fixed ecological generating process**. These are NOT eight natural islands or eight field experiments.

Use source `exposure(seed, "near")` without editing that visitor generator, and original canonical Model3 reproduction and exact genotype-count Markov transition. K=32, mutation=0, no survival/immigration, Chapter2 `prior_selfing` configuration (assurance_cost=0, investment_cost=.5), two reproductive budgets 8 and3, and eight years. The same engineered four diploid founder genotype classes and 27-class full joint support are used throughout.

Within each history, use 128 demographic replicates with independently declared path RNG seeds. **Only the eight newly simulated visitor histories are independent environmental RNG histories**; the 128 paths are nested demographic repetitions, not independent visitor environments. The discovery reference history is NOT included when calculating new-history fractions or ranges.

## Matched surviving source cohort

At each history and budget, evolve all original source trajectories for seven updates to obtain original parent genotype counts at the start of year8. Restrict the comparison to a common cohort of demographic path IDs surviving to parent year8, and use those EXACT SAME IDs for all parent years 1–8.

For each original `C_t,V_t` diagonal, evaluate original source `reproduce()`, not an altered operator. Compute the exact Mendelian expected next HIGH allele direction at the three loci:

```text
D_l(t)=E[p_next,l | C_t,V_t,N_next>0]-p_l(C_t)
      = self_l(t)+outcross_father_l(t)+outcross_mother_l(t).
```

The common survivor cohort avoids misleading trajectory comparisons with different paths at early and late years, but it **conditions on later survival** and is not an unconditional population estimate.

Summarize for each seed separately: number of source survivors, visitor-sequence fingerprint, year1/year8 expected direction mean for matching, investment and assurance; expected viable-self, successful father and mother marginal components; paired demographic MC SE for the year8-minus-year1 matching direction; and whether the matching HIGH allele mean direction switched from negative in year1 to positive in year8.

For the EIGHT newly generated seeds, report their complete denominator (including extinct histories), count with valid source year8 living parents, count/valid-denominator with sign reversal, and spread of mean late expected matching direction across independent RNG-generated visitor histories. DO NOT imply that 8 histories provide a high precision independent ecological population estimate.

## Interpretation and release criteria

Possible outcomes and implications:

- Many positive late matching directions: the earlier flip is not limited to the single numerical historical visitor seed *within the original visitor generator*, but remains a conditional engineering property, not ecological generality.
- Few or no positive late matching directions: the flip is highly history-dependent and should NOT appear as a general model claim.
- Insufficient surviving source parents for some histories: report the limitation and denominator; do not force zero/positive allele direction on extinct populations.
- Early and late signs are *instantaneous expected reproductive filtering* under different evolved parent states; they do NOT demonstrate recovery of lost high alleles, fitness maximization or adaptive balancing selection.
- Exact quadratic source assurance-transmission identity holds for ANY source visitor state under the frozen reproductive formula, but that mathematical identity **does not guarantee** eight-year matching direction reversal under different ecology.

Reproduce:

```bash
pytest -q tests/test_model3_k32_exploratory_visitor_histories.py
python -m scripts.audit_model3_k32_exploratory_visitor_histories --budget 8 --draws 128 --out exploratory-histories-budget8.json
python -m scripts.audit_model3_k32_exploratory_visitor_histories --budget 3 --draws 128 --out exploratory-histories-budget3.json
```

PR420-only CI `model3-k32-new-visitor-history-stress` validates actual seed lists, archive vs newly generated flags, absence of prospectively frozen confirmatory seeds, source reproduction and three-channel Mendelian sum; stores BOTH raw outputs. Do not promote numerical reproducibility claims until CI succeeds and the raw artifact has been inspected. PR stays Draft; no natural island data or SDE/SPDE validation.


## CI-verified outcomes across new visitor seeds

[Dedicated GitHub Actions CI 37947205797](https://github.com/zuizui0223/izu-core/actions/runs/37947205797) SUCCESS on source SHA 5d84435e9e0c90246556f76edef80caadd9dfeae. [Complete raw two-budget artifact 11623478169](https://github.com/zuizui0223/izu-core/actions/runs/37947205797/artifacts/11623478169), SHA256 9b1147964561ef0d8e6df6337034ba68101deb5c8c1d8d40058c19c4f2c76f14, was inspected. Its 2 JSON files include original viable-self and outcross father/mother Mendelian transmission by source year, for all nine archived/reference and new history seeds. Compact record: data/results/model3_k32_new_visitor_history_stress_20261009.json.

### The negative-to-positive matching allele direction reversal is NOT universal

| New visitor histories ONLY (old discovery seed excluded) | Budget8 | Budget3 |
|---|---:|---:|
| Distinct newly generated source visitor RNG histories | 8 | 8 |
| Histories with surviving source parent cohort at year8 | 8 | 8 |
| Negative year1 → positive year8 sign reversal | **4/8** | **5/8** |
| Year8 matching HIGH expected direction positive | **5/8** | **6/8** |
| Initially negative matching expected direction | 6/8 | 6/8 |
| Reversal among initially negative histories | 4/6 | 5/6 |
| Mean year8 expected matching direction across histories | +0.003513 | +0.002018 |
| Full year8 direction range | -0.007223 to +0.013873 | -0.003994 to +0.008291 |
| Change year8 minus year1 range | -0.022898 to +0.070266 | -0.025859 to +0.075045 |

The 128 demographic replicates within each history are NESTED and not independent ecological systems. The visitor-history denominator is 8, not 8×128. These eight histories were selected AFTER seeing the original 26110601 sign reversal, so this is exploratory simulator-seed robustness, not a preregistered confirmation.

### All new seeds and the old reference, no post-outcome removal

| Seed | Budget8 year1 → year8 matching direction | Budget3 year1 → year8 matching direction |
|---|---|---|
| 26110601, old discovery REFERENCE (excluded from new denominator) | -0.062815 → +0.005629 | -0.062815 → +0.003289 |
| 26110602 | +0.000494 → +0.009356 | +0.000494 → +0.001514 |
| 26110603 | -0.037581 → +0.013873 | -0.037581 → +0.008291 |
| 26110604 | -0.028825 → +0.006784 | -0.028825 → +0.005167 |
| 26110605 | -0.002780 → +0.001928 | -0.002780 → +0.000694 |
| **26110606** | **+0.021864 → -0.001033** | **+0.021864 → -0.003994** |
| **26110607** | **-0.077490 → -0.007223** | **-0.077490 → -0.002445** |
| 26110608 | -0.008031 → +0.006374 | -0.008031 → +0.006412 |
| 26110609 | -0.041096 → -0.001954 | -0.041096 → +0.000503 |

Source seed 26110606 reverses in the OPPOSITE direction under both budgets, whereas seed 26110607 stays negative. The old-source 26110601 negative-to-positive reversal is therefore a contingent outcome of a particular visitor/genotype trajectory, not a theorem that assurance-correlated selfing universally forces matching allele sign reversals.

The exact genetic dosage × source linear assurance self seed production identity holds under these source biology settings regardless of visitor history. Its algebraic correctness must not be mistaken for cross-visitor ecological inevitability.

The old reference year8 source mean differs slightly from older 512-path reports because this stress assay deliberately uses 128 source demographic paths and different, documented per-history RNG streams. Source genotype Markov biology is unchanged.

### Evidence scope and next test

Only eight newly RNG-generated visitor histories from the SAME simulator, selected post discovery. No natural island measurements, no independent botanical visitor processes, no new prospective confirmatory cohorts (37110801 through 37110864 remain untouched), and no validated full SDE/SPDE. The year8 source survivor cohort is held identical across parent years but conditions on survival; this cannot identify independent physiological pollinator selection.

At most, the sign reversal shows conditional reproducibility in some stochastic source environments; it is not a general island evolution law. Subsequent research should prospectively lock a new visitor RNG history range and test true held-out outcomes, or seek independent empirical reproductive field data. Keep PR #420 Draft and the universal-sign-reversal / ecological-stabilization claims on HOLD.
