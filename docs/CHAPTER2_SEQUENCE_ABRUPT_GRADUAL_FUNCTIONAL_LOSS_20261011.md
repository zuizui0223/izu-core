# Chapter 2 — Does the *tempo* of pollinator functional loss determine which floral trait evolves first?

**2026-10-11; hypothesis and source implementation only, no admitted new evolutionary outcomes.** This is an intervention on pollinator *functional-optimum trait matching*, not the disappearance of insect individuals or the temporal order of allelic mutations.

## Why the initial functional-profile assumption had to be corrected

The prior exact 165-genotype-state tests #468–#471 fixed the PLANT's matching value at **0.20** while the historical original 48-founder evolving Model3 began with source mean **0.50** and nonzero founder variance. Transplanting the prior matched4 optima (0.15,0.35,0.55,0.75) to shifted4 (0.65,0.75,0.85,0.95) into the evolving founder landscape does **not** yield monotonically deteriorating initial pollination: at the clonal n48 reference matching=.5, investment=.5, assurance=.5, pollen delivery is about 27.21 at λ0, rises above 34 at λ.5, then drops to ~9.35 at λ1. Consequently, calling that gradual schedule a monotonic "pollinator shortage" would be scientifically false.

This project **does not silently reuse that assumption**. It freezes new source profiles with all visitor functional optima at or above matching=.50, and shifts them farther away, always with **four functional types**:

- Start `[.50,.55,.60,.65]` plus four small profile-specific optima offsets Uniform(0,.025), independently seeded for 16 synthetic external profiles.
- Finish `[.80,.85,.90,.95]` plus the SAME four offsets in each profile.
- Fixed breadth .20, effectiveness1, count4 and original Model3 visitor-to-pollen allocation. Reference X=I=A=.5, N48 yields **strictly decreasing total pollen delivery for every tested intermediate λ**. The runner refuses profiles that violate this check.

The alternate visitor schedule thus represents **controlled functional replacement away from the initial plant phenotype**, not fewer insects. Individual evolved plants with different matching genotypes may still experience different fitness consequences; this is part of the biological question.

**Functional slot interpretation:** The four visitor IDs `0–3` are bookkeeping slots whose optimum values are assigned by the controlled schedule. They do **not** track four individual insects changing their own inherited traits, and the Model 3 ecology does not distinguish repeated replacement of functionally different visitors from within-visitor evolutionary change. This study manipulates the net functional-service environment, not pollinator demography.

## Exactly what we manipulate

During the first 100 reproductive updates, replace the original four visitor optima with the mismatched four-type end profile either:

- **Gradual:** interpolate λ(t)=(t+.5)/100 over t=0–99.
- **Abrupt:** maintain the start profile for `k` updates, use ONE numerically interpolated profile for the boundary update, and then the shifted profile thereafter.

The breakpoint `k` and one boundary λ are computed **before any population evolution** from the original reproductive operator applied to a fixed clonal n48 baseline, so that:

```text
Sum[t=0..99] reference_n48_delivered_pollen(gradual[t])
  = Sum[t=0..99] reference_n48_delivered_pollen(abrupt[t]).
```

Both arms then remain at the same shifted4 functional composition from **update100 to399**. Therefore the treatments have equal initial reference cumulative pollen service and equal long-term endpoint composition, but very different *chronology*. The equality is baseline-reference-only: it is NOT true for each evolving population state, each maternal recipient, or natural pollinator abundance.

This is a much sharper timing intervention than comparing abrupt pollinator absence against gradual decline with dramatically different cumulative pollen exposure.

## Original genetics and demographic controls

- The EXACT unchanged original `scripts/model3_island/reproduction.py::reproduce` and `scripts/model3_island/population.py::advance` execute all mating, paternal/maternal pollen transmission, selfing, Mendelian inheritance, finite demography and mutation.
- Original **48 diploid source founders** (seed74001, three trait allele means .50, s.d. .15, separate alleles), **K48**, survival0 and plant seed immigration0.
- Matching, floral investment I and autonomous assurance A ALL have real original diploid variance and may evolve.
- Factorial across assurance timing `delayed/prior`, direct assurance cost `0/.5` (independent factors), and mutation probability `0/.01`.
- 16 independent artificial four-visitor-optimum profiles (seeds48271001–48271016) × four nested demographic repeats (seeds49271001–49271004) × 4 mating cost/timing conditions × 2 mutation rates × 2 visitor timing arms = **1,024 source trajectories of 400 updates**, but **16 synthetic environmental-profile sampling units**, not 1,024 independent ecological systems and certainly not natural islands.

## Primary scientific comparison, frozen before simulation

For each individual original diploid trajectory, use founder-relative:

- First sustained A increase ≥.05 over 20 reproductive updates (e.g. an event from t81 through t100 inclusive **counts** as crossed by update100).
- First sustained I decrease ≥.05 over 20 reproductive updates.
- Times within ±5 updates are categorized as near-simultaneous; missing/censored/unreached/extinct outcomes remain separate (A-only/I-only/neither).

Primary report: the *paired environmental-profile-level* difference in A and I crossing frequencies **by update100**, with the six-category order-classification table and all eight treatment settings. Secondary report includes conditional lag among both-crossed histories but never excludes noncrossers from unconditional outcomes, local paternal-inclusive fitness-gradient distribution at predefined times (not all-individual inference from an eight-person sample), pre-mutation `Cov(g,W)`, and unconditional occupancy at updates100/400.

One explicitly **two-sided** difference test and descriptive profile-cluster bootstrap is registered. There is no prechosen favorable "assurance-first" direction, post hoc horizon or resource retuning. Noninformative results with saturated survival and/or zero crossings are valid failures of the mechanism.

## Null and falsification

- **If** sudden and gradual replacements with same reference cumulative pollen lead to the same inherited order and mean changes, then the proposed pollinator-loss-tempo driver has no support within this 400-update synthetic contrast.
- **If** chronological order changes but persistence does not, then imposed visitor tempo matters for sequence but the conditional order is NOT established as a survival-benefiting mechanism.
- **If** the local investment beta changes sign immediately in both schedules, founder-relative A-first chronological observations may be more plausibly attributable to genetic supply, response rate, assortment, demographic stochasticity or the 20-update event definition rather than a delayed change from positive to negative individual investment selection.
- **If** alternative timing/cost backgrounds or mutation rates change results, state the effect is context-dependent. No cross-system generalization is warranted.

The pre-outcome design lives in `data/design/chapter2_sequence_abrupt_gradual_functional_loss_20261011.json`. The completed prospective four-setting #411, assigned expression-order #418 (pooled practical equivalence), prior historical paired-order #472 and original genome-replay #474 remain distinct evidence ranks. This synthetic test cannot infer the historical mutation order from phylogenies, nor prove natural island evolutionary suicide.

## Executable entry point and review gate

```bash
# Small engineering smoke ONLY, no biological decision:
python -m scripts.run_chapter2_sequence_abrupt_gradual_functional_loss_20261011 \
  --profile-seed 48271001 --repeat-seed 49271001 \
  --schedule abrupt --mating-timing delayed \
  --assurance-cost 0.5 --mutation-rate 0.01 --years 40 \
  --out /tmp/chapter2_abrupt_smoke.json

pytest -q tests/test_chapter2_sequence_abrupt_gradual_functional_loss_20261011.py
```

The complete-cohort execution framework is now implemented, but **NO full evolutionary outcomes have yet been admitted**.

- `scripts/run_chapter2_sequence_abrupt_gradual_batch_20261011.py`: exactly 1,024 original-ABM cases partitioned into **16 equal 64-case shards**, with immutable task identities and per-case atomic SHA256 receipts. Short smoke cases are explicitly named `_SMOKE` and never get a completed biological manifest.
- `scripts/summarize_chapter2_sequence_abrupt_gradual_functional_loss_20261011.py`: **refuses to summarize** unless all 16 full completed shard manifests, all 1,024 original full 400-update biological JSON files and receipt/source-design hashes are present. It groups all four demographic repeats within each independent synthetic visitor-profile cluster and compares abrupt−gradual at that unit, with predeclared two-sided descriptive cluster bootstrap (9,999 draws).
- `tests/test_chapter2_sequence_abrupt_gradual_campaign_20261011.py`: checks complete paired 1,024-case factorial, no reused/colliding cases, no inference from smoke, and strict failure on incomplete data.

Example engineering smoke:

```bash
python -m scripts.run_chapter2_sequence_abrupt_gradual_batch_20261011 \
  --out /tmp/chapter2_timing_smoke --shard-index 0 --shard-count 16 \
  --smoke-years 3 --case-limit 1
```

Full source campaign execution after final-head source CI and independent outcome authorization:

```bash
# The 16 shards may be distributed across workers, each with an isolated
# receipt/output directory whose results are combined losslessly later.
for SHARD in $(seq 0 15); do
  python -m scripts.run_chapter2_sequence_abrupt_gradual_batch_20261011 \
    --out /tmp/chapter2_timing_full --shard-index "$SHARD" --shard-count 16
done
python -m scripts.summarize_chapter2_sequence_abrupt_gradual_functional_loss_20261011 \
  --input-root /tmp/chapter2_timing_full \
  --out /tmp/chapter2_timing_readout.json
```

These are **execution instructions**, not a claim that 1,024 runs have already finished. No biological mean/CI is acceptable until the full source-proofed readout passes its completeness/receipt gates.


## Pre-evolutionary source prediction: when does investment selection turn negative?

A separate **source-only diagnostic** is included rather than treating first observed allele change as a selection-sign observation:

- `scripts/audit_chapter2_sequence_tempo_focal_sign_clock_20261011.py` runs the ORIGINAL native `reproduce` operator on a FIXED N48 clonal X=I=A=.50 population, holding all genomes constant.
- It calculates the full individual genetic return `W_i=.5F_i+.5P_i+S_i`, its focal investment gradient β_I and assurance gradient β_A, and the first update at which β_I becomes **negative beyond the predeclared ±.02 deadband** under the two dose-matched ecological schedules.
- All 16 visitor profiles × delayed/prior timing × cost0/.5 are retained (**64 diagnostic cells**), while initial β_A is tested against zero through the full matching gradient.
- A concrete independent mathematical source prediction for the first frozen profile seed48271001 is:

| Fixed-source mating rule | Abrupt schedule: β_I first negative | Gradual schedule: β_I first negative | Difference |
|---|---:|---:|---:|
| Delayed selfing, cost0.5 | update **30** | update **45** | −15 updates |
| Prior selfing, cost0.5 | update **30** | update **33** | −3 updates |

The current independent equation-level calculation gave baseline β_I≈+0.4655 and β_A≈+0.2168 for delayed/costly, and β_I positive→negative across the replacement profiles. This source-only prediction is subject to original-code CI regression tests, not a verified ABM genetic trajectory or a causal claim about historic island isolation.

**The key scientific separation:** identical first100-update reference *cumulative* pollen delivery does **not** force the same temporal sign crossing. Even if this model-internal local fitness clock is source-verified, whether allele change is advanced by 15 updates is a **separate empirical-like result** depending on genotypic variation, Mendelian inheritance, genetic source W covariance, drift, evolving matching phenotype and demographic feedback. The full cohort must answer that independently.

New source regression: `tests/test_chapter2_sequence_tempo_focal_sign_clock_20261011.py`. Nothing here upgrades the old 51/64 historical chronology to proved selection-mediated causation.

