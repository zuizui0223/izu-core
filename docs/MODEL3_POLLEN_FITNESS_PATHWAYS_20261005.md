# Pollen limitation, investment and selfing: implemented pathways

## Biological rules, not an imposed syndrome

Source: `scripts/model3_island/reproduction.py` and `population.py`, inspected 2026-10-05. The formulas below explain the existing implementation; no biological rule or parameter is changed.

Let z be attraction investment, a autonomous-selfing capacity, x matching position and delta inbreeding depression. The ovule budget is O = O0 exp(-c_z z^2 - c_a a^2). Investment and matching jointly determine affinity to visitors, pollen export and pollen receipt. Pollen transfer excludes return to the same individual. Receipt produces a saturating outcross fertilization fraction p = 1 - exp(-receipt/(2 pollen_scale)).

In delayed selfing, outcross offspring F = O p, raw selfed offspring S = a(O-F), and viable selfed offspring V = (1-delta)S. Maternal viable output is F+V. Prior selfing instead reserves Oa ovules before outcrossing, giving F = O(1-a)p and S = Oa. The two reported settings also differ in capacity cost, so their contrast cannot isolate timing alone.

The pollen assay compares natural receipt against saturating outcross pollen while retaining the relevant allocation order. It is an intervention diagnostic, not the empirical log-response ratio used in Q1.

## Where fitness enters

Outcross parent-pair contributions and viable selfed offspring form a nonnegative parental matrix. Its sum determines the Poisson number of potential resident offspring. Finite vacancies limit recruitment; parental pairs are sampled in proportion to their contributions. Mendelian transmission and mutation then determine offspring traits. Thus reproduction influences both recruitment and inherited composition. Maternal output alone is not the full measure of evolutionary contribution: pollen export can sire offspring on other plants. The fixed-plant diagnostic uses half maternal outcross contribution plus half paternal outcross contribution plus viable selfed offspring.

This is a finite-population reproductive process, not a supplied target phenotype or an externally prescribed fitness optimum. Absolute viable production, relative genetic contribution and realized recruited offspring are distinct quantities. Capacity-limited recruitment can conceal differences in potential offspring when all vacancies are filled.

## Two distinguishable pathways

1. Visitor pathway: limited arrival changes pollen availability and the net reproductive return to investment at a fixed plant state. Identical plants at capacity0.5 showed a positive-to-negative mean investment contribution derivative between near and far visitor exposures at snapshot400. Composition and richness vary together, so this is not a richness-only effect.
2. Capacity pathway: changing autonomous-selfing capacity alters allocation and the reproductive consequences of pollen receipt. Capacity evolution can modify investment trajectories. It need not be a prerequisite: all8,192 fixed/evolving intervention cases are complete, and investment declines in the fixed-capacity far treatment.

Both pathways can operate together. Fixed capacity is not fixed realized selfing: even delayed selfing with constant a produces more selfed offspring when fewer ovules are outcrossed. The existing intervention excludes a requirement for capacity evolution, not all effects mediated through realized selfing. A complete mediation percentage has not been estimated.

Investment costs are unchanged across isolation treatments. Describe reduced returns relative to the same costs, not increased intrinsic physiological cost. Outcross derivatives also contain allocation costs and must not be relabelled pure benefits.

## Why inbreeding depression does not eliminate reproductive assurance

At fixed allocation in the delayed setting, maternal output is O[p+(1-delta)a(1-p)]. Increasing a can rescue unfertilized ovules, but its allocation cost can oppose that gain. Increasing pollen receipt can still improve offspring viability: the partial derivative with respect to p is O[1-(1-delta)a]. This is a conditional maternal identity, not the full selection gradient; male function, allocation and population competition also matter. At delta0.5, selfed offspring retain half the stipulated viability. Depression is fixed, not generated from an evolving deleterious load; purging is not simulated.

## Supported conclusion and boundaries

Capacity can cross a declared change threshold before investment declines, yet investment decline also occurs without evolving capacity. Temporal precedence therefore does not establish a selfing byproduct. Threshold crossing is not the earliest infinitesimal onset, and equally sized changes on abstract trait axes need not be biologically equivalent.

Pollen shortage at fixed plants and compensation in evolved plants are compatible. A smaller fractional seed deficit need not mean more viable offspring. This connects Q1 H3 and H4 conceptually, while H1 and H2 motivate the trait trajectories and pathway controls. Flower colour, open accessibility and four regional responses are not directly represented.

Evidence: MODEL3_FIXEDPLANT_RETURNS_RESULTS_20261005.md; MODEL3_PERSISTENT_PROCESS_RESULTS_20261005.md; MODEL3_ASSURANCE_INTERVENTION_RESULTS_20261005.md; MODEL3_POLLEN_ASSAY_RESULTS_20261005.md; MODEL3_TRAIT_POLLEN_RESULTS_20261005.md. Numerical ABM/deterministic/diffusion closure remains pending.

## Existing full-contribution threshold, and its narrower scope

The repository already implements `investment_invasion_terms` and `syndrome_thresholds` in `scripts/model3_island/selection.py`. These retain male contribution and should be used instead of presenting the maternal identity as a full evolutionary threshold. They describe a rare mutant in a fixed monomorphic resident at capacity, not the exact heterogeneous48-plant assay.

For delayed selfing, write F=Oq and V=(1-delta)aO(1-q), where q is outcross fertilization probability. At mutant=resident the reference genetic contribution is W=F+V. Let q_z be the change in the mutant's fertilization probability with investment, holding resident pollen/competition fixed; let e_z be pollen-export elasticity. The implemented investment gradient is:

beta_z = { [0.5-(1-delta)a] O q_z + 0.5 F e_z - 2 c_z z (0.5 F+V) } / W.

This separates three effects: recipient-side outcross gain minus displaced viable selfing, paternal export gain, and ovule-allocation cost. Thus 'attraction benefit' cannot be reduced to seed production alone. At the current delta0.5, the recipient coefficient is0.5(1-a), nonnegative but decreasing with capacity. Male benefit can remain. The formula does not prescribe how q_z or e_z must vary with isolation: those follow from the visitor/transfer model.

At the same rare-mutant scope, the delayed-selfing capacity gradient is:

beta_a = { (1-delta)(1-q) - 0.5 d q - 2 c_a a[0.5q+(1-delta)a(1-q)] } / [q+(1-delta)a(1-q)],

where d is the configured pollen-discount coefficient. Its terms are reproductive assurance, foregone paternal export and capacity allocation cost. A parameter being available in the model does not imply it is positive in every experimental setting.

The joint local syndrome direction requires beta_z<0 AND beta_a>0. This is a state-dependent pair of inequalities, not a universal threshold of island distance, a global equilibrium, a time-order prediction or proof of the ABM trajectory. It specifies what to measure: pollen fertilization level q, responsiveness q_z, export response e_z, selfing capacity and costs. The same low pollen level can give different investment gradients if the responsiveness of transfer differs.

To discriminate pathways further, preserve the original frozen simulations and declare diagnostic interventions separately. Existing evidence does not hold realized selfing constant, nor separate visitor richness from composition. Do not infer either missing separation from the fixed-capacity result.
