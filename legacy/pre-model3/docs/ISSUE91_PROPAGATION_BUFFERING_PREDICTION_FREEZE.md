# Issue #91 propagation / buffering prediction freeze

Frozen: 2026-08-22

## Why this exists

The comparative programme now contains propagation, buffering, branching and counterdirectional island cases. Before the first real linked *Campanula microdonta* field bundle is inspected, the Izu anchor therefore needs a frozen interpretation map.

The aim is **not** to predict the exact historical Izu sign pattern. It is to stop us from seeing the new field outcomes first and then deciding afterwards whether they were caused by dependency, assurance, network composition or effective service.

No real Issue #91 field row, pilot dispersion, SVD value, FDQ value or treatment outcome was inspected to make this freeze.

## Existing estimands only

No new composite score is introduced.

The freeze uses the already implemented field quantities:

- visit bouts / monitored flower-hour;
- background-adjusted single-visit conspecific pollen deposition (SVD);
- rate-weighted effective pollen service;
- `bagged_autonomous / supplemental_outcross` reproductive ratio;
- `open_pollinated / supplemental_outcross` reproductive ratio;
- the existing `direct_reproductive_dependency_0_1` target;
- strict proboscis-length Rao-Q FDQ when all taxon/trait gates pass.

The independent replication unit remains the **plant**. Flowers and SVD events within a plant are subsamples.

## M1 — service propagation filtered by reproductive dependency

Question:

> Does reduced effective pollen service translate into a larger open-reproduction shortfall where plant dependency is high?

Expected signature:

```text
lower effective service
    -> lower open / supplemental-outcross ratio
and the association is stronger at higher direct dependency
```

A crucial part of this hypothesis is that **visit rate and effective service need not agree**. A frequent visitor with poor SVD can create high visitation but low pollen service.

This model is weakened by repeated, well-admitted high-dependency units that maintain open reproduction despite low effective service.

## M2 — autonomous reproductive assurance buffers low service

Question:

> When effective service is low, is maintained open reproduction associated with high autonomous assurance?

Expected buffered signature:

```text
low effective service
+ maintained open / supplemental-outcross ratio
+ high bagged-autonomous / supplemental-outcross ratio
```

Supplemental outcross remains essential as the denominator control. Otherwise low fruit set could be incorrectly interpreted as pollinator limitation when the real limit is ovules, resources or general reproductive failure.

This model is weakened if open reproduction remains high under low service while the autonomous ratio is also low.

## M3 — network / service allocation

Question:

> Does visitor composition plus per-visit effectiveness change realized service beyond what visit rate or functional exposure suggests?

Expected signature:

- visitor groups differ in background-adjusted SVD;
- units with similar visit rates can have different rate-weighted effective service;
- similar FDQ or richness can still produce different effective service if realized visitor identity and SVD differ.

This is the direct Izu test of the idea suggested by the earlier network-state-sensitive matching→pollen result.

## M4 — non-assurance buffering

Question:

> Can low effective service coexist with maintained open reproduction even when autonomous assurance is low?

If the future admitted data show:

```text
low effective service
+ maintained open reproduction
+ low autonomous ratio / high dependency
```

we record **`non_assurance_buffer_or_unmeasured_filter_candidate`**.

We do **not** then rename the unknown mechanism “resource compensation”, “redundancy”, “establishment filtering”, or anything else unless an independent measurement identifies it.

This rule comes directly from the cross-system discriminator: Guaiacum and Hawaii show why one universal assurance-buffer story is too simple.

## M5 — FDQ is upstream functional exposure, not service

FDQ keeps its strict source-locked role:

```text
FDQ = Σ_i Σ_j p_i p_j |L_i - L_j|
```

It is emitted only when all positive-abundance visitor taxa are resolved and have admitted site-linked numeric proboscis traits.

The freeze makes **no universal prediction that higher or lower FDQ must increase reproduction**. FDQ may change while service or reproduction does not. A reproductive claim still requires effective-service and dependency channels.

Never:

- drop unresolved visitors and renormalize;
- substitute visitor richness/guild diversity for FDQ;
- turn a usable zero-visit window into FDQ = 0.

## Frozen interpretation table

| Future admitted pattern | Primary interpretation |
|---|---|
| low service + low open ratio + high dependency | service-limited / dependency-sensitive candidate |
| low service + maintained open ratio + high autonomous ratio | assurance-buffer candidate |
| low service + maintained open ratio + low autonomous ratio / high dependency | non-assurance buffer or unmeasured filter candidate |
| similar visit rate + divergent effective service because SVD differs | network/service-allocation candidate |
| FDQ differs but effective service and reproductive ratios do not | functional-exposure change buffered before service/reproduction |

These are qualitative signatures, not thresholded classes yet.

## Pilot is not the confirmatory test

The first real pilot may:

1. pass linkage / source-freeze / structural gates;
2. estimate between-plant SVD and treatment dispersion;
3. estimate coverage, damage, loss and pending fractions;
4. report the frozen directional signatures descriptively;
5. reveal which candidate models can actually be discriminated with the observed channels.

It may **not**:

- convert two independent plants into a confirmatory sample size;
- declare one mechanism causal;
- estimate final dependency reliability from ordinary biological repeats;
- choose a threshold because it recreates the historical Izu pattern;
- fit a cross-lineage dependency × FDQ interaction from Campanula alone.

Only after pilot dispersion is available do we lock a biologically meaningful precision target and confirmatory replication.

## Anti-leakage rules

- Do not tune to the historical Izu 8/8 matching decline or 4/4 pollen split.
- Do not select an FDQ direction after seeing reproductive outcomes.
- Keep visit rate, SVD, effective service, FDQ and dependency as distinct channels.
- Do not replace dependency with floral syndrome or corolla shape.
- Null and adverse field results are valid outcomes and do not trigger model rescue.

## What this changes scientifically

Issue #91 is no longer just “measure pollinator dependency”. It is the **highest-value direct discriminator of the multi-gate island mechanism**:

```text
functional / network environment
        -> realized effective service
        -> dependency / assurance filter
        -> reproduction
```

Because the prediction structure is frozen before field outcomes, a favorable result can genuinely strengthen the mechanism and a null/adverse result can genuinely narrow or reject it.

## Claim boundary

These are prospective mechanism signatures, not fitted predictions and not evidence that any one model is true. Historical Bombus loss, historical selection and a causal Oshima–Toshima boundary remain unidentified by the future pilot alone.
