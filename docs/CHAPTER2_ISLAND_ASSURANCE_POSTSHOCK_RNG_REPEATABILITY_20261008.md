# Conditional demographic randomness after island-history assurance allele transfer

**Date:** 2026-10-08. **Status:** exploratory technical repeatability test, NOT a new independent visitor-history confirmation, NOT a genetic mediation estimate. Frozen protocol `data/design/chapter2_island_assurance_postshock_rng_repeatability_20261008.json`.

## Why this is needed

In the original 16-visitor-history, four-setting genotype-state transplant, the full far-history assurance donor and a bounded allele shift that gave the recipient the **same donor assurance mean** produced almost identical *immediate viable maternal output* but sometimes differed in population occupancy after 80 updates. The original independent16 preregistered pollination-mode comparison **FAILED** (+0.140625; 95% visitor-history bootstrap [−0.078125,+0.359375]). Its favourable-looking post-outcome secondary comparisons must not be promoted to confirmation.

A residual occupancy difference is not, by itself, evidence for the causal effect of allele variance: finite recruitment uses random parent selection, survival and mutation, and the two interventions also change allele variances and inter-trait genotype associations. We therefore tested how strongly the residual depends on the **post-switch demographic random stream**, keeping everything biological at the start of the shock unchanged.

## Fixed comparison

Use the **first four visitor-history seeds** (35100801–35100804) of the existing 16-history experiment, selected deterministically by seed order rather than biological outcome. Rerun the identical 400-update historical populations and eight-individual bottleneck with demographic repeat 35101801. Under all four mating-system settings and both near/far recipient backgrounds, compare:

1. Full donor: ranked transfer of both far/near donor assurance alleles to the recipient.
2. Mean target: original recipient assurance alleles shifted boundedly to the **same donor mean**.

For each paired state, run post environments near/far × ovule budget 3/4 × **eight independent post-shock demographic streams** with common random numbers within each full-donor/mean-target pair. All outcomes are terminal occupancy after 80 reproductive updates. There is no plant immigration.

The complete grid contains 16 setting×history groups, 64 genetic treatment states, **1,024 matched postshock pairs and 2,048 postshock trajectories**. The **independent ecological sample size is four visitor histories**. The eight postshock repeats are nested within these histories; they quantify conditional finite-sampling sensitivity, not ecological generality.

## Result: almost equal first-generation payoff, nonidentical later occupancy

The table shows **full donor minus mean-target occupancy** (percentage points), the number of discordant binary terminal occupancy pairs among 128 matched postshock cases per setting/background, and the difference in initial viable maternal output per plant.

| Setting | Recipient background | Occupancy difference | Discordant matched pairs | Immediate viable maternal difference |
|---|---|---:|---:|---:|
| Delayed control | Near | −2.34 pp | 5/128 | +0.000160 |
| Delayed control | Far | −4.69 pp | 12/128 | +0.000104 |
| Prior selfing | Near | +2.34 pp | 15/128 | −0.000071 |
| Prior selfing | Far | +1.56 pp | 8/128 | −0.000009 |
| Pollen discount | Near | +2.34 pp | 9/128 | −0.000003 |
| Pollen discount | Far | +8.59 pp | 15/128 | +0.000158 |
| Direct assurance cost | Near | −0.78 pp | 7/128 | −0.000394 |
| Direct assurance cost | Far | +0.78 pp | 3/128 | +0.000118 |

The difference depends on which stochastic postshock realization was drawn. For delayed-control far recipients, the average paired occupancy difference **among the four historical groups** changed from −18.75 to +6.25 pp across the eight postshock randomizations. For pollen-discount far recipients, it ranged from 0 to +18.75 pp across repeat IDs and was positive when averaged within each of the four historical visitor seeds (+12.5, +9.375, +3.125 and +9.375 pp).

The former shows finite sampling uncertainty can flip the apparent magnitude and direction in a small pilot. The latter means it would also be incorrect to declare every residual due to chance: within the current four-history model scope, the pollen-discount far-donor genotype can retain a reproducible **conditional** edge after averaging repeated demographic streams. Yet it could reflect allele variance, cross-trait association or other differences between the two synthetic allele interventions, not one identified mechanism.

## Scientific interpretation and next causal boundary

The stage-specific distinction is now explicit:

**Immediate reproductive payoff**: the selfing-mating accounting is closely approximated by changing the current assurance mean; this is not novel in itself because it closely follows the mating system's specified fitness rules.

**Longer-term finite persistence**: rare extinctions and recruitment trajectories need not be predicted by the initial female viable-output mean. For the same evolved historical genotype and common visitor process, multiple demographic realizations can yield different endpoint occupancy outcomes. A few genotype-treatment differences survive averaging over the eight replicates, but there is no basis to isolate a unique allele-variance mechanism at four ecological histories.

Do not conflate this technical stochastic replication with a second independent evolutionary confirmation. Before making an Ecology Letters-level causal claim about genetic variance or path dependence, distinguish (a) trait-mean intervention, (b) variance/covariance intervention holding the target mean, and (c) independent visitor-history generality; specify genetic association assumptions and a principled demographic-risk range **before new outcomes**. The previous findings about timed mutational-access order remain failed or exploratory.

## Reproducibility

- Machine-readable design: `data/design/chapter2_island_assurance_postshock_rng_repeatability_20261008.json`
- Result: `data/results/chapter2_island_assurance_postshock_rng_repeatability_20261008.json`
- Replayer: `scripts/run_chapter2_island_assurance_postshock_rng_repeatability.py`
- Aggregator: `scripts/summarize_chapter2_island_assurance_postshock_rng_repeatability.py`
- Manual four-shard workflow: `.github/workflows/chapter2-island-assurance-postshock-rng.yml`
- Local complete raw SHA256: `1d08f199a722ca6f9f6ce1c99fbcc57b17e8a19c09736bb9fb36438aa15f11e3`; GitHub Actions independently reproducing this new result is **not yet established**.
- Biological source is the archived 2026-10-06 four-setting model snapshot, not a changed reproduction model.
- No public DOI or named-island empirical calibration exists for this experimental extension.

**Decision:** Keep PR #413 Draft and preserve all previous preregistered failures. Do not promote the remainder after matching assurance means to a claim that allele variance causes evolutionary rescue.
