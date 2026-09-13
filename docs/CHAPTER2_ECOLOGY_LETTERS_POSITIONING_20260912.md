# Ecology Letters positioning — Lane B v3

Updated: 2026-09-13

## Editorial object

Do **not** center the Letter on the fact that community averaging can reverse a variance ranking. That result is useful setup, but by itself is close to an `O(1)` versus `O(1/k)` law-of-large-numbers comparison.

Center the Letter on:

> **Effective independence is a variance-equivalent coordinate in the linearized theory, but it is not generally a sufficient statistic for nonlinear ecological response. Aggregation and synchrony can alter different components of response variance, so nonlinear systems can enter an interaction-dominated intermediate phase that a one-dimensional `k_eff` reduction cannot represent.**

The Chapter 2 pollination model is one nonlinear ecological demonstration. A structurally distinct adaptive consumer-resource response supplies a second nonlinear class. The exact bilinear case is the solvable baseline. Lane A/Oikos remains a separate, scientifically closed submission object and Lane C remains paused.

## 1. Exact baseline and the actual invariant

For centered independent state `X` and pooled community coordinate `Zbar_k`,

`Y_k = a X + b Zbar_k + c X Zbar_k`

and, for exchangeable copies,

`tau_k = sigma^2 [rho + (1-rho)/k]`.

The exact variance components are

```text
S_k = a^2 Var(X)
C_k = b^2 tau_k
I_k = c^2 Var(X) tau_k
```

so

`I_k/C_k = c^2 Var(X)/b^2`.

Therefore the bilinear model fixes the **relative C/I ordering** for every `k` and `rho`. It does not limit the full system to only two rank orders: the constant `S` component can cross `I` and `C` separately, so three complete orders are possible. The forbidden event is a **C-versus-I reversal**.

For a general smooth response, first-order expansion gives

```text
C_k = A_C tau_k + O(tau_k^2)
I_k = A_I tau_k + O(tau_k^2)
```

so `I/C -> A_I/A_C` only asymptotically. Strong finite-scale `I/C` drift, especially C/I reversal, diagnoses structure outside the bilinear/first-order reduction.

## 2. Chapter 2 violates the exact C/I constraint

Frozen six-seed active-adjustment medians:

| k | S | C | I | I/C | order |
|---:|---:|---:|---:|---:|---|
| 1 | 0.026 | 0.730 | 0.247 | 0.34 | CIS |
| 2 | 0.103 | 0.480 | 0.417 | 0.87 | CIS |
| 4 | 0.273 | 0.235 | 0.495 | 2.10 | ISC |
| 8 | 0.425 | 0.183 | 0.401 | 2.19 | SIC |
| 16 | 0.558 | 0.127 | 0.320 | 2.52 | SIC |

The important nonlinear result is not merely that S overtakes C. The system changes from `C>I` to `I>C`, and I is the largest component at intermediate `k=4`. That is impossible in the exact bilinear model. The numerical `k=4` location is model-specific and is not a natural threshold.

## 3. The intermediate interaction phase is not pollination-specific

The second nonlinear class is an adaptive consumer-resource response:

1. resource traits are drawn from `Beta(2,2)`;
2. attack is Gaussian in consumer-resource trait mismatch;
3. the consumer adapts toward the weighted resource centroid;
4. final intake is Holling-II saturated.

The full exploratory structural-generalization grid contains 54 parameter settings × the six pre-existing seeds = 324 setting-seed trajectories.

Results:

- interaction-dominated intermediate scale: **255/324**;
- C/I ordering reversal: **111/324**;
- full C-dominated → I-dominated → S-dominated sequence: **68/324**;
- intermediate I winner in at least 4/6 seeds: **42/54** settings;
- C/I reversal in at least 4/6 seeds: **18/54**;
- full C→I→S in at least 4/6 seeds: **10/54**, including **9/54** in all six seeds.

This is a post-hoc structural generalization, not a universality theorem, but it rejects the interpretation that the intermediate phase is unique to one pollination parameterization.

## 4. Why `k_eff` fails: variance equivalence does not fix support

The historical reduction is

`k_eff = k / [1 + (k-1) rho]`.

This is exact for the variance of an exchangeable mean. It is sufficient for the bilinear components because those components see the pooled community only through `tau_k`.

For the nonlinear phase-map audit, correlation is constructed by a trajectory-level common-clone mixture. Each copy uses a shared trajectory with probability

`q = sqrt(rho)`

and otherwise an independent trajectory from the same marginal distribution. Hence pairwise copy correlation is exactly `q^2 = rho` for any scalar copy-level statistic.

But the expected number of **distinct trajectory supports** is

`D(k,rho) = k(1-sqrt(rho)) + 1 - (1-sqrt(rho))^k`

for `rho>0` (and `D=k` at `rho=0`).

Thus equal `k_eff` fixes variance equivalence but not the support presented to a nonlinear response operator.

### Exact same-`k_eff=2` contour

The Figure 3 audit uses 48 realizations per seed and the same six-seed ensemble. Along the exact same `k_eff=2` contour:

```text
(k,rho) = (2,0) -> (4,1/3) -> (8,3/7) -> (16,7/15)
order   =   CIS  ->   ICS   ->   ICS   ->    ICS
E[D]    =  2.00  ->  2.66   ->  3.76   ->   6.07
```

The variance-equivalent coordinate is identical, but determinant order changes because support changes.

This is the direct counterexample needed for the Letter: **same `k_eff` does not imply the same nonlinear determinant decomposition.**

### A contour that does preserve order

Along `k_eff=4`:

```text
(k,rho) = (4,0) -> (8,1/7) -> (16,0.2)
order   =   ISC  ->   ISC   ->   ISC
```

This is important. The claim is not that `k_eff` always fails. The claim is that it is **not sufficient**: one counterexample contour is enough to reject sufficiency, while other contours may preserve the reduction.

## 5. Correlation-implementation robustness

Whole-trajectory clone mixing is not the only correlation model.

A second implementation keeps pollinator identities and trait draws independent among copies and correlates only arrival/loss event shocks through Gaussian common components. Realized final-count correlation is measured directly before computing variance-equivalent `k_eff`.

Two frozen comparisons remain decisive:

- correlated `k=16`, realized-count `k_eff≈3.9` → `SIC` in **6/6** seeds, whereas independent `k=4` is `ISC`;
- correlated `k=16`, realized-count `k_eff≈2.3` → `SIC` in **6/6** seeds, whereas independent `k=2` is `CIS`.

So the one-dimensional reduction failure is not dependent on whole-community cloning.

## 6. Role of `I/C`

`I/C` is an exact invariant of the bilinear model and therefore a useful **departure diagnostic**.

It is not a universal invariant of nonlinear ecology. Under identity-preserving shared-event correlation it changes with correlation as well as aggregation. Therefore:

- use `I/C` to show departure from the first-order/bilinear reduction;
- do not claim that nonlinear `I/C` is rho-invariant;
- do not add rho-invariance as a confirmatory criterion to Lane C.

## Revised strongest claim

> **Ecological aggregation and stochastic synchrony cannot generally be collapsed onto a single effective-independence axis. Linearized theory correctly predicts variance-equivalent averaging, but nonlinear response geometry can distinguish systems with the same `k_eff` because aggregation changes the support on which the response operator acts. This creates interaction-dominated intermediate phases and determinant orders that a one-dimensional reduction cannot represent.**

Short form:

> **Effective independence is not a sufficient statistic for nonlinear ecological response.**

## Four main figures

### Figure 1 — exact solvable baseline
Bilinear phase structure, exact `I/C` invariance, C/I ordering constraint, S-crossing boundaries, and correlated variance floors.

### Figure 2 — nonlinear trajectories cross the forbidden C/I boundary
Chapter 2 trajectory plus a representative adaptive consumer-resource trajectory.

### Figure 3 — same variance-equivalent independence, different nonlinear phase
`(k,rho)` determinant-order map with `k_eff` contours. Highlight the exact `k_eff=2` contour where order changes `CIS -> ICS` while expected distinct trajectory support increases `2.00 -> 6.07`.

This figure is now a completed analysis object, not an admission gate.

### Figure 4 — `I/C` as reduction-departure diagnostic
Bilinear constant, Chapter 2 scale trajectory, consumer-resource trajectory/grid, and correlation-sensitivity band. Label `I/C` as a diagnostic, not a nonlinear invariant.

## Lane C implication — parked

Lane C remains paused for resource/governance reasons.

If reactivated later, retain at least two separate pre-outcome axes:

```text
aggregation / support breadth
!=
synchrony / shared stochasticity
```

Do not preregister a single `k_eff` or “broader-and/or-more-stable” scalar as sufficient. Do not reopen the site registry or permit work now.

## Admission status for Lane B

Closed:

- exact bilinear identities and C/I invariant;
- correction that fixed C/I ordering still permits up to three complete rank orders;
- Chapter 2 nonlinear C/I reversal;
- second nonlinear adaptive consumer-resource class;
- identity-preserving shared-event correlation robustness;
- dense `(k,rho)` Figure 3 phase map;
- exact same-`k_eff=2` order-changing counterexample;
- analytic support mechanism for why variance equivalence can fail.

Still open before an Ecology Letters submission:

1. Figures 1, 2 and 4 rendered in final publication form;
2. <5000-word Letter and <150-word abstract;
3. literature placement for variance-equivalent reductions, ecological synchrony and nonlinear context dependence;
4. empirical synchrony magnitude example in Discussion, with no numerical mapping from field synchrony metrics to theoretical `rho`.

Lane A must be submitted independently; Lane B work does not reopen or delay it.
