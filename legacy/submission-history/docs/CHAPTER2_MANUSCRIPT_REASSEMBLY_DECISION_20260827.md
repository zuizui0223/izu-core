# Chapter 2 manuscript reassembly decision

Updated: 2026-08-27

## Decision

The Chapter 2 scientific model reassessment is complete. The product is a **Research Article candidate centered on conditional response geometry**, but there is **no active submission manuscript yet**.

Do not restore or hand-repair the historical Journal of Ecology draft as the authoritative manuscript. Regenerate the active manuscript from the current canonical evidence state and current model results.

## Scientific result that now justifies reassembly

The nontrivial result is no longer `initial heterogeneity is the minimal generator`.

The supported model result is that post-establishment response to pollinator reorganization is conditional on plant starting position and realized interaction context:

- 41 of 96 matched pollinator-community realizations produced both positive and negative responses across the starting-trait grid;
- the mean response geometry was mixed-sign, with sign transitions around 0.30–0.35 and 0.65–0.70 on the synthetic starting-trait axis;
- 16 of 48 fixed joint 10-parameter Latin-hypercube points retained mixed mean geometry, versus 22 all-positive and 10 all-negative points;
- local availability / interaction filtering changed response sign for 737 lineage contrasts across the declared envelope, with median first sign-change strength 0.40;
- the autonomous-assurance route produced no sign rescue among 580 eligible baseline declines at any multiplier from 0.5× through 4×, while preserving broad magnitude attenuation and leaving upstream service unchanged.

These quantities describe the declared synthetic design. They are not estimates of natural prevalence, empirical trait thresholds, or fitted ecological effect sizes.

## New manuscript spine

The manuscript should be rebuilt around this sequence:

1. **Problem:** plant island syndromes mix assembly filtering, in-situ evolution, and post-establishment interaction response, encouraging monotonic interpretations of island effects.
2. **Model scope:** the simulation addresses the third layer, post-establishment interaction response, using an explicit matching and partner-reorganization model. It does not provide evidence for in-situ evolutionary dynamics.
3. **Primary result:** the sign of island-minus-mainland functional-service response is a non-monotonic function of starting functional position.
4. **Robustness result:** mixed response geometry persists in a substantial part of the declared joint parameter space but is not universal; all-positive and all-negative regimes also occur.
5. **Context result:** local availability / interaction filtering can alter branch identity in either direction.
6. **Downstream modifier result:** autonomous assurance attenuates decline magnitude but does not create sign rescue in the tested 0–4× sensitivity envelope.
7. **Ecological interpretation:** heterogeneous island outcomes can arise from the same broad pollinator reorganization when starting functional position and realized local context differ.
8. **Comparative boundary:** external island systems illustrate response diversity and retained failures; they are not validation coverage of the model vocabulary.

## Claims that must stay out

Do not restore any of the following as headline claims:

- `replicated_minimal_generator` as a general ecological discovery;
- `11/11 covered` or equivalent external-state coverage as validation of generality;
- assurance attenuation as an emergent or empirically established buffering mechanism;
- synthetic response frequencies as natural prevalence;
- support strength 0.40 as an empirical filtering threshold;
- the synthetic trait-axis sign switches as calibrated biological trait thresholds;
- historical Bombus causation or a general Izu-flora rule beyond the canonical evidence state.

## Required manuscript work before submission

The regenerated manuscript must:

- state all model equations and parameter values needed to reproduce the reported geometry;
- distinguish empirically motivated directional assumptions from generic sensitivity choices;
- show the response-geometry figure and joint-regime map as primary results;
- report local-context and assurance threshold analyses with their synthetic interpretation boundary;
- clean workflow/debug/provenance language out of Methods;
- resolve citation hygiene, including Lord (2015) and Méndez (2025);
- align every empirical statement with `docs/CURRENT_EVIDENCE_STATE.md`;
- align development claims with `data/design/active_development_mainline.json`;
- keep the submission builder fail-closed until this new active manuscript surface is assembled and audited.

## Product boundary

Model-side scientific recovery succeeded: the programme does not need to fall back automatically to a conceptual Review/Mini-review.

Submission readiness did **not** automatically return. The next unit of work is manuscript reassembly from current state, followed by a claim/evidence audit. If that clean reassembly cannot sustain a focused Research Article without importing blocked empirical claims, then the three-layer island-syndrome decomposition remains the fallback conceptual product.
