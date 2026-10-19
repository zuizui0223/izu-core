# Source-disjoint A/I predictability screen: technical pilot readout

**2026-10-19 | MODEL3 TECHNICAL EXPLORATION, not registered ecological confirmation or a generalized island assembly result.**

## Executed outcome and source admission

- [Original successful science-gate technical job](https://github.com/zuizui0223/izu-core/actions/runs/39275688492), `scientific-gate` job `118139546258`, source head **`ae90c48b657d9c5c92b3a2cfd36955e3d99b42c8`**. Its bounded `test_chapter2_two_origins_disjoint_pilot_20261019.py` step completed **success**. Source script: [`chapter2_two_origins_disjoint_source_pilot_20261019.py`](../scripts/chapter2_two_origins_disjoint_source_pilot_20261019.py). This does not assert independent biological code verification.
- **48 new artificial source genotypes**: 24 TRAIN (source seeds 21010000–21010023) and 24 HELDOUT (21020000–21020023). No reuse of the six previously exposed technical source genotypes, which had source seeds 73000–73005. Both sets are independently generated under the same artificial model and the same A/I source-hint design.
- **4 crossed artificial environments**: budgets B4.5 and B8 × visitor states absent and present. **8 demographic/arrival resets** for each source×environment, all nested. There are **768 records per split**, **1,536 technical source×island×reset pathways total**, **not 1,536 independent lineages or islands**.
- **All-start denominator:** Candidate nonarrival, establishment failure after arrival, later extinction, and three survivor-I-response categories are distinguished. Every original source is present in all-start analysis. Source/phenotype means are not assigned fabricated zeros at extinction.
- The source-registered outcomes and settings are **exposed** by this first technical screen. No independent island-class holdout, predeclared biological SESOI or joint power, inferential interval, p-value, field test, population-level self-compatibility measurement, or multispecies competition.

## New-source held-out prediction, from original job log

Brier score is **lower when a forecast is better**. Models fit half-pseudocount-smoothed stratum prevalence from **TRAIN source labels only**, and evaluate wholly disjoint HELDOUT **source identities** in the same four environments. `ecology_only` knows which artificial island environment is used but not the source genotype. `ecology_A`, `ecology_I` and `ecology_A_I` additionally use the corresponding **pre-existing source trait category**, derived from actual starting genotype. They never use source ID or validation outcomes as predictors. Original label binary groups and repeated paths are nested.

| All-start establishment (n=768 held-out paths) | Expected description | Brier | Difference vs ecology-only |
| --- | --- | ---: | ---: |
| Ecology only | Training-estimated environment-specific baseline | **0.218155** | 0 |
| Ecology + source A category | Information from A before simulated arrival | **0.215711** | **−0.002445** |
| Ecology + source I category | Information from I before simulated arrival | 0.218577 | +0.000422 (worse) |
| Ecology + source A and I | Joint source categories | **0.214831** | **−0.003325** |
| **Full source genotype oracle** | Known exact native Model3 conditional probability × arrival probability | **0.211065** | −0.007090; **not fitted** |

| Establishment conditional on being among 604 arrivals | Brier | Difference vs ecology-only |
| --- | ---: | ---: |
| Ecology only | **0.115624** | 0 |
| Ecology + A | **0.109650** | **−0.005974** |
| Ecology + I | 0.115089 | −0.000536 |
| Ecology + A and I | **0.110089** | −0.005535 |
| Full genotype native probability oracle | **0.106194** | −0.009430; not fitted |

| Surviving at update 6 from all original candidate paths (n=768) | Brier | Difference vs ecology-only |
| --- | ---: | ---: |
| Ecology only | **0.224204** | 0 |
| Ecology + A | **0.179435** | **−0.044769** |
| Ecology + I | 0.222697 | −0.001507 |
| Ecology + A and I | **0.176421** | **−0.047783** |

Original log rounded the Brier and differences to six decimal places; the displayed differences may not match subtraction of the displayed scores in the last digit. A-only reduced held-out Brier error **about 20% relative to ecology-only** for this artificial 6-update survival outcome; I-only reduced it about 0.7%. The held-out **log-loss rankings also favored A over I** for survival, as independently printed in the source job (`0.529273` A versus `0.635694` I versus `0.639429` ecological baseline). The full-genotype **oracle** is NOT a fitted out-of-source model; it uses the same native reproductive kernel whose outcomes were generated and is a reference ceiling, not independently validated accuracy.

## What the result does and DOES NOT imply

**Supported in this bounded technical screen:** Source A category materially improves prediction of early *six-year* lineage persistence on source genotypes not used in training. The same source I category yields little improvement for this particular outcome and synthetic distribution. Source A also improves conditional **first-establishment** prediction, although much less than it improves later survival. This is an informative consequence of the existing Model 3 reproductive mechanism under a fully artificial source distribution.

**Not supported:** strong source trait effects do NOT prove deterministic individual lineage fate, that A was historically fixed on the mainland, that island self-compatibility enrichment in Ch1 was created by colonist sorting, or that I is only altered after settlement. The simulation contains no lineage-level cross-species competition or natural colonization record, and it does not isolate a *single direct causal mediation pathway*. The four island environments are **shared** across training and held-out genotypes, so the scores test new-source prediction **conditional on these same island classes**, not extrapolation to unseen island geographies or functional pollinator assemblages. There is no statement about real-field generality or statistical certainty beyond this unpowered technical split.

**Next evidence requirement:** analyze the distinct A/I `arrival+establishment+persistence filter` versus `within-survivor trait change` stage terms with all candidate denominators; then choose a truly independent source- and island-held-out validation and a source-compatible independent community model *before* attempting a high-impact claim. These new studies require their own prospective contract, biological SESOI and resource/variance review, documented in [the admission note](CHAPTER2_TWO_ORIGINS_PREDICTION_ADMISSION_20261019.md). This technical result does not modify the registered G/S outcomes or inconclusive Q2 result in separate [PR #609](https://github.com/zuizui0223/izu-core/pull/609).
