# Alternative ovule-binomial diploid kernel: individual-selection versus group viability sign boundary

**2026-10-10 — model-internal independent-kernel mechanism control, complete 2048-path source execution. NOT field ecology; no demonstrated evolutionary suicide.**

## Why an alternative model matters

Existing PR #452 Model3 analyses decomposed maternal outcross F, paternal outcross P and viable self S; some focal finite/analytical rare-mutant investment gradients opposed a collective viable-seed gradient, and subsequent 64/192-history Model3 experiments found source-history-dependent *assurance genotype* effects on persistence. The most stringent new 192-donor predeclared genomic persistence contrast did **not** pass its combined bootstrap + distribution-free interval rule, and further same-parameter RNG expansions are not a substitute for a distinct biological mechanism.

An additional, **independently coded ONE-locus diploid/ovule-binomial population model** has therefore been built without calling Model3 reproductive genetics, its three-locus source, visitor-attraction/pollen sharing network, or its Poisson recruitment-and-cap rule. This is a new **toy model structure**, NOT an independently calibrated biological system, alternative published empirical island dataset or a discovery of unknown selfing theory.

Existing comparable literature must be given scientific priority: [Lepers, Dufay & Billiard 2014, *Evolution*, DOI 10.1111/evo.12533](https://doi.org/10.1111/evo.12533) modeled prior selfing with floral investment and pollinator demography and explicitly predicted evolutionary suicide. [Cheptou 2019, *Annals of Botany*, DOI 10.1093/aob/mcy144](https://doi.org/10.1093/aob/mcy144) reviews the opposing evolutionary rescue versus suicide conditions. The historical 3:2 selfing transmission advantage, cost of outcrossing, is not a new result here.

## Exact minimal biological kernel

Each adult carries **one diploid 0/1 mating-strategy locus**, with **a = mean of its two alleles** as the genetically expressed selfing propensity. Eight founders have diploid genomes `[(0,0) ×3, (0,1) ×4, (1,1) ×1]`, initial mean a=0.375. Every adult attempts **two ovules per year**. An ovule matures with probability `phi=0.9`. A selfed seed survives with constant `v=0.6`. Effective pollination is **not fixed independently of population size**:

```
q_N = 0                                  for N <= 1
q_N = q * (N-1)/(N-1+1)                  for N >= 2
```

The two external-pollen strengths are **q=0.8** and **q=0.4**. Independent seed fate probabilities depend on the timing of selfing:

| Schedule | P(viable selfed ovule) | P(viable outcrossed ovule) |
|---|---|---|
| Prior selfing | `phi * a * v` | `phi * (1-a) * q_N` |
| Delayed selfing | `phi * (1-q_N) * a * v` | `phi * q_N` |

The remainder of ovules fail. Prior selfing therefore occupies ovules that might otherwise outcross, while delayed selfing draws only from the unfertilized remainder. Viable outcrossed offspring pick a **different father** uniformly from the remaining adults; no pollen-discount effect on paternal export, no self-incompatibility, and no additional invasion term from changing pollen shares. Each embryo inherits diploid alleles via maternal and paternal Mendelian draws (selfed offspring draw both homologs from one parent independently). All viable embryos undergo **uniform lottery retention up to carrying capacity K=8 or 48**, unlike Model3's Poisson births. There are no adults surviving across years, no immigration and no mutation. At N=1, outcrossing is impossible.

**Two separate genome-to-expression arms** are compared from the SAME founders and paired demographic seeds:

- **Heritable expression:** each adult's selfing propensity is determined by its Mendelian diploid genotype, so source reproductive success can genetically alter the phenotype distribution.
- **Expression frozen:** all adults express the initial founder mean `a0=0.375` for reproduction, while actual diploid alleles **continue to segregate/drift**. This is a phenotype/genotype-coupling intervention, NOT a complete freezing of genetic evolution or a pure additive selective effect from year0.

## Exact F/P/S prediction, frozen before simulations

At a symmetric resident state of census N, because the focal mother's own selfing propensity does not alter father slots assigned from **other** mothers under the no-pollen-discount assumption, focal `P` has *zero marginal derivative*, though its absolute contribution need not be zero.

Writing `C=2*phi=1.8`:

```
Prior:    beta_focal = C * (v - q_N/2)
          Gamma_seed = C * (v - q_N)

Delayed:  beta_focal = Gamma_seed = C * (1-q_N)*v
```

`beta_focal` is the **signed derivative of reproductive gene-copy contributions W** (not log W); if W>0 its sign also agrees with the derivative of log W. `Gamma_seed` is the **group seed-production derivative per adult** under uniform a change, not the derivative of survival probability or density-dependent population growth. `beta_F=-phi*q_N`, `beta_P=0`, `beta_S=2*phi*v` in prior selfing, summing exactly to beta. Delayed selfing fills otherwise empty ovules and has beta_F=beta_P=0; all selection and group gradients are positive except hypothetical complete pollen saturation.

For q=.8, v=.6, and the above mate-limitation function,

- N=1,2,3: beta positive, group gamma positive.
- **N=4: q_N=.6, Gamma_seed=0**, but beta remains positive.
- **N≥5: beta positive, group Gamma_seed negative** (a local individual/group reproductive-output conflict).

For q=.4, group gamma remains positive at all N. For **delayed selfing**, both gradients remain positive at every declared N regardless of q. This establishes an **exact density-dependent sign boundary** in an alternative toy mechanism without relying on stochastic inference or tailored post-outcome thresholds. The inequality **v > q_N/2** for individual increase and **v < q_N** for group harm is precisely the classic selfing gene-transmission conflict. It is not a novel mathematical impossibility or Nature-level theorem.

## Reproducibility and full finite trajectories

- A closed model parameter/design contract was committed **before the results** to `data/design/chapter2_alternative_binomial_kernel_20261010.json`. Seed maturity phi was chosen algebraically before simulation to prevent inevitable starting replacement failure at N=8, not adjusted after observing a trajectory. Input source-design SHA256 **`1b7f00903e494b989cba9aed5722207d57a617c7d57e73dcd6f53a7e96f11575`**.
- Independent standalone simulator `scripts/audit_chapter2_independent_binomial_kernel.py`, tests `tests/test_chapter2_independent_binomial_kernel.py` (ovule probability mass, father absence at N=1, diploid inheritance, threshold N=4, no prior/delayed confusion, source lock, exact paired uncertainty). The original Model3 biology was NOT modified.
- **2 selfing schedules × 2 external pollen strengths × 2 K × 2 expression modes × 128 demographic RNG repetitions = 2,048 complete trajectories**; H20 and H80 occupancy, first extinction, survivor-only allele frequencies and unconditional allele-copy counts retained.
- Executed scientific source SHA **`7505ab4b87858c5dfa5f17985920c47bbab5a3ef`**. [Actions CI #38020498762](https://github.com/zuizui0223/izu-core/actions/runs/38020498762) source-only tests and full calculation/archive PASS. Full [artifact #11658735168](https://github.com/zuizui0223/izu-core/actions/runs/38020498762/artifacts/11658735168), original JSON SHA256 **`860ded2d374f305f66a47a55a3fe148f43accdadea4d2b20218e860ecf659266`**, ZIP SHA256 **`52ec9186772bc192873bc8c21b854c504fce35a177244328e7a194648a98cc7b`**.
- Permanent source-locked compact receipt `data/results/chapter2_independent_binomial_kernel_2048_receipt_20261010.json` preserves all eight H80 comparisons, exact paired exclusive-discordance confidence limits and nulls.

### Full H80 occupancy results (out of 128 demographic replicates per cell)

| Schedule | Pollen q | K | Heritable expression | Frozen expression | Δ (heritable−frozen) | Conservative paired 95% | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| Prior | .8 | 8 | **57** | **78** | **−16.41pp** | [−33.69,+1.88]pp | INCONCLUSIVE |
| Prior | .8 | 48 | 122 | 122 | 0 | [−9.27,+9.27]pp | INCONCLUSIVE |
| Prior | .4 | 8 | **46** | **0** | **+35.94pp** | [+23.21,+46.14]pp | positive |
| Prior | .4 | 48 | **72** | **0** | **+56.25pp** | [+42.60,+66.16]pp | positive |
| Delayed | .8 | 8 | 123 | 128 | −3.91pp | [−9.67,+2.30]pp | INCONCLUSIVE |
| Delayed | .8 | 48 | 128 | 128 | 0 | [−3.37,+3.37]pp | equivalent (single cell) |
| Delayed | .4 | 8 | **100** | **0** | **+78.13pp** | [+65.42,+85.77]pp | positive |
| Delayed | .4 | 48 | **102** | **0** | **+79.69pp** | [+67.14,+87.08]pp | positive |

The **predeclared primary** was prior selfing, high pollen q=.8, K8. Its observed negative persistence difference **−21/128** does *not* exclude zero under the conservative paired 95% interval and therefore **does not prove evolutionary suicide** in this independent kernel. K48 exhibits a complete occupancy ceiling under that condition, despite positive allele rise in the heritable-arm survivors.

Under pollen limitation q=.4, heritable genotype expression has a large *positive* survival association under both prior and delayed selfing. This is **not an independent novel rescue mechanism**: the very small `q_N` at the frozen resident's starting a0 makes its per-capita fecundity subreplacement, while heritable higher selfing propensity can approach a sufficiently productive self route. **The low-pollen frozen-expression arm has 0/128 survivors in every q=.4 H80 condition**, so do not interpret a 35–80pp difference as independent confirmation of a natural mate limitation effect.

The heritable-assurance allele frequencies *among survivors* were approximately .930 (K8, prior, q=.8), .992 (K48, prior, q=.8), and exactly 1 in the low-pollen prior survivors. These survivor-conditioned values reflect within-model selection/drift, not unconditional allele-level survival effects; extinct genotype means remain undefined.

## Synthesis with the original Model3 question

This alternative structure establishes that **the sign conflict of individual reproductive gene transmission and collective viable seeds is not contingent on the original Model3's visitor-attraction matrix or Poisson recruitment**; in this intentionally chosen minimal kernel it follows from classical selfing automatic transmission advantage combined with prior-ovule displacement. Critically the **same local beta/Gamma_seed sign conflict** (N≥5 at q=.8) does **not** guarantee a statistically resolved negative difference in H80 population occupancy. Dynamic feedback when N shrinks can flip the collective seed benefit of selfing to positive, and density cap N-dependent effects can saturate survival.

This is a **model-theoretical control**, not proof of novelty or ecological transfer: the algebraic parameter window was chosen in advance *to demonstrate a sign conflict*. Earlier Model3's selected assurance-allele source effect was *positive*, with its strict prospective source test inconclusive. It is not scientifically legitimate to claim that one kernel confirms rescue and another confirms suicide, because the negative primary in this alternative kernel is unresolved. A more general paper must demonstrate an a priori classification that predicts actual fitness/persistence outcomes across independent biological kernels, and ideally measured reproductive ecology under real island pollinator availability.

**Repository disposition:** Keep PR #452 Draft as a bounded source-backed mechanism laboratory. Keep independently frozen PR #411 floral investment letter and #451 capacity manuscript claims separate. The new independent ovule-binomial kernel is an explanatory and falsifiable counterexample construction; it is not a manuscript-ready broad comparative discovery by itself.
