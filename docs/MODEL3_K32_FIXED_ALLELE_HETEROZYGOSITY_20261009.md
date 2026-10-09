# K32: Heterozygosity perturbation at exactly fixed assurance allele count

## Immediate question

Earlier original-source Model3 engineering comparisons showed that the high
reproductive-assurance allele approaches fixation, while shuffled
assurance diploid genotypes retaining their original marginal
frequencies weaken the positive late matching-allele reproductive
direction. Artificially restoring the entire assurance founder
genotype distribution can reverse that direction but simultaneously
changes high-allele frequency, heterozygosity and genotype association.

This experiment **fixes the assurance high-allele COPY COUNT exactly**
and changes only the number of assurance heterozygotes by two individuals
per living parent population. It is an **artificial genetic-state
sensitivity**, NOT a source evolutionary event, empirical gene edit,
unique estimate of assurance heterozygosity selection, or fully
isolated individual fitness contrast.

## Frozen biological source

Original Model3 K=32, mutation=0, adult survival=0, seed immigration=0,
the prior_selfing canonical Chapter2 mating/viable seed ledger,
three diploid biallelic loci with 27 joint genotype classes,
and only old near visitor history 26110601. Source original parent
states evolve through normal finite Markov reproduction until
parent-years 1,4,8. Every comparison uses exactly the SAME
original nested demographic path identities still occupied
at the start of year8; this is conditioned on late source
survival, never independent ecological visitor histories.
Two archived visitor snapshots are used: year1 and year8.
Only original source reproduction is evaluated on edited
parental genotype states; there are no autonomous eight-year
trajectories of edited populations.

## Exact genetic counterfactual and feasibility

For parent census N, an assurance diploid genotype count triple
`(n_LL,n_LH,n_HH)` has total number of high-allele
copies `A=n_LH+2*n_HH` and heterozygote count `n_LH`.

- `HET_UP` requires n_LL≥1 and n_HH≥1: convert one
  low-low homozygote and one high-high homozygote into
  two low-high heterozygotes. This keeps A constant but
  increases heterozygosity `2/N`.
- `HET_DOWN` requires n_LH≥2: convert two low-high
  heterozygotes into one low-low and one high-high
  homozygote. This keeps A constant but decreases
  heterozygosity `2/N`.
- If the required categories are absent, record the
  change as **infeasible**. Do not create missing high
  or low founder alleles to force an effect. An already
  high-fixed parent (A=2N) cannot be perturbed by
  either operation.

Both controls preserve the exact original N, high-allele
COPY count of EVERY locus, and each individual's genetic
state at the other two loci, with allele values fixed at
.25/.75. Relative to a same-permutation sham, exactly
TWO individuals' assurance diploid genotype pairs change.
The modified genotype state can still change reproductive
mating weights/parent fitness under unchanged canonical
source rules: that is the outcome being measured.

## Remove allele-marginal and association-baseline confusion

For every living source state and each of four fixed random
permutations, shuffle the unordered assurance diploid
genotype pairs across individuals, preserving their full
0/1/2 genotype count distribution. This is the **SHAM**.
Apply the exact two-individual HET_UP or HET_DOWN edit
using the SAME permutation (not a second independent
pairing randomization). Use unchanged genotype states
at the other two loci, and evaluate original reproduce()
under BOTH old visitor snapshots for the same artificial
parent state.

The primary within-feasible-source-path contrast is
**EDIT minus SHAM** expected NEXT high-allele frequency
direction at all three loci, averaging four permutation
replicates inside the demographic source path before
estimating a path-level Monte Carlo standard error.

SHAM minus original also reports how much randomly
breaking the original locus-to-locus genotype alignment
changes the expected direction while leaving all
three full per-locus diploid genotype marginals fixed.
HET_UP and HET_DOWN feasibility classes need not be
the same. A bidirectional local slope is reported
**ONLY** on the intersection of parent populations in
which both are possible; there is no arbitrary
imputation from the opposite feasible subset.

The source matching expected allele shift in each
cell is evaluated relative to that cell's current
parent matching allele frequency, which is held
exactly constant by these assurance edits. Its
high-allele frequency change is therefore a
reproductive-response difference, not an immediate
change in matching allele copy content.

## Biological limits

This design does not uniquely separate heterozygosity
from associations at the level of the two changed
parents: changing their assurance homozygosity also
changes which matching/investment genotypes occur with
which reassurance genotypes at those two individuals.
The paired sham limits random pairing confounding
but does not force identical joint diplotype structure.
Source fertility and viable-selfed seeds can change
as a response even when high allele copies are
fixed, so this is not a controlled constant-fitness
genetics experiment.

The visit condition is one or both snapshots from
a single old archive history, not independent
pollinator environments. By late year8 assurance
may already be high fixed, making the HET_UP
operation rare/impossible; the proportion of
eligible source parent states is a **scientific
result** and must accompany effect sizes. Uncertain
rare-category results are not promoted as broad
adaptive findings.

No canonical Model3 source code, frozen prospective
Chapter2 history cohorts, natural island observations,
causal pollinator fitness experiment, or verified
Ito SDE/SPDE process is changed/established.

## Reproduction

    pytest -q tests/test_model3_k32_fixed_frequency_heterozygosity.py
    python -m scripts.audit_model3_k32_fixed_frequency_heterozygosity --budget 8 --draws 512 --permutations 4 --out fixed-allele-hetero-budget8.json
    python -m scripts.audit_model3_k32_fixed_frequency_heterozygosity --budget 3 --draws 512 --permutations 4 --out fixed-allele-hetero-budget3.json

PR420 CI job `model3-k32-fixed-allele-heterozygosity`
archives raw old-history JSON and refuses to treat
infeasible source parent genotypes as measurements.
**No numerical result is admitted until exact-head
CI has passed and the full raw artifact is inspected.**


## Executed source-verified result and eligibility limits

The corrected source SHA
`1ec2ac1773218b94551a4d8518a4bb9346ff2bd2`
passed the dedicated `model3-k32-fixed-allele-heterozygosity`
job in [GitHub Actions #37937577229](https://github.com/zuizui0223/izu-core/actions/runs/37937577229).
The two-budget complete [raw source-run artifact #11618768969](https://github.com/zuizui0223/izu-core/actions/runs/37937577229/artifacts/11618768969)
has SHA256
`a78a719c6d5c51947db0795a40f4ca21e88dd2fc4a18524a31712fb4794bc545`.
Both budget8 and budget3 regressions, conservation guards,
three source-parent checkpoints and each four random assignment
averages succeeded. Compact committed evidence:
`data/results/model3_k32_fixed_allele_heterozygosity_20261009.json`.

### Biological feasibility decreases toward assurance fixation

Source parental states are restricted to the SAME cohort
still living at start of original source year8, 512 (budget8)
or 506 (budget3). The number of eligible parent states for
two-individual assurance heterozygote operations:

| Original source parent year | Budget8 HET_UP | Budget8 HET_DOWN | Budget3 HET_UP | Budget3 HET_DOWN |
|---|---:|---:|---:|---:|
| Year1 | 512/512 | 512/512 | 506/506 | 506/506 |
| Year4 | 478/512 | 467/512 | 433/506 | 346/506 |
| Year8 | **171/512** | **119/512** | **101/506** | **49/506** |
| Year8 eligible for both | colspan | 86/512 | colspan | 33/506 |

Year8 HET_UP needs at least one *low-low AND high-high*
assurance homozygote. Year8 HET_DOWN needs at least two
assurance heterozygotes. Thus late fixation makes a
large fraction of the source population's original
genotype states **unable to implement either control**
without introducing absent allele states. We did NOT
replace them with fictitious measurements.
The two operations evaluate different subsets unless
explicitly restricted to the 86 budget8 or 33 budget3
original states feasible both ways.

### Exact same-frequency assurance-genotype perturbation results

The numbers below are edited-minus-SAME-PERMUTATION-sham
expected NEXT generation high-allele frequency *direction*
under the archived year8 visitor snapshot, in the original
matching/investment/assurance locus order.
Every edited source parent retains exactly the same count
of high assurance allele copies and unchanged individual
genotypes at matching/investment loci. Each action changes
assurance heterozygote fraction by exactly +/-2/N
where N is the living source parental census.

| Year8 assay, feasible states only | Matching direction, budget8 | Matching direction, budget3 | Assurance own-locus direction, budget8 | Assurance own-locus direction, budget3 |
|---|---:|---:|---:|---:|
| HET_UP | +0.000018 ± 0.000213 | -0.000498 ± 0.000765 | **-0.009203 ± 0.000067** | **-0.017986 ± 0.001791** |
| HET_DOWN | +0.000072 ± 0.000247 | +0.000853 ± 0.000460 | **+0.009062 ± 0.000091** | **+0.013093 ± 0.000918** |

Here +/- denotes nested source-demographic Monte Carlo SE
WITHIN the fixed old visitor history. This is not a confidence
interval over new ecological environments and cannot
establish a broad natural effect. In particular budget3
HET_DOWN is only 49 of 506 eligible parents and is
insufficient to generalize to the high-fixed majority.

**Conclusion for MATCHING:** the fixed-allele-count HET_UP /
HET_DOWN operations fail to produce a stable large matching
direction shift across the two budgets at year8.
Thus the earlier *founder distribution reset* sign
reversal is NOT supported as an effect of changing
assurance heterozygosity alone. It also changes the
assurance allele frequency, both homozygote classes
and individual genotype associations.

**Conclusion for ASSURANCE:** at the exact same current
parent assurance high-allele copy number and matched
locus-assignment baseline, increasing assurance
heterozygosity changes its OWN next-generation
expected transmitted allele direction negatively,
while decreasing heterozygosity changes it positively.
This contrast arises from genotype-specific original
reproductive weights (fitness/assurance self seed
rules + pollen pairing), NOT a new mutation/drift
transition. It is a biologically suggestive controlled
model sensitivity, not a natural heterozygote-fitness
coefficient. Altering two individual assurance diploid
genotypes necessarily changes their within-individual
association to unchanged matching and investment
backgrounds, so this is not a fully isolated
heterozygosity-only physiological effect.

### Why paired sham matters

At original year8 source states, randomly reassigning
the assurance diploid genotype pairs among individuals
(the SHAM; full assurance dosage-class marginal
unchanged) shifts matching-high direction by about
**-0.00285** budget8 and **-0.00206** budget3
under late visitors. Those association-breaking effects
are considerably larger than the direct two-parent
HET_UP / HET_DOWN matching-direction contrasts.
This supports separating genetic background
association from heterozygosity count, while still
not identifying which biological interaction is
causal in real plant systems.

At source year1, both HET_UP and HET_DOWN are
feasible in every original source history. Their
matching direction contrasts under year8 visitors
are approximately -0.000190/+0.000022 (budget8),
-0.000182/+0.000015 (budget3), but assurance own-locus
contrasts are about -0.01181/+0.01181. The strong
assurance own-locus response therefore appears
before the source is near fixation. No prospective
confirmatory visitor histories or natural observations
were opened.

**Acceptance boundary:** one archived old visitor
history 26110601 and artificial founder genotypes,
source canonical biological code unchanged; edited
genotypes do NOT naturally evolve from the frozen
source Markov transition. No isolated field
selfing advantage, model-wide epistasis coefficient,
new independent island evidence, or full SDE/SPDE
validation is asserted.
