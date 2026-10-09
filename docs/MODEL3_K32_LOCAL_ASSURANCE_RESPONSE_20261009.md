
# Model 3 K32 finite source-state assurance perturbation experiment

## Question

The earlier eight-generation comparison found strong mean assurance
high-allele increase, but no robust source-specific endpoint variance
reduction: the source-versus-comparator variance gap reversed sign when
the 256/256 demographic training and evaluation folds were swapped.
Therefore this new experiment tests a **one-step local reproductive
response at the very same integer parental source state**, rather than
repeatedly fitting terminal variance.

## Frozen original settings

- Canonical Model 3 reproduction, pollen self-exclusion, full joint
  three-locus diploid Mendelian offspring law, and capped Poisson
  recruitment are unchanged in the source.
- K=32, zero mutation, zero adult survival or immigration, prior_selfing,
  eight annual updates and the existing engineered four-founder
  27-genotype allele support.
- ONLY archived old visitor history 26110601 (near). The prospective
  independent confirmatory visitor histories are not accessed.
- Run 128 nested demographic source trajectories for ovule budgets 8
  and 3, inspecting source states before updates in generations 3,5,7,8.

## Paired exact counterfactual

For each occupied parent genotype-count state C at an inspection year,
swap exactly ONE assurance allele copy high-to-low or low-to-high in one
individual while keeping capacity, census, two other loci, and source
ecological visitor configuration constant. The parental high-allele
frequency moves by precisely +/-1/(2N); the parental assurance trait
sum changes by +/-0.25.

For the original parent C, compute the source conditional offspring
genotype probabilities using canonical reproduce and the exact Mendelian
kernel. Then fit the assurance exponent theta of a counterfactual
equal-parent neutral-Mendelian model, so the *baseline conditional
expected next-assurance frequency* agrees with source Q(C).

Freeze this fitted theta when computing counterfactual Q(C') after
the single-copy perturbation. Compute the source Q(C') without changing
its biological rule. Contrast the discrete local response slopes:

    source_slope = [source_next_mean(C') - source_next_mean(C)] / delta_p
    control_slope = [tilted_next_mean(C') - tilted_next_mean(C)] / delta_p

A one-step expected change slope equals response slope - 1.
A source slope below the control slope indicates stronger attenuation
of this SPECIFIC allele-copy perturbation than a simple directionally
weighted Mendelian comparator, not unique adaptive stabilizing
selection, and not an eight-year causal variance reduction.

Crucially, at assurance allele p=0 or p=1 the baseline comparator tilt
is unidentifiable: all parent assurance gametes are the same.
Such fully fixed baseline states must be EXCLUDED, not assigned a
fictional zero tilt. Both intervention orientations, exclusions,
sample sizes and source/restoration slopes are recorded separately.

This control is deliberately different biological reproduction and is
calibrated from the source baseline, hence exploratory/post-outcome.
The original source biology is unchanged. It uses exactly one archived
visitor history (NOT 128 independent ecological histories). No natural
observational data, INLA or full continuous SDE/SPDE validation.

## Execution

    pytest -q tests/test_model3_k32_local_assurance_response.py
    python -m scripts.audit_model3_k32_local_assurance_response --out local-response-budget8.json --budget 8 --draws 128
    python -m scripts.audit_model3_k32_local_assurance_response --out local-response-budget3.json --budget 3 --draws 128

The existing PR420-only core CI job model3-k32-local-assurance-response
checks the exact state conservation, baseline equality,
non-identifiable fixation boundary and archived visitor-history
provenance before archiving complete 3/5/7/8-year results.

**Stop line:** No scientific numerical outcome is admitted until
CI and raw result receipt are inspected. Any finding is source
conditioned numerical sensitivity, not independently verified
ecological stabilizing selection.
