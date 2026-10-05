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

The exploratory diagnostic was declared before temporal readout: change of 0.05 maintained for 20 periods; events within five periods are near-simultaneous. Unreached events remain censored. Threshold sensitivities 0.025 and 0.1 are retained in the results.

For delayed selfing with positive mutation:

- Within more-isolated populations relative to founders, capacity rises first in 51/64 histories; 13 are near-simultaneous. Both events occur in all 64. Median crossings: capacity 6, investment 36.5.
- For the additional far-minus-near divergence, investment changes first in 32 histories, capacity first in 10, and 20 are near-simultaneous. Two reach only the investment threshold. Among the 62 jointly crossing histories, median crossings are investment 24.5 and capacity 34.

These are compatible: both treatments can increase capacity early before their additional difference in capacity becomes large. Temporal precedence does not establish mediation. Investment decline independent of evolving capacity requires a fixed-capacity intervention; fixed capacity would still not hold realized selfing constant.

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
