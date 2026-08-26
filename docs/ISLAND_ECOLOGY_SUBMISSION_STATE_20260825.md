# Island ecology submission state

Updated: 2026-08-27

## Current state

The Chapter 2 **scientific model reassessment is complete**, and the model-side route is now a **Research Article candidate centered on conditional response geometry**.

The Chapter 2 Research Article is **not yet submission-ready**. The reason has changed: response-geometry / robustness is no longer the blocker. The remaining work is manuscript reassembly and claim/evidence alignment.

The controlling documents are now:

- `docs/CURRENT_EVIDENCE_STATE.md` for the canonical empirical claim boundary;
- `data/design/active_development_mainline.json` for executable programme state;
- `data/design/manuscript_reassessment_gate_20260826.json` for the Chapter 2 manuscript gate;
- `docs/CHAPTER2_SCIENTIFIC_GATE_RUN_20260827.md` for the completed model reassessment;
- `docs/CHAPTER2_MANUSCRIPT_REASSEMBLY_DECISION_20260827.md` for the manuscript restart boundary.

Historical Journal of Ecology drafts remain provenance only and must not be submitted or hand-repaired as the active manuscript.

## Completed scientific gate

The recovery route specified after the 2026-08-26 critique has now been executed without retuning to the outcome.

- Matched response geometry: 41 of 96 pollinator-community realizations showed mixed signs across starting positions; the mean geometry was also mixed-sign, with sign changes around 0.30–0.35 and 0.65–0.70 on the synthetic starting-trait axis.
- Joint parameter design: 16 of 48 fixed Latin-hypercube points showed mixed mean response geometry, while 22 were all-positive and 10 all-negative.
- Local context: 737 lineage contrasts showed at least one sign change across the declared filtering envelope; median first sign-change strength was 0.40.
- Autonomous assurance: among 580 eligible baseline declines, no sign rescue occurred from 0.5× through 4×; upstream effective service remained invariant. Assurance therefore remains a magnitude attenuator rather than a sign-rescue branch.

These are synthetic robustness and sensitivity results. They are not ecological prevalence estimates or empirically calibrated thresholds.

## Current Research Article claim

The defensible headline is:

> **Post-establishment plant response to pollinator reorganization is conditional rather than monotonic: response sign depends on starting functional position and realized partner context. Local interaction filtering can redirect branch identity, whereas the implemented autonomous-assurance route attenuates response magnitude without crossing the sign boundary in the tested sensitivity envelope.**

This replaces the old `replicated_minimal_generator` headline.

## Claim reassignment

### H2

The endpoint sign identity remains model structure. The manuscript should now lead with the nontrivial response geometry and its robustness across the joint parameter space, not with initial heterogeneity as a universal minimal generator.

### H3

Retain the local-context result as bidirectional response reallocation under **local availability / interaction filtering**. `support_strength` is not beneficial support.

### H4

Retain the distinction between magnitude buffering and sign rescue. The 0–4× sensitivity map found no assurance sign rescue, so assurance is a robust weak attenuator in this implementation rather than a strong alternative branch.

### H5

The 13 systems remain comparative grounding only. `11/11 covered` is not validation of generality; Dominica remains a failed more-specific signed-position projection.

## Required before submission

The response-geometry scientific blocker is closed. Before any submission bundle can be promoted, a new active manuscript must be regenerated from current canonical state and must:

1. expose the model equations and parameter values, distinguishing generic sensitivity choices from empirically motivated directions;
2. report design counts/fractions as synthetic robustness descriptors rather than natural prevalence;
3. replace beneficial-support wording with local-context / availability-filtering semantics;
4. state explicitly that assurance produced no sign rescue through 4× and is retained as magnitude attenuation;
5. remove workflow/debug/import-path/seed-search prose from scientific Methods;
6. remove H5 state coverage as validation and retain external systems only as ecological grounding/boundaries;
7. resolve uncited Lord (2015) and Méndez (2025) references;
8. reconcile every empirical statement with `docs/CURRENT_EVIDENCE_STATE.md` and the active development mainline.

## Submission builder status

The submission bundle machinery should continue to **fail closed**. `data/design/manuscript_reassessment_gate_20260826.json` now records `scientific_reassessment_complete_manuscript_reassembly_required`: the Research Article route is scientifically reopened, but no historical draft is automatically promoted to an active submission surface.

## Fallback

If a clean reassembly cannot sustain a focused Research Article without importing blocked empirical claims, use the three-layer island-syndrome decomposition as a conceptual Review/Mini-review rather than weakening the evidence boundary.
