# Chapter 2: independent intermediate-resource-window confirmation (2026-10-09)

## Where the experiment stands

The complete 64-history PR #416 cohort finished successfully (Run [37856410822](https://github.com/zuizui0223/izu-core/actions/runs/37856410822)). The original **full-grid pooled** primary effect of assigned expression order was **practically equivalent** under the prespecified ±0.05 occupancy region: history-level DID = −0.013589, percentile bootstrap95 [−0.022812, −0.004302]. Even though the interval excludes zero, the practical-effect gate is not met. The historic failed independent16 mutation-access order test remains FAILED.

The original result then suggested a **post-outcome** pattern: with 8 founders/capacity 8, the budget-specific mean DID was −0.064453 at budget 3, −0.049805 at 4, +0.000977 at 2 and −0.009766 at 5 (averaged across the two future visitor environments). Using the originally published aggregate grid, the mean departure at 3 and 4 below *linear interpolation on log budget from 2 and 5* is approximately **−0.051666**. The no-bottleneck/capacity-48 counterpart is approximately **−0.023056**. These numbers are descriptive **hypothesis-generating** summaries: no history-level interval exists for the new selection, and the 64 exposed histories cannot be reused as a fresh confirmation.

## Distinct hypotheses

1. **Independent localized order effect:** transient A-first versus I-first expression histories leave a differential finite-population persistence signature localized at intermediate resource budgets, beyond a declared smooth trend.
2. **Smooth demographic-floor/ceiling effect:** resource supply drives occupancy smoothly from near-certain extinction to persistence. Even a constant genetic or phenotypic schedule effect can have an intermediate-budget maximum on the *probability scale*. A peak alone is therefore not evidence of an ecological threshold or nonlinear genetic mechanism.
3. **Historical-shock context:** a resource-window contrast may be accentuated by the experimental eight-founder bottleneck; compare the unbottlenecked/capacity-48 model without claiming the bottleneck is a measured natural-island process.
4. **No general order effect:** the original practical-equivalence result generalizes; any prior window pattern was multiple-comparison noise or environment-specific heterogeneity.

This is not a search over whichever new budget looks best. The window and flanks below are frozen **before the new seeds are executed**.

## What is frozen and how it is identified

Full machine contract: `data/design/chapter2_order_budget_window_independent_20261009.json`.

- **Independent visitors:** 64 fresh history IDs 38110901–38110964; two nested demographic repeats 38111901/38111902. None overlap the 37110801–37110864 previous cohort.
- **Biological source:** reuse the exact original t0–400 diploid genetics, A-first/I-first transient logit-offset assignments, founder rules, zero plant immigration, two historical environments, four reproductive settings and subsequent 80-update common future. No modification to the original model files, no relabelling of observed genetic crossing order.
- **Output:** 4 reproductive settings × 2 pre-environments × 2 assigned arms × 64 independent histories × 2 repeats = **2,048 complete t400 source states**. Each is forked to 2 stress regimes × 7 full original ovule budgets × 2 future visitor environments = **57,344 futures**.
- **Observed endpoint:** unconditional terminal occupancy (including pre-extinct sources) after 80 updates. Analyze by randomized assignment and all prespecified units, not by surviving genotypes, spontaneous A/I crossing or a selected future visitor regime.

For each new independent visitor history *h*, budget *b*, primary eight-founder regime, and averaging the four settings, future visitor environments and nested repeats, define:

`D_h(b) = [(S_Afirst,far - S_Ifirst,far) - (S_Afirst,near - S_Ifirst,near)]_b.`

The single predeclared *window curvature* estimand is:

`R_h = 0.5 * { [D_h(3) - L_h(3)] + [D_h(4) - L_h(4)] },`

where `L_h(b) = D_h(2) + (D_h(5)-D_h(2)) * ln(b/2) / ln(5/2)`.

A 64-visitor-history bootstrap (9,999 draws, seed 3811092026) yields the two-sided 95% interval. The signed direction was **not** locked as A-first favorable. A practical magnitude of at least **0.05** and interval excluding zero are necessary but **not sufficient** to declare the window effect.

### Mandatory nonwindow smooth competitor

A **history-out-of-fold** predictive test compares:

- **Smooth:** degree-3 polynomial in centered log(budget) for `D_h(b)`, fitted with fixed ridge = 0.0001.
- **Fixed window:** the same cubic smooth predictors **plus one prechosen budget-3/4 indicator**.

Partition the 64 histories into eight deterministic folds by history index mod 8. Fit on 56 entire histories and predict all seven budgets for each heldout set of eight histories. The outcome is the **per-history seven-budget mean-squared-error reduction** from adding the fixed window indicator. Bootstrap these 64 held-out improvements (using the same 9,999 history draws). The positive improvement interval must exclude zero and the average improvement must be at least **0.0001 occupancy²**.

**Confirm** only if the independent `R` magnitude/uncertainty gate **and** the out-of-history smooth-comparator gate both pass. A full R interval strictly inside (−0.05,+0.05) is a bounded practical-equivalence result; all other cases are inconclusive/not distinguishable from the declared smooth model.

This comparator is intentionally more flexible than a straight resource line, but it is **not the set of all smooth ecological mechanisms**; passing is predictive localization *relative to the specified cubic*, not mathematical proof of a discontinuity or a direct gene order effect.

## Mandatory guardrails and results to report

The run must also report the complete budget-specific DID curves (all seven budgets), setting-specific results, absolute A-first/I-first occupancy by historical near/far and resource budget, and the unbottlenecked/capacity-48 comparison. The former cohort's practical-equivalence verdict must remain the official verdict for its registered question regardless of the follow-up outcome.

`scripts/chapter2_order_budget_window_followup.py` has a plan-only mode which **never produces new biological histories**; it reuses the original full-diploid pedigree/source restoration audits, checks all 64 new shard identities before admitting all 2,048 genotypes and 57,344 descendant futures, and computes the fixed new inference only after all source hashes and fork receipts match. Synthetic tests assess false confirmation of cubic curves, positive/negative window signals and denominator integrity without sampling new visitors.

The manual `.github/workflows/chapter2-order-budget-window-independent.yml` defaults to `preflight_only`. A `main`-only, reviewed exact commit-SHA match and explicit `full_cohort_launch_approved=true` are required before production. There is no push-triggered new cohort and PR CI runs synthetic tests only.

## Scientific limit

The experiment distinguishes a **scheduled expressed phenotype order** effect under synthetic model assumptions, not the causal effect of the order in which inherited alleles naturally evolve. Distinct founder bottleneck scenarios are sensitivity treatments, not calibrated island conditions. A budget-3/4 peak may still emerge through a smooth logistic floor/ceiling mechanism; no inference from these simulations alone proves a natural evolutionary tipping point. All generalizations to Izu field populations await population-level reproduction, pollen transfer and recruitment observations.
