# Research trials retained as methodological lessons

This branch previously explored broad GBIF composition analysis, trait filtering, and same-species public-image morphometrics. Those experiments were removed from the active analysis because their observation processes did not support the biological claims being considered.

## Public occurrence records

Useful lessons:

- `0` means no public record was recovered, not biological absence;
- raw Jaccard differences were dominated by richness, nestedness and sampling;
- apparent annual/perennial differences were sensitive to record intensity.

Do not infer complete flora, abundance, occupancy, alpha diversity, true beta diversity, colonization, extinction or lifecycle filtering from these records.

## Public images

Useful lessons:

- multiple photographs from one observation are pseudoreplicates;
- view, organ, stage, cultivation and background must be controlled;
- generic colour and texture ROI features failed a flat Ajania negative control;
- specialist taxa lacked independent Oshima and non-Oshima observations.

Do not use automatic public-image embeddings as evidence of floral evolution. Standardized prospective photography remains a future route.

## Edge and life-history screens

Useful lessons:

- `1 - Jaccard` is total dissimilarity, not species replacement;
- replacement and nestedness must be separated;
- descriptive edge rankings are not causal threshold tests;
- uncertainty and observation effort belong in any future community model.

## Five-candidate ordinal-order / tempered-SMC trial

A later source-level trial expanded the restricted candidate family with a fixed ordinal `isolation_order` proxy and used tempered SMC to stabilize numerical integration. The ordinal proxy could lead within that declared family, but its advantage depended materially on retaining the flower-length channel. `ardens_bridge_loss` remained a plausible restricted alternative in the non-flower channels rather than being uniquely rejected.

Useful lessons:

- a fixed island-order scaffold is not geographic distance, dated colonization history, an isolation mechanism, or pollinator service;
- a candidate winning inside a restricted family does not identify the historical cause represented by its label;
- tempered SMC can improve numerical integration and ranking stability without adding historical observations or causal identification;
- candidate preference that changes under channel ablation is evidence of channel dependence, not a universal island mechanism;
- the bridge-loss and ordinal-order candidates should therefore be treated as competing restricted explanations unless direct mechanism measurements discriminate them.

The five-candidate register and its dedicated source-level workflow are no longer active decision surfaces. Current development instead uses the source-locked focal claim boundaries, the direct effective-service × reproductive-dependency field gate, and explicitly admitted external bridge systems. The retired register/workflow remain recoverable from Git and PR history. Lower-level source-analysis components are not retired by this note and require separate reference and claim audits before removal.

## Rich attraction-trait model incubator

A richer proposed model combined nectar-guide expression, flower size, delayed-selfing geometry, selfing ability, neutral diversity and spatial position. It was intentionally never promoted to an active inference engine because the richer state space was not linked to a measurement design capable of discriminating the proposed pathways.

Useful lessons:

- adding biologically plausible latent structure does not make a reconstruction into field evidence;
- promotion of a mechanistic model requires one explicit biological hypothesis, one declared life cycle with interpretable parameters, one observable measurement set linked to those parameters, and one falsification or discrimination target;
- pollinator-mediated attraction and selfing / delayed-selfing compensation must be distinguishable by planned observations before the model can adjudicate between them;
- the smaller constrained life-history simulation is safer when it retains only transparent attraction--assurance hypotheses and does not convert reconstruction into a field claim.

The legacy incubator is therefore retired from the active tree. Its intended attraction-versus-assurance question remains relevant only when direct measurements make that contrast testable.

## Assets retained

Only the compact threshold-identifiability simulator, fixed three-regime design, central-hypothesis contract and tests remain active. Detailed failed-run products remain recoverable from PR history and workflow artifacts rather than the active tree.
