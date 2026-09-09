# Izu same-block transition-linked chain — Chapter 2 primary empirical gate

## Priority

The primary unresolved empirical task is no longer another synthetic sensitivity or broader island screening. It is a **same tagged plant / same prespecified block** chain in Izu:

```text
pre-outcome plant state
        ×
block visitor richness / composition
        ↓
visitor-specific single-visit pollen deposition (SVD)
        ↓
rate-weighted effective pollen service
        ↓
open / bagged-autonomous / supplemental-outcross dependency panel
        ↓
mature fruit / mature seed
```

A population-level collage assembled from different plants or different temporal blocks does **not** count as the transition-linked bridge.

## Why this is the bridge from the synthetic hierarchy

The current synthetic result separates:

1. **coarse regime placement** — realized richness materially changes the ensemble mean regime;
2. **branch identity** — realized composition interacting with plant starting state generates substantial branch contingency;
3. **finite-community realization** — deterministic mean-field removes branch heterogeneity, while finite realized communities retain it over a broad intermediate range.

The Izu field programme now maps those objects to measurements rather than synthetic labels:

| Synthetic object | Izu field counterpart | Guardrail |
|---|---|---|
| realized richness | block-level observed visitor richness with monitored flower-hours and zero-visit windows retained | no richness claim without effort |
| realized composition | visitor-group composition and, where controlled, SVD-weighted effective-service composition | visitor occurrence is not effectiveness |
| starting state | pre-outcome floral geometry / functional position on the same tagged plant | downstream phenotype cannot be back-filled as starting state |
| interaction service | visitor-specific SVD and rate-weighted effective pollen delivery | no adjusted SVD without no-visit controls |
| dependency | open vs bagged-autonomous vs supplemental-outcross response on the same plant | autonomy, self-compatibility and realized selfing remain distinct |
| branch outcome | plant-level dependency and mature-seed response conditional on block exposure | no synthetic sign label is imposed on field data |

## Strict unit

The strict linkage unit is:

```text
block_id × plant_id
```

`block_id` is fixed before reproductive outcomes are known and identifies one population/site/time exposure window. It cannot be split, merged or moved after inspecting SVD, dependency or seed outcomes.

The existing `population_id`, `field_event_id`, `island_id`, `site_id`, `plant_id` and `flower_id` remain unchanged. The block manifest sits above the existing field files rather than replacing their schemas.

## Structural admission

A **full-chain plant** requires, within one predeclared block:

1. same tagged plant in the dependency registry;
2. pre-outcome geometry for that plant;
3. usable observation effort attached to that plant, including retention of zero-visit windows in the block denominator;
4. at least one linked single-visit SVD assay;
5. at least one no-visit SVD control on the same plant/block;
6. all three core treatments on flowers of the same plant:
   - `open_pollinated`;
   - `bagged_autonomous`;
   - `supplemental_outcross`;
7. terminal analyzable outcomes for the core treatments;
8. every `mature_fruit` treatment linked through `fruit_id` to a mature-seed count.

At least one full-chain plant opens **structural completion only**. It does not open confirmatory inference.

## Primary empirical hierarchy

### H1 — richness-like exposure sets the coarse real-world regime

Estimate block visitor richness only with the explicit observation denominator. Ask whether richness-like exposure explains the mean level of effective service and downstream reproductive response across independent blocks/plants.

This is the empirical counterpart of synthetic richness-sensitive regime placement. It is not a claim that raw observed species count is a causal ecological richness effect.

### H2 — composition × plant state determines residual branch identity

After accounting for richness-like exposure, test whether effective-service composition interacts with pre-outcome plant state to explain residual dependency/seed response.

This is the direct empirical counterpart of the synthetic `starting state × realized composition` branch term.

### H3 — transition-linked propagation

Test the linked chain:

```text
visitor exposure
    -> SVD / effective service
    -> reproductive dependency / pollen limitation
    -> mature seed
```

The primary value is that all links are measured in the same block and tagged plant panel. Association across unrelated publications, islands, seasons or plants does not substitute for this chain.

## Outputs of the audit

`python scripts/audit_izu_transition_linked_chain.py ...` writes:

- `plant_chain_readiness.csv` — same-block/same-plant channel completion;
- `block_chain_readiness.csv` — block richness/composition readiness and number of full-chain plants;
- `block_exposure_by_visitor_group.csv` — monitored effort, visit rates, SVD background adjustment and effective-service composition;
- `summary.json` — whether a real transition-linked block has actually been observed.

## What remains statistical after structural completion

Structural linkage is not enough. Confirmatory inference remains closed until the existing pilot/precision workflow establishes:

- independent-plant dispersion;
- repeated temporal/site blocks;
- biologically meaningful precision goals fixed independently of the observed effect;
- adequate variation in richness and composition for the hierarchical terms;
- explicit loss/damage/pending accounting.

The confirmatory model should retain the hierarchy rather than flatten it into island-level means. Plants are nested within blocks; flowers/visits are subsamples within plants/blocks.

## Claim ceiling

Passing this gate would support a contemporary Izu statement of the form:

> variation in visitor richness/composition is linked, within prespecified local exposure blocks, to visitor-specific pollen delivery and to plant reproductive dependency/seed response, with branch structure evaluated relative to plant starting state.

It would **not** by itself identify:

- historical *Bombus* loss as the cause of the Campanula transition;
- historical evolutionary selection;
- a causal Oshima–Toshima boundary;
- a universal island-syndrome effect;
- natural prevalence of the synthetic branch classes.

Those claim boundaries remain unchanged.
