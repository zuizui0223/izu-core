# Do island floral response shapes recur across pollination environments? A source-native, mechanism-gated synthesis anchored in the Izu Islands

**Draft manuscript. Version 0.7 (2026-08-11). Source-native external validation + measurement-error gates.**

*Campanula microdonta* in the Izu Islands remains the high-resolution mechanistic
anchor. External archipelagos are used to test recurrence and boundary
conditions, not as exchangeable rows in a single global island-effect model.

---

## Abstract

Reduced pollinator availability and altered pollinator composition have long
been proposed to favour smaller, less specialised flowers and greater
reproductive assurance on islands. In the Izu Islands, Inoue's work already
linked smaller *Campanula* flowers and mating-system change to altered
pollinators, and Hendriks (2019) later formalised a broader **Pollinator
Potential Paradigm** in which island pollinator assemblages represent reduced
subsets of mainland pollinator body-size diversity. The unresolved problem is
therefore not whether this mechanism can be imagined, but how to distinguish it
from colonisation history, environment, rewiring, establishment filtering,
measurement error, and heterogeneous biological response channels.

We develop a source-native framework anchored in the unusually deep Izu record.
The source-locked *Campanula microdonta* series separates continuous floral-size
and multilocus-outcrossing erosion from a sharp Oshima→Toshima/post transition
in autonomous reproductive capacity. Contemporary Izu network data do not copy
that historical step: across sites and seasons, pollinator functional diversity
(FDQ) is robustly associated with corrected flower–pollinator trait matching,
while the downstream matching-to-pollen relationship is weaker. Direct
effective pollinator dependency in the same populations remains prospective.

External systems provide distinct response tests. Wanshan–Yongxing and
Ogasawara show that island interaction change can be dominated by partner
turnover rather than a uniform richness decline. A checksum-locked Southwest
Pacific source provides 129 mainland–island colonisation-event morphology
pairs. Among 88 valid source-coded animal-pollinated flower-size pairs, the
direct response slope `log(island size) ~ log(mainland size)` is `0.849`
(island-cluster 95% interval `0.692–0.926`), below the isometry slope of one. A
direct animal-versus-wind slope difference is not robust. Because the original
`log(FI/FM) ~ log(FM)` formulation shares the mainland measurement between the
predictor and response denominator, the starting-size effect is retained
numerically but blocked from formal cross-system admission.

We independently reconstruct all 35 flower-area sister pairs in Hendriks (2019)
and their nine populated island groups. The reconstructed direct OLS slope is
`0.583` (island-cluster 95% `0.213–0.778`), reproducing the reported `0.58` and
providing a second below-isometry response direction. However, an island-cluster
SMA sensitivity (`0.730–1.073`) includes isometry and the underlying thesis
artifact is not checksum locked. Thus two independent systems reproduce a
compression-like island floral response direction under OLS/island-cluster
resampling, but a joint errors-in-variables envelope shows that interval-level
recurrence under a classical x-error model requires mainland-trait reliability
above approximately `0.926` in both systems; that reliability is not observed.

The current contribution is therefore a mechanism- and provenance-gated
synthesis: response channels are kept separate, external recurrence is tested
without manufacturing replication, and apparently supportive effects can be
demoted by measurement/source adversaries. A universal island-flower coefficient
and causal pollinator attribution remain explicitly unresolved.

---

## 1. Introduction

Island flowers are often described as smaller, less conspicuous or more
self-reliant than mainland relatives. Pollinator limitation is an obvious
candidate explanation, but the basic idea is not new. Inoue's Izu studies
reported smaller island *Campanula* flowers and proposed adaptation to smaller
pollinators, while subsequent work framed breeding-system evolution in terms of
bumblebee absence and pollinator availability. Hendriks (2019) generalised a
related idea as the Pollinator Potential Paradigm: if island pollinators form a
reduced subset of the mainland fauna and consequently span a narrower body-size
range, island floral-size diversity may also contract.

Those observations define the prior-art boundary. Demonstrating another
mainland–island size slope does not by itself identify pollinator causation.
Island trait change may instead reflect founding history, progressive
colonisation, climate, island area, disturbance, phenotypic plasticity, lineage-
specific constraints, replacement by different pollinator guilds, or
non-establishment of dependent lineages. Even a true pollinator mechanism can
operate through different biological channels: attraction, mechanical matching,
pollen transfer, autonomous reproduction, realised selfing, or establishment.

The Izu archipelago offers unusual leverage because historical pollination,
breeding-system and floral measurements can be linked to contemporary
plant–pollinator networks and to prospective direct field measurements. We use
Izu as the mechanistic anchor and ask three increasingly demanding questions:

1. **Response shape:** which biological channels show clines, discrete steps,
   no response, or rewiring?
2. **External recurrence:** do independent island systems reproduce compatible
   response directions when analysed in their source-native units?
3. **Mechanistic identification:** does directly measured functional pollinator
   exposure interact with effective reproductive dependency after alternative
   histories and measurement error are considered?

The third question remains prospective. The first two can already be tested
without treating heterogeneous island observations as exchangeable replicates.

### 1.1 Contributions

This study contributes:

1. a source-locked three-channel Izu calibration that separates floral-size,
   mating-system and autonomous-reproduction response shapes;
2. a contemporary functional-exposure analysis linking pollinator FDQ to
   corrected flower–pollinator matching and downstream pollen function;
3. external network contrasts that distinguish partner turnover from simple
   partner-richness loss;
4. a checksum-locked 129-pair Southwest Pacific morphology analysis with direct
   pollination-mode and archipelago heterogeneity tests;
5. an independent 35-pair Hendriks flower-area reconstruction across nine
   island groups;
6. a 2/2 independent-system directional audit of the direct
   `log(island trait) ~ log(mainland trait)` response shape;
7. provenance and errors-in-variables admission gates that prevent supportive
   numerical patterns from being promoted beyond their identification level;
   and
8. a prospective field design separating functional exposure from directly
   measured effective dependency.

The novelty is therefore **not** the pollinator-potential hypothesis itself. It
is the explicit identification architecture used to test and potentially
falsify it.

---

## 2. Materials and methods

### 2.1 Evidence architecture

Each dataset is analysed first in its source-native biological unit. We do not
pool community networks, sister-taxon morphology pairs, population-level mating
systems, occurrence records, photographs and reproductive experiments as raw
observations of one island effect.

A numerical effect can enter the formal cross-system registry only when its
source, comparison units, response definition, uncertainty and sampling hierarchy
are explicit. Multiple islands or taxa within one source do not automatically
create independent system-level replication.

### 2.2 Izu historical response channels

The adopted focal *Campanula microdonta* calibration retains three historical
channels:

```text
flower size                    -> continuous erosion
multilocus outcrossing         -> continuous erosion
autonomous reproductive capacity -> sharp Oshima -> Toshima/post transition
```

Climate, mainland distance, island area/connectivity, volcanic history and
colonisation/genetic history are retained as explicit competitors rather than
being folded into a generic isolation variable.

### 2.3 Contemporary Izu functional exposure

The Hiraiwa–Ushimaru Figshare dataset
(`10.6084/m9.figshare.25025000.v1`) spans three Honshu sites and five Izu islands
across five seasons. Pollinator functional diversity (FDQ), flower–pollinator
trait matching, interaction breadth and pollen receipt are analysed at their
source-defined site/season or plant/site/season units. Leave-one-island and
functional-covariate sensitivities test whether the FDQ association is a simple
mainland/island or Oshima/post artefact.

Visitor identity and frequency are not treated as pollinator effectiveness.
Effective dependency remains unmeasured until direct single-visit pollen
deposition and reproductive treatments are collected in matched populations.

### 2.4 External network systems

Wanshan–Yongxing (`10.5061/dryad.t76hdr8bj`) provides whole-community and
seven-shared-plant visitation matrices. Ogasawara (`10.5281/zenodo.19221853`)
provides legitimate interaction events across island, habitat, invasion context
and season. These systems test rewiring and partner-turnover responses; they do
not measure direct effective dependency.

Galápagos raw network recovery remains transport-blocked, so only
source-published island summaries are used and no plant-level network is
reconstructed.

### 2.5 Southwest Pacific paired morphology

The Southwest Pacific source (`10.1093/aob/mcaf005`; PMCID `PMC12445859`)
contains 129 source-defined mainland–island colonisation events across ten
archipelagos. The exact S2 workbook is checksum locked. Flower-size response is
analysed by source-coded pollination mode and archipelago/family resampling.

The published/source formulation uses

```text
LR = log10(FI / FM)
LR ~ log10(FM)
```

which creates a shared-mainland-measurement coupling. We therefore also express
response shape in the algebraically equivalent direct form

```text
log10(FI) ~ log10(FM)
```

and apply a classical measurement-error partial-identification gate before
formal effect admission.

### 2.6 Hendriks 2019 flower-area reconstruction

The author-uploaded Hendriks MSc thesis exposes Appendix B Table B9. All 35
island–mainland flower-area pairs were transcribed into a checked reconstruction.
Appendix A species lists were used to assign the flower-area pairs to island
groups, and the resulting counts were required to reproduce Table A14 exactly.

We reproduce the thesis OLS anchor, bootstrap pairs, bootstrap Appendix-A island
groups, perform leave-one-island deletion, and calculate standard-major-axis
(SMA) sensitivity. Because the underlying source artifact is not checksum
locked, this reconstruction cannot enter the formal effect registry.

### 2.7 Directional cross-system audit

To test recurrence without pooling incompatible raw effect scales, the two
independent morphology systems are compared only on

```text
slope(log island floral trait ~ log mainland floral trait)
```

where isometry equals one. A direction is considered replicated when the
source-native OLS estimate and island-cluster interval remain below one in each
independent system.

### 2.8 Classical errors-in-variables envelope

For a declared classical x-error sensitivity,

```text
beta_observed = reliability_x * beta_true
```

we calculate the minimum mainland-trait reliability required for each observed
point or island-cluster upper bound to remain below isometry after attenuation
correction. Reliability is not estimated by this analysis; it is a scenario
parameter.

---

## 3. Results

### 3.1 Izu channels do not form one synchronous syndrome

Historical floral size and multilocus outcrossing show continuous ordered
erosion, whereas autonomous reproductive capacity shows a much sharper
Oshima→Toshima/post transition. Contemporary *Campanula* network function does
not reproduce that historical step: post-Oshima corrected trait matching and
realised functional generality are not jointly reduced.

Thus morphology, mating system, autonomous capacity and contemporary interaction
state must remain separate response domains.

### 3.2 FDQ is the strongest current contemporary mechanism-compatible axis

Site/season fixed-effect sensitivities retain positive FDQ coefficients for
corrected trait matching in all eight sites (`+1.835`), mainland three sites
(`+1.541`), Izu five islands (`+1.943`) and post-Oshima four islands (`+2.059`).
Every leave-one-island FDQ coefficient remains positive. Full functional-
covariate models also retain a positive FDQ contribution.

The downstream matching-to-pollen relationship is positive but less robust and
leave-one-island ranges cross zero. The current mechanism chain is therefore
asymmetric:

> **FDQ → trait matching: robust observational association**  
> **trait matching → pollen receipt: positive but attenuated**

### 3.3 External networks show turnover can exceed richness change

For the seven shared Wanshan–Yongxing plants, median visitation LRR is `−2.511`
(95% `−3.323` to `−2.052`), pollinator-richness LRR is `−0.105` (`−1.322` to
`0.288`), and Morisita–Horn partner turnover is `0.980` (`0.944–1.000`).

In the source-defined Anijima Ogasawara context contrast, partner turnover is
`0.682` (`0.497–0.965`) while visitation and richness intervals are less
decisive. These systems show that island interaction responses can be dominated
by replacement and rewiring rather than uniform partner loss.

### 3.4 Southwest Pacific flower-size response is conditional, not a universal mean shift

Valid flower-size data comprise 88 source-coded animal pairs and 38 wind pairs.
For `log10(FI/FM) ~ log10(FM)`, the animal slope is `−0.1510` with island-cluster
95% `−0.3041` to `−0.0725`; the wind slope is `−0.0761` with island-cluster 95%
`−0.1488` to `0.1163`.

A direct animal-minus-wind slope comparison is not robust. Among the six
archipelagos with at least five valid animal pairs, all six point slopes are
negative, whereas mean island/mainland flower-size change varies in sign.
Accordingly, the result is a starting-size-dependent response shape rather than
universal island dwarfism or a demonstrated pollination-mode difference.

The equivalent direct animal slope is `0.8490`, with island-cluster 95%
`0.6916–0.9258`.

### 3.5 Measurement-error coupling blocks formal Southwest Pacific starting-size admission

Under the declared classical error sensitivity, the animal direct point remains
below isometry only if mainland log-size reliability exceeds `0.8490`; keeping
the island-cluster interval wholly below one requires reliability above
`0.9259`. The source does not identify this reliability.

The animal and wind starting-size effects therefore remain numeric and
reportable but are not formal cross-system-model rows. This is an admission
change, not deletion of the observed pattern.

### 3.6 Hendriks independently reproduces the OLS response direction

All 35 Appendix B flower-area pairs and nine nonzero Appendix-A island groups are
reconstructed. The island-group frequency vector exactly reproduces Table A14.

The direct OLS slope is `0.5833`, reproducing the reported value `0.58`.
Pair-bootstrap 95% is `0.3060–0.8491`; island-cluster 95% is
`0.2128–0.7785`. Every leave-one-island OLS point remains below one.

The SMA point is `0.9000`, but its island-cluster interval is
`0.7297–1.0731`, including isometry. Hendriks is therefore a real independent
OLS directional replication but not an errors-in-variables-resolved formal
effect.

### 3.7 Two independent morphology systems reproduce below-isometry OLS response shape

On the common directional statistic:

| system | floral trait | pairs | island groups | direct OLS slope | island-cluster 95% |
|---|---|---:|---:|---:|---:|
| Southwest Pacific animal | flower size | 88 | 10 | **0.8490** | **0.6916–0.9258** |
| Hendriks 2019 | flower area | 35 | 9 | **0.5833** | **0.2128–0.7785** |

Both independent source-native OLS summaries and both island-cluster intervals
are below the isometry slope of one. This is **2/2 directional replication of a
compression-like floral response shape**. No pooled coefficient is estimated.

### 3.8 Joint EIV envelope identifies the remaining assumption

The Southwest Pacific system binds the joint classical reliability condition.
Both corrected point estimates remain below one if mainland-trait reliability is
above `0.8490` in both systems. Both corrected island-cluster intervals remain
below one only if reliability is above `0.9259`.

At a common reliability lower bound of `0.90`, both corrected point estimates
remain below one but the Southwest Pacific corrected cluster upper bound is
`1.0287`. At `0.93`, both cluster intervals remain below one.

These are assumption thresholds, not observations. Because reliability is not
empirically identified and Hendriks SMA uncertainty includes isometry, formal
same-family synthesis remains closed.

---

## 4. Discussion

### 4.1 The recurrent pattern is response compression, not universal dwarfism

The strongest external morphology result is not that all island flowers become
smaller. Southwest Pacific mean response varies across archipelagos, while both
independent morphology datasets show that **large mainland floral values tend to
move downward more strongly than small mainland values** under OLS. This is
closer to a compression or convergence response shape than a uniform directional
shift.

That distinction matters biologically. A pollinator-potential mechanism predicts
a change in the range of viable floral phenotypes more naturally than a fixed
negative mean effect. But the same response shape could also emerge from
energetic constraints, environmental filtering, regression artifacts,
measurement error or other lineage-specific processes.

### 4.2 Pollinator Potential Paradigm is motivation and competitor, not the novelty claim

Hendriks explicitly proposed that reduced island pollinator diversity and
body-size range could reduce floral-size range, while acknowledging Inoue's Izu
pollinator-availability precedent. The present data therefore should not be sold
as the first demonstration of that idea.

What this programme adds is a route from that broad hypothesis to a stricter
identification problem. In Izu we can separately observe functional pollinator
exposure, trait matching, pollen function and — prospectively — direct effective
dependency. Across systems we require source-native independent replication and
allow a result to be demoted by denominator coupling, source provenance or
errors-in-variables sensitivity.

### 4.3 Pollination mode and pollinator function must not be conflated

The Southwest Pacific animal subset has a robust starting-size slope, whereas
the wind subset is uncertain, but the direct between-mode contrast is not
robust. This is a useful falsification: significance in one subgroup and not the
other is not evidence that the subgroups differ.

Likewise, visitor richness, visitation frequency, FDQ, trait matching, partner
turnover, single-visit pollen deposition and effective dependency are different
quantities. The mechanistic target is not a binary animal/wind label but the
interaction between **functional exposure and reproductive dependency**.

### 4.4 External network rewiring argues against a one-dimensional loss syndrome

Wanshan–Yongxing and Ogasawara show that partner replacement can be much stronger
than richness loss. That observation strengthens the need to treat rewiring as
an alternative response mode. A plant lineage may retain reproductive function
by broadening or replacing its pollinator partners rather than by changing
flower size or mating system.

### 4.5 Measurement and provenance uncertainty are scientific results

The denominator-coupling audit materially changed the formal role of the
Southwest Pacific starting-size effect. Hendriks provides an independent
response-shape recurrence, but SMA uncertainty and unlocked provenance prevent
formal admission. These are not clerical caveats; they define which biological
claims the data can identify.

A robust synthesis should therefore report both supportive patterns and the
assumptions under which they survive. The current joint reliability threshold of
approximately `0.926` is useful precisely because it states what new information
would change the decision.

### 4.6 The decisive next step is direct effective dependency in Izu

The current Izu network association is compatible with a pollinator-functional
mechanism but remains observational. The next field gate links tagged flowers to
observation effort, legitimate contacts, single-visit pollen deposition,
rate-weighted effective service, and open/bagged/supplemental reproductive
outcomes.

If a prespecified `functional exposure × effective dependency` interaction
predicts response modes while environmental/history and rewiring alternatives
remain distinct, the programme would move beyond the earlier pollinator-
availability and Pollinator Potential hypotheses toward direct mechanistic
identification.

---

## 5. Current claim boundary

The present evidence supports:

1. channel-specific rather than synchronous Izu responses;
2. a robust observational FDQ-to-trait-matching link in contemporary Izu
   networks;
3. external network rewiring in which partner turnover can exceed richness
   decline;
4. a 2/2 independent-system below-isometry OLS floral response direction under
   island-cluster resampling; and
5. explicit reliability/provenance conditions needed before formal morphology
   synthesis.

It does **not** currently support:

- a universal island-flower coefficient;
- a causal pollination-mode effect;
- a universal mainland-distance effect;
- geological-origin causation;
- historical pollinator-loss causation;
- direct effective dependency; or
- an errors-in-variables-resolved cross-system meta-analysis.

---

## 6. Reproducibility

Key checked outputs include:

```text
data/results/southwest_pacific_pairs/analysis_summary.json
data/results/southwest_pacific_pairs/measurement_error_coupling_sensitivity_summary.json
data/results/hendriks_2019/flower_area_reconstruction_summary.json
data/results/cross_archipelago_morphology_response_shape_summary.json
data/results/cross_archipelago_morphology_eiv_envelope_summary.json
data/results/cross_archipelago_effect_registry_summary.json
data/design/pollinator_potential_prior_art.json
```

Corresponding scripts and tests regenerate the analyses and enforce the
admission boundaries in CI. Source-state failures remain explicit source states
rather than biological zeros.

## 7. Data availability

Source-locked public datasets retain their DOI/version/checksum information in
the repository. Reconstructed Hendriks flower-area values are explicitly marked
as a numerical reconstruction from a search-indexed author upload; the
underlying source artifact remains un-checksummed and is not promoted to a
formal effect row. Candidate sources enter formal synthesis only after their
source-native values, sampling hierarchy and uncertainty pass the declared
admission gates.
