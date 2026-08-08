# Hiraiwa–Ushimaru source-native functional response audit

## Why this dataset matters

The 2024 Hiraiwa & Ushimaru dataset (`10.6084/m9.figshare.25025000.v1`) provides contemporary plant–pollinator network and pollen-receipt data from eight coastal sites:

1. Hitachi;
2. Hitachinaka;
3. Tateyama;
4. Izu Oshima;
5. Niijima;
6. Kozu;
7. Miyake;
8. Hachijo.

The archived data therefore give a direct ecological-function layer spanning a mainland reference, Oshima, and four post-Oshima Izu sites. This is stronger than inferring pollinator dependency from floral form, but it still measures contemporary interactions rather than historical floral evolution.

Repeated seasonal observations are first averaged within `plant × site`. The descriptive focal contrast is then:

```text
mean(post-Oshima Izu sites) - Oshima
```

A plant contributes only when Oshima and at least two post-boundary sites have the relevant metric.

## Two source-defined universes must remain separate

### All network plants

Among every plant in the species-level network table with adequate Oshima/post coverage:

| response | eligible species | lower post | higher post |
|---|---:|---:|---:|
| functional generality | 14 | 6 | 8 |
| corrected trait matching | 16 | 10 | 6 |

Therefore there is **no universal species-level second step** in either interaction breadth or corrected trait matching.

This is an important falsification boundary. The dataset cannot be used to claim that all plants experience the same Oshima-to-post decline.

### Source-defined pollen-success target plants

The original study independently selected 10 dominant, outcrossing, insect-pollinated species for pollen-receipt measurements. Their membership is therefore fixed by the source study, not by the sign of the Oshima/post contrast.

Eight of these species have sufficient Oshima/post coverage for species-level corrected trait matching. All eight have lower post-boundary means:

- *Ampelopsis glandulosa* var. *hancei*;
- *Calystegia soldanella*;
- *Farfugium japonicum*;
- *Glehnia littoralis*;
- *Lysimachia mauritiana*;
- *Melanthera prostrata*;
- *Oxalis corniculata* var. *trichocaulon*;
- *Vitex rotundifolia*.

The same subgroup does **not** show a shared response in the other channels:

| response | eligible species | lower post | higher post |
|---|---:|---:|---:|
| functional generality | 8 | 3 | 5 |
| corrected trait matching | 8 | 8 | 0 |
| pollen receipt | 9 | 5 | 4 |

The coherent result is therefore restricted to corrected trait matching in this independently source-defined functional subset. It must not be generalized to every network plant or turned into a universal fitness decline.

## Campanula: contemporary network function does not repeat the historical breeding step

For *Campanula microdonta* in the contemporary network data:

- functional generality: Oshima `-1.7568`, post mean `-1.2491`, second contrast `+0.5077`;
- corrected trait matching: Oshima `-0.8058`, post mean `-0.2350`, second contrast `+0.5708`.

Both network-derived responses are higher post-boundary than on Oshima. They therefore do **not** mimic the historical source-locked autonomous-reproduction step.

This strengthens the multichannel interpretation: a sharp breeding-system response does not imply that every ecological interaction metric must move in the same direction at the same boundary.

## Farfugium: a useful functional-generalist-style control without a no-effect assumption

For *Farfugium japonicum*:

- functional generality second contrast: `+0.00265` — essentially unchanged in this descriptive site-level contrast;
- corrected trait matching second contrast: `-2.80665`;
- pollen-receipt second contrast: `-0.88773`.

Thus a plant can maintain broad interaction use while experiencing lower functional matching and lower open-pollinated pollen receipt. This is precisely why the generalist negative control should not mean “generalists are unaffected by islands.”

The relevant falsification remains whether specialist-dependent lineages repeatedly show a **shared floral/breeding breakpoint** that is not reproduced in appropriate controls.

## Interpretation boundary

These metrics are not interchangeable:

- functional generality = realized interaction breadth in the sampled network;
- corrected trait matching = network-derived plant–pollinator morphological matching;
- pollen receipt = open-pollinated reproductive-function observation;
- autonomous reproductive capacity = a different experimental breeding-system channel from the historical Campanula literature.

Plant species at a site share the same environmental and network context and therefore are not independent experimental island replicates. The data establish contemporary ecological patterns, not historical selection, floral trait evolution, or causal Bombus loss.

The small source-locked outputs are stored in:

- `data/predictive_meta/hiraiwa_ushimaru_functional_response.csv`;
- `data/predictive_meta/hiraiwa_ushimaru_functional_response_summary.json`.

The raw source files remain reproducibly acquired from Figshare by the dedicated workflow rather than copied into the repository.
