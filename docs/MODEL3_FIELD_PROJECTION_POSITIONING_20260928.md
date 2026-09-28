# Model 3: island-ecological positioning and empirical projection

Date: 2026-09-28. Feasibility assessment, not a new simulation or empirical validation. The completed bridge experiment remains frozen.

## Scientific position

Model 3 addresses how isolation-driven visitor assembly is transmitted through pollen transfer, reproductive assurance, inheritance and finite plant populations into floral investment. Pollination supplies the proximate mechanism; island biogeography supplies the assembly, connectivity and history contrasts. Those processes also occur outside islands, which does not prevent a specific island-ecological question.

The strongest bounded finding from the new bridge is that intervention on annually realized visitor richness changes the sign of the mean isolation contrast, while plant capacity changes its magnitude under the same visitor histories. Thinning also changes identity persistence. This is not proof that richness alone explains isolation. The larger research programme additionally contrasts visitor recovery and seed/genetic replenishment after interruption, under explicitly stated numerical and precision limits.

The candidate contribution is **separating the evolution of reduced floral investment from the evolution of selfing ability, and separating recovery of pollination from recovery of the plant population's evolutionary response across island histories**. The current fixed-assurance bridge shows investment change without evolution of assurance capacity; it does not remove selfing or hold realized selfing constant. Specific cost-removal attribution and robust latent response branching remain unestablished.

Not standalone novelty: pollinators affect floral evolution; reproductive assurance can facilitate persistence; small populations differ from infinite populations; priority effects exist; variance ranks depend on context. Gervasi & Schiestl (2017, https://doi.org/10.1038/ncomms14691) experimentally demonstrated visitor-driven floral divergence. Degottex-Fery & Cheptou (2023, https://doi.org/10.1007/s10682-023-10266-0) explicitly compare finite/infinite populations after a pollinator crash. Their accessible abstract already precludes claiming the broad ABM-versus-deterministic comparison as new; full equation-level priority assessment remains separate.

The accompanying primary-source check, `MODEL3_NOVELTY_PRIMARY_CHECK_20260928.md`, also identifies an opposing empirical direction: Brown & Caruso (2023, https://doi.org/10.1002/ece3.10706) found stronger selection on attraction-related traits under reduced pollination. Thus fewer visitors do not universally weaken attraction selection. The proposed ecological question concerns which conditions produce each outcome, not an assumed universal decline-to-simplification chain. Busch et al. (2022, https://doi.org/10.1111/evo.14572) also precedes pollinator-loss/selfing/genetic-diversity arguments. These are candidate distinctions from nearby work, not a priority certification.

## What the existing 42-system projection actually contains

Read directly from six coordinate files used by `scripts/render_chapter2_nee_v03_figures.py` and the six-source checkpoint:

| Source context | Observation systems |
|---|---:|
| Hawaii | 1 |
| Mallorca | 19 |
| Tenerife | 4 |
| Cabrera | 5 |
| Martinique | 10 |
| Great Britain | 3 |
| Total | 42 |

These are six studies and five island groups, not 42 independent islands. All coordinate sets contain Hill D1 and synchrony phi. Their exported coordinate rows do not contain linked plant population size, breeding treatments, genetic variance or inherited floral trajectories. This statement is about the inspected exports, not an exhaustive assertion that none of the original sources contains any such information.

The former natural plane established variation in ecological context. It did not estimate natural k or verify a synthetic rank crossover. The adaptive consumer-resource model, if called Model 2, was a structural generalization test; it did not itself calibrate floral evolution in these natural systems.

## Three distinct levels of projection

| Level | Deliverable | Current feasibility |
|---|---|---|
| Observed ecological context | Place the 42 systems on their existing D1/phi plane; retain study/site hierarchy and intervals | Already available; valid as context, not Model 3 outcome validation |
| Model-informed scenarios | Match observed exposure summaries to multiple compatible visitor-process settings, then retain uncertainty over unmeasured plant parameters | Requires an observation model and declared simulation design; not yet computed |
| Prediction checked against real response | Fit on some linked populations/periods and evaluate floral/reproductive outcomes on held-out populations/periods | Linked data missing from the coordinate exports; not yet established |

A useful Model 3 figure would retain the observed community plane, then show conditional outcome panels for different plant population sizes and assurance capacities. Unknown coordinates must remain ranges/unassigned, not be filled with a convenient default. There is not yet a validated phase boundary that can be painted under the observed island points.

## Measurement-to-model contract needed before numerical projection

1. **Observation units and time:** preserve the original effort-standardized time bins and detection process. Seasonal non-detection is not extinction; within-season synchrony is not interannual synchrony over 200 generations. Island study plots are not independent geological histories.
2. **Community exposure:** use repeated visit counts, identities and, when available, single-visit effectiveness. Compute comparable model and field summaries with the same observation operator. Observed D1 is not the number of model functional types or pooled histories.
3. **Temporal gaps:** derive zero-visit intervals and gap lengths only where observation effort includes genuine zero records. Missing survey periods stay missing. A short seasonal series cannot identify long-term immigration and loss separately.
4. **Plant finite size:** census reproductive individuals and spatial pollen neighbourhoods separately. Census size is neither effective genetic size nor automatically model carrying capacity. Genetic data and recruitment information constrain the mapping.
5. **Assurance and inbreeding:** autonomous-bagged, open and supplemental-outcross reproduction; distinguish capacity for selfing from realized selfing, and measure progeny performance where possible. The bridge fixed depression at 0.5; this is not an estimated island value.
6. **Investment and evolution:** flower size/nectar/scent need a measured relationship to investment and fitness; a scalar investment is not a colour/shape syndrome. Common-environment, pedigree, temporal or comparable lineage evidence is needed to distinguish inherited differences from plasticity.
7. **History and life history:** use independent colonization/connectivity evidence, generations and seed inputs. Oceanic/continental origin informs history priors; it must not mechanically assign a model result. Life span is not k.

Fit exposure/process settings without opening the focal floral response; propagate multiple compatible settings rather than choosing one that reproduces the flower. A future held-out outcome design must be declared before evaluation. If existing Q1 outcomes informed model development, using them afterward is exploratory comparison, not independent validation.

## Izu as a focused test

The existing Izu rationale records eight sites with five seasonal network snapshots and species-level proboscis coverage for 202/209 named visitor taxa; exact local coverage is incomplete. It also documents partial links among matching, pollen and plant response, and a planned same-plant effectiveness/reproductive-dependency protocol. These support selection for measurement continuity, not a claim that Izu is globally optimal, representative, or already confirms Model 3. No new data were collected or those links re-estimated here.

The tractable field question is: **among island populations with comparable present pollination, do differences in reproductive assurance, population variation and independently documented history predict different investment and recovery?** The simulation motivates this prediction but does not yet demonstrate it in Izu.

Evidence files: `MODEL3_CH2_BRIDGE_ECOLOGICAL_RESULTS_20260928.md`; `MODEL3_ISLAND_ECOLOGICAL_RESULTS_20260927.md`; `CHAPTER2_SIMULATION_FINAL_SCOPE_AND_FIELD_PROJECTION_20260925.md`; `data/results/chapter2_natural_regime_six_source_checkpoint_20260915.json`; its six `source_result_files`; `data/design/chapter2_izu_focal_system_rationale_20260906.json`; `data/design/effective_pollinator_dependency_field_readiness.json`.
