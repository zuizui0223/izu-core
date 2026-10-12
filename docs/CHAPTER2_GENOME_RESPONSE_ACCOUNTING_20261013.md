# Existing-genome realization accounting

2026-10-13. Retrospective accounting of the original 320 ABM trajectories; no new biological cohort.

All 64,000 updates were checked against the original reproductive source and birth-only inheritance/mutation replay. Saved birth states matched exactly. Independent arithmetic from raw genomes and parentage agreed within 5.552e-17. Actual GitHub run [38276636285](https://github.com/zuizui0223/izu-core/actions/runs/38276636285) reproduced all 320 cases; local versus downloaded readouts differed by at most 1.422e-13 across 1,601,280 floating-point fields.

## Investment change over 200 updates

Each row is the signed mean over 32 demographic seeds in one fixed founder/environment context. It is descriptive, not independent ecological replication.

| Founder block | Supply | Composition | Expected selection | Parent sampling | Transmission | Birth mutation | Actual change | I allele fixed by200 |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| causal_confirmation | 0.0 | empty | -0.067910 | -0.004309 | +0.001907 | +0.000000 | -0.070312 | 32/32 |
| causal_confirmation | 0.125 | matched | -0.033484 | -0.006779 | +0.006327 | +0.000000 | -0.033936 | 30/32 |
| causal_confirmation | 0.125 | separated | -0.065105 | -0.008219 | +0.002116 | +0.000000 | -0.071208 | 31/32 |
| causal_confirmation | 1.0 | matched | +0.136490 | -0.011714 | +0.012390 | +0.000000 | +0.137166 | 29/32 |
| causal_confirmation | 1.0 | separated | +0.083891 | -0.000497 | +0.010396 | +0.000000 | +0.093791 | 27/32 |
| causal_main | 0.0 | empty | -0.093482 | +0.001197 | +0.006348 | +0.000000 | -0.085938 | 32/32 |
| causal_main | 0.125 | matched | -0.050198 | +0.021817 | +0.008362 | +0.000000 | -0.020020 | 31/32 |
| causal_main | 0.125 | separated | -0.086929 | -0.025600 | +0.003153 | +0.000000 | -0.109375 | 32/32 |
| causal_main | 1.0 | matched | +0.085032 | -0.010040 | +0.010213 | +0.000000 | +0.085205 | 29/32 |
| causal_main | 1.0 | separated | +0.062327 | -0.009104 | +0.006388 | +0.000000 | +0.059611 | 30/32 |

## Interpretation and boundaries

In the main founder block at supply0.125 with matched visitors, expected investment response accumulated to -0.050198, while realized change was -0.020020. The parental-sampling and transmission terms offset part of the decline. These are exact pathwise contributions: the expected response itself depends on the realized sequence of resident states. They cannot be interpreted as the difference between an actual population and a no-noise counterfactual.

Investment reaches single-allele fixation in 27–32 of 32 trajectories per context. With investment mutation disabled, all subsequent investment response terms are zero. This establishes loss of accessible standing variation within these runs; attributing a deterministic-versus-ABM difference requires a source-matched density comparison. It is not a measurement of neutral genetic diversity.

Only assurance mutates in this cohort; matching and investment retain their original standing alleles. Census remains 42–48, so these runs do not establish an extinction mechanism or a natural-order survival advantage. Signed mean parental/transmission terms do not estimate noise variance.

## Preserved evidence

The [public release](https://github.com/zuizui0223/izu-core/releases/tag/four-question-resolution-20261013) preserves the actual GitHub artifact, the separate raw-genome arithmetic receipt and the actual full readback comparison. Artifact `genome_response_accounting_github_20261013.zip`: 8,281,833 bytes; SHA256 `115636a338c847fdf1f80ae9e39cdfc622fcf38c7f70575e37d245bf7c41b098`. GitHub source revision `d3127ddf2e06014d4d2659d96b4e6ee7bc61ee45`; accounting auditor source SHA256 `344d82931c31b9e6648d1ec5e5ca53c338040f2bdb3a2c92ba35faad4a58bc66` is not substituted for the envelope identity; consult the actual receipt for the exact source digest.
