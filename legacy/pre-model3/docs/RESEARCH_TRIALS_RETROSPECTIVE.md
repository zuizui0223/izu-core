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

Do not use automatic public-image embeddings or guide-screen outputs as evidence of floral evolution. `CURRENT_EVIDENCE_STATE` keeps `visible_signal = blocked_unmeasured / prospective_only`, so the routine PR workflows that repeatedly acquire/render public-photo, herbarium, ROI and guide-screen artifacts are retired. Claim-boundary and operator-falsification modules/results, prospective field templates, and historical artifacts remain where they still reproduce an adopted negative control or future field contract. One-off public-photo availability probes and other exhausted discovery executors are retired from the active tree and remain recoverable from Git history.

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

## Exhausted automated primary-source routing

OpenAlex, Crossref, DOI/publisher routing and batch candidate searches were useful for resolving bibliographic identity, landing pages and supplement filenames for the independent Izu holdout queue. They did not recover lawful source binaries for the three remaining priority lineages.

Useful lessons:

- metadata, publisher landing pages, DOI resolution and supplement filenames are source-routing evidence, not recovered source bytes;
- repeating the same automated route after it has been audited does not add evidence and can make a blocked acquisition state look active;
- `blocked_external_source_delivery` is a source-availability state, not evidence that the underlying measurements never existed;
- Gate A/Gate B must reopen only when a lawful article/supporting binary or user/library/author-supplied source exposes the required population-level measurements and uncertainty/raw observations;
- the durable asset is the machine-readable exhaustion/admission state, not the one-off discovery workflow that produced it.

The routine OpenAlex, Crossref and priority-DOI routing workflows and their one-off executors/helpers/tests are retired from the active tree. Historical routing outputs and the machine-readable exhaustion/admission state remain; removed implementation is recoverable from Git history if a genuinely new route later warrants it. `independent-source-acquisition.yml` remains active because it validates the current admission state and is the correct gate to rerun when new lawful source material is supplied.

## Hiraiwa-Ushimaru legacy Dryad recovery route

The older 2017 Dryad bulk-download endpoint for the archived interaction workbook is currently credential-blocked (HTTP 401), while the actively used 2024 Hiraiwa-Ushimaru evidence is reproducibly acquired and reanalysed through the Figshare source workflow.

Useful lessons:

- a failed legacy transport route is not a biological result and should not appear as an active evidence gate;
- maintaining two source-recovery workflows for the same mechanistic programme is unnecessary when only one route currently supplies the adopted source-native analysis;
- once the failed Dryad route state and lesson are recorded, its executor and source config do not need to remain in the active tree; they can be recovered from Git history if the endpoint materially changes.

The legacy Dryad workflow, acquisition script and source config are retired from the active tree. The transport failure remains documented here without being promoted to a biological claim. The Figshare acquisition-and-analysis workflow remains active because it reproduces the contemporary FDQ, trait-matching, pollen-receipt and functional-moderation evidence used by the current mechanistic synthesis.

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

The dedicated Virtual Izu report workflows and the finite-detection, calibration-bias, field-misspecification and virtual sensitivity/report layers are retired from the active tree after confirming that they have no current evidence/admission consumer. Their historical implementation remains recoverable from Git. Shared gradient, observational-equivalence and pooled-evidence components are retained because they still support current claim-boundary analyses.

## Synthetic Izu ABM recovery and design audit

A separate exploratory ABM generated synthetic island worlds, classified held-out simulated worlds by standardized distance to scenario centroids, and ranked observation designs by recovery accuracy and a declared burden score. It was useful as a computational identifiability exercise but never supplied empirical evidence for the historical Izu mechanism.

Useful lessons:

- successful recovery among synthetic worlds only shows separability under the declared simulator, feature set, noise model and candidate family;
- a design that minimizes a synthetic burden score is not an empirical sampling optimum and cannot replace measured variance, reliability or field linkage;
- classification accuracy against simulated labels does not identify Bombus loss, reproductive dependency or any historical causal route in nature;
- once the direct Issue #91 field pipeline exists, maintaining a second ABM-specific recovery/design surface adds implementation weight without advancing an open scientific admission gate.

The synthetic ABM, its recovery classifier, design audit, CLIs, documentation and dedicated tests are retired from the active tree. Their methodological lesson is retained here and the full implementation remains recoverable from Git history. Current design decisions should use source-locked evidence and the direct field measurement/admission/precision pipeline.

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

Within this retired-trial family, only components that still enforce a current claim boundary, reproduce an adopted result/negative control, or support a declared field/design gate should remain active. Detailed failed-run products and removed exploratory executors remain recoverable from PR history, Git history and workflow artifacts rather than occupying the active tree.
