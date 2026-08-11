# Izu prediction-locked regime-transition programme (`paper/`)

This directory tests whether independent Izu lineages and external island systems
show repeatable **response shapes** under changing pollination environments. Izu
is the high-resolution mechanistic anchor. External systems test recurrence and
boundary conditions. The project is not yet a causal multi-species or
cross-archipelago meta-analysis.

## Current decision

```text
focal_three_channel_calibration_established
+ contemporary_FDQ_matching_link_established
+ external_morphology_direction_replicated_2_of_2
+ errors_in_variables_and_direct_dependency_gates_open
```

The adopted *Campanula microdonta* calibration contains three source-locked
historical channels:

| channel | retained shape | current evidence |
|---|---|---|
| floral size | continuous erosion | source locked |
| multilocus outcrossing | continuous erosion | source locked |
| autonomous reproductive capacity | Oshima → Toshima/post step | source locked |

Contemporary Izu networks add a robust observational association between
pollinator functional diversity (FDQ) and corrected flower–pollinator trait
matching. The downstream matching-to-pollen link is positive but less robust.
Direct effective dependency in the exact populations is not yet measured.

## Prior-art boundary

The broad hypothesis that island pollinator simplification or smaller
pollinators can reduce floral size is **not novel** here.

- Inoue's Izu work already linked smaller island *Campanula* flowers to altered
  pollinators and developed pollinator-availability / bumblebee-absence
  hypotheses for mating-system evolution.
- Hendriks (2019) explicitly proposed the **Pollinator Potential Paradigm** in
  which a reduced island subset of mainland pollinator body-size diversity can
  compress floral-size diversity.

See `data/design/pollinator_potential_prior_art.json` and `paper/NOVELTY.md`.
The project's defensible novelty is the identification architecture:
functional exposure versus effective dependency, heterogeneous response modes,
explicit alternatives, independent-system replication, and provenance /
measurement-error admission gates.

## External morphology state

### Southwest Pacific

The checksum-locked 129-pair source supplies 88 valid source-coded animal
flower-size pairs. In direct response-shape form:

```text
slope(log island flower size ~ log mainland flower size) = 0.8490
island-cluster 95% = [0.6916, 0.9258]
```

The corresponding wind slope is less decisive and the direct animal-versus-wind
slope difference is not robust. The original `log(FI/FM) ~ log(FM)` formulation
also shares the mainland measurement between predictor and response denominator.
The starting-size effects are therefore numerical/descriptive but formally
blocked from the cross-system effect registry.

### Hendriks 2019

All 35 Appendix B Table B9 flower-area pairs have been reconstructed, and their
Appendix-A island assignments reproduce the Table A14 frequency vector across
nine populated island groups.

```text
reported direct OLS slope = 0.58
reconstructed direct OLS = 0.5833
island-cluster 95% = [0.2128, 0.7785]
SMA island-cluster 95% = [0.7297, 1.0731]
```

The underlying author-upload artifact is not checksum locked, and the SMA
interval includes isometry. Hendriks is therefore independent directional
replication, not a formal effect-registry row.

### Directional recurrence

On the common statistic

```text
slope(log island floral trait ~ log mainland floral trait), isometry = 1
```

Southwest Pacific flower size and Hendriks flower area both have source-native
OLS slopes and island-cluster intervals below one. This is a genuine **2/2
independent-system directional recurrence of a compression-like floral response
shape**. It is not a pooled coefficient.

## Joint errors-in-variables envelope

Under the declared classical x-error sensitivity:

- both point estimates remain below isometry if mainland-trait reliability is
  above `0.8490` in both systems;
- both island-cluster intervals remain below isometry if reliability is above
  `0.9259` in both systems.

At `r = 0.90`, both points remain below one but the Southwest Pacific corrected
cluster interval crosses one. At `r = 0.93`, both corrected cluster intervals
remain below one.

These are required assumptions, **not estimated reliabilities**. Hendriks SMA
uncertainty, unknown reliability and unlocked source provenance keep formal
same-family synthesis closed.

## Current cross-archipelago effect registry

```text
total rows                         = 17
empirical numeric rows             = 16
numeric rows with uncertainty      = 9
formal model-eligible rows         = 4
eligible independent clusters      = 2
compatible families in >=2 clusters = 0
formal cross-system fit ready      = false
```

The four eligible rows are three Wanshan–Yongxing network effects and the
Southwest Pacific animal floral-display mean. Starting-size morphology rows and
Hendriks remain outside formal synthesis for declared reasons.

## Competing response shapes

Each eligible lineage-response unit may compare:

```text
none
cline
first_step
second_step
two_step
environment_history
rewiring
```

The goal is not to force all traits into one island syndrome. A lineage may show
a smooth morphological cline, a mating-system transition, an ecological
rewiring response, occupancy filtering, or no ordered response.

## Response domains

| domain | examples | model family |
|---|---|---|
| quantitative trait | size, outcrossing, bagged set | continuous/count/proportion |
| binary or ordinal state | SI/SC, autonomous capacity, accessibility | Bernoulli/ordinal/multistate |
| effective interaction | FDQ, matching, legitimate contact, SVD | continuous/count/network with effort |
| occupancy / establishment | present, absent, replacement | detection-aware occupancy / multistate |

These domains share a response-shape vocabulary but not an effect-size scale.

## Functional exposure is not effective dependency

Visitor identity, visitation frequency, FDQ, trait matching, pollen deposition
and reproductive dependency are different quantities. The direct field chain is
predeclared as:

```text
plant / flower
  -> observation effort
  -> visitor bout / legitimate contact
  -> single-visit pollen deposition
  -> rate-weighted effective service
  -> open / bagged-autonomous / supplemental-outcross outcome
  -> effective dependency
```

Issue #91 is the critical direct-dependency gate.

## Generalist and alternative-channel falsification

Open-generalist lineages are negative controls for a shared specialist-specific
response, not a claim that all generalists must be invariant. Environment,
colonisation history, non-establishment, survivorship, hybrid replacement,
rewiring and alternative pollinator guilds remain first-class competitors.

## Workstreams

| Workstream | Main files | Scientific role |
|---|---|---|
| Focal response calibration | `data/inoue_literature_island_traits.csv`, channel-shape outputs | separates continuous and breakpoint historical channels |
| Contemporary functional mechanism | Hiraiwa–Ushimaru analysis outputs | tests FDQ → matching → pollen-function chain observationally |
| Direct dependency | Issue #91 field templates and precision simulations | prospective causal identification gate |
| External effect registry | `data/results/cross_archipelago_effect_registry*` | prevents heterogeneous systems from becoming pseudo-replication |
| Southwest Pacific morphology | `data/results/southwest_pacific_pairs/` | source-locked 129-pair response and denominator-coupling audit |
| Hendriks reconstruction | `data/source_tables/hendriks_2019_*`, `data/results/hendriks_2019/` | independent 35-pair flower-area direction and island-cluster sensitivity |
| Morphology directional audit | `cross_archipelago_morphology_response_shape_summary.json` | tests 2/2 recurrence without pooling coefficients |
| EIV envelope | `cross_archipelago_morphology_eiv_envelope*` | states reliability assumptions required to preserve recurrence |
| Prior-art lock | `pollinator_potential_prior_art.json`, `NOVELTY.md` | prevents rediscovery from being presented as novelty |
| Observation-operator falsification | ROI/generalist controls | blocks image operators that manufacture geographic phenotype |

## Immediate evidence work

1. Collect the Issue #91 direct SVD + reproductive-treatment pilot.
2. Recover empirical mainland-trait precision/reliability information or a third
   raw paired-flower system with explicit errors-in-variables leverage.
3. Recover and checksum-lock a stable Hendriks source artifact; verify all 35
   pair values and island assignments against it.
4. Continue source-native recovery of the Hetherington-Rauth & Johnson 2020
   136-pair Pacific dataset.
5. Expand direct dependency measurements across a distributed low–intermediate–
   high dependency gradient rather than one endpoint.
6. Keep non-establishment, hybrid replacement and rewiring in the comparative
   sampling frame.

## Evidence boundary

Occurrence is availability or occupancy evidence, not a floral trait. Visitor
identity is not pollinator effectiveness. Bagged capsule set is autonomous
reproductive capacity, not realised selfing. SC is not synonymous with
autonomous selfing. Pollinator Potential is prior art, not current causal proof.
Directional OLS recurrence is not an errors-in-variables-resolved universal
coefficient. Simulation and reliability envelopes are design/sensitivity tools,
not empirical mechanisms.
