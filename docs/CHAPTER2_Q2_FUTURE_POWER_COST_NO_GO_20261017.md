# Q2: After the completed 384-case trial, what *could* be powered prospectively? (2026-10-17)

**Decision: do not run more original-Q2 biological paths or treat the existing `both_inconclusive` co-primary as confirmed.** Any follow-up is a **new study** with its own scientifically justified SESOI, independent founder/visitor pools, source-bound pilot, adverse variance sensitivity, compute budget and reviewed prospective plan. The `main` [power gate](../scripts/validate_chapter2_future_power_20261017.py) applies to future reserved `chapter2_future_registered_*.json` contracts; it does not retrospectively change the original 384 paths.

## Independently reconstructed original source

All **32 nested original Actions ZIPs** were re-opened outside GitHub, and 384 case NPZ source-SHAs, labels, the 8×8 paired far treatment contrasts, six-class cell counts, and **9,999 fixed-seed two-way founder/visitor bootstrap** were recomputed and matched the original [independent Q2 readout](audits/CHAPTER2_Q2_I_SUPPORT_384_ORIGINAL_READOUT_20261016.json):

| Registered far co-primary effect, dense 24 vs sparse 12 carriers | Original estimate | Two-sided Bonferroni-adjusted 97.5% CI | Original verdict |
| --- | ---: | --- | --- |
| Δ[P(A-first)−P(I-first)] | +0.109375 | [−0.125000,+0.343750] | Inconclusive |
| ΔP(I-decline event) | +0.187500 | [−0.062500,+0.421875] | Inconclusive |

**Important:** The first co-primary is an *order-score difference*, **not simply a difference of A-first proportions**. The case-level matched effects include both positive and negative values.

The independently reconstructed two-way sample-variance and residual-MS values exactly matched the frozen [retrospective precision record](audits/CHAPTER2_Q2_CROSSED_RETROSPECTIVE_PRECISION_20261017.json):

| Retrospective component | Order-score effect | I-event effect |
| --- | ---: | ---: |
| Raw variance among eight founder conditional means | 0.0376674107 | 0.0312500000 |
| Raw variance among eight visitor conditional means | 0.0287388393 | 0.0312500000 |
| Crossed residual mean square, **interaction+path noise not separable** | 0.2962372449 | 0.3316326531 |

These raw variances are **not** clean, mutually independent variance components: founder/visitor conditional means already include some residual noise. The source has one stochastic path per founder×visitor cell; founder×visitor interaction cannot be separated from finite-recruitment path noise. The finding that the founder conditional effect means range from **−0.125 to +0.500** is descriptive, **not** proof that founder variance is the unique cause of the wide confidence intervals.

## Sensitivity and execution cost: NOT a sample-size determination

The [merged prospective planning rule](../scripts/validate_chapter2_future_power_20261017.py) contains only an **assumption-based Normal MDE proxy**. Here the original source's *raw* founder variance, *raw* visitor variance, and *residual* MS are all kept (conservatively **double counting** some path noise):

\[
V_{\mathrm{proxy}}(n_F,n_V)
=\frac{v_F}{n_F}+\frac{v_V}{n_V}
+\frac{v_R}{n_F n_V},
\qquad
\operatorname{MDE}_{\mathrm{proxy}}
=(z_{0.9875}+z_{0.90})\sqrt{V_{\mathrm{proxy}}}.
\]

Bonferroni two-sided familywise α=0.05 is applied to two co-primary outcomes; a per-outcome directional power proxy of 0.90 bounds the family of two at 0.80 **by a union bound**, under the Normal assumptions. This is **not** an empirical power estimate for the completed Q2 study and does not guarantee actual joint coverage/power for a future six-category outcome.

| Hypothetical *new independent* founder×visitor labels | MDE proxy: order score | MDE proxy: I event | Full runs if original 2 environments×3 policies were reused | 200-update work |
| --- | ---: | ---: | ---: | ---: |
| 8×8 | 0.401 | 0.402 | 384 | 76,800 |
| 16×16 | 0.257 | 0.254 | 1,536 | 307,200 |
| 24×24 | 0.202 | 0.199 | 3,456 | 691,200 |
| 25×25 | 0.197 | 0.194 | 3,750 | 750,000 |
| 32×32 | 0.171 | 0.168 | 6,144 | 1,228,800 |
| 48×48 | 0.137 | 0.134 | 13,824 | 2,764,800 |
| 74×74 | 0.109 | 0.106 | 32,856 | 6,571,200 |
| 87×87 | 0.100 | 0.097 | 45,414 | 9,082,800 |

**These numbers are not registered scientific sample-size recommendations.** They are strictly the original 8×8 variance proxy held fixed while hypothetical independent label counts change; future true variation, category probabilities and visitor histories may differ. A follow-up must independently justify a *biologically meaningful SESOI*, including why the two co-primary endpoints must both succeed. Choosing **+0.109375 only because it happened to be the observed old order-score difference** would be outcome-conditioned sample-size tuning, not an independently justified prospective hypothesis.

The approximate matched-cost optimum under this simplified proxy is close to **balanced founder and visitor replication**: (\sqrt{v_F/v_V}\approx1.14) for the order score, ≈1.00 for I incidence (assuming comparable cost per added founder/visitor source). Expanding only the visitor histories while keeping eight founder labels would leave the founder variance proxy term unaddressed. This does **not** prove that the founder component is independently identifiable or dominates biological uncertainty.

## Actual decision now

**HOLD new confirmatory Q2 intervention** until a fresh independent pilot or defensibly external source supports the exact estimands and an independently justified SESOI, baseline and adverse variance scenarios, explicit randomized stream independence, and complete resource budget. The current [non-executable template](protocols/CHAPTER2_FUTURE_POWER_CONTRACT_TEMPLATE_20261017.json) stays **not an approved trial**. If the Normal approximation is doubtful, register the full data-generating process and do simulation-based operating-characteristic checking before authorizing new biology.

**Do not delay the supported Chapter 2 primary ecological claim solely to convert Q2's registered inconclusive contrast into significance.** The existing one-paper manuscript rests on the supported fixed-A non-necessity counterexample, conditional order observation and separate source-verified inherited-access limitation; see the [primary hypothesis decision](CHAPTER2_MAIN_HYPOTHESIS_DECISION_20261017.md). DOI-backed external preservation of the completed original source archive remains a separate publication blocker.

**Source:** original [Q2 manual Actions execution #38918737325](https://github.com/zuizui0223/izu-core/actions/runs/38918737325); retrospective [precision note](CHAPTER2_Q2_RETROSPECTIVE_PRECISION_FUTURE_POWER_20261017.md) and [source receipt](audits/CHAPTER2_Q2_CROSSED_RETROSPECTIVE_PRECISION_20261017.json).
