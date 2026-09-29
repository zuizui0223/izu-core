# Chapter 2 NEE reference ledger — 2026-09-15

Status: source-verified bibliography ledger for the active NEE submission surfaces. This ledger does not alter any analysis or route decision.

## Analytical background already used in the manuscript

1. Jost, L. (2006). Entropy and diversity. *Oikos* 113, 363–375. https://doi.org/10.1111/j.2006.0030-1299.14714.x
2. Loreau, M. & de Mazancourt, C. (2008). Species synchrony and its drivers: neutral and nonneutral community dynamics in fluctuating environments. *The American Naturalist* 172, E48–E66. https://doi.org/10.1086/589746
3. de Mazancourt, C. et al. (2013). Predicting ecosystem stability from community composition and biodiversity. *Ecology Letters* 16, 617–625. https://doi.org/10.1111/ele.12088

## Closest prior work for the novelty boundary

4. Schulz, T., Saastamoinen, M. & Vanhatalo, J. (2025). Model-based variance partitioning for statistical ecology. *Ecological Monographs* 95, e1646. https://doi.org/10.1002/ecm.1646

Role in the manuscript: establishes that variance-partition contributions can be estimated within/between ecologically relevant subgroups to study environmental or ecological context dependence. It therefore prevents Chapter 2 from claiming that context dependence of relative importance is itself new.

5. Guilbault, E. et al. (2025). Strong context dependence in the relative importance of climate and habitat on nation-wide macro-moth community changes. *Journal of Animal Ecology* 94, 1948–1961. https://doi.org/10.1111/1365-2656.70107

Role in the manuscript: empirical example showing that relative driver importance can vary across environmental and functional contexts. Chapter 2's novelty must therefore be stated as the transportability/sufficiency question: when does a compressed context retain enough information for a determinant ranking to transport, and what response geometry makes it fail?

## Primary natural-regime sources

### Hawaii

Aslan, C. E., Shiels, A. B., Haines, W. & Liang, C. T. (2019). Non-native insects dominate daytime pollination in a high-elevation Hawaiian dryland ecosystem. *American Journal of Botany* 106, 313–324. https://doi.org/10.1002/ajb2.1233

Dataset: Dryad https://doi.org/10.5061/dryad.tm575v4

### Mallorca

Lázaro, A., Gómez-Martínez, C., González-Estévez, M. A. & Hidalgo, M. (2022). Portfolio effect and asynchrony as drivers of stability in plant–pollinator communities along a gradient of landscape heterogeneity. *Ecography* 2022, e06112. https://doi.org/10.1111/ecog.06112

Dataset: Dryad https://doi.org/10.5061/dryad.m905qfv2p

### Tenerife

Lara-Romero, C., Seguí, J., Pérez-Delgado, A., Nogales, M. & Traveset, A. (2019). Beta diversity and specialization in plant–pollinator networks along an elevational gradient. *Journal of Biogeography* 46, 1598–1610. https://doi.org/10.1111/jbi.13615

Dataset: Dryad https://doi.org/10.5061/dryad.b23v8nn

Bibliographic provenance note: the frozen Tenerife admission JSON contains a transcription typo `10.1111/jbi.13625`. The source config, Wiley article page and Dryad linkage identify the correct DOI as `10.1111/jbi.13615`. The correction is recorded without rewriting the frozen admission object in `data/results/chapter2_tenerife_bibliographic_correction_20260915.json`.

### Cabrera

Serra-Marin, P. E., Solé-Ribalta, A., Lana, A., Borge-Holthoefer, J., Hervías-Parejo, S. & Traveset, A. (2025). Comparative assessment of automated and manual monitoring in comprehensive plant–pollinator communities. *Methods in Ecology and Evolution* 16, 2960–2978. https://doi.org/10.1111/2041-210X.70165

Dataset/source archive: Zenodo https://doi.org/10.5281/zenodo.17130777

### Martinique

Cyrille, N. (2025). Floral offer and seasonality shape plant-pollinator networks in tropical gardens [dataset and analysis code]. dataUBFC. https://doi.org/10.25666/DATAUBFC-2025-03-28

Dataset project members listed in the source record: Nathan Cyrille, Yann Lelièvre, Eddy Dumbardon-Martial, Adam J. Vanbergen, François Bretagnolle & Marie-Jeanne Perrot-Minnot. The deposit states that it supported a manuscript under review at the time of deposition; the primary Chapter 2 natural-regime analysis is locked to the deposited dataset, not to a later publication state.

### England STEP / Great Britain

Holzschuh, A. et al. (2016). Mass-flowering crops dilute pollinator abundance in agricultural landscapes across Europe. *Ecology Letters* 19, 1228–1236. https://doi.org/10.1111/ele.12657

The Chapter 2 source is the UK/England component exposed through the pinned EuPPollNet repository (`31_Roberts`) and its source-native interaction/flower-count files.

### Harmonized European source compilation used for England provenance

Lanuza, J. B. et al. (2025). EuPPollNet: A European database of plant-pollinator networks. *Global Ecology and Biogeography* 34, e70000. https://doi.org/10.1111/geb.70000

Pinned repository for Chapter 2 source audit: `JoseBSL/EuPPollNet`, tag `v1.3.0`.

## Citation boundary

- Cite Schulz et al. and Guilbault et al. when explicitly acknowledging that context dependence of relative importance is prior art.
- State Chapter 2's novelty as a ranking-transportability / sufficiency boundary after context compression, not as discovery of context-dependent driver importance.
- Cite the six primary natural-regime sources for provenance of the 42-system plane.
- Cite EuPPollNet specifically for the harmonized England source and its pre-existing island-study classification.
- The Martinique primary citation remains the dataset DOI unless a later peer-reviewed article is explicitly audited as the same deposited source object.
- Do not use any reference here to imply that the natural sources validate the synthetic `C/I` crossover.
