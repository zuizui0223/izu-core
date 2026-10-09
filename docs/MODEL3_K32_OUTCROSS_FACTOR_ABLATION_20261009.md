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
