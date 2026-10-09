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


## Source-verified results across the eight visitor histories

Dedicated `model3-k32-multihistory-state-visitor-cross`
CI **PASSED** on original source SHA
`0abd8157a9d2f79527c1fb7bb07237cd953b946a`
in [Actions run #37956149435](https://github.com/zuizui0223/izu-core/actions/runs/37956149435).
The [full executed two-budget 2×2×8-history evidence archive #11627938030](https://github.com/zuizui0223/izu-core/actions/runs/37956149435/artifacts/11627938030)
has SHA256 `03ce2a0abbbcc5c87057d8265211c9e539b05e2007a7d9331a18cfe86f1a26a8`.
It contains every surviving demographic path's source-history
conditional Mendelian 2×2 factor outcomes summarized separately
for three loci and original self/father/mother channels.
The compact, CI-linked result is
`data/results/model3_k32_multihistory_state_visitor_cross_20261010.json`.

### Broad result: consistent genotype-state contribution, variable visitor contribution

Eight NEW post-discovery exploratory visitor RNG histories
26110602..26110609, 128 nested original demographic source
paths per history, same source K32 settings as previous work:

| History-level source-model sign or direction | Budget8 | Budget3 |
|---|---:|---:|
| New distinct visitor RNG histories | 8 | 8 |
| Original matching-high allele expected direction negative early | 6/8 | 6/8 |
| Original matching expected direction positive late | 5/8 | 6/8 |
| Negative early to positive late source sign flips | 4/8 | 5/8 |
| **State contribution positive, 2-order average** | **8/8** | **8/8** |
| **Visitor-year contribution negative, 2-order average** | **5/8** | **5/8** |
| **Among observed flips: late parent × EARLY visitor already positive** | **4/4** | **5/5** |
| Among observed flips: EARLY parent × late visitor already positive | 0/4 | 0/5 |
| Among observed flips: both late parent and late visitor conditions required | 0/4 | 0/5 |
| Mean signed state contribution over histories | **+0.030485** | **+0.028837** |
| Mean signed visitor contribution over histories | **−0.005291** | **−0.005138** |
| Range of state contributions | +0.007024 to +0.070266 | +0.001587 to +0.075045 |
| Range of visitor contributions | −0.029922 to +0.018692 | −0.027446 to +0.015415 |

These values are averages over VISITOR RNG histories with
equal history weight; 128 demographic paths per visitor RNG
seed are **nested** and not 1024 independent ecological histories.
Each within-history parent-year pair uses precisely the same
late-original source survivor path identities in all 2×2 cells.
A positive source state contribution is not a universal ecological
reversal: the initial negative direction can be too large
and visitor changes can oppose the source state shift.

### Cases that directly distinguish mechanisms

| Visitor seed | Budget8 parent-state contribution | Budget8 visitor contribution | Early original direction → late original direction |
|---|---:|---:|---|
| 26110603 | +0.032761 | +0.018692 | −0.037581 → +0.013873 |
| 26110605 | +0.024076 | **−0.019369** | −0.002780 → +0.001928 |
| **26110606** | +0.007024 | **−0.029922** | **+0.021864 → −0.001033** |
| **26110607** | **+0.070266** | 0 | **−0.077490 → −0.007223** |
| 26110609 | +0.052450 | **−0.013307** | −0.041096 → −0.001954 |

- Seed **26110603**: both the parental state and visitor
  changes contribute positively. The evolved late source
  parent with the EARLY visitor community already gives
  positive expected direction (+0.001187); the same
  INITIAL parent with late visitors remains negative
  (−0.012882).
- Seed **26110605**: state change is positive but
  later visitors produce a negative net contribution.
  The state contribution exceeds the ecological
  opposition, and late original direction is positive.
- Seed **26110606**: the direction changes
  from initial POSITIVE to late NEGATIVE. The visitor
  change is more negative than the positive state
  contribution; therefore the parental-state trend
  cannot guarantee reversal in the desirable direction.
- Seed **26110607**: visitor snapshots at early and
  late in the cross yield the SAME mating environment
  contribution (zero at this source-factor level).
  The state contribution is strongly positive
  +0.070266 but does not overcome the very
  negative early direction −0.077490. Late
  expected matching direction remains negative.
- Seed **26110609**: an initially negative
  direction moves closer to zero but remains
  negative under budget8; under budget3 it just
  crosses positive.

### Why this materially changes the scientific claim

The old-history 26110601 state contribution of
82–85% was specific to ONE historical visitor
trajectory. The newly crossed eight histories
show an **invariant positive SIGN of the source
parent-state contribution** in this exploratory
set but NOT an invariant positive visitor
contribution or invariant late expected allele
direction. The visitor contribution is often
negative, and signed ratios could exceed
100% or be unstable when the total direction
change is small. Therefore do NOT quote one
universally fixed "state percentage" mechanism.

This is a mechanistic accounting result, NOT
a demonstration that changing assurance
allele frequency by itself is the direct cause:
the source parental state contains all three
joint diploid loci, source individual census and
prior genotype-selective filtering/drift. The
visitors are generated from one synthetic
ecological simulator; the crossed off-diagonal
cells are original SOURCE reproduction at a
hypothetical one-step visitor transplant, not
autonomous ecological or evolutionary trajectories.
The exact two-order state/visitor decomposition
cannot be interpreted as statistically independent
causal effects from natural fields.

The source cohort is selected on survival to
year8; all eight histories were newly simulated
AFTER observing an interesting old-history
sign reversal. No prospective frozen Chapter2
confirmation seeds, natural island observations
or validated SDE/SPDE limit were used. This
precludes a general pollinator-change law or
ecologically confirmed adaptive genotype
response.
