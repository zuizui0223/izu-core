# Chapter 2 prospective extension — causal decomposition of floral syndromes

**Date:** 2026-10-02  
**Status:** prospective extension executed through Stage A + standing-variation Stage B pilot; **not part of the current frozen Chapter 2 claim surface**  
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

### Island-biogeography theory and simulation

Classical and general dynamic island-biogeography models explain biodiversity through immigration, extinction and speciation, often as functions of island area, isolation and ontogeny. More recent dynamic models estimate these processes across real island radiations.

- Whittaker RJ, Triantis KA, Ladle RJ. 2008. *A general dynamic theory of oceanic island biogeography*. Journal of Biogeography 35:977–994. https://doi.org/10.1111/j.1365-2699.2008.01892.x
- Valente L et al. 2020. *A simple dynamic model explains the diversity of island birds worldwide*. Nature 579:92–96. https://doi.org/10.1038/s41586-020-2022-5

**What these frameworks already solve:** how isolation and island history alter colonization, speciation, extinction, richness and endemism.  
**What Chapter 2 asks at a different scale:** how one isolation-sensitive mutualism propagates inside a plant population from visitor arrival and functional composition to pollen transfer, mating, inherited floral change, persistence and extinction.

Thus Chapter 2 is not a replacement for island biogeography. It is a **within-population mechanistic layer beneath the usual island-biogeographic rates**, focused on phenotype realization rather than species richness.

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


## Executed results

### Stage A: the existing Model 3 already separates two syndrome-generating routes

The preregistered causal knockout passed on Python 3.10, 3.11 and 3.12.

Under low visitor activity (`0.05`):

- **no assurance + investment cost 0.5:** total investment gradient `+0.602`, but the 60-year finite population had `0/8` terminal survivors, so no inherited endpoint existed;
- **assurance 0.5 + no investment cost:** gradient `+0.611`, deterministic investment change `+0.0875`;
- **assurance 0.5 + investment cost 0.5:** gradient **`-0.393`**, deterministic change **`-0.0726`**, finite-ABM mean **`-0.0721`**, with full terminal occupancy;
- restoring visitor activity to `0.4` with assurance and cost present moved the gradient to **`+1.681`**.

Thus the negative pollinator-facing investment response is not produced by pollinator scarcity alone. In this operator it appears when low outcross service is combined with reproductive assurance that permits persistence and a positive cost of maintaining pollinator-facing investment.

The two prospectively defined knockouts moved the low-service gradient upward by approximately one full gradient unit:

- assurance effect with cost present: `-0.995` for target-minus-knockout;
- cost effect with assurance present: `-1.004`.

The same-count rematching test was equally clear. Left4 versus right4 visitors differed by **`+2.377`** in the fixed investment gradient at starting access `0.2` and **`-2.377`** at starting access `0.8`; the corresponding deterministic inherited-change contrasts were `+0.189` and `-0.189`. At the symmetric starting access `0.5`, the contrast was essentially zero.

So the existing operator distinguishes:

1. **service-loss / assurance / cost** — a route to reduced pollinator-facing investment;
2. **functional replacement / rematching** — a route that changes which floral state is favoured even when visitor count is unchanged.

Full numeric receipt: `data/results/chapter2_syndrome_causal_knockout_20261002.json`.

### Stage B pilot: genetic availability can make syndrome components asynchronous

A second preregistered pilot changed **only founder standing variation**. The ecological operator, visitor environments, inheritance rules and mutation rate (`0`) were unchanged.

When access standing SD was reduced from `0.15` to `0.03`, its initial density variance fell from about `0.00834` to `0.000494`. The mean absolute deterministic response lost **`0.1136`** relative to the equal-high-variation regime; the corresponding finite-ABM difference was **`0.0961`**.

When investment standing SD was reduced from `0.15` to `0.03`, its initial density variance fell from about `0.00789` to `0.000582`. The mean absolute deterministic response lost **`0.1054`**; the finite-ABM difference was **`0.0830`**.

For example, under left4 visitors:

- equal-high variation: access `-0.150`, investment `+0.119` in deterministic inheritance;
- constrained access: access only `-0.0428`, while investment remained `+0.106`;
- constrained investment: access remained `-0.148`, while investment was only `+0.0104`.

Thus **the same ecological selection operator can generate incomplete or asynchronous syndrome components simply because different trait axes have different available genetic variation**.

This does not show that real flower colour is easier than real corolla architecture. It shows the more general causal point needed by Chapter 2: **selection and evolutionary accessibility are separable stages**.

Full numeric receipt: `data/results/chapter2_trait_accessibility_pilot_20261002.json`.


## Next extension — mutation supply, linkage and pleiotropy

The standing-variation pilot has now established the minimum genetic-filter result: unequal available variation can make trait axes respond asynchronously under the same unchanged ecological operator.

The next extension should therefore **not** add more ecological mechanisms. It should keep Stage A ecology fixed and deepen only the genetic-accessibility layer:

```text
same ecological selection
        ↓
standing variation
        +
trait-specific mutation supply / effect sizes
        +
cross-trait linkage or pleiotropic coupling
        ↓
which syndrome components can move, how fast, and in what combinations
```

This is where literal molecular hypotheses can eventually enter. The appropriate question is not “is colour easy and shape hard?” but:

> **Which distributions of mutational availability and pleiotropic constraint are sufficient to reproduce fast signal-like change, slower architecture-like change, or coordinated multi-trait switches?**

That formulation matches the Chapter 1 observation that broad functional responses can recur while detailed display modules do not converge, without hard-coding a universal molecular hierarchy.

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
