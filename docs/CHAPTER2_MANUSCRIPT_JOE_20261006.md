# Reproductive assurance can precede reduced floral attraction without causing it under pollinator isolation



## Abstract

1. Pollinator limitation can favour both reproductive assurance and reduced floral attraction, but an observed evolutionary sequence does not establish that the first change causes the second. We tested whether temporal order and causal necessity can be separated in one explicit plant–pollinator model of visitor replenishment, pollen transfer, mating, inheritance and finite population dynamics.

2. We combined three contrasts. Fixed-plant assays measured the reproductive return to floral investment before plant evolution. Maintained-isolation simulations measured whether reproductive assurance or floral investment first crossed a predeclared sustained-change threshold. A matched intervention then fixed assurance capacity at 0.5 to test whether assurance evolution was required for investment decline. The temporal and intervention results were independently replicated under a prospectively frozen design using 64 new visitor histories and eight nested demographic repeats.

3. In the focal delayed-selfing, assurance-cost setting, stronger visitor limitation reversed the marginal reproductive contribution of floral investment from +0.5793 to −0.7004 at the same plant state as the outcross component fell from +1.6523 to +0.0854. In both discovery and confirmation, assurance changed first in 51/64 histories at the primary threshold; the confirmatory assurance-first proportion was 0.797 (95% history-bootstrap 0.688–0.891).

4. Blocking assurance evolution did not prevent investment decline. In the independent confirmation, fixed-assurance far populations changed investment by −0.3060 [−0.3181, −0.2941], and the far-minus-near contrast was −0.4354 [−0.4533, −0.4172]. The sequence was not universal: under prior selfing with positive mutation, only 30/64 histories were assurance-first at the same threshold.

5. **Synthesis.** Temporal precedence is not causal necessity. Under the declared delayed-selfing conditions, pollinator isolation can lower the reproductive return to attraction directly while reproductive assurance and attraction evolve as interacting but partly parallel responses. The result is a bounded mechanism, not a universal selfing-syndrome sequence or a calibrated reconstruction of natural island history.



## Keywords

autonomous selfing; floral evolution; island ecology; plant–pollinator interactions; pollen limitation; reproductive assurance; reproductive allocation; visitor replenishment



# Introduction

Pollinator-community change does not act on floral traits directly. Its effects are transmitted through a sequence of ecological processes: visitors differ in functional fit and effectiveness, those differences alter pollen transfer and mating opportunity, reproductive success determines which alleles enter the next generation, and demographic persistence determines whether an evolutionary response can be realized at all. A contemporary pollinator assemblage and a contemporary flower phenotype are therefore separated by several biological stages.

Island plant–pollinator systems are a natural setting in which to examine this sequence. A worldwide network comparison found simpler oceanic-island networks and an association between isolation and network size (Traveset et al., 2016). Self-compatibility is overrepresented among island species in three studied plant families, consistent with a colonization filter (Grossenbacher et al., 2017). Yet a Pacific sister-taxon comparison found no overall reduction in flower size, with differences among islands and families (Hetherington-Rauth & Johnson, 2020). Coastal island comparisons further link visitor functional composition to niche shifts, trait matching and pollination function (Hiraiwa & Ushimaru, 2017, 2024). These studies motivate separating ecological filtering, interaction function and within-population evolution rather than treating them as interchangeable evidence for one pathway.

A central inferential difficulty is identifying where that non-uniformity enters. Opposite floral responses could arise immediately because the same visitor community has different reproductive value for plants starting from different functional states. Alternatively, a common selection direction could be modified during inheritance, demographic sampling, loss of variation or extinction. Reproductive assurance can further preserve populations during poor pollination without necessarily determining which pollinator-facing phenotype is favoured. These alternatives imply different interpretations of an island syndrome: repeated function need not mean repeated form.

We address this problem with one shared biological model rather than separate response rules. Plants carry inherited access/matching, floral-investment and assurance traits. Visitor functional types determine finite compatible pollen transfer; outcrossing and the declared prior- or delayed-selfing rule produce offspring with explicit viability; maternal and paternal contributions undergo Mendelian inheritance; and recruitment, adult survival, immigration and finite population size determine which inherited responses persist. This model is ecologically explicit in causal structure but is not calibrated to a named island, flower colour, corolla dimension, visitor species, kilometre distance or natural evolutionary rate.

The shared reproductive process is examined with complementary assays and evolutionary calculations. Fixed-state assays measure the reproductive consequences of changing investment before plant evolution. Deterministic genotype-density propagation and the finite-individual model then follow reproduction and inheritance in parallel; the latter samples parental contributions, Mendelian segregation and recruitment. The deterministic calculation is a conditional deterministic closure, not the stochastic mean of the finite ABM. Mutation diffusion approximates mutation within the deterministic branch while sexual inheritance remains explicit. Assurance, connectivity and history experiments intervene on this common biology rather than prescribing separate directions of floral response.

The critical inferential distinction is between **what changes first** and
**what change is required for another response**. A sequential selfing syndrome
would predict that reproductive assurance precedes and helps generate reduced
attraction. But visitor limitation could instead alter the return on attraction
directly, so that assurance and investment respond to the same ecological change
without forming a single serial pathway.

We therefore organize the paper around three linked contrasts. Fixed-plant
assays identify whether isolation changes the reproductive return to investment
before plant evolution. Maintained-isolation trajectories quantify the realized
order of assurance and investment change. A matched fixed-versus-evolving
assurance intervention then tests causal necessity. Reproductive-output assays
separate pollen-deficit metrics from viable offspring, and genetic/deterministic
comparisons bound how expected responses are realized in finite populations.

At an identical plant state, stronger visitor limitation can reverse the
marginal reproductive return to attraction. Reproductive assurance often reaches
a declared evolutionary threshold first, but preventing assurance evolution does
not remove investment decline. The observed sequence is therefore real but does
not identify a selfing-mediated causal chain.

A second, less intuitive **exploratory** result follows from the original
intervention: allowing assurance to evolve can reduce the near-far investment
contrast because investment changes in both environments. This interaction was
not included in the independent confirmatory campaign. It therefore motivates,
rather than establishes, the idea that weak geographic divergence can coexist
with substantial evolution within each environment. This is why the manuscript
reports within-population change and between-environment divergence as separate
estimands.



# Materials and Methods

The primary analysis maintains isolation throughout the evolutionary trajectory and uses explicit mechanism interventions on one plant–pollinator model. Fixed-state selection assays, deterministic propagation and finite-population evolution answer complementary questions. No empirical island outcome was used to tune the model or select the direction of any contrast. Trait values, time, distance and demographic frequencies are synthetic coordinates rather than calibrated natural estimates.

## Visitor replenishment and plant population size

The mechanistic control variable is expected successful visitor establishment per reproductive update. In the primary exponential-arrival model, lambda = supply x establishment x exp(-distance/scale) = 0.24 exp(-distance). The same completed 13-distance diagnostic can therefore be displayed on a continuous replenishment-rate axis, approximately 0.01195 to 0.24, without recalculating or changing any outcome. It represents new visitor functional types, not visitation events or visitor abundance. Realized arrival counts remain discrete and stochastic, and type disappearance continues at the same hazard.

Plant capacity is a separate model condition. Capacity 48 does not correspond to a declared island area; the ABM represents finite plants and their inheritance rather than island geometry. The primary contrast isolates visitor replenishment at fixed plant capacity and no plant immigration. Population-size comparisons belong to separate, explicitly labelled experiments. The model has a common external source, not inter-island stepping-stone dispersal. Its relevance to islands is the mechanism of replenishment limitation; the model does not claim to recreate every physical consequence of island size or geography.

The primary experiment starts an established plant population and prevents plant immigration. It therefore investigates within-population evolutionary response to ongoing visitor supply, not filtering among plant species during island colonization. Self-compatibility in comparative floras, autonomous capacity in the model, and the realized fraction of selfed offspring are different quantities. Their possible association motivates Q1–Q2 comparison but does not make the model a direct causal explanation of assemblage-level patterns.

## Primary experiments and causal contrasts

| Question | Experiment | Held fixed / varied | Interpretation |
|---|---|---|---|
| Does visitor limitation change investment returns? | 768 fixed-plant assays | Same 48 plants and capacity 0.5; near/far visitor exposures at indices 0,200,400 | Local reproductive contribution derivative, before plant evolution; visitor composition and amount vary together |
| Which response appears first? | Sustained isolation for 1,000 updates |64 paired visitor histories, eight demographic repeats, both reproductive settings and declared mutation rates | Within-population threshold timing and additional far-minus-near timing reported separately |
| Is capacity evolution necessary? |8,192 matched fixed/evolving-capacity trajectories | Same capacity 0.5 founders without capacity standing variation; permit or block its evolution | Tests necessity of capacity evolution in this cohort; realized selfing remains responsive |
| Does assurance compensate pollen shortage? |12,288 evolved-state supplementation assays | Same sampled plants under natural versus saturating outcross pollen | Raw and viable deficits, retaining selfing timing and inbreeding depression |
| Does a lower deficit mean greater reproduction? |6,912 capacity-by-investment manipulations | Same visitor environment; investment and capacity each 0.25,0.5,0.75 | Whole-population trait intervention, distinct from a focal-mutant gradient |
| What does population finiteness change? | Parallel ABM and deterministic calculations | Shared reproduction, inheritance and visitor exposure | Positive-mutation high-resolution extension stopped; numerical fidelity unresolved |

The maintained-isolation experiment starts 48 plants and four visitor types, uses full generation replacement and no plant immigration, and allows three inherited traits to vary. Stronger isolation reduces continuing visitor arrival; per-type disappearance hazard is unchanged. Delayed selfing with capacity cost 0.5 and prior selfing with no capacity cost both use inbreeding depression 0.5. Consequently, their contrast cannot isolate the timing effect from its associated cost. The main cohort retains capacity standing variation; the capacity intervention deliberately does not. These cohorts must not be pooled as equivalent replicates.

Temporal events use a declared 0.05 change sustained for 20 updates, with crossings within five updates treated as near-simultaneous; thresholds 0.025 and 0.1 are sensitivity analyses. Unreached events are censored. Counts refer to history means over demographic repeats. Equal changes on abstract axes are not assumed to have equivalent natural biological magnitude. Estimates and descriptive intervals preserve the independent visitor-history unit, and extinction is reported separately rather than represented as a zero trait value.

Natural evidence enters only after the synthetic objects and claim boundaries are defined. The confrontation layer combines a formal source audit of 25 research entries across 21 exact geographic labels, a broader source-verified descriptive programme that reached its geography-first stopping rule, source-native secondary reanalyses of compositional change, and existing Izu functional-network / pollen secondary analyses. The formal audit records whether each system directly observes comparable plant response, partner loss or arrival/replacement, realized community change and other mechanism-relevant coordinates without imputing missing axes from outcomes. The broader programme is used to assess biological vocabulary and search saturation, not to estimate natural prevalence.

The Izu secondary-data stress test is likewise deliberately asymmetric. We retain support when functional exposure predicts corrected trait matching, but also retain instability or failure when matching-to-pollen effects are not leave-one-island sign stable, historical signed-position projections fail null correction, or a bridge-state geographic contrast is not independently identified. The natural layer therefore constrains interpretation rather than selecting synthetic parameters.

The natural evidence is therefore a confrontation layer rather than a calibration layer. A future same-unit transition-linked study could directly test the full ecological chain, but current cross-sectional evidence cannot retrospectively identify the historical mechanism that generated a named island phenotype.

After the 2026-10-05 sequence and fixed-assurance results were known, but before
any confirmatory outcomes were generated, we froze an independent replication
design. Discovery visitor histories 76001–76064 and demographic repeats
7101–7108 were not reused. The confirmation used 64 new visitor histories
26100601–26100664 and eight new demographic repeats 26101601–26101608 while
retaining the original founder specification and biological model.

The confirmation contained 4,096 finite-population trajectories. The temporal
component used 2,048 far-arm trajectories crossing two reproductive settings
(delayed selfing with assurance cost 0.5; prior selfing with assurance cost 0),
two mutation probabilities (0 and 0.01), 64 visitor histories and eight nested
demographic repeats. The causal-necessity component used 2,048 trajectories with
assurance capacity fixed at 0.5, crossing the two reproductive settings, positive
mutation, near/far visitor exposure, 64 histories and eight repeats.

The preregistered primary cell was delayed selfing, assurance cost 0.5 and
mutation probability 0.01. For temporal order, the primary definition was a
0.05 founder-relative change sustained for 20 updates; crossings within five
updates were classed as near-simultaneous. Assurance-first success required the
proportion across all 64 independent histories to exceed 0.50 and the lower
bound of a 95% visitor-history bootstrap interval to exceed 0.50.
Near-simultaneous, investment-first and censored histories therefore counted as
not assurance-first in the primary binary proportion. Thresholds 0.025 and 0.10
were frozen sensitivity analyses.

For the fixed-assurance intervention, confirmation required both the far
investment change from founders and the far-minus-near investment contrast at
update 1,000 to be negative, with both 95% visitor-history bootstrap upper
bounds below zero. Each near/far arm also had to retain at least 90% occupancy,
and at least 60 of 64 histories had to remain estimable. Failure of this
admissibility rule was defined as inconclusive rather than successful.

All four setting-by-mutation temporal cells were reported regardless of
direction, but secondary cells could not rescue or overturn the primary
adjudication. No seed extension, threshold retuning, tie-window change, outcome
substitution or biological parameter adjustment was allowed after execution
began. Eight demographic repeats were nested within visitor histories and did
not increase the independent ecological denominator beyond 64.

## Fixed-plant reproductive-return assay

Local reproductive return was evaluated before plant evolution by holding the resident plant state and pollen environment fixed and perturbing floral investment at an interior resident state. The fitness accounting includes one half of maternal outcross production, one half of paternal outcross success and the full viable selfed contribution. We report the derivative of total reproductive contribution with respect to investment together with its outcross and viable-selfed components. Finite differences of independently calculated mutant fitness verified the derivative calculation. This assay diagnoses the immediate reproductive value of attraction under a given visitor environment; it is not an evolutionary trajectory and does not isolate visitor abundance from visitor composition.

## Reproduction and inheritance

The model represents a focal plant population embedded in an externally supported visitor environment. Plants carry additive diploid loci for an abstract access/matching trait and floral investment, with reproductive assurance fixed or inherited depending on the declared experiment. Visitor functional types determine finite compatible pollen delivery. Outcrossing contributes maternal and paternal gametes; delayed selfing can fertilize remaining ovules; inbreeding depression reduces viable selfed offspring; and Mendelian inheritance precedes recruitment, density regulation and adult survival. No rule directly moves a floral trait toward an environmental optimum or toward the best visitor.

The earlier complementary island campaign crossed predeclared families for visitor-history transport, fixed-state reproductive assays, reproductive assurance, seed and pollinator connectivity, founding state, trait-grid representation, population scaling, life history, disturbance chronology and recovery. That campaign contains 19,968 audited cases across 80 production cells plus six held-out transport rows. It is a distinct cohort from the current sustained-isolation experiments above. All cases passed state/receipt audit and 80 predeclared deterministic replay checks. Extinct endpoints remained undefined rather than coded as zero.

Model3 is interpreted at a bounded level. The code's reproductive-year label denotes a reproductive update, not a calibrated calendar year. Distances are standardized dispersal coordinates rather than kilometres, visitors are functional types, and investment is not calibrated to flower colour, size or nectar guides. Numerical resolution and approximation are separate from biological uncertainty. Unadmitted positive-mutation deterministic results cannot be promoted as ecological evidence merely because their qualitative directions look plausible.



# Results

## Visitor limitation lowers the return on attraction before plant traits evolve

At the same fixed plant state and assurance capacity 0.5, the visitor environment
changed the marginal reproductive contribution of floral investment. In the
delayed-selfing setting at snapshot 400, the mean investment contribution
derivative was +0.5793 under near exposure and -0.7004 under far exposure. The
outcross component declined from +1.6523 to +0.0854, while the viable-selfed
component partly offset rather than generated that decline. The intrinsic
investment-cost coefficient was unchanged.

## Reproductive assurance often changes first under sustained isolation

The maintained-isolation cohort followed 64 visitor histories with eight nested
demographic repeats for 1,000 updates. In the delayed-selfing, assurance-cost 0.5
setting with mutation 0.01, assurance crossed the declared 0.05 sustained-change
threshold before investment in 51/64 far-history means; the other 13 were within
five updates. Under prior selfing with zero assurance cost, assurance was first
in 38/64 histories and 26 were near-simultaneous.

This temporal result was then tested prospectively with 64 new visitor histories
and eight new demographic repeats, using the same frozen 0.05 threshold,
20-update persistence rule and five-update tie window. The delayed/costly,
positive-mutation cell again produced **51/64 assurance-first histories** and
13 near-simultaneous histories; the assurance-first proportion was 0.7969 with
a 95% visitor-history bootstrap interval of **0.6875–0.8906**. The declared
success criterion therefore passed. The direction also persisted at the two
predeclared sensitivity thresholds: 48/64 assurance-first at 0.025 and 59/64 at
0.10.

The ordering is not universal across reproductive settings. In the independent
positive-mutation prior-selfing cell, the primary 0.05 threshold gave
30/64 assurance-first and 34/64 near-simultaneous histories
(95% interval for the assurance-first proportion 0.3438–0.5938). The confirmed
sequence claim is therefore restricted to the delayed-selfing, assurance-cost
setting.

Founder-relative order did not equal the order of additional isolation
divergence. In the delayed setting, far-minus-near investment divergence crossed
first in 32 histories, assurance divergence in 10, 20 were near-simultaneous and
two reached only the investment threshold.

## Assurance evolution is not required for investment decline

The matched fixed-versus-evolving-assurance experiment completed 8,192
trajectories. With assurance held fixed at 0.5, far populations still reduced
investment by 0.3099 (descriptive 95% interval 0.2972–0.3220) under delayed
selfing and by 0.3316 (0.3217–0.3411) under prior selfing. Thus an
assurance-first sequence does not establish that assurance evolution is required
for attraction investment to decline.

The preregistered new-history replication independently confirmed this
intervention result. With assurance fixed at 0.5 in the delayed/costly cell,
far investment change was **−0.3060 [−0.3181, −0.2941]** and far-minus-near
investment was **−0.4354 [−0.4533, −0.4172]**; all 64 histories were eligible
and both arms had 100% terminal occupancy. The frozen criterion required both
means and both upper interval bounds to remain below zero, and it passed. The
secondary prior-selfing cell also remained negative
(−0.3316 [−0.3418, −0.3210] from founders; far-minus-near
−0.3094 [−0.3246, −0.2942]).

In the original cohort, an exploratory secondary interaction indicated that allowing assurance to evolve could also narrow the near-far investment contrast.
The four-cell interaction was +0.08468 (0.06782–0.10265) in the delayed setting
and +0.24505 (0.22523–0.26543) under prior selfing. Both environments can evolve
substantially while their difference becomes smaller.

## Lower pollen deficit does not necessarily mean greater viable reproduction

In the delayed/far whole-population intervention at snapshot 400, increasing
investment from 0.25 to 0.75 at assurance capacity 0.5 reduced the fractional
viable pollen deficit by 0.0104 but reduced viable maternal offspring by 15.72
per 48 plants. Pollen shortage, compensation and absolute viable offspring are
therefore not interchangeable readouts.

The earlier bridge and common-environment mutation diagnostics remain
complementary evidence on genetic realization and history dependence; they do
not define the primary paper question.



# Discussion

Reproductive assurance often changed first, but the fixed-capacity intervention
shows that its evolution was not required for floral investment to decline.
Crucially, both components were independently reproduced under a prospectively
frozen design with new visitor histories and new demographic repeats. The
delayed/costly positive-mutation cell repeated the original 51/64
assurance-first count (95% history-bootstrap 0.6875–0.8906), while the fixed-
assurance far investment response remained negative with its entire interval
below zero. This separates two questions that are easily conflated in
island-syndrome arguments: **which trait changes first** and **which trait change
causes another**. Temporal precedence alone cannot answer the second.

The confirmation is setting-specific rather than universal. Prior selfing with
positive mutation produced 30/64 assurance-first histories at the same primary
threshold, with an interval spanning 0.5. We therefore interpret the confirmed
sequence as a property of the delayed-selfing, costly-assurance regime rather
than a general law of selfing-syndrome evolution.

The fixed-plant return assay provides the upstream explanation. At an identical
plant state, stronger visitor limitation sharply reduced the outcross return on
additional attraction and reversed the total investment contribution derivative
in the delayed setting. The selfed component partly buffered this decline rather
than creating it. Isolation can therefore act directly on the reproductive
economics of attraction before assurance evolves.

Allowing assurance to evolve then modifies, rather than simply initiates, that
response. The positive interaction in the fixed-versus-evolving experiment means
assurance evolution can narrow the observed near-far investment contrast because
investment changes in both environments. Consequently, weak geographic
divergence is not evidence of weak evolution. Within-population change and
between-environment divergence must be reported separately.

Selfing-first itself is not a new general hypothesis. Experimental evolution in
*Mimulus* explicitly favored a sequential selfing-syndrome model in which traits
that improve reproductive assurance can change before traits such as flower size
(Bodbyl Roels & Kelly, 2011). Experimental evolution with bumblebees versus
hoverflies has also shown joint divergence of floral signals and autonomous
self-pollination (Gervasi & Schiestl, 2017), while attraction-allocation theory
predates both experiments (Sakai, 1995). The contribution here is therefore not
the existence of a sequence, but the combination of an explicit
island-replenishment process, measured temporal order, and a separate
intervention showing that the observed sequence is not a necessary causal chain.

The pollen-deficit result has a similarly bounded novelty. Reviews of pollen
limitation already emphasize that supplementation responses depend on ecological
context and do not by themselves identify demographic consequence (Ashman et
al., 2004; Knight et al., 2005). Quantitative synthesis further shows that
response variable and resource reallocation can change the estimated magnitude
of pollen limitation (Knight et al., 2006). In an empirical New Zealand tree,
high pollen limitation, selfing and inbreeding depression jointly caused seed
production to overstate effective viable offspring (Van Etten et al., 2015).
Our result is therefore used as a model-level reproductive consequence of the
same allocation process, not as the first demonstration that pollen limitation
and fitness can differ.

## Ecological interpretation

The central result is not simply that island responses are context dependent. The model identifies where context enters the ecological pathway from pollination to evolution. Functional matching can reverse the marginal reproductive return to floral investment before inheritance or demographic updating. That potential response then passes through Mendelian inheritance, and only afterward through finite recruitment, loss of variation, extinction and immigration. What is favoured reproductively, what the deterministic closure predicts, and what is realized in a finite population are therefore different biological objects.

This distinction matters because the three stages did not give interchangeable answers. Controlled visitor compositions generated opposite fixed-state reproductive-return slopes among starting plant states, showing that demographic stochasticity is not required for response non-uniformity. Yet isolation-driven visitor assembly produced a one-directional deterministic inherited response across all 128 visitor histories. Finite populations then reintroduced realized sign heterogeneity in some histories. A system can therefore possess state-dependent evolutionary capacity without expressing that capacity under every ecological regime.

## Reproductive assurance and persistence

Reproductive assurance had its clearest effect on persistence. Under the severe visitor-absence treatment, populations without assurance had no terminal survivors, whereas assurance-present populations persisted. Yet assurance did not impose a common floral endpoint. Its ecological role is therefore better described as insurance that keeps an evolutionary trajectory available than as a rule that directly specifies floral form.

This distinction sharpens how breeding-system change should be interpreted in island plants. Autonomous reproduction can buffer demographic failure while pollinator-mediated selection on access or floral investment continues through a partially separate route. A repeated association between isolation and assurance therefore need not imply a serial pathway in which selfing alone determines subsequent floral simplification. In the model, persistence and pollinator-facing evolution can be coupled without being identical.

## Empirical transport

The model identifies a transition that current island comparisons rarely observe on the same populations: visitor exposure changing through time, its effect on pollen transfer and mating, and the subsequent inherited floral response. Cross-sectional morphology alone therefore cannot identify whether reproductive assurance preceded, mediated or merely accompanied attraction change.

A decisive empirical test would follow the same populations through a pollinator transition while measuring functional visitor exposure, effective pollen transfer, mating route, reproductive output and inherited floral change. That design would test whether the sequence-versus-necessity distinction transports to nature without assigning existing islands to synthetic model cells.

## Ecological validity and limits

Parameter uncertainty is distinct from repeat-to-repeat stochasticity. The primary 64-history, eight-repeat design estimates the latter conditional on synthetic settings; it does not establish robustness to alternative reproductive costs, inbreeding depression, genetic architecture or arrival functions. The two primary reproductive settings jointly change selfing timing and capacity cost. Mutation rates 0 and 0.01 and alternative temporal thresholds reveal substantial changes in effect magnitude and classified order. The replenishment extension supplies trajectories across 13 arrival rates at fixed remaining parameters; the reciprocal and cost/depression grid broadens local selection coverage but does not supply evolutionary trajectories over all those parameter combinations. Consequently, the ecological result is conditional process decomposition, not a universal claim that selfing initiates before investment decline. Detailed coverage and unresolved sensitivities are recorded in MODEL3_ASSUMPTION_SENSITIVITY_SCOPE_20261005.md.

The model is ecologically explicit but not system calibrated. Its strengths come from preserving the causal order of pollination, mating, inheritance and demography, from separating seed and pollinator connectivity, and from keeping extinction distinct from trait change. Its limitations are equally important. Visitor types are functional agents rather than measured species abundances; background flora supports visitors rather than being coevolved explicitly; floral investment and access are abstract traits rather than named colours, corolla dimensions or nectar guides; inbreeding depression is fixed rather than dynamically purged; and time and distance are model coordinates rather than years and kilometres for a particular archipelago.

These limitations define the inference. The model can identify which ecological processes are sufficient to change selection, expected inherited response and finite-population realization. It cannot estimate natural evolutionary rates, reconstruct a named historical island transition or predict the exact floral phenotype expected in a given region. The useful generalization is therefore structural: ecological function can be more repeatable than phenotypic form because the pathway from pollination to realized evolution contains multiple biologically distinct filters.



# Conclusion

Under sustained visitor replenishment limitation, reproductive assurance can
reach a declared evolutionary threshold before floral investment, yet assurance
evolution is not required for investment decline. Both components of this claim
passed a prospectively frozen replication using entirely new visitor histories
and demographic repeats. The confirmed temporal result is restricted to the
delayed-selfing, costly-assurance setting; it is not universal across the
alternative reproductive setting.

The upstream reason is ecological: at the same plant state, stronger isolation
reduces the reproductive return to attraction before the traits themselves
evolve. This makes the central result **sequence ≠ necessity**. Assurance and
attraction are interacting responses to a shared change in reproductive
economics, not a single obligatory serial pathway. Allowing assurance to evolve
can even reduce the near-far investment contrast because both environments
evolve, so geographic effect size and evolutionary amount are not
interchangeable.

The reproductive consequence is similarly non-equivalent across readouts:
slightly lower fractional pollen deficit can coexist with fewer viable offspring.
The mutation/history and finite-versus-deterministic analyses remain supporting
evidence on genetic accessibility and realization, not the paper spine. The
model establishes conditional mechanisms, not calibrated natural rates or a
historical reconstruction of any named island system.



# Figure captions

**Figure 1. Visitor limitation reduces the reproductive return to attraction.** At the same fixed plant state and assurance capacity 0.5, near and far visitor exposures are compared for outcross, viable-selfed and total contribution slopes. In the delayed setting at snapshot 400, total investment contribution changes from +0.5793 to −0.7004 as the outcross component falls from +1.6523 to +0.0854; the viable-selfed component partly offsets that decline. Points are means across 64 paired visitor histories; the interval is for the paired far-minus-near difference. These are reproductive-return diagnostics before plant evolution.

**Figure 2. Sequence and necessity are different questions.** Panel A shows discovery and prospectively frozen confirmation of history-level crossing order. In the primary delayed/costly positive-mutation cell, assurance is first in 51/64 histories in both cohorts; the confirmatory 95% history-bootstrap interval is 0.6875–0.8906. The prior-selfing positive-mutation cell is shown as a scope boundary. Panel B shows the fixed-assurance intervention. In the independent replication, far investment change is −0.3060 [−0.3181, −0.2941] and far-minus-near investment is −0.4354 [−0.4533, −0.4172]. Fixed assurance blocks assurance evolution but does not remove realized selfing.

**Figure 3. Lower pollen deficit need not mean greater viable reproduction.** For both reproductive settings and near/far visitor exposure, the whole-population investment intervention compares change in fractional viable pollen deficit with change in viable maternal offspring. In the delayed/far comparison, increasing investment from 0.25 to 0.75 at assurance capacity 0.5 reduces the fractional viable deficit by 0.0104 while reducing viable maternal offspring by 15.72 per 48 plants. These are fixed-trait reproductive assays, not evolutionary trajectories.

Detailed replenishment gradients, local-selection surfaces, reciprocal-selection parameter sweeps, finite-versus-deterministic comparisons, mutation/history experiments, repeatability analyses and the natural-island evidence ledger are assigned to Supporting Information.



# References

Grossenbacher, D.L., Brandvain, Y., Auld, J.R., Burd, M., Cheptou, P.-O., Conner, J.K., Grant, A.G., Hovick, S.M., Pannell, J.R., Pauw, A., Petanidou, T., Randle, A.M., Rubio de Casas, R., Vamosi, J.C., Winn, A.A., Igić, B., Busch, J.W., Kalisz, S. & Goldberg, E.E. (2017). Self-compatibility is over-represented on islands. *New Phytologist*, 215, 469–478. https://doi.org/10.1111/nph.14534

Hetherington-Rauth, M.C. & Johnson, M.T.J. (2020). Floral trait evolution of angiosperms on Pacific islands. *The American Naturalist*, 196, 87–100. https://doi.org/10.1086/709018

Hiraiwa, M.K. & Ushimaru, A. (2017). Low functional diversity promotes niche changes in natural island pollinator communities. *Proceedings of the Royal Society B*, 284, 20162218. https://doi.org/10.1098/rspb.2016.2218

Hiraiwa, M.K. & Ushimaru, A. (2024). Loss of functional diversity rather than species diversity of pollinators decreases community-wide trait matching and pollination function. *Functional Ecology*, 38, 1296–1308. https://doi.org/10.1111/1365-2435.14527

Traveset, A., Tur, C., Trøjelsgaard, K., Heleno, R., Castro-Urgal, R. & Olesen, J.M. (2016). Global patterns of mainland and insular pollination networks. *Global Ecology and Biogeography*, 25, 880–890. https://doi.org/10.1111/geb.12362

Bodbyl Roels, S. A., & Kelly, J. K. (2011). Rapid evolution caused by pollinator loss in *Mimulus guttatus*. *Evolution*, **65**(9), 2541–2552. [DOI: 10.1111/j.1558-5646.2011.01326.x](https://doi.org/10.1111/j.1558-5646.2011.01326.x).


Gervasi, D.D.L. & Schiestl, F.P. (2017). Real-time divergent evolution in plants driven by pollinators. *Nature Communications*, 8, 14691. https://doi.org/10.1038/ncomms14691

Ashman, T.-L., Knight, T.M., Steets, J.A., Amarasekare, P., Burd, M., Campbell, D.R., Dudash, M.R., Johnston, M.O., Mazer, S.J., Mitchell, R.J., Morgan, M.T. & Wilson, W.G. (2004). Pollen limitation of plant reproduction: ecological and evolutionary causes and consequences. *Ecology*, 85, 2408–2421. https://doi.org/10.1890/03-8024

Knight, T.M., Steets, J.A., Vamosi, J.C., Mazer, S.J., Burd, M., Campbell, D.R., Dudash, M.R., Johnston, M.O., Mitchell, R.J. & Ashman, T.-L. (2005). Pollen limitation of plant reproduction: pattern and process. *Annual Review of Ecology, Evolution, and Systematics*, 36, 467–497. https://doi.org/10.1146/annurev.ecolsys.36.102403.115320

Knight, T.M., Steets, J.A. & Ashman, T.-L. (2006). A quantitative synthesis of pollen supplementation experiments highlights the contribution of resource reallocation to estimates of pollen limitation. *American Journal of Botany*, 93, 271–277. https://doi.org/10.3732/ajb.93.2.271

Van Etten, M.L., Tate, J.A., Anderson, S.H., Kelly, D., Ladley, J.J. & Merrett, M.F. (2015). The compounding effects of high pollen limitation, selfing rates and inbreeding depression leave a New Zealand tree with few viable offspring. *Annals of Botany*, 116, 409–418. https://doi.org/10.1093/aob/mcv118

Sakai, S. (1995). Evolutionarily stable selfing rates of hermaphroditic plants in competing and delayed selfing modes with allocation to attractive structures. *Evolution*, **49**(3), 557–564. [Publisher abstract and DOI: 10.1111/j.1558-5646.1995.tb02287.x](https://doi.org/10.1111/J.1558-5646.1995.TB02287.X).

