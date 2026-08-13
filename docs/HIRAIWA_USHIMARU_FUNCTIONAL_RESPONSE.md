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

The archived data therefore give a direct ecological-function layer spanning a mainland reference, Oshima, and four post-Oshima Izu sites. This is stronger than inferring pollinator interactions from floral form, but it still measures contemporary interactions rather than historical floral evolution.

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

The original study independently selected 10 dominant, nectar-producing, outcrossing insect-pollinated species for pollen-receipt measurements. Their membership is therefore fixed by the source study, not by the sign of the Oshima/post contrast.

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

## Leave-one-post-island sensitivity

The 8/8 trait-matching direction is not simply caused by one extreme southern island, but it is also not perfectly invariant to every post-island omission:

| contrast | eligible | lower post | higher post |
|---|---:|---:|---:|
| full post set | 8 | 8 | 0 |
| omit Niijima | 7 | 7 | 0 |
| omit Kozu | 7 | 7 | 0 |
| omit Miyake | 8 | 6 | 2 |
| omit Hachijo | 8 | 7 | 1 |

When Miyake is omitted, *Lysimachia mauritiana* and *Melanthera prostrata* reverse direction; when Hachijo is omitted, *M. prostrata* reverses direction. The subgroup pattern is therefore **robust to removing Niijima or Kozu and mostly robust overall, but not uniformly leave-one-island-out invariant**.

No species-independent sign-test p-value is used because the plants share the same site environments and network context.

## Campanula: contemporary network function does not repeat the historical breeding step

For *Campanula microdonta* in the contemporary network data:

- functional generality: Oshima `-1.7568`, post mean `-1.2491`, second contrast `+0.5077`;
- corrected trait matching: Oshima `-0.8058`, post mean `-0.2350`, second contrast `+0.5708`.

Both network-derived responses are higher post-boundary than on Oshima. They therefore do **not** mimic the historical source-locked autonomous-reproduction step.

This strengthens the multichannel interpretation: a sharp breeding-system response does not imply that every ecological interaction metric must move in the same direction at the same boundary.

## Farfugium: prospectively locked high-interaction-breadth control

Within the source-defined 10-species pollen-success universe, *Farfugium japonicum* has the highest mean observed `FG_Pla_sp_z` among species passing a prospective coverage rule of at least six of eight sites and at least five functional-generality observations:

- mean functional generality z = `1.67454`;
- functional-generality rows = `8`;
- sites represented = `8`;
- rank among coverage-eligible species = `1`.

The control-selection rule uses only source-defined target membership, functional generality and coverage. It does **not** use corrected trait matching, pollen receipt, floral morphology response or breeding-system response. *Farfugium* is therefore locked prospectively as a high-interaction-breadth control candidate for future phenotype/breeding tests.

This does not make it an effectiveness-defined “generalist” by itself. Realized network breadth and effective pollinator dependency remain distinct concepts.

For the current ecological channels:

- functional generality second contrast: `+0.00265` — essentially unchanged descriptively;
- corrected trait matching second contrast: `-2.80665`;
- pollen-receipt second contrast: `-0.88773`.

Thus a plant can maintain broad interaction use while experiencing lower functional matching and lower open-pollinated pollen receipt. This is precisely why the negative control should not mean “generalists are unaffected by islands.”

The relevant falsification remains whether specialist-dependent lineages repeatedly show a **shared floral/breeding breakpoint** that is not reproduced in appropriate controls.

## Link to the published mechanism

The source study itself reports that lower pollinator functional diversity—especially lower abundance of long-tongued pollinators—reduces plant functional specialization and flower–pollinator trait matching, and that lower community trait matching is associated with lower community pollination success. The present Oshima/post summaries are therefore interpreted as a descriptive geographic projection of a source-tested functional mechanism, not as a replacement for the original GLMMs.

## Interpretation boundary

These metrics are not interchangeable:

- functional generality = realized interaction breadth in the sampled network;
- corrected trait matching = network-derived plant–pollinator morphological matching;
- pollen receipt = open-pollinated reproductive-function observation;
- autonomous reproductive capacity = a different experimental breeding-system channel from the historical Campanula literature.

Plant species at a site share the same environmental and network context and therefore are not independent experimental island replicates. The data establish contemporary ecological patterns, not historical selection, floral trait evolution, or causal Bombus loss.

The small source-locked outputs are stored in:

- `data/predictive_meta/hiraiwa_ushimaru_functional_response.csv`;
- `data/predictive_meta/hiraiwa_ushimaru_functional_response_summary.json`;
- `data/predictive_meta/hiraiwa_ushimaru_trait_matching_sensitivity.json`;
- `data/predictive_meta/prospective_functional_control.csv`.

The raw source files remain reproducibly acquired from Figshare by the dedicated workflow rather than copied into the repository.
