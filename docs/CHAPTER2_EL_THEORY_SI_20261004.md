# Supporting Information: continuous reduction and analytic threshold for Model 3

**Scope.** This supplement derives the continuous and low-dimensional reductions used only to interpret the already frozen Model 3 results. It does not replace the finite ABM or the deterministic genotype-density closure, and it does not calibrate any named island system.

## S1. Four mathematical levels

The same biological operator can be represented at four levels.

1. **Finite ABM.** Explicit diploid individuals, Mendelian inheritance and finite demographic sampling.
2. **Deterministic genotype density.** Discrete diploid genotype masses with the same reproduction and inheritance operator but no demographic sampling.
3. **Exact continuous-genotype system.** Genotype sums are replaced by measures and integrals. Sexual reproduction still integrates over maternal state, paternal state and their gametes, so the exact continuous system is a nonlinear nonlocal integro-difference equation.
4. **Reduced continuous phenotype equation.** Genotype structure is collapsed to a phenotype density. Under additional closure assumptions this becomes a replicator or replicator-mutator equation.

The third level is not a PDE. In other words, the full continuous system is not a PDE; only the reduced phenotype approximation has PDE form. The fourth level is a reduced approximation and is evaluated against the first three.

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

The same accounting was then extended to access, investment and evolving assurance. Across 48 controlled genotype-density cells spanning three founder states, four visitor communities and four assurance trade-off settings, the multivariate Price prediction matched all three next-generation trait means with maximum absolute error 7.2e-16.

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

## S6. Fixed-resident investment invasion threshold (corrected)

Selection changes a rare mutant's investment while holding the resident pollen and recipient environment fixed. Whole-population reproductive sensitivity is a different derivative and can have the opposite sign.

Write F for maternal outcross seed, P for paternal outcross success, S for viable selfed seed, O for ovule production, and W = 0.5 F + 0.5 P + S. At mutant = resident, P = F. Let u=0.1+i, q be resident outcross fraction, rho be resident pollen receipt, and R be pollen export. For delayed assurance with r=a(1-delta):

    q'_mut = exp(-rho/(2*pollen_scale)) * rho/(2*pollen_scale*u)
    F = O*q; S = r*O*(1-q); W = F+S
    B(i) = [(0.5-r)*O*q'_mut + 0.5*F*R'/R]/W
    C(i) = 2*c_I*i*(0.5*F+S)/W
    beta_i = B(i)-C(i).

The paternal term changes through mutant pollen export, not through mutant ovule cost on resident mothers. With no export, its contribution is zero. Prior selfing uses F=O*(1-a)*q and S=O*a*(1-delta); its maternal derivative and selfed derivative are evaluated separately by the same implementation.

The previous expression (1-r)*q'_population/[r+(1-r)*q] - 2*c_I*i changed all resident traits at once. It remains a population sensitivity, but is retired as an evolutionary threshold. At access .2, investment .5 and central four visitors it predicts +0.002989 whereas fixed-resident invasion gives -0.152265, independently matched by the low-frequency genotype-density operator.

No island label or target optimum is added. The corrected gradient is tested against rare-mutant numerical derivatives and exact low-frequency reproduction.

## S7. Threshold validation on all frozen visitor histories

The threshold was evaluated on

    5 access states x 3 investment states x 128 visitor histories.

For natural near-to-far isolation, every history in every tested state shifted the selection margin toward lower investment.

At access = 0.50, the mean far-minus-near shifts were approximately

    investment 0.30 : -0.528074
    investment 0.50 : -0.537250
    investment 0.70 : -0.538250.

Visitor-history pooling strengthened the negative shift:

    investment 0.30 : -0.598511
    investment 0.50 : -0.614043
    investment 0.70 : -0.603867.

Response-blind annual visitor-richness matching removed the universal shift and left the mean difference close to zero:

    investment 0.30 : +0.010550
    investment 0.50 : +0.012642
    investment 0.70 : +0.014214.

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

These frozen activity crossings are retained as earlier numerical results. The retired whole-population derivative cannot establish their invasion-selection mechanism. This correction does not rerun or reinterpret that separate route as universally supported.

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
- scripts/audit_model3_analytic_syndrome_threshold.py (retired population sensitivity only)
- scripts/model3_island/selection.py (corrected fixed-resident gradient)
- data/results/model3_corrected_invasion_bridge_20261004.json
- scripts/audit_model3_analytic_bridge_threshold.py
- scripts/audit_model3_joint_syndrome_vector.py
- scripts/audit_model3_multivariate_price.py
- scripts/audit_model3_joint_G_beta_response.py
- scripts/run_model3_joint_syndrome_finite_followup.py
- data/results/model3_joint_syndrome_rare_mutant_frozen_20261004.json
- data/results/model3_joint_syndrome_finite_frozen_20261004.json
- data/results/model3_joint_syndrome_adjudication_20261004.json

These analyses are explanatory extensions of the frozen campaign and bridge. They do not alter the original simulation outcomes, visitor histories or validation seeds.


## S12. Why assurance requires rare-mutant invasion fitness

Neither investment nor assurance selection can be identified with a derivative that changes the whole resident population. Assurance changes both maternal and paternal transmission. In particular, a selfed seed carries both gametic copies from the same parent, while pollen discounting changes siring success on other plants.

We therefore define a rare mutant with traits `(x_m, i_m, a_m)` in a resident reproductive environment held fixed to first order in mutant frequency. Its expected parental-genome contribution is

    w_mut = 0.5 F_mut + 0.5 P_mut + S_mut,

where

    F_mut = maternal outcrossed seed production,
    P_mut = paternal outcross success on resident mothers,
    S_mut = viable selfed seed.

The selfed term enters with coefficient one because a selfed offspring receives both parental genome halves from the mutant.

Selection gradients are central finite differences of `log(w_mut)` with respect to mutant investment and mutant assurance while resident traits and the resident pollen pool are held fixed.

A low-frequency numerical check embedded one mutant genotype at frequency 1e-7 in the exact deterministic genotype-density operator. Per-capita parental-genome contribution agreed with the analytic rare-mutant expression to the declared numerical tolerance.

## S13. Frozen joint selection-vector design

Before full execution we froze separate criteria for a directional shift and an absolute sign reversal.

The resident grid was

    access    = 0.20, 0.35, 0.50, 0.65, 0.80
    investment = 0.30, 0.50, 0.70
    assurance  = 0.30, 0.50, 0.70,

for 45 resident states, each evaluated on all 128 frozen natural near/far visitor histories.

Four assurance settings were used:

1. delayed selfing with zero direct assurance cost and zero pollen discount, retained only as a structural control;
2. prior selfing, which imposes seed discounting by using ovules before outcrossing;
3. delayed selfing with pollen discount = 1, which penalizes male outcross success;
4. delayed selfing with direct assurance cost = 0.5.

The frozen joint-shift criterion was

    far - near beta_i <= -0.05
    far - near beta_a >= +0.05,

with at least 90% paired-history support and paired-bootstrap 95% intervals excluding zero in the corresponding directions.

The stronger classic sign-reversal criterion required

    near  : beta_i >= +0.05 and beta_a <= -0.05
    far   : beta_i <= -0.05 and beta_a >= +0.05.

These were adjudicated separately.

## S14. Joint rare-mutant results and correlational selection

All 45 resident states passed the joint-shift gate in each of the four settings. The minimum history support for the target quadrant was 127/128.

At the central resident state `(access, investment, assurance)=(0.5,0.5,0.5)`, the mean far-minus-near selection shifts were

| Setting | Delta beta_i | Delta beta_a |
| --- | ---: | ---: |
| Delayed control | -0.537 | +0.788 |
| Prior selfing | -0.398 | +0.703 |
| Pollen discount | -0.428 | +0.769 |
| Assurance cost | -0.537 | +0.689 |

Absolute sign reversal was not a general result. It was absent from the prior-selfing and pollen-discount surfaces and reached only 2/128 histories in the single most permissive assurance-cost state.

The mixed rare-mutant curvature

    gamma_ia = d2 log(w_mut) / (di_mut da_mut)

was negative in every near/far history-state-setting cell. Its sign was unchanged when the mixed finite-difference step was varied from `5e-5` to `1e-4` to `2e-4`.

This is evidence for antagonistic coupling between investment and assurance in the local fitness landscape. It is not evidence by itself for two attractors.

## S15. Full covariance and one-generation response

The exact multivariate Price identity establishes the one-generation mean response from the full parental-genome ledger. To ask whether local invasion gradients also recover the response direction, we compared

    Delta z_exact

with

    Delta z_Lande = G beta,

where `G` is the full 2 x 2 covariance matrix of expressed investment and assurance in the current population.

Across 48 controlled cells:

- the strict predeclared cosine-plus-component-sign gate passed 46/48 cells;
- mean cosine similarity between exact and full-`G` response vectors was 0.99946;
- minimum cosine was 0.99711;
- using full `G` gave lower vector error than diagonalizing `G` in 48/48 cells;
- mean cosine for the diagonal-`G` control was 0.98596.

The two strict-gate failures were not vector reversals. In both, the exact response was nearly axis-aligned and one component was close to zero; the local approximation crossed zero only for that small component while retaining cosine >0.999.

Thus the investment–assurance covariance materially improves local response prediction and should not be silently removed.

## S16. Frozen finite two-trait follow-up

A finite follow-up was frozen before reading the joint-selection outcome. All four assurance settings were run regardless of the rare-mutant result, using

    128 frozen visitor histories
    x 3 prespecified initial states
    x 4 new demographic repeats
    x near/far arms
    x 4 settings
    = 12,288 trajectories.

The initial states were outcross-like `(i=0.7,a=0.3)`, central `(0.5,0.5)`, and selfing-like `(0.3,0.7)`.

A paired history was classified as a syndrome endpoint only when all four demographic repeats were occupied in both near and far arms and

    far - near terminal investment <= -0.05
    far - near terminal assurance >= +0.05.

The opposite outcross endpoint used the reversed inequalities. All other eligible histories were intermediate.

Maximum syndrome-endpoint frequencies were:

| Setting | Maximum syndrome frequency across initial states | Maximum outcross frequency |
| --- | ---: | ---: |
| Delayed control | 0.164 | 0.026 |
| Prior selfing | 0.102 | 0.017 |
| Pollen discount | 0.213 | 0.009 |
| Assurance cost | 0.430 | 0.030 |

The delayed control is not independent evidence for assurance evolution, but it is essential for interpreting the endpoint frequencies: it itself reached a maximum syndrome frequency of 0.164. The frozen >=10% promotion threshold was an absolute procedural gate, not a causal contrast against this control. Relative to the control, prior selfing was lower (0.102), pollen discounting was only modestly higher (0.213), and assurance cost was markedly higher (0.430). Thus finite syndrome-endpoint occurrence is not, by itself, evidence that a trade-off caused the syndrome direction; the clearest trade-off-specific amplification in this comparison is the assurance-cost condition.

No setting met the alternative-endpoint branching rule requiring both syndrome and outcross classes to reach >=10% of eligible histories within a fixed setting and initial state. The finite result therefore supports a **joint syndrome direction**, not common bistable selfing/outcrossing endpoints.

Split-half endpoint-class agreement was generally high (approximately 0.74-0.97) but fell to 0.664 for the assurance-cost selfing-like start, below the frozen 0.70 reproducibility gate.

## S17. Fixed-inbreeding-depression boundary

Inbreeding depression is fixed throughout this extension. Model 3 therefore excludes the purging feedback central to the alternative stable mating systems of Lande & Schemske (1985).

The negative correlational selection, directional joint shift and finite syndrome endpoints reported here must be interpreted under fixed `delta`. Their existence does not identify the purging-driven bimodality of classical mating-system theory.

## S18. Updated novelty boundary

Classical theory already contains:

- the automatic transmission advantage of selfing;
- prior, competing and delayed selfing;
- pollen and seed discounting;
- pollen-limitation thresholds for mating-system evolution;
- purging-driven selfing/outcrossing alternative states;
- coevolutionary links between mating system and floral display.

The contribution here is not a new general selfing threshold. It is the representation bridge within one stochastic visitor-transfer model:

    visitor assembly
        -> rare-mutant joint selection field
        -> exact multivariate Price response
        -> covariance-mediated local response
        -> finite historical realization.

The same near/far visitor histories that generate the island-like finite trajectories rotate the local selection vector toward lower investment and greater assurance across the full frozen state grid, while the finite model shows that this strong low-order directional signal does not imply common alternative endpoint classes.

This is the theory result relevant to the main manuscript's repeatability argument.

## S18. Corrected admission boundary

All frozen finite endpoint counts were recomputed from all 12,288 arm records and retained. The Price identity recheck passed 48/48 (runtime maximum error 7.8e-16). The full-G approximation remains 46/48, not universal response fidelity. No tolerated failure fraction was frozen for automatic promotion; the repaired admission script therefore withholds automatic mechanistic-core promotion when complete response support is absent. This conservative software decision does not erase the exact Price result, joint-gradient result or finite endpoint observations. Old adjudication files are historical, not overwritten. See MODEL3_SELECTION_REPAIR_20261004.md.
