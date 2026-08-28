# Chapter 2 external-prediction upgrade audit

**Decision date:** 2026-08-28
**Decision:** C — formal external prediction is not supported by the current world-data set
**Maximum supported claim:** Level 2
**Manuscript route:** retain the conditional-response-geometry Research Article; do not rebrand it as an Ecology Letters external-prediction paper

## Current state fixed before the new audit

The live GitHub state was re-read rather than inherited from an earlier summary.

- `origin/main` was `98cbb6975295e8c2b8f72291a895d145dbf76f36`, “Render Chapter 2 as a journal-clean submission manuscript”.
- Main CI run `33081110643` passed at that SHA.
- The Chapter 2 scientific-gate run `33081110617` failed before simulation because direct script execution could not import the `scripts` package. The workflow fix in this branch changes only the entrypoint to `python -m scripts...`; it does not change model rules, seeds, points, realizations or thresholds.
- PR #307 was open, mergeable and green. Its scope is submission-metadata synchronization and does not supply new scientific evidence.
- Draft PRs #300 and #304 remained incomplete/failing historical Izu recovery lanes; the active v2 Izu artifacts are already on main and control this audit.
- The active scientific surfaces were `docs/CHAPTER2_CANONICAL_STORY_20260827.md`, `docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_V2_20260827.md`, `docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_SUPPORTING_INFORMATION_20260827.md`, `data/design/chapter2_active_manuscript_mainline_20260827.json` and `data/design/island_ecology_jecology_submission_manifest.json`.

The frozen synthetic facts were reproduced from repository artifacts:

- 96 matched community realizations: 41 mixed-sign, 42 all-positive and 13 all-negative;
- 48 fixed joint points: 16 mixed, 22 all-positive and 10 all-negative mean geometries;
- fixed-surface driver associations: partner loss positive and partner arrival negative for the negative fraction of the starting-position grid;
- baseline sum-of-squares partition: starting position 2.18%, community realization 80.17%, non-additivity 17.64%;
- local filtering changed sign bidirectionally but more readily removed positive branch identity;
- assurance attenuated magnitude but rescued 0 of 580 eligible baseline declines through 4×;
- Izu raw matching followed source state plus broad composition, whereas null-corrected matching was unsupported.

## Design chronology

The external-readiness design was committed before the new admission summary was computed:

- design: `data/design/chapter2_external_prediction_challenge_freeze_20260828.json`;
- source-level audit: `docs/CHAPTER2_EXTERNAL_PREDICTION_SOURCE_AUDIT_20260828.md`;
- machine ledger: `data/design/chapter2_external_prediction_admission_ledger_20260828.csv`;
- deterministic evaluator: `scripts/run_chapter2_external_prediction_readiness.py`;
- frozen result: `data/results/chapter2_external_prediction_readiness_frozen_20260828.json`.

This is not a literature-blind chronology. Published outcomes were already known. The freeze prevents a new round of system replacement, predictor invention, threshold selection or post-hoc fitting; it cannot turn historical papers into prospective data.

## Model-derived control axes

The ten synthetic parameters can be organized into four interpretable control axes without refitting the response surface.

| Axis | Definition | Model basis | Empirical minimum |
|---|---|---|---|
| `T`, turnover imbalance | `z_loss - z_arrival`, with both terms centered and divided by their declared synthetic range | loss and arrival were the two largest sign-stable transition-surface associations | directionally identified loss and arrival/replacement on one transition unit; richness alone is insufficient |
| `D0`, source functional displacement | `(plant source position - partner source centre) / partner source scale` | the matching equation and starting-position response geometry | commensurate source plant and partner traits with a source-defined scale |
| `C`, realized-community shift | `(target partner centre - source partner centre) / partner source scale` plus separately reported richness, FD and turnover | community realization dominated cell-level variation and combined non-additively with position | source and target composition with functional traits on the matched plant-system unit |
| `F`, local filtering | `1 - realized positive opportunity / feasible positive opportunity` | the local projection only removes active plants, partners or feasible pairs and reallocates branches asymmetrically | a prespecified feasible opportunity set plus its matched realized local interactions |

Reproductive assurance is not a fifth sign-regime axis. It remains a downstream magnitude modifier because the frozen envelope produced no sign rescue. The axes are dimensionless coordinates, not empirical calibration of the synthetic `[0,1]` trait axis.

## Competing hypotheses

The frozen design distinguishes:

- `H0`: one universal response direction;
- `H1`: response organized by `D0` alone;
- `H2`: response organized by `T` alone;
- `H3`: response organized by source state × realized community, with the prespecified matching score `abs(D0) - abs(D0 - C)`;
- `H4`: `H3` plus a source-native mapping of `F`.

The formal comparison required at least four geographically de-duplicated systems with one comparable response family, a common outcome-independent predictor contract, matched units and evaluable `H0`–`H3`. Repeated sites, species, seasons, islands within one archipelago, colonization pairs and publication layers were not allowed to increase system `n`.

## Source-admission result

The audited universe contains 25 research entries, not 25 independent archipelagos:

| Layer | Entries |
|---|---:|
| strict manuscript systems | 13 |
| additional cross-archipelago targets | 6 |
| model-development / falsification targets | 6 |

The full Chapter 2 plant-response contract passed in `0/25` entries. Current admission classes are:

| Admission class | Entries |
|---|---:|
| admissible prospective-like full challenge | 0 |
| retrospective explanatory test only | 12 |
| reality boundary only | 8 |
| source-gated / unusable | 5 |

Four entries retain narrower pre-target chronology, but none supplies the requested full challenge. Dominica retains a failed publication-aware signed-position/selection-gradient prediction. Menorca, Cabrera and Giannutri retain network-architecture or local-realization tests without a linked plant-response target. These results remain scientific evidence and falsification; they are not promoted to tests of the joint plant-response surface.

Predictor availability explains the stop. Across the 25 entries, direct or source-derived information exists for source state in 10, community functional shift in 18 and local filtering in 20, while a response quantity exists in 21. Those marginal counts do not align on common units, response families or pre-outcome mappings. The intersection required for an `H0`–`H3` comparison is zero.

## Why the formal analyses were not run

The result is `not_evaluable`, not a negative prediction score.

- `H0`–`H4` model comparison: not evaluable;
- leave-one-system-out: not evaluable;
- leave-one-archipelago-out: not evaluable;
- exact system-label permutation: not evaluable.

Running any of these after imputing missing axes from published response categories would encode the outcome in the predictors. Pooling flower morphology, network topology, pollen receipt, selection gradients and seed outcomes as one ordinal target would also manufacture a response scale that the sources do not share. No classifier was fitted and no system was deleted or replaced by fit.

## Geographic overlap

The ledger has 21 overlap labels for de-duplication, but this is not an independent-archipelago denominator. Important overlaps include:

- strict and additional Ogasawara datasets within one archipelago;
- strict Seychelles disruption and the Mahé network target;
- Menorca and Cabrera within the Balearic region;
- Izu 2017 and 2024 within one focal system;
- linked Hawaiʻi, Nicotiana and Caribbean Gesneriaceae publication sets;
- Rhabdothamnus, Ciarle, Hendriks and Hetherington–Rauth–Johnson across overlapping New Zealand / Southwest Pacific frames;
- nested islands or networks within Galápagos, Wanshan–Yongxing, Mahé, Giannutri and Thousand Island Lake.

Exact cross-study site membership is not available for every multi-system synthesis, so the audit does not report a de-duplicated global `n`.

## Izu anchor and Chapter 3 boundary

No defensible outcome-independent scalar score selected Izu from the global universe. Eligibility, criteria, weights, missingness rules and ties were not frozen before Izu became the focal programme, and adding Chapter 3 phenotype or later field accessibility would reward evidence accumulated after selection.

The allowed statement is narrower: Izu is the data-depth focal triangulation because the programme can connect repeated island networks, quantitative plant–visitor traits, cross-study reproductive information and feasible mechanistic follow-up. This is a transparent design rationale, not an outcome-independent ranking or a validation win.

Chapter 3 phenotype is not used in the score, predictor ledger, response target or Chapter 2 evidence. The dissertation handoff remains:

```text
Chapter 1: WHEN / WHERE regional response vectors differ
    -> Chapter 2: HOW and model-conditional proximal WHY heterogeneous responses are possible
        -> Chapter 3: WHAT phenotype structure is realized in one focal lineage
```

Ultimate WHY remains outside Chapter 2: the analyses do not identify why an island acquired its species pool, source state, colonization history or interaction architecture.

## Figure design

A defensible two-panel figure can be built without projecting unavailable systems into model regimes.

1. **General response phase diagram:** synthetic `T` against matching displacement derived from `D0` and `C`, with uncertainty or realization density and local-filtering branch transitions shown as arrows. Synthetic coordinates and regime frequencies remain labelled as design diagnostics.
2. **External-system projection matrix:** rows are the 25 audited entries and columns are `D0`, loss, arrival/replacement, `C`, richness/FD, `F`, assurance and outcome. Direct, proxy and unavailable cells are shown explicitly. Systems without a full contract remain outside the phase plane rather than being placed from their observed outcome.

Because the empirical projection gate failed, this is a figure design, not a fabricated global phase-map result.

## Decision and next valid gate

The current data support:

> **Level 2 — a conditional synthetic response geometry explains why heterogeneous post-establishment responses are possible.**

They do not support Level 3 because observable variables do not yet place independent systems into predicted regions on a common, outcome-independent contract. Consequently, Level 4 held-out prediction is also unavailable. The Ecology Letters upgrade is not justified from the current repository and public-source state.

The current Journal of Ecology route is not weakened by this decision. External systems remain source-audited reality boundaries, retrospective explanations and retained falsifications. The next valid Level-3 gate requires a newly frozen system or prospective Izu programme with source functional state, directionally identified community perturbation, partner-weighted local filtering, independent assurance and a withheld reproductive response.

Existing public-source routes should reopen only on narrow evidence triggers:

- Galápagos: a provenance-matched raw plant-level network package;
- Hetherington–Rauth–Johnson: the source-native numeric 136-pair table plus measurement uncertainty;
- Mahé: the declared source workbook or an author/institutional copy with identical provenance;
- Thousand Island Lake: a source-native site × time linkage that jointly identifies opportunity and interaction units.

None of those recoveries alone is presumed to create Level 3. Open-ended searching or predictor reconstruction from known outcomes remains closed.
