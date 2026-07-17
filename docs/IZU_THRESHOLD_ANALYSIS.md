# Izu threshold-identifiability analysis

## Scientific target

The retained question is not whether public databases show an island syndrome. It is whether an ordered three-regime design can distinguish no response, smooth clinal change, and a predeclared second-regime threshold.

The biological calibration keeps three Campanula channels separate:

- floral size: cline candidate;
- multilocus outcrossing: cline candidate;
- autonomous reproduction: second-step candidate.

## What the simulation establishes

The recovery audit generates data under each declared shape, refits all candidate shapes, and reports a confusion matrix. Primary diagnostics are false selection of `second_step` when the truth is `cline`, and recovery of `second_step` when it is truly present. Sensitivity analyses should vary effect size, noise, sample size and missing regimes.

## What it does not establish

The simulator does not prove that the real system contains a threshold, identify its historical cause, or estimate unobserved pollinator efficiency. Real channel-level observations and uncertainty are required for that step.

## Next analysis

Fit the same candidate shapes to frozen flower-size, outcrossing and autonomous-reproduction summaries, then compare observed model-selection statistics with the recovery distributions generated here.
