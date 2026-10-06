# How island isolation generates floral change: selection conditions, evolutionary sequence and finite realization

**Status:** active Chapter 2 scientific manuscript — 2026-10-05 process result independently confirmed on new visitor histories and demographic repeats; mutation/history analyses are complementary
**Updated:** 2026-10-06 — the preregistered 4,096-case independent replication confirmed the primary delayed-selfing/costly sequence and fixed-assurance results. The claim remains restricted to its declared reproductive setting.
**Inference architecture:** sustained visitor replenishment limitation → altered pollen transfer and reproductive returns → local selection on attraction and assurance → inherited responses and finite realization. Temporal order is tested separately from causal necessity.
**Controlling state:** `docs/CHAPTER2_PROCESS_MAINLINE_20261005.md`, with result priority governed by `docs/MODEL3_RESULT_PRIORITY_AND_PRESENTATION_20261005.md`. The full-mutation common-environment experiment remains complementary evidence.

## Numerical scope amendment, 2026-10-05

The user stopped the high-resolution 1,000-update extension after verified period 7. It is computationally unresolved, not a failed biological hypothesis or a completed PDE corroboration. No automatic continuation is planned. The completed primary ABM experiments and scoped supplementary diagnostics are retained; no uncompleted high-resolution trajectory is used as biological evidence. See MODEL3_LONG_COMPARISON_DECISION_20261005.md.

## Current primary question and interpretation

The primary question is whether reduced floral attraction under sustained
pollinator limitation is caused by the evolution of reproductive assurance, or
whether both traits can respond in parallel to isolation-altered reproductive
returns.

Three comparisons separate these possibilities. Fixed-plant assays measure how
visitor exposure changes the marginal reproductive return to investment before
plant evolution. Maintained-isolation trajectories measure which trait reaches a
declared change first. A matched fixed-assurance intervention tests whether
assurance evolution is necessary for investment decline.

The primary delayed-selfing, assurance-cost 0.5 sequence result is now
**independently confirmed**. A prospectively frozen replication using 64 entirely
new visitor histories and eight new demographic repeats reproduced 51/64
assurance-first histories at the primary 0.05 threshold
(95% visitor-history bootstrap 0.6875–0.8906). The preregistered fixed-assurance
replication also passed: far investment changed by −0.3060
[−0.3181, −0.2941], and far-minus-near investment by −0.4354
[−0.4533, −0.4172].

The central result is therefore **sequence does not identify necessity**.
Reproductive assurance can change first, yet investment still declines when
assurance evolution is blocked. This confirmed sequence is not universal:
prior selfing with positive mutation gave only 30/64 assurance-first histories
at the same threshold. The claim is consequently restricted to the declared delayed-selfing/costly setting rather than promoted to a general law. Prior selfing with positive mutation did not show an assurance-first majority.

## Abstract

Island pollinator limitation is often associated with greater reproductive
assurance and reduced floral attraction, but temporal order does not show
whether one change causes the other. We separate reproductive return,
evolutionary sequence and causal necessity in one explicit plant–pollinator
model with continuing visitor establishment and loss, pollen transfer,
allocation costs, maternal and paternal reproduction, inbreeding depression and
inheritance.

In the delayed-selfing, assurance-cost 0.5 setting, stronger visitor limitation
reversed the marginal reproductive contribution of floral investment at the
same plant state from +0.5793 to −0.7004 as the outcross component fell from
+1.6523 to +0.0854. In the initial maintained-isolation experiment,
reproductive assurance reached a declared 0.05 sustained-change threshold first
in 51/64 visitor histories. We then froze a confirmatory design before new
outcomes were generated. Using 64 independent visitor histories not used in the
discovery and eight new nested demographic repeats, the same sequence was
reproduced in 51/64 histories
(proportion 0.797; 95% history-bootstrap 0.688–0.891). A separate preregistered
fixed-assurance replication showed that investment still declined when
assurance capacity could not evolve: far change −0.3060
[−0.3181, −0.2941] and far-minus-near −0.4354
[−0.4533, −0.4172].

Thus **temporal precedence is not causal necessity**. Pollinator limitation can
lower the reproductive return to attraction directly while assurance and
attraction evolve as interacting but partly parallel responses. The confirmed
assurance-first sequence is setting-specific: prior selfing with positive
mutation did not show an assurance-first majority at the primary threshold.
These are model-level mechanisms, not calibrated reconstructions of natural island histories. The confirmed assurance-first sequence is setting-specific.

## Keywords

plant–pollinator interactions; pollen transfer; functional matching; reproductive assurance; floral evolution; demographic history; finite populations; island syndrome

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

## What the 2026-10-05 result establishes

At an identical plant state, stronger visitor limitation can reverse the
marginal reproductive return to attraction. Reproductive assurance often reaches
a declared evolutionary threshold first, but preventing assurance evolution does
not remove investment decline. The observed sequence is therefore real but does
not identify a selfing-mediated causal chain.

A second, less intuitive result follows from the intervention: allowing assurance
to evolve can reduce the near-far investment contrast because investment changes
in both environments. Weak geographic divergence can therefore coexist with
substantial evolution within each environment. This is why the manuscript
reports within-population change and between-environment divergence as separate
estimands.

# Materials and Methods

## Ecological scope and claim boundary

The primary analysis maintains isolation throughout the evolutionary trajectory and uses explicit mechanism interventions on one plant–pollinator model. Fixed-state selection assays, deterministic propagation and finite-population evolution answer complementary questions. No empirical island outcome was used to tune the model or select the direction of any contrast. Trait values, time, distance and demographic frequencies are synthetic coordinates rather than calibrated natural estimates.

## Replenishment is distinct from island area and plant population size

The mechanistic control variable is expected successful visitor establishment per reproductive update. In the primary exponential-arrival model, lambda = supply x establishment x exp(-distance/scale) = 0.24 exp(-distance). The same completed 13-distance diagnostic can therefore be displayed on a continuous replenishment-rate axis, approximately 0.01195 to 0.24, without recalculating or changing any outcome. It represents new visitor functional types, not visitation events or visitor abundance. Realized arrival counts remain discrete and stochastic, and type disappearance continues at the same hazard.

Plant capacity is a separate model condition. Capacity 48 does not correspond to a declared island area; the ABM represents finite plants and their inheritance rather than island geometry. The primary contrast isolates visitor replenishment at fixed plant capacity and no plant immigration. Population-size comparisons belong to separate, explicitly labelled experiments. The model has a common external source, not inter-island stepping-stone dispersal. Its relevance to islands is the mechanism of replenishment limitation; the model does not claim to recreate every physical consequence of island size or geography.

The primary experiment starts an established plant population and prevents plant immigration. It therefore investigates within-population evolutionary response to ongoing visitor supply, not filtering among plant species during island colonization. Self-compatibility in comparative floras, autonomous capacity in the model, and the realized fraction of selfed offspring are different quantities. Their possible association motivates Q1–Q2 comparison but does not make the model a direct causal explanation of assemblage-level patterns.

## Current primary experiments and their causal contrasts

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

## Ecologically explicit reproductive and inheritance pathway

The model represents a focal plant population embedded in an externally supported visitor environment. Plants carry additive diploid loci for an abstract access/matching trait and floral investment, with reproductive assurance fixed or inherited depending on the declared experiment. Visitor functional types determine finite compatible pollen delivery. Outcrossing contributes maternal and paternal gametes; delayed selfing can fertilize remaining ovules; inbreeding depression reduces viable selfed offspring; and Mendelian inheritance precedes recruitment, density regulation and adult survival. No rule directly moves a floral trait toward an environmental optimum or toward the best visitor.

The earlier complementary island campaign crossed predeclared families for visitor-history transport, fixed-state reproductive assays, reproductive assurance, seed and pollinator connectivity, founding state, trait-grid representation, population scaling, life history, disturbance chronology and recovery. That campaign contains 19,968 audited cases across 80 production cells plus six held-out transport rows. It is a distinct cohort from the current sustained-isolation experiments above. All cases passed state/receipt audit and 80 predeclared deterministic replay checks. Extinct endpoints remained undefined rather than coded as zero.

Model3 is interpreted at a bounded level. The code's reproductive-year label denotes a reproductive update, not a calibrated calendar year. Distances are standardized dispersal coordinates rather than kilometres, visitors are functional types, and investment is not calibrated to flower colour, size or nectar guides. Numerical resolution and approximation are separate from biological uncertainty. Unadmitted positive-mutation deterministic results cannot be promoted as ecological evidence merely because their qualitative directions look plausible.

## Local selection, isolation gradients and parameter sensitivity

Local rare-mutant fitness holds the resident pollen environment fixed and counts half of maternal outcross production, half of paternal outcross success and the full viable selfed contribution. We evaluate its log-fitness derivatives at interior resident states. Analytical zero-gradient inequalities identify selection boundaries in cost space. Finite differences of independently calculated mutant fitness check numerical implementation; they are not additional biological observations.

Three exploratory diagnostics have separate roles and were specified before their respective calculations. First, 13 visitor-arrival distances from 0 to 3 in steps of 0.25, 64 blocked history seeds, snapshots 0/200/400, 45 fixed resident states and two reproductive settings diagnose changes in selection along isolation. The states cross five matching positions (0.2, 0.35, 0.5, 0.65, 0.8) with investment and capacity 0.3, 0.5 and 0.7. No plant evolves in this diagnostic. Histories share seed blocks, not necessarily visitor identities across distances. Pointwise 95% intervals use 1,999 history-bootstrap resamples. All sign-entry and exit brackets are retained without fitting a unique distance threshold.

Second, the four existing reproductive settings and five controlled communities were evaluated at matching 0.2/0.5/0.8 and 49 evenly spaced interior values from 0.02 to 0.98 for each of investment and capacity. Cross derivatives measure how a change in one resident trait changes selection on the other, using steps 0.0001 and 0.00005. They are not evolutionary velocities and contain no genetic covariance.

Third, a bounded sensitivity diagnostic crosses delayed/prior selfing, depression 0/0.25/0.5/0.75/0.9, investment and capacity costs independently at 0/0.25/0.5/1/2, and pollen discount 0/1. All 500 combinations retain all five controlled communities and 45 resident states. A gradient deadband of 1e-7 classifies increase, decrease or neutrality. All analytical gradients are checked against mutant-fitness differences with step 1e-5 and an absolute tolerance of 1e-6. Positive cross-effect exceptions are independently checked from mutant fitness. These values stress-test the assumed reproductive tradeoffs; they are not empirical parameter distributions or replacements for the frozen primary experiment. All conditions, including counterexamples, are retained. Designs, arrays and verification are indexed in MODEL3_PARAMETER_SELECTION_RESULTS_20261005.md.

## Continuous replenishment extension: completed finite-population gradient

To separate replenishment limitation from plant population size, a finite-ABM extension holds capacity at 48 and varies only the visitor arrival coordinate over the same 13 values used in the local-selection diagnostic. The ecological axis is expected successful establishment, lambda = 0.24 exp(-d), rather than island area or an empirically calibrated distance. No island-to-island migration network is included. The two reproductive settings, founders, 64 visitor-history seeds, eight demographic repeats, mutation probability 0.01, mutation step SD 0.05 and 1,000-update horizon are unchanged. The 11 intermediate coordinates add 11,264 cases to 2,048 existing endpoint cases. This is a finite-individual extension, not a resumption of the stopped deterministic/PDE calculation.

The design and readout were recorded before the intermediate-rate outcomes were examined; previously completed endpoints and local-selection diagnostics were already known, so the extension is exploratory. Readouts retain all rates, endpoints 200/400/1,000, both change from founders and paired change relative to highest replenishment, history-level uncertainty and survival denominators. Threshold crossings use 0.025/0.05/0.10 sustained for 20 updates, with crossings within five updates classified as near-simultaneous. Unreached events remain censored. This experiment estimates the shape of the response across replenishment conditions, not sensitivity to the other fixed parameters. All 13,312 cases completed. Independent reconstruction exactly reproduced 9,993,984 trait coordinates; an independent readout check reproduced all 9,984 event records and 156 endpoint rows. The executable design is in MODEL3_REPLENISHMENT_EVOLUTION_20261005.md; complete tables and evidence routes are in MODEL3_REPLENISHMENT_EVOLUTION_RESULTS_20261005.md.

## Prospective isolation-bridge controls

A 24,576-case bridge campaign was frozen before production outcomes were inspected. It crossed 128 independent visitor-history seeds, eight demographic repeats, three starting floral-investment states and four paired near-versus-far interventions: (1) natural isolation-driven visitor histories; (2) response-blind realized-richness matching at each update by thinning both arms to the smaller count; (3) pooling eight independent visitor histories with count-scaled activity normalization; and (4) increasing plant capacity from 48 to 192 while retaining the natural visitor history. Each intervention was evaluated separately for the finite ABM and deterministic genotype-density counterpart.

The primary endpoint was far-minus-near terminal-minus-initial inherited investment. Directional branching was classified across the three starting states at fixed deadbands `0`, `0.01` and `0.05`, after averaging the eight demographic repeats within each independent history; repeat-specific and first-four versus last-four label instability were also retained. Mean uncertainty used 1,999 history-cluster bootstrap resamples. Extinct trait endpoints remained undefined rather than coded as zero.

Per-update richness matching also changes visitor identity persistence, pooled histories alter environmental composition under a nonlinear reproductive operator, and increased plant capacity changes plant demographic stochasticity rather than visitor-community sampling. These are therefore distinct mechanism diagnostics, not literal field manipulations of species richness, island number or lifespan.

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

Allowing assurance to evolve could also narrow the near-far investment contrast.
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

## Local conditions for syndrome-direction selection

The rare-mutant calculation holds resident pollen supply and recipient competition fixed and counts both parental functions: W=F/2+P/2+S, where F is maternal outcross contribution, P paternal outcross contribution and S viable selfed contribution. Let investment be i, autonomous-selfing capacity a, viable selfed fraction v=1-delta, pollen-discount coefficient d and resident outcross fraction q. For delayed selfing define f=q and l=1-q; for prior selfing f=(1-a)q and l=1. Put s=avl, M=f/2+s and J=1 for prior selfing, otherwise 0. The existing analytical implementation gives:

    c_a* = [v*l - J*q/2 - d*f/2] / (2*a*M)
    c_i* = B_i*(f+s) / (2*i*M)

Here B_i is the fixed-resident marginal investment benefit including maternal and paternal functions. At interior trait values with positive fitness and M>0, investment is selected downward when c_i>c_i*, and capacity upward when c_a<c_a*. Their overlap defines the model's local syndrome-direction region. Negative thresholds are retained, not clipped. The inequalities depend on the resident and visitor environment; they do not impose an island optimum or identify a universal distance threshold.

Independent finite differences across 900 state-by-setting-by-community cells matched both analytical gradients, with maximum discrepancy 1.25e-9. This verifies the local selection calculation, not a claim that every population follows its instantaneous gradient: genetic covariance, loss of variation and finite sampling still intervene. Evidence: `data/results/model3_joint_thresholds_20261004.json` and `MODEL3_PDE_CLOSEOUT_20261004.md`.

These conditions separate two consequences of visitor limitation: the return from replacing unfilled outcross opportunities through selfing, and the marginal return from attracting visitors. Inbreeding depression discounts the former; investment costs must be paid even when the latter is small. The two inequalities need not change sign together. They therefore supply a mechanistic basis for testing the sequence of capacity increase and investment decline, without predicting that sequence from a local gradient alone. The maintained-isolation trajectories below measure realized threshold-crossing order, while the fixed-capacity intervention tests necessity. These are distinct estimands.

## Current flowers do not uniquely determine inherited response

A same-phenotype counterexample identifies a limitation of a phenotype-only closure. A population of 0.5/0.5 homozygotes and one of 0.4/0.6 heterozygotes share investment phenotype 0.5 under the same ecology. Their next-generation means both equal 0.5, but variances are 0 and 0.005. A deterministic equation using only the current phenotype distribution cannot return both outcomes without additional genetic state or closure assumptions. This is a model-specific identifiability result, not evidence that genetic differences caused Q1's regional patterns.

In a separate fixed-environment, bounded-founder-support audit, the reduced zero-mutation phenotype ODE matched the direction of the sexual-genotype model in 25/25 cells at 60,200 and 800 updates. At 800 updates the mean absolute difference was 1.62e-7, but endpoint-mean agreement does not establish matching transient distributions or general genetic closure. At zero mutation this is an ODE, not a diffusion PDE. The genuine PDE component concerns reflected allelic mutation at birth, retaining sexual inheritance as an integral/difference operation. These completed mathematical diagnostics do not resolve the full positive-mutation long-run comparison, which was stopped at the user request after verified update 7.

## Isolation can strengthen existing selection rather than initiate it

An exploratory fixed-resident diagnostic varied visitor-arrival distance over 13 values while retaining the existing ecological rules,64 history seeds,45 resident states and two reproductive settings. At snapshot 400, mean selection for increased capacity was positive even at distance 0 in all 45 states in both settings. In contrast, reduced investment was already favoured in 9/45 delayed/costly states and 22/45 prior/no-cost states, and became favoured somewhere along the sampled distance grid for all states. These state counts are designed-grid summaries, not island prevalence. For the central delayed/costly state, investment selection changed from+0.2277 to-0.4518 between distances 0 and 3 while capacity selection strengthened from+0.5748 to+1.4426. Pointwise uncertainty, nonmonotonic brackets and all snapshots are retained in `MODEL3_ISOLATION_SELECTION_GRADIENT_20261005.md`. Thus capacity-first evolution must not be interpreted as proof that isolation first created selection for capacity. Fixed-state snapshot gradients do not establish temporal order or long-run invasion in fluctuating environments.

## Reciprocal coupling of selection on capacity and investment

An exploratory diagnostic evaluated the existing four reproductive settings and five controlled visitor communities at three matching positions and 49x49 interior investment/capacity states. Across 144,060 evaluated states, increasing capacity reduced the local investment selection gradient, and decreasing investment increased the capacity gradient. This reciprocal directional relationship does not imply that either gradient must cross zero or that finite evolution follows the normalized arrows. At matching 0.5 in the delayed/costly left 4 setting, increasing capacity 0.3 to 0.7 at investment 0.5 reduced the investment gradient 0.53555 to 0.08218; it remained positive. Decreasing investment 0.7 to 0.3 at capacity 0.5 increased the capacity gradient 0.32283 to 0.86753. Numerical step halving preserved all derivative signs. These fixed monomorphic-resident fields do not establish crossing order along an isolation gradient or an irreversible feedback. See `MODEL3_RECIPROCAL_SELECTION_20261005.md` for all conditions, figures and validation.

## Reproductive assumptions delimit reciprocal selection

An expanded exploratory parameter diagnostic crossed selfing timing, inbreeding depression, investment cost, capacity cost and pollen discount independently: 500 combinations, five controlled communities and 45 resident states. All four joint selection-sign regimes occurred. The negative capacity-to-investment cross effect from the narrower diagnostic reversed in 25 of 112,500 designed cases, all with delayed selfing, depression 0.9, pollen discount 1 and one controlled community; independent mutant-fitness calculations confirmed these exceptions. Investment-to-capacity cross effects remained negative throughout this grid. Counts describe the designed parameter domain, not natural prevalence. Thus reciprocal reinforcement is conditional rather than a universal mechanism, and local sensitivity does not establish evolutionary timing robustness. Full design, all outcomes and verification are retained in MODEL3_PARAMETER_SELECTION_RESULTS_20261005.md.

## Why investment can decline without capacity evolution

Holding autonomous-selfing capacity at 0.5 leaves a route for saved ovules to produce selfed offspring. Visitor shortage can lower the extra maternal and paternal outcross contribution obtained from attraction while the investment cost coefficient stays unchanged. Reducing investment can then increase viable reproductive contribution through saved ovule allocation. The intervention therefore tests the necessity of capacity evolution, not the necessity of selfing itself. It does not distinguish an obligate-outcrossing population from a population with fixed capacity. In particular, complete visitor absence with zero selfing gives no viable reproduction in this model; an investment trajectory conditional on persistence cannot be inferred for that boundary case.

## How selection becomes a realized response

The mathematical results address four distinct transitions. The joint thresholds diagnose local selection on investment and capacity. The exact multivariate Price accounting verifies transmission through the declared reproductive and inheritance operations; its identity is not a novel evolutionary law. The associated full-G approximation reproduced the declared response signs in 46/48 audit cells, so local gradients cannot replace direct trajectories. Maintained-isolation simulations below measure the time to a sustained trait change. Finite ABM and density contrasts then ask how the shared rules are realized under different state and sampling representations. Finally, mutation diagnostics ask whether loss and replenishment of variation permit continued change. None of these transitions establishes the next by itself.

A completed one-locus diagnostic isolates the last transition, fixing matching and assurance. After 200 updates under different visitor histories, both groups experience the same environment for 800 updates. With capacity 48 and zero mutation, the eight paired ABM replicates retain one allele on average in each group and show zero mean change over the final 100 updates. With mutation rate 0.01, mean allele counts are 7.75 and 6.5, and mean investment changes over those final 100 updates are 0.00274 and 0.00492. All eight pairs remain occupied. Mutation therefore restores variation and allows further change, but individual repeats do not all move upward. Descriptive 95% repeat-bootstrap intervals for the two final 100-update means at capacity 48 are [-0.02117,0.02717] and [-0.02264,0.03894], respectively. These small-repeat, fixed-history intervals include zero; the positive means alone do not establish consistently positive continuing response. Mutation does not erase history immediately. The terminal paired gap remains 0.1733[0.1192,0.2245]. Capacity 192 results are reported alongside this case in the supplement. This restricted history-switch experiment is not the primary maintained-isolation cohort and is not evidence for irreversible alternate equilibria.

The mutation calculation distinguishes the exact birth operator (1-u)I+uH(sigma²/2) from the diffusion approximation H(u*sigma²/2). Here H is the reflected heat semigroup on allele space. Small jumps justify the local diffusion coefficient u*sigma²/2 per transmitted allele; rare mutation alone does not. Sexual reproduction and Mendelian inheritance remain explicit integral/difference operations. Consequently the PDE result concerns a specified process within deterministic propagation. It neither replaces the finite ABM nor establishes a closed phenotype-only evolutionary PDE. The restricted exact-kernel versus heat comparison also fails the declared 0.005 tolerance in one condition; all results and this failure remain in the supplement.

## Genetic diversity, fitness and model scope

The finite model explicitly tracks two alleles at each of three unlinked trait loci, their transmission, selfing/outcrossing and mutation. Deterministic genotype density retains the genotype distribution while removing finite offspring sampling. The heat equation approximates mutational change of transmitted alleles; it does not represent genetic drift. These representations distinguish the supply and retention of selectable variation from immediate reproductive contribution.

Allelic richness, heterozygosity and trait variance are not interchangeable, and none is an additional fitness bonus in this model. Selfed viability is reduced by a fixed depression coefficient, independent of accumulated homozygosity or deleterious alleles. The model therefore cannot establish evolving genetic load, purging, genome-wide diversity protection, or selection on attraction for the purpose of maintaining future evolvability. Outcrossing reshuffles existing alleles but does not itself introduce new alleles into the closed primary populations. The restricted mutation diagnostic demonstrates loss and replenishment of variation, not the full causal claim that declining attraction erodes genome-wide diversity and thereby lowers future fitness.

## Sustained isolation: sequence, mechanism and reproductive consequences

The maintained-isolation cohort follows 64 visitor histories with eight demographic repeats per history and setting for 1,000 reproductive updates. In the delayed-selfing, capacity-cost 0.5 setting with mutation 0.01, selfing capacity crossed a 0.05 change maintained for 20 updates before investment declined in 51/64 more-isolated history means;13 were within five updates. The prior-selfing, no-capacity-cost setting gave 38 capacity-first and 26 near-simultaneous histories. Smaller changes were often near-simultaneous, especially in the prior setting. These are threshold-crossing times, not the onset of infinitesimal change; the two settings differ jointly in timing and capacity cost.

The order of additional isolation divergence was different. In the delayed setting, far-minus-near investment divergence crossed first in 32 histories, capacity divergence in 10, with 20 ties and two investment-only crossings. Both environments can increase capacity early even when their extra isolation difference appears later. Within-population sequence therefore cannot be substituted for the timing of the isolation effect.

The separate fixed/evolving-capacity experiment completed 8,192 cases, with 2,048 identical zero-mutation control pairs and 84 independently reconstructed estimates. All capacity alleles started at 0.5 in both modes, unlike the standing variation of the primary cohort. At update 1,000 with mutation 0.01, fixed-capacity far populations reduced investment by 0.3099[descriptive 95% interval 0.2972,0.3220] under delayed selfing and 0.3316[0.3217,0.3411] under prior selfing. Thus capacity evolution was not necessary for investment decline under this intervention. Realized selfing remained responsive to pollen supply. Displayed arms retained 512/512 populations except delayed/evolving/near, which retained 511/512; trait contrasts condition on the reported survivors.

At identical plant states and capacity 0.5, visitor snapshot 400 shifted the delayed-setting mean investment contribution derivative from+0.5793 under near exposure to-0.7004 under far exposure. Outcross contribution fell from+1.6523 to+0.0854, whereas the viable-selfed component changed from-1.0730 to-0.7858 and partly offset the total decline. These slopes include allocation costs and both maternal and paternal outcross contributions. Isolation did not increase the intrinsic investment-cost coefficient. Composition and visitor amount changed together, so this comparison does not identify a richness-only effect.

Pollen compensation did not make seed deficits interchangeable with viable reproduction. Fixed-plant exposures showed greater pollen-saturation deficits under stronger isolation, while evolved-state compensation could reduce raw deficits without eliminating the viable-offspring deficit under inbreeding depression. In the same-environment delayed/far manipulation at visitor snapshot 400, increasing investment from 0.25 to 0.75 at capacity 0.5 reduced the viable fractional deficit by 0.0104 but reduced viable offspring by 15.72 per 48 plants. These model assays are distinct from Q1's empirical pollen-limitation effect sizes.

Evidence and scope: [temporal results](MODEL3_PERSISTENT_PROCESS_RESULTS_20261005.md), [capacity intervention](MODEL3_ASSURANCE_INTERVENTION_RESULTS_20261005.md), [pollen and fitness pathways](MODEL3_POLLEN_FITNESS_PATHWAYS_20261005.md), [trait manipulation](MODEL3_TRAIT_POLLEN_RESULTS_20261005.md). The original bridge experiments below are retained as distinct cohorts, not pooled with these additional observations.

## Realized evolution across continuous replenishment

At update 1,000 in the delayed-selfing, capacity-cost setting, mean investment change became more negative across the sampled rates as replenishment declined: from -0.01579 (pointwise 95% history-bootstrap interval -0.03502 to 0.00289) at lambda 0.24 to -0.32909 (-0.33949 to -0.31882) at lambda approximately 0.01195. Capacity increased already at the highest rate, by 0.33472 (0.3241 to 0.3450), versus approximately 0.435 at the lowest rate. Replenishment limitation therefore amplified capacity evolution rather than being necessary for its initiation in these founders. In the prior-selfing, zero-capacity-cost setting, substantial investment decline and capacity increase occurred throughout the gradient; its sampled mean investment changes ranged approximately from -0.343 to -0.316. The joint change in selfing timing and cost prevents attributing this difference to either factor alone. All declared endpoint cells retained 512/512 populations. Complete signed estimates and intervals, including matching and paired contrasts, are reported in the companion tables rather than selecting only the strongest contrasts.

The reference condition changes the temporal question. Founder-relative capacity-first counts at the lowest replenishment rate were 51/64 and 38/64 in delayed and prior settings at the primary 0.05 threshold, respectively, with the remaining histories near-simultaneous. In contrast, the additional delayed-setting divergence from highest replenishment reached the investment threshold first in 32/64 histories, capacity first in ten, both within five updates in 20, and investment alone in two. Thus the temporal order of total evolution is not the order of the additional effect of replenishment limitation. Neither crossing comparison establishes mediation. This distinction links the gradient to the separate intervention showing investment decline without evolution of selfing capacity. No natural distance cutoff or universal evolutionary order is inferred.

## Functional matching changes fixed-state reproductive returns and inherited responses

The prospective reduction audit crossed starting access states `0.20, 0.35, 0.50, 0.65, 0.80` with three four-type visitor compositions and a broad eight-type reference. Under each four-type composition, the fixed-state reproductive assay contained both positive and negative total investment gradients. For example, under `left 4`, the gradient was `+1.5048` at starting access `0.20` but `-0.8720` at `0.80`; the signs reversed under `right 4`.

Here the derivative comes from perturbing one finite plant's investment and recomputing reproduction, including pollen allocation among the resident plants. It measures that plant's expected parental genome contribution: half its maternal outcross contribution, half its paternal outcross contribution, plus viable selfed offspring. It is not the rare-mutant log-fitness gradient used in the analytical selection thresholds, where the resident environment is held fixed. The two diagnostics answer related questions but their numerical values and normalizations must not be interchanged.

Composition mattered at fixed count. The maximum left-versus-right difference in fixed-state total gradient was `2.3768`. By contrast, duplicating each `left 4` functional type to produce eight visitor entries changed the fixed-state, deterministic and ABM operators by at most `1.78e-15` under fixed total activity. This is an operator control, not a claim that field species richness is irrelevant.

The deterministic genotype-density counterpart retained mixed positive and negative inherited investment changes in all three four-type visitor contexts, with a maximum left-versus-right endpoint difference of `0.1891`. Demographic stochasticity is therefore not necessary for response branching under these controlled visitor compositions.

The finite-population ABM also retained mixed signs in all three contexts. In this deliberately simple reduction audit, deterministic-density and mean-ABM response signs agreed in all evaluable cells. The larger island campaign nevertheless shows substantial ABM–density sign disagreement under chronology, assurance, life-history and recovery manipulations, showing that finite demography can strongly alter the realized response.

## Isolation assembly, visitor amount and finite realization act at different stages

The 24,576-case prospective bridge closed the two controls that remained unresolved after the stored-transport audit.

Under natural near-versus-far assembly, the finite ABM mean inherited-investment effect was `-0.1446` (95% history-bootstrap interval `-0.1588 to -0.1306`) and the deterministic-density mean was `-0.4510` (`-0.4716 to -0.4301`). These are two model layers with different state representations; their magnitude difference is not interpreted as a finite-population attenuation factor because the density closure is not the stochastic mean of the ABM. The deterministic response was mixed in `0/128` histories at all three deadbands, whereas the finite ABM was mixed in `12/128`, `8/128` and `1/128` histories at deadbands 0, 0.01 and 0.05, respectively.

Response-blind richness matching equalized near and far visitor counts at every reproductive update. This changed the coarse regime: the mean effect became positive in both finite ABM (`+0.0333`, `0.0245 to 0.0425`) and deterministic density (`+0.0338`, `0.0236 to 0.0444`). Finite-ABM mixed histories increased to `68/128`, `59/128` and `18/128`; deterministic density was mixed in `16/128`, `1/128` and `0/128`. Thus visitor amount/richness strongly shifts the mean regime, while substantial realized heterogeneity remains after count matching, primarily in finite populations at practical deadbands.

Pooling eight independent visitor histories eliminated mixed histories in both finite ABM and deterministic density at all three deadbands. By contrast, increasing plant capacity from 48 to 192 while retaining the natural visitor history reduced finite-ABM mixed histories from `12` to `1` at deadband 0 and from `8` to `1` at 0.01, with none at 0.05. The larger-capacity mean moved from `-0.1446` to `-0.2716`; numerically this closes 41.5% of the trait-effect gap to the density closure, but that fraction is descriptive only and is not interpreted as convergence to a stochastic expectation or as a finite-size attenuation coefficient.

Visitor-environment realization and plant-population finiteness therefore alter the observed response through separable interventions. Neither is equivalent to the other, but the mixed-label changes are not interpreted as identifying a stable latent branching probability.

## Numerical sensitivity and branch-identifiability limits

The numerical audit separated operator consistency from continuous-trait convergence. Re-embedding the same finite founder allele support on a finer grid reproduced individual trajectories exactly and density trajectories to machine precision. In contrast, all 16 comparisons that changed the representation of the initial allele distribution failed to establish ±0.01 equivalence. The signs of the main mean contrasts were retained across the frozen grid-sensitivity designs, but exact effect magnitudes and mixed-history counts were not treated as grid invariant. Mixed classifications were also unstable across demographic repeats, especially after richness matching. We therefore interpret mean directional contrasts and intervention responses more strongly than exact mixed fractions, and stable latent branch prevalence is not identified, and we do not infer a continuous-trait PDE limit.

# Discussion

## Sequence does not identify a selfing-mediated causal pathway

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

## Pollination ecology and realized evolution are distinct biological stages

The central result is not simply that island responses are context dependent. The model identifies where context enters the ecological pathway from pollination to evolution. Functional matching can reverse the marginal reproductive return to floral investment before inheritance or demographic updating. That potential response then passes through Mendelian inheritance, and only afterward through finite recruitment, loss of variation, extinction and immigration. What is favoured reproductively, what the deterministic closure predicts, and what is realized in a finite population are therefore different biological objects.

This distinction matters because the three stages did not give interchangeable answers. Controlled visitor compositions generated opposite fixed-state reproductive-return slopes among starting plant states, showing that demographic stochasticity is not required for response non-uniformity. Yet isolation-driven visitor assembly produced a one-directional deterministic inherited response across all 128 visitor histories. Finite populations then reintroduced realized sign heterogeneity in some histories. A system can therefore possess state-dependent evolutionary capacity without expressing that capacity under every ecological regime.

## A common pollination problem need not produce one floral phenotype

The prospective bridge shows why a recurrent island pressure can coexist with non-convergent phenotype. Matching visitor number at each update between near and far histories reversed the mean inherited-investment contrast in both deterministic and finite-population models. The coarse response regime is therefore highly sensitive to realized pollination opportunity. At the same time, finite-population sign heterogeneity increased after count matching, so the factor that moves the mean need not be the factor that determines lineage-level realization.

Environmental averaging and plant-population size affected a different part of the response. Pooling independent visitor histories removed mixed directional labels, whereas increasing plant capacity changed the finite-population mean and nearly removed mixed labels. The numerical movement toward the density closure is descriptive only because that closure is not the stochastic mean of the finite ABM. These interventions are not equivalent and neither is a pure field manipulation of species richness or island size. Together they show that the realized phenotype depends on both the ecological environments sampled through time and the demographic system sampling those environments.

The primary replenishment experiment supports a conditional association between reproductive assurance and reduced investment, while the separate composition experiment shows that matching state can alter reproductive returns and inherited responses. Together they motivate a distinction between repeated functional responses and variable phenotypic realization. They do not demonstrate evolution toward broader floral accessibility: the abstract matching coordinate has no calibrated mapping to that Q1 trait. Nor does the model assign any observed regional floral pattern to a particular synthetic regime.

Experimental evolution has also connected pollinator removal to adaptive selfing and genomic variation loss. The nine-generation Mimulus analysis extended the earlier experiment and used individual-based simulations to investigate genetic change (Busch et al., 2022). It therefore precedes a broad claim that modeling genetic consequences of pollinator shortage is new. Our restricted mutation diagnostic instead distinguishes retention of rare variants in a deterministic representation from their loss in finite populations, and tests whether mutational supply permits further change under the declared conditions. Fixed inbreeding depression does not model the evolution of genetic load or its purging.

## Reproductive assurance preserves trajectories rather than prescribing phenotypes

Reproductive assurance had its clearest effect on persistence. Under the severe visitor-absence treatment, populations without assurance had no terminal survivors, whereas assurance-present populations persisted. Yet assurance did not impose a common floral endpoint. Its ecological role is therefore better described as insurance that keeps an evolutionary trajectory available than as a rule that directly specifies floral form.

This distinction sharpens how breeding-system change should be interpreted in island plants. Autonomous reproduction can buffer demographic failure while pollinator-mediated selection on access or floral investment continues through a partially separate route. A repeated association between isolation and assurance therefore need not imply a serial pathway in which selfing alone determines subsequent floral simplification. In the model, persistence and pollinator-facing evolution can be coupled without being identical.

History adds a second source of decoupling. Early visitor loss, late visitor loss and uninterrupted histories retained different inherited investment states despite sharing the same final 120-update environment in this supplementary history experiment. Present ecological conditions are therefore not sufficient to reconstruct present phenotype within the model. Similarly, source-population immigration can alter an endpoint partly by replacing ancestry, so apparent recovery cannot automatically be interpreted as adaptation of the resident lineage.

## Geographic isolation compresses distinct ecological connections

A single geographic-isolation coordinate can combine biologically different processes. Pollinator connectivity changes the functional reproductive environment; seed connectivity changes demographic and genetic input. In the 3 × 3 connectivity experiment, changing visitor distance and changing seed distance altered inherited floral investment through different routes and could move it in different directions.

This separation is especially relevant for island comparisons. A geographically remote population may experience poor effective pollination, restricted gene flow, both, or neither, depending on vector movement and source availability. Treating all of these as one isolation mechanism risks attributing a floral response to pollinator limitation when the relevant difference is demographic or genetic connectivity, or vice versa. Model 3 does not resolve those channels in existing observational datasets, but it makes their distinct measurements explicit.

## Natural systems contain the ecological ingredients but not yet the full transition

The source-audited island evidence supports the biological plausibility of the modeled stages without validating one universal pathway. Izu shows a common upstream decline in corrected matching with divergent downstream pollen and tube responses. Ogasawara provides a more coherent access-to-pollen-to-reproduction example, while Hawaii and Puerto Rico–Mona show buffering and Dominica provides an adverse, counterdirectional case. Direct-history systems document founding, partner loss and reintroduction effects. These examples show that propagation, buffering and divergence all occur in nature.

What remains poorly observed is the inherited longitudinal stage. Existing studies rarely combine a measured starting plant state, measured visitor regime, repeated inherited trait or genotype change and enough demographic information to distinguish expected evolution from finite-population realization on the same units. That absence is important because cross-sectional morphology cannot be treated as the natural equivalent of a deterministic evolutionary trajectory simply because such a trajectory exists in the model.

The strongest empirical test is therefore not another broad compilation but a transition-linked study measuring plant state, functional visitor exposure, effective pollen transfer, mating route, reproductive output, inherited change and population history through the same ecological transition. Such data would test whether the stage-specific logic transports to nature without using the model to infer a historical cause after the fact.

## Ecological validity and limits

Parameter uncertainty is distinct from repeat-to-repeat stochasticity. The primary 64-history, eight-repeat design estimates the latter conditional on synthetic settings; it does not establish robustness to alternative reproductive costs, inbreeding depression, genetic architecture or arrival functions. The two primary reproductive settings jointly change selfing timing and capacity cost. Mutation rates 0 and 0.01 and alternative temporal thresholds reveal substantial changes in effect magnitude and classified order. The replenishment extension supplies trajectories across 13 arrival rates at fixed remaining parameters; the reciprocal and cost/depression grid broadens local selection coverage but does not supply evolutionary trajectories over all those parameter combinations. Consequently, the ecological result is conditional process decomposition, not a universal claim that selfing initiates before investment decline. Detailed coverage and unresolved sensitivities are recorded in MODEL3_ASSUMPTION_SENSITIVITY_SCOPE_20261005.md.

The model is ecologically explicit but not system calibrated. Its strengths come from preserving the causal order of pollination, mating, inheritance and demography, from separating seed and pollinator connectivity, and from keeping extinction distinct from trait change. Its limitations are equally important. Visitor types are functional agents rather than measured species abundances; background flora supports visitors rather than being coevolved explicitly; floral investment and access are abstract traits rather than named colours, corolla dimensions or nectar guides; inbreeding depression is fixed rather than dynamically purged; and time and distance are model coordinates rather than years and kilometres for a particular archipelago.

These limitations define the inference. The model can identify which ecological processes are sufficient to change selection, expected inherited response and finite-population realization. It cannot estimate natural evolutionary rates, reconstruct a named historical island transition or predict the exact floral phenotype expected in a given region. The useful generalization is therefore structural: ecological function can be more repeatable than phenotypic form because the pathway from pollination to realized evolution contains multiple biologically distinct filters.

## Independent connection to Q1

| Observational question motivating Q2 | Mechanistic counterpart | Interpretation boundary |
|---|---|---|
| H1: do floral traits vary with isolation? | Continuing visitor arrival/loss generates pollen environments; reproductive contributions and inheritance generate trait changes | An independently specified mechanism, not proof of visitor decline in observed islands |
| H2: does selfing explain floral changes? | Timing of capacity increase, capacity-fixed intervention, reciprocal local selection | Fixed capacity is not zero selfing; investment is not literal flower colour or structure |
| H3: does pollen limitation increase with isolation? | Visitor exposure and supplementation assays under maintained isolation | Synthetic distances and visitor rates are not fitted geographic thresholds |
| H4: do particular traits accompany lower limitation? | Capacity/investment interventions compare pollen deficits with viable offspring output | Whole-population interventions differ from observational association and rare-mutant selection; matching is not calibrated accessibility |

Q1 motivates these questions but supplies no fitted parameter or acceptance target. Four regional responses are not reconstructed by assigning them synthetic visitor pools.

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

# Primary figure assembly and captions

The four main figures now use only repository-committed result summaries as
numerical sources. The independent confirmation enters Figure 2 directly.
Unresolved high-resolution numerical work remains outside the main figures.

**Main Figure 1. Visitor limitation reduces the reproductive return to
attraction.** Asset:
`outputs/figures/model3_return_components_20261005/return_components.pdf`.
At the same fixed plant state and assurance capacity 0.5, near and far visitor
exposures are compared for outcross, viable-selfed and total contribution
slopes. In the delayed setting at snapshot 400, total investment contribution
changes from +0.5793 to −0.7004 as the outcross component falls from +1.6523 to
+0.0854; the viable-selfed component partly offsets that decline. Points are
means across 64 paired visitor histories, and the displayed interval is for the
paired far-minus-near difference. These are reproductive-return diagnostics
before plant evolution.

**Main Figure 2. Sequence and necessity are different questions.** Asset:
`outputs/figures/model3_sequence_necessity_20261005/sequence_necessity.pdf`.
Panel A retains discovery history-level crossing times and reports the
prospectively frozen new-history replication beside them. In the primary
delayed/costly positive-mutation cell, assurance is first in 51/64 histories in
both cohorts; the replication 95% history-bootstrap interval is
0.6875–0.8906. The prior-selfing positive-mutation cell is displayed as a scope
boundary rather than pooled with the primary result. Panel B compares the
original fixed-assurance result with the independent replication. In the latter,
far investment change is −0.3060 [−0.3181, −0.2941] and far-minus-near
investment is −0.4354 [−0.4533, −0.4172]. Fixed assurance does not imply absence
of realized selfing, and the intervention does not estimate a full mediation
fraction.

**Main Figure 3. Lower pollen deficit need not mean greater viable
reproduction.** Asset:
`outputs/figures/model3_trait_pollen_20261005/trait_pollen_snapshot400.pdf`.
For both reproductive settings and near/far visitor exposure, the
whole-population investment intervention compares change in fractional viable
pollen deficit with change in viable maternal offspring. In the delayed/far
comparison, increasing investment from 0.25 to 0.75 at assurance capacity 0.5
reduces the fractional viable deficit by 0.0104 while reducing viable maternal
offspring by 15.72 per 48 plants. These are fixed-trait reproductive assays, not
evolutionary trajectories.

**Main Figure 4. Finite genetic realization bounds the process
interpretation.** Asset:
`outputs/figures/model3_genetic_realization_20261005/genetic_realization.pdf`.
This supporting main figure separates ecological intervention effects from
finite genetic realization and the scoped one-locus mutation diagnostic.
Density is not treated as the exact stochastic expectation of the finite ABM,
and the stopped high-resolution positive-mutation comparison contributes no
validated long-run continuum result.

The 13-rate replenishment surface, full local-selection atlas, reciprocal-
selection parameter grid, assurance-evolution attenuation interaction,
full-mutation common-environment experiment and natural-island confrontation
remain Supporting Information. Mutation/history analyses therefore remain
supporting evidence on genetic accessibility and historical persistence, not
part of the primary causal claim. These analyses define scope and mechanism but
do not compete with the confirmed sequence-versus-necessity result as the
paper-level headline.

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

Busch, J. W., Bodbyl-Roels, S., Tusuubira, S., & Kelly, J. K. (2022). Pollinator loss causes rapid adaptive evolution of selfing and dramatically reduces genome-wide genetic variability. *Evolution*, **76**(9), 2130–2144. [DOI: 10.1111/evo.14572](https://doi.org/10.1111/evo.14572).

Sakai, S. (1995). Evolutionarily stable selfing rates of hermaphroditic plants in competing and delayed selfing modes with allocation to attractive structures. *Evolution*, **49**(3), 557–564. [Publisher abstract and DOI: 10.1111/j.1558-5646.1995.tb02287.x](https://doi.org/10.1111/J.1558-5646.1995.TB02287.X).

Sicard, A., Stacey, N., Hermann, K., Dessoly, J., Neuffer, B., Bäurle, I., & Lenhard, M. (2011). Genetics, evolution, and adaptive significance of the selfing syndrome in the genus *Capsella*. *The Plant Cell*, **23**(9), 3156–3171. [DOI: 10.1105/tpc.111.088237](https://doi.org/10.1105/tpc.111.088237).
