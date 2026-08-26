# Island ecology submission state

Updated: 2026-08-26

## Current state

The Chapter 2 **Research Article is not currently submission-ready**.

A scientific reassessment on 2026-08-26 identified three issues that must be resolved before submission:

1. H2 was overstated as a discovery rather than a model-specific sensitivity/decomposition result;
2. H5 qualitative state coverage was overstated as validation despite weak falsifiability;
3. the current model parameterization and local-context semantics are not exposed or stress-tested strongly enough for the headline claims.

The controlling documents are now:

- `docs/SCIENTIFIC_REASSESSMENT_AFTER_CRITIQUE_20260826.md`;
- `data/design/manuscript_reassessment_gate_20260826.json`.

These supersede the previous metadata-only submission gate.

## What remains valid

The existing simulation outputs, independent blocks, literature screen, source matrix, Dominica failure, state-separability results, manuscript drafts and reproducibility machinery remain retained as provenance.

The three-layer island-syndrome decomposition also remains the conceptual core:

- assembly / colonization filtering;
- in-situ evolution;
- post-establishment interaction response.

What changed is the role of the evidence, not the underlying stored results.

## Claim reassignment

### H2

The endpoint identity `sign(Delta reproduction) = sign(Delta service) = sign(Delta functional opportunity)` is model structure. Initial-position ablation remains informative because trait-adjustment heterogeneity is still present when initial positions are homogenized, but it only establishes dominance of initial position within the declared parameterization. `replicated_minimal_generator` is no longer a submission headline.

### H3

The local-context result is retained after semantic correction. `support_strength` is an availability/filtering stress parameter, not added beneficial support. The interesting result is bidirectional response reallocation under local context filtering.

### H4

Assurance attenuation is largely structural because assurance is implemented as a compensating route. The useful result is the distinction between magnitude buffering and sign rescue, not attenuation itself.

### H5

The 13 systems remain comparative grounding. `11/11 covered` is no longer treated as validation of generality. Dominica remains a failed specific signed-position projection.

## Active scientific gate

Before restoring submission readiness, complete a **response-geometry and parameter-robustness analysis** that answers:

- where in plant functional space a given pollinator-community change produces positive versus negative opportunity response;
- whether sign-switching persists across a broad parameter region rather than one chosen scenario;
- which perturbation parameters control the transition between one-direction and two-direction response;
- whether local context filtering changes sign robustly or only under narrow settings;
- what assurance strength is required for sign rescue.

The next manuscript must also expose the model equations and parameter values, report `5 of 12` rather than `0.4167` as a design count, remove workflow/debug prose from Methods, and clean uncited references.

## Submission builder status

The submission bundle machinery is retained but must fail closed while `data/design/manuscript_reassessment_gate_20260826.json` has status `scientific_reassessment_required_before_submission`.

Author metadata are **not** the active blocker now. The active blocker is scientific response-geometry/robustness.

## Fallback

If the response-geometry analysis does not reveal a stable, interpretable region structure, do not force the Research Article. Reframe as a conceptual Review or Mini-review around the three-layer decomposition of the plant island syndrome.
