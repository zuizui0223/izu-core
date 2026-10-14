# Model 3 K32: directional response versus neutral bounded frequencies

## Target and original ecological study firewall

The frozen Model 3 reproduction, pollen allocation, selfing, Mendelian
segregation and demographic rules are NOT edited. This is a finite-genetic
**counterfactual engineering diagnostic** within PR #420, not a natural-island
observation or an independent population/visitor replicate. The main source arm
is the exact original restricted genotype-count Markov transition.

Pinned configuration: K=32, mutation=0, 8 annual generations, no adult
survival or seed immigration, Chapter 2 `prior_selfing` reproduction parameters,
the same engineered four-founder 27-class joint diploid support, and only the
previously archived near visitor history **26110601** (time indices 0–7).
There is one environmental visitor history; 512 independent demographic
repetitions are nested within it. No prospective Chapter 2 confirmatory
history 37110801–37110864 is opened or reused.

## What null is constructed, and what it changes

For each source finite-population trajectory, first draw its **realized
canonical** offspring genotype counts at time `t+1`. Let `N_{t+1}`
be the source census. In a second neutral-genotype trajectory, impose that
*same* realized census, regardless of its own alleles. Generate
`N_{t+1}` neutral offspring from a full 3-locus Mendelian law using
equal parent contributions:

- If n≥2 distinct parent individuals, use uniformly weighted ordered
  pairs with the same individual excluded from its own outcross pair;
  **genotype-identical but separate plants can still mate**.
- If n=1, allow that parent's self gametes as a declared boundary
  convention.
- Use original gamete probabilities and diploid segregation; do not
  introduce linkage equilibrium approximations after sampling, fixed
  allele-grid smoothing, new alleles, mutation or immigration.
- Once the canonical source population goes extinct, the control is
  forced extinct too; no zeros are imputed as mean allele frequencies.

This control **intentionally changes the reproductive operator**:
it removes all genetic differences in reproductive contributions and
pollinator-mediated preferences. It is a *counterfactual neutral
statistical comparator*, NOT a second realization of source biology
and NOT a defensible natural no-pollinator ecological scenario. Source
census sizes are exogenous to the null; therefore its demographic
equivalence is an imposed conditioning, not a forecast of neutral
population size.

## Exact neutral-martingale property

For the high allele at any source locus, source genotype-count allele
frequency `p` is the mean fraction of high alleles across the
2*n inherited parental copies. Under uniformly selected **distinct**
ordered parent pairs, the paternal and maternal marginal distribution
is uniform over parental individuals. Thus, for the whole joint
genotype-frequency child law `q0`:

```text
E[p_high(t+1) | neutral parent counts, N(t+1)>0]
  = sum_g q0(g) * high_allele_fraction(g)
  = p_high(t).
```

This is an **exact no-direction conditional expectation**, including
all frequencies near 0 or 1. Bounded neutral frequencies can fix, but
their expectation cannot systematically rise from the initial 0.5
purely because the upper ceiling is 1. Conditioning on the survival of
the exogenous source histories does not introduce neutral genotype
selection because the source and neutral reproductive draws have
independent streams, conditional on the imposed source census path.

The source model instead predicts some nonzero directional change from
its unchanged mating/fecundity operators. A comparison of the
eight-generation paired *source minus neutral* high-allele frequency
contrasts directly tests directional response beyond a neutral
boundary/martingale baseline **in these model conditions**.

## What this null does NOT identify

1. It does not isolate selection versus mating assortment, because
   the source directional component jointly contains all source
   non-neutral mating/fitness terms.
2. It does not explain the large **negative covariance** between the
   source's accumulated expected-direction and realized finite-sampling
   components. Those are both path-dependent and can correlate when
   allele frequencies approach fixation.
3. It does not match the source joint probability distribution over
   pollen transport, population sizes, or environmental histories,
   except for imposed realized census sizes.
4. It is a post-outcome **exploratory control**, not an independent test
   of a preregistered ecological claim or full SDE/SPDE comparison.

Scientific interpretation MUST remain separated: a mean-frequency
direction beyond neutrality **does not prove** that lowered endpoint
variance is due to biological stabilization rather than a frequency
ceiling. A ceiling-matched directed null with its own feedback
assumptions would be a different later experiment.

## Executable validation

```bash
pytest -q tests/test_model3_k32_neutral_census_control.py
python -m scripts.audit_model3_k32_neutral_census_control \
  --out neutral-budget8.json --budget 8 --draws 512
python -m scripts.audit_model3_k32_neutral_census_control \
  --out neutral-budget3.json --budget 3 --draws 512
```

The PR#420-scoped `model3-k32-neutral-boundary` job in the existing
`.github/workflows/ci.yml` verifies mass conservation, exact no-drift
allele-frequency expectation, source-history firewall, paired demographic
census agreement and JSON persistence. No new auxiliary automatic workflow
is added (the repo's trigger policy is unchanged).

**Release gate:** Do not claim a successful source-run numerical comparison
until this job finishes and its archive is inspected. The full
main-branch CI and Chapter 2 scientific gate remain separate checks.


## Source-locked eight-generation execution (2026-10-09)

The exact-source test and both numerical experiments succeeded in
[GitHub Actions 37886120572](https://github.com/zuizui0223/izu-core/actions/runs/37886120572)
on source commit `789ad18c58a068ac16d1f7eec905b2fc54ad61cc`.
Full raw neutral and source trajectories are in
[artifact 11596860279](https://github.com/zuizui0223/izu-core/actions/runs/37886120572/artifacts/11596860279);
permanent compact source-locked results are in
`data/results/model3_k32_neutral_matched_census_20261009.json`.

| Budget | Surviving paired histories | Source assurance high-allele mean | Neutral assurance mean | Paired source-minus-neutral mean (MC 95% approximate interval) |
|---|---:|---:|---:|---|
| 8 | 512/512 | 0.97726 | 0.50119 | +0.47607 [+0.46002,+0.49213] |
| 3 | 501/512 | 0.98890 | 0.50497 | +0.48392 [+0.46414,+0.50371] |

The neutral process preserves expectation p=0.5 through its exact
parent-pair Mendelian transition. The strong source-model mean shift is
thus a consequence of source directional reproductive rules in this
tested simulation, **not a generic artifact of frequencies being bounded
above by 1**. The originally observed negative source direction/sampling
covariance can still be a boundary effect and is not causally explained
by this control.

The main source model also produced endpoint assurance high-allele
**fixation (p=1)** in 299/512 (58.4%) budget-8 histories and 415/501
(82.8%) budget-3 survivors, versus 0/512 (0%) and 8/501 (1.60%) in the
matched-census neutral comparator. The source-vs-neutral variance difference
at the endpoint (budget8 0.00176 vs 0.03173; budget3 0.00144 vs 0.04942)
is descriptive: the counterfactual is not mean-matched and does not
identify the contribution of ceiling versus dynamic feedback to the
source's small variance.

Additional endpoint high-allele paired differences were
matching -0.13031 (budget8), -0.08179 (budget3), and
floral investment -0.29025 (budget8), -0.33236 (budget3). These are
not real-world selection coefficients. The total ecological sample size
is one archived visitor history, not 512 independent environments.

**Acceptance boundary:** dedicated neutral CI PASSED on the exact
source SHA. Subsequent commits documenting the evidence do not revalidate
all Python versions; keep #420 Draft until the latest broad CI and
scientific gate have succeeded. No admission of full Ito SDE/SPDE,
natural-island inference, or claimed uniquely causal stabilization.
