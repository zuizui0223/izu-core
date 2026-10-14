# Q3: variation maintenance cannot preserve both endpoint mean and support

Status: deterministic feasibility argument, using the frozen trait definition and previously verified endpoint-fixation observations. No new trajectories, RNG draws, endpoint extraction, or outcome-dependent statistical test. This note does not activate a maintenance experiment or estimate its effect.

## The intervention constraint

Suppose a nonempty diploid population's I alleles must remain in the original interval [L,U]. Let X be an allele copy chosen uniformly from the 2N copies, m its mean, and V its population variance (denominator 2N). In the frozen model each individual's expressed I is the arithmetic mean of its two I alleles. Therefore the mean expressed I over individuals equals m.

For every allele copy, (U-X)(X-L) >= 0. Averaging and expanding gives

`0 <= (U-m)(m-L) - V`, hence `V <= (U-m)(m-L)`.

At upper fixation m=U, or lower fixation m=L, the right-hand side is zero. Thus V=0. A policy that restores positive allele variance after endpoint fixation **cannot simultaneously keep the population mean unchanged and retain the original support interval**. Preserving every individual's expression is stronger than preserving the mean, so it is impossible under those same constraints as well. This conclusion is independent of carrier allocation, population size, mating system, or future random seeds. It applies to a nonempty post-intervention population; changing the number of individuals does not evade the mean/support bound.

This is an impossibility result for one requested combination of constraints, not proof that every maintenance intervention is impossible or that persistence has no causal effect.

## Quantifying the necessary immediate change

Let W=U-L and start at upper fixation. If a policy keeps [L,U] and requires variance at least V0>0, write the new mean m=U-delta. The bound requires

`V0 <= delta*(W-delta)`.

If V0>W²/4 the requirement is impossible anywhere in the interval. Otherwise it necessarily requires

`delta >= (W - sqrt(W² - 4*V0))/2 > 0`.

There is also the symmetric upper bound on delta from the other root. These are necessary conditions; finite allele counts or additional genotype constraints may make a particular variance unattainable. No general sufficiency claim is made. At lower fixation the same argument requires a positive increase in the mean.

For the original restoration support [v-h,v+h], h=1/16, the original all-carrier assignment has variance h²=1/256. This is the maximum possible variance on that interval. Requiring that variance after upper fixation forces m=v and delta=h=0.0625. Equality requires all allele copies at the two endpoints with equal frequencies; in a diploid population this allele-count condition is attainable, though it does not uniquely specify homologue pairing or carrier identities. Restoring that variance necessarily lowers the mean immediately by 0.0625, before any future demographic or selection process. Starting at lower fixation forces an immediate increase by the same amount. It cannot be described as changing only the persistence of variance while holding the investment level fixed.

## Consequence for the remaining Q3 question

The existing-record analysis found upper-endpoint refixation before event completion in all 72 original confirmation event losses. This note does not infer that preventing fixation would recover those events. It shows a concrete constraint on defining an isolated maintenance intervention: rescuing positive variance at those endpoint states while preserving both the original mean and support is not an admissible isolated operation.

A future maintenance contrast must therefore relax at least one of these conditions, for example allow a mean shift within the old support, expand support while controlling mean, or intervene before endpoint fixation while there is interior-mean slack. Each is a different policy and can change additional features of the genotype distribution and reproduction. The last option requires a prospective trigger rule rather than retrospectively selecting paths that later refix. The constraint applies at each time maintenance is imposed; merely choosing an earlier intervention time does not prove indefinite maintenance feasible.

The future estimand must include the complete chosen policy, including its immediate mean or support changes. An effect cannot be attributed solely to a natural persistence mediator without extra structural assumptions or additional well-defined contrasts. Additional replications of A/B/C cannot settle this intervention-definition problem. The current triangle report remains unchanged: its main fixed-support event effect, lack of replicated direction, and operational mean equivalences are the measured results. The original 64-pair primary and the prior confirmation 0.01 question remain unchanged and unresolved.

## Source binding and scope

The verified first triangle archive `Q3_TRIANGLE_SHARD_00.zip` has SHA256 `e96e7c16118ac63e345e498fae2cfd076105d9bcc2ea6ab9c24de3114cd25c60` in the [published campaign](https://github.com/zuizui0223/izu-core/releases/tag/q3-distribution-triangle-20261014). Direct source inspection, without importing or executing the model, confirms:

- `frozen_source/scripts/model3_island/reproduction.py:16` uses `state.alleles.mean(axis=2)` for traits. Source SHA256: `a1d2ad76a2b0d22cda19606fd7d115c3a0506c6dad05e49f3177cbd13ee51c82`.
- `frozen_source/scripts/model3_island/simulate.py:50-51` records the individual allele means and their population mean. Source SHA256: `49780718fba3a152869eec0db83259ee546833ee552bfc939905aa246a962099`.

Fixed original support follows from the declared no-I-mutation/no-arrival intervention and inherited-allele model; here it is also an explicit proposed-maintenance constraint. A maintenance policy with new I alleles need not satisfy that constraint. The 72-loss observation and its post-treatment caveat are in the [existing-record report](CHAPTER2_Q3_EVENT_CONDITIONS_RESULTS_20261014.md); the new triangle results are in the [results report](CHAPTER2_Q3_TRIANGLE_RESULTS_20261014.md).

This establishes a necessary feasibility restriction and an exact endpoint impossibility, not a causal maintenance effect, an explanation of every realised path, or a result about Q1/Q2/Q4 or natural-history causes. The broader goal remains open where actual intervention effects have not been measured or identified.
