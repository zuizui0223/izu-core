# Sustained isolation: endpoint and process-order evidence

The 1,000-period extension is complete: 2,048 new far cases and 2,048 matched existing near references. Each setting/mutation combination has 64 visitor histories and eight demographic repeats. All new far traces match the original history experiment through period 200. Isolation remains different throughout this extension; the original common-environment experiment is preserved separately.

## Endpoints

More-isolated minus less-isolated at period 1,000; descriptive 95% history-bootstrap intervals (5,000 resamples), conditional on paired persistence. These are not multiplicity-adjusted tests.

| Setting | Mutation | Investment difference [interval] | Selfing-capacity difference [interval] |
|---|---:|---:|---:|
| Delayed, capacity cost 0.5 | 0 | -0.141 [-0.164, -0.117] | +0.034 [+0.023, +0.045] |
| Delayed, capacity cost 0.5 | 0.01 | -0.313 [-0.332, -0.296] | +0.100 [+0.090, +0.111] |
| Prior, capacity cost 0 | 0 | -0.030 [-0.043, -0.018] | +0.004 [-0.002, +0.009] |
| Prior, capacity cost 0 | 0.01 | -0.020 [-0.031, -0.010] | +0.002 [+0.0005, +0.0032] |

Matching-position intervals include zero in all four combinations. Paired persistence is 511/512 for delayed/zero-mutation and 512/512 otherwise. Settings jointly vary selfing timing and cost; their contrast cannot identify timing alone. Periods are uncalibrated reproductive updates, not years.

## Two temporal questions

Reporting priority after user clarification: the primary interest is the order of within-population changes, not whether capacity evolution is necessary. The fixed-capacity experiment is supporting mechanism evidence and must not replace this temporal question. Use the main cohort with standing variation in both traits; the homogeneous-capacity intervention has a different starting condition.

The exploratory diagnostic was declared before temporal readout: change of 0.05 maintained for 20 periods; events within five periods are near-simultaneous. Unreached events remain censored. Threshold sensitivities 0.025 and 0.1 are retained in the results.

For delayed selfing with positive mutation:

- Within more-isolated populations relative to founders, capacity rises first in 51/64 histories; 13 are near-simultaneous. Both events occur in all 64. Median crossings: capacity 6, investment 36.5.
- For the additional far-minus-near divergence, investment changes first in 32 histories, capacity first in 10, and 20 are near-simultaneous. Two reach only the investment threshold. Among the 62 jointly crossing histories, median crossings are investment 24.5 and capacity 34.

These are compatible: both treatments can increase capacity early before their additional difference in capacity becomes large. Temporal precedence does not establish mediation. The completed fixed-capacity intervention now supplies a separate test of whether investment can decline without capacity evolution; fixed capacity does not hold realized selfing constant.

### Within-population ordering across declared thresholds

More-isolated treatment, positive mutation,64 visitor-history means (8 demographic repeats each):

| Joint setting | Change threshold | Capacity first | Within5 updates | Investment first |
|---|---:|---:|---:|---:|
| Delayed, capacity cost0.5 | 0.025 | 51 | 13 | 0 |
| Delayed, capacity cost0.5 | 0.05 | 51 | 13 | 0 |
| Delayed, capacity cost0.5 | 0.10 | 57 | 7 | 0 |
| Prior, capacity cost0 | 0.025 | 17 | 47 | 0 |
| Prior, capacity cost0 | 0.05 | 38 | 26 | 0 |
| Prior, capacity cost0 | 0.10 | 54 | 10 | 0 |

Both events are reached in all64 histories for these cells. At the primary0.05 threshold, median crossing times (capacity,investment) are(6,36.5) for delayed and(3,10) for prior. Median paired lags are24 and6 updates respectively; these are not differences between separate medians. A threshold crossing is not the first infinitesimal onset, and the two traits'0-to1 scales need not represent equivalent biological change. In particular, early small changes in the prior setting are usually near-simultaneous. No universal claim that capacity initiates first follows from the threshold analysis.

Figure: `outputs/figures/model3_temporal_order_20261005/temporal_order.pdf`. Scatter points pair the two crossing times for the same history. Bars retain all three declared thresholds. The accompanying CSV includes all768 far-treatment events across both mutation rates; censored zero-mutation cases remain empty, not assigned a fictitious endpoint. Current source verification independently rechecked all2,304 crossings in the complete diagnostic.

## Ecological scope and Q1 connection

Isolation reduces visitor arrival rate; ongoing arrival and loss generate communities, and count-scaled activity lets visitor numbers affect pollen delivery. Reproduction, investment cost, selfing and inbreeding depression determine offspring contributions. No floral direction is imposed.

Endpoints establish model-conditional isolation effects, not a quantified mediation chain. Visitor scarcity, pollen delivery and viable selfed/outcrossed contributions need direct reporting before assigning pathway contributions. Q1 H2 motivates whether investment reduction requires greater selfing; this is not causal validation of the observational estimate. Abstract investment does not separately represent colour or accessibility, and the model is not fitted to regional patterns.

## Evidence and remaining scope

### Visitor exposure audit

Regeneration of all 64 paired histories was checked against the frozen source archive before readout. Both arms start with four visitor types and share the same per-type loss hazard. Across the 1,000 used snapshots, mean visitor-type count is 4.849 near versus 0.305 far; absence fractions are 0.00730 versus 0.75873. The mean longest absence spell per history is 4.48 versus 218.66 periods. Between the 999 observed snapshot transitions, mean established additions are 237.63 versus 11.78. ID-based counts satisfy initial count + additions - losses = final used count for every history.

Thus this strong isolation contrast creates prolonged visitor absence, not merely a modest reduction in richness. Lower replenishment produces that outcome without increasing the per-type loss hazard. These are severe arrival-limitation conditions, not calibrated estimates for typical islands. Shared exogenous histories are counted once, not repeatedly across reproductive settings or demographic replicates. No plant-to-visitor feedback is represented. See `data/results/model3_visitor_exposure_20261005.json` and `scripts/audit_model3_visitor_exposure.py`.

- Design: `data/design/model3_persistent_isolation_20261005.json`.
- Temporal declaration: `data/design/model3_temporal_order_diagnostic_20261005.json`.
- Results: `data/results/model3_persistent_isolation_summary_20261005.json`.
- The original summarizer checks raw tasks/hashes, frozen sources and first-phase equality and refuses partial campaigns.
- `python -m scripts.verify_model3_persistent_readout` independently checks 2,304 crossings, eight endpoint rows and recorded digests without overwriting results.
- Six tests passed in `test_model3_temporal_order.py` and `test_model3_persistent_isolation.py` on 2026-10-05.

These are finite-ABM results. The separate 65-node fifth-update probe passed local marginal accuracy (relative L1 1.31e-12). Long-run accumulated accuracy, grid convergence, positivity and positive-mutation deterministic/diffusion ecological comparison remain incomplete. Overall closure remains open.
