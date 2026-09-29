# Appendix S22. Regime-dependent response hierarchy under active plant adjustment

## S22.1 Question and frozen design

The earlier finite-community system-size audit set `trait_adjustment=0` to isolate stochastic community-composition sampling. That audit therefore could not test whether the relative importance of plant starting state and realized community changes with system size when the headline plant response operator is active.

Before execution, we froze a complementary audit using the unchanged headline `trait_adjustment=0.03`, the existing six-seed sensitivity ensemble, 96 matched community realizations per seed, the same 21 starting positions, and system-size pooling `k={1,2,4,8,16}`. For every replicate, `k` independent pollinator trajectories were pooled at every time step before applying the unchanged plant `endpoint_on_trajectory` operator. The primary decision rule required starting-position sum of squares to exceed community-realization sum of squares at `k=16` in at least 5/6 prespecified seeds, together with a monotonic increase in median starting-position share and monotonic decrease in median community share across `k`.

The original v1 freeze accidentally listed ad-hoc seed IDs and was not admitted. The corrected v2 freeze restores exactly the six pre-existing seeds from the finite-community audit; no result-dependent seed selection was made.

## S22.2 Result

The rank crossover was seed-stable. After correcting the historical mainland/island random-stream collision without changing the six master seeds or any biological parameter, median starting-position share increased from `3.11%` at `k=1` to `12.87%`, `24.70%`, `40.14%`, and `53.53%` at `k=2,4,8,16`, respectively. Median community-realization share declined over the same sequence from `74.27%` to `35.87%`, `23.23%`, `17.38%`, and `14.05%`. Starting-position share exceeded community-realization share in `0/6` seeds at `k=1`, `0/6` at `k=2`, `4/6` at `k=4`, and `6/6` at `k=8` and `k=16`.

Mixed-sign realized communities did not vanish at the crossover. Their corrected six-seed ranges were `43–59/96` at `k=1`, `50–58/96` at `k=2`, `41–56/96` at `k=4`, `36–48/96` at `k=8`, and `26–36/96` at `k=16`. Median state × community non-additivity was `22.82%`, `54.57%`, `50.82%`, `41.97%`, and `32.03%`, respectively.

## S22.3 Interpretation

The variance hierarchy is therefore not globally rank-stable. In the small stochastic-community regime, variation among realized communities dominates. As independent community realizations are pooled while plant adjustment remains active, that additive community component shrinks and plant starting state becomes the larger additive source of response variation. The crossover does not mean that state and community become separable: non-additivity remains substantial, and mixed-sign branch realizations persist at `k=16`.

Together with the separate deterministic mean-field audit, this suggests three model regimes: a small finite-community regime dominated by realized-community variation; an intermediate larger-community regime in which starting state becomes the larger additive component while branching remains; and an asymptotic deterministic limit in which stochastic branch heterogeneity disappears. The median crossover occurs near `k=4`, but seed-level unanimity begins only at `k=8`; neither coordinate is interpreted as a universal ecological threshold.

## S22.4 Claim boundary

This audit strengthens only the model-internal mechanism. It does not estimate natural pollinator-community sizes, show that real island systems cross the same numerical threshold, establish historical causation, or convert the synthetic variance fractions into empirical population variance components. The supported conclusion is that the *ordering of response determinants itself can depend on community stochasticity and system size* when plant state is allowed to respond dynamically.
