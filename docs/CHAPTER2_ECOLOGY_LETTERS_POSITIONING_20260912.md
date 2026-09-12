# Ecology Letters positioning — Lane B v2

Updated: 2026-09-13

## Editorial object

Do **not** center the Letter on the statement that community averaging can reverse a variance ranking. That result is useful, but by itself it is close to an `O(1)` versus `O(1/k)` law-of-large-numbers comparison.

Center the Letter on a stronger statement:

> **Effective independence is a variance-equivalent coordinate in the linearized theory, but it is not generally a sufficient statistic for nonlinear ecological response. Aggregation and synchrony can act on different components of response variance, creating an interaction-dominated intermediate phase that is absent from both the small-system and asymptotic limits.**

The original Chapter 2 pollination model is one nonlinear ecological demonstration. A structurally distinct adaptive consumer-resource response supplies a second nonlinear class. The exact bilinear case supplies the solvable baseline and shows exactly what nonlinear systems are allowed to violate.

The current Oikos Lane A remains a separate, scientifically closed submission object. Lane B does not reopen or delay it.

## 1. Exact baseline: what the bilinear theory really predicts

For centered independent state `X` and pooled community coordinate `Zbar_k`, let

`Y_k = a X + b Zbar_k + c X Zbar_k`

and for exchangeable copies define

`tau_k = sigma^2 [rho + (1-rho)/k]`.

Then the exact two-way variance components are

```text
S_k = a^2 Var(X)
C_k = b^2 tau_k
I_k = c^2 Var(X) tau_k
```

so

`I_k / C_k = c^2 Var(X) / b^2`.

Therefore the exact bilinear theory has two important invariances:

1. `I/C` is independent of both `k` and `rho`;
2. the relative ordering of `C` and `I` can never reverse as `k` or `rho` changes.

A precision correction matters here. Fixed `C/I` ordering does **not** imply only two possible complete rank orders. As `tau_k` decreases, the constant `S` term can cross `I` and `C` separately, so as many as three order regions are possible, e.g. `CIS -> CSI -> SCI`. What is forbidden is a **C-versus-I reversal**.

For a general smooth response, first-order expansion gives

```text
C_k = A_C tau_k + O(tau_k^2)
I_k = A_I tau_k + O(tau_k^2)
```

so `I/C -> A_I/A_C` as `tau_k -> 0`. This is a leading-order asymptotic prediction, not an exact finite-`k` invariance outside the bilinear model.

This gives a useful diagnostic: strong finite-`k` drift in `I/C`, and especially a reversal of the `C` versus `I` ordering, identifies higher-order or nonlinear structure that cannot be represented by the bilinear/first-order reduction alone.

## 2. The Chapter 2 nonlinear model crosses a forbidden C/I boundary

The frozen six-seed active-adjustment result is:

| k | S | C | I | I/C | median order |
|---:|---:|---:|---:|---:|---|
| 1 | 0.026 | 0.730 | 0.247 | 0.34 | CIS |
| 2 | 0.103 | 0.480 | 0.417 | 0.87 | CIS |
| 4 | 0.273 | 0.235 | 0.495 | 2.10 | ISC |
| 8 | 0.425 | 0.183 | 0.401 | 2.19 | SIC |
| 16 | 0.558 | 0.127 | 0.320 | 2.52 | SIC |

The main nonlinear fact is therefore not merely `C -> S` rank crossover. The system passes from `C>I` to `I>C`, and `I` becomes the dominant variance component at an intermediate finite scale.

That `C/I` reversal is impossible in the exact bilinear model and excluded at leading order once the first-order regime is reached. It marks a finite-scale nonlinear phase rather than a restatement of asymptotic averaging.

## 3. A second nonlinear response class reproduces the intermediate interaction phase

To test whether the result is specific to the pollination model, Lane B uses a structurally separate adaptive consumer-resource response:

1. resource traits are drawn from `Beta(2,2)`;
2. a consumer with initial state `X` attacks resources with Gaussian trait-dependent weights;
3. the consumer shifts toward the weighted resource-trait centroid for a fixed number of adaptation steps;
4. final intake follows a Holling-II saturation.

The exploratory structural-generalization audit reports the **entire** 54-setting grid:

- resources per copy: `2, 4`;
- matching width: `0.12, 0.18, 0.25`;
- handling: `1, 2, 4`;
- adaptation rate: `0.05, 0.15, 0.30`;
- `k={1,2,4,8,16}`;
- the existing six-seed ensemble;
- 256 realizations per seed.

Across the resulting 324 setting-by-seed trajectories:

- **255/324** show an interaction-dominated intermediate scale;
- **111/324** reverse the `C` versus `I` ordering;
- **68/324** show the full `C`-dominated small-system -> `I`-dominated intermediate -> `S`-dominated large-system sequence.

At the setting level, an intermediate `I` winner appears in at least four of six seeds for **42/54** settings; `C/I` reversal for **18/54**; and the full `C -> I -> S` winner sequence for **10/54**, including **9/54** in all six seeds.

This is not a universality theorem. It is enough to reject the interpretation that the intermediate interaction phase is a peculiarity of the original pollination parameterization.

## 4. `k_eff` is variance-equivalent, not sufficient

The historical generic note used

`k_eff = k / [1 + (k-1) rho]`

as the scaling coordinate. That is exact for the variance of an exchangeable mean and is sufficient for the exact bilinear variance components because those components depend on the pooled community only through `tau_k`.

The nonlinear claim must be weaker and more precise:

> **`k_eff` is a variance-equivalent coordinate. It is not generally a sufficient statistic for the response decomposition.**

A nonlinear response can depend on properties of the pooled community distribution that are not fixed by its variance: support, higher moments, identity composition, and the geometry on which adaptation or saturation acts.

### Identity-preserving correlation robustness

To ensure that the failure is not an artefact of whole-community clone mixing, the second correlation implementation keeps pollinator identities and trait draws independent among copies. Only arrival/loss event shocks share Gaussian common components.

The realized pairwise correlation of final pollinator counts is then measured directly and converted to a variance-equivalent `k_eff`.

Two comparisons are decisive:

- correlated `k=16` with realized-count `k_eff ~= 3.9` remains `SIC` in **6/6** seeds, whereas frozen independent `k=4` is `ISC`;
- correlated `k=16` with realized-count `k_eff ~= 2.3` remains `SIC` in **6/6** seeds, whereas frozen independent `k=2` is `CIS`.

Thus equal or near-equal variance-equivalent effective independence does not recover the same determinant decomposition.

This directly rules out the strongest historical field-mapping sentence — “effective stochastic independence is the relevant scaling coordinate” — as a general nonlinear claim.

## 5. What `I/C` can and cannot do

`I/C` is valuable because its exact invariance in the bilinear model makes it a clean **departure diagnostic**.

The Chapter 2 model changes from about `0.34` at `k=1` to about `2.52` at `k=16`. The consumer-resource grid also contains broad regions with strong scale dependence in `I/C`.

However, the identity-preserving correlation audit shows that nonlinear `I/C` is **not strictly invariant to correlation implementation**. It is often less responsive to shared-event correlation than the absolute `S/C/I` decomposition, but the current evidence does not justify a confirmatory rule that `I/C` must be rho-invariant.

Therefore:

- use `I/C` in Lane B as a diagnostic of failure of the first-order/bilinear reduction;
- do **not** yet promote “I/C changes with aggregation but not synchrony” to a universal law;
- do **not** add that rho-invariance criterion to Lane C unless a later dedicated theory/audit supports it.

## Revised strongest claim

Preferred:

> **Ecological aggregation and stochastic synchrony cannot generally be collapsed onto a single effective-independence axis. Linearized theory correctly predicts when averaging can reorder persistent state and realization effects, but nonlinear response geometry can decouple community and interaction variance, generating an interaction-dominated intermediate phase that a one-dimensional `k_eff` reduction cannot represent.**

Short form:

> **Effective independence is not a sufficient statistic for nonlinear ecological response.**

## Ecology Letters fit

The target is an **Ecology Letters Letter**, not a Perspective.

The manuscript should be organized as original theory-plus-model research:

1. exact solvable baseline and its invariants;
2. nonlinear violation in the Chapter 2 system;
3. structural replication in adaptive consumer-resource dynamics;
4. failure of variance-equivalent `k_eff` under a second correlation implementation;
5. ecological consequence: aggregation/breadth and synchrony/stability are distinct context axes.

The crossover theorem becomes setup rather than headline.

## Four main figures

### Figure 1 — exact phase structure

Analytic bilinear phase map using `tau_k` (or variance-equivalent `k_eff`) and `c^2 Var(X)/b^2`.

Show:

- exact `I/C` invariance;
- fixed `C/I` ordering;
- the one or two possible S-crossing boundaries;
- correlated-variance floors.

### Figure 2 — nonlinear trajectories break the exact ordering constraint

Overlay:

- Chapter 2 `k` trajectory;
- representative adaptive consumer-resource trajectory;
- the exact-theory constraint that `C/I` ordering cannot flip.

The visual point is the intermediate `I`-dominated region, not the numerical location of any `k` threshold.

### Figure 3 — failure of one-dimensional effective independence

Main panel: `(k, correlation)` order map for the nonlinear system, with variance-equivalent `k_eff` contours.

The critical visual test is whether order and component shares are constant along a `k_eff` contour. They should not be if the reduction fails.

The current identity-preserving event-correlation audit already establishes decisive matched-`k_eff` counterexamples; a dense grid is a figure-completion task rather than a conceptual admission gate.

### Figure 4 — `I/C` as nonlinear-departure diagnostic

Show:

- bilinear exact constant;
- Chapter 2 scale trajectory;
- consumer-resource grid/representative trajectory;
- correlation sensitivity band.

Label `I/C` explicitly as a **diagnostic**, not an invariant of nonlinear ecology.

## Lane C implication — parked, not reopened

Lane C remains paused for resource/governance reasons.

If it is ever reactivated, the Lane B result changes one design principle:

```text
aggregation / support breadth
!=
synchrony / shared stochasticity
```

They must be retained as separate pre-outcome context axes. A single `k_eff`, “broader-and/or-more-stable” score, or any equivalent one-dimensional context modifier should not be preregistered as sufficient.

No current Lane C site registry, permit plan, or Stage-1 design needs to be changed before the resource decision. In particular, do not reopen Lane C now merely to propagate this theoretical consequence.

## Admission status for Lane B

Closed:

- exact bilinear phase identities;
- exact `I/C` invariance in the bilinear case;
- correction that fixed C/I ordering still allows up to three complete rank-order regions;
- Chapter 2 nonlinear `C/I` reversal;
- second nonlinear adaptive consumer-resource class;
- identity-preserving shared-event correlation robustness;
- rejection of `k_eff` as a general sufficient statistic.

Still open before an EL submission:

1. dense `(k, rho)` nonlinear map for Figure 3;
2. final four figures and <5000-word Letter;
3. literature placement of variance-equivalent reductions, ecological synchrony, and nonlinear context dependence;
4. optional empirical magnitude example for natural synchrony, as Discussion support rather than a condition for the theoretical result.
