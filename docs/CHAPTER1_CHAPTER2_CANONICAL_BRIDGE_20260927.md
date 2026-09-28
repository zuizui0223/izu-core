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

B. isolation-driven deterministic genotype-density response
   -> recurrent coarse directional backbone
   -> visitor amount strongly shifts the mean regime

C. finite visitor environment + finite-population ABM
   -> visitor composition/history + plant demography
      strongly modify observed directional heterogeneity; latent branch prevalence remains unresolved
   -> assurance / chronology / connectivity / life history
      further filter persistence and inherited trajectory

                    ↓

recurrent functional syndrome
+
conditional phenotypic realization
```

## Chapter 1 unresolved problems and Chapter 2 answers

| Chapter 1 leaves unresolved | Chapter 2 result | Interpretation |
|---|---|---|
| Why does a common pollination constraint not give one detailed phenotype? | controlled visitor compositions can reverse selection gradient with starting floral state | functional matching has deterministic branch capacity; whether isolation-driven assembly preserves it is regime dependent |
| Are selfing-adjusted display differences still just a mating-system consequence? | controlled-composition branching persists with assurance held fixed | evolution of assurance capacity is not required to create that floral-selection branch; selfing remains present |
| Why can assurance recur while morphology does not converge? | assurance can determine persistence but not impose one floral direction | recurrent insurance function does not imply recurrent phenotype |
| Why can present pollinator state fail to explain present phenotype? | early/late visitor loss yields different endpoints under the same final environment | historical contingency persists after environmental convergence |
| How can isolation increase pollen limitation while assurance/accessibility are associated with lower realized limitation? | assurance can buffer reproductive consequences or preserve persistence without removing the upstream pollination problem | stress and compensation can coexist at different stages of the same response chain |
| What does geographic isolation actually combine? | seed and pollinator connectivity act through distinct routes | one distance coordinate can compress multiple mechanisms |
| Does visitor amount alone explain the island response? | annual response-blind richness matching reverses the mean far-minus-near effect from negative to positive, but finite-ABM mixed histories rise to 68/128 at epsilon 0 | visitor amount strongly sets the coarse regime, but does not determine every realized direction; finite history labels are stochastic rather than fixed latent branches |
| Is "finite community" one mechanism? | eight-history visitor pooling removes mixed labels, while 4× plant capacity independently reduces finite-ABM mixed labels from 12/128 to 1/128 | visitor-environment realization and finite plant demography are separable axes that alter observed heterogeneity; stable latent branch prevalence is not identified |
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

## Original Chapter 2 controls are now resolved inside Model 3

The prospectively frozen 24,576-case bridge closes the two controls that had previously remained unique to Model 2.

1. **Dynamic realized-richness matching.** Annual response-blind matching reverses the mean far-minus-near inherited-investment effect from negative to positive in both finite ABM (`-0.1446 → +0.0333`) and deterministic density (`-0.4510 → +0.0338`). Yet finite-ABM mixed histories increase to `68/128` at epsilon 0 (`59/128` at 0.01; `18/128` at 0.05). Visitor amount therefore strongly positions the coarse regime without uniquely fixing realized direction.
2. **Finite visitor versus finite plant sampling.** Pooling eight independent visitor histories eliminates mixed history-level labels in both model forms, whereas increasing plant capacity from 48 to 192 independently reduces finite-ABM mixed labels from `12/128` to `1/128` at epsilon 0. The two finite axes are separable and both alter realized outcomes, but these finite-repeat labels are not interpreted as stable latent branch states.

A large S/C/I interaction share is not equivalent to directional branching: the visitor-pooled finite ABM has `I=0.542` but `0/128` mixed histories.

These results remove Model 2's last active control-gate role. Legacy exact-richness, synthetic-`k`, response-rule and S/C/I analyses remain Supporting Information/provenance only.

## Direct decomposition of the Chapter 1 isolation axis

The frozen Model 3 connectivity factorial makes the Chapter 1 macroecological isolation axis mechanistically more explicit.

Across all three seed-distance backgrounds, increasing visitor distance from 0 to 3 shifts inherited floral investment downward by `-0.21145`, `-0.20065` and `-0.17282`, while realized selfing rises by approximately `+0.44` in every case.

By contrast, increasing seed distance from 0 to 3 shifts investment upward / makes its decline weaker at every visitor-distance level (`+0.01685`, `+0.01885`, `+0.05548`) and strongly increases retained founder ancestry.

Thus one geographic-isolation coordinate can combine at least two biologically distinct channels with different phenotypic consequences:

> **pollinator isolation increases realized selfing in the cited fixed-capacity comparison; this is distinct from evolution of reproductive-assurance capacity, while seed connectivity, starting state, community composition and history can prevent one detailed floral endpoint.**

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

> **Chapter 1 shows that island syndromes are more repeatable at the level of ecological function than detailed phenotype. Chapter 2 shows a compatible mechanism: isolation can create a recurrent coarse directional pressure, visitor amount shifts the mean regime, and visitor-environment plus plant-demographic realization strongly modifies the distribution of phenotypic outcomes.**

Short version:

> **Same island problem, recurrent functions, different realized evolutionary solutions.**

## Claim boundary

This bridge is mechanistic, not a retrospective fit of Chapter 1. Do not assign Chapter 1 regions to Model 3 cells, infer natural branch frequencies from simulations, or claim that current regional display patterns identify their historical pollinator causes.


Current Ch1 source audit and investigator motivation: [2026-09-28 audit](CHAPTER2_CH1_MOTIVATION_AUDIT_20260928.md). Ch1 is motivation, not a Model 3 fitting target.
