# Mutation diffusion and common-environment memory — 2026-10-04

User approved extension after PDE-closeout. Parent7ad67eb6. Old frozen numerical biology is preserved by default; new explicit optional interventions freeze mutation on selected trait axes and substitute the reflected heat kernel for the Bernoulli reflected-jump kernel in density only.

## Scientific distinction
Exact birth mutation is (1-u)I+u H(sigma^2/2), applied independently to each transmitted allele. Diffusion approximation is H(u*sigma^2/2). Sexual reproduction remains a nonlocal integral/difference operator. This is a genuine heat-PDE component composed with sexual births, not a pure phenotype PDE or a continuous-time replacement of reproduction.

## Fixed prospective diagnostic design
- One mutable investment locus; fixed access=.5 and assurance=.5; same Mendelian, pollen, cost, selfing and demographic machinery. No inference to joint-assurance evolution or Chapter1 regions.
- Same48 founders, investment genotypes .4/.4,.4/.6,.6/.6 equally represented. For capacity192 clone/reindex the same genotype proportions.
- Past200 reproductive periods: center4 visitors [.35,.45,.55,.65] versus no visitors. Then both environments use center4 for800periods. All periods use fixed visitor activity. Absence is an explicit contrast, not universal island history.
- Mutation rates0 and .01, sd=.05. These are declared synthetic perturbations, not inferred natural rates. No tuning to produce alternative endpoints.
- Density: allele nodes11,21,41; exact-jump and heat approximation at each. Report common-time means, variance, full distributions, mass and late drift. Numerical acceptance for fine-grid terminal mean change<.005 and exact/heat gap<.005; failure means unresolved fidelity, not biological null.
- Finite ABM: capacities48,192; seeds6101..6108; both histories and mutation settings, continuous allele mutation. Eight repeats are an initial diagnostic only, not a powered claim of rare alternative states. Matched seeds reduce noise but do not remove history effects. Archive trajectories and occupancy, report uncertainty; if intervals span zero report unresolved.
- Report memory as paired historical mean difference after common environment at0,200,800 periods, conditional on occupancy plus unconditional extinction. No two-attractor claim from finite horizons.

## Execution
1. Add tested opt-in mutation-axis mask to inheritance/advance/simulate and density; unchanged defaults and RNG draw counts.
2. Heat-kernel option only in density; test mass, positivity, u=0/u=1 equivalence, small-jump convergence and frozen-locus behaviour.
3. Run all declared density and finite cases, store trajectories/source hashes and precision diagnostics. Code-level tests precede full runs.
4. Review results independently; distinguish validation completion from numerical/scientific support. Full three-trait PDE, new natural calibration and purging are outside this diagnostic.
