# Chapter 2 figure regeneration

Updated: 2026-09-27

## Active command

Install the repository development environment and run:

```bash
python -m pip install -e '.[dev]'
python scripts/generate_chapter2_unified_model3_figures.py
```

The generator fails closed unless all four current source objects are available and valid:

- `data/results/model3_unified_reduction_audit_frozen_20260927.json`;
- `data/results/model3_ch2_bridge_prospective_frozen_20260927.json`;
- `data/results/model3_island_v2_summary/review_compact.json`;
- `data/results/chapter2_unified_model3_real_island_projection_20260927.json`.

It writes a regenerated figure-input receipt to:

`data/results/chapter2_unified_model3_figure_inputs_20260927.json`.

## Main figures

The active journal-facing figure set is:

1. **Figure 1 — from pollination ecology to realized floral evolution**  
   `fig1_unified_model3_nested_levels.svg/png`  
   Functional matching and finite pollen transfer → reproductive selection → Mendelian inherited expectation → finite-population realization. The left panel shows how starting plant state changes the reproductive return to floral investment.

2. **Figure 2 — prospective 24,576-case isolation bridge**  
   `fig2_model3_prospective_isolation_bridge.svg/png`  
   Compares natural near/far assembly, annual response-blind richness matching, eight-history visitor pooling and fourfold plant-capacity increase for finite ABM and deterministic density. This figure carries the final old-Chapter-2 control closure.

3. **Figure 3 — history, assurance and connectivity**  
   `fig3_model3_history_assurance_connectivity.svg/png`  
   Shows chronology under a common final environment, assurance-dependent persistence, and distinct seed versus pollinator connectivity routes.

4. **Figure 4 — real-island A/B/C confrontation**  
   `fig4_real_island_abc_confrontation.svg/png`  
   Summarizes source-locked propagation, branching, buffering, counterdirectional and unresolved natural response modes, and identifies the inherited longitudinal B layer as the main empirical gap.

## Frozen values that must be reproduced

The current main-figure generator is tied to the following frozen results:

- controlled fixed-composition branch capacity: starting state can reverse reproductive-selection direction;
- prospective bridge verified denominator: **24,576 cases / 128 histories / 16 execution shards**;
- natural far-minus-near inherited-investment mean:
  - finite ABM **-0.1446**;
  - deterministic density **-0.4510**;
- annual richness matching reverses the mean:
  - finite ABM **+0.0333**;
  - deterministic density **+0.0338**;
- finite-ABM mixed histories after richness matching: **68/128, 59/128, 18/128** at deadbands 0, 0.01 and 0.05;
- eight-history visitor pooling: **0/128 mixed** in both model forms at all declared deadbands;
- plant capacity 48 → 192: finite-ABM mixed histories **12/128 → 1/128** at deadband 0;
- common-final-environment chronology: early visitor loss, late visitor loss and uninterrupted histories retain different inherited-investment endpoints;
- real-island confrontation: 14 evidence-rich system layers across 12 geographic clusters, used as structural confrontation rather than prevalence estimation.

## Supporting-information role of legacy figures

The former response-geometry figure stack remains provenance / Supporting Information only:

- exact realized-richness matching;
- synthetic `k` pooling;
- response-rule sensitivity;
- historical S/C/I decomposition;
- community-mean asymptotic calculation;
- old metadata-readiness and Izu structural-audit visualizations.

Those figures must not be routed back into the main manuscript as a second biological mechanism.

## Inference boundary

The main figures are synthetic mechanistic summaries plus a source-locked natural confrontation. They do **not** imply:

- natural calibration of Model 3 time, distance, investment or extinction frequency;
- a field species-richness effect equal to the annual thinning intervention;
- that pooled visitor histories represent island number or lifespan;
- that deterministic genotype density is a continuous diffusion PDE;
- natural prevalence from the 14-system response-mode counts;
- assignment of Chapter 1 regions to Model 3 parameter cells;
- historical *Bombus* causation.

The active manuscript captions are authoritative if this documentation and the manuscript ever diverge.
