# Model 3, first implementation unit: reproduction and life-history exposure

Status: concrete implementation specification for review; no model-3 scientific outcomes inspected. This unit supports, but does not yet implement, evolutionary population dynamics. It does not replace either archived model class or reopen their frozen results.

## User objective

Retain the question of convergence versus region-specific floral responses. Derive eventual inherited change from reproduction rather than a best-partner/centroid movement rule. Include life history, while distinguishing repeated flowering, lifespan, effective exposure and generations. Preserve Chapter 2's current response-regime controls and place this work in a separate third model class.

## Why this is the first independent unit

Before adding inheritance, verify that viable offspring and male/female contributions balance, and that life-history exposure has a defined interpretation. These contracts can be rejected or accepted independently of any floral evolutionary outcome. An inherited-life-cycle implementation is the next separate unit; the current unit must never output an evolutionary conclusion.

## Reproductive ledger

Inputs describe one flowering episode for n focal plants:

- `transfer[i,j]`: expected compatible outcross pollen units delivered from donor i to recipient j, nonnegative finite n by n array. The diagonal must be exactly zero; autonomous selfing is separate.
- `ovules[j]`: nonnegative finite available ovules, vector length n.
- `pollen_scale[j]`: strictly positive finite pollen units in the saturation function, vector length n.
- `autonomous_selfing[j]`: probability in [0,1] that an ovule remaining unfertilized after outcross opportunities is autonomously selfed.
- `inbreeding_depression[j]`: proportional loss of selfed offspring viability in [0,1], applied once.

This first ledger implements a declared **delayed-selfing limiting case**, with no prior/competing selfing and no dynamic genetic load. `transfer` is supplied after any pollen-export loss; the ledger does not silently invent pollen discounting or trait costs. The upstream donor/visitor model must later produce transfer matrices with its own resource budget.

For recipient j:

`P_j = sum_i transfer[i,j]`

`outcross_j = ovules_j * (-expm1(-P_j/pollen_scale_j))`

`selfed_raw_j = autonomous_selfing_j * (ovules_j - outcross_j)`

`selfed_viable_j = selfed_raw_j * (1 - inbreeding_depression_j)`

Assign `outcross_j` among donors in proportion to `transfer[i,j]/P_j`, with all donor contributions zero when P_j is zero. Record the full donor-by-recipient offspring matrix. Male outcross offspring per donor are its row sums. Female outcross offspring per recipient are column sums. Viable maternal offspring are outcross plus viable selfed offspring.

Record parental genome equivalents as `0.5*female_outcross + 0.5*male_outcross + selfed_viable`. This is a bookkeeping quantity, not a population growth rate or automatically the selection coefficient in a partially selfing age-structured population.

Required identities: total maternal outcross equals total paternal outcross; total genome equivalents equals total viable offspring; no ovule is fertilized twice; zero compatible pollen gives zero outcrossing; full inbreeding depression gives zero viable selfed offspring. Expected fractional counts are allowed. No random sampling, normalization to a fixed population, gradients, trait updates or survival-to-adulthood assumptions enter this unit.

## Life-history schedule and exposure

Inputs per individual: effort per flowering season, flowering probability per season, and survival probability between adjacent seasons. Effort is nonnegative; probabilities lie in [0,1]. Let the horizon contain h seasons. Survival has length h-1. Probability of being alive in season 0 is 1; later probabilities are cumulative products of intervening survival probabilities. Expected flowering effort is alive probability times flowering probability times effort.

Record total expected effort and, if positive, normalized effort weights separately. When total effort is zero, report exposure as `not_evaluable`, not zero, one, infinity, or an invented regularized estimate. Effort is declared before outcome inspection; observed offspring counts must not be used to construct these predictive weights.

For a symmetric positive-semidefinite h by h correlation matrix R with unit diagonal, and predetermined normalized weights w, report `variance_multiplier = w.T @ R @ w`. The exposure API accepts a nonnegative finite vector of length at least one: a zero-sum vector returns not_evaluable; otherwise its sum must equal one within 1e-10, or it is rejected. Do not silently normalize a non-unit input. If variance_multiplier exceeds 1e-10, `k_eff = 1/variance_multiplier`. If its absolute value is at most 1e-10, report `zero_variance_diagnostic` with no finite k_eff; a value below -1e-10 is an error. Do not silently cap k_eff at the nominal number of episodes: negative correlation can exceed that value.

This is an equal-marginal-variance scalar diagnostic. Do not claim that it preserves nonlinear seed set, maternal and paternal fitness simultaneously, multivariate communities, or the old pooled-history k. Retain the full schedule and R in outputs. No ecological time autocorrelation is estimated from synthetic data in this unit.

## Numerical and software contract

Python >=3.10; NumPy >=1.24 already belongs to the repository dev dependencies. Modules live under `scripts/`, matching the existing modeling tools. Float64 calculations; accounting checks use absolute tolerance 1e-10 plus relative tolerance 1e-12. Correlation symmetry/unit-diagonal/eigenvalue tolerance is 1e-10. Reject nonfinite inputs, malformed dimensions, empty plant/schedule arrays, negative budgets, invalid probabilities and non-PSD correlation matrices. Do not repair or clip invalid input data. Zero-reproduction and zero-exposure states remain visible.

Deterministic test fixtures are mathematical identities, not scientific parameter estimates. The first receipt contains test identities and hashes, not evidence for convergence, divergence or an S/C/I transition.

## Next units, explicitly outside this implementation

1. Visitor activity, attraction/access, finite pollen resources and carryover produce transfer matrices and resource-dependent ovule/pollen budgets.
2. Maternal/paternal sampling and diploid inheritance, followed by annual/stage-structured survival and recruitment. Include a no-selection drift control and sorting-only comparator.
3. Freeze the biological parameter ensemble, horizons and intervention outcomes before running a scientific comparison. Keep conditional S-reduction and persistent-S alternatives rather than requiring either outcome.

This boundary prevents verification of a reproduction calculator from being presented as completion of the full life-history evolutionary model.
