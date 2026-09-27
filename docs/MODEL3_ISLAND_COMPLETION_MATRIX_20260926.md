# Model 3 island ecology: final requirement audit

All declared computations and reporting are complete. Numerical convergence and narrow conditional precision are **not established**; those are retained negative gate outcomes, not certified passes. Remote delivery verification is recorded separately after push. The active scientific manifest is `data/design/model3_island_v2.json`, SHA256 `0dcf6190c27f5fc9c50b07a270826932691f8c21886ff4b148c6fe299bf3135e`.

## Scientific coverage

Evidence is in `data/results/model3_island_v2_summary/summary.json`, `cells.csv`, the 70 per-condition trajectory figures, the eight-panel `ecological_comparisons` figure and the four-panel `floral_return_assays` figure (each PNG/SVG/PDF). Detailed interpretation is in `MODEL3_ISLAND_ECOLOGICAL_RESULTS_20260927.md`; numerical assessment is in `MODEL3_ISLAND_NUMERICAL_REVIEW_20260927.md`.

| Requirement | Declared cells / cases | Verified deliverable and outcome |
|---|---:|---|
| Fixed-assurance attraction returns | 16 / 2,048 | All outcross and total parental-contribution gradients and history intervals; all 16 shown in assay figure. Assurance and investment cost interact with visitation/mismatch; not realized selection or causal mediation. |
| Chronology | 5 / 1,280 | Early/late equal-duration absence and mismatch plus uninterrupted reference; same final 120 years; trajectories, occupancy and paired endpoints retained. Early absence differs from late absence. |
| Separate seed/visitor isolation | 9 / 2,304 | All 3 x 3 distance cells in heatmap and tables; distances in dispersal-scale units, not km. Assembly contrasts bundle arrivals and community histories. |
| Founding/separation | 4 / 1,024 | Empty founding 255/256 terminal occupancy; undefined initial trait baseline retained. Identical-state label controls yield identical summaries; no claim that geological histories are equivalent. |
| Fixed/evolving assurance | 7 / 1,792 | Timing, discount and cost controls retained. Disabled assurance has 0/256 survival; traits undefined. Expected reproduction and viable resident-recruit selfing have separate denominators. |
| Restoration and genetic recovery | 14 / 3,584 | Seven recovery arms and seven linked uninterrupted controls, including 2,000-year horizons. Paired trait intervals, heterozygosity, ancestry and occupancy reported. No irreversibility or mutation-load/purging claim. |
| Capacity and numerical resolution | 14 / 3,584 | Capacity 48/192/768, fixed-total/per-capita supply, all 16 grid contrasts, bias/MAE and precision reviewed. No individual grid interval is contained in the +/-0.01 tolerance; convergence unestablished. |
| Life history | 5 / 1,280 | Annual, 4/10-year adults, annual/lifetime budgets; parental-age generation intervals and trajectories. Years are not generations for overlapping adults. |
| S/C/I and prediction transport | 6 / 3,072 | Training and disjoint held-out histories, four decompositions and four transport tests; within-cell variation explicit. Occupancy decomposition undefined at zero variation. Descriptive investment ranks do not establish universal ranks. |

Total: **80 cells, 19,968 cases**; 86 summary rows include the held-out cohorts. Ordinary trajectory cells have 128 independent histories x 2 demographic repeats; assay cells have 128 histories. No outcome-selected additions.

## Implementation, execution and scientific gates

| Requirement | Evidence / disposition |
|---|---|
| Approved implementation and legacy regressions | `MODEL3_ISLAND_IMPLEMENTATION_AUDIT.md`: five independent-review findings repaired, 1,948 full-suite passes and one skip recorded. Package grew from 168 to 174 tests with continuation tests. Fresh exact-head CI is required at delivery. |
| Finite expectation versus density closure | Archived exact one-step expectation and pollen-exclusion diagnostics preserved; long-run difference not uniquely attributed to drift or added into causal percentages. Density is a discrete closure, not PDE. |
| Frozen implementation and earlier science | All 18 source hashes match the manifest; all 14 baseline hashes match `data/design/model3_island_frozen_baseline_hashes.json`, as checked by the provenance generator. |
| Prospective configuration and runtime | Exact source ZIP/runtime metadata and v2 design retained. Original runtime STOP at 15,565 cases retained; outcome-blind compute amendment executed exactly 4,403 missing cases. No scientific setting changed. |
| Complete production | `model3_island_v2_completion.json`: 19,968/19,968, no terminal stop reason. |
| State and provenance audit | `model3_island_v2_audit.json`: passed, 19,968 cases checked, 80 first-per-cell exact replays. This is not field validation. |
| Precision | Four of 70 trajectory rows meet conditional target, 64 fail, two undefined. Occupancy bound half-width 0.12004 meets the declared 0.125 planning target, not the stricter 0.02 numerical tolerance. |
| Effective exposure | Implemented and tested covariance-based diagnostic; production histories do not supply an admissible stationary covariance estimate. Numerical k is not evaluable, never substituted with old history pooling. |
| Figures | Main eight-panel figure and all-assay figure visually inspected; source summary hashes and artifact byte hashes recorded. Per-cell supplements preserve all trajectory rows. |
| Results and discussion | Nine scientific families discussed, including non-support, extinction and limitations. Q1 only motivates; no four-region fitting or 42-island projection. |
| Novelty | Primary precedents reviewed in `MODEL3_NEAREST_PRECEDENTS_20260926.md`. Generic selfing rescue, history dependence and individual/density differences are not claimed as first discoveries. Novelty priority unproven. |
| Reproducibility | Exact source/runtime, design, complete compact results, all 19,968 case/array hashes and generated artifact hashes delivered. Raw NPZ remain local and are not represented as remotely deposited. |
| Publication claim ceiling | Completed computational experiment, not certification of continuous convergence, field calibration or publication-ready quantitative evolutionary magnitudes. |

## Regeneration

Use the recorded runtime and exact source bytes. Run the audit and summary commands in `MODEL3_ISLAND_DELIVERY_AUDIT_20260927.md`, then both `scripts/plot_model3_island_ecology.py` and `scripts/plot_model3_island_assays.py`, then `python -m scripts.build_model3_island_provenance`. Rebuilding raw simulations is a new execution; the historical compute amendment is not an unlimited reset mechanism.

The scientific task was to execute and assess the prospective comparisons, not force support. Negative numerical and precision assessments close those tests with restricted claims; they do not justify tuning until the preferred result appears.
