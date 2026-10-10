# Assurance-locus transfer to new post-t20 visitors with three nested diploid-genotype draws

**2026-10-10 — Completed original-source future-environment transfer; NOT an independent new donor-history confirmation or natural-Izu result.**

## Goal and causal source

Earlier #452 original full-genome and artificial-locus-mosaic tests suggested that the assurance-locus genotype state formed under source-selected parentage was more favorable for later survival than the matching+investment loci in the same fixed Model3 environment, especially under K8/B48 and reduced selfed-offspring viability. Those studies reused the same exposure and had only one whole-genome donor resampling per source history.

A fresh, pre-execution-locked model-internal transfer experiment therefore used the **same original 64 source historical visitor IDs 61024001–61024064** to replay two original competing parentage operators through t20. All original 64 are admitted into the audit: selected-original source donors survived t20 in **58/64**, neutral-parentage donors in **52/64**, and BOTH donors in **50/64**. Only those 50 have a complete genotype distribution on both sides; the remaining 14 do not magically acquire counterfactual donors.

**What is genuinely new:** for each original source ID, a disjoint visitor RNG seed **61026001–61026064** was generated for **post-t20 visitor transitions**. These new arrival/loss trajectories inherit the old source history's actual community at t20, so the new future dynamics are stochastic and independently seeded *conditional on the earlier, already exposed source ecology and donor genotypes*. Source genomes are not fresh ecological/history evidence.

For each original eligible paired donor history, **three independently seeded samples of eight entire joint diploid plant genotypes** were extracted from original selected-history donor genotypes and original neutral-history donor genotypes. Alleles, origins and mutation flags for each entire individual were preserved, and those samples were crossed into **four genotype source compositions**: neutral-all, selected-assurance-only, selected-matching+investment-only and selected-all. Each genome was evaluated under future K8 and K48 with the SAME starting recipient N0=8, constant pollen B48, original canonical selected parentage, common matched future visitors and demographic RNG. This yields **50 eligible donor histories × three nested genome draws × four genome compositions × two future capacities = 1,200 actual source paths**.

## Frozen input, exact execution and full archive

- Pre-outcome future-transition, donor-resampling and uncertainty contract: `data/design/chapter2_t20_assurance_new_future_multidraw_20261010.json`; SHA256 **`a92ca999cfe34355b42a2f6d08c9ea37b0c6ed12d907387d15611549174ff8ff`**.
- Scientific execution source commit **`91cc80e2481f952602d7965b76d0b75a8a8a008a`**. [Actions #38018738837](https://github.com/zuizui0223/izu-core/actions/runs/38018738837): focused smoke test passed, all original donor eligibility and 1,200 futures executed successfully, original JSON archive upload passed.
- [Full original artifact #11657541979](https://github.com/zuizui0223/izu-core/actions/runs/38018738837/artifacts/11657541979): raw JSON SHA256 **`4a863af7b1f4d0addd5fc233a97491d865fc324d0dfaa555f133a369ecb34b62`**, ZIP SHA256 `7b39085cb171e91e7a6502651797efb303145c2439ce842b87707be3756d6e6c`. The complete 64 original donor t20 statuses, 64 new visitor seeds, independent whole-genome selected/neutral draw indices, every genotype module and all 1,200 outcomes are inside the original JSON.
- Code `scripts/audit_chapter2_t20_assurance_new_future_multidraw.py`, source-only test `tests/test_chapter2_t20_assurance_new_future_multidraw.py`, compact original-data receipt `data/results/chapter2_t20_assurance_new_future_multidraw_receipt_20261010.json`.
- History-level inferential unit is **50 original conditional donor histories**, not 150 independently generated donor histories. Three genotype resamples are nested; the 64 new future innovation seeds were paired one-to-one to the original donor histories and only 50 contributed to genotype comparison.

## Full results, 80 updates

Observed surviving trajectories out of 150 **nested genotype draws**, not 150 independent ecosystems or donor histories.

| Genetic source composition | Recipient K8 | Recipient K48 |
|---|---:|---:|
| All three loci neutral source | 57/150 | 122/150 |
| **Selected history assurance locus only** | **103/150** | **141/150** |
| Selected history matching/investment only | 58/150 | 127/150 |
| All selected-source loci | 109/150 | 145/150 |

At K8, the **predeclared primary assurance-only** versus neutral-all survival difference was **+46/150 = +0.30667**. The 1999 history-cluster bootstrap percentile interval over 50 originally eligible source IDs, after taking the mean of three nested genotypes within each source ID, was **[+0.193,+0.4333]**. However, the separately predeclared distribution-free Hoeffding confidence interval on 50 bounded history-level effects [-1,1] was **[−0.0775,+0.6908]**. Because the decision rule required BOTH lower bounds > +0.05, the **primary verdict is INCONCLUSIVE**, not a confirmed 5pp ecological benefit.

At K48, the assurance-only survival contrast was **141/150 vs 122/150**, +0.12667; history-cluster bootstrap95 **[+0.040,+0.220]**, Hoeffding95 **[−0.2575,+0.5108]**, also INCONCLUSIVE under the source-locked strict rule.

The other-two-loci-only contrast is tiny in this group: **+0.00667** at K8 and **+0.03333** at K48. The full selected-all genomic source contrast is **+0.34667** at K8 and **+0.15333** at K48. Two-order *descriptive* assurance/other-loci allocations of the full effect are at K8 +0.32333/+0.02333, at K48 +0.12333/+0.03000. These are **artificial source-genotype factor contrasts**, not natural biological mediation fractions or independent locus selection coefficients.

The new-future-environment test therefore **reproduces the qualitative assurance genotype-source signal** of the old static-source dataset while explicitly acknowledging that the old genetic donors have not been independently recreated.

## Why a second, wholly fresh donor cohort is necessary

The older survivor-conditioned donor sources are already selected: even a new random future after t20 cannot reverse the fact that their starting allele distributions, selected donor status and genotype differences were outcome-exposed before this experiment. At n=50, the two-sided Hoeffding 95% radius for history-bounded paired effects is **sqrt(2 log(40)/50) ≈ 0.3841**. Simply increasing genotype resampling three-to-tenfold would not increase the independent number of source histories; the worst-case confidence bound remains wide.

The next predeclared experiment therefore uses **192 entirely new original source visitor histories AND disjoint 192 new future visitor transition seeds**, with two nested donor genotype samples each, at the same focal settings and the same stringent interval rule. The new design is `data/design/chapter2_assurance_independent_source_future_192_20261010.json`. This is prospectively specified relative to that cohort's future outcomes but **still tests a hypothesis selected after earlier within-model exploration**.

## Scientific boundaries

- All source genotypes and populations arise in one fixed Model3 mechanism; not 192 independent real islands or alternative validated biological models.
- Source donor selection conditions on survival to t20 in BOTH selected and neutral original pasts; this is a **post-treatment principal-stratum-like conditional comparison**, not unconditional evolutionary rescue or complete causal mediation.
- Two genetic ancestry sources are combined into artificial genomic mosaics with potentially novel cross-locus associations. An assurance-locus source replacement also changes within-locus distribution/variance/ancestry, not merely its mean phenotype.
- Fixed inbreeding depression and zero mutation exclude deleterious-load accumulation and mutational meltdown. There is no evidence here that individual-selected alleles cause natural island extinction or evolutionary suicide.
- The original source t20 ancestry, full transcript and raw paths remain available; no retrospective overwriting of source cohorts or inference thresholds was done.

**Disposition:** keep the result as a positive *model-internal exploratory transfer* with a clearly **inconclusive stringent model-conditional primary inference**; retain every null and alternative mechanism, and do not merge into #411/#451 manuscript claims.
