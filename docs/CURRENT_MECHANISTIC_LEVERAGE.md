# Current mechanistic leverage

## Bottom line

The current Izu programme supports **heterogeneous response modes linked by a contemporary pollinator-functional mechanism**, not one universal island-flower syndrome.

Evidence is kept at three levels:

1. **response shape established** — what changes in a defined biological channel;
2. **mechanistic leverage** — whether explicit alternatives or source-native functional exposures constrain interpretation;
3. **causal attribution** — still blocked. `data/predictive_meta/current_mechanistic_leverage.csv` keeps `causal_claim_allowed = no` for every current evidence unit.

The strongest historical breakpoint remains the focal *Campanula microdonta* autonomous-reproduction transition. The strongest contemporary mechanism-compatible link is **pollinator functional diversity (FDQ) → corrected flower–pollinator trait matching**. Independent morphology, interaction breadth and reproductive responses remain heterogeneous rather than collapsing into one response syndrome.

## Campanula: continuous channels and breakpoint channel must remain separate

### Flower size

The historical focal literature supports island-series floral-size erosion, but source-native population-genetic evidence also supports ordered colonisation history. The historical size cline is therefore a strong descriptive pattern but a weak mechanism discriminator.

A completely independent contemporary field dataset supplies site-level corolla-tube means measured from five flowers per plant species at each site. In those data, *Campanula microdonta* has Oshima mean `26.9825 mm` and mean across Niijima, Kozu, Miyake and Hachijo `19.4534 mm` (`-27.9%`). This independently reproduces the lower-post morphology direction.

The contemporary series lacks Toshima and within-site SD/SE, so it cannot distinguish a smooth cline from an Oshima/post step or enter the A-grade inverse-variance holdout.

### Multilocus outcrossing

Outcrossing declines strongly along the historical island series. Tested climate PC1, mainland distance, island area/connectivity and pre-1986 volcanic-recency axes do not reproduce the ordered erosion as well as island order.

Island order is nevertheless not a causal exposure. The allozyme literature supports progressive southward colonisation, while the RAPD literature identifies exceptions including multiple immigration on Miyake. The continuous mating-system pattern remains confounded with demographic history.

### Autonomous reproductive capacity

This remains the strongest historical breakpoint channel. The Oshima-to-Toshima transition is much sharper than the continuous morphology/outcrossing patterns and is not reproduced by tested climate, mainland distance, static geography or pre-observation volcanic-history alternatives.

That gives the channel the strongest current breakpoint leverage, but not historical causal identification: an unmeasured breeding-system, founder or demographic threshold could still coincide with the same boundary.

### Contemporary Campanula network function does not copy the historical breeding step

In the 2024 network data, *Campanula microdonta* shows **higher**, not lower, post-Oshima values for both realized functional generality (`+0.508`) and corrected trait matching (`+0.571`) relative to Oshima.

Thus the historical autonomous-reproduction step is not a synchronous all-channel ecological step. Morphology, mating system, autonomous capacity and contemporary network function remain distinct response domains.

## Contemporary network evidence

The reproducibly acquired Hiraiwa–Ushimaru 2024 Figshare dataset (`10.6084/m9.figshare.25025000.v1`) spans three Honshu sites, Oshima, Niijima, Kozu, Miyake and Hachijo across five seasons.

### All network plants reject a universal second step

After seasonal rows are aggregated within `plant × site`:

| response | eligible species | lower post | higher post |
|---|---:|---:|---:|
| functional generality | 14 | 6 | 8 |
| corrected trait matching | 16 | 10 | 6 |

There is no universal species-level Oshima/post response in contemporary network function.

### Source-defined pollen-success target plants show a bounded matching signal

The source study independently selected 10 dominant outcrossing insect-pollinated plants for pollen-receipt measurements. Among eligible members:

| response | eligible species | lower post | higher post |
|---|---:|---:|---:|
| functional generality | 8 | 3 | 5 |
| corrected trait matching | 8 | 8 | 0 |
| pollen receipt | 9 | 5 | 4 |

Corrected trait matching is directionally coherent in this source-defined subset, while interaction breadth and pollen receipt are not.

Leave-one-post-island sensitivity is strong but not perfect: 7/7 lower after omitting Niijima or Kozu, 6/8 after omitting Miyake, and 7/8 after omitting Hachijo.

Among seven target plants with complete five-island coverage, Oshima is the only possible island baseline for which the mean of the other four islands is lower in **7/7** species; corresponding values are Niijima `5/7`, Kozu `5/7`, Miyake `2/7`, Hachijo `1/7`. This argues against an arbitrary-baseline artifact, but Oshima remains a single geographic bridge-state site.

### Boundary identifiability remains limited

The contemporary design contains three mainland sites, **one Oshima bridge-state site**, and four post-boundary sites. Five seasons are temporal replication, not five independent Oshima-like geographic units. Plant species sharing sites are not independent boundary experiments.

A site-aware model can estimate a descriptive Oshima/post contrast, but cannot separate an Oshima-specific site effect from a causal second-boundary effect.

## Continuous pollinator functional exposure is the strongest contemporary mechanism link

The binary boundary is not the only available exposure. The same network dataset contains pollinator functional diversity (`FDQ`) varying across all eight sites and five seasons.

The archived source code fits community corrected trait matching using functional diversity and evenness; the source Figure-3 best model has:

- FDQ coefficient: `+1.5540`;
- FEve coefficient: `-9.2976`.

A transparent fixed-effect sensitivity model,

`TM_z ~ FDQ + FEve + site fixed effects + season fixed effects`,

produces the following FDQ coefficients:

| subset | site × season rows | FDQ coefficient | site-centered FDQ–TM correlation |
|---|---:|---:|---:|
| all 8 sites | 40 | `+1.8346` | `+0.3025` |
| mainland 3 sites | 15 | `+1.5414` | `+0.1810` |
| Izu 5 islands | 25 | `+1.9426` | `+0.4034` |
| post-Oshima 4 islands | 20 | `+2.0590` | `+0.3410` |

The relationship therefore does **not** require mainland observations. More importantly, it persists after Oshima is removed: within Niijima, Kozu, Miyake and Hachijo alone, higher pollinator functional diversity is associated with higher corrected trait matching after time-invariant site differences and common seasonal shifts are absorbed.

The island-only direction is not carried by a single site. Leave-one-island FDQ coefficients are:

- Izu 5-island subset: `+1.432` to `+2.226`, all positive;
- post-Oshima 4-island subset: `+1.456` to `+2.333`, all positive.

This materially changes the interpretation. The FDQ → matching signal is not simply another encoding of mainland versus island, Oshima versus southern islands, or Bombus-present versus Bombus-absent geography. **Continuous pollinator functional structure still matters inside the post-boundary region itself.**

It remains observational. Time-varying weather/resources, network feedback, measurement error and historical selection are not removed, so this is a **contemporary functional mechanism link**, not a historical causal estimate and not proof that Bombus loss generated the pattern.

Source lock: `data/predictive_meta/hiraiwa_ushimaru_continuous_functional_exposure.json`.

## Does plant specialization moderate the FDQ → matching slope?

### Do not use legacy floral-form labels as dependency

The old candidate-screening classification based on family/floral form is not an effective-pollinator dependency dataset and is excluded from this test.

Two source-native continuous plant moderators were estimated using **mainland sites only**, before using island response rows:

1. mainland realized plant functional generality (`FG_Pla_sp_z`) — interaction breadth, not dependency;
2. mainland corolla-tube length (`tube`) — morphology, not dependency.

Nine source-defined pollen-success target plants pass the minimum three-mainland-observation gate, producing 105 plant × site × season rows. The descriptive sensitivity model includes plant, site and season fixed effects plus FEve.

### Realized interaction breadth does not robustly moderate the FDQ slope

At mean moderator value:

- FDQ coefficient: `+0.2880`;
- `FDQ × mainland breadth`: `+0.00723`.

The interaction changes sign under sensitivity:

- leave-one-site range: `-0.128` to `+0.093`;
- leave-one-plant range: `-0.151` to `+0.197`.

### Tube length also does not provide a stable moderator

- FDQ coefficient: `+0.2952`;
- `FDQ × mainland tube length`: `+0.0675`;
- leave-one-site range: `-0.045` to `+0.204`;
- leave-one-plant range: `-0.243` to `+0.212`.

The sign is not stable. Therefore neither available proxy explains species-level FDQ-slope heterogeneity robustly.

This is **not evidence that pollinator dependency is irrelevant**. It only bounds two available proxies.

Source lock: `data/predictive_meta/hiraiwa_ushimaru_functional_moderation.json`.

## Why direct dependency moderation is currently not identifiable in the 10 target plants

A primary-source audit constrains nine of the ten source-defined target pollination systems:

- **resolved external species-level: 4**;
- **partial: 5**;
- **unresolved: 1** (*Persicaria senticosa*).

The resolved systems do not span a Bombus-dependency gradient:

- *Ampelopsis glandulosa*: functional specialization on short-tongued scoliid wasps and solitary bees (`10.1016/j.flora.2021.151921`); the 2024 target is var. *hancei*, so transfer remains species-level external evidence;
- *Calystegia soldanella*: self-incompatible, pollinator-dependent broad bee system (`10.2307/2656764`), plus strong 2017 reproductive sensitivity to long-tongued-pollinator loss;
- *Lonicera japonica*: effective mixed diurnal-bee + nocturnal-hawkmoth system (`10.1139/b98-119`);
- *Vitex rotundifolia*: multiple hymenopteran pollinators with *Megachile kobensis* dominant/well matched in coastal Japan (Maeta et al. 2004).

Partial evidence further constrains broad/diverse entomophily for *Farfugium* and *Glehnia*, a population-variable selfing/outcrossing system in *Oxalis corniculata*, and non-exclusive functional responses/interactions in *Lysimachia* and *Melanthera*.

Crucially:

- source-resolved high-dependency Bombus targets in this 10-species set: **0**;
- effective dependency measured in the exact 2024 Izu target populations: **0**.

Therefore a direct `dependency × FDQ` model is currently **design-blocked**, not null. The dominant target set is survivor-conditioned: strict high-dependency lineages that fail to establish, hybridize or rewire are less likely to appear among shared dominant coastal plants in the first place.

Files:

- `data/predictive_meta/hiraiwa_ushimaru_pollen_target_dependency_readiness.csv`;
- `data/design/pollen_target_dependency_moderation_readiness.json`.

## Direct morphology also rejects one common response direction

The 2024 archive stores species × site mean tube lengths based on five measured flowers per species per site. Within-site SD/SE are absent, so these are B+ directional data rather than A-grade effect sizes.

Among eight eligible target species:

- shorter post: 3;
- longer post: 4;
- equal: 1.

Thus direct floral morphology does not show a universal second-boundary direction.

### Farfugium: high interaction breadth does not mean stasis

*Farfugium japonicum* was prospectively selected using only realized functional generality and coverage (`mean FG_Pla_sp_z = 1.675`, eight sites). Its channels are non-synchronous:

- functional generality: `+0.00265` Oshima→post;
- corrected trait matching: `-2.80665`;
- pollen receipt: `-0.88773`;
- site-mean tube length: `11.276 mm` on Oshima vs `10.339 mm` post (`-8.3%`).

The blind visible-display control is still inferentially inconclusive: mainland `n=5`, Oshima `n=1`, post `n=1`, all score 3. No equivalence/no-change claim is allowed.

## Direct reproductive sensitivity is heterogeneous

The 2017 Hiraiwa–Ushimaru natural experiment provides a separate validation layer:

- *Calystegia soldanella*: fruit set decreases as long-tongued-pollinator biomass/matching decrease;
- *Vitex rotundifolia*: fruit set shows no significant relationship with those exposures;
- *Lysimachia mauritiana*: fruit set changes in the counterdirection with long-tongued-pollinator biomass.

Oshima fruit-set data were unavailable after a landslide, so these responses cannot localize the focal second boundary. They nevertheless establish sensitivity, resilience and counterdirectional reproductive modes under the same functional exposure gradient.

## Survivor conditioning and alternative response modes

A clean same-lineage specialist survivor is not an unbiased sample of high dependency.

- mainland pure *Goodyera henryi* is Bombus-dependent, but on Kozu pure *G. henryi* was not recovered; the island comparator is hybrid with *G. similis* and uses a scoliid-wasp interaction → `hybrid replacement + interaction rewiring`;
- *Calanthe aristulifera* supplies a same-lineage example in which a mainland large-bee interaction is replaced by a plausible small-sweat-bee route on Mikura;
- *Lilium auratum* var. *platyphyllum* supplies an alternative Lepidoptera timing mechanism, although variety and geography are confounded.

Establishment failure, taxonomic/hybrid replacement and interaction rewiring are response domains, not invalid missing data.

## General floristic boundary is not the Oshima–Toshima boundary

Suzuki (1956) reports 1038 archipelago taxa, including 103 southern and 43 northern elements, and places the conspicuous southern-element northern limit at **Miyakejima** and northern-element southern limit at **Mikurajima**, rather than Oshima–Toshima.

This historical external control weakens the alternative that every Oshima–post pattern merely reflects the archipelago's generic whole-flora north–south boundary. It is not a modern normalized species × island matrix; the source-reviewed occupancy analysis remains blocked until such a matrix is obtained.

## What the paper can now argue

The strongest defensible synthesis is:

> **Plant responses to altered pollination environments in the Izu Islands are channel- and lineage-specific, but contemporary network data expose a common functional mechanism axis.** In focal *Campanula*, continuous morphology/outcrossing erosion is separated from a sharp autonomous-reproduction transition. Independent contemporary data reject a universal morphological, interaction-breadth or reproductive response, while pollinator functional diversity is positively associated with flower–pollinator trait matching even within the post-Oshima islands and after time-invariant site effects are absorbed. Available breadth and tube-length proxies do not robustly moderate that relationship, and direct dependency moderation remains unidentified because the shared dominant target set lacks a source-resolved high-dependency Bombus endpoint and is survivor-conditioned.

The pollinator hypothesis is therefore not a universal-syndrome claim and not yet a fitted binary specialist/generalist effect. It is a structured hypothesis about **functional pollinator exposure × effective dependency × response mode × establishment history**.

## Decisive next evidence

1. obtain effective-pollinator dependency measurements for the **same Izu populations**, especially a high-dependency endpoint;
2. broaden the sampling frame beyond shared dominant survivors so failure to persist, hybrid replacement and rewiring can enter as outcomes;
3. recover population-level uncertainty for independent morphology (Weigela, Ligustrum, Hosta or equivalent) to open A-grade effect-size synthesis;
4. recover a reviewed multi-island flora matrix for establishment/filtering without occurrence-zero shortcuts;
5. match population-history covariates to the same trait populations rather than using island order as history;
6. obtain another independent bridge-state geography or a temporal regime transition before interpreting Oshima/post contrasts causally.

Until those gates are met, causal attribution remains closed.
