# Chapter 2 — Orthogonal capacity experiment: whole-cohort post-outcome mechanism-channel audit (2026-10-09)

**Status: EXPLORATORY AFTER SEEING THE OUTCOME.** The prospectively frozen primary result remains **`inconclusive`**, with mean +0.0018484189 and 64-history bootstrap95 [−0.0034583915,+0.0073367698]. Do **not** use the following channel comparisons as a second confirmatory test.

## Execution, provenance, full admission

- Original new t400 cohort: [GitHub Actions Run #37887039116](https://github.com/zuizui0223/izu-core/actions/runs/37887039116), 64 histories and 2,048 source genotypes; original source run SHA `c581d20313326b40233b438ca78fa1c55923b14c`.
- Original future experiment + frozen readout: [Run #37887290489](https://github.com/zuizui0223/izu-core/actions/runs/37887290489), 172,032 futures; future source SHA `e29116f3c2fb062be3da3f3ed9b3ca869499e220`. Immutable full readout is merged under PR #435, SHA-256 `e52d92a4586b92ca0aa3e93b560b2d603d63a9e9ee0b7fa61432a5b7f734d69c`.
- Read-only **full raw archive** replay: [Run #37890907635](https://github.com/zuizui0223/izu-core/actions/runs/37890907635), **success**. Audited all 64 future shards, 2,048 source receipts and 172,032 outcome cells *before* considering any exploratory channel result.
- Original machine-readable posthoc artifact: [chapter2-orthogonal-posthoc-mechanism-audit-20261009](https://github.com/zuizui0223/izu-core/actions/runs/37890907635/artifacts/11598298067).
- Exact execution code is `scripts/chapter2_orthogonal_mechanism_posthoc.py` on branch `chapter2/orthogonal-mechanism-readonly-20261009`, source-locked by the above Actions run. No biological history or future trajectory was regenerated.
- All estimated contrasts use the **64 visitor histories** as bootstrap units (9,999 draws; post-outcome descriptive seed `2026100951`). Branches, budgets and demographic repeats are not independent units.

## A real structural issue: capacity changes the pollen-delivery equation directly

Even when **the exact same eight diploid t400 founder genotypes and starting population size** are used for the F8/C8 and F8/C48 arms, initial female reproductive returns differ between arms. Across all authentic source/setting/visitor/budget/gate cases the **maximum absolute arm difference** at t0 was:

| Total population payoff at initial postshock update | Maximum absolute difference, F8/C8 vs F8/C48 |
|---|---:|
| Viable selfed seeds | 8.47888 |
| Viable outcross seeds | 18.92452 |
| Expected pollen export | 0.00000 |

These are **maxima across original case records, not history-average treatment effects**. Baseline and self-half gates retained identical t0 population counts; the self-half gate reduced viable selfed seeds by exactly 50% while leaving initial outcross seed production and expected pollen export unchanged.

The *canonical source code* makes the cause intelligible: in `scripts/model3_island/reproduction.py`, pollen-transfer recipient weights are normalized by

`affinity.sum(axis=0, keepdims=True) + config.capacity * config.background_ratio`.

Thus the capacity switch **simultaneously modifies** (i) local demographic carrying capacity / recruitment vacancies in `scripts/model3_island/population.py::advance`, **and** (ii) the dilution of pollinator-mediated pollen delivery among background floral resources. The second component acts **at t0**, before future population-size trajectories can diverge. In delayed-selfing settings, changing female outcross receipt also changes the amount left for selfing.

The registered manipulation does identify a **model-conditional composite intervention on the `capacity` parameter** with matched F8 genotypes. It **does not** identify *pure demographic ceiling dependence at fixed pollination background*. Genotype matching and common random-stream initializations cannot remove this structural coupling. This is an additional, distinct limitation of interpretation, not a numerical invalidation of the full-cohort experiment.

## New exploratory reproduction/persistence signatures

Define `D` as A-first minus I-first and `tau = D_baseline − D_self_half`. The following are **post-outcome descriptive sensitivity estimates**, averages over all predeclared settings, environments, nested repeats and log-weighted seven-budget axis:

| Channel \ population regime | F8/C8 | Same F8/C48 | All available founders/C48 |
|---|---:|---:|---:|
| Initial viable selfed seeds, `tau` | +0.16062 | +0.13489 | +0.99337 |
| Initial viable outcross seeds, `tau` | 0 | 0 | 0 |
| Initial expected pollen export, `tau` | 0 | 0 | 0 |
| Cumulative selfed recruits over 80 updates, `tau` | +5.326 | +26.008 | +20.908 |
| Cumulative outcross recruits, `tau` | −0.948 | −9.410 | −6.203 |
| Cumulative total recruits, `tau` | +4.378 | +16.598 | +14.705 |
| Terminal population size, `tau` | +0.04797 | +0.19442 | +0.08943 |
| Terminal occupancy, `tau` | +0.005770 | +0.003922 | +0.001121 |

The zero initial outcross/pollen sensitivity is expected **by the construction of the postzygotic gate**, not a newly discovered biological invariant.

For the **paired between-capacity sensitivity**, keeping the same eight founder genomes:

- Cumulative selfed recruits: F8/C8 minus F8/C48 `−20.682`, descriptive bootstrap95 [−31.159,−10.107].
- Cumulative outcross recruits: `+8.462`, bootstrap95 [+4.153,+12.838].
- Cumulative total recruits: `−12.220`, bootstrap95 [−23.500,−0.579].
- Early extinction by update 20: `−0.001108`, bootstrap95 [−0.00655,+0.00441].
- **Frozen terminal-occupancy primary remains** `+0.001848`, bootstrap95 [−0.003458,+0.007337], **`inconclusive`**. Exploratory resampling under a different seed also crosses zero.

The sizable 80-update recruitment differences are **cumulative over trajectories of unequal survival duration** and can reflect survival, competition, genetic change, founder composition and future demographic feedback. They do not establish a mediated fitness benefit, or imply that the difference in recruits is the cause of the terminal occupancy contrast. In particular, recruitment can vary while the registered binary 80-update outcome remains unresolved.

## What to test next without retrospectively changing the decision

The next genuinely discriminating experiment would orthogonalize **two independently controlled model levers**, not simply rerun the capacity contrast:

1. `K` = demographic carrying-capacity ceiling in `advance` (8 or 48).
2. `B` = background pollen-recipient dilution normalizer in `reproduce` (equivalent to capacity multiplier 8 or 48, **independent** of `K`).

A prospective design could use the exact same eight t400 founding genomes in all four `K × B` cells, new independent visitor histories, identical initial random-stream specifications and the same postzygotic selfed-viability intervention. It would isolate the direct pollen-dilution lever from the demographic vacancy ceiling in this **model**, conditional on the chosen background-ratio formulation. In implementing it, do **not** call the canonical `reproduce` with capacity 8 when population exceeds eight under `K=48`; that would violate the `n <= config.capacity` invariant. The correct design needs a *separately declared background-normalization override* while preserving the demographic capacity and reproduction conservation audit.

No such new 2×2 intervention has been launched or confirmed in this audit; no new natural-island claim is made.

**Revision to earlier narrative:** The independent result does not isolate a single demographic carrying-capacity mechanism; it tests a composite capacity parameter that alters both demographic ceilings and the pollen-sharing environment. The paper's stronger four-setting conclusion—that pollinator limitation reduces floral investment even with assurance evolution blocked, while assurance evolution compresses geographic investment divergence—remains unchanged.
