# Two trait-specific selection thresholds, private/social floral returns, and recoverability

**2026-10-18 — mechanistic synthesis for ONE developing NEE Article, PR #590.** This is an evidence-ranked integration of existing verified source and a set of prospective falsifiers, **not** a new preregistered or confirmatory experiment. It does not modify original Q1–Q4 registered contrasts, signed genomes, Figures, or historical provenance. Old historical Q1–Q4 identifiers remain unchanged; the ONE Article's **three central questions** are onset necessity, recoverability, and assurance's effect on that window.

## Precise candidate mechanism

> Pollinator scarcity changes the individual reproductive returns to floral investment and reproductive assurance through **distinct local selection conditions**, without requiring assurance evolution to initiate floral reduction. Autonomous assurance can directly protect selfed reproductive output, whereas increased floral investment improves the focal mother's outcross pollen receipt, the focal plant's siring success, and potentially **other mothers'** reproduction through pollen export. Private and collective viable-seed returns can consequently favor different floral investments in some states. Assurance may subsequently alter plant persistence, the selection favoring restored investment and the inherited HIGH-I support needed for recovery.

The word **"can"** matters throughout. Different local sign conditions do **not** imply two universally ordered pollen-scarcity breakpoints, two independent ecological axes, a general population optimum, or a general evolutionary no-return point. Both gradients depend on the same current genetic state, visitor composition/activity, mating timing, inbreeding depression and allocation costs. Historical A expression fixed at 0.5 is **not** no selfing.

## Exactly what "two thresholds" means in original Model3

Read-only source: `scripts/model3_island/selection.py` (`syndrome_thresholds`, `investment_invasion_terms`) and unchanged `reproduction.py`. At fixed interior monomorphic resident traits `(M,I,A)`, density at carrying capacity and specified functional visitors, these provide two *cost-threshold surfaces*:

- `beta_A > 0` iff `c_A < c_A_star(state,visitors)`: selection to raise inherited assurance capacity in the rare-mutant local approximation.
- `beta_I < 0` iff `c_I > c_I_star(state,visitors)`: selection to reduce inherited floral investment in the same source approximation.

They are separate sign tests, **not guaranteed distinct time moments** or independently identified thresholds in geographic isolation. If translating them into critical visitor-service levels, each root must be solved under an explicit visitor-composition/exposure path with a fixed reference genotype and checked for root existence, nonmonotonicity, multiple roots and boundaries. The original registered trait-change clocks (51/64 in one delayed/cost setting, 30/64 in prior selfing) are sustained finite-population *event detection*, **not** these local roots.

For delayed selfing only, with pollen-fertilization fraction `q`, maternal outcross `F=Oq`, viable selfed output `S=(1-delta) A O(1-q)`, `O=O0 exp(-c_I I²-c_A A²)`, and `W=F+S` in a monomorphic resident, the source expresses the local investment gradient as:

```text
beta_I = ((1/2 - (1-delta)*A)*O*dq/dI
          + (1/2)*F*(d log exported_pollen/dI)
          - 2*c_I*I*((1/2)*F+S)) / W
```

This includes **focal maternal outcross, focal paternal outcross, displaced viable selfing and cost**. "Focal receipt alone falls below cost" is an incomplete fitness criterion. The local assurance gradient has the selfing gain and (where pollen discount applies) paternal export loss:

```text
beta_A = ((1-delta)*(1-q)
          - (1/2)*pollen_discount*q
          - 2*c_A*A*((1/2)*q+(1-delta)*A*(1-q)))
          / (q+(1-delta)*A*(1-q))
```

The `prior` setting uses different expressions, already handled by the source code. These are local rare-mutant approximations, not a heterozygous finite-population causal decomposition. Existing `scripts/audit_model3_joint_thresholds.py` and `tests/test_model3_syndrome_thresholds.py` independently checked these sign conditions, with source-appropriate caveats.

## Empirical rank of the source model's private/social contrast

**Source-supported, conditional local (not evolutionary population optimum):**

- The frozen finite focal-vs-collective viable-seed derivative synthetic grid has **14/384** resolved `beta_focal < 0, Gamma_seed > 0` cells (362 aligned; 8 inconclusive), zero resolved inverse-direction cells. These are hand-authored contexts, **not 384 independently sampled islands**. Source receipt: `data/results/chapter2_beta_gamma_seed_engineering_receipt_20261010.json`. One delayed-selfing example has beta **-0.06317366954** versus Gamma_seed **+0.15822876051**.
- At the source-equivalent `K=48, B=48` rare-mutant comparison, **6/192** retain `beta_rare < 0, Gamma_seed > 0`, 178 aligned and 8 inconclusive. The rare mutant is not interchangeable with a 1/8 finite focal perturbation. Source receipt: `data/results/chapter2_beta_gamma_rare_limit_receipt_20261010.json`.
- Actual original evolved diploid checkpoint genomes show a **positive nonfocal viable-seed response** to unilateral increased I in **62–63/64 original near visitor histories** (depending on mating rule) in `docs/CHAPTER2_EVOLVED_GENOME_POLLEN_SERVICE_GATE_20261010.md`. Its focal *maternal* sign alone cannot substitute for full `0.5*F+0.5*P+S` genetic contribution, and these are correlated old histories rather than independent new confirmation.

`Gamma_seed` is a derivative of **collective expected viable seed output** when ALL plants' I is changed. It is **not** an optimum for long-term population persistence. Under capacity-saturated recruitment, a local seed advantage need not change future occupancy, and actual evolution to a socially inferior strategy is **not established**. The original delivery-matched control almost removed the seed-output gap when total pollen delivery was held equal, indicating that the observed community effect is mainly an effect of **amount delivered**, not evidence of an additional routing advantage.

**Previously verified, but not proof of the new complete causal chain:**

- Q1: I declines with A expression held at 0.5 and still self-capable. Independently sampled founders support the no-necessity counterexample within the stated model. Assurance-first is 51/64 under one delayed/cost condition, not a universal threshold order (30/64 for prior selfing).
- Q2 genetic support: retrospective source-only HIGH-I founder-mean exclusion in **1,455/2,304** closed, occupied histories, including **1,201/2,048** from eight static visitor-present contexts; these do **not** establish positive high-I selection after restoration or a time before imposed visitor extirpation. Separate eight-history synthetic pilot found one first upper-support closure at `t_G=39`, four updates AFTER its imposed `T_E=35`, while all 8 remained alive.
- Q3 assurance: one registered, pilot-informed demographic stress experiment has pooled assurance-evolvability × historic visitor-replenishment occupancy interaction **+0.1083984375**, but this is not general survival insurance from a naturally evolved A-first lineage. Eight-history recovery pilot gives opposite directional descriptions under unconditional high-I attainment versus post-treatment selected decline/survival denominators; **no identified assurance effect on `t_G` or a probability-defined `t_star`**.

## Fault tolerance versus genetic recoverability (2026-10-18 addendum)

A pollinator *fault* should mean failed effective pollen fertilization, measured as f=1-q; named visitors may still be present. Under delayed selfing, the Model3 expected viable maternal seed production is Y=O[q+(1-delta)A(1-q)]. Comparing the SAME genotype at q=1 and q=0, the proportion retained after complete pollen failure is (1-delta)A. At delta=0.5 and A=0.5 the floor is 0.25 of that plant state's ovule output. This is a normalized **functional failure-buffering** identity, not a new measured fault-tolerance rate or population survival probability. At the SAME genotype, if effective outcross success q varies among years with O and A held constant, Var(Y)=O^2[1-(1-delta)A]^2 Var(q). Insurance attenuates the transmission of pollination variation to expected maternal seed production; this is NOT a proof about long-run geometric population growth, extinction risk, or selection. Tests in `tests/test_chapter2_pollination_failure_buffer_identity_20261018.py` check this algebra and the original native delayed/prior reproductive ledgers without running new ecological histories. Direct resource costs change absolute O and can reverse the A comparison.

Under costless delayed selfing and no pollen discount, the Model3 local assurance gradient is proportional to (1-delta)(1-q), nonnegative, and zero at q=1. Zero is neutrality, **not strict evolutionary irreversibility**: drift and mutation can still change A. Under prior selfing, outcross ovules are preempted; direct A cost lowers O; pollen discount can reduce siring. Any of these may favor a decrease in A when service returns. The original HIGH-I upper-allele bound cannot be copied to A without verifying the A-locus mutation and immigration permissions.

I changes effective pollen acquisition and paternal siring; A buffers female seeds conditional on pollen failure. More assurance dampens maternal incremental benefit of q because d(Y/O)/dq=1-(1-delta)A, but does not necessarily reverse the full genetic investment gradient (which includes pollen export). High-I return requires a favorable full-parentage gradient **and** access to sufficiently high I alleles, followed by successful finite transmission. Retaining those alleles does not guarantee recovery. Test the possible asymmetry **functional reproductive robustness versus evolutionary reconfigurability** under independently assigned founder-by-visitor A policies and separately report occupancy, selection gradient, HIGH-I support clock and restoration success.

The ecological antecedent for resistance/tolerance versus recovery is separate from these new Model3-specific definitions. Kalisz, Vogler & Hanley (2004), doi:10.1038/nature02776, is a precedent for context-dependent autonomous selfing and mixed mating, not an independent validation of Model3's no-return clock.

## Falsification and required future tests: single-paper Q1–Q3

**Q1 / parallel thresholds, not serial necessity.** At fixed inherited reference genotypes, cross functional-pollinator service and mating rule; verify `beta_A` and `beta_I` source analytical signs independently of finite detected-event order. A guaranteed A-first claim is **rejected** if the sign roots reorder, disappear or multiple roots occur; report all paths rather than select favorable ones.

**Q1 / private vs collective return.** For each independently specified visitor/resident/census context, calculate BOTH focal total parental gene-copy derivative `beta_I` and collective viable-seed derivative `Gamma_seed`, plus **separately** a prospective unconditional occupancy/persistence response `Gamma_persist(H)` with a defined low-density regime. A seed-level sign conflict does not imply a persistence conflict. The strong collective-underinvestment claim requires a measured, registered group-level persistence objective AND inherited trait change in the direction of individual selection.

**Q2 / recoverability.** Declare founder-relative `I_star`, no-I-mutation/no-seed-immigration structural support clock `t_G`, restored-visitor positive-return assay, and separately the stochastic time-specific `P(regain I_star within H | alive, already declined)`. `t_G` is a sufficient loss of one target when genetic access closes; no finite-H failure alone establishes permanent evolutionary loss. Exogenous visitor return must pass fixed-genotype expected pollen-transfer and outcrossing efficacy checks before its failure is blamed on plants.

**Q3 / assurance shift.** Assign A-evolvable vs expressed A=0.5 FIXED at the beginning of independently crossed founder × visitor histories; keep the new policy's visitor-loss schedule identical. Preserve the **unconditional** joint survival/high-I attainment per randomized history, in addition to *selected* conditional regaining after decline. Compare upper-I support-loss cumulative incidence with extinction as a **competing event**, rather than treating extinct populations as zero-I or discarding them. A future "freeze A at attained expression" intervention from evolved checkpoint states is distinct from the original historical fixed-A policy, and cannot replace it. No independent effect direction, environmental root count or equal-effect margin is yet registered.

The existing #585 pre-execution two-axis power/provenance gate applies to a separately identified future study; the 2×2 exploratory crossed blocks, 144 nested futures, and 2,304 earlier source cases are not independent additive sample size. Keep all old positive, inconclusive and negative decisions, immutable archives and the active single NEE Article research route.
