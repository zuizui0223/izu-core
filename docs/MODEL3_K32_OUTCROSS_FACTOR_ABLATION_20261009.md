# Model 3 K32 — eight-generation outcross-factor counterfactuals

## Main question

The previous exact Shapley ledger analysis found distinct donor-export,
visitor-routing, and maternal-outcross-seed *algebraic* contributions to the
one-step assurance-high-allele frequency variance, under an artificial
reference. Shapley values are not independent biological interventions.

This experiment changes **one weight factor at a time** in an autonomous
eight-generation comparator, while leaving the original biological source
Model 3 unchanged. The estimand is the change in simulated genetic outcomes
caused by each *precisely declared edge-preserving, mass-normalized
factor-flattening intervention*. It is NOT a unique causal partition of
real pollination, donor pollen or maternal fitness.

## Strict source conditions

- K=32, mutation=0, 8 generations, no adult survival or seed immigration;
  original canonical Chapter 2 prior_selfing setting, four engineered
  three-locus founder genotypes expanded to K, fully joint 27-genotype support.
- Only OLD archived visitor history 26110601 / near, 8 source visitor
  states. **Do not** open any Chapter 2 prospective confirmatory history.
- 512 *nested demographic trajectories per arm*, and only ONE independent
  visitor-history environment. No natural field observations.
- Source arm calls original genotype_count_markov_step with canonical
  reproduce(), self exclusion, and exactly Mendelian offspring.
- All controlled arms also start from identical engineered founders,
  independently recompute the **unmodified source reproduce ledger on
  THEIR CURRENT genotype state**, and replace only the outcross-pair
  weights. Source history, pollen and birth rules are unmodified in files
  under scripts/model3_island/.

## Exact three-intervention definitions

Canonical outcross father row i, mother column j (i!=j) is:

    W_ij = exported_i * (delivered_ij/exported_i)
           * (outcross_female_seeds_j/receipt_j).

Call the three factors E_i, R_ij, M_j. Use zero for ratios whose
denominator is 0; original absent donor-recipient mating edges remain
zero throughout.

1. **Equalize donor export:** replace all strictly positive E_i with
   their mean across originally exporting donors; preserve zero donors.
   Retain R_ij and M_j. This removes donor-export *heterogeneity*
   within its active support. It does NOT turn off pollinators or remove
   the source's visitation dependence from R.
2. **Equalize visitor routing:** for each donor i, replace positive
   R_ij by the donor's total delivered-per-export fraction divided
   equally among only its original positively served recipients.
   Preserve each donor's total routing share, absent links, E_i, M_j.
   This removes donor-specific recipient routing preferences on current
   support; it is NOT a removal of all visitor behaviour or abundance.
3. **Equalize maternal outcross provisioning:** replace positive M_j
   values by the global receipt-weighted mean
   sum_j(outcross_female_j)/sum_j(receipt_j), over recipient-positive
   mothers. Retain E_i and R_ij. This removes *maternal heterogeneity*
   in viable seed yield per unit pollen received; it does NOT remove
   resource-cost or assured-selfing effects from the ORIGINAL ledger
   before the alternative pairs are formed.

**For ALL controls**, rescale the altered outcross matrix to exactly
preserve the source-current-state total outcross viable seed intensity,
retain the original individual selfed-seed masses exactly, and set
outcross diagonal strictly to zero. This guarantees the *same source
conditional capped-Poisson N law* and self/outcross intensity fraction
when comparing two operators at the SAME genotype parent state.
The donor/recipient genotype offspring distribution changes through
the original Mendelian kernel.

Because the altered populations genetically diverge over years, the
source biological ledger computed on different genotype populations
may have different TOTAL viable seed intensities in later generations.
Consequently autonomous population extinction frequencies **may**
differ indirectly even though no direct census intensity intervention
was applied at any given parent state.

The finite population is sampled with a common generation-and-replicate
RNG seed across arms, but shifted genotype probabilities may consume
the shared random stream differently. It is a **paired seeded design**,
not the same realized offspring vector or a guaranteed variance-optimal
common-random-number coupling.

## Required outputs and interpretation

For all source and three controls, at every generation report population
extinction, unconditional census and 27-class genotype richness, number
of initial allele types fully lost (six total), survivor-only three trait
means and assurance high-allele frequency, assurance-locus heterozygote
fraction, and complete fixation probability. Extinct populations have
NO allele-frequency/trait value; richness and allele type loss are
defined at 0 and six, respectively.

At generation eight report each counterfactual-minus-original difference
and demographic MC standard error; for trait/heterozygosity/fixation
differences use only *paired trajectories alive in both arms*. The
unconditional extinct probability and allele-loss/richness differences
include all paired demographic replicates.

**Critical identification limits:** all three interventions alter
outcross weights and MUST be labelled different reproductive biology.
They are not independent causal coefficients and need not add up to the
previous Shapley contributions. Holding current total viable seed
intensity constant suppresses direct demographic effects; its long-run
results are a controlled mechanism sensitivity, not a complete
ecological removal/replacement of pollinators or maternal resources.
Results may depend on which visitor history and initial genotypes are
chosen. One fixed old visitor history is NOT 512 islands.

A small change in eight-generation population outcome is not proof
that a mechanism is biologically unimportant: by generation eight
source viable selfing dominates in this engineering case, and
assurance-high allele can be near fixed.

## Executables

```bash
pytest -q tests/test_model3_k32_outcross_ablation.py
python -m scripts.run_model3_k32_outcross_ablation --out outcross-ablation-budget8.json --budget 8 --draws 512
python -m scripts.run_model3_k32_outcross_ablation --out outcross-ablation-budget3.json --budget 3 --draws 512
```

The existing automatic core CI includes a PR#420-specific job for these
two conditions and archives raw results. Do not promote any numerical
claims before that job has successfully finished and evidence was
inspected. Original Model 3 genetic/fecundity biology is untouched.

## Verified autonomous eight-generation simulations

Exact source run and CI evidence:
[GitHub Actions #37893767488](https://github.com/zuizui0223/izu-core/actions/runs/37893767488),
`model3-k32-outcross-ablation` job **PASS** on SHA
`5d57d06cb0a0975f0c128a2fec2c36a8ed0ef3dc`.
[Both raw cases, artifact 11598764619](https://github.com/zuizui0223/izu-core/actions/runs/37893767488/artifacts/11598764619),
SHA256 bbbbbf220291fae79d613e6d0a431fbbb21e38b416bba944ec8696342e59946c.
Permanent source-lock is
`data/results/model3_k32_outcross_ablation_20261009.json`.

### Endpoints at eight years

| Budget | Arm | Survivors / 512 | Assurance-high allele frequency given occupancy | Assurance heterozygote fraction given occupancy | Genotype richness unconditional | Initial allele types lost unconditional |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| 8 | Original Model3 | 512 | 0.97861 | 0.01898 | 4.3242 | 0.8262 |
| 8 | Equal donor export | 512 | 0.98624 | 0.01141 | 3.8691 | 0.9863 |
| 8 | Equal visitor routing | 512 | 0.98776 | 0.00995 | 4.5781 | 0.9766 |
| 8 | Equal maternal provision | 512 | 0.98801 | 0.00946 | 4.0176 | 0.9629 |
| 3 | Original Model3 | 505 | 0.98403 | 0.01193 | 3.1152 | 1.3965 |
| 3 | Equal donor export | 504 | 0.98889 | 0.00672 | 2.8359 | 1.5488 |
| 3 | Equal visitor routing | 507 | 0.99159 | 0.00534 | 3.3223 | 1.4844 |
| 3 | Equal maternal provision | 506 | 0.98974 | 0.00446 | 3.0820 | 1.4434 |

Across this fixed visitor history, all three **specified, normalized**
interventions shifted the survivor mean assurance high allele upward
and decreased assurance-locus heterozygote frequency relative to
original Model3. The source-to-control mean-frequency differences
among both-arm survivors at budget8 were +0.00763 (donor),
+0.00916 (routing), and +0.00940 (maternal). Their *paired nested
demographic* MC standard errors were 0.00181, 0.00181 and 0.00162.
At budget3 the paired frequency differences were +0.00482
(SE 0.00317), +0.00807 (SE 0.00288), +0.00563 (SE 0.00358).
Only the directional routing effect at budget3 had an approximate
95% normal MC interval excluding zero; this is a **within-history**
precision diagnostic, not ecological independent replication.

### Genotype richness and extinction caution

Importantly, genotype richness does NOT shift uniformly with
assurance fixation. Equalizing donor export lowers joint-genotype
richness, equalizing routing raises it, and equalizing maternal
provisioning tends to lower it at budget8 but changes little
under budget3. This shows that **convergence in one allele frequency
need not be convergence of the entire multilocus genotype repertoire**.

In budget8 all four arms were occupied in all 512 draws, so zero
observed extinction events does NOT establish true extinction
probability zero. In budget3 the number of extinctions was original
7/512, donor 8/512, routing 5/512, and maternal 6/512. Those rare-event
differences are too small relative to finite Monte Carlo uncertainty
to support any meaningful rank of extinction-risk fidelity.

One-at-a-time ablations control SOURCE-CURRENT-STATE viable seed
intensity and selfing mix but allow the independently evolved
genotypes to change future source-computed intensities. They are not
the same mathematical estimand as the prior one-step Shapley
heterozygosity variance components. In particular, the fact that
the maternal term had the largest negative *conditional variance*
Shapley magnitude does NOT imply its autonomous eight-year effect
must be the largest on genotype richness, mean assurance evolution,
or population extinction.

**Scope:** old visitor 26110601/near ONLY, simulated artificial
founders, 512 nested demographic paths per arm, no independent
ecological histories, no natural-island observations, no
preregistered confirmatory cohorts, and no source biological
code edits. The comparator arms are deliberately different
mating-weight laws; they are controlled simulations, not
confirmed fitness responses in the field or SDE/SPDE evidence.
