# Chapter 2 — Prospectively frozen postzygotic seed-viability factorial: final readout (2026-10-09)

**Scientific status:** All 2,048 frozen diploid ancestral states and 229,376 complete future cells were admitted. The **predeclared primary controlled self-viability sensitivity passed** in the synthetic 8-founder/capacity-8 regime; secondary evidence limits remain important.

## Frozen sources and exact audit

- Original pre-outcome factorial design: `data/design/chapter2_postzygotic_viability_factorial_20261009.json` (PR #426); complete run infrastructure merged in PR #427.
- Actual [GitHub Actions run #37869990792](https://github.com/zuizui0223/izu-core/actions/runs/37869990792), **completed / success**; executed source SHA `9f69db754ede497b012f4e7dcba5d2aaae9c090a`.
- Exactly **64/64 new-future shards** and the preflight and final readout succeeded; no failed shards. Each of 2,048 sources generated **84** new counterfactual future cells (three attenuation gates × 28 postshock conditions), totaling **172,032** new futures.
- Independent admission reverified all 2,048 pre-existing complete t400 diploid source states, their state checksums and pedigree provenance, **57,344 unmodified archived baseline** future cells, and all 172,032 postzygotic-intervention futures, **229,376** cells total.
- Machine-readable exact original artifact: [`postzygotic-factorial-full-adjudication`](https://github.com/zuizui0223/izu-core/actions/runs/37869990792/artifacts/11590096413).
- Archived original bytes: [`results/chapter2/postzygotic_factorial_confirmatory_readout_20261009.json`](../results/chapter2/postzygotic_factorial_confirmatory_readout_20261009.json); SHA-256 `41b6513a762f8e1d1be7df8ec3533812abc1fc23dd0a37ea78f7c02c1f2826ca`.
- Exactly **64 visitor-history clusters** are treated as independent bootstrap units. The 229,376 futures are paired/nested experimental branches, not 229,376 independent histories.

## Primary result — selfed-seed viability sensitivity is supported

The assigned historical phenotype-expression order (A-first versus I-first) was randomized previously. These futures reuse the exact already-exposed 64 historical visitor histories and their immutable evolved t400 genotypes. Only **viable seed contribution *after fertilization*** was intervened upon, at each of 80 future reproductive updates, without changing visitor histories, pollen transfer, initial genotypes or random-number identifiers.

Within each history, integrate the 4 mating-rule settings, historical near/far conditions, 2 demographic repeats, 2 future visitor environments, and 7 originally frozen log-weighted ovule budgets, all in the synthetic **8 founders / capacity 8** primary regime.

| Controlled seed-retention gate | A-first minus I-first terminal occupancy | 95% visitor-history bootstrap |
| --- | ---: | --- |
| Baseline selfed=1, outcross=1 | **+0.01208971** | [+0.00675347, +0.01748078] |
| Selfed half, outcross=1 | **+0.00394459** | [+0.00121169, +0.00666289] |
| Selfed=1, outcross half | **+0.01126288** | [+0.00621231, +0.01612581] |
| Both half | **+0.00504580** | [+0.00265916, +0.00742135] |

**Frozen estimand:** `tau_self = (A-first − I-first)_baseline − (A-first − I-first)_self_half`.

- Estimate: **+0.00814511806** occupancy probability (= **+0.8145 percentage points**).
- 95% 64-history paired bootstrap: **[+0.003708083, +0.012773055]**.
- Prespecified positive/negative two-sided support rule: interval excludes 0 and absolute mean ≥ **0.005**; **PASSED**.
- Frozen main verdict: `nonzero_controlled_self_viability_sensitivity`.

Reducing postzygotic viable selfed seed output by half attenuates the existing small A-first absolute survival advantage under strong 8-founder bottleneck conditions. The baseline contrast was 0.01209; the attenuated contrast 0.00394, i.e., around two-thirds smaller **on this model probability scale**. This is a controlled *model* sensitivity, not a measured selfing-mediated genetic indirect effect.

## Contrasts that do NOT independently support a general mechanism

- Outcross-half sensitivity in the 8-founder regime: **+0.00082683**, 95% [−0.00268029,+0.00412480]; no resolved positive effect.
- 2×2 factorial nonadditivity: **+0.00192803**, 95% [−0.00165862,+0.00551550]; does not resolve interaction.
- No bottleneck / capacity 48: the selfed-half sensitivity was **−0.00128290**, 95% [−0.00477814,+0.00224615]; no analogous supported positive sensitivity in that synthetic regime. Both near/far and all seven budgets are available in the machine JSON.
- Near/far decomposition of the primary capacity-8 schedule contrast: baseline **near +0.01656, far +0.00762**; selfed-half **near +0.00641, far +0.00148**. This does **not** prove a specific far-island rescue mechanism.

Thus the supported primary response is **conditional on the predeclared severe founder/capacity stress**. Do not generalize it to unrestricted capacities, all ecological environments or natural islands.

## Counterfactual manipulation fidelity

- Exactly unchanged original model reproductive ledger in unattenuated baseline; exact baseline futures were **read from their previously audited archive**, never rerun to change the benchmark.
- Frozen old-history smoke before full execution matched the canonical no-op future exactly; per-treatment mass/accounting tests checked maternal, outcross, selfed and paternal expected offspring consistency.
- Under self-half, the primary A-first−I-first initial viable-selfed-output contrast changes **+0.396341 → +0.198171**, while female outcross initial output remains **−0.236956** and expected pollen export remains **−0.798532**. Under outcross-half, the original initial outcross-output contrast halves, and the original expected pollen export remains unchanged.
- Postshock 80-step cumulative selfed and outcross recruit counts are documented in the JSON but **depend on persistence time**. They cannot serve as independently randomized causal mediators of the occupancy difference.

## Scientific interpretation and non-negotiable limits

1. This is **prospectively specified conditional perturbation** on previously exposed inherited states, not a completely new independent prehistory cohort and not a study of *naturally observed genetic-first-change order*.
2. The intervention changes viable seed supply for every future update, and therefore can change density, genotype frequencies and extinction hazard jointly. Even a positive controlled sensitivity does **not** identify a unique natural genetic or recruitment mediation pathway.
3. The historical PR #416 preregistered **far−near interaction** conclusion was *practically equivalent* within its old ±0.05 threshold. That conclusion is unchanged.
4. The later independent 3/4 intermediate-resource budget-window confirmation **failed** and stays failed. This new controlled gate does not retroactively confirm that exploration.
5. No environmental conditions or seed-viability fractions are calibrated from real Izu field survival data. A modeled *local population occupancy* advantage is not total genetic or lifetime reproductive fitness.
6. The phenotypic expression-order intervention was assigned by model history; its outcome is not a direct causal effect of spontaneous evolutionary change order.

## Next scientific decision

The supported finding motivates a focused explanation of **why viability sensitivity is detectable in the founder-limited population but not capacity 48**, e.g., recruitment bottleneck, demographic ceiling, reduced variation after founder sampling or stronger opportunity for stochastic extinction. These must be separated by matched interventions or explicitly frozen new designs, not by post hoc survivor conditioning or selecting favorable resource budgets.

No new evolutionary prehistory or unapproved biological simulation was launched by the result-archive pull request.
