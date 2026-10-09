# Chapter 2 — Independent budget-window confirmation: completed negative result (2026-10-09)

## Final result, no retrospective hypothesis promotion

**Prospective follow-up PR #419 completed successfully.** The 64 *new* visitor histories (38110901–38110964), 2,048 complete t400 inherited diploid sources and 57,344 future branches passed the production reader's fail-closed completeness, pedigree, genotype, source-hash and 28-cell posthistory checks. The full run has **success** status.

- [Production GitHub Actions run #37862121201](https://github.com/zuizui0223/izu-core/actions/runs/37862121201).
- Executed source SHA: `868164c24b6a6f17e7530941600fcb50e7281342`.
- Original [complete audited outcome artifact](https://github.com/zuizui0223/izu-core/actions/runs/37862121201/artifacts/11587460323).
- **Byte-exact archived readout**: [`results/chapter2/independent_window_confirmation_20261009.json`](../results/chapter2/independent_window_confirmation_20261009.json). Original JSON SHA-256: `fa3d4103b3f3a84781c052907012a0dfed13caebb247c80f4c34b760a536cc58`, validated in a successful GitHub Actions archival job, [#37863250446](https://github.com/zuizui0223/izu-core/actions/runs/37863250446).
- New prospective protocol SHA-256: `39918e4fe6650f99b0eac4372449509bdef45e58318dc760906d7a8ca3d9fe30`.
- Unmodified original biological protocol SHA-256: `b6f6336875b04a131434ef35d6ec42b59dc14a1e4c59e7e4d6f2513e24a04fdd`.

The original full-grid primary test from #416 remains **`equivalent_within_predeclared_ROPE`**, and the historically failed independent16 mutational-priority test remains **FAILED**. Neither changes because a distinct follow-up was run.

## Predeclared independent primary confirmation

The new primary endpoint is the **64-history mean** of budget-3-and-4 far–near A-first-versus-I-first DID residual **below the log-budget line connecting budgets 2 and 5**, in the eight-founder/capacity-8 stress. The fixed threshold is |mean residual| ≥0.05 and a two-sided 95% bootstrap interval excluding zero, **plus** predictive out-of-history improvement over a predeclared cubic log-budget smooth comparator.

| Predeclared primary gate | Completed new independent cohort |
| --- | ---: |
| Mean window residual | **−0.0151491962** |
| 64-history 95% bootstrap interval | **[−0.0488260038, +0.0180349631]** |
| Residual magnitude/CI gate | **FAIL** |
| CV prediction MSE improvement: smooth minus smooth+window | **−0.0000484355** |
| 64-history 95% bootstrap interval of heldout MSE improvement | **[−0.0001413328, +0.0000426256]** |
| MSE predictive improvement gate (minimum +0.0001) | **FAIL** |
| **Official locked decision** | **`window_residual_practically_equivalent`** |

The interval includes zero and lies strictly inside the predeclared (−0.05,+0.05) practical-equivalence region. The fixed additional window term does not improve held-out history prediction; on average, it worsens prediction. **Therefore the previously exposed budget-3/4 peak is not independently confirmed as an additional localized expression-order effect.** This is not a claim that all possible small or condition-specific order effects are mathematically zero, nor does this cubic baseline exhaust all smooth ecological processes.

## What changed between the original exposed histories and new prospective histories?

The *original* 64 histories were used only to formulate the post-outcome hypothesis, **not** pooled with the new cohort in its formal bootstrap.

| Ovule budget | Original exposed 64-history primary-stress pooled DID | New independently generated 64-history primary-stress pooled DID |
| --- | ---: | ---: |
| 0.5 | 0.000000 | 0.000000 |
| 1 | 0.000000 | 0.000000 |
| 2 | +0.000977 | 0.000000 |
| 3 | **−0.064453** | **+0.002930** |
| 4 | −0.049805 | **−0.062500** |
| 5 | −0.009766 | −0.024414 |
| 8 | +0.000977 | −0.005859 |

The earlier strongest signal at budget 3 did **not** replicate; the largest absolute budget-specific DID in the new cohort is at budget 4. **Do not rename a shifted, post-outcome budget-4 trough as confirmation.** Budget-specific figures are descriptive (multiple budgets examined) and do not replace the predeclared joint gate.

The old exploratory pooled curvature was approximately −0.051666; the **new independent** curvature is −0.015149. These cannot be mistaken for two independent confirmatory estimates: the old one was selected after exposure.

## Bottleneck and mating-system checks

The compulsory **unbottlenecked/capacity-48** comparator also failed both gates:

- window residual **−0.01592645**, history bootstrap95 **[−0.04502427, +0.01181989]**;
- smooth-vs-window prediction improvement **−0.000000208**, interval **[−0.00008697, +0.00009062]**;
- decision: **`window_residual_practically_equivalent`**.

At budget 4 in the primary eight-founder model, the new descriptive far–near DID differs by mating setting: delayed control **−0.035156**, prior selfing **−0.085938**, pollen discount **−0.089844**, assurance cost **−0.039062**. At budget 3 the corresponding effects were **−0.019531, +0.039062, −0.007812, 0.000000**. No consistent, exactly located cross-setting budget-3 step is supported.

## The important ecological interpretation and remaining question

The primary capacity-8 binary occupancy curve exhibits pronounced **floor/ceiling compression**. For both assigned arms, near and far pre-environments, occupancy at budgets 0.5, 1 and 2 is **0** in the newly sampled histories; at budget 8 occupancy ranges approximately **0.989–1.000** across the four treatment-by-pre-environment means. Thus any difference in the occupancy probability is necessarily most observable in the intermediate 3–5 range. **This is a plausible mathematical explanation for apparent intermediate-budget peaks, not a newly demonstrated causal biological mechanism.**

A new independent 64-history campaign therefore failed to support the model-specific claim that a *fixed* intermediate budget window carries a practically meaningful expression-order effect above a smooth resource response. It does not refute every possible history/setting-specific effect and does not measure natural island extinction risk.

**Next methodologically defensible task:** inspect the existing archived annual A/I *inherited* trajectories, source extinction and absolute occupancy by assigned schedule as **descriptive process diagnostics**, without post-treatment selection or genetic-order causality claims. Before any further independent biological cohort, specify a distinct estimand justified by that process analysis rather than shifting the window after failed replication.

No new cohort, biological parameter change, retuned significance gate or retroactive claim promotion is authorized by this readout.
