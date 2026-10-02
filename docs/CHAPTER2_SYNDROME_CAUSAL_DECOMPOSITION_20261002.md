# Chapter 2 prospective extension — causal decomposition of floral syndromes

**Date:** 2026-10-02  
**Status:** prospective research extension; **not part of the current frozen Chapter 2 claim surface**  
**Parent model:** unified Model 3 on main at `945fc5a46b3e2e23cd41cd89ed67d01a12707ead`

## Core idea

The extension treats **island syndrome, selfing syndrome and pollination syndrome as recurring outcomes, not causal mechanisms**.

Chapter 1 asks what recurs in nature. Its current handoff is that reproductive assurance and floral accessibility/generalization recur more consistently than detailed pollinator-facing phenotype. Chapter 2 should therefore ask a different question:

> **Which separable causal routes can generate a syndrome-like combination of traits, and why do those component traits need not evolve at the same rate or even in the same direction?**

The working causal chain is:

```text
isolation / pollinator loss or replacement
        ↓
visitor amount + functional composition
        ↓
pollen transfer and outcross opportunity
        ↓
┌───────────────────────────────────────────────┐
│ route A: reproductive-assurance substitution │
│ route B: pollinator functional rematching    │
└───────────────────────────────────────────────┘
        ↓
selection on pollinator-facing traits
        ↓
inheritance under available genetic variation
        ↓
finite recruitment / survival / extinction
        ↓
realized syndrome component(s)
```

The syndrome is therefore the **joint realized phenotype at the bottom of the chain**, not an explanatory variable placed at the top.

## What is already established in adjacent theory

The novelty claim must not be that any one component is unprecedented.

### Mating-system theory

Porcher & Lande (2005) modelled pollen limitation, pollen discounting, selfing and inbreeding depression and showed that pollen limitation can strongly favour high selfing through reproductive assurance.

- Porcher E, Lande R. 2005. *The evolution of self-fertilization and inbreeding depression under pollen discounting and pollen limitation*. Journal of Evolutionary Biology 18:497–508. https://doi.org/10.1111/j.1420-9101.2005.00905.x

**What this already solves:** why pollen limitation can favour selfing.  
**What it does not by itself solve:** why a pollinator-facing floral investment should subsequently be reduced, retained, or redirected.

### Floral attraction / specialization theory

Sargent & Otto (2006) linked pollinator abundance and effectiveness to evolution of floral specialization.

- Sargent RD, Otto SP. 2006. *The role of local species abundance in the evolution of pollinator attraction in flowering plants*. The American Naturalist 167:67–80. https://doi.org/10.1086/498433

**What this already solves:** how pollinator abundance/effectiveness can alter optimal attraction/specialization.  
**What it does not by itself solve:** the full path through reproductive assurance, explicit Mendelian inheritance, finite recruitment and persistence.

Recent trait-matching eco-evolutionary models also formalize mutualistic trait matching; for example, Eriksson et al. (2026) allow pollinators to evolve in response to plant-composition change while plants are non-evolving.

- Eriksson et al. 2026. *Eco-Evolutionary Dynamics of Generalist and Specialist Pollinators Facing Plant Diversity Changes*. Ecology and Evolution. https://doi.org/10.1002/ece3.73182

### Syndrome literature

The selfing syndrome is a well-established repeated association between mating-system transition and traits such as reduced floral display and herkogamy, but its genetic architecture is heterogeneous rather than a single universal route.

- Sicard A, Lenhard M. 2011. *The selfing syndrome: a model for studying the genetic and evolutionary basis of morphological adaptation in plants*. Annals of Botany 107:1433–1443.

Pollination syndromes likewise summarize recurrent suites of floral traits associated with functional pollinator groups but are descriptions of trait–pollinator association rather than one universal causal pathway.

- Dellinger AS. 2020. *Pollination syndromes in the 21st century: where do we stand and where may we go?* New Phytologist 228:1193–1213. https://doi.org/10.1111/nph.16793

A recent genomic review explicitly emphasizes that pollination-syndrome shifts require coordinated change across multiple component traits and that dominance, pleiotropy, linkage and standing genetic variation can alter accessibility of those transitions.

- *Genomic and Molecular Bases of Pollination Syndrome Evolution*. Annual Review of Plant Biology, 2026. https://doi.org/10.1146/annurev-arplant-072125-082325

## The intended novelty

The target contribution is therefore **not** “the first model of selfing,” “the first pollinator-matching model,” or “the first island simulation.”

It is the following integration:

> **A recurrent floral syndrome is generated, or fails to be generated, by explicitly separable ecological, reproductive, genetic and demographic stages. The same pollinator deterioration can therefore produce recurrent functional insurance without requiring one recurrent detailed phenotype.**

More specifically, the prospective extension tests four distinctions that syndrome labels normally collapse.

### 1. Reduced positive selection is not the same as adaptive trait reduction

If pollinator service declines, the benefit of a pollinator-facing trait can decline. But a weaker positive benefit alone does not force the trait downward.

For an abstract pollinator-facing investment (z),

[
g_z
=
rac{\partial B_{poll}(z)}{\partial z}
-
rac{\partial C(z)}{\partial z}.
]

A directional decline requires the remaining cost or another directional force to exceed the pollination benefit. Therefore the model must distinguish:

- **relaxed selection:** pollination benefit approaches zero but no countervailing cost is present;
- **adaptive reduction:** pollination benefit declines while a positive allocation/maintenance cost remains.

This distinction is a central causal target of Stage A.

### 2. Reproductive assurance is a substitution route, not a synonym for floral reduction

Autonomous reproduction can replace some lost outcross function. The hypothesized route is:

```text
pollinator service ↓
        ↓
outcross opportunity ↓
        ↓
reproductive assurance carries more reproduction
        ↓
marginal benefit of pollinator-facing investment ↓
        +
investment cost remains
        ↓
selection can favour lower investment
```

The key prediction is not simply “selfing increases.” It is that the sign of selection on floral investment should depend jointly on pollinator service, assurance and investment cost.

### 3. Pollinator loss and pollinator replacement are different perturbations

A decline in visitor number changes the amount of service. A shift from one functional visitor composition to another changes the location of the matching optimum even at identical visitor count.

Stage A therefore separately manipulates:

- visitor activity/service at fixed composition;
- visitor functional composition at fixed count.

A composition-driven response is interpreted as **functional rematching**, not as the reproductive-assurance route.

### 4. Selection on a trait and evolutionary accessibility of that trait are different

Stage A deliberately does not claim that flower colour is intrinsically “easy” and floral architecture intrinsically “hard.”

There is biological motivation for trait-specific accessibility, but it is system-dependent. Floral pigmentation can sometimes change through a single major regulatory locus; for example, an R3 MYB regulator underlies a major anthocyanin QTL between *Mimulus lewisii* and *M. cardinalis*. Conversely, corolla-tube formation depends on coordinated developmental growth and the tasiRNA–ARF/auxin pathway in *Mimulus*, although major loss-of-function mutations can also strongly alter tube formation.

- Yuan/Yuan-lab work on anthocyanin QTL: https://doi.org/10.1534/genetics.113.148239
- Ding et al. 2020, corolla-tube developmental genetics: https://doi.org/10.1105/tpc.18.00471

Thus Stage B, if opened, will parameterize **trait-specific evolutionary accessibility** rather than hard-code a universal colour-versus-shape ordering.

Candidate parameters are:

- standing genetic variance by trait;
- mutation supply by trait;
- mutational effect-size distribution by trait;
- cross-trait mutational covariance / pleiotropic coupling.

The decisive test will be whether unequal accessibility changes the **order and completeness** with which syndrome components appear under the same ecological selection.

## Stage A — frozen causal knockout using existing Model 3

The exact design is frozen in:

`data/design/chapter2_syndrome_causal_knockout_20261002.json`

No Model 3 biological operator is changed.

### Route A: assurance × cost

Factorial:

- visitor activity: low (0.05) versus reference (0.4);
- fixed assurance: (0) versus (0.5);
- floral-investment cost: (0) versus (0.5);
- functional visitor composition held fixed;
- starting access held fixed.

Primary endpoint:

- fixed-state marginal total reproductive return to floral investment.

Secondary propagation endpoints:

- deterministic inherited investment change;
- finite-ABM inherited investment change;
- terminal occupancy.

The preregistered causal signature is:

1. low service + assurance + cost gives a negative investment gradient;
2. removing assurance moves that gradient upward;
3. removing investment cost moves that gradient upward.

### Route B: rematching at equal visitor count

Factorial:

- identical visitor count (four visitor types);
- left-, centre- and right-shifted functional compositions;
- starting access (0.2, 0.5, 0.8);
- activity, assurance and investment cost fixed.

The preregistered signature is a same-count left-versus-right composition contrast that either reverses the sign of the investment gradient or differs by at least the predeclared gradient threshold.

## Stage B — conditional next step

Stage B is **not yet an accepted Model 3 result**.

It is opened only if Stage A confirms at least one ecological route and the abstract access/investment representation remains insufficient to explain asynchronous trait response.

The minimal extension should preserve the existing ecology and change only the genetic-availability layer:

```text
same ecological selection
        ↓
equal genetic accessibility       asymmetric genetic accessibility
        ↓                          ↓
synchronous response              lagged / partial trait response
```

This is the direct model analogue of the Chapter 1 observation that broad functional responses can recur while detailed display modules do not converge.

## Claim firewall

Until new simulations are frozen and executed, the current Chapter 2 paper remains unchanged.

Do **not** claim from this prospective extension that:

- a literal selfing syndrome has already been generated;
- floral investment equals flower colour;
- access equals corolla-tube geometry;
- colour is universally more evolvable than morphology;
- any molecular pathway has been inferred for Izu;
- a synthetic time, distance or effect size is calibrated to nature.

The prospective novelty is the **causal decomposition itself**. Trait-specific molecular interpretation is a later layer to be tested, not assumed.
