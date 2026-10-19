# Existing matched A/I endpoint repeatability

**Exploratory post-outcome readback, zero new biological updates.** Four original ZIP hashes and the two designs at the recorded source head were checked. The [receipt](audits/CHAPTER2_MATCHED_AI_REPEATABILITY_20261019.json) retains source identities, all-start occupancy and both epsilon0/.05 summaries. The [reader](../scripts/audit_matched_AI_repeatability_20261019.py) imports no model or producer.

The older 24,576-case bridge fixed A=.5 and cannot compare evolved A with I. A separate existing finite follow-up has both traits evolving: four settings, three initial states, 128 visitor histories, four repeats and paired near/far arms at census200 (12,288 arm trajectories).

## Attained states

Each row uses the same contexts for both traits, requiring all four repeats occupied in both arms. Compute sample variance across four repeats within each context, then average over contexts. Agreement counts and variance are different metrics.

| Setting | Start | Eligible /128 | Far variance A | Far variance I | Identical A endpoints | Identical I endpoints |
|---|---|---:|---:|---:|---:|---:|
| pollen_discount | outcross_like | 108 | 0.012635 | 0.014709 | 31 | 33 |
| pollen_discount | central | 128 | 0.002157 | 0.025431 | 111 | 16 |
| pollen_discount | selfing_like | 128 | 0.008138 | 0.021922 | 66 | 11 |
| delayed_control | outcross_like | 116 | 0.010462 | 0.018633 | 45 | 24 |
| delayed_control | central | 128 | 0.002645 | 0.023966 | 107 | 17 |
| delayed_control | selfing_like | 128 | 0.009725 | 0.025187 | 54 | 22 |
| assurance_cost | outcross_like | 101 | 0.009953 | 0.015212 | 42 | 30 |
| assurance_cost | central | 128 | 0.008545 | 0.021602 | 66 | 20 |
| assurance_cost | selfing_like | 128 | 0.014188 | 0.016179 | 25 | 27 |
| prior_selfing | outcross_like | 118 | 0.013330 | 0.016861 | 25 | 27 |
| prior_selfing | central | 128 | 0.002116 | 0.028320 | 111 | 7 |
| prior_selfing | selfing_like | 128 | 0.009277 | 0.025259 | 57 | 9 |

A has smaller far endpoint variance in all12 setting/start summaries. Exact endpoint agreement does not always rank A higher. This is a descriptive result about the attained state under these conditions, not a formal intrinsic-determinism ranking.

## A uniform contrast can be zero

Central-start counts at epsilon0 (all128 contexts eligible in each setting):

| Setting | A unanimous contrast signs | Of these all zero | I unanimous contrast signs | Of these all zero |
|---|---:|---:|---:|---:|
| pollen_discount | 100 | 100 | 26 | 25 |
| delayed_control | 103 | 103 | 32 | 12 |
| assurance_cost | 54 | 52 | 25 | 12 |
| prior_selfing | 117 | 117 | 36 | 36 |

More repeatable A endpoints therefore do not establish a consistently positive A response to reduced pollination. Near and far may attain the same A. These contrasts are terminal far-minus-near, not each trajectory's initial-to-final change.

## Limits and next step

- Post-outcome descriptive analysis; no p-values or confirmatory trait-ranking verdict.
- Five I/A allele nodes, M fixed at .5 and no mutation. Initial variation, boundaries and convergence can affect variance.
- Trait summaries are survivor-conditional; excluded contexts remain in the receipt's all-start occupancy counts.
- Four repeats per context cannot establish near-certain outcomes.
- Endpoint JSONs do not contain event order or genetic-closure timing, and do not test actual readaptation.
- This comparison required no new simulation. Search original trajectory archives before proposing any new timing/direction run.
