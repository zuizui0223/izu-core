# Independent Model 3 t0–200 visitor-removal test — source-readback verdict (2026-10-15)

**Evidence state:** The registered biological production workflow [38720038469](https://github.com/zuizui0223/izu-core/actions/runs/38720038469) successfully executed **all 16 source-locked shards**, with **2,048 genetically explicit new trajectories and 409,600 model updates**. Its final aggregation job initially **FAILED**, not because original biological output was invalid, but because an admission check incorrectly required exactly 48 plants **in every year**. Local independent re-read admitted all 16 original GitHub ZIP SHA-256 checksums, every case receipt and all full-array identity checks. Exactly **14/2048** trajectories temporarily had fewer than 48 plants (minimum 44), while **all 2048 ended with N=48** and genetic/update accounting held to 1e−12. The checked validator has been corrected to permit integer `0<N<=48`, without changing any biological trajectory or source parameter. A separate **readout-only** GitHub Actions recovery, when complete, is the cross-runtime certification; no rerun or re-selection of original paths is authorized.

## Experiment and estimand

The original frozen Model 3 source kernel was loaded byte-for-byte from the authenticated 2026-10-06 original model ZIP. The **64 new seed histories 28110601–28110664** (one seen in a disclosed 32-path engineering pilot), two *fixed* new founder genome backgrounds, four source reproductive rules and the paired treatments gave 2048 new native paths for 200 updates. Exposures are **native low-visitor far replenishment** versus **all visitor types removed from t0**. Policies are **A genetic evolution permitted** versus **A held at 0.5**, which still permits autonomous selfing. No wild-island data, naturally extinct colony or visitor compensation process is observed here.

For each history and founder, define `E−F` as final investment `I200(evolving A)−I200(fixed A)`. The registered interaction is `(E−F under native far visitors)−(E−F with zero visitors)`. Two fixed founder backgrounds are averaged **within** each history; bootstrap units are 64 visitor/demographic history clusters, not 2,048 independent ecology replicates. Interactions for the four rules have descriptive Bonferroni-family **98.75%** percentile-bootstrap intervals (4,096 draws). For transparency, exclude the 1 visible pilot seed in a separate 63-history panel; the frozen all64 design is also shown.

## Primary 63-holdout panel (excluding already-inspected seed28110601)

| Original mating rule | Native far E−F I200 | Zero-visitor E−F I200 | Registered interaction and 98.75% visitor-history bootstrap interval |
|---|---:|---:|---:|
| delayed_control | +0.00776 | +0.05867 | **−0.05092 [−0.08714, −0.01238]** |
| prior_selfing | +0.01814 | +0.05867 | **−0.04054 [−0.07502, −0.00670]** |
| pollen_discount | +0.02447 | +0.05867 | −0.03420 [−0.07637, +0.00428] |
| assurance_cost | +0.01290 | +0.03464 | −0.02174 [−0.06023, +0.01877] |

The registered **all64 panel** leads to the same scoped decision: interaction −0.04845 [−0.08811,−0.00994], −0.03849 [−0.07286,−0.00610], −0.03184 [−0.07367,+0.00654], and −0.01835 [−0.05798,+0.01952], same setting order.

**Primary interpretation:** Removing all visitors does *not* abolish the positive **relative** I preservation conferred by allowing reproductive assurance to evolve. In these two founder backgrounds and this 200-year horizon, zero-visitor E−F is **larger** than native-far E−F in delayed and prior selfing under the familywise history-cluster interval. Pollen discount and direct assurance cost have same-direction means, but their adjusted intervals contain zero. This is a synthetic-model causal contrast of assigned visitor condition × A policy; it is **not** causal identification of the original archived far-sign mechanism or natural-Izu evolutionary history.

**Control:** With exactly zero visitor pollen, the original reproductive equations for delayed control, prior selfing and pollen discount become identical (the same no-assurance-cost term); matched random streams therefore yield **the exact same 0-visitor paths in all three rules**, not three independent mechanistic replications. Direct A cost retains a distinct resource constraint.

## The source histories do not support a universal founder-independent effect

| Original mating rule | Interaction, founder 28111601 | Interaction, founder 28111602 |
|---|---:|---:|
| delayed_control | −0.00477 | −0.09213 |
| prior_selfing | −0.02822 | −0.04876 |
| pollen_discount | +0.02450 | −0.08818 |
| assurance_cost | +0.01391 | −0.05061 |

For delayed control, the mean interaction is primarily carried by one of only **two** genetically independent founder states; for prior selfing both are negative. The new 64 history streams are independent demographic/pollinator sequences but **not 64 independent founder genotypes**. No universal fitness law or drift share can be inferred from two backgrounds.

Nor is far or zero-visitor investment increasing absolutely. For example, the mean founder I is ≈0.50119, whereas delayed-control I200 is 0.40429 (native far A fixed) / 0.41185 (native far A evolvable) and 0.27185 (zero visitor A fixed) / 0.32786 (zero visitor A evolvable). **All four means fell from founder I**. Relative preservation, not absolute growth, is the finding.

## Price-weighted genetic response versus realized recruitment residual

The native yearly identity has been checked for each of 409,600 updates. The 63-history accumulated E−F in the conditional expected parental-genetic Price term (mean raw I units) is:

| Rule | Native far Price E−F | Native far realized residual E−F | Zero-visitor Price E−F | Zero-visitor realized residual E−F |
|---|---:|---:|---:|---:|
| delayed | +0.03174 | −0.02398 | +0.05620 | +0.00247 |
| prior | +0.04462 | −0.02648 | +0.05620 | +0.00247 |
| pollen discount | +0.02006 | +0.00441 | +0.05620 | +0.00247 |
| A allocation cost | +0.02347 | −0.01056 | +0.04061 | −0.00597 |

The sums exactly equal the corresponding E−F endpoint contrasts. With no visitors, the static fitness equation is `W_i ∝ exp(−c_I I_i²) × A_i exp(−c_A A_i²)`; its monomorphic **local I log-gradient is −2c_I I**, independent of A but **not zero**. Evolving A changes the distribution of parental genomes, offspring recruitment, genetic composition and their histories. These parental Price/residual columns are exact **state-dependent bookkeeping**, not a uniquely identified percentage due to selection, covariance, Mendelian sampling or drift.

## Decision for the Letter

1. The simplistic explanation “A evolves → visit loss stops all I selection → investment is retained” is inconsistent with original equations and the new contrast.
2. The result is informative for finite inherited multi-generation dynamics, but *does not uniquely explain* the larger original far E−F t1000 mean nor establish a founder-independent universal genetic law.
3. Q1 remains a source-verified model-specific consequence built on prior cooptimization theory; **Q2 response order and Q3 finite inherited realization** remain better candidates for the main conceptual contribution; Q4 survival is a distinct conditional study.
4. Preserve this experiment as a bounded source-backed Supporting Information/mechanism check. To claim a broadly general mechanism, independently vary **founder genetics** (not only new visitor histories) and reproduce the signed interaction; do not search retrospectively for a favorable subset.

## Original source availability and admission

- Original biological output artifacts: [GitHub Actions 38720038469](https://github.com/zuizui0223/izu-core/actions/runs/38720038469) — all 16 shard jobs successful, each original ZIP and embedded .npz/.json receipt retained.
- [Immutable pre-activation protocol](protocols/chapter2_far_early_independent_visitor_knockout_20261015.json), source manifest hashed as `d1ddc2e70a453d1cdec5334563a53aadda6e4999e097d1c96744aca901a47b4a`; original protocol SHA-256 `330126dd47803b27443a62064260446255d359d791b2f33d08f9c837247d5a42`.
- [16-artifact checksum inventory](protocols/chapter2_far_early_readout_recovery_activation_20261015.json); original model source SHA cannot be silently changed between shards.
- [Fixed readout program](../scripts/summarize_chapter2_far_early_independent_visitor_knockout_20261015.py) and [regression test](../tests/test_chapter2_far_early_independent_visitor_knockout_20261015.py).
- A separate, original ZIP-verified independent full-cluster readout is retained outside the repository as `ch2_far_independent_2048_verified_readout_20261015.json`; import/deposit only after the readout-only Actions gate and provenance review.

**No journal submission, public archival DOI, natural-island causal claim, unadjusted single-rule generality, or new experiment was produced by this retrospective recovery.**
