# Model 3 K32: mean-matched frequency ceiling versus state-dependent feedback

## Goal and scope

The earlier frozen eight-generation source comparison established a strong
mean directional shift in reproductive-assurance high-allele frequency
(p ≈ 0.98 at K32), while an unbiased neutral Mendelian null with the **same
realized source census** remained close to 0.5. This **does not** explain
the source's small endpoint variance or strongly negative covariance between
accumulated conditional reproductive-filtering and offspring-sampling terms.
An allele-frequency ceiling alone can restrict endpoint variance.

This follow-up asks a narrower question: **if a control model is forced to
match the *entire eight-generation mean allele-frequency trajectory* and
the same observed source population sizes, does it reproduce the negative
cumulative covariance and late variance compression?**

The answer is NOT yet evidence of ecological selection, because matching
the mean trajectory after inspecting outcomes is explicitly exploratory.

## Protocol

- Source: original canonical Model3 genotype-count Markov transition,
  including exact mating/pollen/selfing/capped-Poisson recruitment and full
  diploid Mendelian segregation. No original Model3 source code is modified.
- Fixed K=32, mutation rate 0, zero adult survival/immigration,
  8 generations, archived visitor history **26110601 / near** only,
  27-class engineered 3-locus founder support, budget=8 or 3.
- The comparator inherits the **same realized source N at each time step**
  and retains neutral full-joint Mendelian genotype probabilities q0,
  including absent support, before applying a retrospective uniform,
  population-wide per-year exponential weight to assurance high-allele
  dosage: q_theta(g) proportional to q0(g)*exp(theta_t*b_assurance(g)).
- For each time step separately, solve theta_t by monotonic bisection
  so that the **analytical comparator cohort mean of next allele
  frequencies** equals that year's *observed source cohort mean*.
  Because the comparator uses SOURCE OUTCOMES for calibration, it cannot
  be considered an independent prediction or prospective hypothesis test.
- The comparator is **not source Model 3 biology**: it removes source
  pollinator/fecundity genotype differences and introduces an artificial
  time-varying assurance-direction bias. It retains the [0,1] frequency
  boundary, absorption at allele loss, exact full joint Mendelian support
  and per-trajectory source census.
- If the target cannot be attained without resurrecting an extinct
  allele, record the explicit status MEAN_MATCH_BOUNDARY_UNATTAINABLE
  and do **not** promote or claim successful mean matching.

For each surviving trajectory, write p(t+1)-p(t) =
[q(t)-p(t)] + [p(t+1)-q(t)], separately for source and comparator. Record
the cumulative directional and finite-sampling terms, their separate
variances and 2*covariance, endpoint assurance frequency variance and
fixation, and actual versus calibrated mean trajectory by year.

## Interpretation matrix

| Comparator outcome after matching source mean | Supported within THIS numeric case | NOT established |
|---|---|---|
| Similar late frequency variance and similarly negative cumulative covariance | Ceiling plus external time-varying directional tilt may be sufficient to reproduce the descriptive source phenomenon | Causal proof that source feedback is absent |
| Markedly greater endpoint variance or weaker negative covariance | Source dependence structure differs from this mean- and census-matched comparator | Unique identification of adaptive stabilizing selection |
| Mean target infeasible because genotype alleles already lost | Unconditional absorption constrains what a no-mutation comparator can represent | Source output is invalid; absent alleles must not be reintroduced |
| Source and comparator means not close in realized 512 draws | Insufficient Monte Carlo precision or an inadequate calibration despite matching analytical means | Confirmatory rejection of a preregistered ecological hypothesis |

The source and comparator can have different multilocus genotype structure
even after matching marginal assurance-frequency mean and N. Such
differences are possible alternative explanations for endpoint covariance.

## Reproduction and gating

    pytest -q tests/test_model3_k32_mean_matched_ceiling.py
    python -m scripts.audit_model3_k32_mean_matched_ceiling \
      --out ceiling-budget8.json --budget 8 --draws 512
    python -m scripts.audit_model3_k32_mean_matched_ceiling \
      --out ceiling-budget3.json --budget 3 --draws 512

The PR#420-scoped job model3-k32-mean-matched-ceiling in the original
.github/workflows/ci.yml executes and archives both. It enforces the
precise source conditions and refuses to endorse mean matching if
allele-absorption makes it impossible.

**Release boundary:** all results are engineering simulations from ONE old
visitor history. Do not label them natural-island evidence, independent
ecological cohorts, a causal selection proof, exact stochastic-process
equivalence, continuous-time SDE/SPDE or geographic INLA analysis.
