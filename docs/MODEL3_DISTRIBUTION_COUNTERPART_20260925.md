# Individual model and its distribution counterpart

Status: mathematical derivation and implementation contract; not a completed PDE experiment. Q1 is inspiration only.

## What the current simulator is

Plant individuals carry two diploid loci. Visitor entries are functional types; their assembly is stochastic external forcing. The simulator is an individual-based stochastic eco-evolutionary model, with synchronized annual reproduction and overlapping adult cohorts when survival is positive. It is not spatial, and no individual pollinator flights are tracked.

## Faithful deterministic object

Let n_t(g) count plants with genotype g, H(g' | g_m,g_f) be the exact two-locus independent Mendelian offspring kernel, and B_t(g_f,g_m;n,C) be the expected viable offspring ledger, including delayed selfing on the individual-level diagonal. B is computed from the same visitor activity, finite effective pollen dose, ovule investment and mating rules as the individual model. Define total viable expectation b_t = sum B and the offspring distribution

q_t(g') = sum_{f,m} B_t(g_f,g_m) H(g'|g_m,g_f) / b_t.

When b_t=0, set recruitment identically zero; do not normalize an empty distribution.

Conditional on the current integer population, survivor count S is Binomial(N,s), potential recruits Z are Poisson(b_t), and S and Z are independent. The exact conditional one-step expectation is

E[n_{t+1}(g') | n_t,C_t] = s*n_t(g') + q_t(g')*E[min(Z,K-S)].

This equality concerns the conditional expectation of **counts**, not the expectation of survivor-conditioned mean traits. The shared density cap makes recruitment stochastic, but thinning is independent of offspring genotype, which permits the factorization. It does not establish that iterating expected counts equals the expectation of whole stochastic paths: generally E[F(n)] != F(E[n]).

An infinite-density deterministic closure has the schematic form

n_{t+1} = s*n_t + min(b_t,K-s*N_t)*q_t.

This is an **integrodifference/reproduction-operator model**, not a PDE. A justified large-population comparison must scale background pollen loss with carrying capacity, hold density and activity fixed, and derive the vanishing individual self-exclusion correction. Simply inserting fractional genotype counts into an individual diagonal-exclusion matrix is wrong. Mendelian selfing remains separate and does not vanish in that limit.

## Why a PDE is an additional limit

A continuous-time age-structured formulation could use a transport equation in age, with death and a nonlocal reproductive boundary carrying H. But annual synchronized births imply impulses or a year-to-year map. Annual survival zero cannot be replaced by a finite constant death rate through -log(s). A diffusion term in floral trait space would further require a stated mutation/small-step limit; the current model has no mutation, so inserting positive trait diffusion would change the biology and restore variation that the individual model can lose.

Primary mathematical precedent: [Champagnat, Ferriere & Meleard (2006), Unifying evolutionary dynamics](https://doi.org/10.1016/j.tpb.2005.10.004), [author-hosted paper](https://nchampagnat.perso.math.cnrs.fr/TPBlatex63.pdf). Its individual-to-macroscopic framework distinguishes deterministic integral/differential limits and stochastic limits according to scaling. It does not prove convergence for this new sexual-reproduction model. A sexual-hermaphrodite precedent is [Rudnicki & Zwoleński, Model of phenotypic evolution in hermaphroditic populations](https://doi.org/10.1007/s00285-014-0798-3): a nonlocal inheritance kernel belongs in the population distribution equation. Abstract-level evidence was checked; no theorem is transferred to this model.

## Comparison to implement and verify

Use the same inheritance kernel, initial genotype support, visitor histories and reproductive accounting. First verify one-step mean counts against repeated individual transitions at a fixed state, then examine finite-population scaling. Separate conditional-on-one-visitor-history deterministic dynamics from averaging different environmental histories: removing demographic sampling does not remove stochastic island community assembly.

Check population mass, Mendelian moments, positivity, zero-reproduction extinction, self/outcross accounting and numerical discretization error. Compare response time, standing-variation loss, endpoints and extinction; a deterministic path that remains positive is not evidence that finite populations persist. Common-mean paths can conceal opposing individual histories. Report runtime only after measurement; a high-dimensional inherited-genotype distribution can cost more than an individual model.

The current implementation and campaign therefore cannot yet claim an ABM-versus-PDE result. The primary campaign tests individual population and time-scale sensitivity; this mathematical comparator is a separately auditable extension.

## Matched initial conditions for the next comparison

`founder_density` supplies the law obtained by projecting independent uniform
founder alleles onto equally spaced nodes. Endpoint nodes have half the
probability of interior nodes; an unordered heterozygote has multiplicity two
at each locus. Equal weights over all unordered genotypes are incorrect.
`project_founders` also returns the exact empirical frequencies of a particular
projected finite founding population. A within-history finite-versus-density
comparison must initialize BOTH models from those same projected founders.

Projection is an explicit numerical change relative to the continuous founder
law in the archived campaigns. The archived continuous ABM cannot be relabeled
as the matched discrete-grid ABM. Use a separately declared projected-founder
ABM and document grid refinement, preferably retaining the same continuous
draws before projection. The theoretical founder law is useful for grid-error
diagnostics; it must not replace empirical founders on only one comparison arm.
The projection has measure-zero nearest-node ties resolved by NumPy rounding.
No campaign numerical design or long-term outcome is asserted by these helpers.
