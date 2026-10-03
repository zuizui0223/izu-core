# Chapter 2 finite-history signal diagnostic — 2026-10-03

**Status:** exploratory post-hoc diagnostic using the exact verified exports from the original prospective bridge. No simulation was rerun.

## Why this diagnostic was needed

The occupied finite bridge has a directional aggregate mean but sign-level history labels are unstable across demographic repeats. That makes the raw count of mixed histories an unsafe standalone measure of evolutionary repeatability.

The diagnostic therefore asks a narrower question: **is there a reproducible continuous visitor-history signal underneath demographic noise, and do the two interventions that reduce mixed-sign histories do so by the same mechanism?**

## Analysis

For each intervention, the finite-ABM far-minus-near investment tensor has dimensions:

`3 starting states × 128 visitor histories × 8 demographic repeats`.

A balanced crossed variance decomposition treats starting state as fixed, visitor history and start×history as random, and demographic repeat as residual. Variance components are constrained at zero. We report:

- history-structured continuous variance;
- residual demographic variance;
- reliability of one finite trajectory;
- reliability of the eight-repeat mean;
- split-half correlation of history means (repeats 1–4 vs 5–8, averaged over starts);
- the existing sign-based mixed-history and repeat-disagreement counts.

Uncertainty is a 1,999-resample visitor-history cluster bootstrap using seed `927032`.

## Result

| Intervention | mixed histories (ε=0) | repeat-label disagreement | history variance | demographic residual | reliability of 8-repeat mean | split-half history r |
|---|---:|---:|---:|---:|---:|---:|
| natural | 12 | 97 | 0.00549 | 0.02677 | **0.621** | **0.690** |
| richness matched | 68 | 128 | 0.00188* | 0.02573 | 0.369 | 0.424 |
| visitor pooled | **0** | 77 | 0.00042 | 0.02916 | **0.103** | **0.214** |
| capacity 192 | **1** | 31 | 0.00875* | 0.01489 | **0.825** | **0.852** |

*history-structured variance includes the estimated start×history component when positive.

For the natural bridge, the history main-effect variance is 0.00549 (95% bootstrap interval 0.00404–0.00711) and the demographic residual is 0.02677. A single finite trajectory is therefore noisy (ICC 0.170), but averaging the eight declared repeats gives reliability 0.621 (0.549–0.681). The independent first-four versus last-four history means correlate at 0.690 (0.592–0.770).

The two interventions that nearly remove mixed-sign histories do **not** do the same thing to continuous history structure.

### Larger plant population

Capacity 48→192 reduces mixed histories from 12 to 1 and repeat-label disagreement from 97 to 31. At the same time:

- demographic residual falls by 0.01188;
- history main variance rises by 0.00252;
- eight-repeat reliability rises from 0.621 to **0.825**;
- split-half history correlation rises from 0.690 to **0.852**.

The paired bootstrap interval for the reliability increase is +0.147 to +0.263.

Thus larger capacity makes direction more uniform **while history-specific effect magnitude becomes more reproducible**, not less.

### Pooled visitor histories

Pooling eight visitor histories also removes mixed mean-history labels (12→0), but the continuous result moves in the opposite direction:

- history main variance falls by 0.00507;
- demographic residual does not fall;
- eight-repeat reliability falls from 0.621 to **0.103**;
- split-half history correlation falls from 0.690 to **0.214**.

The paired bootstrap interval for the reliability change is −0.607 to −0.395.

Thus environmental pooling makes direction look more uniform largely while **erasing reproducible history structure**.

## Scientific implication

The same visual outcome—fewer mixed-sign histories—can arise from biologically different changes.

> **Directional sign uniformity is not a sufficient measure of evolutionary repeatability.**

In Model 3, larger plant populations reduce demographic noise while preserving or strengthening a reproducible history imprint, whereas visitor-history pooling suppresses the history imprint itself. Both can produce nearly uniform directional labels.

The defensible general implication is therefore not that one intervention “increases repeatability” more than another. It is that **repeatability is multidimensional: directional parallelism, magnitude repeatability and historical imprint can move differently.**

## Claim boundary

This diagnostic is exploratory and post-hoc. It does not estimate natural variance components, prove a general law of evolution, or turn the synthetic history seeds into natural island replicates. Capacity scaling changes the population process, and visitor pooling changes the experienced environment under a nonlinear reproductive operator. The result is used to diagnose why sign-based repeatability can be misleading inside the declared model.
