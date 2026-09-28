# Chapter 2 model unification decision — final 2026-09-27

## Decision

> **Model 2 is no longer required as an active scientific model or control gate for Chapter 2.**

One nested Model 3 now answers the core mechanism and the two original controls that had remained unique to Model 2.

## Evidence chain

### A. Fixed-state branch capacity

Controlled visitor compositions can reverse reproductive-selection direction across starting floral states before inheritance or demographic updating.

### B. Deterministic genotype-density realization

The same reproduction and Mendelian operator can retain branching under controlled compositions, but under the prospective natural isolation-driven assembly contrast it is one-directional.

### C. Finite-population realization

Finite ABM trajectories can realize mixed directions under the same isolation-driven histories. The prospective bridge identifies why.

## Prospective bridge closure

Frozen result: `data/results/model3_ch2_bridge_prospective_frozen_20260927.json`

Full interpretation: `docs/MODEL3_CH2_BRIDGE_PROSPECTIVE_RESULTS_20260927.md`

Workflow run: `36311030639`

Verified cases: `24,576`

### Original control 1 — dynamic realized-richness matching

Annual response-blind count matching reverses the mean far-minus-near inherited-investment effect:

- finite ABM: `-0.1446` → `+0.0333`;
- deterministic density: `-0.4510` → `+0.0338`.

Finite-ABM mixed histories increase from `12/128` to `68/128` at epsilon 0; at epsilon 0.05, `18/128` remain mixed after matching.

Thus visitor amount strongly positions the coarse mean regime, while count matching does not remove realized branch heterogeneity.

### Original control 2 — finite visitor community versus finite plant population

Pooling eight independent visitor histories removes mixed history-level branches in both finite ABM and deterministic density at all deadbands.

Increasing plant capacity from 48 to 192 while retaining the natural visitor history reduces finite-ABM mixed histories from `12/128` to `1/128` at epsilon 0 and to `0/128` at epsilon 0.05.

Therefore finite visitor-environment sampling and finite plant demographic sampling are distinct contributors.

## Important correction to earlier unification wording

The correct statement is not:

> branching persists deterministically under every island regime.

It is:

> **Model 3 has deterministic state-dependent branch capacity, but isolation-driven assembly can produce a common deterministic direction; visitor-environment and plant-demographic sampling strongly modify heterogeneous realized responses, while stable latent branch prevalence remains unresolved.**

## S/C/I status

S/C/I remains a descriptive magnitude decomposition only. The pooled-visitor finite ABM has `I = 0.542` but zero mixed-sign histories, proving that interaction share is not equivalent to directional branching.

## Final Model 2 role

Legacy Model 2 is retained only for:

- historical service-endpoint provenance;
- historical exact-richness and synthetic-`k` comparison;
- response-rule sensitivity;
- historical S/C/I decomposition;
- community-mean asymptotic analysis.

It must not be narrated as a second biological mechanism or as an unresolved gate required for Chapter 2 completion.

## Scientific synthesis

```text
isolation-driven visitor rarity
      -> coarse deterministic pressure

visitor amount/richness
      -> shifts mean response regime

finite visitor composition/history
+ finite plant demography
      -> modify observed directional heterogeneity; latent branch prevalence remains unresolved

assurance / connectivity / chronology
      -> filter persistence and inherited outcome
```

## Natural claim ceiling

The result is synthetic and model-conditional. Annual matching changes identity persistence, visitor pooling changes nonlinear environmental averaging, and plant-capacity manipulation is not a visitor-community manipulation. No natural rates, branch prevalence, named historical cause or field threshold is estimated.
