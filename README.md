# Izu Core — conditional island plant response and evolutionary realization

`izu-core` is the Chapter 2 repository for asking why the same broad plant–pollinator reorganization can produce different plant responses rather than one universal island trajectory, and how those conditional responses propagate through reproduction, demography and inheritance.

## Current state

**Chapter 2 two-model closure (2026-09-27):** the [response-rule factorial](docs/CHAPTER2_UPDATE_FACTORIAL_RESULTS_20260925.md) shows that neither C/I reversal nor C→I→S is universal across update rules. The completed [Model 3 island campaign](docs/MODEL3_ISLAND_ECOLOGICAL_RESULTS_20260927.md) then carries conditional responses through offspring production, selfing/outcrossing, inheritance, finite demography, connectivity and history. Its 19,968 audited cases show model-conditional historical contingency, assurance-dependent persistence and non-universal inherited floral-investment trajectories. The [final scope and field projection](docs/CHAPTER2_SIMULATION_FINAL_SCOPE_AND_FIELD_PROJECTION_20260925.md) now defines both linked layers and their natural claim ceiling.

**Chapter 2 is scientifically closed without new focal field data, but the journal package is reopened for Model 3 integration.** Its canonical scientific state is **Model 2 response geometry + Model 3 demographic/evolutionary realization + source-audited metadata/secondary-data confrontation**.

```text
Model 2: conditional response geometry
    -> exact realized-richness control
        -> finite-community / system-size determinant hierarchy
            -> downstream filtering and assurance
Model 3: demographic/evolutionary realization
    -> offspring + selfing/outcrossing + inheritance
        -> persistence / extinction + inherited floral investment
            -> history / connectivity / life-history contrasts
                -> source-audited natural claim ceiling
```

The active integration contract is [`data/design/chapter2_model3_integration_lock_20260927.json`](data/design/chapter2_model3_integration_lock_20260927.json). The older [`chapter2_simulation_metadata_completion_lock_20260912.json`](data/design/chapter2_simulation_metadata_completion_lock_20260912.json) remains historical provenance for the pre-Model-3 chapter state, and the existing claim-by-claim map remains [`docs/CHAPTER2_SIM_META_EVIDENCE_MATRIX_20260912.md`](docs/CHAPTER2_SIM_META_EVIDENCE_MATRIX_20260912.md) until the submission evidence matrix is regenerated.

The active manuscript is [`docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md`](docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md). The active narrative lock is [`docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md`](docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md). The existing Oikos manifest [`data/design/chapter2_oikos_submission_manifest_20260831.json`](data/design/chapter2_oikos_submission_manifest_20260831.json) remains the pre-Model-3 submission contract and must be regenerated before submission; current chapter/submission-state supersession is recorded in the 2026-09-27 integration lock.

Historical V2 manuscripts, the former three-result/four-act narrative locks, literature screens and frozen empirical audits remain provenance. They must not be treated as the current manuscript surface.

## Scientific contribution

Island syndromes can conflate three distinct processes:

1. **Colonization / assembly filtering** — which lineages arrive and persist;
2. **In-situ evolutionary change** — how established island lineages diverge from source populations;
3. **Post-establishment interaction response** — how established lineages respond when pollinator functional composition and local interaction context change.

Chapter 2 now links two synthetic layers. **Model 2** isolates post-establishment interaction response and shows a **conditional response geometry**: realized richness helps place the coarse ensemble regime, while plant starting state evaluated against realized community composition retains branch contingency. **Model 3** asks what happens after that functional response reaches reproduction: pollen delivery, reproductive assurance, offspring viability, Mendelian inheritance, density regulation, survival, connectivity and disturbance history jointly determine whether a population persists and how inherited floral investment changes.

The hierarchy of response determinants is **not fixed**. Under the historical small finite-community regime, community realization is the largest additive component. Under the collision-free hierarchical RNG correction, pooling independent community trajectories under active plant adjustment raises the median starting-position share from **3.11% at `k=1` to 53.53% at `k=16`**, while the median community-realization share falls from **74.27% to 14.05%**. Starting position exceeds community realization in **4/6** prespecified seeds at `k=4` and **6/6** at `k=8` and `k=16`; mixed branching remains at `k=16` in **26–36/96** realizations. Historical offset-stream values remain archived as provenance only. The numerical crossover is model-specific and is not a natural threshold.

Exact stepwise realized-richness matching provides the key structural control. Under the collision-free RNG correction it shifts the ensemble mean geometry to all-positive in **6/6** prespecified matching seeds, yet **55–64/96** individual community realizations remain mixed and state × community non-additivity remains **28.48–43.64%**. Therefore the original 2026-09-07 gate requiring mixed **mean** geometry fails; the supported claim is narrower: richness helps set the coarse mean regime, while starting state × realized composition retains branch contingency within that regime. The older equal-turnover result (**70/96** mixed; **65.61%** non-additivity) is retained as a historical offset-stream structural-control record rather than current Monte Carlo inference.

A finite-community limit analysis then shows that the deterministic mean-field kernel contrast is all-positive. Branch heterogeneity is therefore finite-community in the asymptotic sense, but its persistence well beyond rare empty-community events means it is not merely a tiny-N extinction artefact.

These are synthetic mechanism and robustness results, **not natural frequencies or calibrated ecological thresholds**.

## Model 3: demographic and evolutionary realization

The completed island campaign is part of Chapter 2 rather than a post-Chapter-2 side project. It contains **19,968 audited cases** across the frozen island design and six held-out transport rows.

The current chapter-level reading is deliberately qualitative and mechanistic:

- identical final environments can retain different inherited investment endpoints after different visitor-loss histories;
- reproductive assurance can determine whether a terminal evolutionary comparison exists at all;
- seed connectivity and pollinator connectivity act through different routes and should not be collapsed into one isolation coordinate;
- similar S/C/I ordering does not guarantee transport of marginal trait predictions across disturbance regimes.

Model 3 does **not** calibrate natural evolutionary rates, extinction probabilities or a specific flower trait, and numerical refinement remains incomplete for some magnitudes. Those limits are retained in the Chapter 2 claim ceiling.

## Metadata confrontation layer

The source-audited natural layer is part of Chapter 2 completion, but it has a bounded role: **biological plausibility, adversarial stress testing and empirical identifiability**, not full validation of the synthetic mechanism.

The formal source audit remains frozen at **25 research entries across 21 exact geographic labels**:

- direct comparable plant response: **21/25**;
- direct partner arrival/replacement: **2/25**;
- full outcome-independent contracts: **0/25**;
- formal external prediction: **`not_evaluable`**.

A later descriptive layer reached **42 research entries across 37 exact geographic labels**, and the geography-first world programme reached its declared saturation rule. Further cross-sectional searching is therefore not a Chapter 2 completion requirement.

Existing Izu secondary analyses contribute both support and failure:

- functional exposure → corrected matching: supported and leave-one-island sign robust;
- matching → pollen: positive on average but not leave-one-island sign stable;
- eight lower-matching shared targets: tube shorter 3 / longer 4 / equal 1; pollen lower 4 / higher 4;
- historical signed-position projection after null correction: unsupported;
- Oshima bridge as a causal geographic boundary: not independently identified.

That mixture is intentional. The natural evidence makes the modeled ingredients biologically non-vacuous while preventing the simulation from being narrated as already validated historical causation.

## Downstream modifiers

Local filtering and reproductive assurance are retained because they change realized responses without replacing the upstream mechanism. Local filtering reallocates branches asymmetrically; reproductive assurance attenuates magnitude but does not rescue sign within the declared envelope.

## Izu and post-Chapter-2 validation

Izu remains valuable because it offers unusually strong measurement continuity, contemporary functional-network data and an implementation-ready prospective field design. The existing secondary-data layer already contributes to the completed Chapter 2 metadata confrontation.

For the current paper, however, Izu visitor → effectiveness → dependency → mature-seed E3/E4 is an **optional future validation programme, not a submission gate or completion criterion**. Scientifically it is now classified as **post-Chapter-2 transport/falsification**. Present-day Izu associations do not identify historical *Bombus* loss.

## Post-Chapter-2 prospective transport / NEE lane

The previously built NEE Registered Report materials are retained because they provide a rigorous outcome-independent future transport design. They do **not** define an unfinished field-data task for Chapter 2. The Oikos manuscript is currently reopened only to integrate Model 3 text, figures, Supporting Information and render/audit surfaces; this does not create a new empirical completion gate.

Reusable prospective surfaces:

- [`docs/CHAPTER2_NEE_PREDATA_UPGRADE_CONTRACT_20260912.md`](docs/CHAPTER2_NEE_PREDATA_UPGRADE_CONTRACT_20260912.md) — human-readable promotion and stop rules;
- [`data/design/chapter2_nee_predata_promotion_lock_20260912.json`](data/design/chapter2_nee_predata_promotion_lock_20260912.json) — machine-readable P1–P6 / Q1–Q6 promotion contract;
- [`docs/CHAPTER2_NEE_REGISTERED_REPORT_STAGE1_V0_1.md`](docs/CHAPTER2_NEE_REGISTERED_REPORT_STAGE1_V0_1.md) — pre-data Nature Ecology & Evolution Registered Report Stage-1 skeleton;
- [`docs/CHAPTER2_EXTERNAL_TRANSPORT_TRIAGE_20260912.md`](docs/CHAPTER2_EXTERNAL_TRANSPORT_TRIAGE_20260912.md) — bounded role of existing Seychelles, *Nicotiana* and *Guaiacum* evidence.

The future transport design keeps the frozen E1–E4 architecture:

```text
E1  coarse richness/amount regime
E2  pre-outcome plant state × realized composition
E3  visitor → SVD/effective service → dependency → mature seed
E4  qualitative determinant-order confrontation across effective-service breadth/stability
```

Synthetic `k` remains model-specific. Visitor richness, Hill diversity and effective-service breadth are not literal field estimates of `k`, and no field threshold near `k≈4` is predicted.

Any later pilot/precision work belongs to this post-Chapter-2 study. It is not needed to call Chapter 2 complete.

## Chapter 2 / Chapter 3 boundary

Chapter 2 closes with:

1. **Model 2:** conditional response geometry;
2. exact realized-richness separation of coarse regime placement from branch contingency;
3. finite-community/system-size and response-rule results showing regime-dependent determinant ordering;
4. local filtering and assurance as downstream functional modifiers;
5. **Model 3:** explicit reproduction, inheritance and finite-demographic realization of conditional island responses;
6. history, connectivity, life-history and recovery contrasts showing that one current environment need not imply one inherited endpoint; and
7. source-audited metadata / secondary-data confrontation that fixes the natural empirical claim ceiling.

Chapter 3 (`zuizui0223/shimahotarubukuro`) owns the directly measured focal phenotype. Chapter 3 phenotype values are **not** used to tune, rescue, validate or retroactively prove the Chapter 2 mechanism.

## Active scientific and submission surfaces

- [`docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md`](docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md) — active manuscript.
- [`docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md`](docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md) — active narrative contract.
- [`data/design/chapter2_model3_integration_lock_20260927.json`](data/design/chapter2_model3_integration_lock_20260927.json) — active superseding two-model Chapter 2 integration lock.
- [`data/design/chapter2_simulation_metadata_completion_lock_20260912.json`](data/design/chapter2_simulation_metadata_completion_lock_20260912.json) — historical pre-Model-3 completion lock.
- [`docs/CHAPTER2_SIM_META_EVIDENCE_MATRIX_20260912.md`](docs/CHAPTER2_SIM_META_EVIDENCE_MATRIX_20260912.md) — simulation ↔ metadata ↔ claim-ceiling map.
- [`THESIS_CHAPTER_POSITIONING.md`](THESIS_CHAPTER_POSITIONING.md) — dissertation-level two-model Chapter 2 architecture and HOW / proximal-WHY / ultimate-WHY boundary.
- [`docs/MODEL3_ISLAND_ECOLOGICAL_RESULTS_20260927.md`](docs/MODEL3_ISLAND_ECOLOGICAL_RESULTS_20260927.md) — completed Model 3 island ecological readout.
- [`docs/MODEL3_ISLAND_COMPLETE_READOUT_20260927.md`](docs/MODEL3_ISLAND_COMPLETE_READOUT_20260927.md) — complete numerical readout and qualification.
- [`data/design/chapter2_oikos_submission_manifest_20260831.json`](data/design/chapter2_oikos_submission_manifest_20260831.json) — current Oikos submission contract.
- `scripts/render_island_ecology_submission_manuscript.py` — compatibility renderer delegating to the canonical mechanism-mainline render.
- `scripts/render_oikos_submission_rtf.py` — Oikos RTF renderer.
- `scripts/build_island_ecology_submission_bundle.py` — fail-closed submission bundle builder.
- `scripts/build_island_ecology_review_archive.py` — anonymous review archive builder.

## Submission status

The scientific question is closed at the declared two-model claim ceiling, but the **Oikos submission package is not currently submission-ready** because Model 3 has just been promoted into the active manuscript. Before returning to author-only metadata blockers, the Model 3 figure, Supporting Information, renderer output and fail-closed submission audits must be regenerated and checked. No new focal field data are required.

The post-Chapter-2 NEE/field lane may remain pre-data indefinitely without changing Chapter 2 scientific closure.

## Claim boundary

This repository does **not** claim that:

- synthetic response frequencies estimate prevalence in nature;
- the crossover near `k=4` is a natural threshold;
- visitor richness or Hill diversity is literally synthetic `k`;
- the 42/37 descriptive breadth is an independent global prevalence sample;
- the frozen 25 systems validate one universal mechanism;
- metadata constitute full natural validation of the synthetic determinant hierarchy;
- a synthetic [0,1] coordinate is calibrated to a named field trait;
- Model 3 time, dispersal distance, extinction frequency or investment magnitude are calibrated natural rates;
- present functional structure identifies the historical cause of focal-lineage divergence;
- Chapter 3 phenotype validates Chapter 2; or
- the prospective Izu E3/E4 chain is required for Chapter 2 completion.

The retained contribution is a **two-layer synthetic explanation of a recurrent-but-nonuniform island syndrome, completed by source-audited natural confrontation at a bounded claim ceiling**: Model 2 explains conditional functional branching; Model 3 shows how reproduction, assurance, demography, connectivity and history condition persistence and inherited floral trajectories. Existing natural evidence defines which ingredients are biologically supported versus not yet identifiable.

### Interpretation updates (2026-09-25)

- [Simulation novelty and primary-source comparison](docs/CHAPTER2_SIMULATION_NOVELTY_AUDIT_20260925.md)
- [Q1 four-region discussion and Q2 connection](docs/CHAPTER1_FOUR_REGION_TO_CHAPTER2_DISCUSSION_20260925.md)

### Model 3 implementation and completed island campaign

Model 3 is now integrated into Chapter 2. The original calculation foundation remains reproducible with `python -m scripts.verify_model3_reproduction_exposure --out <new-receipt.json>`, while the completed island campaign and its numerical qualifications are documented in [`docs/MODEL3_ISLAND_ECOLOGICAL_RESULTS_20260927.md`](docs/MODEL3_ISLAND_ECOLOGICAL_RESULTS_20260927.md), [`docs/MODEL3_ISLAND_COMPLETE_READOUT_20260927.md`](docs/MODEL3_ISLAND_COMPLETE_READOUT_20260927.md) and [`docs/MODEL3_ISLAND_NUMERICAL_REVIEW_20260927.md`](docs/MODEL3_ISLAND_NUMERICAL_REVIEW_20260927.md). The model remains synthetic and is not a calibrated reconstruction of natural islands.
