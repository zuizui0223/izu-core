# Island pollinator-history reciprocal transplant — exploratory 2026-10-08 readout

**Inference status:** exploratory, NOT confirmatory; 4 independently generated visitor histories with 2 nested demographic repeats. No inference on natural-island fitness, causal temporal ordering, or evolutionary rescue.

## Executed screen and provenance

The protocol was declared on this branch before running the screen (see `data/design/chapter2_island_history_transplant_20261008.json`). A local 512-case replication used the archived biological source package (`sources.zip`) recovered from the hash-recorded **2026-10-06 generality campaign, shard 31**, along with the predeclared branch parameters. The isolated branch runner/summary, which is intended to reexecute the same biological rules, still requires separate CI-backed execution. Accordingly, these outcomes are labelled an **offline exploratory run**, not a CI-verified branch-result file.

- 128 common pre-switch populations; each forked at update 400 into four post-switch treatments, yielding **512/512 completed cases**.
- Four histories × two nested repeats; the 512 cases are **not independent experimental replicates**.
- All stored 128 group JSON cases and their SHA-256 receipts verified. Each group's four post treatments had identical switch-time population genotype snapshot hashes.
- All 512 post-switch populations were occupied at update 800. Minimum post-switch population size was positive in every case. Thus **no extinction or demographic rescue contrast is identified**.
- No new mutation after switch does **not** freeze inheritance or selection. The initial standing genetic variation and segregation remain active; mutation=0 merely suppresses new mutational input.
- The zipped run outputs and raw receipts have SHA-256 `9492d1448f7a26bb00d4aab23ada4375805ad9254470a4ff490b4223e39b37f8` (local review artifact, not an externally deposited DOI).

## The two inherited histories remain phenotypically different

Within each setting/mode/history/repeat, the founders were identical before selection and the newly generated visitor process for a given post environment was shared. The table below shows **far-pre minus near-pre** floral investment under common post=near conditions, in the evolving-assurance arm. Each cell is a mean of four history means (two nested demographic repeats per history).

| Reproductive setting | Difference at switch 400 | Endpoint with post mutation=0 | Endpoint with post mutation=.01 |
|---|---:|---:|---:|
| Delayed control | -0.1954 | -0.1948 | -0.1780 |
| Prior selfing | -0.2138 | -0.2008 | -0.1329 |
| Pollen discount | -0.1848 | -0.1901 | -0.1119 |
| Direct assurance cost | -0.2366 | -0.2313 | -0.2168 |

The corresponding common post=far treatments also retained negative endpoint history contrasts. Across all 16 setting × assurance mode × post-environment combinations, adding new mutation reduced the **magnitude** of the endpoint inherited-history contrast in 15 and increased it slightly in one (prior-selfing, fixed assurance, post-near). This is a descriptive count of model cells, not independent confirmation or proof of a universal mutation-mediated increase in evolvability.

The endpoint gap could reflect inherited starting differences rather than divergent ongoing selection; these data do **not** identify a unique path-dependent adaptive basin or selection mechanism.

## Payoff consequence: viability and outcross need not rank histories the same way

Immediately at the switch, both historical populations encountered the same first post-switch visitor community. The following common-environment outcomes are **far-history minus near-history per resident plant**, evolving assurance only:

| Setting | Difference in viable maternal output | Difference in female outcross output | Difference in pollen export |
|---|---:|---:|---:|
| Delayed control | -0.069 | -0.722 | -0.732 |
| Prior selfing | **+0.378** | -0.072 | -0.533 |
| Pollen discount | **+0.261** | -0.344 | -0.344 |
| Assurance cost | -0.362 | -1.026 | -1.272 |

Prior-selfing viable maternal contrast was positive in all four independently generated visitor histories (history means +0.400, +0.292, +0.774, +0.043); pollen-discount was positive in three of four. These are 4-history descriptive replicates; do **not** report confidence intervals or sign-test evidence.

In these rules, the formerly low-replenishment population can produce **more viable maternal offspring through elevated assurance while providing less outcross function** under the same contemporary visitor regime. This is the precise payoff trade-off potentially worth prospectively confirming. Pollen export is not equivalent to total male genetic fitness, because selfed offspring contribute both parental genome copies. Immediate viable maternal output is not extinction probability or later population growth at a fixed carrying capacity.


## Post-outcome fixed-state payoff intervention: investment versus assurance

After inspecting the viable-maternal sign differences above, we executed a **new, explicitly post-outcome diagnostic**. For each setting/history/repeat/mode pair, the complete finite population was evolved independently for 400 reproductive updates in both historical environments. At the switch, for each resident matching background we clamped *both inherited alleles* for investment and assurance to either the near-history or far-history **population mean**, in a 2 × 2 factorial, using the **same visitor community**. The effects are the average of the two simple changes at the other trait level, and their factorial interaction. Clamping changes trait variance and the observed history effect also includes matching and covariance; these effects are *not* causal dynamic mediation fractions.

In the **near-history matching background**, evolving-assurance mode, differences in viable maternal output after switching population mean values from near-history to far-history were:

| Setting | Change from investment mean | Change from assurance mean | I × A factorial interaction | Observed whole-population history contrast |
|---|---:|---:|---:|---:|
| Delayed control | -0.063 | +0.083 | +0.028 | -0.069 |
| Prior selfing | **+0.194** | **+0.168** | +0.026 | **+0.378** |
| Pollen discount | +0.029 | **+0.264** | +0.022 | **+0.261** |
| Assurance cost | **-0.302** | +0.055 | +0.137 | -0.362 |

The **far-history matching background** produced the same broad reading for the two positive viability settings: prior-selfing investment +0.214, assurance +0.160; pollen-discount investment +0.103, assurance +0.274. The cost setting remained negative for the investment change (-0.121), while the assurance change was positive (+0.103). All are uncalibrated, model-unit, descriptive four-history means.

Interpretation: similar low floral investment and high assurance states can correspond to *distinct underlying payoff balances*. In prior selfing, reduced investment allocation and assurance both raise immediate viable maternal output in the fixed-state counterfactual; under pollen discount, assurance dominates that direct change. In the costly-assurance setting, investment decrease has the opposite immediate maternal-output effect in this matched background. This is a stronger falsifiable mechanistic prediction than simple co-occurrence of a small floral phenotype and selfing. It does **not** demonstrate an increase in demographic rescue or prove that the same factorial attribution holds under natural island conditions.

Reproducible branch runner: `scripts/diagnose_chapter2_island_history_payoff.py`; source-archived offline exploratory counterpart: `payoff_factorial.py`, `payoff_factorial_raw.json`, and `payoff_factorial.log` in the separately maintained local review artifact.

## What this does and does not resolve for island ecology

This screen isolates selection *after* establishment and holds plant immigration absent; it does not model Baker's-law arrival filtering, real island distances, geological times, empirical pollinator populations, wind-pollinated floral evolution or the distribution of natural island traits. The trait is abstract floral investment, not measured corolla area. The two pre-environments are visitor-functional-type replenishment levels, not actual island identities.

**Candidate mechanistic claim for next independent test:** different ancestral pollination histories can create a latent **female viable-output versus outcross-transfer trade-off** under identical current pollination, and the sign of the viable-output contrast depends on how selfing is implemented (prior, delayed, discounted or costly). This prediction is more specific and falsifiable than generic eco-evolutionary feedback or “island syndrome causes smaller flowers.”

**Next falsification tests:** (i) rerun the exact protocol on independent histories at sufficient history-level n; (ii) factorially clamp inherited investment and assurance states to test which trait changes the immediate payoff contrast while controlling matching; (iii) modify demographic risk **prospectively** if extinction/persistence is to be a claim; (iv) independently contrast post-establishment adaptation with founding/arrival filters. Direct intervention on *trait-change order* is still required before stating that order itself causes persistence or changes future adaptive capacity.

All outcomes are outside the frozen four-setting causal-necessity/attenuation confirmation used by the current Ecology Letters manuscript.


## Independently frozen 64-history payoff test (separate from the four-history exploratory screen)

After the first four visitor-history results were observed, the **new 64-history cohort, two nested repeats, four settings, two assurance modes, paired near/far prehistories and five primary sign/interval criteria were frozen before inspecting the new cohort** in `data/design/chapter2_island_payoff_confirmation_20261008.json`. The new cohort was then independently run from the archived biology source as 1,024 paired cases / 2,048 prehistories. Its local offline readout is recorded in `data/results/chapter2_island_payoff_independent_offline_20261008.json`; the separate GitHub Actions workflow rerun is not yet the provenance of these numerical values.

**Outcome: 4 of 5 preregistered criteria passed; the global all-five gate FAILED.** Do not reclassify it as all-confirmed or rewrite the fifth criterion.

| Predeclared sign at identical post-switch visitors, far-pre minus near-pre | History-level mean | 95% bootstrap | Pass |
|---|---:|---:|:---:|
| Prior selfing, evolving assurance, viable maternal > 0 | +0.3292 | [+0.2589, +0.4011] | yes |
| Pollen discount, evolving assurance, viable maternal > 0 | +0.3533 | [+0.2742, +0.4366] | yes |
| Assurance cost, evolving assurance, viable maternal < 0 | **−0.0131** | **[−0.1080, +0.0833]** | **NO** |
| Prior selfing, evolving assurance, female outcross < 0 | −0.1413 | [−0.1782, −0.1044] | yes |
| Pollen discount, evolving assurance, female outcross < 0 | −0.2774 | [−0.3835, −0.1740] | yes |

All estimates average the two repeats within each of the **64 independent visitor histories**, then bootstrap histories 9,999 times with the frozen seed 2810082026. The cost-setting sign prediction from the four-history exploratory sample did not generalize.

A different, **post-outcome explanatory** comparison shows that for every setting, the far-history minus near-history viable-maternal contrast was negative with fixed assurance but less negative or positive with assurance allowed to evolve:

| Reproductive setting | Fixed assurance: viable difference | Evolving assurance: viable difference | Evolving-minus-fixed interaction (exploratory) |
|---|---:|---:|---:|
| Delayed control | −0.3098 | +0.2891 | +0.5989 [0.4723, 0.7251] |
| Prior selfing | −0.1241 | +0.3292 | +0.4533 [0.3536, 0.5507] |
| Pollen discount | −0.1191 | +0.3533 | +0.4725 [0.3783, 0.5700] |
| Assurance cost | −0.2926 | −0.0131 | +0.2795 [0.1476, 0.4116] |

The delayed-control positive viability contrast is **new secondary evidence**, not one of the frozen five tests. The explanatory mean-clamping diagnostic also changes relative to the tiny exploratory cohort: at a near-history matching background, the viable-output shift attributed to changing assurance means is +0.335 delayed, +0.258 prior, +0.307 pollen discount, +0.050 costly; the corresponding investment-mean shifts are −0.059, +0.074, +0.040 and −0.083. These are fixed-state counterfactuals in a variance-clamped artificial population, **not** dynamic causal mediation.

### Island-ecological implication and stop line

The biologically testable distinction is between **female viable-output compensation** and **loss of outcross pollen transfer**. A formerly low-pollinator population can have greater maternal viable seed potential under the same present pollinator community even while delivering less outcross reproduction. But direct assurance costs can prevent a clear viability rank advantage; the frozen assay does not establish a general negative cost-setting contrast.

A single present-day flower phenotype or seed-set snapshot cannot, on its own, reconstruct which mating strategy or historic pollinator environment produced it. The observation is model-only and must not be translated into universal island-plant fitness or real-island extinction without empirical measures. This independent experiment ends at a **common-community immediate reproductive assay**, not a 400-year post-switch persistence assay; the earlier 512-case pilot had no extinction at all. Neither experiment establishes evolutionary rescue, an effect of trait-change temporal order itself, or long-term adaptive capacity.

Next manuscript test is an independently specified observation/field comparison that resolves maternal seed viability, realized selfing and outcross male function separately, not just flower size or a single seed-set metric. No current Ecology Letters manuscript claim is silently broadened by the 4/5 gate.
