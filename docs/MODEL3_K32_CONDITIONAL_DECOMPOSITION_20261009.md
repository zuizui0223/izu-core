# Model 3 finite stochastic versus deterministic proxy — identifiable error decomposition

## Scientific question

Under the **same frozen Model 3** mating, inheritance and birth-census
law, why can a single deterministic expected-value trajectory differ from
the realized distribution of finite-population trajectories? Disentangle
three **mathematically declared contrasts** without claiming to identify a
unique biological effect of "drift" or a stand-alone continuous-time SDE.

**Fixed engineering design:** K=32, mutation rate=0, eight annual updates,
zero adult survival, zero immigration, canonical Chapter 2 prior_selfing
parameters, engineered four-founder two-allele-per-locus genotype support
(27 joint diploid classes); OLD archived near visitor history **26110601**
for years 0–7. Two separate reproductive resource budgets, 8 (primary)
and 3 (stress). No future independent visitor cohorts 37110801–37110864,
no natural island observations, no alteration of scripts/model3_island/.

## Exactly matched source conditional law

For an integer vector of full-joint diploid genotype counts C_t,
canonical reproduce() yields parental pairing weights, a total viable
offspring intensity lambda(C_t,E_t), and the exact Mendelian genotype
probabilities q(C_t,E_t). The next realized cohort is

    N_{t+1} = min(Poisson(lambda),32);
    C_{t+1} | (N_{t+1}=n,C_t,E_t) ~ Multinomial(n,q).

The six allele types in the engineered support are tracked separately
from the 27 diploid genotype classes. Genotypes may reappear from
segregation, but a fully lost allele cannot return under zero mutation
and no immigration. Extinction is absorbing.

For h among *next census*, *extinction*, *realized diploid genotype
richness*, *lost allele types*, or *occupancy-weighted survivor trait
mean numerator*, the function F_h(C_t)=E[h(C_{t+1}) | C_t,E_t] is computed
analytically. The lost-allele calculation uses the probability that a
single offspring genotype contains no copy of a given allele, raised to
the number of independent offspring, averaged over the capped-Poisson
distribution (including N=0). No trait mean is fabricated for an extinct
population: the numerator is 0 when unoccupied and the displayed
population trait mean would be obtained by dividing aggregate trait
numerators by aggregate occupancy.

## Telescoping finite-state identity

From M independent demographic runs *nested within one old visitor
history*, let X_t^{(i)} be the realized **integer** parental genotype
census, bar X_t its ensemble average, and R_d(bar X_t) the
Hamilton/largest-remainder deterministic integer representation.

Let R_u(bar X_t) be a **pre-declared unbiased dependent-rounding
distribution**: E[R_u(bar X_t)] = bar X_t and 0<=sum_g R_u,g<=32.
It preserves expected genotype copy counts, including exact zero support,
while allowing integer count vectors acceptable to the unmodified
individual-based reproductive operator.

Define:

    A = empirical mean h(X_{t+1}^{(i)})
    B = empirical mean F_h(X_t^{(i)})
    C = MC mean F_h(R_u(bar X_t))
    D = F_h(R_d(bar X_t))

Then the audited equality is **exact algebra**:

    A - D = (A - B) + (B - C) + (C - D).

Interpretations and limitations:

- A−B: finite-realization Monte Carlo residual conditional on the
  observed parental states, with a paired conditional residual SE.
  **Not the causal effect of drift on mean evolution.**
- B−C: state-distribution contrast (same average parent counts,
  different higher moments). It depends on the specified unbiased
  rounding reference and includes nonlinear source responses. **Not a
  uniquely isolated Jensen/selection term.**
- C−D: effect of this particular integerization convention compared
  with unbiased dependent rounding, again source-law evaluated.
- A−D: total discrepancy relative to the deterministic representative
  at that **generation**. D is not the whole eight-generation
  deterministic plug-in path; changes in D are calculated from the
  exact ensemble mean of current parental states. No claim that
  this is a causal decomposition of the difference between autonomous
  long-run dynamical models.

The source-state contrast is zero in the first generation by design
because every finite run shares the same integer founder census. The
randomized-rounding procedure does NOT change biological inheritance:
it is an explicit auxiliary mathematical reference to isolate one
numerical convention.

## Law of total variance: a second, more direct stochasticity diagnostic

With N=next-generation census and X=current parental genotype census,

    Var(N) = E[Var(N|X)] + Var(E[N|X])

when the outer distribution is the **empirical finite-source parent
ensemble**. Each term is computed from the original capped-Poisson
recruitment kernel, not from a Gaussian or SDE. Compare the sum with
the independently sampled observed next census variance. The finite
difference is Monte Carlo precision, not a new biological mechanism.

This gives a proper separation of **conditional demographic noise**
and **between-parent-state heterogeneity**, but does not separate
selection from drift in the trajectories that generated those states.

## Reproducibility

Run:

    python -m scripts.audit_model3_k32_nonlinearity_rounding \
      --out decomposition-budget8.json --budget 8 --draws 512 --rounds 256

    python -m scripts.audit_model3_k32_nonlinearity_rounding \
      --out decomposition-budget3.json --budget 3 --draws 512 --rounds 256

    pytest -q tests/test_model3_k32_nonlinearity_rounding.py

The existing core automatic ci.yml contains a PR#420-only extra
numerical job, alongside the normal Python 3.10/3.11/3.12 tests.
Outputs are archived as model3-k32-decomposition-engineering when this
job succeeds. The auxiliary Model3 workflows remain manual-only under
the repository's workflow-trigger policy.

**STOP line:** No new biological histories, field fit, parameter
retuning, full deterministic-PDE numerical validity, Ito SDE or SPDE
is inferred from this finite-source comparison. The three contrasts
are mathematically useful, but their ecological generalization requires
independent visitor history replication and source-operator sensitivity.
