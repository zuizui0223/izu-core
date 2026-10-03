# Chapter 2 history versus demography repeatability audit — 2026-10-03

**Status:** exploratory post hoc diagnostic; not preregistered.

## Why this audit was needed

After the persistence-boundary audit, the depression-0.75 deterministic mixed-history result could no longer support nonparallel evolution among persisting populations. The focal repeatability evidence therefore came from the occupied depression-0.50 finite ABM, where the mean response was negative but sign labels were repeat-sensitive.

That raises a sharper question: are finite realized differences structured by the simulated visitor history, or are they mostly demographic noise?

## Data

No new simulation was run. The diagnostic reconstructs the exact finite-ABM response tensor from all 16 archived shards of the frozen 24,576-case bridge:

- 128 independent visitor histories;
- three starting investment states;
- eight demographic repeats;
- natural, richness-matched, visitor-pooled and capacity-192 interventions.

The endpoint is the paired far-minus-near terminal-minus-initial investment response.

## Diagnostic

A balanced mixed-ANOVA decomposition treats starting state as fixed, visitor history as random, history × starting state as random and demographic repeat as residual. Because this diagnostic was designed after the focal outcomes were known, inferential statistics are explanatory rather than confirmatory.

We additionally compute a split-half reliability: for each visitor history, average repeats 1–4 and 5–8 (and average the three starts), then correlate the two independent estimates across 128 histories. Bootstrap intervals resample histories; a permutation diagnostic independently shuffles history labels within each start × repeat.

## Result

| intervention | mixed histories ε=0 | history variance | demographic variance | single-trajectory ICC | reliability of 8-repeat mean | first4 vs last4 history r |
|---|---:|---:|---:|---:|---:|---:|
| Natural | 12 | 0.00549 | 0.02677 | 0.170 | 0.621 | **0.690** |
| Richness matched | 68 | 0.00154 | 0.02573 | 0.068 | 0.369 | **0.424** |
| Visitor pooled | 0 | 0.00042 | 0.02916 | 0.014 | 0.103 | **0.214** |
| Capacity 192 | 1 | 0.00801 | 0.01489 | 0.370 | 0.825 | **0.852** |

The split-half correlations are larger than the history-shuffled null in all four treatments, but the mechanistic contrast is the important part.

Compared with the natural arm, visitor pooling reduces split-half history reliability by **0.476** (paired bootstrap 95% interval −0.667 to −0.287), whereas increasing plant capacity raises it by **0.162** (0.070 to 0.262).

## Interpretation

Two interventions both make categorical sign outcomes look more parallel:

- visitor pooling changes mixed histories from 12 to 0;
- capacity 192 changes mixed histories from 12 to 1.

But they do so for opposite reasons.

**Visitor pooling removes the environmental-history signal itself.** History variance and continuous split-half repeatability collapse.

**Larger plant capacity reduces demographic noise and exposes a more reproducible history signal.** Mixed sign labels nearly disappear even though continuous history reliability becomes stronger.

Therefore a categorical count of parallel/nonparallel signs cannot identify the mechanism generating apparent evolutionary parallelism. Fewer mixed-sign histories can mean either stronger recovery of an underlying history-conditioned response or erasure of the history contrast being measured.

## Claim boundary

This was motivated after outcomes were known. It is a mechanism audit, not a preregistered headline test. It does not estimate natural history variance, natural demographic stochasticity or branch prevalence.
