# Simulation closure and projection to real islands

## Final-form decision

The current simulation is sufficient as a **bounded mechanistic proof-of-concept**, with reproducible primary results and explicit response-rule sensitivity. It is not a calibrated forecast of floral evolution, island colonization, or reproductive output in a named island. No additional mechanisms are required merely to close the present question. A genetic/demographic model would be a separate project with a new estimand and prospective design.

The retained claim is: **within the declared model family, determinant rankings can change with community aggregation and with how plant state responds to the community.** Neither C→I→S nor C/I reversal is universal across response operators. In particular, the no-threshold, centroid, constant-speed condition remains C-dominated by component medians across all audited k. This limits generalization without invalidating the frozen primary result.

The source/configuration contract, complete cell arrays, reconstructed statistics and all conditional contrasts are in `data/results/update_factorial_20260925/`. The artifact validator checks exact inventory, unique design cells, source/config identity, historical hashes, all terminal-cell statistics and paired contrasts. It never refreshes a mismatching manifest to make a run pass. LF/CRLF text representations alone are equivalent.

## What the model actually contrasts

Each cell compares final service after separate mainland-like and island-like visitor histories, from the **same initial plant trait**. Both trajectories permit plant adjustment. Island minus mainland therefore is not before versus after colonization, an estimate of evolutionary change, or a causal island effect in observational data. Service is a saturating transformation of mean compatibility, not visitor abundance, visitation volume, fitness or seed set.

S measures variation among initial positions in expected service contrasts. It is not retention of ancestral traits. C measures an additive history-pair effect. I is the non-additive remainder in the crossed deterministic design. Natural residuals cannot be equated with I because measurement error and unobserved environmental variables also contribute. Pollinators are functional-type agents, with no explicit abundance or lineage identity. Steps are uncalibrated updates. k concatenates independent visitor histories at each step and weights them through their current numbers of types; it is not an equal-weight temporal average.

## Mapping to field measurements

| Model concept | Measurable ecological counterpart | What cannot be inferred directly |
|---|---|---|
| Plant starting state | Floral tube depth/opening and relevant reproductive traits measured before the focal response; predeclared scaling | Current mainland mean is not automatically the ancestral state; the scalar model does not implement a colour/shape syndrome vector |
| Visitor trajectory | Repeated, effort-standardized visitor identities, frequencies and functional traits in the same time blocks; record zero visits | Island ID or a one-time species list is not a community history; non-detection is not extinction |
| Functional match | Flower access × mouthpart/body fit, checked with contact and pollen-delivery observations | Gaussian matching and external-type penalty 0.82 are hypotheses, not empirical calibrations |
| Effective service | Visits per flower-hour × background-corrected single-visit conspecific pollen deposition, by visitor group | This absolute field service is not numerically identical to model mean-match service; calibrate a link or use qualitative predictions |
| Reproductive consequence | Open, autonomous-bagged and supplemental-outcross treatments, mature fruit/seed endpoints on linked plants | Pollen deposition, pollen limitation and seed set are different quantities; do not collapse them |
| S/C/I analogue | Replicated plant-state ranges crossed with multiple community/time blocks; predict response surfaces over common support | Do not fit four region labels and call their variance shares synthetic S/C/I; no regional fractions have been estimated |
| k-related context | Partner diversity and temporal synchrony measured separately, with standardized effort and environmental controls | Hill D1 is not k; no empirical k=4 threshold, island-area conversion or year conversion |
| Response rule | Repeated measurements on the same individuals/lineages; common-environment or manipulation designs | Snapshots cannot identify plasticity versus evolution; best-match motion is not a fitness-gradient model |

## Testable predictions, to freeze before new outcomes

1. A changed visitor assemblage need not affect all floral states equally. Test trait × visitor-context response surfaces rather than imposing one mean island effect.
2. Distinguish concentration of **effective pollen delivery** among visitor groups from raw visitation dominance. A few effective groups motivates a best-partner-like hypothesis; distributed effective contributions motivates a community-integrated hypothesis. Neither measurement alone identifies the plant update operator.
3. Under comparable partner diversity, jointly fluctuating contributors may offer less temporal buffering than asynchronous contributors. Measure synchrony rather than treating high diversity as automatic averaging. This is a field prediction, not a result proved by the independent-copy model.
4. To explain response-rule effects, compare terminal-trait change separately from functional response. The fixed-state control already shows that retaining a trait does not ensure high S.

Field inference should retain island/site/time nesting, detection and sampling effort, phylogenetic or lineage structure where needed, and weather/habitat confounders. Reserve independent populations or periods for evaluation; select models and thresholds before inspecting those outcomes. No new numeric success threshold is introduced by this document.

## Roles of the 42 systems and Izu

**42 systems from six studies** locate observed communities in breadth–synchrony space. They are neither 42 independent islands nor a validation of the synthetic C/I crossover. Existing source and sampling-depth sensitivities remain applicable. They establish observed context diversity, not natural k calibration or historical mechanism.

**Izu is the linked-measurement opportunity**, selected after the geography-first global audit, not because it is close to Atami or guaranteed to agree with the model. Existing evidence includes eight sites with five seasonal network snapshots and species-level proboscis values for 202/209 named visitor taxa; exact local trait coverage remains incomplete. Independent five-island Campanula phenotypes are a downstream handoff, not retrospective Chapter 2 validation.

The most useful next chain is:

`tagged plant and pre-response traits → effort-matched visitor history → single-visit pollen delivery + no-visit controls → reproductive dependency treatments → mature fruit/seed outcome`.

This is already aligned with `data/design/effective_pollinator_dependency_field_readiness.json`; field evidence remains missing. Consult `data/design/chapter2_izu_focal_system_rationale_20260906.json` for selection rationale and limitations. Flower colour/form associations in Q1 can motivate trait–visitor hypotheses but cannot identify actual visitor guilds or selection without those measurements.

## Stop rule and publication wording

Close the current simulation once identity checks, reference replay, complete artifact reconstruction, relevant tests and independent review pass, and publish all operator-dependent and negative results. Do not add population dynamics, genetics or extra fitted parameters to restore a desired ranking.

Suggested statement: **Community change does not map uniquely onto plant response: in this model family, both community aggregation and the plant response rule affect which component dominates. Natural rates, prevalence and historical causes remain to be tested.**

Primary ecological context: Traveset et al. (2016), https://doi.org/10.1111/geb.12362. Network differences motivate field questions but do not validate these synthetic response rules.
