# Research trials retained as methodological lessons

This branch previously explored broad GBIF composition analysis, trait filtering, and same-species public-image morphometrics. Those experiments were removed from the active analysis because their observation processes did not support the biological claims being considered.

## Public occurrence records

Useful lessons:

- `0` means no public record was recovered, not biological absence;
- raw Jaccard differences were dominated by richness, nestedness and sampling;
- apparent annual/perennial differences were sensitive to record intensity.

Do not infer complete flora, abundance, occupancy, alpha diversity, true beta diversity, colonization, extinction or lifecycle filtering from these records.

## Public images and visible-signal exploration

Useful lessons:

- multiple photographs from one observation are pseudoreplicates;
- view, organ, stage, cultivation and background must be controlled;
- generic colour and texture ROI features failed a flat Ajania negative control;
- specialist taxa lacked independent Oshima and non-Oshima observations;
- blind cards, herbarium/media availability, ROI calibration and public-image positive controls are observation-process diagnostics, not measurements of effective pollination or reproductive dependency;
- a guide/visible-signal channel remains prospective until a final directly measured dataset and analysis are explicitly declared.

Do not use automatic public-image embeddings or guide-screen outputs as evidence of floral evolution. `CURRENT_EVIDENCE_STATE` keeps `visible_signal = blocked_unmeasured / prospective_only`, so the routine PR workflows that repeatedly acquire/render public-photo, herbarium, ROI and guide-screen artifacts are retired. Their modules, scripts, tests, gate tables, prospective templates and historical artifacts remain available for targeted audit or an explicitly declared future visible-signal dataset.

## Edge and life-history screens

Useful lessons:

- `1 - Jaccard` is total dissimilarity, not species replacement;
- replacement and nestedness must be separated;
- descriptive edge rankings are not causal threshold tests;
- uncertainty and observation effort belong in any future community model.

## Rank-weighted pilot synthesis

An early comparative pipeline assigned evidence ranks and functional-group labels to heterogeneous Izu observations, then summarized direction with fixed rank weights. It was useful for exposing source-recovery gaps, but it was never a variance-weighted meta-analysis and its broad observation table predates the current source-locked admission rules.

Useful lessons:

- evidence rank is not an effect-size variance and must not be used as a substitute for formal uncertainty;
- qualitative direction, between-taxon context, web descriptions and source-unlocked geographic claims cannot become independent quantitative replicates by assigning weights;
- public colour descriptions and other visible-signal leads remain outside the adopted evidence until prospectively measured or source-locked under the current gate;
- source recovery and explicit effect-family compatibility must precede formal cross-system pooling;
- a diagnostic that is honest as a screening summary can still become misleading once a stricter evidence registry supersedes its admission rules.

The dedicated `meta-analysis-pipeline` workflow and the rank-weighted observation/rank stack are retired from the active tree, and the consolidated offline runner no longer executes that synthesis. The separate quantitative source-lock validator is retained because it enforces provenance and uncertainty requirements rather than manufacturing a pooled result. Current cross-system decisions come from the source-locked effect/bridge registries and `CURRENT_EVIDENCE_STATE`.

## Five-candidate ordinal-order / tempered-SMC trial

A later source-level trial expanded the restricted candidate family with a fixed ordinal `isolation_order` proxy and used tempered SMC to stabilize numerical integration. The ordinal proxy could lead within that declared family, but its advantage depended materially on retaining the flower-length channel. `ardens_bridge_loss` remained a plausible restricted alternative in the non-flower channels rather than being uniquely rejected.

Useful lessons:

- a fixed island-order scaffold is not geographic distance, dated colonization history, an isolation mechanism, or pollinator service;
- a candidate winning inside a restricted family does not identify the historical cause represented by its label;
- tempered SMC can improve numerical integration and ranking stability without adding historical observations or causal identification;
- candidate preference that changes under channel ablation is evidence of channel dependence, not a universal island mechanism;
- the bridge-loss and ordinal-order candidates should therefore be treated as competing restricted explanations unless direct mechanism measurements discriminate them.

The five-candidate register and its dedicated source-level workflow are no longer active decision surfaces. Current development instead uses the source-locked focal claim boundaries, the direct effective-service × reproductive-dependency field gate, and explicitly admitted external bridge systems. The retired register/workflow remain recoverable from Git and PR history. Lower-level source-analysis components are not retired by this note and require separate reference and claim audits before removal.

## Virtual Izu calibration and stress suite

Fixed-seed virtual baseline, calibration-bias, finite-detection and field-misspecification runs were useful while the model and measurement design were being stress-tested. They remain simulations rather than empirical evidence.

Useful lessons:

- synthetic recovery can expose estimator bias, detection failure and model misspecification, but cannot validate the historical biological mechanism;
- rerunning the same fixed-seed reports on every unrelated `channel_id/` change adds CI activity without adding empirical information;
- regression protection belongs in unit tests for the underlying modules, while synthetic reports can remain reproducible through their scripts and historical workflow artifacts;
- direct field measurements and source-locked evidence should control current claim promotion, not a synthetic benchmark passing.

The four dedicated Virtual Izu report workflows are retired from routine PR CI. Their scripts, modules, tests and existing documentation remain available for targeted reproduction or later audit.

## Cross-archipelago replication operating-characteristic simulation

A fixed-seed synthetic study compared the same total number of island units distributed across different numbers of independent archipelago systems. It was a design diagnostic, not external empirical replication.

Useful lessons:

- the independent inferential unit for cross-system generalization is the archipelago/system cluster, not each island sampled inside a cluster;
- deep sampling inside only one or two systems cannot substitute for replication across independent systems when between-system heterogeneity is possible;
- treating island units as exchangeable can produce misleading uncertainty and direction-detection behavior when system-level heterogeneity exists;
- the number of independent systems, not simply the total number of islands, should control whether a cross-archipelago effect family is considered replicated;
- synthetic operating characteristics can guide sampling and admission rules but cannot create empirical support for a universal island rule.

The dedicated replication-simulation workflow and its generated JSON/CSV are retired from the active `data/results` surface now that the empirical bridge/effect registries explicitly track independent system clusters. The scenario config, simulator, design module and tests remain available for targeted design work.

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
