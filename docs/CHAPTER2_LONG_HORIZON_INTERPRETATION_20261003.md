# Chapter 2 long-horizon interpretation audit — 2026-10-03

**Status:** completed prospective deterministic/mutation horizon diagnostic; finite-population long-horizon persistence diagnostic separately frozen and pending.  
**Design:** `data/design/chapter2_long_horizon_stationarity_20261003.json`  
**Result:** `data/results/chapter2_long_horizon_stationarity_20261003.json`

## Decision

The 200-season Model 3 response must **not** be described as a demonstrated stationary or equilibrium island-syndrome endpoint.

The prospective horizon extension to 6400 reproductive seasons failed the frozen stationarity criteria for both the isolation backbone and the standing-variation/mutation comparison.

## Deterministic isolation backbone

At inbreeding depression 0.75, the mean far-minus-near inherited-investment effect changed:

| reproductive season | mean effect | negative histories | mixed | positive | neutral |
|---:|---:|---:|---:|---:|---:|
| 200 | -0.4142 | 122 | 2 | 1 | 3 |
| 400 | -0.3186 | 117 | 4 | 3 | 4 |
| 800 | -0.1794 | 109 | 0 | 1 | 18 |
| 1600 | -0.0774 | 70 | 0 | 0 | 58 |
| 3200 | -0.0181 | 27 | 0 | 0 | 101 |
| 6400 | -0.00195 | 3 | 0 | 0 | 125 |

The late intervals did not satisfy the prospectively frozen stationarity rules.

This decay toward zero is **not evidence of clean adaptive convergence**. The deterministic genotype-density closure enters a sub-individual expected-mass regime. At season 200, 98.18% of far start×history density trajectories already have expected density mass below one individual; by season 1600, all near trajectories also have expected mass below one. Median far density mass is approximately 0.00030 at season 200 and approximately 3.8e-8 from season 800 onward.

Therefore the density model is informative as a deterministic inherited expectation, but long-run trait values after expected mass falls below one must not be interpreted as a persisting natural population.

The original finite-population bridge remains distinct: at its frozen 200-season horizon and inbreeding depression 0.5, all 3072 natural near cases and all 3072 natural far cases were occupied. Thus the finite 200-season result is not itself an extinction artifact.

## Standing variation versus mutation

The high-standing/no-mutation to low-standing/central-mutation response ratio changed:

| season | high standing response | low standing + mutation response | high / low |
|---:|---:|---:|---:|
| 200 | 0.1794 | 0.0402 | 4.47 |
| 400 | 0.1968 | 0.0769 | 2.56 |
| 800 | 0.2015 | 0.1354 | 1.49 |
| 1600 | 0.2039 | 0.2252 | 0.91 |
| 3200 | 0.2039 | 0.3014 | 0.68 |
| 6400 | 0.2039 | 0.3659 | 0.56 |

The low-standing population with the central mutation input catches and overtakes the high-standing no-mutation reference between 800 and 1600 seasons. The late response ratio and genetic-variance diagnostics remain nonstationary at season 6400.

The defensible interpretation is therefore **early-response advantage from standing variation**, not persistent genetic-accessibility dominance.

This time ordering has direct theoretical precedent: adaptation from standing variation is expected to begin faster, while the contribution of de novo mutation can increase through time. It should therefore be used as a scope correction and mechanism validation, not advertised as a new general principle by itself.

## Consequences for the EL framing

Retain:
- visitor functional composition can redirect selection at fixed visitor number;
- at a fixed, declared 200-season horizon, aggregate response and history-level parallelism are different objects;
- finite demography and history modify realized outcomes;
- genetic accessibility is time dependent.

Demote/remove:
- any claim that the negative deterministic isolation backbone is a long-run stationary syndrome;
- any claim that history-level nonparallelism demonstrated at the focal horizon necessarily persists indefinitely;
- any claim that standing variation is a persistent dominant accessibility filter.

New candidate general statement:

> **Evolutionary repeatability is both resolution-dependent and horizon-dependent: a syndrome-like aggregate direction observed during a bounded adaptive window need not define either the underlying trajectories or the long-run evolutionary endpoint.**

This remains a model-derived statement. Natural island prevalence and natural time scales are not identified.

## Why not simulate geological time

A Model 3 step is a reproductive season. Extending the same stationary visitor process for thousands or millions of steps does not add succession, changing source pools, speciation, coevolution, juvenile stages or calibrated natural mutation/demographic rates. Once finite-population persistence fails, further trait iteration is not a biological equilibrium experiment.

The relevant empirical question is therefore not “how many millions of years until equilibrium?” but “over what biologically plausible response window do selection, genetic input and demographic persistence operate?”

