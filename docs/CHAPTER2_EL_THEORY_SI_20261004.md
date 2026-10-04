# Supporting Information: continuous reduction and analytic threshold for Model 3

**Scope.** This supplement derives the continuous and low-dimensional reductions used only to interpret the already frozen Model 3 results. It does not replace the finite ABM or the deterministic genotype-density closure, and it does not calibrate any named island system.

## S1. Four mathematical levels

The same biological operator can be represented at four levels.

1. **Finite ABM.** Explicit diploid individuals, Mendelian inheritance and finite demographic sampling.
2. **Deterministic genotype density.** Discrete diploid genotype masses with the same reproduction and inheritance operator but no demographic sampling.
3. **Exact continuous-genotype system.** Genotype sums are replaced by measures and integrals. Sexual reproduction still integrates over maternal state, paternal state and their gametes, so the exact continuous system is a nonlinear nonlocal integro-difference equation.
4. **Reduced continuous phenotype equation.** Genotype structure is collapsed to a phenotype density. Under additional closure assumptions this becomes a replicator or replicator-mutator equation.

The third level is not a PDE. The fourth level is a reduced approximation and is evaluated against the first three.

## S2. Mutation has a genuine diffusion limit, but the focal bridge has D = 0

Model 3 mutates transmitted alleles with probability u by a reflected Gaussian step with standard deviation sigma on the interval [0,1]. The reflected-normal kernel is the Neumann heat semigroup. For weak mutation,

    D = u sigma^2 / 2

is the diffusion coefficient per mutable transmitted allele.

The numerical audit compared the implemented mutation matrix with Neumann heat-semigroup eigenmodes. Maximum discretization error declined from approximately 3.13e-5 at 51 nodes to 1.96e-6 at 201 nodes, and the weak-mutation approximation improved at the expected order as sigma decreased.

The focal isolation bridge has mutation_rate = 0. Therefore D = 0 in that analysis. The island-like investment response is not produced by a hand-coded diffusion toward an island optimum.

## S3. Exact one-generation Price identity for additive trait means

Let z_g be an additive expressed trait of genotype g and p_g its adult frequency. Define total parental-genome contribution per adult genotype as

    w_g
      = 0.5 * maternal outcross contribution
      + 0.5 * paternal outcross contribution
      + viable selfed seed contribution.

The selfed term enters once rather than one half because both gametic copies in a selfed offspring come from the same parent.

With mutation = 0, immigration = 0 and survival = 0, uniform capacity thinning changes total offspring number but not the offspring trait mean. Mendelian segregation preserves the expected parental allele value for an additive trait. Hence

    mean(z)' = sum_g p_g w_g z_g / mean(w)

and therefore

    mean(z)' = mean(z) + Cov(z,w) / mean(w).

This is the standard Price covariance identity applied to the explicit Model 3 parental-genome ledger, not a new theorem.

### Numerical validation

For the frozen reduction audit, five starting access states were crossed with five visitor communities. In all 25 cells, the Price update matched the next-generation mean investment from the exact deterministic genotype-density operator to numerical precision (maximum absolute error below 1e-12).

A later multivariate audit extends the same accounting to access, investment and evolving assurance; that extension is kept outside this locked SI until its separate rare-mutant validation is complete.

## S4. Reduced phenotype replicator equation

Collapsing genotype structure to an investment phenotype density p(i,t) gives the reduced equation

    dp/dt = (w(i; p, V) / mean(w) - 1) p + D d2p/di2.

For the focal bridge D = 0, so the operative reduction is a frequency-dependent replicator equation rather than a diffusion-driven PDE.

No context-specific coefficient was fitted to reproduce the frozen responses. The fitness function uses the same visitor affinity, pollen export, recipient competition, outcrossing, delayed assurance and investment-cost terms as Model 3.

### Controlled 60-season fidelity

Across the 25 fixed visitor-community cells:

- deterministic genotype density and the reduced continuous equation agreed in response direction in 25/25 cells;
- mean absolute investment error was approximately 0.00434;
- maximum absolute investment error was approximately 0.01234.

Thus the reduced selection field captures the coarse direction and much of the mean trajectory in controlled environments.

## S5. Frozen isolation bridge confrontation

The reduced continuous phenotype selection model was then applied to the exact 128 frozen visitor-history seeds and the same projected founders.

| Intervention | Exact genotype-density mean far-minus-near investment | Reduced continuous mean |
| --- | ---: | ---: |
| Natural | -0.450983 | approximately -0.251735 |
| Response-blind richness matched | +0.033757 | approximately +0.022762 |
| Visitor-history pooled | -0.556042 | approximately -0.325516 |

The reduction recovered:

- 9/9 start-by-intervention signs;
- the same ordering: pooled < natural < richness-matched;
- correlation approximately 0.987 between the nine reduced and exact condition means.

The reduced-versus-exact slope was approximately 0.586, so the reduction systematically attenuated magnitude. This is the useful boundary: the local phenotype selection field contains the directional regime, whereas explicit sexual inheritance contributes substantially to the inherited magnitude.

## S6. Analytic investment threshold

For an occupied monomorphic state with delayed assurance, Model 3 parental fitness can be written

    w(i) = O0 exp(-c_I i^2) [ r + (1-r) q(i) ],

where

    i = floral investment,
    c_I = investment cost,
    q(i) = outcrossed-ovule fraction generated by the visitor-transfer operator,
    r = a (1-delta),
    a = reproductive assurance,
    delta = inbreeding depression.

Differentiation gives

    d log(w) / di = B(i) - C(i),

with

    B(i) = (1-r) q'(i) / [ r + (1-r) q(i) ],
    C(i) = 2 c_I i.

Therefore investment increases locally when B(i) > C(i) and decreases when B(i) < C(i).

No island label, distance coefficient or island optimum appears in this condition. Isolation affects direction only through the visitor environment and therefore through q and q'.

## S7. Threshold validation on all frozen visitor histories

The threshold was evaluated on

    5 access states x 3 investment states x 128 visitor histories.

For natural near-to-far isolation, every history in every tested state shifted the selection margin toward lower investment.

At access = 0.50, the mean far-minus-near shifts were approximately

    investment 0.30 : -0.803337
    investment 0.50 : -0.651279
    investment 0.70 : -0.497247.

Visitor-history pooling strengthened the negative shift:

    investment 0.30 : -0.921111
    investment 0.50 : -0.755125
    investment 0.70 : -0.561365.

Response-blind annual visitor-richness matching removed the universal shift and left the mean difference close to zero:

    investment 0.30 : +0.016611
    investment 0.50 : +0.016624
    investment 0.70 : +0.015152.

This parallels the exact genotype-density intervention ordering and identifies the visitor-mediated marginal return as the directional mechanism.

## S8. Why the variance does not close in the same way

The same one-generation reduction was applied to investment variance. After the identical phenotype-selection step, exact Mendelian inheritance sometimes increased and sometimes decreased the next-generation variance relative to the phenotype-only closure.

The sign of the inheritance correction therefore depends on ecological and genotype context. A single context-independent nonnegative diffusion coefficient cannot exactly represent sexual inheritance. Mating averages parental states while Mendelian segregation can re-expand variation, and their balance changes with the current population.

This does not imply that history reliability is literally a second-moment statistic. It does show that exact closure of the mean does not imply closure of the higher-order inheritance structure that controls how effect magnitude is distributed among histories and genotypes.

## S9. Reinterpreting the failed assurance-by-cost robustness route

The preregistered Route A robustness surface found that the activity value at which the investment gradient crossed zero moved with inbreeding depression:

    delta = 0.25 : activity approximately 0.182
    delta = 0.50 : activity approximately 0.096
    delta = 0.75 : activity approximately 0.040.

The threshold explains the direction of this movement. Since r = a(1-delta), increasing delta lowers r. For q'(i) > 0, the marginal pollination term B(i) increases as r falls. A stronger reduction in pollination opportunity is therefore required before B(i) falls below C(i), so the crossing moves to lower visitor activity.

This does not rescue Route A as a universal mechanism. Its inherited sign still failed the preregistered life-history robustness rule. Instead, the failed robustness surface becomes a mapped boundary of the same reproductive-return equation.

## S10. Novelty and precedent boundary

None of the following is claimed as new:

- the Price covariance identity;
- allocation costs of pollinator attraction;
- reproductive assurance as a benefit of selfing under pollen limitation;
- pollen discounting and prior-selfing thresholds;
- reduced floral display associated with selfing;
- pollen limitation allowing multiple reproductive solutions.

The relevant precedents include Price (1970), Lloyd (1979), Porcher & Lande (2005), Harder & Aizen (2010), and Teixido & Aizen (2019).

The narrower contribution is the bridge across representations of one explicit island-floral operator: stochastic visitor assembly changes pollen transfer; the same operator yields the finite ABM, deterministic genotype-density system, exact nonlocal continuous system, reduced replicator equation and analytic investment threshold; and the threshold predicts the frozen near/far intervention structure without fitting a named island or imposing an island optimum.

## S11. Reproducibility files

The theory-integration branch includes the companion audits and tests:

- scripts/audit_model3_continuum_limit.py
- scripts/audit_model3_reduced_pde_selection.py
- scripts/audit_model3_reduced_pde_one_step.py
- scripts/audit_model3_reduced_pde_trajectory.py
- scripts/audit_model3_reduced_pde_second_moment.py
- scripts/audit_model3_reduced_continuum_bridge.py
- scripts/audit_model3_analytic_syndrome_threshold.py
- scripts/audit_model3_analytic_bridge_threshold.py

These analyses are explanatory extensions of the frozen campaign and bridge. They do not alter the original simulation outcomes, visitor histories or validation seeds.
