# Izu multi-species floral-response meta-analysis — working design

**Status: design (2026-07-03). Public-data, multi-species test of whether the *Campanula microdonta* island-syndrome response generalises across the shared Izu pollinator-loss gradient.**

## Core question

The Izu archipelago shares one environment: a distance-structured loss of bumblebees (*Bombus diversus* mainland → *B. ardens* Ōshima → small bees only, south). Treating each plant species that spans the gradient as a **replicate of the same natural experiment**, do floral/mating-system traits shift in a **shared direction** (floral reduction + selfing), i.e. does the Campanula finding reproduce across many species?

## Predictive structure (this is what makes it a test, not a fishing trip)

- **H1 (specialists):** species dependent on large-bodied bees (bumblebees / long-tongued) for outcrossing → island populations show floral reduction + increased selfing (the Campanula pattern).
- **H0 / falsification (generalists):** species pollinated by many small generalist insects, not bumblebee-dependent → **no trend** (or weak). Included deliberately as negative controls — if these also "shift", the pollinator-loss interpretation is undermined.
- **Counter-direction cases (real):** some Izu endemics **enlarge** flowers — Sakuyuri (*Lilium* cf. *auratum platyphyllum*, world's largest lily flowers) and Ōshima azalea (*Rhododendron*, larger/brighter than mainland *R. kaempferi*). Their pollination systems differ (hawkmoth/large-flower vs bumblebee), so they are expected to break the reduction trend. → **moderator = pollination specialisation / functional group.**
- **Endemic morphology focus:** endemics (シマホタルブクロ, ハチジョウイボタ *Ligustrum*, シマガマズミ *Viburnum*, サクユリ, オオバエゴノキ, etc.) show the strongest morphological divergence — the extreme cases in both directions; analysed as a highlighted subset.

Meta-analytic model: random-effects pooling of a standardised mainland→island floral-response effect size, with **pollination specialisation** as the primary moderator, and terms for **phylogenetic non-independence** and **shared-island dependence**.

## Evidence tiers (honest quality separation — inherited + improved from the seed workflow)

- **Tier 1 — literature (quantitative).** Published mainland vs island floral/mating-system measurements. Anchors so far:
  - Inoue 1986, *Evolution of Campanula punctata in the Izu Islands* (Plant Species Biology) — pollinator change + breeding-system shift.
  - Inoue 1990, *Evolution of Mating Systems in Island Populations of Campanula microdonta: Pollinator Availability Hypothesis* (Plant Species Biology).
  - **Ligustrum ovalifolium** (Oleaceae) — floral morphology + pollinator fauna, island vs mainland populations (second directly usable taxon; also spans 6 Izu islands in GBIF).
  - General theory (not Izu but calibrates expected direction/magnitude): pollinator-loss → rapid selfing-syndrome evolution, smaller/less conspicuous corollas, reduced nectar (Evolution 2022; convergent-selfing-syndrome 2023).
- **Tier 2 — flower photos (semi-quantitative).** iNaturalist/GBIF research-grade images, **blinded scoring** of relative traits (colour intensity, spot/guide presence, relative corolla proportions). Absolute size only where a scale is present. Extends coverage to many species lacking published measurements. (Uses seed workflow's blinded_guide_photo_review.)
- **Tier 3 — occurrence (availability).** GBIF/iNaturalist occurrence = does the species span mainland + ≥N islands. Defines the candidate pool; never a trait value.

## Candidate pool (GBIF, this study)

Broad Izu envelope holds ~41,000 plant occurrences. Per-island facet probe (mainland Izu-peninsula ref + 6 islands):
- **319 plant species** on mainland + ≥2 islands; **289** on ≥3 islands; **113** on ≥5 islands.
- Filtered to insect-pollinated angiosperms (drop ferns, grasses/sedges, wind-pollinated trees): candidate table in `paper/izu_entomophilous_candidates.*` (generated; see script).

## LLM/web literature mining (ongoing)

Selfing / island reproductive-biology research is well advanced; use web search to pull mainland↔island floral/mating-system studies for candidate species and to classify each candidate's pollination functional group (specialist bumblebee vs generalist). This both populates Tier 1 and assigns the moderator.

## Workflow reuse + improvement (from the *Campanula* seed)

Reuses: constrained-simulation power layer (for required replication), four-gate eligibility screen, GBIF/iNat collection, blinded photo review, source-locked transcription. Improvements: pollination-specialisation moderator, counter-direction (enlargement) handling, endemic subset, effect-size + phylogenetic/shared-island dependence gates, PRISMA-style accounting.

## Threshold / anti-cline focus (the headline pattern)

The signature that most strongly implicates pollinator loss — and separates it from a smooth environmental cline — is a **step (breakpoint), not a gradient**. In *Campanula microdonta* autonomous selfing jumps 11%→100% exactly at the *Bombus*-loss boundary (Ōshima→Toshima) instead of rising smoothly (Spearman ρ only +0.34 despite a large mean contrast). The archipelago has **two candidate regime boundaries** — large *Bombus diversus* lost, then *B. ardens* lost, then no bumblebees — already modelled by `channel_id/two_breakpoint_counterfactual.py` (`LARGE_BOMBUS → ARDENS → NO_BOMBUS`) with the Inoue evidence in `data/two_breakpoint_evidence/`.

Meta-analytic test (per species that spans the gradient):
1. Fit **step vs smooth-cline vs none** to each trait along the ordered islands; record the **breakpoint location**.
2. **Shared-breakpoint test:** do specialist species step at the *same* boundary (the bumblebee-loss boundary)? A common breakpoint across independent lineages is far stronger evidence of a common driver than any single cline, and cannot be produced by an unstructured environmental gradient.
3. **Moderator interaction:** predict specialists show a **threshold** at the *Bombus*-loss boundary; generalists show **no step** (flat or weak cline). This is the anti-cline version of the falsification test — a shared threshold in specialists but not generalists is the target result.

Reuses/extends the repo's `two_breakpoint` machinery from one species to the multi-species panel.

## Photo sources incl. SNS / YAMAP (Tier C, with caveats)

Beyond GBIF/iNaturalist, geotagged citizen photos can expand species×island coverage for the blinded photo tier:
- **YAMAP** (JP hiking app) — dense geotagged plant photos on exactly these islands; strong for presence + relative floral traits.
- **SNS** (X/Instagram, hashtag/geotag) — high volume, lower reliability.

Handling: treated as **rank C at best** (blinded relative-trait scoring), often demoted to **rank D** when location/ID is uncertain. Mandatory checks before use: (i) licence/ToS permits research use of the image or only derived measurements are retained; (ii) geolocation actually on the focal island (not a cultivated/garden record); (iii) independent species-ID confirmation; (iv) scale bar required for any absolute size, else relative traits only. These sources **expand volume** but never override peer-reviewed (A/B) evidence, consistent with the rank weighting.

## Evidence ranking (every data point carries an explicit confidence rank)

Each species×trait observation is graded A–E and weighted accordingly (`paper/evidence_ranks.csv`, applied in `paper/evidence_observations.csv`):

| Rank | Tier | What it is | Weight |
|---|---|---|---:|
| A | literature | peer-reviewed **quantitative** (extractable effect size + n) | 1.00 |
| B | literature | peer-reviewed **qualitative** (stated direction, no numbers) | 0.70 |
| C | flower photo | **blinded** relative-trait score from research-grade images | 0.50 |
| D | web description | **non-peer-reviewed** flora/field-guide/park/encyclopaedia text asserting a difference — low confidence, **expands species coverage** | 0.25 |
| E | occurrence | spans the gradient but no trait evidence — pool membership only, not a response point | 0.00 |

Rank **D** is the deliberate low-confidence, volume-expanding tier: when peer-reviewed data are absent for a species, a flora/field-guide statement (e.g. "island form has larger/paler flowers") still enters, but down-weighted and flagged. The pooled estimate is reported both at full weight and in a **rank-A/B-only sensitivity analysis**, so conclusions are never driven by low-confidence text. Seeded observations already include counter-direction D-rank cases (Sakuyuri, Ōshima azalea enlargement) alongside A-rank Campanula reductions.

## Reproducibility (GitHub Actions)

`.github/workflows/meta-analysis-pipeline.yml` runs on every push/PR that touches the pipeline: it installs the package, runs the comprehensive detectability sweep, regenerates the calibration-seed island analysis, and runs `paper/validate_meta_inputs.py` (checks the rank rubric A–E, observation integrity, rank-A⇒effect-size rule, and candidate-pool size). Existing `ci.yml` runs the 257-test suite on Python 3.10–3.12. Together these make the simulation results and the evidence tables reproducible from a clean checkout.

## Honest caveats

Occurrence ≠ trait response; photos rarely give absolute size; historical literature is unevenly available across taxa; isolation rank is a proxy; publication bias toward species that *do* show a pattern (mitigated by deliberately including generalist negative controls and photo-tier species with no prior study).
