# Equal-initial-A Q3 pilot: completed outcomes and the precision decision

**2026-10-18 — exploratory result, not confirmation of the unified hypothesis.**
One-paper parent: PR #590. Controlling pilot: PR #597. Do not pool the
heterogeneous-initial-A pilot #596, the earlier 8 histories, or 2,304 old
source histories as independent replicates of this effect.

## Source and what actually executed

The frozen pilot design preceded execution. Head `cc17c7355d27b907b71b124046990b914e4963dd`
was tested as merge checkout `57d022dfd382eef4df2e63f9e0aebb451ae46605`,
[Actions 39106340477](https://github.com/zuizui0223/izu-core/actions/runs/39106340477).
Python 3.10/3.11/3.12 jobs all passed. Their event records and endpoint counts
agree; the logged fixed-arm accessible-census sum differs by about 3.55e-14.
These are replays of the SAME producer, not independent implementations.

There were 6 independent founder seeds x 6 independent visitor-history
seeds x 2 nested demographic repeats x 2 A policies: 144 paths, 80 updates,
11,520 unique historical updates. Both policies started with the same
48 diploid adults, all expressed A=0.5, while retaining A alleles in
(.25,.75), (.5,.5), (.75,.25) pairs. Delayed selfing, direct A cost 0.5,
zero I/A/M mutation and zero seed immigration were used. Fixed A still
permits selfing. Functional visitors changed from six to one, then zero
from update 35. No restored-descendant evolutionary futures were run.

The event source table is [retained separately](audits/CHAPTER2_EQUALA_PILOT_EVENT_SOURCE_20261018.json).
It was transcribed from connector-read CI event summaries and checked
against counts, paired moments, all three event tables and original
accessible-census sums. This is NOT a fresh readback of raw NPZ genomes.

## Results from the complete event table

| By census 80 | Fixed A | Evolving A |
|---|---:|---:|
| HIGH-I founder-target support lost | 42/72 (58.33%) | 58/72 (80.56%) |
| Living | 72/72 | 72/72 |
| Living with HIGH-I allele support | 30/72 | 14/72 |
| Mean accessible censuses, t=0..80 (81 slots) | 63.9306 | 53.5694 |
| HIGH-I loss strictly before imposed t=35 | 7/72 | 18/72 |

The paired loss difference is **+22.22 percentage points**, and the
accessible-census difference is **-10.3611**. Among 72 paired streams,
36 lost support in both policies, 8 in neither, 22 in evolving only and
6 in fixed only. Six founder-specific paired differences range from
-8.33 to +58.33 points; five are positive and one negative.

All 144 populations survived: this pilot does not establish a survival
benefit or practical equivalence in survival. HIGH-I closure means failure
of a necessary allele-support condition for the strict founder-mean target,
not observed failure of post-return evolution or loss of all partial recovery.
The 1,296 positive same-genotype pollen-service assays only establish that
those imposed visitors deliver effective pollen; they are not 1,296 recovery trials.

## Independent, read-only uncertainty calculation

The new reviewer imports NO Model3 simulation operators. It reconstructs
both paired endpoints and the source moment estimates directly from the
144 event records. Founder and visitor levels are resampled independently;
both policy arms remain paired and the two nested repeats are averaged
within each sampled cell. This is the pigeonhole-bootstrap approach for
crossed sources (Owen 2007, doi:10.1214/07-AOAS122; Owen & Eckles 2012,
doi:10.1214/12-AOAS547).

All 462 possible multinomial count vectors for each six-level axis are
enumerated: 213,444 count-vector pairs representing 6^12=2,176,782,336
ordered resamples. Integer multiplicities remove Monte Carlo sampling
error from the empirical bootstrap distribution. **They do not make
confidence-interval coverage exact**, especially with only six source
levels per axis. These intervals are post-outcome exploratory diagnostics,
not retrospectively registered hypothesis tests.

| Evolving minus fixed | Nominal 95% percentile interval | Nominal 97.5% marginal sensitivity |
|---|---|---|
| HIGH-I loss probability | [0.00, +45.83] pp | [-4.17, +50.00] pp |
| Accessible census count | [-20.1667, -0.4028] | [-21.5694, +1.0278] |

The 97.5% column illustrates a two-endpoint Bonferroni-style sensitivity;
it is not a claim of exact simultaneous coverage. **No confirmed Q3
ratchet/lifeboat verdict follows.** The direction is suggestive after
matching initial A expression, but its uncertainty remains material.

## What this provides to #585, and what it does not

Recomputed paired HIGH-I loss moment components: founder 0.0233333,
visitor 0 after truncation, founder x visitor interaction 0.0655556,
within-cell demographic 0.2777778. A truncated zero is not evidence that
true visitor variance vanishes. With two repeats the cell-level combined
interaction/noise component is 0.2044444.

Applying #585's normal/Bonferroni screening convention (two outcomes,
familywise alpha=.05, joint directional screening target=.80) gives these
**assumption-dependent minimum detectable effect proxies**, not power
estimates or execution authorization:

| F x V, with two repeats and two policies | Historical paths | Baseline proxy | Explicit stress assumption |
|---|---:|---:|---:|
| 6 x 6 | 144 | 34.46 pp | 58.72 pp |
| 16 x 16 | 1,024 | 16.74 pp | 31.14 pp |
| 32 x 32 | 4,096 | 10.74 pp | 20.89 pp |
| 64 x 64 | 16,384 | 7.17 pp | 14.35 pp |

The stress column assumes founder=visitor=.05, interaction=.20,
within-cell=.40; these are transparent sensitivity assumptions, NOT
estimated upper confidence limits. For example, a hypothetical 15-pp
target could pass the baseline screen at 32x32 but fail that stress
screen. It has not been selected as a biological SESOI.

**Decision: HOLD new confirmation.** An empirically informed genetic-loss
variance is now available. However, no survival failures were observed,
a scientifically justified smallest important effect is not yet fixed,
and a source-qualified adverse-variance/full joint-power review is absent.
Simply expanding the same ceiling-saturated survival experiment cannot
be claimed to test both halves of the unified hypothesis. Preserve this
pilot, then define a separate prospective design rather than enlarge it
until a preferred sign appears.

## Reproduction and verification

Run `python -m scripts.audit_chapter2_equalA_precision_20261018 --out NEW.json`.
Four focused read-only tests cover event admission, source-count/moment
rederivation, exact resampling weights against brute-force 2x2 enumeration,
and rejection of zero-filled/missing event records. No biological paths
were added by this reviewer. All original source, seeds, protocol files,
main, and past positive/negative/inconclusive results are unchanged.
