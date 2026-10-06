# Current Ch2: ecological process decomposition

> **Routing decision, 2026-10-06:** the 2026-10-05 ecological results below are
> the paper-level controlling narrative on
> `codex/model3-full-mutation-closeout-20261004`. The full-mutation
> common-environment history experiment is retained as complementary genetic/
> history evidence, not the paper spine.

The **temporal-order claim** remains restricted to the delayed-selfing,
assurance-cost 0.5, positive-mutation setting. A separately preregistered
four-setting generality test has now broadened a different claim: investment
decline does not require assurance-capacity evolution, and assurance evolution
attenuates the near–far investment contrast across all four declared
reproductive settings. Temporal order and causal necessity remain separate.

The central result is not merely that reproductive assurance often changes
before floral investment. The key causal distinction is that **assurance can
change first without being required for investment decline**. At an identical
plant state, stronger visitor limitation lowers the marginal reproductive return
to investment; blocking assurance evolution therefore does not remove the
investment response. A second prospective intervention now confirms that allowing assurance
evolution reduces the observed near–far investment contrast across delayed
control, prior selfing, pollen discount and assurance-cost settings. This
attenuation is a common-four-cell interaction, not a mediation fraction; both
environments can still undergo substantial evolution.

Post-confirmation decomposition localizes 78–90% of the attenuation to additional
investment decline in the near/high-replenishment arm, with a smaller far-side
relief. A corrected fixed-resident rare-mutant diagnostic shows the same asymmetry
in local selection: increasing assurance weakens investment selection far more
under near than far visitor histories because maternal outcross and paternal
pollen-export returns remain larger where pollination is still effective. This
explains the interaction locally without treating it as a dynamic mediation
fraction.

**Confirmatory status, 2026-10-06:** a prospectively frozen 4,096-trajectory
replication using 64 new visitor histories and eight new demographic repeats
passed both primary success rules. In the delayed-selfing/costly,
positive-mutation cell, assurance was first in 51/64 histories at the 0.05
threshold (95% history-bootstrap 0.6875–0.8906). With assurance fixed at 0.5,
far investment change was −0.3060 [−0.3181, −0.2941] and far-minus-near
investment was −0.4354 [−0.4533, −0.4172]. The sequence result is not universal:
the corresponding prior-selfing positive-mutation cell gave 30/64
assurance-first histories at threshold 0.05. The confirmed **temporal-order**
claim is therefore restricted to the delayed-selfing, assurance-cost setting.

**Generality status, 2026-10-06:** a separately frozen 8,448-trajectory campaign
used 64 additional visitor histories and eight additional demographic repeats.
All four reproductive settings passed the preregistered rule: fixed-assurance
far-minus-near investment was negative with intervals below zero, while the
common-four-cell evolving-minus-fixed interaction was positive with intervals
above zero. The interactions were +0.1605 delayed control, +0.2200 prior
selfing, +0.1915 pollen discount and +0.1007 assurance cost. Terminal occupancy
was 1.0 in every arm/mode and all 64 histories were eligible in every setting.

This document supersedes the September bridge-centred narrative for the active manuscript. Older designs, results and submission snapshots remain provenance; their numerical claims have not been overwritten. The active submission manuscript is `CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md`; `CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md` is retained as the long-form process/provenance manuscript. The historical Oikos renderer reads a fixed snapshot under `legacy/submission-history/model3_bridge_20261004/`.

## Question and manipulation

How does limited visitor replenishment change the reproductive returns to selfing capacity and floral attraction, and the order and extent of their inherited responses?

The manipulated ecological quantity is successful establishment of new visitor functional types per reproductive update. The 13-rate experiment varies this quantity at fixed plant capacity 48. The rate is not visitation frequency or calibrated geographic distance; plant capacity is not island area. Island isolation motivates a restriction on replenishment without claiming to reproduce island geometry, all colonization processes or a stepping-stone archipelago.

## One model, parallel calculations

```text
visitor establishment and disappearance + plant/genetic state
                            |
       pollen transfer, costs and mating opportunities
                            |
     viable maternal, paternal and selfed contributions
             /                              \
 local selection/threshold assay     reproduction and inheritance
                                      /                    \
                          finite-individual ABM    genotype-density model
                          sampled offspring        conditional propagation
                                                          |
                                              exact birth-mutation kernel
                                               vs heat approximation
```

The threshold calculation diagnoses selection; it does not prescribe the ABM update. ABM is not downstream of a density trajectory. Density is not asserted to be the stochastic mean of the finite ABM. A continuous-genotype formulation retains nonlocal sexual inheritance; diffusion approximates the mutation component only.

## Five questions and evidence

| Question | Evidence | Supported interpretation |
|---|---|---|
| When does selection change? | Joint cost thresholds, 900 independent numerical checks, 13-rate local assay | Capacity can already be favoured at high replenishment; investment selection can reverse. No universal geographic cutoff. |
| How do traits affect each other? | 144,060-state reciprocal diagnostic and 112,500-case parameter grid; fixed-capacity and trait interventions | Reciprocal effects are conditional; 25 positive capacity-to-investment cross-effect exceptions remain. Local coupling is not proven dynamic mediation. |
| Which change is realized first? | Maintained conditions, 13,312 finite trajectories; both founder-relative and paired high-supply readouts | Capacity-first total evolution can coexist with investment-first additional divergence. Threshold timing is not infinitesimal onset or necessity. |
| What does finite genetic realization change? | Separate zero-mutation ABM/density bridge and one-locus mutation diagnostic | Population sampling and state representation change realized outcomes; mutational supply can retain variation. Full positive-mutation high-resolution comparison remains unresolved. |
| What happens to reproduction? | 12,288 supplementation assays and 6,912 trait interventions | Lower fractional pollen deficits need not mean more viable offspring when costs and inbreeding depression remain. |

All experiments retain their own founders, times, mutation settings and independent replication units. The 13-rate extension is exploratory, with its readout declared before reading intermediate-rate outcomes but after endpoint results were known. Its 64 histories and eight nested demographic repeats do not become 512 independent visitor environments.

## Primary versus complementary evidence

Primary: maintained replenishment conditions, local selection, capacity intervention and pollen/offspring consequences. The older 24,576-case bridge remains a separately labelled comparison of finite versus deterministic realization; its 128 histories are not pooled with the newer 64-history cohort.

Complementary: environmental equalization/history experiments, phenotype-only closure counterexample, and source-audited natural systems. These do not determine the primary question or calibrate the model. Q1 is independent motivation. Investment is not a calibrated flower-colour or accessibility phenotype, and the four Q1 regions are not assigned to synthetic regimes. The natural archive does not establish longitudinal inherited responses corresponding to this full model.

## Numerical closure

The stopped high-resolution 1,000-update comparison stays stopped. Verified local updates do not constitute long-horizon validation. The 9-to-13 grid comparison failed 31/32 endpoint gates; the restricted heat-versus-jump example also retains its failed tolerance. `MODEL3_LONG_COMPARISON_DECISION_20261005.md` records why no admitted cheap replacement was available. This is an explicitly unresolved numerical branch, not a successful PDE confirmation or a biological falsification.

## Current authoring and delivery

- `scripts/render_chapter2_process_manuscript.py`: current manuscript, without repository routing metadata.
- Main figures: `figure_model3_return_components.py`, `figure_model3_assurance_compression.py`, `figure_model3_trait_pollen.py`, `figure_model3_genetic_realization.py`.
- Full gradient: `figure_model3_replenishment_evolution.py`; all conditions and censoring retained.
- Numerical figure verification: `verify_model3_rate_figures.py`, plus the per-figure receipts and poster-native-chart verifier.
- Review delivery: `build_chapter2_process_review.py` includes the four main figures, their numerical inputs and working sources at their original relative paths. `verify_chapter2_process_review.py` extracts the package separately and redraws all four figures; numerical exports must agree exactly. This is figure-level reproduction, not a complete raw-data deposit.
- Completion ledger: `MODEL3_ECOLOGICAL_CLOSEOUT_STATUS_20261005.md`.

The historical Oikos bundle and its frozen claim tests reproduce the earlier bridge submission. They are not the delivery route for this updated process manuscript. No journal submission, public data deposition, universal sequence, stable attractor or natural-island causal validation is claimed.
