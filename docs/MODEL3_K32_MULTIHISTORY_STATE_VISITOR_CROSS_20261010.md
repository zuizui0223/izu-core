# Original K32 Model3: 8 visitor RNG histories × early/late parent genotype-state crossover

## Where the analysis stands

Source-locked earlier experiments showed that the original near visitor
history 26110601 had a matching HIGH allele expected reproductive
direction that switched negative to positive with time. An exact 8×8
original source parent-year × visitor-year cross for that ONE old
history apportioned the time difference mostly to evolved parental
genotype/census state (~82–85% under that particular same-survivor
cohort). A later, fully post-outcome exploratory check of EIGHT new
visitor RNG histories 26110602..26110609 showed only 4/8
(budget8) or 5/8 (budget3) matching negative→positive reversal:
it is **not universal**. Finally a source-affinity/richness visitor
year1–2 forecast was worse than the training-mean baseline in
leave-one-whole-visitor-history-out tests.

The present study asks whether the **same 2×2 component structure**
that characterized the old history is itself repeatable across
all eight previously generated exploratory histories, including
their negative outcomes. No further visitor RNG seeds are added.

## Exact original-only 2×2 crossing

For each of the eight new simulated near visitor histories,
run 128 original Model3 genotype-count Markov paths
for seven updates. Source model is unchanged:
K32, mutation0, adult survival0, immigration0,
Chapter2 prior_selfing assurance_cost0,
investment_cost0.5, three biallelic diploid loci,
four founder genotypes, 27 complete joint genotype classes.

Select the same original path identities STILL LIVING
at the start of parent year8. For each such path,
take its original parent populations from reproductive
year1 and year8. Cross each parent state against
the year1 and year8 visitor snapshots from THAT SAME
individual visitor RNG history; never swap between
different random histories. Off-diagonal
parent × visitor combinations are one-generation
hypothetical transplants and are NOT propagated forward
or deemed new independent ecosystems.

Under original reproduce() and the original
Mendelian genotype law, evaluate three locus expected
offspring HIGH allele frequency directions and exact
self-seed, outcross paternal and outcross maternal
successful gene-transmission components in each of
the four cells.

For each source demographic path and each of the
four exact gene-transmission components, let
A=D(early-parent, early-visitor),
B=D(early-parent, late-visitor),
C=D(late-parent, early-visitor),
D=D(late-parent, late-visitor).

The exact two-order descriptive attribution is

    state=.5[(C-A)+(D-B)]
    visitor=.5[(B-A)+(D-C)]
    interaction=D-C-B+A

and state+visitor=D-A on every original path.
The 2×2 interaction must NOT be added a second
time to the already order-symmetrized state
and visitor contributions. The source parent-state
term includes all original genetic loci and N;
it is NOT the isolated causal effect of assurance
allele frequency or of a physiological selfing trait.

All three locus expected allele directions must
equal self+father+mother separately for every cell
and for each derived contrast, both pathwise and
after nested demographic averaging. The 128
paths are nested WITHIN each visitor history.

## Endpoint sign categories and limits

Use the ORIGINAL matching HIGH source expected
one-generation frequency direction, never the
realized eight-year change. Record across all
EIGHT independent simulated visitor RNG histories:

- number with early source negative / late source positive;
- number with late parents under EARLY visitor conditions
  already positive (conditional state-only transplant);
- number with early parents under LATE visitor conditions
  already positive (conditional visitor-only transplant);
- of the negative→positive flips, number requiring
  BOTH late parent state and late visitors to reach a
  positive 2×2 cell, rather than a single transplant;
- distribution of signed state and visitor
  attributions and interaction, but DO NOT
  calculate unstable percentages of signed effects
  when total difference is close to zero;
- within-history genotype matching HIGH allele
  frequency changes as a descriptive state variable.

These categories are SOURCE-MODEL expectation contrasts,
not estimates of how a real ecosystem responds to
replacing visitor communities. The next-year source
direction in one counterfactual cell does not imply
the off-diagonal environmental transplant could
produce the late state historically. The source
path cohort is selected on late survival.

Eight visitor RNG seeds are all sampled from ONE
original visitor generator AFTER outcome discovery;
they do not comprise independent natural island
sampling, preregistered heldout confirmation,
a general source theorem about sign reversals,
or a valid Ito SDE/SPDE limit. We use no frozen
prospective Chapter2 seed 37110801..37110864.

## Reproduction

    pytest -q tests/test_model3_k32_multihistory_state_visitor_cross.py
    python -m scripts.audit_model3_k32_multihistory_state_visitor_cross --budget 8 --draws 128 --out cross-new-histories-budget8.json
    python -m scripts.audit_model3_k32_multihistory_state_visitor_cross --budget 3 --draws 128 --out cross-new-histories-budget3.json

Dedicated CI job: model3-k32-multihistory-state-visitor-cross.
Numerical claims are withheld until source-locked
CI success and raw artifact inspection. PR stays Draft.
