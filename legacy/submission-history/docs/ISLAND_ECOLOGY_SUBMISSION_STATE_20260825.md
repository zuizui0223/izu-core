# Island ecology submission state

Updated: 2026-08-27

## Current state

The Chapter 2 **scientific model reassessment is complete**, and the model-side route is now a **Research Article candidate centered on conditional response geometry**.

The Chapter 2 Research Article is **scientifically assembled but not yet submission-ready**. Response geometry, conditional-WHY diagnostics, claim/evidence alignment, figures and tables are complete. Actual submission remains blocked by author-supplied identity metadata and declarations, followed by a successful fail-closed bundle build.

The controlling documents are now:

- `docs/CURRENT_EVIDENCE_STATE.md` for the canonical empirical claim boundary;
- `data/design/active_development_mainline.json` for executable programme state;
- `data/design/manuscript_reassessment_gate_20260826.json` for the Chapter 2 manuscript gate;
- `docs/CHAPTER2_SCIENTIFIC_GATE_RUN_20260827.md` for the completed model reassessment;
- `docs/CHAPTER2_MANUSCRIPT_REASSEMBLY_DECISION_20260827.md` for the manuscript restart boundary;
- `docs/CHAPTER1_CHAPTER2_HOW_WHY_AUDIT_20260827.md` for the cross-chapter claim audit;
- `data/results/chapter2_conditional_why_diagnostics_frozen_20260827.json` for the added fixed-design diagnostics;
- `docs/ISLAND_ECOLOGY_RESEARCH_ARTICLE_ACTIVE_DRAFT_20260827.md` for the active manuscript.

Historical Journal of Ecology drafts remain provenance only and must not be submitted or hand-repaired as the active manuscript.

## Completed scientific gate

The recovery route specified after the 2026-08-26 critique has now been executed without retuning to the outcome.

- Matched response geometry: 41 of 96 pollinator-community realizations showed mixed signs across starting positions; the mean geometry was also mixed-sign, with sign changes around 0.30–0.35 and 0.65–0.70 on the synthetic starting-trait axis.
- Joint parameter design: 16 of 48 fixed Latin-hypercube points showed mixed mean response geometry, while 22 were all-positive and 10 all-negative.
- Local context: 737 lineage contrasts showed at least one sign change across the declared filtering envelope; median first sign-change strength was 0.40.
- Autonomous assurance: among 580 eligible baseline declines, no sign rescue occurred from 0.5× through 4×; upstream effective service remained invariant. Assurance therefore remains a magnitude attenuator rather than a sign-rescue branch.
- Fixed-surface regime diagnostic: the additive 10-parameter model explains 61.10% of fixed-design variation in negative trait-grid fraction. Partner loss and arrival are the largest signed coefficients; regime contrasts also implicate saturation, trait adjustment and replacement penalty. This is boundary diagnosis within the declared design, not causal parameter selection.
- Starting-position × community decomposition: community realization accounts for 80.17% of baseline total sum of squares, the non-additive remainder for 17.64%, and starting position for 2.18%. The one-observation-per-cell remainder combines interaction and simulation noise.
- Filtering directionality: sign changes are bidirectional but asymmetric. At every non-zero filtering strength, positive baselines cross to non-positive more often than negative baselines cross to non-negative.

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

## Chapter connection and claim ceiling

Chapter 1 establishes where contrasting island states and response vectors are observed. Chapter 2 asks how a common broad perturbation can propagate differently across already-established lineages and why those responses differ conditionally.

- **HOW:** matching, local filtering and reproduction form the propagation architecture.
- **Proximal WHY:** the realized consequence depends on starting functional position, community realization and local filtering.
- **Ultimate WHY:** not answered here. Chapter 2 does not explain why a regional species pool, island interaction environment or lineage starting state arose, and no Chapter 1 region is assigned to a Chapter 2 synthetic regime.

## Required before actual submission

1. Supply final author order, affiliations, corresponding-author details and optional ORCIDs.
2. Supply acknowledgements, funding, author contributions, inclusion statement and conflict-of-interest text.
3. Approve the explicit submission declarations.
4. Run the submission builder successfully and retain its validation report.

## Submission builder status

The submission bundle machinery continues to **fail closed**, now against the active post-reassessment manuscript, frozen scientific identities and author-supplied metadata. The historical reassessment gate remains provenance; it does not route historical drafts into the current package.

## Fallback

If later editorial revision would require blocked empirical or ultimate-WHY claims, retain the present conditional claim ceiling rather than promoting synthetic design frequencies or comparative examples into field validation.
