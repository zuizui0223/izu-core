# Chapter 2 next question: when does individual reproductive selection diverge from population persistence?

**Design status — 2026-10-10: PROPOSED, not prospectively registered, no outcomes produced.** This is the umbrella scientific question for the post-#411 theoretical program, not a retroactive claim from #420, #451 or #452.

> Predict the boundary between alignment and mismatch of individual reproductive selection and population persistence from maternal-outcross, paternal-outcross and viable-self transmission, then falsify that prediction in finite-population evolutionary trajectories.

## 1. Separate the three axes before fitting

For a *rare individual* mutant trait value `z_m` in a held-fixed resident pollen/recipient environment:
```
W_mutant = 0.5 F_mutant + 0.5 P_mutant + S_mutant
beta_z = d log(W_mutant) / d z_m | z_m = resident z
```
Use existing canonical `scripts/model3_island/selection.py` and `scripts/audit_model3_joint_syndrome_vector.py`. Each `beta` is a local invasion gradient, **not** a finite-population allelic selection coefficient or a realized change in mean phenotype. Record signed `beta_F`, `beta_P`, `beta_S` contributions by differentiating the corresponding terms in W, including normalization and fixed resident competition; positive shares must not be treated as independent causal effects.

At the *population level*, define two different group-level targets:
```
Gamma_seed,z = d log(E[sum_over_residents(F_i + S_i)]) / d z
               under a simultaneous group-trait expression shift
Gamma_persist,z(H) = d P(N_H > 0 | do(group trait z)) / d z
                     at specified horizon H and explicit subsequent evolution policy
```
The first is a viable-seed-production response, not a lifetime population fitness estimate. `Gamma_persist` is an intervention contrast in **absolute unconditional persistence probability**, never a survivor-only mean trait. The collective trait operation must be fixed: imposed expression versus inherited allele change must not be interchanged. Prespecify positive perturbation direction, finite-difference step, endpoints, uncertainty intervals, biologically relevant deadbands, and boundaries. For K manipulations, hold pollen dilution background **B** independently fixed.

The exact identity `sum_i paternal outcross = sum_i maternal outcross` applies to each complete, conserved outcross-parentage ledger. **Paternal competition is zero-sum only conditional on a fixed total number of viable outcross offspring**; altered attraction can also change that total. A favorable `P` component is therefore a hypothesis for conflict, not an algebraic proof of group harm. Likewise prior selfing can displace outcross ovules but costs/depression and genetic contribution must be counted rather than assumed.

## 2. Predictions fixed before any relevant new outcomes

For every declared trait, visitor history, reproductive setting and K/B cell, classify only when *both* signed effects are resolved relative to predeclared near-zero regions:

| Rare-mutant beta | Group-persistence Gamma | Registered qualitative outcome |
|---|---|---|
| + | + | aligned increasing trait |
| - | - | aligned decreasing trait |
| + | - | individual-favored, population-harming **discordance candidate** |
| - | + | group-favored, individual-selected-against **discordance candidate** |
| uncertain/equivalent | any or uncertain | **inconclusive**, never retroactively assigned a quadrant |

Also draw a **separate beta × Gamma_seed map**, not just beta × Gamma_persist. The two group targets may disagree; classify and report that difference rather than pooling them.

Working mechanistic predictions to make falsifiable:
- **H1, reproductive increment:** where the mutant fitness slope is dominated by additional *viable* seed production via maternal increase or delayed-self ovule filling, the beta/Gamma_seed signs are more often aligned.
- **H2, redistribution/competitive loss:** in cells where paternal siring *share* increases with approximately unchanged group outcross totals, or prior selfing displaces viable outcross offspring, beta/Gamma_seed discordance occurs more often than matched incremental-seed cells. Reject H2 if sham-matched effects fail the anticipated interaction; do not use a universal paternal-zero-sum premise.
- **H3, demography:** the beta/Gamma_persist relation depends on K, seed budget, inbreeding depression and evaluation horizon even when beta/Gamma_seed align. Predeclare a null or weak-effect outcome as admissible.
- **H4, evolutionary mechanism (distinct from static intervention):** a cell labeled individually favorable but population-harming in the static map yields **lower unconditional persistence under trait evolution than under an otherwise matched trait-freeze intervention**, with a directionally appropriate realized trait change. This stronger criterion is needed for an evolutionary-suicide claim.

Outcome-neutral failures: static beta and Gamma have same sign everywhere; component label fails to predict any discordance above an environment-only baseline; apparent conflict disappears when matched pollen totals or complete F/P/S ledger are used; short-horizon signs are not robust; evolution-enabled trajectories do not differ from trait-frozen controls; or early lineage extinction makes the necessary trait trajectories unobservable. All remain reportable.

## 3. State-transplant experiment: useful, but not a full genetic causal decomposition by itself

The exposed engineering cohort had at update20, ovule-budget8, full-period half-self, **21/24 alive in both K8 and K48**. This equal **marginal** number of survivors **does not imply** the same demographic paths survived, equal genetic composition, equal population census, or absence of selection bias from conditioning on survival. Record intersection of matched alive path IDs and the complete pre-exposure denominators. Any transplant at update20 estimates a **conditional post-survival intervention** over a declared donor selection rule, not the original time0 population-level K effect.

Freeze and validate:
1. Obtain complete K8- and K48-source **joint three-locus diploid individual genotype arrays** from each admissible real surviving parent state. Do not infer genotypes from means or factorize loci. Allele origins, mutation flags and within-individual linkage must be preserved or explicitly reset with documented artificial ancestry.
2. For each donor genetic source G in {evolved-under-K8, evolved-under-K48}, choose a common **recipient census N0** independent of source K, e.g. N0=8 where source has adequate support. At fixed N0 randomly resample **whole joint genotypes**, not separate trait alleles. Reconstruct unique individual IDs; do not reuse duplicate IDs or invent genetic variants. Record the resampling RNG as a separate source of uncertainty.
3. Cross donor G with target K in {8,48} at fixed B=48, same calendar/visitor snapshot, gate and independent *future* demographic RNG histories. Thus four cells (G8,K8), (G48,K8), (G8,K48), (G48,K48) have equal **starting N0** and comparable external environments. A separate N0 factorial is needed to distinguish initial census size from later carrying-capacity regulation.
4. Report `Y(G,K,N0)` = **unconditional** persistence to update80 after transplant among all experimentally admitted recipients. Matched common RNG is variance reduction, not a guarantee that single trajectories are monotone. Direct donor-group contrasts estimate an intervention on the *observed joint genotype distribution* of selected survivors; they are not the causal effect of one locus or of past drift alone.
5. Define `genetic-source main contrast = [(Y(G48,K8)-Y(G8,K8))+(Y(G48,K48)-Y(G8,K48))]/2` and `capacity main contrast = [(Y(G8,K48)-Y(G8,K8))+(Y(G48,K48)-Y(G48,K8))]/2` for **balanced two-factor averaging**. Report a **separate** `G × K difference-in-differences`. The two averaged contrasts sum to the across-corner contrast, so **do not add a second 'interaction residual' to them**. Two-order Shapley allocation divides interaction dependence between factors; it does not uniquely identify ecological mechanisms.

## 4. Two essential dynamic controls are different interventions

- **Joint-genotype composition clamp:** a naive independent redraw of N genotypes from the fixed donor distribution every generation *introduces new finite sampling variance* and alters the inheritance process. It is NOT a no-drift control. A clamp must specify whether it fixes exact genotype counts, deterministic probability weights, or only expected moments; exact target fractions may be impossible with N<=8, particularly after a changing census. Require integerization diagnostics and sham-resampling controls. If no unbiased integer-preserving clamp can be implemented without changing the source biological kernel, mark this arm **NOT IDENTIFIED**, not 'pure demographic stochasticity'.
- **Within-population homogenization:** setting all three diploid allele pairs to each population's trait means collapses variation and changes Mendelian support, genotype covariance and potentially fitness (nonlinear). This is deliberately *different* biology. It can test a variance/heterogeneity hypothesis with matched sham, but cannot isolate drift or guarantee maintained group mean after replacement.

The strongest causal test of continuing genetic contribution is a **source-matched independently randomized post-update20 genotype-law intervention** compared at the same census and K, backed by controls tracking how the changed genetic operator alters both mean seed recruitment and genetic variance. No one clamp makes the remaining K effect automatically 'purely demographic'.

## 5. Model scope and prospective statistical lock required

**Model 3 in this frozen experiment has fixed inbreeding depression delta, zero mutation, and only three inherited trait loci (matching/access, floral investment, reproductive assurance).** It contains no accumulated deleterious mutational load, purging or mutation-driven meltdown. Loss of assurance alleles, changes at matching/investment loci and finite-locus segregation variance are the relevant genetic channels; claims about natural small-island genetic load are excluded.

A future main experiment must seal, *before* generating new data: full factorial cells, common visitor-history generator, **new previously unexposed independent ecological history IDs** (64 is only a planning candidate, not an established powered N), independent source genotypes, founder selection and transplant rules, time20 survival/conditioning protocol, all replacement-clamp sham operations, fixed K/B and a bounded multi-budget averaging policy including floors/ceilings, meaningful thresholds/ROPE, multiplicity policy, entire-visitor-history bootstrap or hierarchical interval, power under both null and alternatives, and raw-source/reproducibility archive. Do not promote outcomes from one hand-authored visitor regime or the prior 24-path engineering grid to formal confirmation.

**Submission condition:** demonstrate independently that F/P/S decomposition predicts where beta × Gamma_persist conflicts, and that an *evolution-enabled* arm relative to a properly matched freeze arm tests the predicted direction of **unconditional** persistence. Only then discuss evolutionary rescue/suicide; absent an empirical calibration, any positive finding remains model-conditional and not a natural Izu Islands conclusion.

## Relation to existing papers

Keep #411's preregistered four-setting floral-investment conclusion unchanged; keep #451's one supported K-at-B48 **assigned expression-order** primary distinct; treat #420 as a source-operator finite genetics audit and #452 as current mechanism-engineering bridge. This proposed higher-order question supplies a new, independently testable research program, **not a new result retroactively obtained in those PRs**.
