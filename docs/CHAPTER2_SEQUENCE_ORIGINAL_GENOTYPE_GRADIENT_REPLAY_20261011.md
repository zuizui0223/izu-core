# Chapter 2 | Historical selection onset: source-identical diploid replay

**2026-10-11 — retrospective original-history instrumentation, not a new ecological experiment or prospective confirmation.** One manuscript direction: why A (autonomous selfing assurance capacity) and I (floral attraction investment) exhibit observed temporal precedence, and whether that precedence implies a necessary cause or subsequent survival benefit.

## Main result of archival feasibility inspection

The archived `data/results/model3_persistent_isolation_summary_20261005.json` records first sustained founder-relative and extra-isolation divergence crossing times for 64 history clusters. Original annual Model3 population case traces retain **N, trait means/variances and number of distinct alleles**, not every resident's diploid genotype per year. The raw model case `*.npz` stores genomes at **t=0,200,400,1000 only**.

Therefore neither the first annual *selection-gradient sign switch* nor its delay relative to A/I allele changes can be computed from trait means alone. The correct next step is to **replay the original exact visitor histories and independent random streams**, inspecting the complete original diploid `PlantState` before reproduction. This new auditor calls the SAME original `scripts/model3_island/reproduction.py::reproduce` and `population.advance` as the historical `scripts/run_model3_persistent_isolation.py`, with the actual original `exposure(seed,arm)`, founding allele seed **74001**, visitor seeds **76001–76064**, nested demographic replicate seeds **7101–7108**, no changes to reproduction, survival, mutation or mutation supply.

## Recorded estimands are deliberately distinct

1. **Exact realized year-by-year genomic state:** original N, mean/variance of the three diploid traits, unique allele counts, numbers of visitor functional types and total delivered pollen. This uses the original population transition with its original keyed RNG streams.
2. **Expected inherited directional response** at the *existing* genomic state, before newborn mutations:

   `W_i = 0.5F_i + 0.5P_i + S_i`; `E[offspring trait mean | at least one locally recruited offspring] = sum_i W_i g_i / sum_i W_i`. We record expected investment and assurance change relative to current adult mean. This is the actual source Price covariance (given original Mendelian parent-pair sampling), NOT the same as a local one-focal derivative. Mutation at historical rate .01 means this is **pre-mutation** directional expectation, not a prediction of exact realized change.

3. **Sampled finite one-individual local gradients:** at each selected early reproductive update perturb the two parental homologs for **one focal at a time** by `±0.005`, leave all other individuals unchanged, and compute `d log(W_i)/d I_i` and `d log(W_i)/d A_i`. F, P and S are all included. The default eight representative adults are selected deterministically across the focal trait ranking; the runner also supports `--sample-n 0` to evaluate ALL adults. The code records *number sampled and number for which a bounded central difference is available*, plus the median, minimum, maximum and counts of positive/negative/near-zero source gradients.

   **Important:** eight sampled gradients are NOT a census-wide selection sign, and the sign of a group covariance need not equal a local one-individual derivative. No missing gradient near allele boundaries is imputed.

## Source identity gate

There are two evidence ranks:

- **Replay from original algorithms without archived raw case comparison:** original RNG seed and algorithm source faithfully executed, and independent uninstrumented original prefix transition checked with regression tests. This is a valid *new retrospective calculation* but not an exact recovered original archived genotype trajectory merely because the seeds match.
- **Archive-matched original replay:** user supplies original raw `outputs/model3_persistent_isolation_20261005/persistent_core_...far.npz` and `outputs/model3_full_mutation_20261004/core_...near.npz` with their individual JSON SHA256 receipts. The runner verifies task identity, original case-file SHA256, the entire trace prefix and every available diploid checkpoint t0/200/400/1000. On a single mismatch it raises an error and **cannot** report archived case identity.

There is no original raw case archive in the GitHub current repository tree. The production GitHub artifact/archive location must be recovered if exact original correspondence is to be claimed for the entire 64×8 historical collection; unit tests alone do not replace it.

## What an actual selection-timing result would require

After archival identity verification, evaluate the same 64 histories, both near/far, all eight nested repeats, and preferably every adult at each specified early update. Compare separately:

- first date of **marginal** investment and assurance gradient positive/negative classification under all living source states;
- first date of **genomic** 0.05 trait change sustained 20 updates (existing frozen rule), preserving extinct and non-crossing histories;
- functional pollen mismatch, visitor richness and delivered pollen, and plant N through the same histories;
- historical selfing timing/cost (the present delayed/costly versus prior/cost-free historical comparison is doubly confounded).

The original 51/64 assured-first historical result is independently archived, but proving it was caused by an earlier selection sign switch is **NOT yet possible** without the full matched replay and a new independent loss-timing intervention. The present code is an enabling audit of a bounded original model history, not confirmation that the first response was adaptive or necessary.

## Reproduction

```bash
python -m scripts.audit_chapter2_sequence_source_genome_replay_20261011 \
  --setting assurance_cost --seed 76001 --rep 7101 --arm far \
  --years 1000 --gradient-until 80 --sample-n 8 \
  --archive-root outputs \
  --out /tmp/model3_76001_7101_far_source_selection_replay.json

pytest -q tests/test_chapter2_sequence_source_genome_replay_20261011.py
```

For a short original-RNG sanity check without archived data, omit `--archive-root` and use `--years 14`. The output explicitly marks such replay as **not archive-verified**. No background pipeline is asserted to be running. No redefinition of #411, #418, #422, #442 or the frozen 0.05/20-updates sequence diagnostic.

**Next decision:** find and verify original raw historical NPZ/receipt archives, then use source-matched annual gradients to test the hypothesized mechanism instead of describing it as already supported. A separate prospective abrupt-versus-gradual functional-pollinator replacement study can then test timing causally, controlling flower genotype, source pollen, census and total exposure.


## Source-cohort identity upgrade: one COMPLETE eight-replicate paired historical comparison

Companion runner `scripts/audit_chapter2_sequence_paired_original_replay_20261011.py` replays the preidentified **source visitor history76001**, both original near/far arms and **all eight original demographic repeats 7101–7108** under the 2026-10-05 delayed-selfing/costly setting, mutation rate0.01. Thus **16 original genomic trajectories** share the same original founders and streams; there are still only **one original independent visitor-history cluster**.

For this history, the original frozen 1000-year event record establishes that all six crossing events (founder-relative far and incremental far-minus-near, thresholds0.025/0.05/0.10) first cross by update43. Consequently the original 20-update sustained-crossing contract can be checked from an exact replay of **the first 100 updates**, without inventing new times for events originally censored later.

The companion reader repeats the **exact original eight-replicate mean-available and jointly-occupied pairing** of `scripts/summarize_model3_persistent_order.py`; it compares each detected event time/category to the existing frozen `data/results/model3_persistent_isolation_summary_20261005.json`, failing on **any** mismatch. A focused regression runs all 16 trajectories and pins the original threshold0.05 values:

| History76001 within 100 original reproduced updates | Assurance crossing | Investment crossing | Frozen category |
|---|---:|---:|---|
| Far arm relative to its own founder | 5 | 20 | assurance first |
| FAR-minus-NEAR increment | 17 | 15 | near-simultaneous (within 5) |

These are the **original archived source event values**, not new model outcomes; the paired replay makes their original diploid source provenance checkable from exact seeded transitions. Passing six event assertions independently corroborates the original crossing times for one history, but it is **NOT a substitute for bytewise matching all raw historical 1000-year NPZ/receipts** and does not by itself explain the selection mechanism.

```bash
python -m scripts.audit_chapter2_sequence_paired_original_replay_20261011 \
  --years 100 --gradient-until 50 --sample-n 4 \
  --out /tmp/chapter2_sequence_76001_original_pair.json

pytest -q tests/test_chapter2_sequence_paired_original_replay_20261011.py
```

We do **not** claim that the main environmental cause of precedence is proven. This checks the foundation before comparing *local full-W beta sign onset* to *genomic change onset*. A single-model original replay remains retrospective even if it reproduces every published source event.
