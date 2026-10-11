# Chapter 2 joint genetics–persistence: full post-outcome resource × horizon engineering grid

**2026-10-10.** This is a **post-outcome engineering diagnostic**, NOT a prospective test of PR #420's natural adaptive claim or PR #451's A-first/I-first expression-order hypothesis.

## Provenance and exact execution

The previous 80-update, 3-ovule, source-matched synthetic pilot had 0/48 occupied paths at K8 in every gate. Rather than select only conditions exhibiting an effect, we **committed the entire coarse grid before running any of its grid outcomes** in `data/design/chapter2_joint_multigen_occupancy_surface_20261010.json`: ovule budgets **3, 4.5, 6, 8** crossed with horizons **40, 80**, all K8/K48, gate and visitor-regime cells, 24 demographic replicates each. This design was motivated by and hence **post-outcome** relative to the first budget3 result.

- Full source SHA: `fe3dcd23855f8dc560f9fa4dd630e3efec178114`.
- Actions [CI #38011897964](https://github.com/zuizui0223/izu-core/actions/runs/38011897964): focused unit tests **PASS**, full-grid execution **PASS**, artifact-upload **PASS**. Full suite was separate and not a condition for the already archived grid result.
- [Original artifact ID 11653541956](https://github.com/zuizui0223/izu-core/actions/runs/38011897964/artifacts/11653541956): raw `chapter2-joint-budget-surface.json`, 9,338 bytes, SHA256 `9321185840a6d0ae2b52044b78b499fa97bca5c627765f92c130586520b2fbfc`; original ZIP SHA256 `e1627dff144b5c581ebd56f9bbbd10e443df87a1dee23b02ce25f5e85476a108`.
- Complete machine-retrieved compact result (32 regime/K/budget/horizon rows): `data/results/chapter2_joint_multigen_budget_surface_receipt_20261010.json`.
- Single deterministic eight-genotype founder state, no mutation, no immigration, no adult survival. Identical source genotypes, identical demographic RNG replicate identities, fixed pollen background B48. Two synthetic static visitor regimes (two artificial visitor traits vs zero visitors). **No independently generated ecological visitor history** and no field data. There is NO A-first/I-first expression schedule and no dynamic mutation-order manipulation.

## 80-update occupancy across the full resource budget

Results are **occupied paths out of 24**, with the complete 40-update and visitor-free controls preserved in the source receipt.

| Budget | Two visitors K8 baseline | K8 half-self | Two visitors K48 baseline | K48 half-self | K8 half-outcross | K48 half-outcross |
|---|---:|---:|---:|---:|---:|---:|
| 3 | 0 | 0 | 4 | 0 | 0 | 4 |
| 4.5 | 17 | 0 | 23 | 0 | 20 | 22 |
| 6 | 24 | 1 | 24 | 8 | 23 | 24 |
| 8 | 24 | 14 | 24 | 21 | 24 | 24 |

**No-visitor matched control at 80 updates** (baseline / half-self / half-outcross):
- Budget 3: K8 0/0/0; K48 0/0/0.
- Budget 4.5: K8 17/0/17; K48 19/0/19.
- Budget 6: K8 24/0/24; K48 24/0/24.
- Budget 8: K8 24/14/24; K48 24/17/24.

At 40 updates, the transition is similarly broad: budget3 K8 0/24 under baseline, budget4.5 20/24, budget6 24/24 and budget8 24/24 in two-visitor conditions. All half-self outcomes and full no-visitor negative controls are preserved in the source receipt. The no-visitor outcross gate is analytically inactive and matched baseline outcomes coincide across the grid.

## Interpretable result and why it is NOT a new confirmation

**Result:** Finite-horizon population persistence displays a **strong resource-dependent nonlinear transition** in this highly constrained synthetic Model3 setting. At budget3, the small-K baseline is at an empirical extinction floor. At budget6–8, baseline occupancy reaches an empirical ceiling (24/24). Halving viable selfed seed shifts the occupancy window strongly even when visitors are absent; halving outcrossed viable seeds has little effect in the specific visitor regime chosen here.

The **descriptive K8 minus K48** *selfed-seed gate sensitivity* under two visitors can even change sign with budget, at 80 updates:
- Budget3: (0−0)−(4−0) = **−4/24**.
- Budget4.5: (17−0)−(23−0) = **−6/24**.
- Budget6: (24−1)−(24−8) = **+7/24**.
- Budget8: (24−14)−(24−21) = **+7/24**.

**Interpretation:** A capacity-dependent survival contrast is not a fixed inherent property of the words “selfing assurance”; its magnitude and even descriptive direction in this synthetic system depend on resource supply and whether both K arms lie near survival floors/ceilings. That is consistent with distinct genetic transmission, seed-viability and demographic bottlenecks. It does **not** show a causal reversal of *evolutionary selection*, prove a universal survival threshold, or refute the independently registered #451 K interaction.

**Why not equivalent to #451:** #451's registered estimand is `[D(K8,baseline)−D(K8,half_self)]−[D(K48,baseline)−D(K48,half_self)]` with `D(K,g)=P(occupied | A-first,K,g)−P(occupied | I-first,K,g)`, averaged across original predeclared resource/visitor/reproductive settings. This engineering grid lacks A/I assignments and computes instead absolute untreated-minus-gate occupancy at each K. It therefore **cannot reproduce, disconfirm or pool with** #451's +0.0077457 controlled interaction.

**Statistics:** Twenty-four demographic paths under a single unchanging synthetic visitor condition are Monte Carlo realizations, NOT independent environmental histories or independent islands. A 0/24 or 24/24 result is a finite sample observation, not a true probability of 0 or 1. Condition-dependent Monte Carlo uncertainty and the post-outcome design prohibit general ecological claims.

## Implications for the common #420/#451 theory

The earlier first-generation expectation showed an assurance-high source transmission direction above zero (e.g. +0.0431 in the two-visitor budget3 baseline), although all 48 budget3 K8 paths were extinct at 80 updates. This is a valid **non-equivalence of different mathematical observables**, not causal evidence that increasing genetic assurance causes population extinction.

The new full grid now resolves the immediate engineering barrier: **nondegenerate baseline survival conditions exist (budget4.5) and a nondegenerate half-self survival condition exists (budget8) in the same model**. However, no single budget offers broad mid-range occupancy for *every* gate/K arm, and selecting only favorable contrasts after this grid would be outcome selection. A prospective test must therefore freeze a bounded multi-budget estimand and whole-visitor-history independent sample before any new outcomes, including an explicit A/I arm if direct PR #451 transfer is desired.

## Repository decision

Keep #411 as the independent four-setting floral-evolution main result, #451 as a bounded demographic companion with one registered supported primary, #420 as exploratory finite-genetic source accounting, and #452 as a distinct **mechanistic engineering bridge**. Retain all negative/floor/ceiling cells in the record. Do not merge the source-matched engineering findings into an untested cross-level causal mediation narrative.
