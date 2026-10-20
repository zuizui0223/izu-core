# A-mutation × I-payoff × I-parental pairing: six-policy technical readout

**2026-10-20 | SOURCE-ADMITTED BOUNDED TECHNICAL EXPLORATION — NOT CONFIRMATORY A–I HITCHHIKING.** Numerical values and policy semantics come from the successful [Chapter 2 scientific-gate Actions run #39366637628](https://github.com/zuizui0223/izu-core/actions/runs/39366637628), job `118445015594`, original executed HEAD `11c05a08af195c3e4dbe0d012f0b70398d5bb873`. The source-side tests ran [`scripts/chapter2_ai_mutation_payoff_pairing_20261020.py`](../scripts/chapter2_ai_mutation_payoff_pairing_20261020.py), whose six biological-intervention arms and inferential limits were recorded in the [pre-outcome technical protocol](CHAPTER2_AI_MUTATION_PAYOFF_PAIRING_PROTOCOL_20261020.md). All 16 historical technical source configurations' unmodified `Aon_Inative` controls matched the native original Q1 time series/genome at the declared numerical tolerance, and the I-neutralized genotype-shuffle controls conserved source M/A, occupancy, breeding-mode counts and A mutation histories **within an A-mutational policy**. Underlying original reproductive, genetic and founder routines were not edited.

## Exactly what was done

Two previously disclosed PR569 founder genomes `560201,560202`, two previously disclosed visitor histories `560301,560302`, near/far imposed visitor states and two historic mating regimes `delayed_control,assurance_cost` form **16 founder×visitor×regime cases**, not 16 independent source populations. Every original source genome begins with **all A alleles exactly 0.5**. Six arms per case, 24 reproductive updates and mutation probability .01 where permitted give **96 short synthetic trajectories**. This is neither a replay of all 1,024 original PR569 1000-update evolutionary results nor 96 natural islands. No predeclared scientific minimal effect, source-heldout test, permutation significance test or phylogenetic/field calibration exists for these interventions.

Aoff means only de-novo A mutation is prohibited while autonomous reproduction at A=.5, Mendelian transmission and M/I mutation remain possible. I-neutral means its **expressed genotype-dependent maternal/paternal payoff** is standardized to I=.5 **only for the native reproductive ledger**; its actual offspring allele variants remain inherited. I-shuffle is deliberately artificial: it reassorts **complete diploid I genotypes plus their provenance flags** among living parents before every update, preserving the I locus's complete genotype marginal, rather than implementing biological crossover between physically linked loci.

## Complete all-start occupancy and source-averaged final-I readout

All six arms in **all 16 original source cases** remained occupied at the end of update24. Consequently the following means are across all 16 original source cells; although numerical mean I is defined here for every arm, that does not turn the 16 cells into iid replicates. If an arm had gone extinct, I would have been undefined rather than zero.

| Parent-I payoff | New A mutation | I pairing manipulation | Occupied /16 | Mean final inherited I across occupied sources |
| --- | --- | --- | ---: | ---: |
| Native genotype-dependent I benefit/cost | Allowed | None | **16/16** | **0.53829378** |
| Native | Prevented | None | **16/16** | **0.57427800** |
| I-dependent payoff neutralized (expressed I=.5) | Allowed | None | **16/16** | **0.55085506** |
| I-dependent payoff neutralized | Prevented | None | **16/16** | **0.48192407** |
| I-dependent payoff neutralized | Allowed | I diplotype shuffled each census | **16/16** | **0.48150622** |
| I-dependent payoff neutralized | Prevented | I diplotype shuffled each census | **16/16** | **0.46689625** |

Exact *descriptive policy contrasts* for these 16 source-cell means:

| Source-conditional contrast | Evolving A mutation minus preventing de-novo A mutation in mean final I |
| --- | ---: |
| With original direct-I fitness | **−0.03598422** |
| With expressed direct-I fitness neutralized | **+0.06893098** |
| With direct-I fitness neutralized and I diplotypes shuffled each census | **+0.01460997** |

A conventional two-factor contrast between the latter two A-mutation differences is approximately **+0.05432101** in native I trait units. This is a **descriptive interaction among controlled model interventions**, NOT an identified percentage mediated by genomic hitchhiking: recurrent artificially reshuffling I among current plants changes I–A and I–M genotype associations and parent identity, not merely the effective recombination rate. The remaining +0.01461 under shuffling also cautions against a simplistic all-or-nothing explanation.

This is an informative **synthetic mechanism screen** because I's *current direct genotype-dependent payoff* is held constant in the I-neutral conditions, yet mutation at A can still alter inherited mean I through multigenerational parentage, stochastic transmission and indirect genetic associations. The reduction in the A-mutation contrast when the inherited I diplotype association is repeatedly perturbed is **consistent with association-dependent transmission effects**. It does NOT demonstrate that the historical founder-specific sign differences in PR569 were created by the same route, or that selfing-specific physical linkage is responsible. Their main 1000-update panel starts with A monomorphic but allows A mutations, and has independently re-sampled founders and visitor histories not represented here.

## Mixed signs across environmental contexts

For the original 8 crossed founder×visitor×mating-setting cells, the near–far **difference of the A-mutation-induced I terminal contrast** already appeared heterogeneous in the first source log; e.g., delayed-control source 560201×560302 had native **−0.148721** but neutral-I **+0.190038**, while delayed-control 560202×560301 had native **+0.077901**, neutral-I **+0.206528** and shuffled neutral-I **−0.246807**. Thus **the sign is not uniformly predicted across contexts**. A new [case-level source regression](../tests/test_chapter2_ai_mutation_payoff_pairing_20261020.py) was added after the first experiment to preserve all 16 × 3 original individual source contrasts and print their signs. Those results are a readback of the SAME finite 96 paths, not fresh confirmation; their new CI should be checked before additional numerical claims.

## Source-specific signs — exposed technical panel (not iid)

The follow-up **case-level source regression** completed successfully in [scientific gate **39367112484**](https://github.com/zuizui0223/izu-core/actions/runs/39367112484), job `118446400955`. It reads the **same 16 source cells and the same six technical policies**, with no independent simulation sample or new biological replication. Each value below is the effect of enabling rather than disabling *de-novo A mutation* on final I within the specified `setting × founder × visitor × near/far` cell. The last column is **(I-neutral mutation contrast) minus (I-neutral-with-I-reassignment mutation contrast)**.

| Setting | Founder | Visitor | Near/far | I native: Aon−Aoff | I-neutral: Aon−Aoff | I-neutral + shuffle: Aon−Aoff | Pairing-intervention contrast |
| --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| delayed_control | 560201 | 560301 | near | -0.157973 | -0.012771 | -0.007281 | -0.005489 |
| delayed_control | 560201 | 560301 | far | -0.157396 | +0.012460 | +0.035697 | -0.023236 |
| delayed_control | 560201 | 560302 | near | +0.024071 | -0.042325 | +0.005109 | -0.047434 |
| delayed_control | 560201 | 560302 | far | -0.124650 | +0.147713 | -0.027695 | +0.175408 |
| delayed_control | 560202 | 560301 | near | -0.075054 | +0.112374 | +0.072325 | +0.040050 |
| delayed_control | 560202 | 560301 | far | +0.002846 | +0.318902 | -0.174482 | +0.493384 |
| delayed_control | 560202 | 560302 | near | -0.028587 | +0.144146 | +0.070052 | +0.074094 |
| delayed_control | 560202 | 560302 | far | +0.002573 | +0.005485 | -0.033145 | +0.038629 |
| assurance_cost | 560201 | 560301 | near | +0.048897 | -0.037680 | +0.180852 | -0.218532 |
| assurance_cost | 560201 | 560301 | far | -0.077860 | +0.040332 | +0.089009 | -0.048677 |
| assurance_cost | 560201 | 560302 | near | +0.028017 | +0.073230 | +0.058937 | +0.014293 |
| assurance_cost | 560201 | 560302 | far | -0.128995 | +0.036245 | -0.009741 | +0.045986 |
| assurance_cost | 560202 | 560301 | near | -0.051304 | +0.151849 | -0.014619 | +0.166468 |
| assurance_cost | 560202 | 560301 | far | +0.115145 | +0.190578 | +0.075557 | +0.115020 |
| assurance_cost | 560202 | 560302 | near | -0.107099 | +0.040137 | -0.164789 | +0.204926 |
| assurance_cost | 560202 | 560302 | far | +0.111620 | -0.077779 | +0.077975 | -0.155754 |

**Source-group heterogeneity is pronounced.** With I payoffs neutralized but native genotype associations intact, the source-specific A-mutation effect is **positive in 12/16 cells** and negative in 4/16. After artificial I-diplotype reallocation it is **positive in 9/16 cells** and negative in 7/16. The pairing-intervention contrast itself is positive in **10/16**, negative in **6/16**, with mean **+0.054321**, median **+0.039339**, and a highly heterogeneous range **[-0.218532, +0.493384]**. The biggest positive case is `delayed_control / founder 560202 / visitor 560301 / far`: I-neutral Aon−Aoff **+0.318902**, after reshuffling **−0.174482**. The counterexample `assurance_cost / founder 560201 / visitor 560301 / near` goes from **−0.037680** without shuffling to **+0.180852** with shuffling.

For a **single fixed artificial source-regime group**, an indirect genetic association mechanism is visibly possible under I-neutral payoffs. But the size and even **sign** of that effect are strongly contingent on the original founder/visitor/near-far history. The data cannot justify a universal statement that I-diplotype reassignment *always reduces* mutation-induced I response, nor can 16 crossed cells be analyzed as independent islands. The original near and far states share founder and visitor seeds; the same two founders and visitor seeds recur across both mating regimes. The mean interaction is driven partly by large positive cases. No preregistered across-source interval or independent held-out founder/visitor ensemble was run.

## Specific reason novelty is still not established

- The one-step I-neutral, A–I correlated-parent sign change previously demonstrated is the existing Price selection covariance identity; neither it nor the current 24-update extension proves a new population-genetic law.
- Actual PR569 founder A variation was **exactly zero at t0**, so any indirect A–I association must arise *after* A mutation or under family/demographic composition changes. The mutation-origin tracer over 12 updates found 216 A births but **no robust high-I-background A mutation advantage at equal follow-up age**. It has not linked individual mutation-origin variants to signed 1000-update I outcomes.
- No new held-out founders/visitors or natural I measurements are available, and pairwise source RNG streams are shared across near/far and A/I interventions.
- Aoff changes both possible future A phenotypes and associated mating histories, while I shuffled changes I inheritance across parents. The observed factorial interaction is not unique causal mediation attributable to physical A–I hitchhiking.
- PR #569's **fresh-founder 4-setting decision remains 3/4** (direct A cost inconclusive). Source-supported one-Article work on [PR #609](https://github.com/zuizui0223/izu-core/pull/609) remains unmodified by these engineering experiments.

**Next scientifically decisive gate:** Fix a new independent founder×visitor full-history source design with mutation-event pedigrees, isolate no I direct-payoff vs I mutational supply separately, use parentage-preserving conditional alignment randomizations and independently held-out contrasts. Report the all-start set including failed A mutant births, neutralized/no-mutation controls, and across-source uncertainty; no post-hoc favorable-source selection.
