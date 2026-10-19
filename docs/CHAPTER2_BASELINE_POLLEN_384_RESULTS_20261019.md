# Baseline pollen limitation and the additional-decline response

## Outcome

The frozen exploratory factorial supports a larger incremental assurance response after weak than strong baseline pollen limitation, in both declared initial-A strata. All 384 trajectories survived. This is a model-conditional baseline-regime/history interaction, not an independent confirmation of a universal law or the instantaneous pollen-deficit effect alone.

## Source and design

[Actions 39233450099](https://github.com/zuizui0223/izu-core/actions/runs/39233450099) completed one full pilot at `eb785dc6865ca1842ec9d6c7d511778c74e03478`: 12 founders × four demographic repeats × two nominal initial-A states × two baseline effectiveness levels × two future arms = 384 trajectories. Every trajectory has 30 prefix and 50 future updates. Within each baseline, future arms share the census-30 population and RNG state; starting genotypes match across baseline arms within each initial-A stratum.

Six external visitors have effectiveness 0.03 or 1.0; activity stays at 0.4 or falls to 0.04. Delayed assurance evolves with direct cost 0.5, capacity 48, ovule budget 8, pollen budget 20 and inbreeding depression 0.5. Mutation and immigration are absent. [Frozen protocol](protocols/CHAPTER2_BASELINE_POLLEN_LIMIT_2X2_FROZEN_20261019.json). This is distinct from the 2026-10-16 Q2 384-path, 200-update investment-support experiment, whose `both_inconclusive` result is unchanged.

The initial dispatch using a SHA was rejected (HTTP 422), creating no run. A verified branch was dispatched once. All raw endpoints, per-update reproduction records, protocol, environment and checksums are in the [draft release](https://github.com/zuizui0223/izu-core/releases/tag/untagged-d629250631040da07a99); it is not a DOI deposit. The original ZIP was downloaded again and SHA256-verified. [Provenance](audits/CHAPTER2_BASELINE_POLLEN_384_PROVENANCE_20261019.json).

## Primary comparison

Within each baseline, compare `(A80−A30)decline − (A80−A30)control`. Because the prefix is shared, this equals the terminal decline-minus-control difference. The interaction is weak minus strong. Units are A trait units, not realized-selfing percentage points.

| Initial A | Strong baseline: additional A response | Weak baseline: additional A response | Interaction | Descriptive founder-bootstrap 95% interval | Positive founders |
|---:|---:|---:|---:|---|---:|
| 0.3 | +0.008735 | +0.112413 | +0.103678 | [0.069499, 0.137804] | 11/12 |
| 0.5 | +0.004612 | +0.088162 | +0.083550 | [0.041450, 0.128147] | 10/12 |

The independent resampling unit is the founder (12), not the trajectory (384). Four demographic repeats are nested. Initial-A strata share founder construction, so they are not two independent replications. Intervals are exploratory and unadjusted; no confirmatory p-value or biological minimum effect was registered. Because all 384 populations survived, this realized allocation has no differential survivor exclusion. [Complete audit](audits/CHAPTER2_BASELINE_POLLEN_384_AUDIT_20261019.json).

## Measured pollen service and inherited state

q is expected outcross fertilization divided by available ovules before selfing. It is neither visitor abundance nor a selfing-compensated deficit. The values below are the first future reproduction from the same census-30 population.

| Initial A | Baseline | q maintained | q after decline | Prefix A change |
|---:|---|---:|---:|---:|
| 0.3 | strong_baseline_limitation | 0.142031 | 0.017202 | +0.266547 |
| 0.3 | weak_baseline_limitation | 0.997989 | 0.542219 | -0.032172 |
| 0.5 | strong_baseline_limitation | 0.120796 | 0.014416 | +0.186795 |
| 0.5 | weak_baseline_limitation | 0.997175 | 0.528713 | -0.067274 |

Under strong baseline limitation, A had already risen before the shock. A was monomorphic at census 30 in 22/48 strong versus 1/48 weak prefixes for initial A=0.3, and 10/48 versus 1/48 for initial A=0.5. Every prefix-fixed pair retained the same A in both futures. Strong-baseline terminal A contrasts were exactly zero in 45/48 and 42/48 pairs. These facts do not establish that selection was absent or that fixation was the sole mediator. The same proportional activity decline also changes q by different amounts; this is not an equal-absolute-deficit intervention.

## Investment and synthesis

Additional I responses were −0.080241 and −0.035699 under strong baseline limitation, but +0.020725 and +0.024631 under weak limitation (initial A=0.3 and 0.5). Preserve these positive contrasts. Earlier four-setting evidence established that I can decline without A evolution under reduced replenishment; it did not establish that every visitor-activity reduction lowers I.

The [stored variation analysis](CHAPTER2_VARIATION_CLOCK_RESULTS_20261019.md) shows evolving assurance shortens occupied I-polymorphic duration by 2.628 updates at B8 (family 95% interval −3.447 to −1.809), but extends it by 12.684 at B4.5 (11.984 to 13.383) alongside better survival. Together, the results support a conditional mechanism: pollen service affects trait returns, while prior evolution and persistence shape the inherited state and variation available for later responses. They do not prove A-mediated genetic causation, a universal timing order, permanent irreversibility, or natural island-flora filtering.

## Independent verification

[Independent reader review](audits/CHAPTER2_BASELINE_POLLEN_384_INDEPENDENT_REVIEW_20261019.json) checked all file hashes, 384 identities, paired prefixes, genetic summaries, 30,720 allocated reproduction records and occupancy, and recomputed founder interactions/bootstrap without importing either producer or endpoint auditor. Full state hashes cannot be reconstructed from summary records; their format and pairing were checked, not full-state replay.
Local Python 3.10 re-reading versus Actions Python 3.12 differed in 34 floating summary fields, maximum 5.55e-16. Strict differences are [preserved](audits/CHAPTER2_BASELINE_POLLEN_384_STRICT_DIFFERENCES_20261019.json). A post-run technical tolerance of 1e-12 was used only for floating comparisons; categorical/integer fields remained exact, and raw values, effects, intervals and scientific thresholds were unchanged.
