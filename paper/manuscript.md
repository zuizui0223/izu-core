# Does floral reduction under pollinator loss generalise across an island flora? A public-data, multi-species, mechanism-resolved test of the flower-size island rule on the Izu gradient

**Draft manuscript. Version 0.4 (2026-07-03). Multi-species synthesis (public data + simulation).**
Author: zuizui0223. A single system (*Campanula microdonta*, Izu) is used only as a fully-measured calibration seed and workflow template; the study question is comparative. All results are reproducible from this repository and CI (see *Reproducibility*).

---

## Abstract

Island flowers are famously smaller, less showy, and more selfing than mainland relatives, and this is usually attributed to the loss of effective pollinators. But the attribution is almost always argued one species at a time, where floral traits, pollinator regime, establishment, environment, and colonisation history are hopelessly confounded along the same axis. We ask instead whether the response is **shared across many species** that experience *one common environment* — the Izu archipelago's distance-structured loss of bumblebees — and whether its sign follows what pollination biology predicts. This turns the Izu chain into a mechanism-resolved test of the **flower-size "island rule"**: island flowers evolving toward intermediate, pollinator-size-matched sizes under a less diverse, smaller-bodied fauna.

We assemble the test entirely from public data, using a workflow generalised and improved from a single-species channel-identification pipeline. From GBIF we identify **156 insect-pollinated angiosperms** that span the mainland + ≥2 Izu islands (16 on all six). We classify each by pollination functional group (the moderator): **30 bumblebee/long-tongue specialists vs 89 open-flower generalists**, plus 13 large-flowered non-bee species. Every trait observation is graded on an explicit **A–E evidence hierarchy** (peer-reviewed quantitative → web/flora description), and pooled at full weight and rank-A/B-only. A comprehensive simulation (90 parameter cells) shows the design can recover the true mechanism across the space **only if the environmental background is calibrated** (95–99% vs 0% for naive analysis at realistic loss depths), and that visitation data alone are insufficient — an interaction-level channel is required.

Current synthesis: the fully-measured seed species shows corolla reduction (lnRR = −0.77, −54%) and a selfing increase that **steps** at the bumblebee-loss boundary rather than clining smoothly (an "anti-cline" threshold, detected automatically). A second peer-reviewed species (*Ligustrum ovalifolium*) shows the same island corolla-tube/stamen reduction, most pronounced on the most isolated island. Large-flowered non-bee species (Sakuyuri lily, Ōshima azalea) run the other way, enlarging — as the island rule predicts. The rank-weighted direction score is strongly positive for specialists and intermediate-tubular species and negative for large-flowered ones; the generalist negative-control cells remain the key data gap, to be filled from the photo tier. We present this as a reproducible, honestly-graded framework and a first result, not a completed pooled estimate.

---

## 1. Introduction

The reproductive "island syndrome" — smaller, less conspicuous flowers and increased autonomous selfing — recurs across island floras and is generally explained by reproductive assurance under pollinator scarcity. The explanation is ecologically compelling but inferentially weak when built on one species, because a single mainland→island trait cline is equally consistent with an environmental gradient, drift on small islands, or colonisation history.

Two moves strengthen it. First, treat **many co-distributed species as replicates of one shared natural experiment**: if a common pollinator change drives the syndrome, species exposed to the same change should respond in parallel, and species *not* dependent on the lost pollinators should not. Second, make the prediction **directional and mechanism-specific** using the flower-size island rule: under a less diverse, smaller-bodied island pollinator fauna, flowers should evolve toward intermediate, pollinator-matched sizes — so large-flowered bumblebee specialists should reduce most, already-small generalists should barely change, and large non-bee flowers may even enlarge.

The Izu archipelago is an unusually clean setting: bumblebees (*Bombus diversus* on the mainland, *B. ardens* only on the nearest island) drop out with distance, leaving small halictid/megachilid bees. We use it to test whether floral reduction under pollinator loss **generalises across the flora**, and whether its sign matches the island-rule prediction — assembling the whole test from public data (occurrence, literature, and citizen photos) with an explicit evidence hierarchy.

### 1.1 Contributions

1. A public-data, multi-species test framework for pollinator-loss-driven floral evolution, generalised and improved from a single-species workflow.
2. A GBIF-derived candidate pool (156 species) with a transparent pollination-functional-group moderator (30 specialist vs 89 generalist).
3. An A–E evidence hierarchy applied to every observation, with rank-weighted synthesis reported at full and high-confidence-only weight.
4. An automatic step/cline classifier that localises the "anti-cline" threshold to the bumblebee-loss boundary.
5. A comprehensive simulation delimiting when the signal is recoverable, and honest identification of the remaining data gaps.

---

## 2. Materials and methods

### 2.1 Shared environment and species pool

The Izu chain (mainland reference + Ōshima, Toshima, Niijima, Kōzushima, Miyake, Hachijō) carries one distance-structured pollinator gradient. From a broad GBIF envelope (~41,000 plant occurrences) we facet occurrences per island and retain insect-pollinated angiosperms present on the mainland + ≥2 islands: **156 species** (`paper/izu_entomophilous_candidates.csv`), 16 on all six islands.

### 2.2 Moderator: pollination functional group

Each species is assigned specialist_bee / generalist_open / large_flower / nonbee_special / abiotic_ambig by family with genus overrides and a recorded confidence (`paper/classify_functional_groups.py`). Primary contrast: **30 specialist vs 89 generalist**; 13 large-flower (counter-direction), the rest off-hypothesis. Prediction (island rule): specialists reduce most; generalists ≈ 0 (negative control); large non-bee flowers may enlarge.

### 2.3 Evidence hierarchy and tiers

Every species×trait observation is graded (`paper/evidence_ranks.csv`): **A** peer-reviewed quantitative (weight 1.0), **B** peer-reviewed qualitative (0.7), **C** blinded photo score (0.5), **D** web/flora description (0.25, low-confidence volume-expander), **E** occurrence-only (0.0). Data tiers: Tier-1 literature; Tier-2 blinded flower photos (iNaturalist/GBIF-media/YAMAP/SNS); Tier-3 occurrence. A blinded photo pipeline (`paper/build_photo_scoring_sheet.py`) shuffles per-region images and hides the island until after scoring.

### 2.4 Response shape (anti-cline threshold)

`channel_id/gradient_shape.py` selects among none/cline/step by AICc (sized for small per-species n) and returns the breakpoint location — the multi-species generalisation of the *Campanula* selfing threshold. A **shared** breakpoint at the bumblebee-loss boundary across independent specialists is stronger evidence of a common driver than any single cline.

### 2.5 Synthesis and design validation

Effect sizes use the log response ratio (mainland vs most-isolated island); where only direction is known, a rank-weighted direction (vote) synthesis by functional group is reported at full and A/B-only weight (`paper/meta_synthesis.py`). A comprehensive simulation over pollinator-loss depth × environmental confound × island number × analysis mode (`paper/comprehensive_sweep.py`) establishes when recovery is possible.

---

## 3. Results

### 3.1 The design works only with environmental calibration (simulation)

Across 90 parameter cells (300 replicates), an analysis that calibrates the per-island environment recovers the true pollinator-loss mechanism in **95–99%** of replicates at every loss depth; the same analysis ignoring the background collapses to **~10%** at a modest loss and to **0%** (rejecting all mechanisms) once service drops by ≥0.40 — worst exactly where the syndrome is strongest. Visitation data alone give 0% unique recovery (95% false-mechanism survival); one interaction-level channel (pollen deposition) restores 91%. Usable discrimination needs ~90 plant-units/island.

### 3.2 The seed species: reduction (cline) + a threshold selfing shift

*Campanula microdonta* corolla length falls from 49.9 mm (mainland) to 23.1 mm (Hachijō): **lnRR = −0.77 (−54%)**, a smooth cline (ρ = −1.00). Autonomous selfing instead **steps**: bagged capsule set jumps 11%→100% exactly at the Ōshima→Toshima bumblebee-loss boundary (classifier: step at order ≈ 1.5), while temperature is flat and precipitation steps at a *different* boundary — climate does not co-localise with the reproductive threshold.

### 3.3 Three independent specialist lineages reduce; large non-bee flowers enlarge

The reduction is not confined to *Campanula*. **Three independent bumblebee-associated lineages** shift the same way: *Ligustrum ovalifolium* (Oleaceae; Kato et al. 2014, Bot. J. Linn. Soc. 174:489) has shorter corolla tubes and stamens on the islands, most pronounced on the most isolated island; and *Chionographis japonica* (Melanthiaceae; Suetsugu et al. 2024, New Phytologist) has **shorter floral tubes on Kōzushima under bumblebee absence**, shifting to short-tongued *Xylocopa*. In the opposite direction, large-flowered non-bumblebee taxa enlarge: the Sakuyuri lily (*Lilium auratum*; Nakajima 2018, Plant Species Biol.) and the Ōshima azalea (larger, brighter than mainland *Rhododendron kaempferi*) — as the island rule predicts for flowers not tied to the lost bumblebees.

### 3.4 Rank-weighted synthesis

| Functional group | Weighted direction score | Support / oppose |
|---|---:|---:|
| specialist_bumblebee (Campanula, Chionographis) | **+4.65** | 6 / 0 |
| intermediate_tubular (*Ligustrum*) | **+1.40** | 2 / 0 |
| large_flower (Sakuyuri, azalea) | **−0.95** | 0 / 2 |
| generalist_open (negative control) | — | **no data yet** |

The predicted structure holds across independent lineages: every specialist/intermediate observation supports floral reduction/selfing; both large non-bee taxa oppose it (enlargement). The A/B-only sensitivity preserves the whole pattern (now mostly peer-reviewed). The **generalist control cells remain empty** — the decisive falsification test cannot be populated from available data (§4), the one acknowledged incompleteness.

---

## 4. Discussion

Assembled from public data across many co-distributed species, the Izu evidence so far is consistent with a shared, pollinator-loss-driven floral response whose **sign tracks pollination biology** rather than geography alone: bumblebee-dependent species reduce and self more (with the reproductive-assurance component appearing as an anti-cline **threshold** at the loss boundary), while large non-bee flowers move the other way. That directional split is what the flower-size island rule predicts and is hard to reproduce with an unstructured environmental gradient or drift, which have no reason to respect pollination functional groups or to place a shared breakpoint at the bumblebee boundary.

The two response axes are not equally supported, and we say so. **Floral morphology** (size/tube reduction) carries the signal across independent lineages; the **mating-system axis** (selfing) is thin — a dedicated search found no quantitative outcrossing-rate series beyond *Campanula*, with only qualitative self-compatibility elsewhere (e.g. insular *Clerodendrum izuinsulare* more self-compatible than its widespread congener), framed by Baker's law. Conclusions about increased *selfing* therefore rest largely on one genus, whereas conclusions about floral *reduction* are multi-lineage.

The honest limits are explicit and drive the remaining work. Only one species is fully quantitative (a variance-weighted random-effects estimate needs more effect sizes); the **generalist negative controls are unfilled**, and because peer-reviewed generalist floral series are scarce, they must come from the blinded photo tier, which single-source coverage shows is sparse (Toshima especially) and needs pooling across iNaturalist, GBIF media, YAMAP, and SNS. *Prunus speciosa* is excluded (island origin, inverted polarity). The simulation (§3.1) is a reminder that even with more data, the analysis must calibrate the per-island environment or it will mis-identify the mechanism.

---

## 5. Reproducibility

Pure-Python, zero runtime dependencies (Python ≥ 3.10); GitHub Actions runs the pipeline and the 264-test suite.

```
pip install -e .
python paper/comprehensive_sweep.py            # §3.1 simulation
python paper/threshold_analysis.py             # §3.2 step/cline classification
python paper/classify_functional_groups.py     # §2.2 moderator
python paper/meta_synthesis.py                 # §3.4 synthesis
python paper/validate_meta_inputs.py           # evidence-table integrity
python -m pytest --basetemp=C:/pt              # 264 passing (Windows: short basetemp)
```

## 6. Data availability

Candidate pool, evidence tables, classification, and all scripts are in this repository (`paper/`, `channel_id/`, `data/`). Occurrence/photo proxies are availability evidence only; literature values are source-locked.
