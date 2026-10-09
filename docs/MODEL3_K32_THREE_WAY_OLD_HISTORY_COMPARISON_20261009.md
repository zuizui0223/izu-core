# Model 3 K=32, 8-generation three-way engineering comparison (2026-10-09)

## Fixed design and source boundary

This **numerical engineering experiment is not natural-island field data** or a new independent biological hypothesis test. Execute:

~~~bash
python -m scripts.compare_model3_three_k32_old_history \
  --out model3-k32-three-way-old-history.json --draws 512 --budget 8
python -m scripts.compare_model3_three_k32_old_history \
  --out model3-k32-three-way-old-history-budget3.json --draws 512 --budget 3
pytest -q tests/test_model3_three_way_old_history.py
~~~

Parameters: K=32, mutation probability 0, 8 annual updates; survival=0, seed immigration=0. The primary budget is 8; budget=3 is separately labeled **resource-stress sensitivity** under otherwise identical fixed conditions, so extinction can be interrogated rather than inferred from a non-extinction regime. **The biological parameter source is the frozen Chapter 2 `prior_selfing` config**, `data/design/chapter2_assurance_generality_20261006.json`, to match the existing three-arm K32 implementation. The fixed-support helper supplies *only the engineered founder genotype support*, not a separate reproductive-parameter regime. The visitor sequence comes only from old archived history **26110601 (near)** at time indices 0–7, and **never** from frozen prospective 37110801–37110864 cohorts. Fixed 27-class joint diploid genotype support is the pre-existing engineered four-founder/two-allele-per-locus comparison fixture, cloned to K=32. These engineered founders **are not** the historical biological eight-founder cohort; only the ecological visitor trajectory is from the old source history. No source biological code in scripts/model3_island is edited; every transition uses canonical reproduce() and Mendelian probabilities. This test is a *single* environmental visitor history with nested simulation draws, not n=512 independent ecological tests.

## Three mathematical objects

1. **Exact finite stochastic genotype-count Markov recurrence**. For each integer census, reconstruct every plant (so individual self-pollen exclusion is preserved), call canonical reproduce, draw the original capped-Poisson recruits, draw exact joint-diploid Mendelian offspring categorically. This has the same restricted transition law as the original ABM, rather than a new biological theory.

2. **Deterministic conditional-expectation plug-in closure**. At each generation, compute source-law offspring probabilities q, capped-Poisson expected recruits *conditional on being occupied* and multiply q by that number. Propagate approximate survival by multiplying 1-exp(-intensity). **For the next generation's source reproduction**, transform fractional expected genotype counts into finite parental individuals with mass-preserving largest-remainder integerization, documenting the L1 projection error. Therefore this model is neither a solution to a full deterministic PDE nor E[X_t] of the nonlinear finite Markov process. Avoid treating positive fractional genotype counts as realized genetic polymorphism. Report one-step analytic conditional genotype-presence/richness/Simpson predictions at the final *proxy parent* state to permit a more appropriate comparison than naive nonzero fractional support.

3. **Projected Gaussian integer-state closure**. It uses the *same* frozen reproduction/intensity, exact pre-projection multinomial first and second moments, but tangent Gaussian counts are clipped, re-normalized and largest-remainder integerized. It has no theoretical guarantee of genotype presence/loss equivalence and is **not** an SDE/SPDE. The finite-count lattice and all 3 loci are retained.

Exact and Gaussian arms propagate their **own** independent states across eight generations. Do not update from a reference state at each generation. Each arm runs 512 demographically independent repeats with seeded streams. A source-paired visitor trajectory does not make finite ensembles paired Monte Carlo observations.

## Metrics and their meanings

- Extinction probability, mean census, and their Monte Carlo standard errors. Zero trait values are **never** imputed for extinct populations.
- Mean of each of the three trait means **conditional on occupancy**, with SE among surviving nested demographic draws.
- Mean number of positive-count **joint diploid genotype classes**, per-class original founder genotype absence at generation 8 including and excluding extinct endpoints, and genotype Simpson diversity, 1-sum(count/N)^2 (zero convention only for an extinct *diversity index*, not for a trait).
- **Allele loss** across six initially available alleles (two at each locus), separate from genotype-class absence: in a no-mutation system genotype classes can reappear from parental Mendelian combinations, whereas alleles truly lost cannot return without immigration/mutation.
- Integer census and total-count conservation error (numerical correctness), largest-remainder parent projection L1 (deterministic approximation), and absolute deviations relative to the finite stochastic reference (model accuracy).

No ecological effect-size p-values, no cross-island claim, no posterior, no biological confirmation. Finite Markov comparisons use Monte Carlo estimates, which themselves have sampling error; benchmark errors are not all statistically resolved differences. Raw numerical receipt should be archived by workflow artifact **model3-k32-three-way-old-history**; do not write output claims until that CI run succeeds and the receipt is inspected.

## Known interpretation limits

The deterministic plug-in parent projection is essential because the unchanged original reproduction operator is defined on individual integer parents. The original continuous-density model density_step() is **not** automatically equivalent: it approximates pollination and genotype-class self-exclusion, and its positive-mutation grid-refinement issues remain separate. A discrepancy between exact finite and deterministic should **not** be assigned uniquely to demographic drift; nonlinear ecological payoffs, survivor conditioning and numerical projection also matter. Gaussian mean agreement does not establish tail, extinction or rare genetic-memory accuracy.

At most this is a source-locked eight-generation **numerical method comparison**, not evidence that islands evolve deterministically or stochastically and not a validated SDE or SPDE. Future independent visitor histories must be approved and prospectively isolated from #411/#418 confirmed results. This experiment must not alter their frozen claims.
