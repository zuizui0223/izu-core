# Source-matched genetic transmission and occupancy — exact one-step engineering preflight

**Date:** 2026-10-10. **Status:** executable source restricted *engineering* (synthetic fixture), NOT a new preregistered biological test or a multiple-generation result.

## Why this follows #420 and #451

PR #420 establishes the exact finite-Mendelian accounting of source parent-state expected allele directions, including viable self, outcross father and outcross mother channels, under a restricted no-mutation finite reproduction kernel. PR #451 summarizes a *different* eighty-update, fixed-B capacity experiment, with an independent registered K interaction under an experimentally imposed A-first versus I-first expression schedule. Both analyses are conditional on one model family, but their environmental histories, genetic settings, time horizons and inference targets differ. It is invalid to equate either #420's allele-direction term or #451's expression schedule with population-level natural fitness.

The first bridge step is to ask **what can be established rigorously without simulating any new visitor history or any future population trajectory?**

## Implemented exact test

`scripts/audit_chapter2_joint_one_step_genetics_occupancy.py` uses the EXISTING, unmodified canonical `PlantState`, `Ledger`, complete diploid allele array, and Chapter2's existing `reproduce_kb` and `gate_postzygotic_seed_viability`. It constructs one deterministic 8-founder fixture from the existing seed-controlled founder generator, with **two hand-authored visitor functional phenotypes, not old or new archived visitor histories**. The restricted biological setting is `prior_selfing`, 8 ovules, zero adult survival, zero mutation, zero immigration.

The factorial engineering cells are:

- Same exact initial 8 genotypes and same two visitor phenotypes in all arms.
- K=8 or K=48, with pollen-background denominator fixed at B=48.
- Viable seed multipliers baseline (self=1, outcross=1); half-self (0.5,1); half-outcross (1,0.5).

For each source state and gate, `ledger.outcross[father,mother]` plus `ledger.self_viable[parent]` gives the canonical parent-pair weights `w`. The unconditional Poisson intensity is `lambda=sum(weights)`; after population-cap truncation, `N=min(Poisson(lambda),K)`. For no surviving adults and no seed immigration, `P(N=0)=exp(-lambda)` **exactly for either positive K**.

At a surviving next generation, the Mendelian diploid trait mean is

```text
mu_child = sum_{father,mother} w_fm * (b_f+b_m)/2 / lambda
         = source_viable_self / lambda * self_dosage
           + outcross_father / lambda * father_dosage / 2
           + outcross_mother / lambda * mother_dosage / 2
```

where the three terms are weighted sums over source genotype-allele dosage, not a selection coefficient. This is checked separately for all three original matching, investment and assurance loci. The offspring covariance includes **between parental-pair and within-pair independent Mendelian segregation**. Conditioning on occupancy gives

```text
Cov(mean allele dosage | N>0, C, visitors)
= Cov(one offspring dosage | C, visitors)
  * E[1/N | N>0, C, visitors, K]
```

These equalities require exact restricted, independent offspring parent sampling, original Mendelian inheritance, and zero mutation/adult survival/immigration; they are not an SDE/SPDE approximation.

## Structural prediction and diagnostic interpretation

**At t+1, same source state and B implies K8 and K48 must have exactly the same** (i) reproductive ledger, (ii) total viable seed intensity, (iii) immediate occupancy probability and (iv) *conditional expected* offspring allele frequencies, even under the viability gates. **They can differ** in expected realized census and the *conditional variance* of the finite offspring allele mean, since `min(Poisson(lambda),K)` differs.

This is a mechanistically informative **structural null**: any fixed-B K moderation of assigned-order persistence after eighty updates cannot be explained by a direct first-generation K effect on pollen receipt or one-off extinction probability from the same parents. It must involve a later demographic-state path, or a different experimental estimand. It does **not** say which later path was causal or when the actual intervention matters. It does not overwrite the independently inconclusive early-vs-late timing primary (#448).

Likewise, lowering viable-self versus viable-outcross seed weights can simultaneously change immediate extinction intensity and conditional expected gene transmission. Those are distinct outputs with no guarantee that their signs mean the same biological benefit; this preflight does NOT establish a real transmission-persistence mismatch.

## Fail-closed and reproducibility boundaries

- `tests/test_chapter2_joint_one_step_genetics_occupancy.py` checks K invariances, exact three-channel reconstruction, fixed original pollen/prezygotic ledger fields, population-cap and covariance ordering, extinction nulls, and rejection of unsupported mutation/survival/immigration.
- `data/design/chapter2_joint_genetic_occupancy_bridge_preflight_20261010.json` names the synthetic fixture, source conditions, engineering nulls, and a **separate blocked, unregistered multigeneration proposal**.
- Run `python -m scripts.audit_chapter2_joint_one_step_genetics_occupancy` for a **deterministic fixture-only diagnostic**; use `--out FILE` if a local machine-readable receipt is needed. Importing or testing does not access archived visitor histories and does not trigger any prospective cohort.
- There is no direct import from the **unmerged** #420 source branch into current `main`; the exact restricted moment algebra is independently implemented against currently merged canonical modules. Reconcile with #420 after review, not through a silent cherry-pick of the whole PR.
- This preflight runs **zero** 80-update synthetic visitor trajectories; cannot identify natural mutation order, natural fitness, causal mediation, island area, geographic INLA or SDE/SPDE validity.
- All future confirmatory seeds, effective sample sizes, bootstrap thresholds and archive/publication routes **remain unspecified and blocked** until an independently frozen power-and-design decision. Never reuse previously exposed Chapter2 cohorts.

## Required next mechanistic decision

Before any future runs, decide whether the next experiment should keep #451's *assigned phenotypic* A-first versus I-first schedule (to test a new **genetic transmission signature of that intervention**) or use spontaneous **inherited** evolution (to test actual natural-order surrogate dynamics). These are **two different experiments** with distinct causal estimands. A new design should not silently move between them. No prospective experiment was launched by this PR.
