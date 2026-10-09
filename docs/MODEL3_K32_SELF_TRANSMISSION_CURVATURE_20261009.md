# Original Model 3: linear assurance seed function but nonlinear allele transmission

## Why this is a critical correction

The source Chapter2 prior_selfing config actually has
**assurance_cost = 0, investment_cost = 0.5, inbreeding depression=0.5**.
Canonical \`reproduce()\` sets for each parent i:

\[
s_i = B(1-d)\exp(-0.5\,I_i^2)\,a_i.
\]

Viable self-seed intensity is **linear in assurance phenotype a_i**,
conditional on investment I_i. Earlier speculation that the assurance
cost function itself was nonlinearly stabilizing is therefore NOT true
for the specific prior_selfing experiment under study.

Nevertheless, selfed offspring HIGH-allele transmission depends on
the product of parent assurance dosage b_i and viable selfed seeds.
Because a_i = 0.25 + 0.5 b_i, where b_i in {0, 1/2, 1},
the numerator involves

\[
a_i b_i = 0.25\,b_i + 0.5\,b_i^2.
\]

This is nonlinear in **the genetic dosage being transmitted** despite
linearity of seed production in a_i. That difference matters biologically:
a parent homozygous high with b=1 transmits high alleles in all
selfed offspring, whereas a heterozygote with b=0.5 transmits
a high allele in one half of gametes, and the low homozygote none.

## An exact paired-parent identity at constant allele copies

For a living parent population, assurance high-allele frequency
p = mean_i b_i is held EXACTLY fixed by the artificial
two-individual HET_UP or HET_DOWN change. Define

\[
M = \sum_i s_i\,(b_i-p),\quad
T = \sum_i s_i + \sum_{ij} o_{ij}.
\]

This M/T is exactly the selfed-seed contribution to the
next-generation expected high-allele direction q-p, under
the original canonical Model3 viable-mating kernel.

HET_UP (one LL + one HH -> two LH) conserves sum b_i,
but the change in \(\sum a_i(b_i-p)\) at those two parents is
exactly **-1/4**, whatever the parent allele frequency p.
HET_DOWN (two LH -> one LL and one HH) gives **+1/4**.
This does NOT mean the total selfed seed count changes:
at EQUAL investment weights \(w_i=\exp(-.5 I_i^2)\),
\(\sum \Delta a_i=0\) and hence \(\Delta\sum s_i=0\)
EXACTLY for either operation.

At the two changed individuals, define \(w_0,w_1\),
\(\bar w=(w_0+w_1)/2\) and
\(\Delta F_i = a_i^{edit}(b_i^{edit}-p)
                  -a_i^{sham}(b_i^{sham}-p)\).
Then the **exact successful allele numerator** difference is

\[
\Delta M = B(1-d)\left[
\bar w\sum_{\rm pair}\Delta F_i
+\sum_{\rm pair}(w_i-\bar w)\Delta F_i
\right].
\]

Term 1 is the intrinsic (a*b) **genetic dosage transmission
curvature**, at the mean investment weight of the two edited
parents. Term 2 is investment/genotype **alignment**, due to
the unequal investment discount of the two particular
edited parents; it need not retain the same sign across
demographic paths.

Because total viable seed output can change, the exact
selfed-seed *direction* difference between the edited and sham
reproductive states is

\[
\Delta (M/T) =
 \frac{\Delta M}{T_{\rm sham}}
 -
 \frac{M_{\rm edit}(\Delta S+\Delta O)}
      {T_{\rm sham}\,T_{\rm edit}},
\]

where \(\Delta S\) and \(\Delta O\) are changes to the absolute
viable self and outcross seed masses. This four-component
decomposition (curvature/T_sham, alignment/T_sham,
normalization from ΔS, normalization from ΔO)
is exactly verified against \(\Delta(M/T)\)
from canonical source ledger at every individual
parent/counterfactual/visitor condition.

The self viable seed mass ΔS itself has **ZERO intrinsic
equal-investment-curvature term**. Its change arises from
how the two edited assurance phenotypes are allocated
across different investment traits, while ΔO depends
on the complete original pollen transport / maternal
allocation rules.

## Fixed-source evidence boundary

This is an exact mathematical analysis of source
Model3 (K32, u0, survival0, immigration0, prior_selfing,
old visitor seed 26110601 near only). Original parent
states are obtained from source old-history trajectories
at parent years1,4,8, selected on surviving at start
of year8. The source rule is unchanged. Four paired
random assignments of current assurance diplotype
counts are compared (edit minus identically randomized
sham), with BOTH old archived year1 and year8 visitor
snapshots. Each edit changes exactly two assurance
diploid genotypes and preserves high-allele copies,
other two locus genotypes, and current parent census.
HET_UP/HET_DOWN eligibility near fixation remains
strictly constrained and differs between operators.

The decomposition establishes algebraic reproductive
weighting, **not causal physiological heterozygote fitness,
universal selfing advantage, or real botanical epistasis**.
It does not demonstrate independent ecological replication,
natural plant data, prospective confirmatory visitor
cohorts or a valid continuous SDE/SPDE.

## Commands

    pytest -q tests/test_model3_k32_self_transmission_curvature.py
    python -m scripts.audit_model3_k32_self_transmission_curvature --budget 8 --draws 512 --permutations 4 --out self-curvature-budget8.json
    python -m scripts.audit_model3_k32_self_transmission_curvature --budget 3 --draws 512 --permutations 4 --out self-curvature-budget3.json

PR420-only CI job: \`model3-k32-self-transmission-curvature\`.
No numeric component results accepted until source CI
passes and full raw artifact is inspected.
