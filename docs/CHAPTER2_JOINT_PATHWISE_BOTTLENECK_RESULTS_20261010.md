# Chapter 2: when does finite capacity alter extinction timing? A pathwise synthesis of the entire synthetic grid

**2026-10-10 — SOURCE-LOCKED, post-outcome engineering diagnostic. Not a new ecological confirmation or a reproduction of the #451 A-first/I-first registered effect.**

## Source and verification

- Same original deterministic eight-genotype source, same demographic repeat RNG identities and **exactly the same two hand-authored/static visitor regimes** used in the earlier PR #452 resource grid. No new visitor histories, cohort seeds, mutation, adult survival, seed immigration, field data, or A-first/I-first assigned-expression interventions.
- K = 8 versus 48, pollen-recipient background B = 48, prior selfing, ovule budgets **3, 4.5, 6, 8**, gates baseline / half viable self / half viable outcross.
- Newly audited paths: 24 previously exposed demographic RNG identities per condition, through 80 updates. The occupancy outcome is retained at 40 and 80 and checked against **all 32 original regime × budget × horizon × K** source-locked rows, separately for every gate. The checks passed *exactly*; this is not an independently sampled new cohort.
- Executed code: `scripts/audit_chapter2_joint_pathwise_bottlenecks.py`. Dedicated tests: `tests/test_chapter2_joint_pathwise_bottlenecks.py`. Source commit `ebd5dc936b68cc5d547164313627f621efe53a23`, [CI #38012545640](https://github.com/zuizui0223/izu-core/actions/runs/38012545640), focused tests/execution/upload successful. [Raw JSON and original receipt artifact #11655475278](https://github.com/zuizui0223/izu-core/actions/runs/38012545640/artifacts/11655475278), JSON SHA256 `e1add69f6a09ebb28f22fa960f9b1c994b1f366cf4b404ad20f4affd531b6d43`, ZIP SHA256 `a7509f3d4a83f4ea73f26533db83926d5ac3a294df8dc23fd37185c94c8092b0`.
- Repository-preserved compact receipt: `data/results/chapter2_joint_pathwise_bottlenecks_receipt_20261010.json`, showing all 16 regime × budget × K conditions at 80 updates, their checkpoints 20/40/80, discordant paired paths and low-census encounters.
- Earlier execution failures were **software diagnostics**, not contradictory ecological results: (1) the pilot unit-test's invalid-scope contract was too permissive; corrected to exactly one full archival mode and one small-test mode; (2) full replay matched the original counts but the JSON writer rejected a NumPy integer; converted to a native integer and added whole-output JSON serialization regression. The *successful source* reran both gates without relaxed evidence checks.

## Temporal occupancy is not captured by the 80-year endpoint alone

**Two artificially defined visitors, viable self-seed halved. All counts are survived / 24.**

| Ovule budget | K | At year 20 | At year 40 | At year 80 | Losses in years 21–80 |
|---|---|---:|---:|---:|---:|
| 3 | 8 | 0 | 0 | 0 | 0 (already extinct) |
| 3 | 48 | 0 | 0 | 0 | 0 (already extinct) |
| 4.5 | 8 | 0 | 0 | 0 | 0 (already extinct) |
| 4.5 | 48 | 0 | 0 | 0 | 0 (already extinct) |
| 6 | 8 | 6 | 4 | 1 | 5 |
| 6 | 48 | 8 | 8 | 8 | 0 |
| 8 | 8 | **21** | 17 | **14** | **7** |
| 8 | 48 | **21** | 21 | **21** | **0** |

At budget **8**, K8 and K48 have identical 20-update occupancy (21/24) under the half-self gate, but K8 subsequently loses seven additional paths while K48 loses none. At budget **6**, K8 loses five of six paths still present at 20 updates, whereas K48 keeps its eight. At budgets 3–4.5, both gated arms have reached the empirical occupancy floor by 20 updates, so there is no surviving group available for late divergence.

**Baseline comparison:** with two visitors at budget 8 *without* the half-self gate, all 24 paths at both K values survive every checkpoint; budget 6 baseline is likewise 24/24 at both capacities. Therefore the late-loss signature appears under engineered viability stress and is not an assertion that small K necessarily causes late extinction at all resource conditions.

## Bottleneck warning signal, not evidence of a causal mediator

For the same two-visitor, half-self 80-update paths, the number of 24 repeats experiencing **any live census of 1–2 individuals** before the horizon was:

| Ovule budget | K8 | K48 |
|---|---:|---:|
| 3 | 18 | 18 |
| 4.5 | 22 | 22 |
| 6 | **23** | 18 |
| 8 | **13** | **4** |

The corresponding budget-8 baselines both had **0/24** such low-census encounters; at budget 6 baseline they had 2/24 (K8) and 0/24 (K48).

This is compatible with repeated small-census exposure contributing to later extinction risk, but a low census may be an *effect of* declining reproduction or impending extinction, not an independently manipulated cause. We do **not** compute an artificial causal mediation proportion or conclude that genetic drift rather than population regulation, genotype composition or viability deficit produced the late losses. Some first extinction times occur before any late checkpoint.

## Negative controls and nonuniform capacity interaction

- With **zero visitors**, the self-halving effect persists: at budget 8, half-self K8 occupancy goes **17 → 14 → 14** from years 20/40/80; K48 goes **19 → 17 → 17**. It is inappropriate to attribute the entire half-self sensitivity to visitor substitution.
- In zero-visitor conditions **half-outcross and baseline have exactly identical paths**, not just equal pooled survivor counts. This is a strict negative control because there is no successful outcross-seed channel to alter.
- Under the two-visitor artificial regime the **descriptive K8-minus-K48 difference in baseline-minus-halfself occupancy sensitivity** changes with budget: `−4/24, −6/24, +7/24, +7/24` at 3, 4.5, 6, 8 ovules respectively (80 updates). This is neither a preregistered effect-size trend nor a universal threshold law: floors, ceilings, finite demography and survivor conditioning all move with budget.
- The **half-outcross** gate can show individual demographic paths with the opposite survival label under shared RNG streams, such as the budget-4.5 K8 two-visitor context. Do not promote pathwise discordance to evidence that outcrossed offspring are harmful; nonlinear stochastic trajectories are not pairwise monotone by construction.

## What this changes, and what it does not

The current synthetic mechanism result is more specific than the older assertion that K merely "changes persistence": **in the higher-budget self-viability-stressed regimes, capacity changes whether early survivors remain occupied through a second, later demographic interval.** This is a source-reproducible statement about *when* stochastic paths disappear, not a claim about an isolated temporally causal viability intervention.

This does **not** contradict #448's independent preregistered **inconclusive** early-versus-late timing primary, because that test randomized the temporal location of the seed-viability reduction and examined a K interaction on *A-first versus I-first* assignment differences. Here the viability reduction is full-period and **there is no A/I manipulation at all**.

Likewise, #420's expected source genetic transmission direction and #411's floral-investment evolution cannot be treated as an identified genetic mediation chain into these endpoint occupancies. Genotypes are tracked only among real survivors; extinct trait frequencies remain undefined. Follow-up priorities, if later preregistered, are to separate an unconditional population genetic trait *mass* outcome from survivor-only allele means and to contrast parental-genotype-state effects with demographic regulation under independently generated visitor histories. That experiment is **not** performed here.

**Inference unit:** at most 24 demographic paths within *one* deterministic ecology per visitor regime. There are **zero independent ecological history draws** and zero natural island populations. All claims of cross-island generality, universal fitness benefit, confirmed adaptation and complete SDE/SPDE approximation remain blocked.
