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
