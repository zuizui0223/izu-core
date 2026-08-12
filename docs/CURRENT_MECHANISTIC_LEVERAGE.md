# Current mechanistic leverage

## Bottom line

The current Izu programme supports **heterogeneous response modes linked by a
contemporary pollinator-functional mechanism axis**, not one universal
island-flower syndrome.

Evidence is kept at three levels:

1. **response shape established** — what changes in a defined biological
   channel;
2. **mechanistic leverage** — whether explicit alternatives or source-native
   functional exposures constrain interpretation;
3. **causal attribution** — still blocked. Current evidence units retain
   `causal_claim_allowed = no` unless direct identification is available.

The strongest historical breakpoint remains the focal *Campanula microdonta*
autonomous-reproduction transition. The strongest contemporary
mechanism-compatible link is **pollinator functional diversity (FDQ) → corrected
flower–pollinator trait matching**. A new external layer now gives **2/2
independent-system directional replication of a below-isometry floral response
shape under OLS/island-cluster resampling**, but errors-in-variables and source
provenance gates prevent promotion to a universal coefficient or causal
pollinator mechanism.

## Prior-art boundary: the broad pollinator-compression idea is not new

The mechanistic claim must be narrower than "island pollinator simplification
causes smaller flowers".

Inoue's 1986 Izu *Campanula* study already reported smaller island flowers and
suggested adaptation to smaller pollinators. His subsequent 1988/1990 breeding-
system work explicitly developed bumblebee-absence / pollinator-availability
hypotheses for the Izu series.

Hendriks (2019), *The island rule and its application to multiple plant traits*,
then introduced the **Pollinator Potential Paradigm** as a general explanation
for reduced island floral-size diversity: an island pollinator assemblage is a
subset of the mainland pool and may therefore contain a narrower pollinator
body-size range, which could favour a narrower floral-size range.

That thesis empirically tested floral response shape across island–mainland
sister taxa, not observed pollinator body-size distributions, single-visit
pollen transfer, or population-specific effective dependency. The current
project's mechanistic contribution is therefore the **identification problem**:
separating functional exposure, effective reproductive dependency, response
mode, rewiring, establishment history and measurement/source artifacts rather
than proposing pollinator-potential compression itself.

## Campanula: continuous channels and breakpoint channel must remain separate

### Flower size

The historical focal literature supports island-series floral-size erosion, but
source-native population-genetic evidence also supports ordered colonisation
history. The historical size cline is therefore a strong descriptive pattern but
a weak mechanism discriminator.

A completely independent contemporary field dataset supplies site-level
corolla-tube means measured from five flowers per plant species at each site. In
those data, *Campanula microdonta* has Oshima mean `26.9825 mm` and mean across
Niijima, Kozu, Miyake and Hachijo `19.4534 mm` (`-27.9%`). This independently
reproduces the lower-post morphology direction.

The contemporary series lacks Toshima and within-site SD/SE, so it cannot
distinguish a smooth cline from an Oshima/post step or enter the A-grade
inverse-variance holdout.

### Multilocus outcrossing

Outcrossing declines strongly along the historical island series. Tested climate
PC1, mainland distance, island area/connectivity and pre-1986 volcanic-recency
axes do not reproduce the ordered erosion as well as island order.

Island order is nevertheless not a causal exposure. The allozyme literature
supports progressive southward colonisation, while the RAPD literature
identifies exceptions including multiple immigration on Miyake. The continuous
mating-system pattern remains confounded with demographic history.

### Autonomous reproductive capacity

This remains the strongest historical breakpoint channel. The Oshima-to-Toshima
transition is much sharper than the continuous morphology/outcrossing patterns
and is not reproduced by tested climate, mainland distance, static geography or
pre-observation volcanic-history alternatives.

That gives the channel the strongest current breakpoint leverage, but not
historical causal identification: an unmeasured breeding-system, founder or
demographic threshold could still coincide with the same boundary.

### Contemporary Campanula network function does not copy the historical breeding step

In the 2024 network data, *Campanula microdonta* shows **higher**, not lower,
post-Oshima values for both realized functional generality (`+0.508`) and
corrected trait matching (`+0.571`) relative to Oshima.

Thus the historical autonomous-reproduction step is not a synchronous
all-channel ecological step. Morphology, mating system, autonomous capacity and
contemporary network function remain distinct response domains.

## Contemporary network evidence

The reproducibly acquired Hiraiwa–Ushimaru 2024 Figshare dataset
(`10.6084/m9.figshare.25025000.v1`) spans three Honshu sites, Oshima, Niijima,
Kozu, Miyake and Hachijo across five seasons.

### All network plants reject a universal second step

After seasonal rows are aggregated within `plant × site`:

| response | eligible species | lower post | higher post |
|---|---:|---:|---:|
| functional generality | 14 | 6 | 8 |
| corrected trait matching | 16 | 10 | 6 |

There is no universal species-level Oshima/post response in contemporary network
function.

### Source-defined pollen-success targets show a bounded matching signal

Among eligible members of the source-defined target set:

| response | eligible species | lower post | higher post |
|---|---:|---:|---:|
| functional generality | 8 | 3 | 5 |
| corrected trait matching | 8 | 8 | 0 |
| pollen receipt | 9 | 5 | 4 |

Corrected trait matching is directionally coherent in this subset, while
interaction breadth and pollen receipt are not.

## Continuous FDQ is the strongest contemporary mechanism link

The archived source model gives FDQ coefficient `+1.5540`. A site/season
fixed-effect sensitivity gives:

| subset | FDQ coefficient |
|---|---:|
| all 8 sites | `+1.8346` |
| mainland 3 sites | `+1.5414` |
| Izu 5 islands | `+1.9426` |
| post-Oshima 4 islands | `+2.0590` |

Every leave-one-island FDQ coefficient remains positive. A full
functional-covariate model retaining richness, `D`, FDQ, FRic and FEve also
retains positive FDQ coefficients and substantial incremental fit.

This relationship persists without mainland sites and without Oshima. It is
therefore not merely a binary mainland/island, Oshima/post or sampled Bombus
label. It remains observational: time-varying weather/resources, network
feedback and measurement error are not removed.

## Downstream matching → pollen receipt is attenuated

After flowers are averaged within `plant × site × season`, trait-matching
coefficients remain positive in all sites, Izu5 and post4, but leave-one-island
ranges cross zero. The mechanism chain is deliberately asymmetric:

> **FDQ → trait matching: robust**  
> **trait matching → pollen receipt: positive but materially less robust**

The 2017 experiment likewise supplies sensitive, resilient and
counterdirectional reproductive responses among *Calystegia*, *Vitex* and
*Lysimachia*.

## Direct dependency moderation remains empirically blocked

The 10 source-defined pollen targets contain 4 externally resolved, 5 partial
and 1 unresolved pollination systems, but:

- source-resolved high-dependency Bombus targets = `0`;
- direct effective dependency measured in the exact 2024 Izu populations = `0`.

Mainland realized breadth and tube length do not robustly moderate the FDQ slope
and cannot be promoted to dependency.

The field measurement chain is implementation-ready:

```text
plant/flower
  -> observation effort
  -> visitor bout/contact
  -> single-visit pollen deposition
  -> rate-weighted effective service
  -> open / bagged-autonomous / supplemental-outcross outcome
  -> fruit / seed / optional parentage
```

Issue #91 records the raw-data acceptance specification. Issue #92 records the
independent-source locality/n/uncertainty/dependency admission specification.

## Prospective dependency × FDQ design simulation

Existing data answer a design question before field collection. The simulation
anchors only the observed structure — 8 sites, 5 seasons, 9 proxy-eligible taxa
and 105 rows — while treating dependency values, reliability and interaction
effects as explicitly synthetic.

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

These values are synthetic operating characteristics, not empirical power.
Their design implication is nevertheless clear: **additional rows cannot
substitute for missing predictor support**. Direct dependency measurement
reduces attenuation, one high endpoint is valuable, and a distributed
low–intermediate–high dependency gradient is more informative than adding many
taxa inside a narrow survivor range.

## External network systems show rewiring rather than one response syndrome

Wanshan–Yongxing provides a matched seven-plant external network contrast in
which visitation declines strongly while pollinator partner turnover is almost
complete; partner richness is much less decisive. Ogasawara independently shows
substantial partner turnover under invasion/habitat context while visitation and
richness intervals are broader.

These are useful boundary conditions: ecological interaction structure can
change through **rewiring and replacement**, not only through monotonic loss of
visitor richness. Neither system measures direct effective dependency.

## External morphology now has directional, not formal, replication

### Southwest Pacific 129-pair source

The checksum-locked source-native analysis of 129 mainland–island colonisation
events gives a robust negative starting-size response among 88 valid
source-coded animal flower-size pairs. In equivalent direct form:

```text
slope(log island flower size ~ log mainland flower size) = 0.8490
island-cluster 95% = [0.6916, 0.9258]
```

A direct animal-minus-wind comparison is not robust, so this does not establish
pollination-mode moderation.

The original `log(FI/FM) ~ log(FM)` formulation shares the mainland measurement
between predictor and response denominator. The formal starting-size effect is
therefore blocked by the denominator-coupling admission gate even though the
numerical pattern is retained.

### Hendriks 2019 independent flower-area reconstruction

All 35 Appendix B Table B9 flower-area pairs have been reconstructed, and their
Appendix-A island assignments exactly match the reported Table A14 frequency
vector across nine populated island groups. The rounded reconstruction
reproduces the author OLS slope:

```text
reported direct OLS = 0.58
reconstructed direct OLS = 0.5833
island-cluster 95% = [0.2128, 0.7785]
```

The island-cluster SMA interval is `[0.7297, 1.0731]`, which includes isometry.
The VUW Open Access thesis record is now resolved, but the exact PDF/data bytes
remain undelivered and not checksum locked. Hendriks therefore remains
directional replication evidence rather than a formal effect-registry row.

### Cross-system response-shape result

On the common directional statistic

```text
slope(log island floral trait ~ log mainland floral trait), isometry = 1
```

Southwest Pacific flower size and Hendriks flower area both show OLS slopes and
island-cluster intervals below one. That is a genuine **2/2 independent-system
directional recurrence of a compression-like floral response shape**.

It is not a pooled coefficient because the traits are not identical, Hendriks
provenance remains unlocked, and errors-in-variables are not jointly resolved.

## Joint errors-in-variables envelope

A classical x-error partial-identification audit now quantifies the assumption
needed to preserve the 2/2 OLS recurrence:

- both point estimates remain below isometry if mainland-trait reliability is
  above **0.8490** in both systems;
- both island-cluster intervals remain below isometry if reliability is above
  **0.9259** in both systems.

At a common lower bound `r = 0.90`, both corrected point estimates remain below
one but the corrected Southwest Pacific cluster upper bound becomes `1.0287`.
At `r = 0.93`, both corrected cluster intervals remain below one.

These are required conditions under a declared classical error model, not
estimated reliabilities. The SMA boundary and unobserved reliability keep formal
same-family synthesis closed.

## What the paper can now argue

The current strongest synthesis is:

> **Plant responses to altered island pollination environments are channel- and
> context-specific, while two independent island–mainland morphology systems
> reproduce a compression-like response direction under source-native OLS and
> island-cluster resampling. In Izu, contemporary FDQ provides an observational
> functional link to flower–pollinator matching, but direct effective dependency
> and errors-in-variables remain the critical identification gates.**

This is intentionally different from claiming that reduced pollinator potential
causes a universal island floral-size rule. That broad hypothesis is prior art.
The current mechanistic programme tests the sharper interaction:

> **functional pollinator exposure × directly measured effective dependency ×
> response mode × establishment/history**

while preserving rewiring, replacement, environment and measurement error as
explicit alternatives.

## Decisive next evidence

1. collect the Issue #91 *Campanula* SVD + reproductive-treatment pilot and
   replace synthetic reliability/variance/loss assumptions;
2. extend direct dependency measurements across low, intermediate and high
   dependency lineages rather than one endpoint alone;
3. obtain empirical measurement precision/reliability for paired floral traits
   or another source-native system that supports an explicit errors-in-variables
   model;
4. checksum-lock and independently verify the Hendriks 35-pair source artifact;
5. recover the Hetherington-Rauth & Johnson 2020 136-pair source-native table or
   another compatible independent morphology system;
6. broaden beyond shared survivors so non-establishment, hybrid replacement and
   rewiring enter the sampling frame; and
7. obtain independent bridge-state or temporal regime replication before
   interpreting Oshima/post causally.

Until those gates are met, causal attribution and formal cross-system pooling
remain closed.
