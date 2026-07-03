# Can pollinator-loss-driven floral shifts generalise across an island flora? A source-graded, multi-species test design for the Izu gradient

**Draft manuscript. Version 0.5 (2026-07-03). Evidence-graded comparative design (public data + simulation).**

*Campanula microdonta* is the fully measured calibration system. The study's contribution at this stage is a reproducible, falsifiable multi-species test and a source-graded evidence map—not a completed cross-lineage meta-analysis.

---

## Abstract

Island flowers are often described as smaller, less showy and more selfing than mainland relatives, usually as a response to reduced pollinator service. That explanation is difficult to test in a single species because floral traits, environment, colonisation history and pollinator assemblages change together. We develop a source-graded framework for testing whether a shared, distance-structured pollinator-regime transition across the Izu archipelago predicts parallel floral responses among co-distributed plant taxa.

From a GBIF-derived pilot cohort of 156 insect-pollinated angiosperms occurring on the mainland plus at least two Izu islands, we define a protected comparison set: specialist candidates, generalist negative controls, large-flower counter-direction candidates and non-bee specificity controls. Evidence is separated into direct geographic comparisons, source-recovery targets whose taxonomic or sampling scope requires verification, and comparative context that must not be pooled as a within-species island effect. Literature, blinded photo evidence and occurrence records are never treated as interchangeable.

The source-locked calibration series for *Campanula microdonta* shows corolla reduction from mainland to Hachijō (lnRR = −0.77; −54%) and an autonomous-selfing shift at the Ōshima→Toshima bumblebee-loss boundary. Published reports for *Ligustrum*, *Chionographis*, Sakuyuri lily and *Clerodendrum* are retained as source-recovery or comparative-context leads rather than counted as independent geographic replicates until their primary tables, taxonomic scope and sampling units are checked. Current evidence therefore establishes a strong focal system and a transparent test design, while the cross-lineage conclusion remains explicitly pending.

---

## 1. Introduction

The reproductive "island syndrome"—smaller or less conspicuous flowers and increased autonomous reproduction—has frequently been attributed to reproductive assurance under pollinator limitation. A single mainland-to-island cline, however, cannot distinguish pollinator effects from environment, drift, founding history or phenotypic plasticity.

The Izu archipelago offers a potentially powerful test because co-distributed plants experience overlapping geographic structure. A general explanation predicts that taxa dependent on large-bodied or long-tongued bee service should respond differently from accessible, broadly visited flowers and from systems whose effective visitors lie outside the bumblebee regime. The relevant result is not a generic mean change: it is an interaction between response and independently supported functional group, ideally with a shared change-point at a documented regime boundary.

This study therefore asks a constrained question: **after direct comparison scope and pollination functional group have been independently verified, do Izu taxa show a shared, functionally structured geographic floral response?** We first construct the evidence architecture required to answer it without turning occurrence records, photographs or taxonomic comparisons into interchangeable pseudo-replicates.

### 1.1 Contributions

1. A source-graded, multi-species design for an Izu floral-response meta-analysis, with direct effects, ordinal evidence and discovery leads kept separate.
2. A GBIF-derived pilot cohort of 156 gradient-spanning entomophilous angiosperms nested within a reported 319-species mainland + ≥2-island parent universe.
3. Protected specialist, generalist, large-flower and non-bee comparison strata that prevent literature availability from preselecting the result.
4. An explicit distinction between `primary_geographic`, `pending_scope_check` and `comparative_context` observations.
5. A calibration analysis for *Campanula microdonta* and a simulation-based statement of what additional channels are required for causal discrimination.

---

## 2. Materials and methods

### 2.1 Geographic candidate universe

The Izu chain comprises a mainland reference plus Ōshima, Toshima, Niijima, Kōzushima, Miyake and Hachijō. A GBIF island-facet probe reported 319 vascular plant species on the mainland plus at least two islands, 289 on at least three islands and 113 on at least five islands. The present 156-species insect-pollinated table is a pilot analysis cohort, not the upper limit of systematic literature screening.

### 2.2 Protected functional-group comparison

The first-pass functional classification is a transparent search-prioritisation device, not evidence of pollinator dependence. The initial 40-species screening docket reserves 30% specialist candidates, 40% generalist negative controls, 20% large-flower counter-direction candidates and 10% non-bee or ambiguous systems. Every species enters the U6 mechanism subset only after taxon-specific pollination evidence is recorded with geographic scope, visitor guild, accessibility traits and source page/table/figure.

### 2.3 Evidence roles and tiers

Each source observation receives both an evidence rank and a synthesis role.

- **Primary geographic evidence** is a direct, source-checked mainland–island or ordered-island comparison with compatible taxonomic and sampling units. It is eligible for the main direction synthesis and, when numeric, a future random-effects meta-analysis.
- **Pending-scope evidence** is a promising peer-reviewed report whose original comparison units, taxonomic rank, locality mapping or sample sizes have not yet been transcribed. It remains outside the primary synthesis.
- **Comparative context** includes interspecific or form-level comparisons and Web/flora statements. These guide hypotheses and source recovery but are never counted as independent within-species island effects.

Evidence ranks remain: A = peer-reviewed quantitative, B = peer-reviewed qualitative, C = blinded photo score, D = Web/flora description, E = occurrence-only. The rank expresses source/measurement quality; the synthesis role expresses comparison eligibility. Neither substitutes for the other.

### 2.4 Response shape and planned synthesis

For taxa with at least four verified ordered geographic positions, the workflow compares none, smooth cline and step models using AICc. A shared step at a documented pollinator-regime boundary is a planned test, not an assumption. The current `meta_synthesis.py` reports the *Campanula* quantitative anchor and an evidence-role-aware direction summary; it does not produce a variance-weighted meta-analysis until multiple independent effects exist.

---

## 3. Results

### 3.1 Calibration: a direct *Campanula* geographic series

*Campanula microdonta* corolla length declines from 49.9 mm on the mainland to 23.1 mm on Hachijō (lnRR = −0.77; −54%). Its autonomous-selfing measure shifts from 11% to 100% at the Ōshima→Toshima boundary in the source-locked series. This is the current quantitative calibration system; it demonstrates a pattern that a broader analysis must test rather than presuppose.

### 3.2 Current evidence inventory

The current table contains direct geographic *Campanula* observations, five source-recovery targets and three comparative-context observations. *Ligustrum ovalifolium* and *Chionographis japonica* are promising published leads, but their geographic units, taxonomic scope and extractable values have not yet been validated against full text. The Sakuyuri lily and *Clerodendrum izuinsulare* comparisons are retained as evolutionary context rather than being pooled as direct within-species island effects. The Ōshima azalea record is a Web/flora lead requiring an original measurement and taxonomic source.

### 3.3 No cross-lineage primary estimate yet

Under the direct-geographic eligibility rule, the present dataset does not yet support a cross-lineage pooled estimate or a specialist-versus-generalist moderator test. Generalist negative controls have no retained trait observations, and large-flower counter-direction cases are not yet primary geographic effects. This is a result about the state of evidence, not evidence that generalists are invariant.

---

## 4. Discussion

The present work supports a narrower but stronger claim than a completed Izu-flora meta-analysis: the *Campanula* series provides a well-specified calibration system, and the archipelago supports a falsifiable comparative design. The crucial next test is whether independently verified specialist taxa share a response that generalist negative controls do not, after environmental and taxonomic alternatives are handled explicitly.

The principal risk in public-data synthesis is not merely missing data. It is a false increase in replication when interspecific comparisons, island forms, pictures, distributions and direct population series are pooled under one label. The evidence-role layer prevents this. In particular, a named island taxon may be biologically informative for divergence and speciation, but it cannot be treated automatically as a mainland-to-island within-species effect.

The next empirical targets are: (1) recover original tables and locality/sample information for the five high-priority B-rank sources; (2) reconstruct the full 319-species U0 parent universe and search it systematically in Japanese and English; (3) validate functional groups at taxon level; (4) audit generalist photo availability and phenology across sources; and (5) collect targeted field and paternity/visitor data where public evidence cannot identify mechanism. A future publication can be either a quantitative meta-analysis or, if numeric recovery remains sparse, a systematic evidence map with predeclared exploratory ordinal analyses. The final format follows the evidence recovered, not the initial preferred headline.

---

## 5. Reproducibility

Pure-Python, zero runtime dependencies (Python ≥ 3.10). The repository contains the calibration analysis, evidence-role-aware synthesis, candidate dockets and source-discovery workflows.

```bash
pip install -e .
python paper/comprehensive_sweep.py
python paper/threshold_analysis.py
python paper/classify_functional_groups.py
python paper/meta_synthesis.py
python paper/validate_meta_inputs.py
python -m pytest --basetemp=C:/pt
```

## 6. Data availability

Candidate tables, source-graded evidence records, screening dockets and analysis scripts are in this repository. Public occurrence and photo records are candidate availability evidence until reviewed; literature values enter the main analysis only after source-locked transcription.
