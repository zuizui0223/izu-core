# Izu Core — Model 3 island reproductive economics

This repository is the Chapter 2 mechanism paper built around **one ecologically explicit Model 3**.

Current paper title:

> **How island isolation generates floral change: selection conditions, evolutionary sequence and finite realization**

The [2026-10-05 ecological process mainline](docs/CHAPTER2_PROCESS_MAINLINE_20261005.md)
governs the scientific narrative on this branch. The full-mutation
common-environment experiment is complementary genetic/history evidence; it is
not the paper spine.

The 2026-10-05 result is the active paper hypothesis. Its primary delayed-selfing/costly positive-mutation sequence and fixed-assurance predictions are now **independently confirmed under the frozen new-history design**; broader sequence generality is not claimed.

The paper's biological claim is that the order of trait change and the causal
requirement for that change are different questions. Under sustained visitor
replenishment limitation, reproductive assurance often reaches the declared
change threshold before floral investment, yet blocking assurance evolution
does not prevent investment decline. The upstream fixed-plant assay shows why:
visitor limitation lowers the reproductive return to attraction before plant
traits evolve.

This primary process result is now **independently confirmed** under a frozen
new-history design. With 64 new visitor histories and eight new demographic
repeats, the delayed-selfing/costly positive-mutation cell again gave 51/64
assurance-first histories at threshold 0.05 (95% history-bootstrap
0.6875–0.8906). In the separate fixed-assurance replication, far investment
change was −0.3060 [−0.3181, −0.2941] and far-minus-near investment was
−0.4354 [−0.4533, −0.4172]. The confirmed temporal sequence is setting-specific:
the prior-selfing positive-mutation cell did not show an assurance-first
majority at the same threshold.

### Current ecological focus (2026-10-05)

**Does reproductive assurance evolution cause reduced floral attraction, or are
both responses generated in parallel by isolation-altered reproductive returns?**

The strongest completed results are:

- at the same plant state, the delayed-setting investment contribution derivative
  shifts from **+0.5793** under near exposure to **-0.7004** under far exposure;
  the outcross component falls from **+1.6523** to **+0.0854**, while the selfed
  component partly offsets rather than drives that decline;
- under maintained isolation, assurance reaches the primary 0.05 change threshold
  first in **51/64** delayed-setting far histories, with 13 near-simultaneous;
- when assurance is fixed at 0.5, far populations still reduce investment by
  **0.3099** in the delayed setting and **0.3316** in the prior setting, so
  assurance evolution is **not required** for investment decline;
- allowing assurance to evolve can **narrow the near-far investment contrast**
  because investment changes in both environments, so weak geographic divergence
  need not imply weak evolution;
- in the far fixed-trait assay, higher investment can slightly reduce the
  fractional viable pollen deficit while also reducing viable offspring
  (**-15.72 per 48 plants** in the delayed setting), showing that pollen shortage
  and reproductive return are not interchangeable readouts.

The ecological synthesis is therefore **sequence ≠ necessity**: a trait that
changes first is not automatically the cause of a later trait change. Isolation
changes the reproductive economics facing both traits, and their realized
coupling depends on mating assumptions, genetic state and finite population
realization. Time, distance and trait axes remain uncalibrated synthetic
coordinates.

The additional completed cohorts are distinct from the earlier bridge
design described below; shared near references must not be counted as new runs:

- **Sustained isolation:** 2,048 new far trajectories plus 2,048 existing matched
  near references; 64 visitor histories and eight demographic repeats per setting.
  [Results and temporal-order limits](docs/MODEL3_PERSISTENT_PROCESS_RESULTS_20261005.md).
- **Continuous replenishment:** 13 rates at fixed plant capacity 48; 11,264 new
  trajectories plus 2,048 reused positive-mutation endpoints. All 13,312 cases,
  9,984 event records and 156 endpoint rows are independently verified.
  [Complete results and uncertainty](docs/MODEL3_REPLENISHMENT_EVOLUTION_RESULTS_20261005.md).
  Rates represent established visitor types per update, not visits, kilometres or island area.
- **Fixed plants, changed visitor environment:** 768 verified local assays. At the
  same plant state and capacity0.5, the more-isolated visitor histories produce
  lower investment returns and greater pollen-saturation deficits in the reported
  snapshot comparison. This is a local selection diagnostic, not realized evolution.
  [Results and assumptions](docs/MODEL3_FIXEDPLANT_RETURNS_RESULTS_20261005.md).
- **Evolved-plant pollen assays:** 12,288 verified snapshots. Raw seed compensation
  and deficits after inbreeding depression can differ; pollen limitation is not
  interchangeable with visitor scarcity.
  [Assay results](docs/MODEL3_POLLEN_ASSAY_RESULTS_20261005.md).
- **Fixed versus evolving capacity:** all 8,192 trajectories are complete; 84
  estimates were independently reconstructed and 2,048 zero-mutation pairs are
  identical. Investment declines with capacity fixed at0.5. This does not hold
  realized selfing constant. Both modes lack initial assurance-locus variance.
  [Intervention results](docs/MODEL3_ASSURANCE_INTERVENTION_RESULTS_20261005.md).
- **Trait-by-pollen intervention:** 6,912 completed assays separate fractional
  deficits from absolute viable offspring. [Results](docs/MODEL3_TRAIT_POLLEN_RESULTS_20261005.md).
- **Numerical comparison:** the high-resolution 1,000-update run was stopped at the user
  request after verified period7. The positive-mutation long comparison remains
  computationally unresolved; no automatic restart is planned. Completed local,
  fixed-support and restricted mutation diagnostics retain their stated scope.
  [Stop and alternatives](docs/MODEL3_LONG_COMPARISON_DECISION_20261005.md).

Q1 motivates these independent mechanistic questions. Abstract investment is not
an explicit flower-colour or accessibility phenotype, and no regional Q1 pattern
is used to select parameters. See the [H1–H4 correspondence and claim boundaries](docs/MODEL3_Q1_MECHANISM_MAP_20261005.md)
and the [full closeout requirements](docs/MODEL3_ECOLOGICAL_CLOSEOUT_STATUS_20261005.md).

For the explicit trade-offs, fitness accounting and remaining pathway limits, see
[the pollen-to-evolution explanation](docs/MODEL3_POLLEN_FITNESS_PATHWAYS_20261005.md).

The ecological argument is:

```text
isolation -> continuing visitor arrival/loss -> pollen transfer
                              |
              reproductive contributions and local selection
                              |
                 shared reproduction and inheritance
                        /                    \
         finite individual ABM       deterministic genotype density
         sampled offspring           conditional number propagation
                                             |
                                exact mutation / diffusion approximation
```

[Current result priorities and evidence boundaries](docs/MODEL3_RESULT_PRIORITY_AND_PRESENTATION_20261005.md)
separate the ecological headline, unexpected contrasts and mathematical support.

## What the simulation actually contains

Model 3 is a forward eco-evolutionary simulation, not a statistical fit to named islands.

Each diploid plant state contains three trait axes:

- **access / matching** — which visitor functional types the flower matches best;
- **floral investment** — how strongly the plant invests in the pollinator-facing floral phenotype;
- **reproductive assurance** — the capacity for autonomous reproduction when outcross pollen is limited; this axis can be fixed by intervention or allowed to evolve.

Access and floral investment are inherited in the active trajectories; assurance is inherited only in the treatments that explicitly allow it to evolve.

Each visitor has a functional optimum, breadth and effectiveness. Plant–visitor matching determines finite pollen transfer. Floral investment can increase visitor-mediated return but carries a reproductive allocation cost, so the direction favoured by selection depends on both the plant's starting state and the realized visitor environment.

A full Model 3 reproductive update follows this biological order; the fixed-state assay deliberately stops after the reproductive step before inheritance or population updating:

```text
visitor environment
        ↓
functional matching + pollen export / receipt
        ↓
outcrossing + autonomous selfing
        ↓
viable offspring
        ↓
Mendelian inheritance
        ↓
adult survival + seed arrival + finite recruitment
        ↓
next plant population
```

The same reproductive operator is then viewed at three nested levels:

| layer | what is retained | question |
|---|---|---|
| **fixed-state assay** | reproduction only; no inheritance or population update | Which direction of floral investment is favoured now? |
| **deterministic genotype density** | reproduction + exact Mendelian expectation; no demographic sampling | What inherited change is expected without finite-population sampling? |
| **finite-population ABM** | reproduction + inheritance + explicit individuals, recruitment and extinction | Which expected trajectories are actually realized and persist? |

The prospective isolation bridge changes visitor connectivity rather than assigning synthetic cells to real islands. In the frozen bridge, the primary comparison is a **near** versus **far** visitor-arrival environment, followed by prespecified interventions that diagnose different parts of the mechanism: annual visitor-count matching, pooling independent visitor histories, and increasing plant capacity.

That earlier bridge cohort's **24,576 computational cases** are (not the current mutation/intervention campaign size):

```text
128 independent visitor histories
× 3 starting floral-investment states
× 8 nested demographic repeats
× 8 near/far intervention arms
= 24,576 cases
```

The independent ecological denominator is therefore **128 visitor histories**, not 24,576 cases. Synthetic time, distance and trait coordinates are mechanistic coordinates rather than calibrated natural units.

## Current scientific result

The active process paper separates four biological objects that should not be
collapsed:

1. **current reproductive return** — what additional floral investment yields at
   a fixed plant state;
2. **realized evolutionary order** — which inherited trait reaches a declared
   change threshold first;
3. **causal necessity** — whether evolution of the first-changing trait is
   required for the second response;
4. **reproductive consequence** — whether pollen-deficit metrics track absolute
   viable offspring.

The primary process result is now independently confirmed. In the preregistered
delayed-selfing, assurance-cost 0.5, positive-mutation cell, 64 new visitor
histories again produced **51/64 assurance-first histories** at the primary 0.05
threshold (95% history-bootstrap **0.6875–0.8906**). A separate new-history
fixed-assurance replication retained a negative far investment change
(**−0.3060 [−0.3181, −0.2941]**) and negative far-minus-near effect
(**−0.4354 [−0.4533, −0.4172]**).

The supported synthesis is:

- visitor limitation can lower the marginal reproductive return to attraction
  before plant traits evolve;
- reproductive assurance can reach a realized change threshold before floral
  investment in the confirmed delayed/costly regime;
- **temporal precedence is not causal necessity**: investment still declines
  when assurance capacity cannot evolve;
- assurance evolution can narrow the observed near-far investment contrast even
  when both environments undergo substantial within-population evolution;
- a smaller fractional pollen deficit can coexist with fewer viable offspring;
- the assurance-first sequence is **not universal** across reproductive
  settings: prior selfing with positive mutation gave 30/64 assurance-first
  histories at the same primary threshold;
- the effective ecological sample size is 64 visitor histories; eight
  demographic repeats are nested and are not independent ecological replicates.

The 13-rate extension, mutation/history experiments, finite-versus-deterministic
bridge and unresolved high-resolution positive-mutation numerical comparison are
supporting evidence rather than confirmatory substitutes for this process claim.
Stable latent branch prevalence, calibrated natural rates, named historical
causes and region-to-model-cell assignments remain unidentified.

## Active paper surface

Scientific narrative:

- `docs/CHAPTER2_MANUSCRIPT_ACTIVE_20260831.md` — active manuscript.
- `docs/CHAPTER2_PROCESS_MAINLINE_20261005.md` — current claim spine and parallel-model structure.
- `docs/CHAPTER2_CANONICAL_STORY_20260927.md` — historical bridge narrative.
- `docs/CHAPTER2_MODEL_UNIFICATION_DECISION_20260927.md` — why Model 3 is the only active mechanistic model.
- `docs/CHAPTER2_SUBMISSION_ROUTE_FIREWALL_20260927.md` — current/legacy boundary.
- `docs/MODEL3_Q1_MECHANISM_MAP_20261005.md` — current independent H1–H4 correspondence.
- `docs/CHAPTER1_CHAPTER2_CANONICAL_BRIDGE_20260927.md` — historical Chapter 1 → Chapter 2 handoff.

Model 3 evidence:

- `docs/MODEL3_ISLAND_ECOLOGICAL_RESULTS_20260927.md`
- `docs/MODEL3_ISLAND_NUMERICAL_REVIEW_20260927.md`
- `docs/MODEL3_CH2_BRIDGE_PROSPECTIVE_RESULTS_20260927.md`
- `docs/MODEL3_CH2_BRIDGE_ECOLOGICAL_RESULTS_20260928.md`
- `data/results/model3_ch2_bridge_prospective_frozen_20260927.json`
- `data/results/model3_island_v2_summary/`

Historical bridge-submission control (not the newer process manuscript):

- `data/design/chapter2_unified_model3_lock_20260927.json`
- `data/design/chapter2_oikos_submission_manifest_20260927.json`
- `data/results/chapter2_submission_closure_audit_20260928.json`

Implementation:

- `scripts/model3_island/` — finite-population and deterministic Model 3 implementation.
- `scripts/model3_island_bridge_ops.py` — prospective bridge interventions.
- `scripts/render_chapter2_process_manuscript.py` — current process manuscript renderer.
- `scripts/figure_model3_selection_process.py`, `scripts/figure_model3_sequence_necessity.py`, `scripts/figure_model3_return_components.py`, `scripts/figure_model3_genetic_realization.py` — current primary figures.
- `scripts/figure_model3_replenishment_evolution.py` — complete replenishment-gradient panels.
- `scripts/generate_chapter2_unified_model3_figures.py` — historical bridge Figures 1–4.
- `scripts/render_chapter2_oikos_generality_overlay.py` — historical snapshot renderer.
- `scripts/render_chapter2_supporting_information.py` — historical bridge Supporting Information.
- `scripts/build_island_ecology_submission_bundle.py` — historical Oikos bundle.
- `scripts/build_island_ecology_review_archive.py` — historical anonymous reviewer archive.

## Natural evidence boundary

Natural systems confront the mechanism by layer rather than being fitted to synthetic parameter cells.

- **A — ecological / selection:** partly observed.
- **B — inherited longitudinal response:** the principal natural-data gap.
- **C — finite / history realization:** partly observed through founding, partner-loss, recovery and persistence systems.

The broader source programme contains **42 research entries / 37 exact geographic labels**. The formal identifiability audit contains **0/25 complete A → B → C contracts**. These counts are evidence-breadth descriptors, not branch-prevalence estimates.

Chapter 3 phenotype values are **not** used to tune, rescue, validate or retroactively prove Chapter 2. Future field work is prospective transport/falsification.

## Reproduction

Fast reviewer checks:

```bash
python -m pip install -e '.[dev]'
pytest -q \
  tests/test_chapter2_model3_submission.py \
  tests/test_chapter2_mechanistic_funnel.py \
  tests/test_chapter2_branch_identifiability_boundary.py \
  tests/test_chapter2_independent_unit_reporting.py \
  tests/test_chapter2_submission_closure_audit.py \
  tests/test_chapter2_unified_model3_figures.py \
  tests/test_model2_legacy_firewall.py
```

Full active regression surface:

```bash
pytest -q
```

Full 24,576-case regeneration is manual-only through `.github/workflows/model3_ch2_bridge_production.yml`. See `REPRODUCE.md`.

## Legacy archive

Historical work remains recoverable but is not part of the current paper or automatic scientific gate:

- `legacy/model2/` — retired Model 2 response geometry, synthetic-`k`, S/C/I and former SI controls.
- `legacy/routes/nee/` — retired NEE route.
- `legacy/routes/ecology-letters/` — retired Ecology Letters analytical route.
- `legacy/submission-history/` — superseded manuscript and submission drafts.
- `legacy/model3-development/` — superseded Model 3 development notes.
- `legacy/pre-model3/` — pre-Model3 top-level scripts and tests.

Git history remains the authoritative provenance for removed current-tree locations. Legacy files must not be cited as current manuscript surfaces.

## Claim ceiling

Do not claim that:

- Model 3 is calibrated to natural kilometres, geological time or evolutionary rates;
- mixed-history fractions estimate natural branch prevalence;
- annual visitor-count matching is a pure field species-richness experiment;
- visitor pooling is literal island number or lifespan;
- the deterministic genotype-density model is a diffusion PDE;
- current Izu associations identify historical *Bombus* causation;
- cross-sectional floral morphology is a measured inherited longitudinal trajectory.
