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

## 2. Trait matching → pollen receipt is positive but attenuated

The archived source Figure-5 reproductive-success line uses a positive TM coefficient of `+0.04865`.

Because the pollen table contains multiple flowers per plant × site × season, flowers are first averaged within that cell. A sensitivity model with plant, site and season fixed effects gives:

| subset | plant × site × season cells | TM coefficient |
|---|---:|---:|
| all 8 sites | 124 | `+0.0295` |
| mainland | 46 | `+0.0468` |
| Izu5 | 78 | `+0.0353` |
| post4 | 60 | `+0.0342` |

The average direction is positive in every geographic subset, but the leave-one-island sensitivity crosses zero:

- Izu5: `-0.004..+0.073`;
- post4: `-0.078..+0.101`.

**Interpretation:** trait matching has a positive reproductive-function association, but it is materially weaker and less geographically robust than the upstream FDQ → matching association.

Source lock: `data/predictive_meta/hiraiwa_ushimaru_matching_to_pollen.json`.

## 3. Direct FDQ → pollen receipt is not promoted to a main result

Exploratory fixed-effect fits of pollen receipt directly on FDQ are small and leave-one-island unstable. This is consistent with attenuation through plant-specific reproductive biology and is not source-locked as a strong mechanism claim.

The paper should therefore not say that pollinator functional diversity uniformly determines reproductive success. The supported structure is:

> **pollinator functional diversity → trait matching: robust contemporary association**  
> **trait matching → pollen receipt: positive but attenuated/conditional**  
> **long-term reproductive assurance / morphology / persistence: distinct response modes**

The independent 2017 reproductive study reinforces this structure: *Calystegia soldanella* is sensitive to long-tongued-pollinator loss, *Vitex rotundifolia* is resilient in fruit set, and *Lysimachia mauritiana* changes counterdirectionally.

## 4. Dependency moderation remains a separate unresolved question

Available mainland realized interaction breadth and tube length do not robustly moderate the FDQ → matching slope. Those are not effective-pollinator dependency measures.

A primary-source audit of the 10 pollen-target plants yields 4 externally resolved species-level pollination systems, 5 partial and 1 unresolved, but **zero source-resolved high-dependency Bombus targets and zero exact-2024-Izu dependency measurements**. Direct dependency moderation is therefore design-blocked, not null.

Files:

- `data/predictive_meta/hiraiwa_ushimaru_functional_moderation.json`;
- `data/predictive_meta/hiraiwa_ushimaru_pollen_target_dependency_readiness.csv`;
- `data/design/pollen_target_dependency_moderation_readiness.json`.

## Claim boundary

None of these contemporary associations establish that historical Bombus loss caused the focal *Campanula* autonomous-reproduction transition, flower-size erosion, or mating-system change. Their value is narrower and stronger: they supply an independently observed, continuously varying functional mechanism axis against which the historical response modes can be interpreted and prospectively tested.
