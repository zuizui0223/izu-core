# Model 3 PDE closeout plan — 2026-10-04

Base: 4b7d7bc7. User authorizes validation through completion. Preserve all frozen biological operators and outcomes. This is a post-hoc approximation audit, not a new preregistered biological hypothesis.

## Completion contract
Identify the exact nonlocal inheritance representation; determine what the existing reduced equation approximates; separate numerical error, continuous-time approximation, and phenotype closure error. Finish code/tests, archive full diagnostics with source hashes, and revise active claims. A failed approximation is a completed finding, never a reason to retune.

## Fixed diagnostics before execution
1. Same frozen 25 controlled access/community cells; initial genotypes unchanged; horizons 60, 200, 800 reproductive periods. Compare exact density, phenotype map, and normalized replicator ODE on identical initial phenotype support. Report mean/variance discrepancies, signs (zero tolerance 1e-10), mass, positivity. No calibration to real years or equilibrium claim.
2. Repeat ODE with rtol 1e-8/atol 1e-10 and rtol 1e-10/atol 1e-12. Numerical agreement target 1e-6 for terminal mean. Explicit weak-update maps with h=1, .5, .25, .125 at time 60 test continuous-time convergence; h changes the reduced update, not the frozen sexual model.
3. Exact counterexample to phenotype-only closure: identical phenotype .5 represented by .5/.5 versus .4/.6 investment genotypes, identical access/assurance and community. Compare next-generation mean and variance. This tests information loss, not island branching.
4. Mutation kernel: retain existing spectral audit; separate mutation probability from small-jump limit. Do not copy per-allele diffusion directly into diploid phenotype PDE. Correct overstatements about variance and reflecting boundaries.
5. Run existing continuum/Price/bridge audits and tests. Archive diagnostics and source hashes. Update active SI/manuscript with discrete-map versus continuous-time distinctions, and explain ecological significance.

Implementation: one additional audit module and tests; minimal documentation corrections. No new ecosystem parameters, no changed seeds, no new ABM campaign. Exact continuous genotype measure dynamics remain nonlocal; no claim of a proven full sexual-model PDE limit. Long-term finite evolution/branching is a separate goal from closing this approximation audit.


User steering: connect the independently tested Chapter 2 to Chapter 1 as pattern to candidate mechanism, without fitting Q1 regional outcomes. The model must generate syndrome directions from ecology rather than impose them. Added algebraic local joint cost thresholds to the already corrected fixed-resident operator; independently check all 45 states x 4 settings x 5 communities, including sign and equality at feasible cost boundaries. No new empirical calibration or retuning. The PDE closeout's scientific role is to separate selection direction from inherited dynamics.
