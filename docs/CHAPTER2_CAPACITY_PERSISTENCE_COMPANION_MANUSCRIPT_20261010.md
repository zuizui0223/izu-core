# Demographic context conditions the persistence consequences of reproductive expression history

**Standalone mechanistic companion — working manuscript, 2026-10-10**  
**Evidence policy:** this article concerns a specified stochastic pollination–reproduction–genetics model, not a calibrated Izu Islands extinction forecast. `A-first` and `I-first` are **experimentally assigned transient phenotypic expression schedules**, not the spontaneous genetic order of mutation appearance. No new inferential tests were performed to compose this manuscript.

## Abstract

Changes in reproductive assurance and investment in pollinator attraction may unfold in different sequences, but whether the sequence affects finite-population persistence—and through which demographic conditions—remains difficult to distinguish from other reproductive mechanisms. Using a genetically explicit, individual-based plant model with stochastic visitor histories, we assigned equal-dose, transient reproductive expression schedules (assurance first or floral investment first) and quantified occupancy after 80 subsequent updates. The original preregistered difference-in-differences between near and far visitor environments was practically equivalent, and an independent restricted-resource-window hypothesis failed. A later controlled intervention reduced viable selfed seed retention by half, revealing a model-conditional sensitivity of the schedule effect in an eight-founder/capacity-eight bottleneck. Initial comparisons confounded founding abundance, demographic capacity and pollen delivery because the canonical capacity parameter also enters the pollen-recipient dilution denominator. After separating demographic capacity `K` from pollen-background dilution `B`, a prospectively registered, independently generated 64-history test at fixed `B=48` supported stronger selfed-seed-viability sensitivity at `K=8` than `K=48` (absolute occupancy interaction **+0.00775**, paired 95% history bootstrap **[+0.00250,+0.01302]**). Two other independent visitor-history cohorts showed positive secondary/descriptive estimates of the same contrast. A subsequent prospectively registered test did not resolve whether a viability intervention in the first rather than the last 40 updates was the main cause. Demographic capacity therefore moderates a **small, engineered seed-viability dependence of assigned reproductive expression history within this model**, without establishing natural genetic-order mediation or a general island rescue law.

**Keywords:** reproductive assurance; floral investment; finite-population demography; pollen delivery; selfed-seed viability; experimental expression history; ecological modeling; evidence hierarchy.

## Introduction

Pollinator limitation can change the relative returns to floral attraction and autonomous reproduction. These trait responses have at least three distinct causal questions: whether reproductive assurance is *necessary* for attraction-investment decline; whether the *order* of expression matters for local persistence; and whether any persistence contrast depends on the reproduction ledger, population regulation or both. Treating these as one pathway risks confusing temporal precedence with necessity and reproductive output with lifetime fitness.

The companion addresses only the latter two questions. The associated four-reproductive-setting main study showed that low visitor replenishment reduces floral investment even when assurance evolution is blocked, whereas allowing assurance to evolve compresses the near–far investment contrast. That independently confirmed result concerns inherited trait investment under sustained ecological environments. Its experimental arms all had terminal occupancy one; it does **not** estimate extinction mediation. Here the outcome is deliberately different: binary occupancy after 80 updates in stressed populations with at most eight founders at the start of follow-up.

The working hypotheses evolved adaptively as mechanisms were tested. We therefore report the original negative or inconclusive tests first and keep later registered primaries separate from results selected after seeing previous cohorts. We do not interpret three separately simulated cohorts as three independent model architectures.

## Methods

### Genetically explicit finite-population system

An individual-based model represents diploid alleles for visitor matching, floral investment and reproductive assurance; stochastic visitor arrivals/loss and plant recruitment are coupled to fertilization, viable selfed-seed production, other parentage and demographic competition. The archival prehistory comprises 400 reproductive updates. We use the inherited t400 states as authenticated starting sources and advance the subsequent population for **80 updates** under matched, pre-specified stochastic visitor histories. All pre-extinct sources and later extinctions remain in the analysis. `K` bounds the number of plants and associated demographic vacancies; it is not island area, and the modeled visitor regime is not calibrated geographic distance.

The experimental expression history assigned an **A-first** (reproductive assurance expression before investment expression) or **I-first** transient schedule with matched cumulative prescribed expression exposure. Alleles mutate and segregate under the same frozen source mechanism: the intervention does **not** force which genetic mutation arose first. At postshock entry expression offsets are zero.

### Why independent K and B were required

In the unmodified canonical reproduction equation the recipient pollen-transfer weight is normalized using `affinity.sum(axis=0) + config.capacity × config.background_ratio`. Directly changing `config.capacity` therefore alters both demographic carrying capacity and the background pollen-recipient dilution **before population numbers diverge**. An authenticated read-only audit of the first orthogonal experiment confirmed identical eight-founder starting population sizes but different initial female viable seed outputs across its K8/K48 regimes; expected pollen export remained identical.

A dedicated production module `reproduce_kb` changed only that denominator to `affinity.sum(axis=0) + B × config.background_ratio`, leaving the original `K` limit and core demography intact. Synthetic complete-ledger tests showed byte-identical reproduction with the canonical routine whenever `B=K` and identical initial reproductive ledgers across K arms at fixed B. A biological engineering pilot used already exposed histories before any independent confirmation cohort was generated.

### Interventions, outcome, and inference

For any capacity/pollen-background condition and postzygotic gate `g`, define `D(K,B,g)` as the mean difference in terminal occupancy probability between randomized A-first and I-first schedules. The binary outcome is whether any plants remain after 80 postshock updates. Define `tau(K,B) = D(K,B,baseline) − D(K,B,half_selfed)`, with `half_selfed` halving the *viable selfed-seed* ledger contribution (not pollen export or viable outcross seed at the intervention point). The primary K contrast is `tau(K8,B48) − tau(K48,B48)`, in **absolute occupancy probability**.

The independent confirmation sampled **64 entirely new visitor-history identities 41110901–41110964**, generated **2,048 complete full-diploid t400 source groups**, and admitted **114,688 future outcome cells** (two K conditions, two gates, seven budgets, two future visitor environments and original settings/history axes). Exactly the same up-to-eight founder genotypes entered K8 and K48 at fixed B48. The analysis used the frozen seven-budget logarithmic weights, equally averaged four reproductive settings and historical near/far states, pooled nested repeats and future visitor environments **within each history**, and bootstrapped **64 matched visitor-history clusters**, not future branches. The preregistered 9,999-draw, two-sided percentile bootstrap (seed `2026100967`) required an absolute mean at least **0.005** and a 95% interval excluding zero for support. Practical equivalence required the entire interval strictly within ±0.005; otherwise the result was inconclusive.

A distinct post-outcome cross-cohort comparison reads the original SHA-256–pinned machine outputs **without a newly fitted pooled interval or new significance test**. The broader four-arm K×B and later timed-viability cohorts each registered different primaries.

### Evidence and provenance firewall

We treat archived original-design outcomes, outcome-selected exploratory effects, and newly preregistered independent confirmations as different evidential levels. Original fixed near/far DID equivalence and an unsuccessful preregistered intermediate budget-window confirmation remain negative. Missing/partial raw source/future ZIPs fail full admission; original t400 alleles, parentage receipts, future artifact SHA-256 and history-level unit counts were checked before each scientific readout. No selective resampling of an exposed visitor history was permitted.

## Results

### 1. Order effects were small and not specific to geographic visitor history

The original assigned-expression-order near/far difference-in-differences passed the preregistered **practical-equivalence** bound ±0.05. The independently predeclared 3/4-ovule-budget-window follow-up **failed**. Thus the original prediction of a distinctive far-environment or resource-window rescue effect was not supported. A small absolute A-first-minus-I-first occupancy advantage still appeared in some bottlenecked conditions, but this is not a universal precedence effect and is not the original positive primary.

### 2. A controlled selfed-seed intervention changed the small schedule advantage

In an eight-founder/capacity-eight stress regime, a predeclared postzygotic intervention halving viable selfed-seed contribution reduced the A-first-minus-I-first occupancy difference from **+0.01209** at baseline to **+0.00394**. Sensitivity was **+0.008145**, 95% history-bootstrap **[+0.003708,+0.012773]**, satisfying its original frozen threshold. A matched outcross-seed viability contrast did not resolve a nonzero effect. The postzygotic manipulation identifies a **controlled response to viable selfed seeds**, not natural genetic mediation.

### 3. The first capacity contrasts were either confounded or inconclusive

Comparing F8/K8 with a full-founding-population/K48 regime suggested a positive moderator, but that was **post-outcome exploratory** and simultaneously changed founding abundance, genomic sampling, demographic K and the pollen-delivery denominator. A new independently sampled matched-founder experiment changed K8 to K48 with eight founder genomes held fixed. Its registered primary sensitivity contrast was **+0.001848**, 95% **[−0.003458,+0.007337]**, **inconclusive**. A full subsequent two-lever experiment separated K and B; its **preregistered primary** B8 versus B48 at fixed K8 was **−0.001753**, 95% **[−0.006334,+0.002872]**, also **inconclusive**. Its K effect at fixed B48 was positive, but remained **secondary/descriptive** and motivated the next study.

### 4. An independent predeclared test supported demographic K moderation at fixed B48

With fresh visitor histories, matched founding genotypes and an explicit constant pollen-background denominator, the registered K8–K48 contrast was:

| Registered fixed-B48 quantity | Occupancy effect | 95% paired history bootstrap |
|---|---:|---:|
| `tau(K8,B48)` | +0.009977 | [+0.006340,+0.013613] |
| `tau(K48,B48)` | +0.002231 | [−0.001599,+0.006151] |
| **Primary: K8 minus K48** | **+0.007746** | **[+0.002497,+0.013015]** |

The registered mean exceeds 0.005 and the entire interval is positive; **43 of 64 history clusters** contributed positive contrasts. Its machine verdict is `supported_controlled_demographic_K_moderation_at_fixed_B48`. This is **about 0.775 occupancy percentage points** of interaction sensitivity, not the overall effect of K on persistence.

Two other **independently generated** 64-history cohorts had directionally concordant estimates of this same full-period contrast: **+0.013430** (four-arm K×B cohort) and **+0.008580** (timed-viability cohort). Both were *secondary descriptive* measures selected in experiments with **different registered primaries**. Across the three original JSONs the unweighted numerical mean **+0.009919** is **descriptive only**; no pooled interval, formal equivalence or threefold confirmatory success is claimed. See `docs/CHAPTER2_K_B48_THREE_COHORT_EVIDENCE_COMPARISON_20261010.md` and Figure 1.

### 5. A later prospective timing contrast did not resolve early versus late importance

After exploratory extinction-time diagnostics suggested later response, an independent **four-gate** experiment used another unused 64 histories and 229,376 futures. Selfed viable seeds were halved during updates **0–39**, **40–79**, or **0–79**, with an unchanged baseline. Its registered primary, the **difference between late-only and early-only K moderation**, was **−0.002965**, history-bootstrap **[−0.007263,+0.001317]**: **inconclusive**, neither nonzero support nor practical equivalence. The full-period K contrast (+0.008580) is a *descriptive secondary*, not a successful test of the timing hypothesis. Different interval crossings for early and late alone cannot identify when the causal mechanism acts.

## Discussion

The main mechanism resolved here is **conditional rather than universal**. A finite-population demographic parameter changes how the advantage of an experimentally ordered reproductive expression history responds to removal of viable selfed offspring, even when the recipient pollen-background normalizer is held fixed. The direct reproduction-ledger separation matters because the unmodified model mistakenly makes a capacity manipulation change pollen availability as well as density limitation. Isolating B did not remove the K effect in the new registered study.

Neither the supported K interaction nor its descriptive cohort concordance demonstrates that more cumulative selfed recruits *mediate* local persistence. Recruitment totals are accrued over trajectories that may end at different times. The fully archived exploratory channel audit also found that the 60-update extinction signature appeared stronger than the 20-update signature, but the independently registered early-versus-late test **did not support preferential timing**. We must not infer temporal onset from juxtaposed marginal intervals.

The results also do **not** establish a general law that evolving selfing first rescues island populations. `A-first` and `I-first` are assigned schedules of *phenotype expression* at equal prescribed exposure, whereas the natural genetic sequence of inherited mutations remains stochastic and unmanipulated. The outcome is **binary occupancy after a finite horizon** under strong stress, not individual lifetime reproductive fitness, landscape colonization, or field-calibrated extinction. Demographic K and pollen dilution B are mathematical controls in a single model family, not measured island area and flower-resource background. Accordingly, replication across visitor histories **within** that model does not demonstrate external validity across natural island plant systems.

This mechanistic companion should remain **separate** from the four-setting floral-investment paper intended for *Ecology Letters*: that paper asks whether reproductive assurance must evolve for pollinator-limitation-driven investment decline and why assurance evolution compresses near–far divergence. The stressed demographic experiments have different outcomes, interventions and inference targets; do not turn them into a downstream mediation claim in the main paper.

## Data and reproducibility

The source of truth is the **four separate original, exact-byte machine readouts** and full run artifacts cited in:

- `docs/CHAPTER2_PERSISTENCE_CAPACITY_COMPANION_POSITION_20261009.md`
- `docs/CHAPTER2_K_B48_THREE_COHORT_EVIDENCE_COMPARISON_20261010.md`
- `docs/CHAPTER2_INDEPENDENT_RAW_ARCHIVES_20261009.md`

All four original-cohort raw genomes, pedigrees and future outcome shard ZIP archives (**521 original ZIPs**) have been SHA-verified and backed up in **unpublished GitHub draft Releases**, not a public DOI deposit. The original Actions artifacts are time-limited; external DOI-backed deposit, licensing/access decision and independent external re-download validation remain **open under Issue #436**. The current source-backed JSON and plotted original confidence intervals do not substitute for access to these complete raw biological-model archives.

## Submission claim firewall

**Admissible headline:** *Within a stochastic genetically explicit model, demographic capacity at fixed pollen-background dilution moderates the selfed-seed-viability dependence of a randomized reproductive expression-history occupancy contrast.*

**Not admissible:** *Evolution of selfing first rescues real island plants*, *demographic capacity establishes a universal extinction threshold*, *three independent confirmatory replications*, or *the early-versus-late viability mechanism is proven*.

**Editorial state:** standalone companion manuscript draft, not a submitted or peer-reviewed publication; no new analysis or claims of empirical validation are implied.
