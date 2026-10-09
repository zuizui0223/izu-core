# Chapter 2 — Independent intermediate-budget-window confirmation: final readout (2026-10-09)

## Run and immutable scientific status

- Frozen design: [`data/design/chapter2_order_budget_window_independent_20261009.json`](../data/design/chapter2_order_budget_window_independent_20261009.json), merged in PR #419.
- Complete independent prospective run: [GitHub Actions #37862121201](https://github.com/zuizui0223/izu-core/actions/runs/37862121201) — **completed / success**.
- Exact executed source SHA: `868164c24b6a6f17e7530941600fcb50e7281342`.
- Original machine artifact: [budget-window-independent-confirmatory-readout](https://github.com/zuizui0223/izu-core/actions/runs/37862121201/artifacts/11587460323).
- Canonical exact result snapshot: [`results/chapter2/order_budget_window_independent_20261009.json`](../results/chapter2/order_budget_window_independent_20261009.json), SHA-256 **`fa3d4103b3f3a84781c052907012a0dfed13caebb247c80f4c34b760a536cc58`**.
- All **64 prehistory shards**, **64 postshock shards** and **one final all-case audit** completed successfully, with all **2,048 full t400 diploid source states** and **57,344 futures** admitted before adjudication. They do not count as 57,344 independent ecological units.
- The new 64 visitor histories `38110901–38110964` were independent of the previously exposed `37110801–37110864`. The previous outcome was not used as a replicate in confirmatory inference.

## Preregistered primary verdict — NOT CONFIRMED

The prespecified intermediate-budget estimand is the history-paired **far–near difference-in-differences** of A-first versus I-first occupancy in the 8-founder/capacity-8 synthetic scenario, evaluated at budgets 3 and 4 relative to log-budget linear interpolation between the frozen flanking budgets 2 and 5.

| Frozen primary diagnostic | Value |
| --- | ---: |
| Fixed-window mean residual | **−0.0151491962** |
| 64 visitor-history percentile-bootstrap 95% interval | **[−0.0488260038, +0.0180349631]** |
| Fixed-window effect size threshold | 0.05 absolute occupancy |
| Window effect gate | **FAILED** |
| Held-out cubic-smooth baseline vs fixed-window indicator: mean MSE improvement | **−0.0000484355** occupancy² |
| MSE improvement 95% history-bootstrap interval | **[−0.0001413328, +0.0000426256]** |
| Required minimum MSE improvement | +0.0001 occupancy² and a 95% interval above zero |
| Out-of-history smooth-predictive gate | **FAILED** |
| **Frozen joint decision** | **`window_residual_practically_equivalent`** |

The 95% interval is wholly inside (−0.05, +0.05), but includes zero; within the stated **synthetic model and prespecified effect region**, the independent mean window curvature is practically equivalent to zero. This is **not** proof of an exactly zero effect. The additional 3/4 indicator slightly *worsened* held-out prediction relative to a cubic function of log budget, so the selected window is not independently justified.

### Previous exposed cohort vs new independent cohort

| Eight-founder primary regime | Previously exposed 64 histories (exploratory) | New independent 64 histories |
| --- | ---: | ---: |
| Budget 2, pooled DID | +0.000977 | 0.000000 |
| Budget 3, pooled DID | −0.064453 | **+0.002930** |
| Budget 4, pooled DID | −0.049805 | **−0.062500** |
| Budget 5, pooled DID | −0.009766 | −0.024414 |
| Predetermined 3/4 window residual vs log-budget 2/5 interpolation | −0.051666 (descriptive only) | **−0.015149** (independently adjudicated) |

A conspicuous negative budget-4 point in the new results is **not** sufficient to rescue the window hypothesis. The prior strong budget-3 signal disappeared, the fixed 3/4 contrast was small, and the out-of-history smooth comparator did not improve. Choosing budget 4 post hoc would constitute a new selection and is not confirmatory evidence.

### Mandatory no-bottleneck comparator

The unbottlenecked/capacity-48 scenario also failed both gates:

- Window residual mean **−0.0159264534**, 95% history bootstrap **[−0.0450242727, +0.0118198916]**.
- Held-out smooth-comparator mean MSE improvement **−0.0000002081**, interval **[−0.0000869659, +0.0000906173]**.
- Frozen decision: `window_residual_practically_equivalent`.

The comparison is between **synthetic stress regimes** and does not estimate extinction probabilities on natural islands.

## Setting heterogeneity is descriptive, not a new confirmatory gate

The full machine-readable result retains, without filtering, the four reproductive-setting-specific DID curves across all seven budgets, absolute near/far occupancy for both randomized schedules, and both shock regimes.

For the new primary-capacity-8 cohort:

| Reproductive setting | Budget 3 DID | Budget 4 DID |
| --- | ---: | ---: |
| `delayed_control` | −0.019531 | −0.035156 |
| `prior_selfing` | +0.039062 | −0.085938 |
| `pollen_discount` | −0.007812 | −0.089844 |
| `assurance_cost` | 0.000000 | −0.039062 |

The signs and magnitudes differ between settings and budgets; those subgroups were not independent new ecological units and do **not** justify changing the pooled prospectively frozen claim.

## What changed scientifically

- The preceding full-cohort PR #416 **general expression-order effect** was classified `equivalent_within_predeclared_ROPE`, despite excluding zero, because its magnitude was below its own preregistered minimum. That result is unchanged.
- The **post-outcome 3/4-resource localization** motivated this independent cohort. It has now **failed** its own two-part predeclared confirmation (fixed-window effect and smooth predictive separation).
- The historic failed independent16 *mutation-access-priority* result remains FAILED. These experiments manipulate **temporary expressed phenotype schedules**, not the naturally first-changing genetic locus.
- The data do not establish a universal resource threshold, an evolved-genetic-order rescue effect, or a naturally calibrated Izu plant-population survival mechanism.
- A smooth demographic probability floor/ceiling remains a plausible mechanism but was **not proven** merely by the failure of the window test. The specific cubic smooth model served as the prespecified predictive comparator, not as confirmation of a biological mechanism.

## Reproduction and next decision

```bash
gh run download 37862121201 --repo zuizui0223/izu-core \
  --name budget-window-independent-confirmatory-readout --dir /tmp/chapter2-independent-window
sha256sum /tmp/chapter2-independent-window/independent_window_confirmation.json
# expected: fa3d4103b3f3a84781c052907012a0dfed13caebb247c80f4c34b760a536cc58
```

**Next:** Preserve this negative confirmation and stop treating a hand-picked budget 3/4 window as a validated mechanism. A genuinely different biological question (for example, absolute occupancy effects versus DID or inheritance-mediated responses) requires its own pre-outcome definition and, when confirmatory, new independent histories. **No additional histories are approved or launched by this result-archival PR.**
