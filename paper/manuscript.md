# A comprehensive simulation-and-meta-analysis framework for detecting pollinator-loss-driven mating-system evolution on island gradients

**Draft manuscript. Version 0.3 (2026-07-03). Methods + synthesis (simulation & meta-analysis).**
Author: zuizui0223. The simulation, meta-analysis, and data-collection methods are generalised and improved from a channel-identification workflow originally built for *Campanula microdonta* on the Izu Islands, which enters here only as a single calibration seed. All numbers are reproducible from this repository (see *Reproducibility*).

---

## Abstract

Islands repeatedly show a "reproductive syndrome" — increased selfing and reduced floral display — widely attributed to the loss of effective pollinators. Testing that attribution from any single species is underdetermined: floral traits, pollinator service, establishment, and geographic position all covary along the same gradient. We address the problem at two levels that a single case study cannot: **comprehensively by simulation** (mapping when the signature is detectable across the phenomenon's parameter space) and **cumulatively by meta-analysis** (deriving how much cross-taxon evidence a decisive test needs). The simulation, meta-analytic-eligibility, and data-collection methods are adapted and improved from a channel-identification workflow developed for one island bellflower system.

A comprehensive sweep (90 parameter cells; 300 replicates each) yields a sharp, general result. An analysis that **calibrates the environmental background** recovers the true pollinator-loss mechanism in 95–99% of replicates across the *entire* space — every depth of pollinator loss and island count tested. The identical analysis that **ignores the background** (attributing all island differences to floral traits) succeeds only when there is no pollinator loss; its recovery collapses to ~10% once service drops by 0.20 and to **0%** (100% empty compatible set) once it drops by ≥0.40. The failure scales with the depth of loss — so exactly the systems where the island syndrome is most pronounced are where naive analysis is guaranteed to mis-identify the mechanism. Design analysis further shows that visitation data alone are insufficient (0% unique recovery; 95% false-mechanism survival), that a single interaction-level channel — effective stigma pollen deposition — restores it (91%), and that usable discrimination needs ~90 plant-units per island. From these we derive concrete meta-analytic replication targets and an improved eligibility screen.

We contribute (i) a reusable, comprehensively-validated simulation for the pollinator-loss/mating-system phenomenon, (ii) simulation-derived design and meta-analysis requirements (which channel, how many individuals, islands, and independent lineages), and (iii) an improved data-collection and screening workflow. A worked calibration seed (Izu *C. microdonta*: outcrossing–isolation ρ = −0.96, corolla–isolation ρ = −1.00, autonomous selfing stepping up exactly at the bumblebee-loss boundary) anchors the simulation to a real gradient without being the object of the claim.

---

## 1. Introduction

The shift from outcrossing to selfing is among the most common transitions in flowering plants and is conspicuous on islands, where reduced, less showy flowers and autonomous self-pollination recur. The standard explanation is **reproductive assurance** under pollinator scarcity. Island archipelagos with a distance-structured loss of large-bodied pollinators — the Izu Islands, where bumblebees (*Bombus*) thin out southward, are a clean example — look like natural experiments for this hypothesis.

The difficulty is inferential, and it does not go away with more careful fieldwork on one species. Along a single geographic axis, reproduction, pollinator regime, establishment probability, environment, and colonisation history are confounded; a trait cline is compatible with all of them. Two things are therefore needed that a single case study structurally cannot provide:

1. **Comprehensive simulation** — to establish *where* in the phenomenon's parameter space the pollinator-loss signature is even recoverable, and how badly naive analysis fails, rather than reporting one benchmark point.
2. **Meta-analysis** — to convert repeated mainland→island transitions across lineages into a cumulative test, which requires knowing in advance how many taxa, islands, and individuals, measured on which channel, are enough.

This paper builds both, and does so by **generalising and improving a workflow** first developed for a single system (*Campanula microdonta*, Izu). That workflow contributed a constrained life-history simulator, a scenario-recovery/design-power layer, a taxon-eligibility screen, and a public-data collection pipeline; we reuse its architecture, extend it from one benchmark to a full sweep, and upgrade its data-collection and eligibility rules. The single system is retained only as a calibration seed (§6).

---

## 2. The workflow we generalise, and what we improve

| Component (seed workflow) | Role | Improvement in this paper |
|---|---|---|
| Constrained life-history simulation (`life_history`, `guide_scenarios`) | retain the parameter set compatible with all declared observations under a declared `W(z)=F(z)·E(z)` life cycle | run it comprehensively over a parameter grid (§3), not at one point |
| Scenario recovery / design power (`operating_characteristics`, `guide_design_power`) | ask whether a plan recovers a known virtual mechanism, vs sample size & noise | extend to a channel × sample-size × island-count × loss-depth grid; derive meta-analytic replication targets (§4) |
| Gradient benchmark (`izu_gradient_benchmark`) | calibrated vs flat-environment recovery on one island scaffold | sweep loss depth, environmental confound, and island number; quantify how failure scales with loss (§3) |
| Taxon eligibility screen (`izu_comparative_taxon_screen`) | four gates: taxonomy, mainland reference, ≥2 island populations, compatible protocol | add quantitative effect-size and phylogenetic/shared-island-dependence gates for a real meta-analysis (§4, §5) |
| Public-data collection (GBIF / iNaturalist fetchers; source-locked literature; blinded trait review) | availability evidence and trait proxies kept separate from quantitative claims | formalise as a PRISMA-style, provenance-locked collection protocol usable across taxa (§5) |

All components are pure-Python, dependency-free, and unit-tested (257 tests passing).

---

## 3. Result 1 — A comprehensive detectability map

We simulate an ordinal island gradient with a known true mechanism (`visit_attraction + assurance`, i.e. pollinator-dependent outcrossing plus selfing assurance) and sweep four controls: **pollinator-loss depth** (drop in service from the mainland-proximate to the isolated end), **environmental confound** (establishment multiplier at the isolated end), **island number** (2/4/8), and **analysis mode** (calibrated vs flat). Each of 90 cells uses 300 replicates. Recovery is invariant to the establishment confound over the tested range, so we tabulate unique-truth recovery by loss depth × island number:

| Pollinator-loss depth | Islands | CALIBRATED recovery | FLAT (naive) recovery |
|---:|---:|---:|---:|
| 0.00 (no loss) | 2 / 4 / 8 | 0.97 / 0.99 / 0.99 | 0.97 / 0.99 / 0.99 |
| 0.20 | 2 / 4 / 8 | 0.97 / 0.98 / 0.99 | **0.10 / 0.15 / 0.13** |
| 0.40 | 2 / 4 / 8 | 0.98 / 0.99 / 0.98 | **0.00 / 0.00 / 0.00** |
| 0.60 | 2 / 4 / 8 | 0.96 / 0.97 / 0.99 | **0.00 / 0.00 / 0.00** |
| 0.75 | 2 / 4 / 8 | 0.95 / 0.97 / 0.98 | **0.00 / 0.00 / 0.00** |

Two general conclusions follow. First, **environmental calibration is sufficient across the whole space**: knowing the per-island background restores 95–99% recovery regardless of how deep the pollinator loss is. Second, **naive analysis fails in proportion to the signal it is meant to explain**: with no pollinator loss it is fine, but its recovery collapses to ~10% at a modest loss (0.20) and to exactly 0% — rejecting every candidate — once loss reaches 0.40. The systems most likely to show a strong island syndrome (deep pollinator loss on the far islands) are precisely those where an uncalibrated gradient comparison is guaranteed to mis-identify or over-reject. Adding islands modestly improves calibrated recovery but does **not** rescue the naive analysis.

*Reproduce:* `python paper/comprehensive_sweep.py`

## 4. Result 2 — From design power to meta-analytic requirements

Holding the true mechanism fixed, we ask what a plan must measure and at what scale.

**Which channel.** Visitation data alone — the most commonly reported observation — fail: unique-truth recovery 0.000 with a false mechanism surviving 95% of the time. Adding one interaction-level channel collapses the ambiguity: legitimate-contact fraction → 0.902, effective stigma pollen deposition → 0.908 (zero false survivors).

| Plan | Unique recovery | False survivors |
|---|---:|---:|
| visits only | 0.000 | 0.946 |
| + legitimate-contact fraction | 0.902 | 0.001 |
| + effective pollen deposition | 0.908 | 0.000 |

**How many individuals.** For the leading channel, discrimination becomes usable near n ≈ 90 plant-units per island (unique recovery 0.12 → 0.31 → 0.73 at n = 10 / 30 / 90).

**How many islands / lineages.** Result 1 shows 2 islands already give high per-taxon recovery *when calibrated*; the binding constraint for a cross-taxon claim is therefore not islands-per-taxon but **independent lineages**. A meta-analysis of pollinator-loss-driven selfing needs several genuinely independent mainland→island lineages, each cleared for comparable effect sizes and for shared-island/phylogenetic dependence. Translating these into a pre-registration: measure an interaction-level channel (not visits), calibrate per-island environment, target n ≈ 90 per island, ≥2 islands per lineage, and ≥3 independent lineages before pooling.

*Reproduce:* `python examples/handling_deposition_design_power.py`, `python examples/guide_design_power_sweep.py`

## 5. An improved, provenance-locked data-collection and eligibility workflow

Generalising the seed workflow's collection rules into a cross-taxon protocol:

1. **Availability vs measurement separation.** GBIF/iNaturalist occurrences and photographs are collected as *availability* and *lead* evidence only; they never become quantitative trait values or presence/absence of pollination. (Implemented: `fetch_gbif_occurrences`, `fetch_izu_inaturalist_snapshots`, blinded photo review.)
2. **Source-locked transcription.** Published reproductive/floral values are transcribed into a source-locked table with per-value provenance, frozen as a pre-field baseline.
3. **Four-gate eligibility (retained):** accepted taxonomy; traceable mainland reference; ≥2 verified island populations; compatible measurement protocol.
4. **Two new gates (improvement):** a *quantitative effect-size gate* (a lineage enters the pooled analysis only with a comparable, extractable effect size and its uncertainty) and a *dependence gate* (declared model terms for phylogenetic non-independence and shared-island effects). These convert the screen from a readiness checklist into a meta-analysis admission rule.
5. **PRISMA-style accounting.** Report candidates identified, screened, excluded (with reason), and admitted, so the synthesis is auditable.

Applied now, the screen admits one focal lineage (*C. microdonta*) and lists candidate lineages (e.g. *Dianthus japonicus*, *Farfugium japonicum*) as discovery-only pending distribution and taxonomic verification — i.e. the meta-analysis is not yet startable, and the protocol says so explicitly rather than pooling prematurely.

## 6. Calibration seed: the Izu *Campanula microdonta* gradient

To keep the simulation anchored to a real system, we calibrate against compiled island-level data for one bellflower (mainland Honshu + six Izu islands; Inoue series, source-locked). This system is a *seed*, not the object of the claim.

- **Pollinator regime:** bumblebees only at the two mainland-proximate sites (*B. diversus* mainland, *B. ardens* Ōshima); halictids ubiquitous; a sharp loss boundary at Ōshima→Toshima.
- **Reproductive shift:** autonomous selfing (bagged capsule set) steps from 5.5%/11.3% (bumblebee sites) to 90–100% (bumblebee-free) — a threshold at the loss boundary; realised outcrossing declines monotonically with isolation rank (Spearman ρ = −0.96).
- **Floral reduction:** corolla length contracts monotonically (ρ = −1.00; 49.9 → 23.1 mm, n = 5).
- **Weak climate covariation:** temperature ρ = +0.49, precipitation ρ = +0.64 (non-monotonic) — a poor alternative to pollinator loss.
- **Mechanistic ordering:** among competing island scenarios, bumblebee "bridge loss" ranks first (log-marginal compatibility −48.5) over small-bee substitution, body-size-only, and environment-only.

These real values fall in the deep-loss / strong-signal region of the Result 1 map — the region where §3 shows calibration is essential and naive analysis fails — confirming the simulation is anchored to a realistic operating point.

*Reproduce:* `python scripts/run_island_multichannel_analysis.py --input data/inoue_literature_island_traits.csv --output-json out/mc.json --output-md out/mc.md`

## 7. Limitations

The simulation is a declared model of the phenomenon, not a universal law; recovery rates are conditional on the life cycle, parameter ranges, and interval calibration. The calibration seed is compiled historical, correlational data (n = 7 populations; corolla n = 5); isolation rank is a proxy correlated with distance and history. The meta-analysis is a *design*, not yet an execution: only one lineage is eligible. Compatibility orderings are prior-Monte-Carlo rankings, not posterior probabilities.

## 8. Reproducibility

Pure-Python, zero runtime dependencies (Python ≥ 3.10).

```
pip install -e .
python paper/comprehensive_sweep.py                 # Result 1 (90-cell sweep)
python examples/handling_deposition_design_power.py  # Result 2 (channel)
python examples/guide_design_power_sweep.py          # Result 2 (sample size)
python scripts/run_island_multichannel_analysis.py --input data/inoue_literature_island_traits.csv \
    --output-json out/mc.json --output-md out/mc.md  # calibration seed (§6)
# Windows: run pytest with a short basetemp to avoid MAX_PATH / %TEMP% ACL issues
python -m pytest --basetemp=C:/pt                    # 257 passing
```

## 9. Data availability

All simulation code, the compiled source-locked calibration table (`data/inoue_literature_island_traits.csv`), and the collection/eligibility scripts are in this repository. Occurrence and photographic proxies are retained as availability evidence only.
