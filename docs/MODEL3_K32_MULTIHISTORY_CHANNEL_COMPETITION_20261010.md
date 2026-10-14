# Model3 K32 — What drives the positive parent-state contribution across eight visitor histories?

## Scientific location

The fully CI-verified original source 2×2 parental-state × visitor-year
cross over all eight post-discovery visitor RNG histories 26110602–26110609
gave a POSITIVE order-symmetrized matching-high allele expected-direction
state contribution in 8/8 simulated histories under each budget.
Yet late expected directions were not universally positive, and visitor
effects were often negative. The previously reported old-reference
~82–85% attribution cannot be transferred as a universal signed ratio
because state and visitor contributions can have opposite signs.

This audit does not generate any additional visitor history, change
canonical source mating biology, rerun source genotype trajectories,
or touch the prospectively frozen Chapter2 confirmatory cohort.

## Exact original source reproduction components

Each source 2×2 cell uses the canonical reproduce() ledger,
complete 27-class diploid genotype state, original Mendelian gamete
inheritance, K32, 0 mutation/survival/immigration, Chapter2
prior_selfing and one of the same eight archived within-history
original visitor snapshots. On a common subset of original source
parent paths alive at year8, allele direction decomposes EXACTLY:

    D_matching = viable_SELF_transmission
               + outcross_FATHER_transmission
               + outcross_MOTHER_transmission.

The two-order state and visitor contrasts are linear combinations
of these individual-cell quantities. Therefore the same exact
identity holds for each contrast and for the average across histories:

    State_D = State_SELF + State_FATHER + State_MOTHER,
    Visitor_D = Visitor_SELF + Visitor_FATHER + Visitor_MOTHER.

We use the ALREADY ARCHIVED complete two-budget source cross JSONs,
not the compact table, in order to preserve each original
individual visitor history, its per-channel mean, and demographic
standard error.

## Inference unit and estimands

Report for each budget separately:

- mean signed contribution from each channel, across exactly
  **eight independent visitor RNG histories**;
- the between-history sample standard deviation and its descriptive
  8-history mean SE, which is NOT uncertainty over natural islands;
- counts of positive, negative, or exactly zero visitor-history
  channel contributions — not 128 × 8 independent observations;
- per-history channel results, including historical sign-flip
  status and source year8 survivor count;
- the same decomposition for the visitor-year effect and total
  original observed diagonal source early→late change;
- exact 3-locus identities and original provenance checks.

Each original source history's 128 demographic source
trajectories are nested and cannot be pooled into one
false ecological sample. Both budget3 and budget8 use
the SAME eight ecological RNG histories, not 16 environments.

## Scientific interpretation boundary

A positive source viable-self marginal term does NOT prove that
more selfing was independently selected for, that it alone
caused a directional switch, or that pollinators became
unimportant. Selfed-seed gene-transmission direction is
a covariance under original genotype-dependent source
reproduction — allele composition, assurance, investment,
matching, census, and prior demographic stochasticity can
all contribute.

If self transmission is positive in every history but outcross
contributions are negative in most, the supported finding is a
**competing-channel model property**, not a deterministic
adaptive result. This distinction matters because the original
total late allele direction remains negative in some histories.

Only synthetic visitor RNG histories selected AFTER previous
outcome exposure are studied, one original visitor simulator,
zero natural island measurements, zero new preregistered
confirmatory visitor histories and no verified complete
SDE/SPDE continuum inference. Historical visitor state
crossing is non-autonomous one-step reproductive expectation.

## Reproduce and gate

    pytest -q tests/test_model3_k32_multihistory_channel_competition.py
    python -m scripts.audit_model3_k32_multihistory_channel_competition \
      --budget8 cross-new-histories-budget8.json \
      --budget3 cross-new-histories-budget3.json \
      --out multihistory-channel-competition.json

Within PR420 CI job model3-k32-multihistory-state-visitor-cross,
first rerun the exact original 8-history crosses then compute the
channel source-lock from those TWO raw JSONs, verify the
self + father + mother sums for each locus and contrast,
and archive the derived compact report with the raw sources.

The current numerical estimates require source-linked CI to
succeed before being described as repository-verified evidence.


## CI-verified original Model3 channel competition

The original K32 source parent/visitor 2×2 cross and new three-channel
postprocess were independently checked in
[GitHub Actions 38008400006](https://github.com/zuizui0223/izu-core/actions/runs/38008400006),
job `model3-k32-multihistory-state-visitor-cross`, **SUCCESS**
on scientific SHA `5db5822d4ba523459599160c170e1198de4b52cc`.
The [raw archived original budget8, budget3 and per-channel
outcomes (artifact 11652381028)](https://github.com/zuizui0223/izu-core/actions/runs/38008400006/artifacts/11652381028),
SHA256 `f8fd68b9a3f5b04923259e8e13280b1b1a00b763ce0584eef146393dacd71cc0`,
contain all eight source visitor RNG histories, all three
genetic loci, all four self/father/mother/total terms and
the corresponding state × visitor contrasts.

Compact permanent receipt:
`data/results/model3_k32_multihistory_channel_competition_20261010.json`.

### Why source state pushes matching HIGH direction positive but ecology does not always

Reported as the mean over EIGHT equally weighted source
visitor RNG trajectories, each with 128 nested original
demographic paths, same late-surviving parent identities
across early/late cells. Values are original Model3
**expected one-generation allele-frequency DIRECTION
contrasts**, not realized genetic frequency changes.

| Symmetrized source PARENT-STATE contribution to matching-high direction | Budget8 mean ± among-history SE | Budget3 mean ± among-history SE | Number positive (budget8 / budget3) |
|---|---:|---:|---:|
| **Viable SELF seed allele transmission** | **+0.040252 ± 0.003280** | **+0.038802 ± 0.002366** | **8/8, 8/8** |
| Outcross pollen FATHER transmission | -0.002950 ± 0.002312 | -0.003045 ± 0.003350 | 2/8, 2/8 |
| Outcross maternal RECIPIENT transmission | -0.006818 ± 0.002511 | -0.006920 ± 0.003512 | 2/8, 2/8 |
| **Outcross father + mother summed** | **-0.009767** | **-0.009965** | 2/8, 2/8 |
| **Total parent-state attribution** | **+0.030485 ± 0.007453** | **+0.028837 ± 0.008693** | **8/8, 8/8** |

The corresponding visitor-year contribution averaged
**−0.005291 ± 0.005561** budget8 and
**−0.005138 ± 0.004969** budget3; the signed
visitor contribution was negative in 5/8 histories
under both budgets. Its selfed seed component
was small on average (−0.000624 / −0.000648);
its combined outcross father+mother component
was more negative (−0.004667 / −0.004490).

Hence the old single-history explanation needs to
be REFINED: the *positive signed SOURCE parental-state
effect* across these eight post-outcome histories is
largely a positive viable SELF seed transmitted-allele
component, while source outcross father/mother
component **counteracts it in six of eight histories**.
Visitor-year changes themselves often act through
negative outcross-parent transmitted allele marginals.
These patterns explain why it is possible to
have all eight positive parental-state contributions
but still only 4/8 or 5/8 negative→positive final
source direction sign reversals.

### Limits: reproduction accounting, not independent causal selection

The phrase "self term dominates" means the EXACT
source selfed-seed successful-gene-transmission
covariance, which changes with genotype
frequencies, assurance, investment, census and
survivor selection. It does **NOT** mean source
selfing alone causally favors the matching-high
allele, and it does **NOT** show natural adaptive
preservation of nectar-guide or pollinator
matching traits. An exact positive self term can
be predicted algebraically for these source
population/genotype histories yet fail to
make matching-high expected direction positive
when initial selection pressure is strongly
negative or visitor/outcross source effects
oppose it.

The between-history SEs are descriptive of just
eight different stochastic visitor histories
sampled from ONE source visitor generator after
the original source sign-flip discovery. Neither
the 128 nested paths per history nor the
budget8 and budget3 repetitions are
independent ecological environments.
There are no actual island populations,
no preregistered external visitor history
confirmation, no field pollinator-selection
fitness measurement and no demonstrated
complete SDE/SPDE continuum approximation.
