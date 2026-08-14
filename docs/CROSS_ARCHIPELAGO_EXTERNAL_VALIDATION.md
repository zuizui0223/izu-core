# Cross-archipelago external validation

External archipelagos test recurrence, heterogeneity, and mechanism boundaries around the Izu anchor. They do **not** form exchangeable rows in a universal island-effect model, and they do not retroactively identify historical *Bombus* causation in Izu.

The machine-readable sources of truth are:

- `data/results/cross_archipelago_effect_registry.csv`
- `data/results/cross_archipelago_effect_registry_summary.json`
- `data/results/cross_archipelago_morphology_response_shape_summary.json`
- `data/design/external_bridge_system_registry_summary.json`
- `data/design/active_development_mainline.json`

This document is intentionally concise so the narrative does not drift away from those checked states.

## Current admission state

The effect registry currently contains:

```text
total rows                         = 17
empirical numeric rows             = 16
numeric rows with uncertainty      = 9
cross-system model-eligible rows   = 4
eligible independent systems       = 2
compatible effect families in >=2 independent systems = 0
formal cross-system fit ready      = false
```

The four eligible rows come from the Wanshan–Yongxing paired system and the Southwest Pacific morphology source. Ogasawara contributes numeric context effects. These rows use different exposures, responses, and independent units, so model eligibility at the row level does not make them poolable.

Plant-, event-, or bootstrap-level uncertainty never creates additional independent island transitions or archipelagos.

## Source-native network/context systems

### Wanshan–Yongxing

Wang et al. (2025; article DOI `10.1111/btp.70027`, data DOI `10.5061/dryad.t76hdr8bj`) provide whole-community and matched-seven-plant visitation matrices.

The retained result is a strong visitation decline accompanied by very high partner turnover, while the pollinator-richness contrast is much less decisive. This is evidence of ecological rewiring / partner replacement in one island pair, not a causal estimate of geological origin, FDQ, single-visit effectiveness, or reproductive dependency.

Checked outputs are in `data/results/wanshan_yongxing/`.

### Ogasawara

The checksum-locked 2026 CC BY dataset (`10.5281/zenodo.19221853`) supports source-native interaction and invasion-context contrasts. The retained Anijima result is substantial partner turnover / rewiring under spatially structured invasion contexts, while interaction-count and richness intervals are less decisive.

This is context evidence, not a randomized invasion effect and not direct pollen-deposition or dependency evidence.

Checked outputs are in `data/results/ogasawara/`.

### Galápagos

The published-summary layer remains usable, but the raw plant-network archive is still transport/indexing blocked. Source-published island summaries can support descriptive context; plant-level network reconstruction and turnover analysis remain closed until the raw archive is recovered.

A blocked transport route is not a biological zero.

Checked state is in `data/results/galapagos/`.

### Canary–Balearic

Same-community derivative data were recovered from an open PLOS/PMC route after the original Oxford supplementary route remained blocked. Selected seasonal derivative profiles did not survive the declared multiple-testing correction and remain outside the formal cross-system effect registry.

Checked outputs are in `data/results/canary_balearic/`.

## Morphology response-shape recurrence

Two independent source-native morphology systems currently show the same **OLS directional response shape** when written as

```text
slope(log island floral trait ~ log mainland floral trait)
isometry = 1
```

| system | trait | n pairs | island groups | OLS slope | island-cluster interval |
|---|---|---:|---:|---:|---:|
| Southwest Pacific animal-pollinated pairs | source-defined flower size | 88 | 10 | `0.84901` | `[0.69164, 0.92580]` |
| Hendriks 2019 | flower area | 35 | 9 | `0.58334` | `[0.21279, 0.77849]` |

Both OLS island-cluster intervals are below isometry. This is a real **2/2 independent-system directional recurrence of a compression-like response shape** under the declared analysis.

It is not a pooled coefficient.

### Hendriks provenance is complete

The exact lawful VUW institutional PDF (`10.26686/wgtn.17136800`, versioned `10.26686/wgtn.17136800.v1`) has been recovered and checksum locked:

```text
SHA-256 = 4abbe2b1c4b7b1a809df0127e66184385425919a45043260cd2c51a45df37c42
```

All 35 Appendix B Table B9 flower-area pairs and all 35 Appendix-A island assignments have been strictly reverified against those bytes. The mapped island-frequency vector reproduces Table A14. The Hendriks provenance gate is therefore **complete**.

That provenance repair does not solve the remaining statistical boundary: mainland-trait reliability is still not empirically identified, and the Hendriks island-cluster SMA interval `[0.72967, 1.07310]` includes isometry.

### Measurement-error boundary

For Southwest Pacific, the observed animal OLS response-shape point remains below isometry under the declared classical x-error correction only above its required mainland-trait reliability threshold, and retaining the full island-cluster interval below isometry requires reliability above approximately `0.9258`. That reliability is not empirically estimated from the source.

For Hendriks, source provenance is now locked, but measurement reliability remains unidentified and the symmetric-axis sensitivity includes isometry.

Therefore:

```text
source provenance jointly locked      = true
errors in variables jointly resolved  = false
trait definitions identical           = false
formal same-family meta-analysis ready = false
```

Use the morphology result as directional recurrence only. Do not infer a universal island coefficient, pollinator causation, effective-dependency causation, or geological-origin causation.

## External mechanism bridges

The separate mechanism-bridge registry currently contains three independent partial systems:

| system | current bridge state | main missing link |
|---|---|---|
| California Channel Islands, *Nicotiana glauca* | partial | cross-year / cross-paper linkage prevents one matched transition unit |
| Caribbean Gesneriaceae | partial | no matched direct per-visit pollen function |
| Xisha *Cordia subcordata* two-island system | near-complete within archipelago | Dong-side direct effectiveness and controlled dependency are missing |

Counts:

```text
independent partial-or-stronger systems = 3
near-complete within-archipelago systems = 1
complete systems                         = 0
formal cross-system mechanism fit ready  = false
```

The current best bridge is the Xisha *Cordia subcordata* system. Closing the Dong-side direct single-visit effectiveness and controlled reproductive-dependency gap has more decision value than adding another weak descriptive island example.

Partial mechanistic recurrence strengthens plausibility and exposes alternative mechanisms. It cannot substitute for the direct Issue #91 Izu field measurements.

## Historical replication simulation

A fixed-seed simulation previously explored how the number of independent archipelagos affects interval behaviour under between-system heterogeneity. It supported the design lesson that independent system clusters matter more than raw island count for external validity.

That synthetic implementation/result surface has been retired from the active tree. The lesson is preserved in `docs/RESEARCH_TRIALS_RETROSPECTIVE.md`; it is not empirical support and is not a field sample-size prescription.

## Current synthesis

The external layer currently supports four bounded conclusions:

1. **Interaction change can be dominated by partner turnover rather than uniform richness loss.** Wanshan–Yongxing and Ogasawara provide independent context examples.
2. **A compression-like morphology response direction recurs in two independent systems under source-native OLS + island-cluster analysis.** Both source artifacts are now provenance locked.
3. **The morphology recurrence is not yet an errors-in-variables-resolved universal effect.** Reliability is unmeasured, Hendriks SMA uncertainty includes isometry, and the trait definitions are not identical.
4. **Mechanism bridges are partial, not complete.** Three independent systems provide pieces of the functional-exposure / pollen-function / reproductive-dependency chain, with Xisha *Cordia* currently nearest to a matched within-archipelago bridge.

## Claim boundary and next gate

External systems may establish recurrence, rewiring, source-native morphology response shapes, or partial mechanism links. They do not establish:

- a universal mainland-distance effect;
- a universal oceanic-island coefficient;
- a causal pollination-mode effect;
- historical *Bombus* causation in Izu;
- effective dependency inferred from visitor identity, syndrome, occurrence, or morphology; or
- a formal cross-system causal model.

Formal cross-system fitting stays closed until a compatible estimand family with source-locked uncertainty exists in at least two independent system clusters and the relevant measurement-error/admission gates are satisfied.

The active empirical mainline remains Issue #91: direct matched Izu measurements of effective service and reproductive dependency. In parallel, close the strongest external bridge only when a new source or measurement supplies the missing causal link.
