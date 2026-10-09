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
