# Why the equal-A pilot cannot test a substantial positive survival benefit

**2026-10-18. Source-derived diagnostic, not a new evolutionary experiment.**
Single paper: PR #590. Existing equal-initial-A pilot and read-only review: PR #597.
The frozen pilot, its seeds and its 42/72 versus 58/72 HIGH-I losses are unchanged.
This addition integrates transition probabilities; it does not sample populations.

## Decision

Do not enlarge the existing B=8 experiment to claim a positive survival-rescue
benefit of A evolution. Under the exact source conditions, the fixed-A comparator
already has an 80-update extinction-probability upper bound of approximately
**1.6075e-15**. Therefore the largest possible positive difference
`P(alive_80 | evolving A) - P(alive_80 | fixed A)` is at most the same bound.
This is a comparison theorem evaluated numerically, not an inference that zero
observed deaths proves a zero true risk. A negative survival effect is not ruled out.

The genetic-access question remains informative in this environment: both
populations can survive while HIGH-I support disappears at different rates.
A survival companion needs an explicitly distinct, pre-specified demographic
challenge; it must not be silently pooled with the original experiment.

## Source and analytical proof

Pinned source commit: `cc17c7355d27b907b71b124046990b914e4963dd`.
The original CI checked merge `57d022dfd382eef4df2e63f9e0aebb451ae46605`.

- [`reproduction.py`](https://github.com/zuizui0223/izu-core/blob/cc17c7355d27b907b71b124046990b914e4963dd/scripts/model3_island/reproduction.py)
  specifies annual viable maternal output under delayed selfing.
- [`population.py`](https://github.com/zuizui0223/izu-core/blob/cc17c7355d27b907b71b124046990b914e4963dd/scripts/model3_island/population.py)
  draws Poisson potential recruits and caps them at available capacity.
- The frozen equal-A design sets K=48, no adult survival, no seed immigration,
  no mutation at any locus, direct assurance cost .5, and fixed expressed A=.5.
  The base design gives ovule budget B=8, investment cost .5 and depression .5.
- Founder I alleles lie in {.375,.5,.625}; expressed I is a diploid mean.
  Closed inheritance therefore keeps every descendant I in [.375,.625].

Let q_i be the effective outcross fertilization fraction, v=1-delta=.5,
and O_i=B exp(-.5 I_i^2-.5 A_i^2). The native parentage ledger has total
viable offspring expectation

```
Lambda_t = sum_i O_i [q_i + v A_i (1-q_i)].
```

For the fixed-A=.5 arm and every possible visitor condition, q_i >= 0,
so its expected viable offspring per adult is bounded below by

```
r_min = 8 exp[-.5(.625)^2 - .5(.5)^2] (.5)(.5)
      = 1.4518443019048164.
Lambda_t >= r_min N_t.
```

At N=48 this is at least 69.6885 potential viable recruits, with a cap of
48. The one-step probability of zero recruitment at that census is at most
exp(-69.6885)=5.4282e-31. **This one-step number is NOT the 80-step bound**:
small intermediate populations must also be included.

Define a comparison chain starting from Z_0=48:

```
Z_(t+1) = min(48, Poisson(r_min Z_t)).
```

Poisson variables can be coupled monotonically in their mean. Inductively,
N_t >= Z_t, since the native fixed-arm mean is at least r_min N_t and both
use the same upper cap. Consequently,

```
P(native fixed-A extinction by t) <= P(Z_t=0).
```

Zero is absorbing because there is no immigration. For 0<=j<48,
P[n,j]=exp(-nr)(nr)^j/j!, and P[n,48]=P(Poisson(nr)>=48).
Iterating this 49-state probability vector over 80 updates gives the bound
1.6075032057658e-15. Independent 70-digit Decimal recursion checks the
floating-point calculation. Numerical agreement is not a formal interval
arithmetic certificate, but the comparison inequality itself is analytical.
No corresponding survival bound is claimed for arbitrary evolving-A states.
Finite K also means eventual extinction remains possible; r>1 is not immortality.

## A demographic contrast that has not already reached the survival ceiling

The source per-capita no-service output for fixed diagnostic I,A is

```
r(B,I,A)=B (.5) A exp[-.5 I^2-.5 A^2].
```

To put fixed diagnostic A=.5 below replacement and A=.75 above replacement
for EVERY I in the inherited interval, the budget must satisfy

```
exp[.5(.625)^2+.5(.75)^2]/(.5*.75) < B
B < exp[.5(.375)^2+.5(.5)^2]/(.5*.5)

4.2947431563 < B < 4.8627633221.
```

An illustrative B=4.5 (56.25% of the old ovule budget) lies inside this
analytically determined interval. It is a **post-pilot prospective proposal**,
not a retrospectively registered treatment and not a chosen biological SESOI.

| Fixed diagnostic genotype | B=8 potential recruits/adult | B=4.5 potential recruits/adult |
|---|---:|---:|
| A=.5, I in [.375,.625] | 1.4518 to 1.6452 | .8167 to .9254 |
| A=.75, I in [.375,.625] | 1.8627 to 2.1108 | 1.0478 to 1.1873 |

For a 45-update, no-service, fixed-trait comparison chain starting at 48,
the computed B=4.5 survival range is **0.00157 to 0.17020** for A=.5 and
**0.97760 to 0.9999991** for A=.75, across the two endpoint I values.
These are probability integrations for diagnostic genotypes, NOT new
observed histories or a predicted evolving-arm effect. The evolving arm is
not guaranteed to attain A=.75. Bounds on fixed genotypes cannot be copied
to a heterogeneous evolving population without checking its trajectory.

### Why budget is a useful source-native demographic control

At the SAME genotypes, census, visitors and other parameters, B does not
enter pollen affinity, export, receipt or q_i in the source implementation.
Multiplying B by s multiplies all outcross and viable-self entries of the
parentage matrix by s. Therefore its normalized parent-selection
probabilities are unchanged. This isolates a direct change in recruitment
intensity without directly changing relative parental return in that fixed
state. Later census changes can still alter pollen transfer and evolution.
This statement does not apply to a different model where q depends on B.

## Executable next-study scope, without retroactive confirmation

1. Keep the B=8 historical, equal-initial-A comparison as the test of the
   genetic-support clock. Survival here is a descriptive guardrail, not an
   endpoint on which a substantial positive rescue effect can be powered.
2. For a separate prospective companion, retain the preassigned historical
   A policies and clone ALL original histories at a predeclared checkpoint,
   including deaths as failures. Compare unchanged B=8 against the same
   specified budget challenge in both policy arms, with fresh paired
   demographic streams. Never select only high-A survivors. A=0.75 is only
   the analytical diagnostic; do not force it into the evolving arm.
3. Use historical A-policy by demographic-challenge interaction in
   unconditional occupancy as the rescue estimand, alongside the recorded
   inherited support. Keep actual pollinator-return recovery as its own
   calibration: a demographic challenge is not pollinator restoration.
4. The new shock's variance, scientific effect threshold, independent
   founder/visitor counts and resource budget still require #585 review.
   The old B=8 zero-variance survival estimate is invalid for powering this
   new challenge. Do not enlarge or relabel either old pilot as confirmation.

This gives a concrete candidate intervention and a reason for it without
changing the data, forcing a desired observed effect, or claiming that the
complete robustness/recoverability hypothesis has been proved.

## Verification and reproduction

Run:

```
python -m scripts.audit_chapter2_demographic_ceiling_20261018 --out NEW.json
pytest -q tests/test_demographic_ceiling_20261018.py tests/test_audit_equalA_precision.py
```

Six new deterministic tests check the scalar source-derived law, probability
mass, the cap/absorbing state, tiny-path exhaustive enumeration, monotonicity,
an independent 70-digit Decimal evaluation, the resource interval and
fail-closed source assumptions. Together with four existing review tests:
**10 passed locally**. No original biological operator is imported or modified
by this audit. Repo-wide CI and a second native implementation remain distinct
from this local verification; do not infer they passed from these tests.
