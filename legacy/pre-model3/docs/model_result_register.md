# Izu model-result register

## Why this register exists

The repository currently contains two useful but non-equivalent analysis families.
They reuse some literature channels, yet differ in observation unit, candidate
mechanisms, and objective function. A winner in one family must not be converted
into a winner in the other by comparing rank numbers, likelihood values, or
pattern errors.

The register is a reproducible guardrail against that temptation. It reports
what each family supports **within its own declared comparison**, what both
families reject, and what remains unidentified.

## Analysis families

| family | observation unit and objective | candidates compared | essential limitation |
|---|---|---|---|
| Source-level multichannel | 17 outcrossing summaries, 7 bagging rows, 6 flower-length rows, and declared residual/error models; ranks restricted evolutionary scenarios by source-level compatibility | `ardens_bridge_loss`, `small_bee_substitution`, `body_size_only`, `environment_only` | Has no explicit `isolation_order` scenario; marginal compatibility is numerically fragile when importance-sampling ESS is low |
| Island-stage pattern | island-level composite of outcrossing, bagging, and flower-length signal; compares deterministic stage benchmarks by mean absolute error | `pollinator_hierarchy`, `environment_only`, `isolation_order` | Does not retain source-row likelihoods, within-island variation, an occupancy model, or a causal demographic process |

These are therefore **not** two estimators of one identical model.

## Current outputs

The current source-level analysis ranks `ardens_bridge_loss` first in its
restricted scenario family. The profile optimizer also places it first, and it
remains first in each leave-one-channel-out run. However, the associated
observation-scale sensitivity sweep reports very low importance effective sample
sizes: the bridge scenario has rank-one fraction 1.000 but a minimum ESS near 1
and median ESS near 2, with warnings in every tested cell. Rank direction is a
useful diagnostic; the size of its marginal-compatibility advantage is not yet
numerically resolved.

The current deterministic stage-pattern analysis instead ranks
`isolation_order` first (MAE 0.1252), `pollinator_hierarchy` second (MAE
0.1719 in the locked coding), and `environment_only` third (MAE 0.3390). When
five non-mainland *Bombus ardens* non-report/no-effort states are varied across
all 32 logical context codings, `pollinator_hierarchy` remains rank 2 in every
configuration. This does not establish an isolation mechanism; it shows that
the low-dimensional island-order benchmark fits the currently locked composite
signal more closely than the current bridge benchmark.

## Claims that can be stated now

### Supported across both current families

> The particular temperature–precipitation proxy gradient currently implemented
> is not the leading stand-alone explanation for the available mating-system,
> autonomous-reproduction, and flower-size channels.

This is a statement about the implemented `environment_only` models. It is not
a general claim that environment plays no role.

### Conditionally supported only within the source-level scenario family

> Among the currently declared source-level evolutionary scenarios,
> `ardens_bridge_loss` is the most compatible region for the retained direct
> literature summaries; the numerical magnitude of that preference requires
> stronger integration because importance-sampling ESS is low.

This is not yet a symmetric comparison against a source-level island-order
alternative.

### Conditionally supported only within the stage-pattern benchmark family

> For the current island-level composite signal, the ordered-island benchmark is
> closer than the current bridge hierarchy benchmark.

This is not a causal claim that geographic isolation drove the observed traits.

## Claims that remain blocked

- Nectar-guide or spot loss, its direction, and its selective mechanism: no
  island-resolved, geographically verified and blind-reviewed guide/spot data
  enter either analysis.
- Historical *B. ardens* occupancy, extinction, or colonization: a non-report in
  the historical rate table is not an absence observation, and the uncertainty
envelope is not an occupancy model.
- Pollination effectiveness: positive visitor-rate rows are availability/context
  evidence, not per-visit pollen deposition, seed siring, or fitness evidence.
- A dated evolutionary sequence or demographic transition: neither analysis is a
  historical reconstruction.

## The decisive next comparison

The next analysis must place the competing explanations on the **same
observation scale**. The minimal analytic move is to add an explicit
`isolation_order` scenario to the source-level model family, with the same
source-level likelihoods, residual terms, and numerical diagnostics used for the
existing scenarios. That will test whether island order still wins after
source-level uncertainty is retained, or whether the apparent stage-level
advantage depended on collapsing records into a simple island signal.

In parallel, the field/data move is to obtain island-matched contemporary:

1. blind-reviewed nectar-guide/spot phenotype measurements;
2. calibrated camera visitation and legitimate-handling measurements;
3. reproductive outcomes that separate autonomous assurance from outcrossed
   contribution; and
4. enough repeated effort to model pollinator detection rather than treating a
   non-report as absence.

## Register output

```bash
python scripts/build_model_result_register.py \
  --source-level artifacts/source_level_island_analysis.json \
  --profile artifacts/source_level_profile.json \
  --sensitivity artifacts/source_level_sensitivity.json \
  --stage-pattern artifacts/pollinator_hierarchy_counterfactual.json \
  --ardens-envelope artifacts/ardens_nonreport_envelope.json \
  --output-json artifacts/model_result_register.json \
  --output-csv artifacts/model_result_claims.csv \
  --output-md artifacts/model_result_register.md
```

The generated CSV is a claim registry, not a source of new evidence. It exists
so manuscript prose, slide claims, and future analysis branches can be checked
against the same explicit boundaries.
