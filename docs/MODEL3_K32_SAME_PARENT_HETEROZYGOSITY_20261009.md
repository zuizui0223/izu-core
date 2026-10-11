# PR #420: One-step same-parent genotype variance at exactly matched means

## Why this check replaces the earlier variance claim

The demographic 256/256 cross-fit showed a **sign reversal** of the
eight-generation source-minus-comparator endpoint variance when the
training and holdout halves were reversed (budget3). In addition,
holdout endpoint assurance allele-frequency means were unequal,
and frequencies close to fixation have reduced available variance.
Consequently an autonomous source-specific **stabilizing variance
mechanism is not identified** by the old-history cross-fit.

A sharper analytical diagnostic avoids both eight-year external
trajectory calibration and cross-fit endpoint mean mismatch by
conditioning on the **same integer parental genotype census** from
the original finite Model3 process.

## Source and counterfactual

- Source: complete joint 3-locus diploid parental genotype counts from
  original Model3, exact canonical reproductive mating intensity and
  pollen exclusion, and exact Mendelian child genotype law q_source.
- Counterfactual: **same parent state**, but a neutral equal-gamete
  Mendelian law q0 that samples both ordered parent gametes uniformly
  **with replacement, including same-individual self pairs**. Reweight
  q0 by an external assurance-dosage exponential tilt so its expected
  high-allele frequency matches q_source **at that same parent state**.
  This differs intentionally from the earlier distinct-individual
  neutral control. The full parent-pair support ensures that a source
  selfed genotype cannot fall outside the comparator's support.
- Both offspring distributions use exactly the SAME capped-Poisson
  recruitment intensity, same N distribution and same conditional
  target mean. The null deliberately changes reproductive weights; it
  is **not original Model3 biology**.
- Population states to be audited arise independently from original
  source trajectories for years 0..7, with one pre-existing OLD
  visitor history 26110601 (near), K32, zero mutation/adult survival/
  seed immigration, Chapter 2 prior_selfing biology, existing engineered
  four-founder/27 genotype-class genetic support. Budget8 and budget3
  remain separate sensitivity regimes.
- If the matched mean cannot be attained on the inherited support, the
  code records an explicit **MATCHED_MEAN_UNATTAINABLE** status.
  Do not create lost alleles, alter the source genotype or waive the
  matching equality.

## Exact structural identity

For a diploid high-allele dosage in the offspring,
b ∈ {0, 1/2, 1}, define

```text
mu = E_q[b],
H  = P_q(b=1/2).
```

Then `b^2 = b - (1/4)*I[b=1/2]`, hence exactly:

```text
Var_q(b) = mu * (1-mu) - H/4.
```

For conditionally iid joint Mendelian offspring with the same positive
realized census N, mean high-allele frequency variance equals
`Var_q(b)/N`. Averaging over the SAME capped-Poisson N conditional on
occupation produces

```text
V_source(C) - V_control(C)
 = -(H_source(C) - H_control(C))/4 * E[1/N | N>0, C].
```

This equality is exact at each current source parent state C. It
removes the algebraic `mu(1-mu)` boundary term from the *conditional*
contrast. The **remaining heterozygosity difference** is a
description of the offspring genotype distribution, NOT causal proof
that pollinators or selfing alone produced adaptive variance regulation.

The sample path ensemble averages and their Monte Carlo SE are only
uncertainty among demographic histories nested within ONE visitor
environment, not independent ecology replicates. Across years,
the same demographic histories recur and observations are correlated.

## Scientific interpretation

If source and counterfactual offspring variance match after holding
parent genotypes, N law and allele mean fixed, the source has no extra
one-step assurance-frequency dispersion under THIS neutral-tilt null,
even if their autonomous eight-year endpoint distributions differed.

If the dispersion still differs, the matched conditional difference is
exactly traceable to offspring heterozygosity at this locus.
The expected frequency direction is held equal, so this identifies
a *within-generation genetic packaging* distinction, not a
unique stabilizing-selection mechanism.

**Neither case by itself explains the large negative covariance of
eight-generation cumulative source filter and sampling terms.** That
long-horizon correlation depends on nonlinear state feedback, repeated
drift and absorption; it cannot be separated by a one-step identity.

## Run and evidence boundary

```bash
pytest -q tests/test_model3_k32_same_parent_heterozygosity.py
python -m scripts.audit_model3_k32_same_parent_heterozygosity --budget 8 --draws 512 --out same-parent-budget8.json
python -m scripts.audit_model3_k32_same_parent_heterozygosity --budget 3 --draws 512 --out same-parent-budget3.json
```

The core CI includes a PR#420-only same-parent-moments job and uploads
the JSON as an engineering artifact. Source canonical biology code
remains unchanged. No prospective confirmatory cohorts (37110801..64),
natural island observations, geographic INLA or full SDE/SPDE is used.

**Do not promote results until the head's numerical CI and source
artifact have been checked.**


## Validated old-history numeric result

Run [37889777989](https://github.com/zuizui0223/izu-core/actions/runs/37889777989)
executed the dedicated `model3-k32-same-parent-moments` job
successfully at source SHA `76e83d2917024da9dced0ce59bfbb224b2b92550`
(Python 3.11). The exact equality and old-history guards passed for
both budgets. The [full raw executed JSON artifact 11597781387](https://github.com/zuizui0223/izu-core/actions/runs/37889777989/artifacts/11597781387)
has SHA256 `6d1ae5a0e57215cf8f4249b7c52d2dba7c279a46677ace39a1cdc68633081826`.
Permanent concise result:
`data/results/model3_k32_same_parent_heterozygosity_20261009.json`.

### Eighth-year source parent states (analytical next-generation moments)

| Mean across comparable source parental states | Budget 8 | Budget 3 |
|---|---:|---:|
| States with nonempty parents | 512 | 509 |
| Same next-generation expected assurance high-allele frequency | 0.977777 | 0.982318 |
| Source q heterozygote probability | 0.019987 | 0.011805 |
| Mean-matched comparator q heterozygote probability | 0.040535 | 0.026669 |
| Source next living-population high-allele frequency variance | 0.000477218 | 0.000989500 |
| Comparator next frequency variance (identical mean and N law) | 0.000316682 | 0.000687698 |
| **Source minus comparator** one-step conditional frequency variance | **+0.000160536** | **+0.000301802** |
| Nested demographic-parent-state MC SE of the difference | 0.0000112 | 0.00006377 |
| Maximum algebraic identity residual | 3.65e-17 | 4.69e-17 |
| Mean-match support failures | zero | zero |

Across all eight generations, the average source-minus-counterfactual
conditional variance difference was positive in both budget regimes.
Its size shrinks late as assurance allele frequency approaches one.
The *source* offspring heterozygosity probability remained BELOW the
counterfactual at the evaluated parental states. Consequently a mean-
and-census-matched source step has **larger finite allele-frequency
noise**, even though its long-horizon endpoint allele-frequency
variance is **smaller** when assurance is nearly fixed.

This distinction is essential:

1. **Between independent populations at the eight-year endpoint:**
   allele fixation and previous genotype state histories compress the
   observed distribution; this statistic compares different parental
   distributions and depends on the previous outcomes.
2. **Within one parent genotype census for the next birth episode:**
   the source law yields fewer heterozygous offspring, which increases
   conditional frequency variance relative to this full-support,
   mean-matched counterfactual. This is an exact one-step identity
   comparing two different reproductive kernels at the **same** state.

The counterfactual here permits same-parent gamete pairs (with
replacement), deliberately unlike the earlier distinct-individual
neutral comparator. This prevents source selfed offspring support from
being artificially deleted. Exact mean 0/1 cases are defined by
the boundary limit of exponential reweighting, not an illegal
finite-weight approximation or reconstructed allele.

### Implications and strict stop line

The one-step result identifies **offspring heterozygosity as the exact
algebraic mediator of variance differences after matching mean and N**.
It does NOT establish selfing alone as the causal mechanism: pollen
matching, source fecundity, individual mating weights and selfing are
joint in the source operator. It does not imply **stabilizing selection**,
nor does it resolve a robust source-specific eight-generation variance
reduction (that prior claim was undermined by the two-fold holdout sign
reversal). Such a claim would require further mechanism-specific
counterfactuals and ecologically independent confirmation.

The tests used only one old visitor history, artificial fixed
genotype support and nested source simulation repeats. Frozen
confirmatory history seeds and natural island data remain unused;
there is no geographical INLA or validated complete SDE/SPDE.
