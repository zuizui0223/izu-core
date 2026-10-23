# R2: exact maternal pollen-payoff boundary under the frozen Model 3 assay

**2026-10-23 — exploratory, source-conditional, no biological population simulation.** This is a static analysis of the original native reproductive operator. It does not revise R1–R5, the registered G/S, or the independent fresh-founder R2 verdict (**inconclusive overall**).

## Why investigate this mechanism?

The archived 384-path exploratory factorial showed sparse additional assurance-A responses after strong previous pollen limitation. It also showed terminal convergence and source constraints. The two historical baselines had different *actual pollen receipt*, not only different prior genotypes. Consequently the distinction between pollen payoff and genetic accessibility matters before making an evolutionary-memory claim.

## Exact instantaneous maternal accounting

For the frozen delayed-selfing, no-pollen-discount setting, let q be the fraction of available ovules fertilized by outcross pollen before selfing, v = 1 − depression = 0.5, and c_A = 0.5 the direct assurance allocation cost. At fixed M and I, ovules are proportional to exp(−c_A A²). The source's viable maternal seed return is

    Y(A,q) = O(A) [ q + v A (1−q) ].

Holding recipient pollen q fixed, the exact maternal log-return derivative is

    g_A = v(1−q) / [q + v A(1−q)] − 2 c_A A.

For the interior region where 1−2 c_A A² is positive, this derivative crosses zero at

    q_star(A) = v(1−2 c_A A²) / [v(1−2 c_A A²) + 2 c_A A].

Thus q_star(0.3)=0.602649 and q_star(0.5)=0.428571. These are **conditional pollen-fertilization cutoffs for a local maternal payoff**, not a population-scale tipping point, founder threshold, speciation threshold, or full paternal-inclusive A selection gradient.

## Eight frozen visitor reporter contexts

The new runner loads the **exact original frozen 384 design** and checks original native operator SHA identities. It constructs 48 identical artificial plants with M=I=.5, A=.3/.5; six visitors have either the original strong or weak effectiveness, with original control or decline activity. It checks the full native reproduction ledger against the exact maternal formula and a central finite-difference derivative, in **all eight** source conditions, without population advancement.

Original approximate static q, with rounded analytical gradients:

| Reporter A | Original visitor baseline | Future activity | Approximate q | Maternal log-return gradient | Direction |
|---:|---|---:|---:|---:|---|
| 0.3 | Strong limitation | 0.40 | 0.145 | +1.264 | Positive |
| 0.3 | Strong limitation | 0.04 | 0.017 | +2.684 | Positive |
| 0.3 | Weak limitation | 0.40 | 0.995 | −0.297 | Negative |
| 0.3 | Weak limitation | 0.04 | 0.440 | +0.234 | Positive |
| 0.5 | Strong limitation | 0.40 | 0.145 | +0.691 | Positive |
| 0.5 | Strong limitation | 0.04 | 0.017 | +1.369 | Positive |
| 0.5 | Weak limitation | 0.40 | 0.995 | −0.497 | Negative |
| 0.5 | Weak limitation | 0.04 | 0.440 | −0.018 | Negative |

The q values are from the *pre-execution homogeneous reporter diagnostic* in the original frozen protocol. Because pollen discount is zero and all reporters share M and I, their pollen fraction is independent of A. The new native source reader calculates the unrounded eight-cell numbers; this table is not a set of newly simulated evolutionary outcomes.

A drop in pollen delivery changes not only the magnitude but, for some existing reporter states, **the sign of the current maternal return**. Yet that fact does not establish that observed 384-path A responses were caused by that gradient. The plant's paternal contribution, standing alleles, lineage history, finite sampling, and the change in complete population state remain distinct.

## Requirements for an independently identifiable next R2 experiment

1. Capture full diploid t30 donor genotypes, allele origins, M/I/A covariance, pedigree links, population size, actual recipient-specific pollen delivery, and matching state; summary mean A is not a sufficient state representation.
2. Cross **new independent founders** with **new independent visitor histories** and matched future decline/control streams. Common external visitor activity is *not* mother-specific equality of q.
3. Use source-native evolutionary futures as one experiment. Keep any artificial recipient-pollen equalization **strictly a static maternal intervention** unless a validated pollen-donor transmission law is separately introduced. Report equalization failures, not imputed zero differences.
4. Separately register outcomes for the frequency of biologically meaningful A responses, signed A magnitude conditional on nonzero, all-start A/I changes, target-allele support and extinction. Pick meaningful thresholds and independent source-axis power **before** seeing new outcomes.
5. Freeze source commit, schedules, seeds, inference rules, provenance and population-run authorization in a new independent protocol. Existing 384 exposed data cannot be made prospectively confirmatory by relabeling.

At identical complete inherited state, external visitors and random sources, the native Markov model has no extra historical label effect. Prior history may nevertheless matter through the state it leaves, including allelic support, A/M/I distribution and demography.

## Source paths and execution

- Original frozen protocol: docs/protocols/CHAPTER2_BASELINE_POLLEN_LIMIT_2X2_FROZEN_20261019.json
- Original native population runner: scripts/chapter2_pollen_baseline_factorial_20261019.py
- Native reproductive operator: scripts/model3_island/reproduction.py
- New static reader: scripts/audit_chapter2_r2_static_maternal_pollen_boundary_20261023.py
- New read-only regression: tests/test_chapter2_r2_static_maternal_pollen_boundary_20261023.py

Commands: python -m scripts.audit_chapter2_r2_static_maternal_pollen_boundary_20261023 ; python -m pytest -q tests/test_chapter2_r2_static_maternal_pollen_boundary_20261023.py.

All new biological population updates, prospective p-values and registration promotions remain **zero**.
