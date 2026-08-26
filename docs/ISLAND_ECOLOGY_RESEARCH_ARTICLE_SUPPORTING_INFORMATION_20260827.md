# Supporting Information — Conditional response geometry under island pollinator reorganization

**Status:** active manuscript companion  
**Updated:** 2026-08-27  
**Main manuscript:** `docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_20260827.md`

This Supporting Information is part of the active manuscript surface. It exposes the complete model rules required to reproduce the response-geometry, local-context and assurance analyses. The numerical values below are synthetic design and sensitivity choices unless explicitly identified as literature-motivated directions; they are not empirical estimates of one island system.

# Appendix S1. Pollinator environments and matching model

The mainland-like scenario begins with 9 pollinator types, partner-arrival probability 0.28 per step, partner-loss probability 0.015 per extant partner per step, trait dispersion 0.22, generalist fraction 0.35 and replacement fraction 0.05. The oceanic-island scenario begins with 4 pollinator types, arrival probability 0.12, loss probability 0.055, trait dispersion 0.16, generalist fraction 0.58 and replacement fraction 0.22. Pollinator traits are generated around 0.5 on a bounded synthetic matching axis [0,1].

For plant trait `x`, pollinator trait `p` and breadth `b`,

`mismatch = |x - p|`

`raw_match = exp(-(mismatch / b)^2)`.

Generalists use `b = 0.42`; specialists use `b = 0.16`. Introduced/replacement partners receive a multiplicative factor 0.82. Match values are bounded to [0,1].

Under the fixed visit budget, for extant pollinators `j`,

`mean_match = mean_j(match_j)`

`service = 1 - exp(-saturation * mean_match)`.

If no pollinator remains, service is zero. Richness therefore changes partner composition rather than automatically increasing total visitation opportunity.

# Appendix S2. Plant-lineage state and trait adjustment

For the broader lineage simulations, initial synthetic plant traits follow a truncated Normal distribution with mean 0.5 and SD 0.18. Pollinator dependency `d ~ Uniform(0.35, 0.95)`, assurance ceiling `c ~ Uniform(0.10, 0.90)`, assurance responsiveness `r ~ Uniform(0.004, 0.035)`, trait-adjustment scale `a ~ Uniform(0.01, 0.055)`, and initial assurance state is 0.08. The main envelope uses 24 lineages and 120 steps.

When current service is below 0.45 and at least one pollinator is extant,

`x_(t+1) = clamp[x_t + a * (p_best - x_t), 0, 1]`.

This process is retained for completeness but is too weak in the tested envelope to support a substantive inference about in-situ evolution.

# Appendix S3. Weighted opportunity and local availability / interaction filtering

For each plant row, the pre-saturation weighted opportunity assigned to pollinator `j` is

`w_j = match_j / N_pollinators`,

so `sum_j(w_j) = mean_j(match_j)`.

The parameter historically named `support_strength`, here denoted `s`, is local availability / interaction-filtering stress and not beneficial support. The same generic sensitivity value is used in three nested layers:

- plant active probability: `P(plant active) = 1 - s`;
- pollinator active probability: `P(pollinator active) = 1 - s`;
- pair retention probability conditional on feasibility and pollinator activity: `P(pair active) = 1 - s`.

Zero active plant rows are allowed and are not repaired. The inherited pollinator layer conditions on at least one globally active feasible pollinator. Pair draws are not repaired if they create partnerless plants or an empty local network.

The final pair mask is the intersection of the independently drawn plant mask and the pollinator/pair mask. For every retained positive plant row, surviving pair weights are rescaled so that the row total equals the original global opportunity total. Partnerless positive plants are removed locally rather than assigned manufactured service. No new plant, pollinator or pair can be created. At `s = 0`, the projection is bypassed exactly.

After support projection, local affinity redistributes retained pair weights. At context strength `h`,

`factor_j = (1 - h) + h * U(0.1, 1.9)`.

Rows are renormalized to their exact pre-context total. The manuscript analyses use `h = 0.5`.

# Appendix S4. Partner effectiveness, effective service and reproduction

For realized pollinator `j`, quality at strength 1 is

`q_j = 1 + U(-0.8, 0.8)`,

so `q_j` lies in [0.2, 1.8]. Quality acts only on existing positive weights and is geography-independent.

`effective_score = sum_j(w_j * q_j)`

`effective_service = 1 - exp(-saturation * effective_score)`.

Let `d` be pollinator dependency, `S` current effective service, `c` assurance ceiling and `A` current assurance state. The pollinator-dependent route is

`P = d * S`,

and the autonomous route is

`U = (1 - d) * c * A`.

Combined reproductive output is

`R = 1 - (1 - P) * (1 - U)`,

bounded to [0,1]. If `R < 0.50`, assurance increases as

`A_(t+1) = min(c, A_t + r)`.

Because this architecture intentionally adds a compensating downstream route, attenuation of decline magnitude is partly structural. Sign rescue is the stronger discriminating outcome.

# Appendix S5. Assurance sensitivity multiplier

For multiplier `k >= 0`,

`c_k = min(1, c * k)`

`r_k = min(1, r * k)`.

The fixed envelope is `k in {0, 0.5, 1, 1.5, 2, 3, 4}`. A lineage is eligible for sign rescue only when, at `k = 0`, both island-minus-mainland effective-service and reproduction contrasts are negative. Sign rescue requires the reproduction contrast to become non-negative while upstream service remains unchanged.

The final fixed run contained 580 eligible baseline declines and zero sign rescues through 4×; upstream effective-service mismatch count was zero.

# Appendix S6. Matched response geometry

Starting positions are `x_0 in {0.00, 0.05, ..., 1.00}`. Within each realization, every starting position receives the same mainland pollinator trajectory and the same island pollinator trajectory. The fixed primary run contains 96 matched pollinator-community realizations.

The mean response geometry is mixed-sign, with mean sign switches between 0.30–0.35 and 0.65–0.70 on the synthetic coordinate. These are model coordinates, not calibrated biological thresholds.

# Appendix S7. Joint robustness design

The joint analysis uses 48 fixed-seed Latin-hypercube points and 24 matched community realizations per point. Ten dimensions vary simultaneously: trait dispersion, generalist fraction, replacement fraction, partner loss, partner arrival, saturation, trait adjustment, generalist breadth, specialist breadth and replacement penalty.

Each point is classified from the mean starting-position geometry as mixed-sign, all-positive or all-negative. The final counts are 16 mixed, 22 all-positive and 10 all-negative points. These frequencies describe the declared synthetic design volume only.

# Appendix S8. Local-context threshold design

Filtering strengths are `s in {0, 0.10, 0.25, 0.40, 0.50, 0.60, 0.75}` with saturation values 1, 2 and 3, 12 replicates per saturation, 4 local contexts, 24 lineages and 120 steps. The same seed ensemble is used across strength values.

For each lineage, the first non-zero filtering strength at which the sign of island-minus-mainland reproduction differs from its `s = 0` sign is recorded. Across the fixed envelope, 737 lineage contrasts changed sign at least once; the median first sign-change strength was 0.40. This 0.40 value is a synthetic sensitivity threshold, not a field-estimated ecological threshold.

# Appendix S9. Interpretation boundary

The following are not empirically identified by the model: the numerical sign-switch locations on the synthetic trait axis; the median local-filtering first-sign-change strength; the frequency of mixed/all-positive/all-negative design points; an assurance multiplier required in any natural lineage; or 24 lineages, 120 steps and saturation values as demographic quantities.

Empirical claims remain controlled by `docs/CURRENT_EVIDENCE_STATE.md`. External island systems provide ecological grounding and falsification boundaries only; they are not treated as validation coverage of a broad response vocabulary.
