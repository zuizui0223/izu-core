# Supplementary external-system reference matrix

Frozen: 2026-08-24

This table documents the **13 strict external island-system challenges** used in the manuscript. The sources support observed-state assignment only. They were not used to choose ABM parameters, random seeds, state thresholds or mechanisms.

| System | Frozen external state | Primary source(s) | Source-locked boundary |
|---|---|---|---|
| Izu multi-taxon Hiraiwa–Ushimaru | branching | Hiraiwa & Ushimaru 2024, DOI `10.1111/1365-2435.14527`; 2017, DOI `10.1098/rspb.2016.2218` | Cross-study recurrence of response heterogeneity; not same-estimand replication. |
| Ogasawara *Psychotria homalosperma* | same-direction propagation | Watanabe et al. 2018, DOI `10.1111/1442-1984.12183`; Watanabe & Sugawara 2015, DOI `10.1093/aobpla/plv087`; Watanabe et al. 2014, DOI `10.1016/j.flora.2014.09.006` | Physical-access asymmetry and directional pollen transfer; historical replacement is not randomized and numeric signed position is unavailable. |
| Hawaiʻi lobelioids | buffering / resilience | Case et al. 2026, DOI `10.1111/1365-2435.70415`; Case et al. 2026, DOI `10.1002/ece3.74123` | Cross-study propagation boundary; no same-tagged full chain and no empirically identified ABM buffer mechanism. |
| Dominica *Heliconia* | retained falsification | Temeles et al. 2013, DOI `10.1111/jeb.12053`; Martén-Rodríguez et al. 2011, DOI `10.1007/s00442-011-2043-8` | Frozen negative signed-position projection failed; mapping remains unretuned. |
| California Channel Islands *Nicotiana glauca* | buffering / alternative | Schueller 2004, DOI `10.3732/ajb.91.5.672`; Schueller 2007, DOI `10.1007/s10682-006-9125-9` | Higher selfing capacity and morphology differ while a current island service deficit was not detected; establishment filtering remains an alternative. |
| Puerto Rico–Mona *Guaiacum sanctum* | reproductive axes decouple | Fumero-Cabán et al. 2022, DOI `10.26786/1920-7603(2022)669` | Visitor context differs strongly while the self/outcross index remains similar; do not collapse all reproductive axes into a single buffer state. |
| Caribbean Gesneriaceae | branching | Martén-Rodríguez et al. 2015, DOI `10.1111/1365-2745.12457`; Martén-Rodríguez & Fenster 2010, DOI `10.1890/08-2115.1`; Martén-Rodríguez et al. 2010, DOI `10.1111/j.1469-8137.2010.03330.x` | Clade-level cross-study recurrence, not a matched population causal chain; per-visit effectiveness missing. |
| New Zealand *Rhabdothamnus solandri* | same-direction propagation | Anderson et al. 2011, DOI `10.1126/science.1199092` | Bird-functional-loss natural experiment supports propagation to seed and recruitment; not a numerical fit of the ABM trait-position route. |
| Mariana Guam–Saipan | same-direction propagation | Mortensen, Dupont & Olesen 2008, DOI `10.1016/j.biocon.2008.06.014` | Brown-treesnake-associated bird extirpation is a particular natural experiment, not a generic island-isolation mechanism. |
| Seychelles ant disruption | same-direction propagation | Global Ecology and Conservation 2023, DOI `10.1016/j.gecco.2023.e02413` | Within-island ant-context experiment; validates qualitative propagation, not a unique ABM mechanism. |
| Mauritius *Roussea simplex* | same-direction propagation | Hansen & Müller 2009, DOI `10.1111/j.1744-7429.2008.00473.x` | Within-island invasive-ant experiment; not evidence for the ABM trait-position mechanism or a universal ant effect. |
| Canary/Teide honeybee network | branching | Valido, Rodríguez-Rodríguez & Jordano 2019, DOI `10.1038/s41598-019-41271-5` | Common network perturbation produces plant-specific reproductive responses; reproductive axes are not collapsed. |
| Bahamas *Pavonia bahamensis* | same-direction propagation | Rathcke 2000, DOI `10.1890/0012-9658(2000)081[1951:HCRAPL]2.0.CO;2` | Hurricane also caused resource limitation; the strict state uses the source-separated additional pollination-limitation component. |

## State-count contract

- branching: **3** systems;
- same-direction propagation: **6** systems;
- buffering / alternative: **2** systems;
- reproductive-axis decoupling constraint: **1** system;
- retained falsification: **1** system.

Total: **13**.

## Reproducibility paths

The machine-readable version is `data/design/simulation_manuscript_external_system_reference_matrix.json`.

The strict admission contract remains `data/design/system_agnostic_multi_system_validation_gate_v2.json`, and the frozen state readout remains `data/results/system_agnostic_abm_multi_system_validation_v2_frozen.json`.

## Interpretation boundary

The table supports the statement that independent island systems occupy response-state classes represented by the already-frozen model vocabulary. It does **not** support a statement that one empirical mechanism explains all 13 systems, that all 13 are successful validations, or that qualitative state compatibility is a numerical model fit.
