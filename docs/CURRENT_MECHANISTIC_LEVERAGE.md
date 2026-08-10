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

### Source-defined pollen-success targets show a bounded matching signal

Among eligible members of the source-defined target set:

| response | eligible species | lower post | higher post |
|---|---:|---:|---:|
| functional generality | 8 | 3 | 5 |
| corrected trait matching | 8 | 8 | 0 |
| pollen receipt | 9 | 5 | 4 |

Corrected trait matching is directionally coherent in this subset, while interaction breadth and pollen receipt are not.

## Continuous FDQ is the strongest contemporary mechanism link

The archived source model gives FDQ coefficient `+1.5540`. A site/season fixed-effect sensitivity gives:

| subset | FDQ coefficient |
|---|---:|
| all 8 sites | `+1.8346` |
| mainland 3 sites | `+1.5414` |
| Izu 5 islands | `+1.9426` |
| post-Oshima 4 islands | `+2.0590` |

Every leave-one-island FDQ coefficient remains positive. A full functional-covariate model retaining richness, `D`, FDQ, FRic and FEve also retains positive FDQ coefficients and substantial incremental fit.

This relationship persists without mainland sites and without Oshima. It is therefore not merely a binary mainland/island, Oshima/post or sampled Bombus label. It remains observational: time-varying weather/resources, network feedback and measurement error are not removed.

## Downstream matching → pollen receipt is attenuated

After flowers are averaged within `plant × site × season`, trait-matching coefficients remain positive in all sites, Izu5 and post4, but leave-one-island ranges cross zero. The mechanism chain is deliberately asymmetric:

> **FDQ → trait matching: robust**  
> **trait matching → pollen receipt: positive but materially less robust**

The 2017 experiment likewise supplies sensitive, resilient and counterdirectional reproductive responses among *Calystegia*, *Vitex* and *Lysimachia*.

## Direct dependency moderation remains empirically blocked

The 10 source-defined pollen targets contain 4 externally resolved, 5 partial and 1 unresolved pollination systems, but:

- source-resolved high-dependency Bombus targets = `0`;
- direct effective dependency measured in the exact 2024 Izu populations = `0`.

Mainland realized breadth and tube length do not robustly moderate the FDQ slope and cannot be promoted to dependency.

The field measurement chain is now implementation-ready:

```text
plant/flower
  -> observation effort
  -> visitor bout/contact
  -> single-visit pollen deposition
  -> rate-weighted effective service
  -> open / bagged-autonomous / supplemental-outcross outcome
  -> fruit / seed / optional parentage
```

Issue #91 now records the full raw-data acceptance specification. Issue #92 records the independent-source locality/n/uncertainty/dependency admission specification.

## Prospective dependency × FDQ design simulation

Existing data can still answer a design question before field collection. The simulation anchors only the observed structure — 8 sites, 5 seasons, 9 proxy-eligible taxa and 105 rows — while treating dependency values, reliability and interaction effects as explicitly synthetic.

For a declared moderate interaction:

| design | calibrated detection probability |
|---|---:|
| current proxy-like structure | `0.065` |
| proxy + doubled seasons | `0.075` |
| proxy + four sites | `0.085` |
| direct measurement, narrow 9 taxa | `0.125` |
| direct + one high endpoint | `0.248` |
| direct full span, 10 taxa | `0.428` |
| direct narrow span, 16 taxa | `0.213` |
| direct full span, 16 taxa | `0.525` |

These values are synthetic operating characteristics, not empirical power. Their design implication is nevertheless clear: **additional rows cannot substitute for missing predictor support**. Direct dependency measurement reduces attenuation, one high endpoint is valuable, and a distributed low–intermediate–high dependency gradient is more informative than adding many taxa inside a narrow survivor range.

Files:

- `docs/DEPENDENCY_FDQ_DESIGN_SIMULATION.md`;
- `data/design/dependency_fdq_design_scenarios.json`;
- `data/results/dependency_fdq_design_simulation.json`.

## Independent source layer

*Weigela*, *Ligustrum* and *Hosta* remain B-grade directional sources. They currently constrain response shape but do not provide population means, independent `n`, uncertainty and exact locality mapping sufficient for quantitative admission. None independently localizes the predeclared Oshima–Toshima shared step.

*Goodyera* supplies hybrid replacement plus interaction rewiring; *Calanthe* supplies same-lineage rewiring; *Lilium* supplies an alternative Lepidoptera timing mechanism with variety–geography confounding.

## What the paper can now argue

> **Plant responses to altered pollination environments in the Izu Islands are channel- and lineage-specific, but contemporary network data expose a common functional mechanism axis.** Focal *Campanula* separates continuous morphology/outcrossing erosion from a sharp autonomous-reproduction transition. Contemporary FDQ is strongly associated with flower–pollinator matching even within post-Oshima networks, while the downstream reproductive link attenuates. Direct effective dependency is the next prospective measurement, and design simulation shows that a distributed dependency gradient is more informative than simply expanding proxy rows.

The pollinator hypothesis is therefore about **functional pollinator exposure × directly measured effective dependency × response mode × establishment history**.

## Decisive next evidence

1. collect the Issue #91 *Campanula* SVD + reproductive-treatment pilot and replace synthetic reliability/variance/loss assumptions;
2. extend direct dependency measurements across low, intermediate and high dependency lineages rather than one endpoint alone;
3. recover at least one Issue #92 population-level independent morphology source with locality, biological `n` and uncertainty;
4. broaden beyond shared survivors so non-establishment, hybrid replacement and rewiring enter the sampling frame;
5. recover a reviewed multi-island flora matrix for establishment filtering;
6. obtain independent bridge-state or temporal regime replication before interpreting Oshima/post causally.

Until those gates are met, causal attribution remains closed.
