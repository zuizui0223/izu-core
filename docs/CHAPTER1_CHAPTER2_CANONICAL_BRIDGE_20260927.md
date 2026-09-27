# Chapter 1 → Chapter 2 canonical bridge — 2026-09-27

## Dissertation question

Chapter 1 establishes three simultaneous facts:

1. island isolation is associated with stronger pollen limitation;
2. reproductive assurance and floral accessibility/generalization recur across geographic strata;
3. detailed pollinator-facing floral display does not converge on one regional direction, and selfing does not absorb every residual display association.

That leaves one central mechanistic problem:

> **Why can a recurrent island pollination problem generate recurrent functional insurance without generating one recurrent floral phenotype?**

Chapter 2 answers that problem with one nested Model 3.

## The bridge

```text
CH1: WHAT recurs and what does not?

isolation
  -> stronger pollen limitation
  -> recurrent assurance/accessibility
  -> but colour/architecture realization differs among regions
  -> selfing does not explain every display association

                    ↓ unresolved mechanism

CH2: WHY can that happen?

A. fixed-state reproductive assay
   plant state × visitor functional composition
   -> opposite reproductive-selection directions

B. deterministic genotype-density inheritance
   -> non-uniform inherited trajectories persist
      without demographic sampling

C. finite-population ABM + history
   -> assurance / chronology / connectivity / life history
      determine persistence and realized inherited trajectory

                    ↓

recurrent functional syndrome
+
conditional phenotypic realization
```

## Chapter 1 unresolved problems and Chapter 2 answers

| Chapter 1 leaves unresolved | Chapter 2 result | Interpretation |
|---|---|---|
| Why does a common pollination constraint not give one detailed phenotype? | controlled visitor compositions can reverse selection gradient with starting floral state | functional matching has deterministic branch capacity; whether isolation-driven assembly preserves it is regime dependent |
| Are selfing-adjusted display differences still just a mating-system consequence? | controlled-composition branching persists with assurance held fixed | assurance is not required to create that floral-selection branch |
| Why can assurance recur while morphology does not converge? | assurance can determine persistence but not impose one floral direction | recurrent insurance function does not imply recurrent phenotype |
| Why can present pollinator state fail to explain present phenotype? | early/late visitor loss yields different endpoints under the same final environment | historical contingency persists after environmental convergence |
| How can isolation increase pollen limitation while assurance/accessibility are associated with lower realized limitation? | assurance can buffer reproductive consequences or preserve persistence without removing the upstream pollination problem | stress and compensation can coexist at different stages of the same response chain |
| What does geographic isolation actually combine? | seed and pollinator connectivity act through distinct routes | one distance coordinate can compress multiple mechanisms |
| Does island type itself generate the response? | matched founding/separation labels do not differ without biological state/history differences | oceanic/continental labels are not mechanisms by themselves |
| Why can colour and architecture decouple? | matching/investment selection is conditional, but literal colour is not represented | general mechanism partly answered; colour-specific mechanism remains open |

## What is genuinely solved

Within the declared Model 3, Chapter 2 now separates **branch capacity** from **branch realization**:

- controlled visitor compositions can generate opposite reproductive-selection directions before demographic stochasticity;
- those controlled branches can persist under deterministic Mendelian inheritance;
- the stored isolation-driven near-versus-far contrast is instead deterministic one-directional, while finite ABM histories can be mixed;
- finite demography can therefore be decisive for realized heterogeneity in some assembly regimes;
- historical sequence can leave different inherited endpoints even after current environments become the same.

This is stronger than saying only that responses are context dependent, but narrower than claiming that isolation always generates deterministic branching. It also resolves the apparent H3/H4 tension: a harsher isolation-associated pollination environment and traits that reduce its realized reproductive cost are not contradictory because they occupy different stages of the causal chain.

## What remains unresolved within the original Chapter 2 controls

Two old Chapter 2 questions are still open inside Model 3:

- whether heterogeneous inherited responses remain after **response-blind annual realized-richness matching** of near and isolated visitor histories;
- whether the relevant finite-community effect is specifically **finite visitor-community sampling**, separately from finite plant-population sampling.

A frozen prospective bridge design addresses these with richness-matched, visitor-pooled and larger-capacity controls. Until it is executed, the legacy Model 2 exact-richness and synthetic-`k` analyses remain active benchmark evidence, not merely historical decoration.

## Direct decomposition of the Chapter 1 isolation axis

The frozen Model 3 connectivity factorial makes the Chapter 1 macroecological isolation axis mechanistically more explicit.

Across all three seed-distance backgrounds, increasing visitor distance from 0 to 3 shifts inherited floral investment downward by `-0.21145`, `-0.20065` and `-0.17282`, while realized selfing rises by approximately `+0.44` in every case.

By contrast, increasing seed distance from 0 to 3 shifts investment upward / makes its decline weaker at every visitor-distance level (`+0.01685`, `+0.01885`, `+0.05548`) and strongly increases retained founder ancestry.

Thus one geographic-isolation coordinate can combine at least two biologically distinct channels with different phenotypic consequences:

> **pollinator isolation repeatedly strengthens reproductive assurance in the frozen model, while seed connectivity, starting state, community composition and history can prevent one detailed floral endpoint.**

This is a post-hoc interpretation of the already frozen connectivity factorial, not a calibrated distance effect. Full details are in `docs/CHAPTER1_MODEL3_ISOLATION_CHANNEL_BRIDGE_20260927.md`.

## What remains unsolved

Chapter 2 does not reconstruct which exact Model 3 trajectory generated the northern-midlatitude, northern-high-latitude, tropical or southern-extratropical Chapter 1 pattern.

In particular, it does not identify:

- a specific historical pollinator loss for each region;
- a literal mapping from the abstract access/investment axes to each colour class;
- natural Model 3 parameter values for the four Chapter 1 strata;
- a full longitudinal source-state → visitor transition → selection → inherited response → finite-demographic outcome chain.

The missing evidence is the natural **B layer**: inherited longitudinal change under a measured visitor regime, joined to A and C on the same transition units.

## Connection to the real-island confrontation

The source-locked real-island evidence makes the bridge less hypothetical:

- Izu shows a common upstream matching decline followed by divergent pollen and tube responses;
- Ogasawara and Xisha show stronger functional-access → reproductive propagation;
- Hawaii and Puerto Rico–Mona show buffering;
- Dominica retains a failed signed-position prediction;
- Surtsey, Tiritiri Matangi, New Zealand *Rhabdothamnus* and Mariana bird-loss systems supply founding, reintroduction or loss histories.

Thus natural islands already occupy multiple response modes predicted to be possible by the nested architecture. They do not yet supply one complete natural A → B → C reconstruction.

## Thesis-level conclusion

> **Chapter 1 shows that island syndromes are more repeatable at the level of ecological function than detailed phenotype. Chapter 2 shows why: isolation can create a recurrent coarse directional pressure, visitor amount shifts the mean regime, and finite visitor plus plant-population realization determines how much phenotypic divergence is expressed.**

Short version:

> **Same island problem, recurrent functions, different realized evolutionary solutions.**

## Claim boundary

This bridge is mechanistic, not a retrospective fit of Chapter 1. Do not assign Chapter 1 regions to Model 3 cells, infer natural branch frequencies from simulations, or claim that current regional display patterns identify their historical pollinator causes.
