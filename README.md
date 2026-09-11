# Izu Core — conditional island plant response geometry

`izu-core` is the Chapter 2 repository for asking why the same broad plant–pollinator reorganization can produce different post-establishment plant responses rather than one universal island trajectory.

## Current state

**Chapter 2 is scientifically closed, and the synthetic gate is closed.** The active paper follows one mechanism-first sequence:

```text
conditional response geometry
    -> exact realized-richness control
        -> finite-community / system-size determinant hierarchy
            -> downstream filtering and assurance
                -> bounded empirical claim ceiling
```

The active manuscript is [`docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md`](docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md). The active narrative lock is [`docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md`](docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md), and the Oikos route is controlled by [`data/design/chapter2_oikos_submission_manifest_20260831.json`](data/design/chapter2_oikos_submission_manifest_20260831.json).

Historical V2 manuscripts, the former three-result/four-act narrative locks, literature screens and frozen empirical audits remain provenance. They must not be treated as the current manuscript surface.

## Scientific contribution

Island syndromes can conflate three distinct processes:

1. **Colonization / assembly filtering** — which lineages arrive and persist;
2. **In-situ evolutionary change** — how established island lineages diverge from source populations;
3. **Post-establishment interaction response** — how established lineages respond when pollinator functional composition and local interaction context change.

Chapter 2 isolates the third layer. Its central result is a **conditional response geometry**: realized richness helps place the coarse ensemble regime, while plant starting state evaluated against realized community composition retains branch contingency.

The hierarchy of response determinants is **not fixed**. Under the historical small finite-community regime, community realization is the largest additive component. As independent community trajectories are pooled under active plant adjustment, the median starting-position share rises from **2.55% at `k=1` to 55.84% at `k=16`**, while the median community-realization share falls from **72.98% to 12.72%**. Starting position exceeds community realization in all six prespecified seeds from `k=4` onward, while mixed branching remains at `k=16` in **28–42/96** realizations. The numerical crossover is model-specific and is not a natural threshold.

Exact stepwise realized-richness matching provides the key structural control. It shifts the ensemble mean geometry to all-positive in **6/6** prespecified matching seeds, yet **51–65/96** individual community realizations remain mixed and state × community non-additivity remains **42.72–48.51%**. Equalizing the baseline partner-arrival/loss rates still leaves **70/96** mixed realizations and **65.61%** non-additivity.

A finite-community limit analysis then shows that the deterministic mean-field kernel contrast is all-positive. Branch heterogeneity is therefore finite-community in the asymptotic sense, but its persistence well beyond rare empty-community events means it is not merely a tiny-N extinction artefact.

These are synthetic mechanism and robustness results, **not natural frequencies or calibrated ecological thresholds**.

## Downstream modifiers

Local filtering and reproductive assurance are retained because they change realized responses without replacing the upstream mechanism. Local filtering reallocates branches asymmetrically; reproductive assurance attenuates magnitude but does not rescue sign within the declared envelope.

## Empirical claim boundary

World and Izu evidence now have a bounded role: biological plausibility, falsification context, reviewer audit and identification of what remains unmeasured. They are **not required validation** of the synthetic determinant hierarchy.

The formal source audit remains frozen at **25 research entries across 21 exact geographic labels**:

- direct comparable plant response: **21/25**;
- direct partner arrival/replacement: **2/25**;
- full outcome-independent contracts: **0/25**;
- formal external prediction: **`not_evaluable`**.

A later descriptive layer reached **42 research entries across 37 exact geographic labels**, and the geography-first world programme reached its declared saturation rule. Those assets remain Supporting Information/provenance rather than a coequal manuscript result.

## Izu and future validation

Izu remains valuable because it offers unusually strong measurement continuity, contemporary functional-network data and an implementation-ready prospective field design. Existing Izu analyses also preserve useful negative results, including the unsupported null-corrected historical signed-position projection and the unsupported prespecified Oshima-source bridge.

For the current paper, however, Izu visitor → effectiveness → dependency → mature-seed E3/E4 is an **optional future validation programme, not a submission gate or completion criterion**. Present-day Izu associations do not identify historical *Bombus* loss.

## Chapter 2 / Chapter 3 boundary

Chapter 2 closes with:

1. conditional response geometry;
2. exact realized-richness separation of coarse regime placement from branch contingency;
3. a finite-community/system-size result showing regime-dependent determinant ordering; and
4. downstream modifiers plus a bounded empirical claim ceiling.

Chapter 3 (`zuizui0223/shimahotarubukuro`) owns the directly measured focal phenotype. Chapter 3 phenotype values are **not** used to tune, rescue, validate or retroactively prove the Chapter 2 mechanism.

## Active scientific and submission surfaces

- [`docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md`](docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md) — active manuscript.
- [`docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md`](docs/CHAPTER2_MECHANISM_MAINLINE_LOCK_20260911.md) — active narrative contract.
- [`THESIS_CHAPTER_POSITIONING.md`](THESIS_CHAPTER_POSITIONING.md) — dissertation-level HOW / proximal-WHY / ultimate-WHY boundary.
- [`data/design/chapter2_oikos_submission_manifest_20260831.json`](data/design/chapter2_oikos_submission_manifest_20260831.json) — current Oikos submission contract.
- `scripts/render_island_ecology_submission_manuscript.py` — compatibility renderer delegating to the canonical mechanism-mainline render.
- `scripts/render_oikos_submission_rtf.py` — Oikos RTF renderer.
- `scripts/build_island_ecology_submission_bundle.py` — fail-closed submission bundle builder.
- `scripts/build_island_ecology_review_archive.py` — anonymous review archive builder.

## Submission status

The scientific gate is closed. Non-metadata submission surfaces are intended to close on the mechanism-mainline contract; actual submission remains fail-closed on author-supplied identity and declaration fields such as author order/affiliations, corresponding-author details and ORCID, prior-work context, acknowledgements/funding, inclusion/conflict declarations, ethics confirmation and final metadata-driven bundle construction.

## Claim boundary

This repository does **not** claim that:

- synthetic response frequencies estimate prevalence in nature;
- the crossover near `k=4` is a natural threshold;
- visitor richness or Hill diversity is literally synthetic `k`;
- the 42/37 descriptive breadth is an independent global prevalence sample;
- the frozen 25 systems validate one universal mechanism;
- a synthetic [0,1] coordinate is calibrated to a named field trait;
- present functional structure identifies the historical cause of focal-lineage divergence;
- Chapter 3 phenotype validates Chapter 2; or
- the prospective Izu E3/E4 chain is required for Chapter 2 completion.

The retained contribution is a **synthetic conditional-response mechanism with a bounded empirical claim ceiling**: richness influences coarse regime placement, state × realized composition retains branch contingency, determinant ordering changes across finite-community regimes, and downstream processes modify rather than replace that architecture.
