# Final Model3 architecture and workflow

## One generative biological model, parallel realizations

Model3 defines island visitor arrival/loss, pollen transfer, ovule and pollen budgets, reproductive assurance and its trade-offs, Mendelian inheritance, mutation at gamete transmission, recruitment, survival and optional plant immigration. It does not encode an island floral optimum. Chapter1 is motivation, never a parameter-fitting or acceptance target.

    Common ecological/reproductive/genetic rules
      |-- finite ABM: individuals and finite sampling
      |-- deterministic genotype population:
             |-- original birth-mutation jump kernel (reference)
             |-- reflecting heat-PDE birth mutation (approximation)

ABM is not downstream of deterministic propagation. Deterministic density is not asserted to be the exact expectation of the finite ABM. Finite pollen self-exclusion, demographic sampling and nonlinear regulation can produce differences.

## Mathematical representation, not additional model numbers

The deterministic genotype grid is a numerical representation. Its continuous-genotype counterpart is an integral-difference formulation of sexual inheritance. The exact mutation kernel is a Bernoulli mixture of identity and reflected Gaussian jumps. The PDE option replaces that component by a reflecting heat semigroup in the small-jump approximation; sexual reproduction remains integral/difference. No adult phenotype diffusion is substituted for Mendelian genetics.

The existing phenotype replicator map/ODE and invasion-threshold equations are explanatory reductions/diagnostics, not extra biological engines. Their claim scope is local selection or reduced fidelity, not full inherited trajectories.

## Analysis workflow

1. Specify ecological conditions independently of floral outcomes.
2. Generate shared visitor histories and founder states.
3. Calculate local rare-mutant selection/thresholds when asking which direction is favoured.
4. Propagate the same declared conditions through parallel ABM and deterministic reference.
5. Compare the birth-PDE approximation against the reference, separately from the finite-population comparison.
6. Report selection, evolved traits, persistence and common-environment memory separately.

## Finalization gates

The architecture is fixed here. The full-mutation campaign has completed all 4,368 declared cases. ABM repetition precision passed at the prespecified maximum. Positive-mutation density grid precision failed, so a quantitatively validated continuum replacement has not been established. This does not redefine the reference model or invalidate the independently supported ABM result. See `MODEL3_FULL_MUTATION_RESULTS_20261004.md` for the complete distinction between campaign completion and numerical fidelity.

The focal full-validation campaign allows allthree traits(access,investment,assurance) to evolve, uses two declared assurance settings, and compares isolation histories followed by identical current visitors. It is synthetic, not an estimate of geological time or a reconstruction of Chapter1 regions. Finite-horizon memory is not a claim of alternative stable attractors.

## Concrete ecological rules in this campaign

Each plant carries two alleles at each of three unlinked loci. Their mean
defines access/matching position, floral investment, and reproductive
assurance on [0,1]. These are abstract functional traits, not calibrated
flower colours or measured selfing rates. Assurance is capacity to self;
realized selfed recruitment also depends on pollen supply, timing and
inbreeding depression.

Visitor immigration candidates are Poisson with mean `0.3 exp(-distance)`
per reproductive period and establish with probability 0.8. Distances 0
and 3 therefore give expected established arrivals 0.24 and about 0.01195.
Each visitor disappears with probability `1-exp(-0.05)` per period. Both
arms begin with four visitor types; matching optima are sampled uniformly.
Only immigration distance differs between arms during the first 200 periods.
Afterward both receive exactly the near arm's next 800 visitor states.
This is a controlled environmental equalization, not a claim that an island
physically approaches the mainland. No distance in kilometres is assigned.

Affinity equals `(0.1 + investment) exp(-((access-optimum)/0.2)^2)`.
Investment raises attraction but reduces ovule supply through its cost.
Pollen export and outcross fertilization saturate; donor and recipient
competition are explicit. Selfed offspring viability is multiplied by 0.5.
The focal delayed-assurance case also imposes assurance cost 0.5; the
prior-selfing comparison has assurance cost zero. They are two joint settings,
not a factorial isolation of timing versus cost.

Capacity is 48, adult survival zero, and each period replaces the adult cohort.
Time is consequently a reproductive generation in this annual setting,
without calibration to calendar or geological years. The legacy configuration
field is named `years`/`reproductive_year`; that name supplies no calibration.
Mutation occurs per transmitted allele with probability 0 or 0.01 and
reflected Gaussian step width 0.05. All three loci are allowed to mutate.

ABM samples recruitment, parents and segregation. Deterministic propagation
retains fractional genotype abundances and uses continuous density regulation.
It also does not remove an individual donor's own pollen as the finite ABM
does. Thus an ABM-minus-density contrast combines finite genetic/demographic
sampling, pollen self-exclusion and nonlinear regulation; it is not by itself
a causal estimate of drift alone.

## PDE role and chronology

Let H(t) denote reflecting heat diffusion on the allele interval. The original
birth mutation is `(1-u) I + u H(sigma^2/2)`, while the diffusion approximation
is `H(u sigma^2/2)`. Agreement to leading small-jump order does not imply
equality at fixed u and sigma. Numerical grid error and this approximation
error are tested separately. Sexual reproduction remains an integral/difference
operation in both descriptions.

Mutation/history tests were motivated by earlier exploratory results; the
subsequent full campaign was specified before its outcomes. The latter
does not retrospectively make the former confirmatory. PDE remains a candidate
main result if its validated comparison adds evolutionary understanding;
its rhetorical placement is not a scientific acceptance criterion.
