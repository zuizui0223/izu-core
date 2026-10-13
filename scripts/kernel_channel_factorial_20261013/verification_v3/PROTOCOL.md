# Existing-kernel recruitment/genotype factorial diagnostic

Post-discovery algebraic analysis; not confirmatory biological evidence. Freeze before calculating new hybrids. No original biological rules, source histories, parameters, conditions, initial states, horizon or event definitions change.

## Inputs and scope

Use only the already admitted native_regenerated_kernels_and_state_curves.npz (SHA256 d34fc60c389775f88fa8a54051fdfe90a76ef7864b8f5a813b99d5f0b68ca172) and duration_accounting.json (SHA256 cd4c2f8fc8584fce1b453d31a6a4bee9f96d7d22853831ccce95caf8c7253ba2). Preserve 96 original kernels, 48 pairs, 165 states, K=8, H=80 and all-heterozygote N=8 initial population. M=.2 and A=.35 are constant; expression treatment clamps investment I=.35 while genomic I remains inherited. This is not an assurance-clamp full-genome ABM.

Source transition rows are capped-Poisson recruitment followed by multinomial offspring genotypes. Existing source factorial audit treats recruitment intensity mu and offspring-genotype distribution q as separate channels in an existing factorial implementation. Extend the same algebra to the entire saved 48-pair inventory, without executing reproduction or advance.

## Recover and validate channels before interpretation

For every living row recover mu=-log(T[row,extinct]) and q from the three N=1 target probabilities normalized by their sum. Require 0<T[row,extinct]<1, finite strictly positive N=1 total probabilities and finite nonnegative unit-sum q; fail closed if a channel cannot be recovered. Independently recover q from expected target genotype counts divided by expected target census. Reconstruct each entire original kernel as capped-Poisson(mu) times multinomial(q). Reject all nonfinite inputs, channels, reconstructed matrices, curves and diagnostic metrics. Require maximum absolute discrepancy <=1e-12, stochastic-row closure <=1e-12 and recovered q agreement <=1e-12. Preserve raw discrepancy values. No tolerance adjustment after outcomes. Extinct row remains absorbing.

## Four channel combinations

For each original pair calculate T(mu_native,q_native), T(mu_native,q_clamped), T(mu_clamped,q_native), T(mu_clamped,q_clamped) from recovered channels. Hybrids are artificial statewise operator interventions, not realized biological trajectories or pure natural mediation. Preserve both original corner laws.

Starting from the original initial state propagate each law through 80 updates. Endpoint reward is occupancy at census80. Restricted duration is the sum of occupancy at censuses0..79, exactly as original. Verify each reconstructed original-corner full occupancy curve and its absolute endpoint/duration against its saved corner before interpretation, in addition to both contrasts against all original 48 comparison records at <=1e-12. Retain all four occupancy curves, all48 contrasts, all original 12 endpoint-positive/duration-negative labels and other36 cases, without filtering outcomes.

## Exact factorial accounting, no unique causal share

Write F00=clamped mu/clamped q, F10=native mu/clamped q, F01=clamped mu/native q, F11=native mu/native q. For each reward report recruitment-only F10-F00, genotype-only F01-F00, interaction F11-F10-F01+F00, full F11-F00. Preserve native-reference contrasts F11-F01 and F11-F10 too. Verify exact additive closure <=1e-12. Do not allocate interaction or label either reference a unique causal proportion. Absolute signs under the specified artificial laws may explain how count and genotype channels combine in this finite kernel; they cannot establish natural sequence benefit, historical cause or universal ecological boundary.

## Independent verification and publication

Separate verifier must not import producer. Recover q via target-count expectations and mu independently, reconstruct with independent arithmetic, verify all original corners and 192 hybrid laws and curves. Publish frozen protocol/source before new hybrid readout; retain input identities, source hashes and independent receipt. No inferential test, selected subset hypothesis or new random stream. Technical failure is not a scientific null. If original-row reconstruction fails, stop and preserve failure instead of replacing source values or changing tolerance.

Capture all source/protocol hashes from the prepublished frozen manifest before computation and verify unchanged again before output publication. No source identity may be inferred only after computation.
