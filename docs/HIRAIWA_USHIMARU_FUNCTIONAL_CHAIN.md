# Contemporary pollinator-functional chain in the Hiraiwa–Ushimaru source data

## Purpose

This note separates three statements that must not be collapsed:

1. pollinator functional diversity (`FDQ`) is associated with community corrected trait matching (`TM_z`);
2. trait matching is associated with open-pollinated pollen receipt;
3. neither association by itself identifies a historical cause of floral or breeding-system evolution.

All raw data are reproducibly acquired from Figshare source `10.6084/m9.figshare.25025000.v1`.

## 1. FDQ → corrected trait matching is the robust upstream link

The archived source Figure-3 community model gives an FDQ coefficient of `+1.5540`.

A transparent sensitivity model,

`TM_z ~ FDQ + FEve + site fixed effects + season fixed effects`,

returns:

| subset | rows | FDQ coefficient | site-centered FDQ–TM correlation |
|---|---:|---:|---:|
| all 8 sites | 40 | `+1.8346` | `+0.3025` |
| mainland 3 sites | 15 | `+1.5414` | `+0.1810` |
| Izu 5 islands | 25 | `+1.9426` | `+0.4034` |
| post-Oshima 4 islands | 20 | `+2.0590` | `+0.3410` |

The post-Oshima model uses only Niijima, Kozu, Miyake and Hachijo. The sampled pollinator-species table contains no Bombus rows in these four island networks, so the positive FDQ relationship inside this subset cannot be a simple contrast between observed Bombus-present and Bombus-absent site-seasons.

The direction also survives every single-island omission:

- Izu5: `+1.432..+2.226`, all positive;
- post4: `+1.456..+2.333`, all positive.

**Interpretation:** continuous pollinator functional structure contains explanatory variation inside the post-boundary region itself. The contemporary mechanism should therefore be represented by functional diversity rather than reduced to a binary Bombus label.

This remains observational. Fixed effects remove time-invariant site differences and common seasonal shifts, but not time-varying weather/resources, measurement error, network feedback or historical selection.

Source lock: `data/predictive_meta/hiraiwa_ushimaru_continuous_functional_exposure.json`.

## 2. Trait matching → pollen receipt is positive but network-state sensitive

The archived source Figure-5 reproductive-success line uses a positive TM coefficient of `+0.04865`.

Because the pollen table contains multiple flowers per plant × site × season, flowers are first averaged within that cell. A sensitivity model with plant, site and season fixed effects gives:

| subset | plant × site × season cells | TM coefficient |
|---|---:|---:|
| all 8 sites | 124 | `+0.0295` |
| mainland | 46 | `+0.0468` |
| Izu5 | 78 | `+0.0353` |
| post4 | 60 | `+0.0342` |

The average direction is positive in every geographic subset, but the leave-one-island sensitivity crosses zero:

- Izu5: `-0.004..+0.073`; only omission of Hachijo is negative;
- post4: `-0.078..+0.101`; only omission of Hachijo is negative.

The new real-data omission audit localizes that fragility more precisely.

### Plant identity does not explain the shared positive coefficient

For both Izu5 and post4, all **9 estimable leave-one-plant models remain positive**:

- Izu5 range: `+0.0217..+0.0532`;
- post4 range: `+0.0177..+0.0521`.

The *Oxalis corniculata* var. *trichocaulon* omission makes the fixed-effect design singular, so it is explicitly non-estimable and is not counted for either sign.

This does not mean plant biology is homogeneous. It means no single estimable plant taxon is responsible for the positive shared TM coefficient.

### The instability localizes to season 3 and, post-Oshima, Hachijo × season 3

Leaving out one season at a time gives:

- Izu5: `-0.0147..+0.0636`; only season 3 omission is negative;
- post4: `-0.0316..+0.0654`; only season 3 omission is negative.

Leaving out one complete site × season network state at a time sharpens the result:

- Izu5: all **24/24 estimable** omissions remain positive, `+0.0088..+0.0521`;
- post4: **18/19** remain positive; the only sign reversal is omission of `Hachijo × season 3`, which gives `-0.0406`.

Thus the positive post-Oshima matching-to-pollen coefficient is not a stable property of every network state. A particularly informative Hachijo season-3 state supplies enough leverage that removing it reverses the post4 coefficient. When Oshima is included, no single site × season omission reverses the Izu5 coefficient, although removing all of Hachijo or all of season 3 still does.

### Site × season clustered uncertainty also remains broad

`TM_z` is shared by plants within one site × season network state, so plant × cell rows cannot be treated as independent exposure replicates. CR1 sandwich uncertainty clustered by site × season gives:

| subset | clusters | TM coefficient | cluster SE | 95% t interval | two-sided p |
|---|---:|---:|---:|---:|---:|
| all 8 sites | 38 | `+0.0295` | `0.0232` | `[-0.0175, +0.0765]` | `0.212` |
| mainland | 14 | `+0.0468` | `0.0457` | `[-0.0518, +0.1455]` | `0.324` |
| Izu5 | 24 | `+0.0353` | `0.0322` | `[-0.0314, +0.1019]` | `0.285` |
| post4 | 19 | `+0.0342` | `0.0406` | `[-0.0510, +0.1194]` | `0.411` |

Every point estimate remains positive, but every cluster-aware interval contains zero. Interval overlap with zero is **not** evidence of biological absence; it says that the current network-state replication does not support a precise, geographically stable downstream coefficient.

**Interpretation:** the upstream FDQ → matching relationship is reproducible across island omissions and source covariates, whereas translation from matching into open-pollinated pollen receipt is directional but uncertain and strongly network-state dependent. The contemporary mechanism is therefore not a deterministic `FDQ -> matching -> pollen` cascade with one fixed downstream coefficient.

Source locks:

- `data/predictive_meta/hiraiwa_ushimaru_matching_to_pollen.json`;
- `data/predictive_meta/hiraiwa_ushimaru_matching_to_pollen_heterogeneity.json`.

## 3. Direct FDQ → pollen receipt is not promoted to a main result

Exploratory fixed-effect fits of pollen receipt directly on FDQ are small and leave-one-island unstable. This is consistent with attenuation through plant-specific reproductive biology and network-state dependence and is not source-locked as a strong mechanism claim.

The paper should therefore not say that pollinator functional diversity uniformly determines reproductive success. The supported structure is:

> **pollinator functional diversity → trait matching: robust contemporary association**  
> **trait matching → pollen receipt: positive direction, cluster-uncertain and network-state conditional**  
> **long-term reproductive assurance / morphology / persistence: distinct response modes**

The independent 2017 reproductive study reinforces this structure: *Calystegia soldanella* is sensitive to long-tongued-pollinator loss, *Vitex rotundifolia* is resilient in fruit set, and *Lysimachia mauritiana* changes counterdirectionally. Those plant-specific reproductive modes remain relevant even though no single estimable plant taxon drives the shared contemporary TM coefficient.

## 4. Dependency moderation remains a separate unresolved question

Available mainland realized interaction breadth and tube length do not robustly moderate the FDQ → matching slope. Those are not effective-pollinator dependency measures.

A primary-source audit of the 10 pollen-target plants yields 4 externally resolved species-level pollination systems, 5 partial and 1 unresolved, but **zero source-resolved high-dependency Bombus targets and zero exact-2024-Izu dependency measurements**. Direct dependency moderation is therefore design-blocked, not null.

Files:

- `data/predictive_meta/hiraiwa_ushimaru_functional_moderation.json`;
- `data/predictive_meta/hiraiwa_ushimaru_pollen_target_dependency_readiness.csv`;
- `data/design/pollen_target_dependency_moderation_readiness.json`.

## Claim boundary

None of these contemporary associations establish that historical Bombus loss caused the focal *Campanula* autonomous-reproduction transition, flower-size erosion, or mating-system change. Site × season clusters are shared observational exposure states, not experimental treatments. Their value is narrower and stronger: the data identify a robust upstream functional-mechanism axis and show directly that its downstream reproductive-function expression is conditional rather than uniform, which sharpens what the prospective dependency measurements must explain.
