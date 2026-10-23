# R2: maternal viable seeds and full parental-genome return can favor opposite A directions

**2026-10-23 — static source-kernel comparison only, no biological evolution.** All existing R1–R5 conclusions remain untouched, including the independently founded R2 four-setting overall INCONCLUSIVE result. This is a mathematical negative control and a previously exposed source-model experiment, not a new confirmation.

## Why this matters

The original 384-path exploratory pollen factorial found a large additional A response following historically weak pollen limitation, versus small additional response after historically strong limitation. Both standing A variation and current pollen delivery differed. The new question is whether immediate *maternal seed production* correctly represents the selective return on a rare A allele. **It does not always do so in Model 3**, because genetically selfed descendants and half-shares of outcross offspring carry distinct parental-genome contributions.

The existing Model 3 donor-row/recipient-column Ledger defines a focal parent's expected genetic contribution as

    W_g = 0.5*F_maternal_outcross + 0.5*P_paternal_outcross + S_viable_self

with one copy through each outcross route and two copies in the source's viable-selfed parent accounting. At the same fixed resident state, zero pollen discount means changing one focal A allele has no direct effect on its paternal pollen export.

For delayed selfing, define q as the focal mother's outcross-fertilization fraction before selfing, v=1−inbreeding_depression, and c_A the resource-allocation cost of assurance. Holding M and I fixed, ovules are proportional to exp(−c_A A²). The local maternal return gradient is

    beta_m = v(1−q) / [q + v A(1−q)] − 2 c_A A.

The local full parental-genome return derivative is

    beta_g = [v(1−q) − 2 c_A A (0.5 q + v A (1−q))]
             / [q + v A(1−q)].

Their difference is an exact nonnegative **accounting identity**:

    beta_g − beta_m = c_A A q / [q + v A (1−q)].

It is not an estimated genetic causal-mediation component. For original v=.5 and c_A=.5, the positive-return cutoff q values at interior A are

    q*_maternal = v (1−2 c_A A²) / [v (1−2 c_A A²) + 2 c_A A]
    q*_genetic = v (1−2 c_A A²) / [v (1−2 c_A A²) + c_A A].

| Reporter A | Maternal q cutoff | Full parental-genome q cutoff |
|---:|---:|---:|
| 0.3 | 0.602649 | 0.752066 |
| 0.5 | 0.428571 | 0.600000 |

These values are **not** evolutionary phase-transition boundaries, population-fixation cutoffs, or natural-island pollen thresholds.

## Eight native frozen-source static conditions

The new diagnostic loads the original 384 pilot protocol and verifies original source-operator SHA identities before evaluating any condition. Artificial reporters contain 48 identically expressed diploid adults at M=I=.5 with A=.3/.5 and original six visitors. Four external pollen environments are evaluated per A. Only the focal plant's A expression is perturbed ±1e−6; all other adults remain fixed, and no offspring are sampled or recruited.

Each of the eight cases verifies both analytic gradients against native source finite differences, plus unchanging paternal export and source q when focal A varies. The original homogeneous q admission values give the rounded display:

| Reporter A | Pollen baseline | Future activity | Approx q | Maternal gradient | Full genetic gradient |
|---:|---|---:|---:|---:|---:|
| 0.3 | Strong | 0.4 | .145 | +1.264 | +1.344 |
| 0.3 | Strong | .04 | .017 | +2.684 | +2.700 |
| 0.3 | Weak | .4 | .995 | −.297 | −.147 |
| 0.3 | Weak | .04 | .440 | +.234 | +.360 |
| 0.5 | Strong | .4 | .145 | +.691 | +.793 |
| 0.5 | Strong | .04 | .017 | +1.369 | +1.385 |
| 0.5 | Weak | .4 | .995 | −.497 | −.248 |
| **0.5** | **Weak** | **.04** | **.440** | **−.018** | **+.172** |

The final row is a **source-specific discrepancy in payoff definitions**: total viable maternal seed production alone favors lower A, but expected parental genetic contribution favors higher A. Consequently seed counts alone must not substitute for genetic return when discussing the evolution of reproductive assurance. Neither gradient gives the actual finite-population response directly.

## How this narrows R2 without rewriting earlier science

The source's weak-limit homogeneous q can move from near-saturation (both gradients negative) to limited pollen after decline (full genetic gradient positive). Under strong limitation the static full genetic gradient is positive even before additional decline, while inherited A variation may already have been reduced. This is a **mechanistically plausible synthesis of separate source checks**; it does not identify the unique cause of the archived 384-path interaction, estimate fixation mediation, or show a natural island colonization effect.

R1's fixed-A floral decline, R3's trait-specific repeated endpoints, R4's separate preregistered G/S policy contrasts and post-outcome X, and R5's bounded transfer distinctions stay at their original evidential ranks. The classical selfing transmission advantage is not newly discovered by this one model calculation.

The exact derivative scope assumes delayed selfing, zero pollen discount and a single rare focal A change in an otherwise fixed reporter state. Prior selfing and pollen discount have different source accounting. The full expected parental-genome return is one-year accounting, **not an empirically demonstrated invasion coefficient, natural fitness measurement, or guaranteed evolutionary direction**. No additional generations, novel source founder histories, simulation outcomes, new p-values or re-registration are introduced.

## Reproduce

- Source diagnostic: scripts/audit_chapter2_r2_parental_return_boundary_20261023.py
- Numeric tests: tests/test_chapter2_r2_parental_return_boundary_20261023.py
- Original frozen design: docs/protocols/CHAPTER2_BASELINE_POLLEN_LIMIT_2X2_FROZEN_20261019.json
- Original native pollen ledger: scripts/model3_island/reproduction.py

Run from repository root:

    python -m scripts.audit_chapter2_r2_parental_return_boundary_20261023
    python -m pytest -q tests/test_chapter2_r2_parental_return_boundary_20261023.py
