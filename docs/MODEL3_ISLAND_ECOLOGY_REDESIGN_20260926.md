# Model 3: island ecological redesign and novelty audit

Status: proposed scientific design, 2026-09-26. Not a frozen experiment, implemented extension, or new result. Baseline inspected at 4c4347e148197b43ddbb231931cd733b5f79f720. Preserve all archived runners and results.

## Purpose and user constraints

The primary contribution must be an ecological result about floral evolution on islands. Deterministic approximation, S/C/I, ranking reversal and transportability are explanatory tools, not the subject of the paper. Q1 supplies inspiration only: do not fit four regional responses or assign regions to synthetic regimes. Compare repeated islands along isolation and establishment histories; include life history, pollen limitation, inbreeding depression, mutation and drift in the appropriate experiments. Computational success is not evidence of novelty.

## What the present model can and cannot establish

The existing model implements inherited access/matching and floral investment, finite pollen transfer, delayed selfing, fixed inbreeding depression and demographic sampling. It lacks distance-based arrival, plant immigration, mutation and explicit island founding/separation histories. Its deterministic counterpart is a discrete genotype-density map, not a PDE. `scripts/model3_meanfield.py` explicitly removes both demographic sampling and individual pollen self-exclusion. It is not the expectation of the finite process; nonlinear recruitment also requires a one-step expectation audit. Consequently, declining differences between capacity 48 and 192 do not by themselves isolate drift or demonstrate convergence. The existing coarse/refined grids have not established numerical convergence.

The earlier long runs primarily exhaust standing variation. Extending them alone cannot support a mutation-maintained evolutionary limit. Maintain the distinction between an abstract investment trait and measured flower size, colour or pollination syndrome.

## Nearest literature: overlap before novelty

This is a targeted audit, not an exhaustive review or proof of absence. Source access level is recorded below; no date is inferred from search-engine age labels.

| Primary source | Verified overlap | Consequence |
|---|---|---|
| Pannell & Barrett (1998), *Baker's Law Revisited*, full author PDF [1] | Colonization/extinction, reproductive assurance, perenniality and dormancy already linked in a metapopulation model | Assurance plus lifespan is not a new principle |
| *Mating System Plasticity Promotes Persistence and Adaptation of Colonizing Populations*, publisher search abstract only [2] | Mating plasticity, persistence and adaptation after colonization | Full-text equations must be compared before claiming a distinct mechanism |
| Tomasini (2022), *The role of spatial structure in multi-deme models of evolutionary rescue*, publisher full text [3] | Migration can promote or prevent rescue; spatial structure changes effective migration | Intermediate migration benefits and spatial rescue are established ideas |
| *Parallel reduction in flowering time from de novo mutations enable evolutionary rescue in colonizing lineages* (2022), publisher full text [4] | New mutations and flowering evolution in island colonizing lineages | Mutation-enabled island floral adaptation alone is not novel |
| Champagnat, Ferriere & Meleard (2006), author manuscript [5] | Individual stochastic processes, macroscopic limits and time scalings | ABM-to-density/PDE convergence is not itself a new ecological result; their asexual/haploid construction is not a theorem for this sexual model |
| *Island colonization in flowering plants is determined by the interplay of breeding system, lifespan, floral symmetry, and arrival opportunity*, indexed primary article [6] | Direct overlap with island arrival, floral traits, life history and breeding system | Essential nearest empirical comparator; full methods audit still required |
| *Transient Eco-Evolutionary Dynamics and the Window of Opportunity for Establishment of Immigrants*, publisher abstract [7] | Arrival order and evolutionary priority effects | Do not claim the first evolutionary arrival-order effect |

Existing repository audits `CHAPTER2_RESPONSE_REGIME_NOVELTY_20260925.md` and `CHAPTER2_SIMULATION_NOVELTY_AUDIT_20260925.md` also reject novelty based merely on mixed island responses or distribution-sensitive variance rankings. Their conclusions remain in force.

## Recommended ecological question

When do the relative arrival and loss histories of plants and effective pollinators allow floral adaptation, and when do they leave persistent floral divergence or prevent population persistence?

Candidate contribution: identify whether two islands with the same present connectivity, size and pollinator summary can differ predictably because plants and effective pollinators became established at different times, and identify when subsequent immigration erases that difference. This combines floral change with occupancy, rather than studying only surviving populations. Historical contingency itself is established; novelty must rest on a specific, tested mechanism and discriminating predictions.

Compare three options explicitly:

1. **Recommended:** repeated-island arrival/history experiments, with floral trajectories and persistence as primary outcomes. More ecological content; requires separate plant and pollinator arrivals.
2. Distance x size x assurance response surfaces without arrival-history manipulation. Simpler, useful baseline, but substantial overlap with established rescue and mating-system theory.
3. ABM approximation and factor-ranking theory as the main paper. Technically coherent, but contrary to the user's requested ecological emphasis; retain only as supporting analysis.

## Prospective hypotheses and their alternatives

H1: Relative arrival timing affects establishment and floral evolution beyond present-day pollinator availability. Test paired early/late visitor schedules with matched visitor identities, total exposure and final environment. Compare with no history dependence; do not infer timing effects from differing total pollen alone. A schedule-matched diagnostic is an intervention, not a natural-history simulation.

H2: Reproductive assurance permits persistence through a visitor gap, but surviving floral trajectories depend on subsequent effective visitation and investment costs. Separate demographic buffering from selection on investment using fixed-trait and neutral-parent controls. Low investment with no visitors can follow directly from the cost function; that result alone is not a discovery.

H3: Continued seed immigration can erase founder-dependent divergence while sustaining populations; pollinator arrival can change selection without introducing plant alleles. Cross these processes instead of changing both through one isolation parameter. Alternatives include no erasure or purely demographic effects.

H4: Longer reproductive lifetimes buffer short visitor interruptions but need not buffer persistent absences. Match annual reproductive effort separately from lifetime effort; compare interruption duration relative to realized generation time. Do not interpret survival-only effects when allocation changes simultaneously.

H5: Founding versus separation histories can leave different trait and occupancy trajectories at matched current environment. Factor inherited diversity, initial abundance and initial visitor composition separately, then test the natural bundled histories. A contrast between bundled histories is a total history effect, not proof of one component.

Any unsupported hypothesis stays unsupported. Neither a non-monotonic isolation response nor a C-to-I-to-S sequence is required for success.

## Island process contract

Use distinct plant-seed and visitor-functional-type source pools. Arrival rate = source supply x probability of reaching the island x establishment probability. Distances enter reach probabilities through declared, guild-specific kernels; rates are per unit time. Allow multiple arrivals with a count process. Distinguish colonization from routine visitation and arrival from establishment. Uncalibrated distance/scale ratios remain dimensionless; do not label them as actual kilometres.

An oceanic-founding scenario starts with suitable habitat and a colonization process; a continental-separation scenario inherits an assembled population and community before connectivity changes. Neither represents every geological island class. Recolonization must be possible where seed arrivals continue; distinguish first lineage extinction from subsequent island occupancy. Island area influences declared capacity and habitat availability, not every rate by an unexplained common multiplier.

A visitor cannot establish on an otherwise empty island without resources. Either model background floral resources explicitly as a declared environmental support, or make establishment conditional on available resources. The first version can study a focal plant within a background flora; it must not claim whole-island coassembly or reciprocal coevolution.

Mutation occurs during inheritance with declared rates and effect distributions; immigration is a separate source of alleles. A fixed selfing parameter tests assurance treatments, not evolution of selfing. Fixed offspring depression does not model purging or genetic-load rescue. These claim boundaries survive the extension unless those mechanisms are separately implemented and validated.

## Outcomes and comparisons

Primary outputs by distance/history and time: probability of occupancy, lineage persistence/recolonization, distributions of floral trait changes, and genetic variation. Trait outcomes after extinction are undefined, never zero. Report occupancy and survivor-conditional traits together; immigrant replacement must not be mistaken for within-lineage evolution. Track ancestry and decompose observed change into inherited resident response and immigration/composition where identifiable.

Use paired visitor histories and initial states across interventions; independently replicate demographic, inheritance and mutation streams within each pair. Distance treatments need independent island histories as biological simulation replicates. Monte Carlo precision must be chosen before production: worst-case binomial half-width approximately 1.96/(2 sqrt(R)); roughly 1,068 independent replicates are needed for a 0.03 half-width. This is a planning approximation, not a guarantee for rare events or conditional outcomes. Use an outcome-blind pilot for timing and numerical validity, then freeze the production design. Boundary searches and confirmation seeds must be separate.

Test seed arrival, pollinator arrival, history, assurance and lifespan with discriminating interventions before attempting an enormous full factorial. Naturalistic bundles and one-factor counterfactuals answer different questions; report both labels accurately.

## Time, k and S/C/I

R = replicate islands estimates uncertainty; it is not ecological k. A candidate effective exposure count concerns independent reproductive environments experienced during a lifetime/generation. Estimate it from a predeclared service or selection time series and reproductive weights, respecting autocorrelation. Do not equate it to longevity, richness, island count or the old concatenated-history pooling operator. Report undefined/nonstationary cases rather than forcing a scalar k.

For S/C/I, cross initial plant states S with exogenous visitor histories C and repeat demographic/mutation sampling D within cells. Decompose cell expectations with residual within-cell stochastic variation reported separately; do not call demographic residual I. Analyse trait changes, not only final trait values that mechanically retain starting differences. Extinction changes support: use occupancy decomposition and clearly conditional trait decomposition, avoiding survivor-selected causal attribution. Old numeric shares cannot be carried forward.

Transport means prospectively predicting a held-out island regime from another, with declared trait/persistence endpoints and prediction error. Factor rankings require identical intervention ranges and weights; changes of input distribution can reverse rankings without changing biology. Rank reversals are secondary explanations only if robust and ecologically interpretable.

## Deterministic comparison as a supporting experiment

Retain the shared reproduction/inheritance operator. Audit one-step conditional expectations, density regulation and finite pollen self-exclusion before attributing a gap to stochasticity. Compare deterministic and stochastic models conditional on the same visitor path; a separate environment-averaging experiment addresses the loss of visitor fluctuations. Environmental randomness need not vanish when plant capacity grows.

Increase capacity at fixed density, per-capita resources and immigration convention; a different capacity treatment can separately represent changing island area. Match mutation and migration scaling explicitly. Establish allele-grid convergence before fitting a population-size convergence rate. A genotype-density model is a valid counterpart; trait-grid refinement alone does not turn a discrete sexual inheritance map into a PDE.

Use the density model first for conditional selection directions and equilibria, then stochastic runs for reachability, variable retention and extinction over declared horizons. Initial direction does not prove a long-term endpoint. Mutation diffusion is not genetic drift. Large-population and long-time limits need not commute: finite closed populations may eventually go extinct while the deterministic system persists. Therefore convergence claims require a fixed horizon or an explicitly derived joint scaling. Fast-time averaging requires verified timescale separation and averaging of the reproductive operator, not substitution of mean visitors into a nonlinear function.

## Required implementation decisions before freezing a campaign

1. Complete full-method comparisons for sources [2], [6], [7], and focused arrival-lag theory. Narrow or abandon the candidate novelty if already covered.
2. Specify source pools, dispersal kernels, resource support, settlement and density scaling, with ecological units and calibration limits.
3. Define genomic state, mutation, ancestry tracking, founder/separation initialization and random-stream contract. Keep frozen model3 files unchanged; new versioned module family.
4. Derive a shared reproductive operator and one-step expectation tests, then island event scheduling and paired interventions.
5. Test conservation, zero-arrival and zero-mutation limits, recolonization, same-seed replay, life-history units, and numerical refinement. Verify no-source closed islands and source-fed occupancy separately.
6. Freeze endpoint definitions, meaningful effect thresholds, independent replication, horizons and compute budget before production. Publish negative and non-evaluable outcomes as well as ecological patterns.

This is a dependency outline, not an approved file-level implementation plan. Outstanding specification choices and source checks mean the redesign goal remains active. No new simulation has been launched and no previous result has been replaced.

## Addendum: existing attenuation result and the Ch1-motivated mechanism contrast

User steering: retain the existing individual/density evidence alongside arrival-order and mismatch experiments. Ch1 motivates competing explanations, not regional calibration or proof that a model mechanism caused the observed patterns.

### Numeric recheck

Recomputed directly from `data/results/model3_grid_summary_20260925/endpoints.csv`, selected, grid3, annual, selfing 0.5, depression 0.5, 64 histories per cell. Changes subtract each trajectory's own initial investment.

|Year|Capacity|Start|Island individual change|Island density change|
|---|---|---|---|---|
|100|48|0.3|-0.025716|-0.068429|
|100|48|0.7|-0.027653|-0.067137|
|100|192|0.3|-0.050977|-0.067848|
|100|192|0.7|-0.053520|-0.067071|
|400|48|0.3|-0.032992|-0.100898|
|400|48|0.7|-0.031429|-0.100866|
|400|192|0.3|-0.076278|-0.099586|
|400|192|0.7|-0.073796|-0.099456|

At year 100, capacity 48, start 0.3, mainland change is +0.036149 individual and +0.069620 density. Mainland-minus-island changes therefore differ by 0.061865 versus 0.138049. This is a reduction in the difference of mean responses; it is not a demonstrated reduction of every paired response. Both mainland and island populations have finite capacity here, so do not attribute the entire attenuation to finite island populations alone. Add an asymmetric large-source/small-island comparison.

The proposed trait-specific absolute-error summary needs correction. For the same annual capacity-48 island cells at year 400, mean absolute individual-density access gaps are 0.053321 and 0.055315; investment gaps are 0.068340 and 0.069876. The proposed access absolute gap near 0.008 is not reproduced for these cells. Signed mean bias and mean absolute error must be reported separately; cancellation is not accurate prediction. No broad trait-specific robustness claim follows from these numbers.

The deterministic trajectory is not a proven optimum. A difference persisting to year 400 rejects disappearance within that tested horizon, not all longer transients. Common visitor history does not ensure identical selection gradients once population density, genotype frequencies and pollen allocation diverge.

### Competing ecological explanations for reduced floral investment

1. **Selfing-mediated pathway:** pollinator changes alter autonomous reproductive assurance or realized selfing, changing marginal benefits of attraction. The current fixed selfing-capacity parameter does not implement evolved selfing. Realized selfing can nevertheless change with outcross pollen availability; record capacity and realized rate separately.
2. **Direct marginal-return pathway:** holding assurance capacity and other genetic traits fixed, pollinator abundance, effectiveness or mismatch changes how much additional attraction increases male and female reproductive success. Investment can decline if its marginal return falls below its marginal cost. Pollinator loss does not itself increase the physiological cost coefficient.
3. **Finite-population constraint:** stochastic inheritance, loss of variation and finite pollen transfer can limit or change either response. These processes can explain attenuation, but require separated interventions, not attribution from an endpoint gap.

A lower visitation level does not guarantee weaker selection for attraction: competition for scarce effective visitors can strengthen its marginal advantage. Functional mismatch can instead make additional attraction ineffective. Estimate trait-dependent reproductive success and local marginal returns; test both directions. Matching/access and investment remain abstract traits, not floral colour or structural complexity without an explicit measurement map.

### Identifying experiments

First retain fixed assurance capacity while crossing visitor abundance, functional mismatch and arrival timing; record pollen delivery, male and female parentage, realized selfing, viable recruitment, density and genetic variance. Use standardized assay populations with identical density/genotype composition to separate changed selection surfaces from changed available variation. Cost-free and declared cost-gradient treatments diagnose whether reduced investment depends on allocation cost; they are mechanistic interventions, not naturally costless flowers.

Then compare fixed assurance with an explicitly heritable assurance trait under the same external histories, including pollen/ovule discounting contracts and inbreeding depression. Do not add a pleiotropic rule that forces investment to decrease when selfing increases: that would build the desired syndrome into the model. This extension needs its own inheritance and fitness specification. A total fixed-versus-evolving contrast includes demographic feedback; it is not automatically a clean statistical mediation estimate.

For arrival history, compare a visitor gap followed by recovery with an exposure-matched sequence without the long gap. Test recovery alone versus recovery plus independently specified seed immigration or mutation supply. Distinguish restored population numbers from restored genetic variation. A lasting floral response after visitor recovery is a candidate historical legacy, not established irreversibility.

Supporting finite-process audit: separate pollen self-exclusion, demographic sampling and inherited-allele sampling where a valid shared operator permits it; validate one-step expectations including recruitment truncation. Maintain interactions between these components rather than assuming their endpoint contributions add. Repeat grid refinement and capacity scaling before calling the attenuation resolution-independent.

### Novelty ceiling and Ch1 bridge

Selfing, adaptation and diversity loss already have direct precedents, including experimental pollinator removal: [Busch et al. (2022)](https://onlinelibrary.wiley.com/doi/10.1111/evo.14572). The contribution cannot be merely that small/selfing populations lose variation. Candidate advance is a tested explanation of when pollinator-history changes select lower investment, when assurance mediates that response, and when finite-population loss of evolutionary capacity prevents the predicted response or its recovery.

Ch1 can motivate these alternatives and identify discriminating field measurements: autonomous assurance versus realized outcrossing, effective pollen delivery, visitor-trait mismatch, floral investment, genetic variation and demographic history. A residual association after adjusting for a coarse selfing category does not prove direct pollinator selection; mediation, measurement error and shared causes remain possible. No fitted assignment of the four regions to these mechanisms is authorized or supported.

## Updated nearest-literature assessment

See `MODEL3_NEAREST_PRECEDENTS_20260926.md` for the follow-up primary-source audit. Peterson & Kay and Zell et al. have now been inspected beyond abstract level. Xu (2023) and Degottex-Fery & Cheptou (2023) add close precedents on pollen limitation, selfing rescue and finite/infinite population comparisons. The earlier access-status table records the initial search; this follow-up supersedes it where explicitly stated. The broad ABM comparison or assurance/colonization result is not the novelty claim.

## Sources

1. https://www.zoology.ubc.ca/let/pdfs/Pannell_Barrett_1998.pdf
2. https://www.journals.uchicago.edu/doi/10.1086/679107
3. https://onlinelibrary.wiley.com/doi/10.1111/jeb.14018
4. https://www.nature.com/articles/s41467-022-28800-z
5. https://nchampagnat.perso.math.cnrs.fr/TPBlatex63.pdf
6. https://pmc.ncbi.nlm.nih.gov/articles/PMC11617658/
7. https://www.journals.uchicago.edu/doi/10.1086/715829
