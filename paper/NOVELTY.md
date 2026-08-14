# Methodological novelty — current self-audit

The useful novelty is **not** the generic hypothesis that island pollinator
simplification can favour smaller flowers or compress floral size. That idea
predates this project.

- Inoue's Izu work already linked island *Campanula* flower-size reduction to
  changes in pollinator availability and pollinator body size.
- Hendriks (2019), *The island rule and its application to multiple plant
  traits*, explicitly proposed the **Pollinator Potential Paradigm**: island
  pollinator assemblages may contain a reduced subset of mainland pollinator
  body-size diversity, narrowing the range of floral sizes favoured on islands.

Hendriks tested flower-size response shape across island–mainland sister taxa,
but did not directly measure pollinator functional distributions, single-visit
pollen transfer, or population-specific effective dependency. The prior-art
boundary is therefore explicit: **pollinator-potential compression is an
existing biological hypothesis; this project asks how to identify, falsify, and
partition that mechanism across response channels and independent systems.**

## 1. Step, cline, and no-response are competing biological hypotheses

The focal *Campanula* evidence contains separable channels:

- floral size: continuous erosion;
- multilocus outcrossing: continuous erosion;
- autonomous reproductive capacity: sharp Oshima → Toshima/post transition;
- contemporary interaction breadth and trait matching: neither simply copies
  the historical breeding-system step.

This separation matters because island responses need not form one syndrome or
one monotonic axis. A trait may change gradually, switch after an ecological
boundary, remain stable, broaden through partner replacement, or track
colonisation/environmental history rather than pollinator regime.

The cross-lineage test therefore treats

```text
none | cline | first_step | second_step | two_step | environment_history | rewiring
```

as competing response modes. A shared breakpoint or shared response shape across
independent lineages is a result to be earned, not inferred from the focal
species.

## 2. Functional exposure is separated from effective dependency

A major advance over a generic pollinator-availability hypothesis is to keep two
biologically different quantities distinct:

1. **functional exposure** — what pollinator functional distribution a plant
   population actually experiences; and
2. **effective dependency** — how much reproductive function is lost when
   effective pollination service is reduced.

The current contemporary Izu data provide a strong observational link from
pollinator FDQ to corrected flower–pollinator trait matching. The downstream
matching-to-pollen relationship is positive but weaker. Direct effective
pollinator dependency in the exact populations remains prospective.

The field chain is therefore designed as

```text
functional exposure
  -> legitimate contact / single-visit pollen deposition
  -> rate-weighted effective service
  -> open / autonomous / supplemental-outcross reproduction
  -> effective dependency
  -> response mode
```

rather than treating pollinator species richness, absence, visit frequency, or
flower morphology as interchangeable proxies for dependency.

## 3. Heterogeneous data can share a question without sharing an effect scale

The registry accepts separate native observation models for:

- continuous and proportional traits;
- binary or ordinal states, including SI/SC;
- effective interaction states;
- detection-aware island occupancy;
- source-native network contrasts; and
- paired island–mainland morphology response shapes.

This permits broad screening while preventing a presence/absence record, a
network-turnover contrast, and a sister-taxon flower-size slope from being
pooled as noisy measurements of one latent "island effect".

## 4. Independent-system replication is not manufactured from islands or taxa

The project now has a concrete example of why this rule matters.

Southwest Pacific source-native animal-pollinated flower-size pairs and the
independent Hendriks (2019) flower-area sister pairs both show a direct

```text
slope(log island floral trait ~ log mainland floral trait) < 1
```

under island-cluster resampling:

- Southwest Pacific animal flower size: slope `0.8490`, island-cluster interval
  `[0.6916, 0.9258]`;
- Hendriks flower area: slope `0.5833`, island-cluster interval
  `[0.2128, 0.7785]`.

This is **2/2 independent-system directional replication of a compression-like
response shape under OLS**, not a pooled island-rule coefficient. Multiple
islands within one source do not become independent cross-system replications.

## 5. Measurement error is an admission gate, not an afterthought

The Southwest Pacific source initially appeared to give a robust negative slope
for `log10(FI/FM) ~ log10(FM)`. But the mainland measurement enters both the
predictor and the response denominator. A dedicated denominator-coupling audit
therefore demoted the starting-size rows from formal effect admission while
retaining the numerical result.

The independent Hendriks reconstruction avoids that exact algebraic coupling by
using direct `log(island) ~ log(mainland)` regression, yet x-axis measurement
error can still attenuate the slope. Its island-cluster SMA interval includes
isometry.

A joint classical errors-in-variables envelope now states the assumption needed
for the 2/2 OLS direction to survive:

- both point estimates remain below isometry if mainland-trait reliability is
  above `0.8490` in both systems;
- both island-cluster intervals remain below isometry if reliability is above
  `0.9259` in both systems.

Those are **required conditions, not estimated reliabilities**. Formal
same-family synthesis therefore remains closed.

## 6. Generalists and alternative channels provide falsification, not decoration

The negative-control prediction is not that every open-generalist trait is
perfectly flat. It is that generalists should not repeatedly share a
specialist-specific response shape or breakpoint merely because they occur on
the same islands.

The design also keeps explicit alternatives:

- loss of self-incompatibility / gain of self-compatibility;
- autonomous reproduction;
- realised selfing;
- de-specialisation or functional broadening;
- replacement by a different specialised guild;
- ecological interaction loss without immediate morphological change;
- non-establishment and survivorship filtering;
- hybrid replacement; and
- environment / colonisation-history responses.

The informative target is therefore a dependency-class × functional-exposure ×
response-mode interaction, not a one-dimensional selfing syndrome.

## 7. Prediction locking precedes independent lineages

`data/predictive_meta/regime_transition_registry.csv` fixes analysis role,
dependency class, response domain, observation unit, regime coverage, evidence
status and allowed response models. One lineage × one prespecified response
family is one comparison unit, so multiple islands, images or correlated traits
cannot masquerade as independent evolutionary replications.

The external effect registry applies the same principle at the system level.
A formal cross-system model opens only when compatible source-locked effects with
defensible uncertainty occur in at least two independent system clusters.

## 8. Failed observation operators remain falsification results

The public-image work required both a known-flat biological control and a
technical sensitivity control. Several crop operators detected technical
changes but manufactured regional differences in the flat *Ajania* control. No
operator was released to the broad specialist holdout.

This remains a reusable methodological contribution: validate the observation
process before interpreting a regional phenotype.

## 9. Source provenance and extraction state constrain claim level

Numeric effects require exact source location, population units, sample size,
uncertainty, taxonomy, geography, wild status and compatible units.

The Hendriks flower-area reconstruction illustrates why provenance and effect
admission must remain separate gates. The exact lawful VUW institutional PDF is
now recovered and checksum locked, and all 35 Appendix B Table B9 numerical
pairs plus all 35 Appendix-A island assignments have been strictly reverified
against those bytes. The Hendriks provenance gate is therefore complete, and
the OLS anchors reproduce the thesis results.

That provenance repair does **not** make the Hendriks slope a formal
cross-system effect. Mainland flower-area measurement reliability is still not
empirically identified, the island-cluster SMA interval includes isometry, and
flower area is not treated as an exchangeable raw effect scale with the
Southwest Pacific source-defined flower-size response. Hendriks therefore
supports source-locked directional recurrence while formal same-family pooling
remains closed.

Likewise, the 136-pair Hetherington-Rauth & Johnson (2020) Pacific source remains
candidate-only until its source-native numeric table is recovered.

## 10. Simulation and sensitivity are design diagnostics, not empirical replication

Retained constrained diagnostics may quantify which observation plans can
discriminate declared mechanisms, and reliability envelopes quantify assumptions
needed for a result to survive measurement error. Neither is evidence that the
simulated mechanism or assumed reliability holds in nature. Legacy synthetic
suites that no longer change an admission or field-design decision have been
retired from the active tree and remain recoverable from Git history.

## Current empirical contribution

The evidence-bearing contribution has advanced beyond the initial evidence-map
stage, but remains deliberately narrower than a completed causal meta-analysis:

1. a source-locked focal *Campanula* calibration separating continuous floral
   size/outcrossing erosion from a sharp autonomous-capacity transition;
2. a contemporary observational functional axis in which FDQ robustly predicts
   corrected trait matching, with a weaker downstream pollen-function link;
3. source-locked external network systems showing that partner turnover can be
   much stronger than partner-richness decline;
4. a checksum-locked 129-pair Southwest Pacific morphology source with explicit
   pollination-mode, archipelago and denominator-coupling adversaries;
5. a checksum-locked Hendriks institutional source with all 35 flower-area pairs
   and all 35 island assignments strictly reverified, reproducing the reported
   OLS response shape across nine populated island groups;
6. a 2/2 independent-system directional replication of below-isometry floral
   response under OLS/island-cluster resampling;
7. an explicit joint EIV envelope showing that interval-level recurrence under
   the declared classical model requires reliability above about `0.926`, while
   reliability itself remains unobserved; and
8. an executable provenance/admission framework that prevents positive-looking
   source results from being promoted when their sampling hierarchy,
   measurement model, or causal interpretation is unresolved.

## What is still novel enough to defend

The strongest defensible novelty is **not a new pollinator-potential story**. It
is the combination of:

- channel-specific response-shape inference rather than a single island
  syndrome;
- direct separation of functional exposure from effective reproductive
  dependency;
- independent-system replication without manufacturing replication from taxa or
  islands;
- explicit establishment, rewiring, hybrid and environmental alternatives;
- negative controls and prediction locking before broad source recovery; and
- provenance- and measurement-error-aware admission gates that can *demote* an
  apparently supportive result.

If the prospective Izu SVD + reproductive-treatment data identify a reproducible
`functional exposure × effective dependency` interaction while the declared
alternative channels remain separated, that would be the project's strongest
mechanistic advance beyond Inoue's pollinator-availability hypothesis and
Hendriks' Pollinator Potential Paradigm.

Until then, causal attribution and a universal island-flower coefficient remain
closed.
