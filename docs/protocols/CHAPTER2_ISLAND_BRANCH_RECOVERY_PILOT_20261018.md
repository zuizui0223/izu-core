# One-paper island divergence: Q3 pollinator-return feasibility pilot (2026-10-18)

**Status:** EXPLORATORY protocol drafted before pilot outcomes; NOT a registered confirmatory experiment, no authorization to replace frozen Chapter 2 decisions. Branches from PR #590's one-NEE-Article working route. The Ecology Letters historical source, archived 2,304 genomes, Q2 384-path `both_inconclusive`, all figures and original receipts remain unchanged.

## One question, three conditional tests

Why do island plant lineages exposed to limited effective pollination fail to converge on one reproductive syndrome, and what keeps the resulting reproductive changes from reversing?

- **Q1 / common response:** Floral investment I can fall while evolutionary assurance A is fixed at expressed 0.5; this is **not** prohibition of self-fertilization and does not directly establish change in dioecious plants.
- **Q2 / divergence (UNTESTED):** Compare (a) evolved selfing and (b) sex-separated reproduction, with a third *colonization-filtering-only* alternative. Male sterility alone produces females + hermaphrodites, not complete dioecy. The classical second female-sterility/male-specialization step, linkage, sex-specific gamete constraints, pollen limitation and inbreeding-depression dynamics need separate pre-implementation validation. Scarce pollinators need not favor de novo dioecy. Do not equate dioecy in island floras to local evolution.
- **Q3 / reversibility (THIS PILOT):** Ask whether high-I ancestral expression is attainable following an imposed functional-pollinator return, whether original high-I alleles were lost, and whether enabling A evolution alters unconditional *probability of returning to high I*. No sex-locus or deleterious-mutation model in this pilot.

## An existing result, not a restoration result

The read-only source review in PR #590 and independent PRs #591/#592 found 1,455/2,304 original occupied finite Model3 paths with upper-I allele support below that path's founder I mean; 758 before I fixation, 697 at fixation. The older 703/2,304 counts LOWER-I access closure. Neither numerator is a pollinator-restoration trial, an unconditional A-policy effect, nor an estimate of loss before permanent pollinator extirpation.

## Fixed exploratory micro-pilot only

- **Biological operator:** unchanged `scripts.model3_island.reproduction.reproduce`, `population.advance`, `history.reflect_unit` and the original `PlantState`/`VisitorState` data types. Finite-plant trajectories only; density is not used as finite expectation.
- **Config anchor:** read `data/design/model3_island_v2.json` `base_config`. Preserve ovule, pollen, saturation, selfing timing, selfed viability, capacity 48 and two-episode ledgers. For this pilot explicitly set delayed selfing, assurance cost 0.5, I/M/A mutation rate 0, plant seed supply 0, annual survival 0, count-scaled visitor activity 0.4. These are artificial values; no real island/annual calendar calibration.
- **Population:** two independently seeded synthetic founder blocks; each has 48 diploid plants and standing three-valued I alleles 0.375/0.5/0.625. Target `I_star` is that founder's true initial expressed mean.
- **Exogenous visitors:** two independently drawn visitor histories crossed with the founders, matched across policies. Functional service starts with six visitor types (periods 0–4), falls to a single type (periods 5–34), and is set to zero from **T_E=35** onward with no replenishment. This is an **imposed** permanent removal on the unrescued historical arm, unlike a sampled empty year.
- **Historical policy:** assign `A_evolving` vs `A_fixed_0.5` at time zero; two histories per founder, 2×2×2=8 full historical paths to census 45; no post-hoc survivor selection. Matched initial genotypes, environmental history and stream *namespaces*; finite divergence of RNG consumption is allowed and is not individual-event coupling.
- **Checkpoints:** t=10, 30, 45 (two before imposed T_E and one after). Record complete living state including ID, age, origin, mutation marks and diploid genome.
- **Counterfactual futures:** from every saved checkpoint run two **externally assigned** futures: `functional_pollinators_restored` (the same six functional visitor types) and `continued_pollinator_loss` (no functional visitors), for H=25 reproductive updates and two independently seeded conditional futures per state and environment. Restore visitors, **not high-I alleles**. No seed immigration or mutation.
- **Time/domain:** 8×3×2×2 = **96 exploratory future trajectories**, 2,400 future updates + 360 historical updates; no other conditions, search or adaptive repeats. Independent inferential blocks remain 2×2 founder×visitor, not 96 independent islands.
- **Diagnostics:** exact high-I support theorem (occupied `max I-allele < I_star`), founder-relative current I, finite-H high-I return requiring 5 consecutive post-return living censuses with mean I >= `I_star`, at-H occupancy, a fixed focal-mutant positive-selection diagnostic after return, no-mutational rescue guarantee, and the full unconditional denominator including previously extinct histories. A declined-population-only result is optional description, NOT causal policy contrast.
- **Pairing:** a future stream is separately keyed by founder, visitor, checkpoint, future replicate, and environment, and reused for both historical A policy labels. Same stream ID does not guarantee synchronous individual draws if policies yielded different resident states.
- **Output:** explicit new `--out` path only; deterministic JSON with source SHA256, design and independent-block identifiers; refuse overwrite.
- **Scientific success criteria:** this pilot checks whether the experimental implementation and data products can measure the estimand. It does **NOT** assign ratchet/lifeboat, infer `T_R`, compute inferential confidence intervals, or support the Baker–dioecy mechanism. A confirmed A-policy effect requires separate fresh-founder × fresh-visitor power/SESOI design and pre-execution review under #585.

## Two clocks and four mechanistic states

`T_E` is a policy-imposed permanent absence date in the untreated history. `T_R` would be the earliest pre-registered, uncertainty-supported, sustained loss of restoration success **despite positive ecological selection for higher I**. This pilot cannot identify `T_R`. A structural high-I support closure supplies one sufficient mechanism for failure only when I mutation and migration are forbidden; retained upper support does not imply realized return.

Never treat loss of floral investment as proof of an evolutionary trajectory to dioecy, nor equate Baker's law (self-compatibility as a colonization advantage) with a prediction that every colonist actually self-fertilizes. Independence of island contrasts and colonization filtering versus within-lineage changes must be tested with external data.

## Exit gate

Advance Q2 sex genetics only after the exploratory operator/readout has passed adversarial validation; then model (1) sex-specific male and female functions and both fertility-loss paths, (2) dynamic genetic load and purging with appropriate within-family inheritance, (3) independently identifiable colonization filtering. A full Q2/Q3 joint-power study must pass #585 **before** its confirmatory run; the present pilot is never repurposed as that confirmation.
