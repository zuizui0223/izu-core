# Izu effective-service rank-crossover bridge

## Decision

The September 10 synthetic rank crossover is promoted to a new prospective field confrontation, but its numerical system-size parameter is **not** transferred to Izu as raw visitor richness.

The synthetic audit pooled independent pollinator trajectories. Therefore neither observed visitor richness nor an effective number of visitor groups is literally `k`. The field test asks only whether the **ordering of response determinants** changes along a measured effective-service scale.

## Existing Chapter 2 chain

The primary empirical unit remains `block_id × plant_id`:

```text
pre-outcome plant state
        ×
block visitor exposure / composition
        ↓
visitor-specific single-visit pollen deposition
        ↓
rate-weighted effective pollen service
        ↓
open / bagged-autonomous / supplemental-outcross dependency
        ↓
mature seed
```

E1–E3 remain unchanged:

- **E1:** richness-like exposure tests coarse regime placement;
- **E2:** effective-service composition × plant starting state tests residual branch identity;
- **E3:** visitor → SVD/service → dependency → mature seed tests transition-linked propagation.

## New E4: qualitative rank-order confrontation

E4 asks:

> As effective pollen service becomes broader and/or realized service becomes more stable across prespecified blocks, does the relative contribution of plant starting state increase while the contribution of realized community/service composition decreases?

This is the field-facing counterpart of the synthetic result that starting-position share rose and community-realization share fell as independent pollinator trajectories were pooled. A field result is not required, or allowed, to reproduce the synthetic crossover near `k=4`.

## Field service-breadth coordinate

For block `b` and visitor group `g`, define the controlled effective-service weight

```text
w_bg = visit_rate_per_flower_hour × background_adjusted_single_visit_conspecific_pollen_deposition
```

When all controlled weights are non-negative and their total is positive,

```text
p_bg = w_bg / sum_g(w_bg)
N_eff_service,b = 1 / sum_g(p_bg^2)
```

`N_eff_service` is the Hill-q2 effective number of visitor groups contributing pollen service. It is useful because a block dominated by one visitor group is distinguished from a block in which several groups contribute comparable service.

It is **not** a direct estimate of synthetic `k`.

The helper script

```text
python scripts/derive_izu_effective_service_scale.py \
  --block-exposure results/.../block_exposure_by_visitor_group.csv \
  --output results/.../block_effective_service_scale.csv
```

writes:

- controlled effective-service group count;
- total effective pollen delivery;
- Hill-q2 effective service breadth;
- Hill-q2 evenness;
- maximum single-group service share;
- explicit mapping boundary.

Negative background-adjusted service is not clipped to zero to manufacture a diversity value. If any group is uncontrolled/missing or any controlled weight is negative, the scale is unavailable for that block.

## More faithful stochastic-realization coordinate

The closest field analogue of the synthetic community-realization term is not species richness. It is **variation among repeated prespecified blocks in realized effective service**.

Once repeated blocks exist, quantify dispersion in total effective service and effective-service composition after observation-effort control. This `service_realization_stability` coordinate is kept separate from service breadth:

- breadth asks how many visitor groups effectively contribute within a block;
- stability asks how much the realized service state varies among comparable blocks.

The second is conceptually closer to the stochastic component that shrinks under synthetic pooling.

## Confirmatory comparison

The outcome remains same-plant dependency and mature seed. Starting state is measured before outcomes; community state is the controlled effective-service composition.

The confirmatory analysis should compare the predictive/variance contribution of:

1. starting state;
2. realized effective-service composition;
3. their non-additive interaction;
4. total effective service and prespecified nuisance covariates;
5. service breadth/stability as modifiers of that hierarchy.

The preferred comparison is hierarchical and out-of-block. Flowers and visits remain subsamples; plants are nested in blocks. Scale strata, if used, must be defined from exposure-only information before mature-seed outcomes are inspected. No outcome-driven breakpoint search is allowed.

## What would count as correspondence

A qualitative correspondence requires both directions:

- starting-state contribution increases with broader/more stable service;
- realized-community/service-composition contribution decreases.

The starting-state × composition term must still be reported. A rank reversal does not imply that state and community become separable.

## Falsification

The synthetic-to-field correspondence weakens or fails if:

- determinant ordering is stable across the observed service scale;
- community contribution does not decline with service breadth/stability;
- starting-state contribution does not rise;
- the apparent pattern disappears under out-of-block prediction;
- observation effort, total service, site/time or other prespecified covariates explain it;
- the result requires choosing a cutoff after seeing mature-seed outcomes.

## Chapter boundary

This transition-linked visitor → effectiveness → dependency → mature-seed chain belongs to **Chapter 2**, because it directly tests HOW interaction reorganization propagates and the proximal WHY of branch variation.

Chapter 3 retains the direct multivariate *Campanula microdonta* phenotype as the realized phenotype endpoint. Chapter 3 phenotype values are not used to tune E4, choose field scale cutoffs, or retrospectively validate the Chapter 2 synthetic model.

## Claim ceiling

A successful E4 can support:

> the dominant source of contemporary reproductive variation in Izu changes with effective-service context, while state × community contingency remains.

It cannot support:

- `k=4` as a natural threshold;
- visitor richness as literal synthetic system size;
- historical *Bombus* loss as the cause of the observed pattern;
- a universal island threshold;
- a claim that all island systems share the same rank crossover.
