# Model 3 Chapter 2 bridge — prospective results and final interpretation

Date: 2026-09-27
Status: frozen prospective result

## Provenance

- workflow run: `36311030639`;
- workflow head: `b59b39cbf13a6313d9005f54e7a23c0b5703573c`;
- verified cases: `24,576`;
- independent visitor histories: `128`;
- deterministic execution shards: `16`;
- summary artifact: `10929715247`;
- artifact SHA256: `63215332a97f3140ea8cc4b7d380384023f5b25284713b3486f21ac47c3fb253`;
- frozen compact receipt: `data/results/model3_ch2_bridge_prospective_frozen_20260927.json`.

The production analysis followed the pre-outcome interpretation rules in `docs/MODEL3_CH2_BRIDGE_PROSPECTIVE_INTERPRETATION_20260927.md`. No result direction, mixed fraction, S/C/I ranking or agreement with legacy Model 2 was an execution success criterion.

## Primary result

The old Chapter 2 controls can now be answered inside Model 3, but the answer is more structured than a simple replication of legacy Model 2.

> **Richness/visitor amount strongly sets the coarse isolation response, whereas visitor-community realization and finite plant demography jointly modify the distribution of realized directional outcomes; exact latent branch prevalence is not identified.**

## 1. Natural isolation-driven assembly has a directional deterministic backbone

Under the unmodified near-versus-far visitor-assembly contrast:

| model | mean far-minus-near investment change | 95% history-bootstrap interval | mixed histories at eps=0 / 0.01 / 0.05 |
|---|---:|---:|---:|
| finite ABM | `-0.1446` | `[-0.1588, -0.1306]` | `12 / 8 / 1` of 128 |
| deterministic density | `-0.4510` | `[-0.4716, -0.4301]` | `0 / 0 / 0` of 128 |

The deterministic inherited response is therefore one-directional under this isolation-driven assembly contrast. Finite ABM trajectories can nevertheless realize mixed signs.

This corrects an over-broad earlier interpretation. Model 3 can produce deterministic state-dependent branching under controlled visitor compositions, but that does **not** mean the natural isolation-assembly contrast is deterministically branched.

The finite-history labels are themselves demographic realizations rather than stable latent branch identities. At epsilon 0, at least two of the eight repeat-specific labels disagree within **97/128** natural histories. This is why the finite result is interpreted as realized stochastic heterogeneity, not as 12 histories possessing a fixed deterministic branch state.

## 2. Dynamic richness matching changes the coarse regime and exposes strong finite realized-sign heterogeneity

Response-blind annual matching thinned near and far visitor histories to identical annual counts. Mean count became `0.6603` in both arms, with matched empty years retained.

| model | natural mean | richness-matched mean | mixed histories at eps=0 / 0.01 / 0.05 |
|---|---:|---:|---:|
| finite ABM | `-0.1446` | `+0.0333` | `68 / 59 / 18` after matching |
| deterministic density | `-0.4510` | `+0.0338` | `16 / 1 / 0` after matching |

Thus annual richness matching does **not** merely leave the same mean response with residual noise. It reverses the mean isolation effect from negative to positive in both model realizations.

At the same time, the finite ABM becomes much more heterogeneous: `53.1%` of histories are mixed at epsilon 0 and `14.1%` remain mixed even at epsilon 0.05. Deterministic density shows only weak near-zero mixed branching (`16/128` at epsilon 0, `1/128` at 0.01 and `0/128` at 0.05).

This heterogeneity is especially stochastic at the finite-population level: **128/128** richness-matched histories show at least one disagreement among their eight repeat-specific labels at all three deadbands. The mean-over-eight classification is therefore a descriptive distribution of realized outcomes, not evidence for a stable hidden branch assigned to each visitor history.

The supported interpretation is therefore:

> **Visitor amount/richness strongly controls the coarse mean regime, while identity/composition plus finite-population realization govern much of the remaining realized-sign heterogeneity.**

Annual thinning also changes visitor identity persistence, so this is not a pure field species-richness causal effect.

## 3. Finite visitor-community realization is a separate axis of realized heterogeneity

The pooled-visitor intervention combines eight independent visitor histories with count-scaled activity normalization.

| model | mean effect | mixed histories at eps=0 / 0.01 / 0.05 |
|---|---:|---:|
| finite ABM | `-0.2259` | `0 / 0 / 0` |
| deterministic density | `-0.5560` | `0 / 0 / 0` |

Pooling visitor histories eliminates mixed history-level labels in both model forms.

This shows that **finite visitor-environment sampling matters independently of finite plant population size**. The pooling operation changes environmental averaging and functional composition under a nonlinear reproductive operator; it is not an island-count or lifespan manipulation.

## 4. Finite plant demography is a separate source of mixed-label sensitivity

Plant capacity was increased from `48` to `192` while the natural visitor history was kept unchanged.

- finite-ABM mixed histories fell from `12` to `1` at epsilon 0;
- from `8` to `1` at epsilon 0.01;
- and from `1` to `0` at epsilon 0.05;
- the finite-ABM mean moved from `-0.1446` to `-0.2716`, closing about `41.5%` of the gap toward the deterministic mean `-0.4510`.

Therefore finite plant demography is not interchangeable with finite visitor-community sampling. Both interventions alter realized outcomes through different routes, but neither identifies a stable latent branching probability. Repeat-label disagreement also falls with larger plant capacity (from 97/128 to 31/128 histories at epsilon 0), consistent with reduced demographic sampling variability.

## 5. S/C/I magnitude decomposition is not equivalent to directional branching

The visitor-pooled finite ABM has:

- `S = 0.091`;
- `C = 0.367`;
- `I = 0.542`;

yet has `0/128` mixed histories at every deadband.

Thus a large non-additive `I` component can describe response-magnitude structure without implying positive/negative directional branching. S/C/I remains a useful descriptive decomposition but cannot be used as a proxy for the biological claim that different lineages evolve in opposite directions.

## Original Chapter 2 questions — final status

| original question | prospective Model 3 answer |
|---|---|
| Do finite populations show different realized signs across starting states? | **Descriptively yes**, but the mixed-history labels are deadband- and repeat-sensitive; the natural deterministic density contrast is one-directional and stable latent branch prevalence is not identified. |
| Does richness/visitor amount explain the mean? | **Strongly yes in this design.** Annual richness matching reverses the mean far-minus-near effect from negative to positive. |
| Does richness matching eliminate branch heterogeneity? | **No in the finite ABM.** Mixed histories increase strongly after matching. Deterministic mixed branching is weak and disappears at the 0.05 deadband. |
| Does visitor-environment realization alter descriptive mixed labels? | **Yes.** Pooling eight visitor histories removes mixed labels completely, but the compound intervention does not identify a pure latent-branch effect. |
| Does finite plant-population size alter descriptive mixed labels? | **Yes.** Fourfold larger plant capacity nearly removes mixed labels, but the manipulation changes several finite-demographic processes and does not identify latent branch prevalence. |
| Are visitor finiteness and plant finiteness the same mechanism? | **No.** They are separable axes and both contribute. |
| Does S/C/I ranking identify directional branching? | **No.** High interaction share can coexist with zero mixed-sign histories. |
| Does present environment uniquely determine phenotype? | **No.** The existing chronology experiment still retains different inherited endpoints under a common final environment. |

## Model 2 retirement

The two controls that previously justified keeping Model 2 active have now been run prospectively inside Model 3:

1. response-blind dynamic realized-richness matching;
2. finite visitor-environment averaging separated from finite plant-population size.

Both are evaluable and scientifically informative. Therefore:

> **Model 2 is no longer required as an active scientific model or control gate for Chapter 2.**

It remains valuable as historical/SI provenance for:

- the earlier service endpoint;
- exact-richness and synthetic-`k` comparison;
- response-rule sensitivity;
- historical S/C/I decomposition;
- the community-mean asymptotic calculation.

Those results should not be presented as a second biological mechanism.

## Chapter 1 consequence

Chapter 1's unresolved pattern can now be connected more precisely:

```text
Chapter 1
isolation -> stronger pollen limitation
          -> recurrent assurance/accessibility
          -> but detailed phenotype differs among regions

Chapter 2
isolation-driven visitor loss/rarity
          -> coarse directional pressure
richness/visitor amount
          -> strongly changes the mean regime
finite visitor composition/history
+ finite plant demography
          -> determine which alternative trajectories are realized
assurance/history/connectivity
          -> further filter persistence and inherited outcome
```

This yields a stronger dissertation interpretation than 'context dependence':

> **Island isolation can impose a recurrent functional problem and even a common deterministic backbone, while finite ecological and demographic realization generates divergent phenotypic outcomes.**

That structure explains why Chapter 1 can show a recurrent functional syndrome without one recurrent detailed floral phenotype.

## What remains genuinely unresolved

The remaining gap is empirical rather than a missing Model 2 control:

- no natural system in the current archive closes the full A -> B -> C chain;
- the inherited longitudinal **B layer** remains poorly observed;
- the model does not identify the historical cause of any specific Chapter 1 regional colour/architecture pattern;
- synthetic distances, times, investment values and branching frequencies are not calibrated natural quantities.

These gaps should be retained as external falsification targets, not filled by additional retuning of the current simulation.
