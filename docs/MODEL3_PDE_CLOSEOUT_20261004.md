# Model 3 PDE closeout and generative syndrome thresholds — 2026-10-04

## Scientific purpose

Chapter 1 asks whether the island syndrome is visible in global floral patterns. Chapter 2 independently asks when island ecological processes generate syndrome-direction selection and how inherited, finite populations realize it. Chapter 1 motivates the question but supplies neither fitted regional parameters nor success targets. Floral investment is not literal colour; assurance is not a complete realized mating-system measurement. No fitted reconstruction of Earth's islands is claimed.

Isolation enters the frozen bridge through visitor-arrival distance (near 0, far 3), not a floral optimum or a directional evolution rule. The generated visitor history enters pollen transfer and reproductive costs, then sexual inheritance. Plant immigration is zero in this focal bridge: it is a visitor-connectivity experiment in closed plant populations, not a complete model of all island assembly processes. Species pools, affinity kernels and cost functions remain assumptions. Delayed assurance without costs is a structural positive control, not independent evidence for selfing evolution.

## What is complete

The exact continuous genotype formulation remains a nonlinear nonlocal sexual-inheritance integral update. Symbolically, births are obtained by integrating maternal and paternal genotype measures against the reproductive-output and inheritance kernels, with a separate selfed term. Replacing sums by integrals does not remove Mendelian segregation or make that update a local PDE.

The existing reduced phenotype model instead removes explicit genotype inheritance. Its discrete map is p_next proportional to p*w; its normalized continuous-time limit is dp/dt=(w/mean(w)-1)*p. At zero mutation, D=0: this audit is an ODE for masses on fixed atomic support. The full128-history reduced bridge used the discrete map, not the continuous-time ODE. Documentation now makes that distinction explicit.

## Completed diagnostics

Same frozen 25 fixed-community cells, identical initial genotypes, no changed biology:

| Reproductive periods | Matching mean-change directions | ODE versus sexual-density mean absolute error | Maximum error |
|---|---:|---:|---:|
| 60 | 25/25 | 0.004337913 | 0.012341680 |
| 200 | 25/25 | 0.000897042 | 0.006333844 |
| 800 | 25/25 | 0.000000162 | 0.000001979 |

Tightening the ODE solver tolerance changed terminal means by at most 2.39e-12. Mass error was at most 1.03e-14 and recorded masses were positive. For the reduced map alone, halving the weak-update time step halved mean L1 error against the ODE: 0.00228849, 0.00114533, 0.00057294, 0.00028653. This checks its continuous-time limit, not a continuous-time limit of the full sexual model.

The long-horizon agreement is conditional on the same bounded founder support and fixed environments. It does not establish continuous-founder convergence, realistic geological time, global equilibria or island branching. Comparable end means do not imply equivalent transient genotype structure.

## Why the exact model retains genetics

Two populations have exactly the same phenotype distribution, investment=0.5, and the same ecology. One consists of 0.5/0.5 homozygotes, the other of 0.4/0.6 heterozygotes. The next-generation means both equal0.5, but variances are0 and0.005. An autonomous phenotype-only equation supplied the same state cannot predict both. Additional genetic state or explicit closure assumptions are necessary. This is a stronger diagnosis than claiming that positive and negative variance corrections alone rule out diffusion; reflecting boundaries can affect variance.

Ecologically, plants with the same current flowers can carry different hidden variation and therefore generate different offspring variation. This is a mechanism-level possibility, not evidence that it caused Chapter1's four-region differences.

## Genuine diffusion component

Reflected allelic mutation has a heat-kernel interpretation. The local small-jump coefficient is u*sigma^2/2 per transmitted allele. At fixed diffusion time, repeated exact-kernel eigenvalues approach the heat equation across three modes as jump size decreases. Merely making jumps rarer at fixed size gives a nonlocal jump generator. The allelic coefficient must not be copied unchanged into a diploid phenotype equation. No full positive-mutation phenotype PDE was fitted or substituted for the sexual operator.

## Joint syndrome generation conditions

The corrected rare-mutant fitness is W=F/2+P/2+S, holding resident pollen supply and recipient competition fixed. Let investment=i, assurance=a, viable selfed fraction=v=1-delta, pollen-discount coefficient=d, and resident outcross fraction=q. For delayed selfing use f=q and l=1-q; for prior selfing use f=(1-a)q and l=1. Put s=a*v*l, M=f/2+s, and J=1 for prior selfing, zero otherwise.

    c_a* = [v*l - J*q/2 - d*f/2] / (2*a*M)
    c_i* = B_i*(f+s)/(2*i*M)

B_i is the corrected fixed-resident marginal investment benefit, including female and male function. For interior i,a, positive fitness and M>0:

    investment decreases under local selection iff c_i > c_i*
    assurance increases under local selection iff c_a < c_a*

The overlap is the local syndrome-direction region. Thresholds depend on the resident and visitor environment, are not imposed optima, and may be negative. They must not be clipped. Selection shifts with isolation need not cross either zero; covariance and finite dynamics can also prevent joint realized change. The formula is conditional on this model, not a new universal selfing law or a measured distance threshold.

Independent finite differences across45 states x4settings x5communities (900cells) match both analytic gradients, maximum error1.25e-9. Additional tests check equality at feasible cost thresholds, prior/delayed timing, empty visitors and the corrected investment gradient.

## Chapter 2 conclusion and Chapter 1 connection

Island visitor assembly changes the marginal reproductive return of floral investment and reproductive assurance. These changes yield explicit local conditions for syndrome-direction selection without entering an island floral optimum. Sexual inheritance and finite population processes determine how that selection is realized. The reduced model helps explain direction; it cannot replace the genetic state in general.

Compare these predictions with Chapter1 only after independent derivation. Shared trends provide qualitative consistency; regional differences motivate possible mechanisms but are not explained merely by naming visitor groups. This closeout does not supply a natural-island calibration, proof of the observed floral-colour mechanism, or evidence for two stable island attractors. Previous46/48 G-beta gates and failed endpoint branching remain unchanged.

## Reproduction and evidence

- scripts/audit_model3_pde_closeout.py → data/results/model3_pde_closeout_20261004.json
- scripts/audit_model3_continuum_limit.py → data/results/model3_mutation_limit_closeout_20261004.json
- scripts/audit_model3_joint_thresholds.py → data/results/model3_joint_thresholds_20261004.json
- New threshold implementation: scripts/model3_island/selection.py (no reproductive or inheritance operator changed).
- Full25x800 controlled audit,900gradient checks, existing 12 continuum/bridge/Price tests and a final 36 focused, document and artifact-budget tests passed. This is not full repository CI.

The PDE approximation audit is completed within these declared boundaries. A genuinely new positive-mutation phenotype closure or empirical calibration would be a new model/validation project, not an unreported extension of this one.


## Historical dependence versus alternative endpoints

The pre-existing fixed-assurance bridge has independently validated differences among visitor histories in continuous evolution magnitude. That result is distinct from the evolving-assurance finite follow-up, whose opposite endpoint remains below3% and whose frozen branching rule failed. Neither result by itself proves persistent memory after different histories are switched to an identical current environment, nor two attractors under one stationary environment. Those common-environment persistence tests were not part of this PDE closeout and were not performed here.
