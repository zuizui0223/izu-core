# Island Evolutionary River v1

## Purpose

Visualize island evolutionary change as a changing **space of possible ecological states**, not as an animation of individual ABM agents or sequential snapshots.

The figure should answer:

> As isolation accumulates, which interaction states remain feasible at island scale, how can local partner availability split that feasible space into alternative local channels, and how can interaction weights reorganize inside each channel?

## Visual grammar

### Horizontal axis: accumulated island constraint

Use the frozen ABM v4 `isolation_index` from 0 to 1. This is a process index, not kilometres or chronological time.

### Outer river: island-scale feasible opportunity

The river half-width is proportional to the frozen v4 `final_partner_types` gradient. The river therefore narrows monotonically as isolation removes feasible partner opportunity.

This outer envelope corresponds to:

`mainland / weak constraint -> island feasible partner pool -> strongly isolated feasible partner pool`

States outside this envelope are shown as unavailable under the current island-scale opportunity constraint. The visualization must not imply that every point inside the envelope has been empirically observed.

### Local branches: support-varying local contexts

Inside the island-scale river, show multiple local channels representing ABM v6 local partner-support subsets. These are **alternative local realizations inside the same island feasible pool**, not separate islands and not ABM individuals.

The generic v6 support-strength envelope is `0, 0.25, 0.5, 0.75`. Positive support strength can remove locally unavailable members of the island-feasible pollinator pool but cannot add partners absent from it.

Branching should be shown as a fan / braided river, not as moving dots.

### Within-channel texture: weighted realization

Use fine internal strokes or opacity modulation to indicate ABM v5 within-support interaction-weight reorganization. This layer must remain visually subordinate to support branching because Menorca falsified support-preserving reweighting as sufficient by itself.

### Lower state trajectories

Using the same frozen v4 gradient, show compact trajectories for:

- interaction diversity proxy: decreases with isolation;
- plant niche overlap proxy: increases with isolation;
- mean reproduction: not forced to decline monotonically.

These trajectories provide the ecological interpretation of the shrinking state space without turning the visualization into a conventional dashboard.

## Evidence layers

The visualization must distinguish three evidence types:

1. **Frozen directional model result** — v4 continuous isolation gradient values from `data/results/abm_v4_global_continuous_isolation_gradient.json`.
2. **Mechanism-class structure** — v6 local-support branching and v5 within-support reweighting. Generic support/weight strengths are sensitivity envelopes, not empirical estimates.
3. **Empirical falsification marker** — PR #195 showed that Menorca local weighted-architecture variation exceeded the support-preserving v5 envelope for both frozen target metrics. This motivates emphasizing support branching, but Menorca amplitudes must not be used to scale the v6 channels.

## Required labels

The primary visual should label the hierarchy explicitly:

`island feasible opportunity -> local partner availability -> realized weighted architecture`

Also label the outside region as `unavailable / excluded by current island-scale constraint` rather than `extinct`, because the model does not identify all excluded states with historical extinction.

## Prohibited visual forms

Do not use:

- agent dots moving frame-by-frame;
- TenSnap-like ABM snapshots;
- a literal island coastline drawn from imagination;
- an animation that implies isolation_index is chronological time;
- a single deterministic evolutionary path;
- Menorca target amplitudes to choose branch widths or support strengths;
- a Sankey whose width implies empirical abundance unless explicitly labeled model-derived.

## Deliverables

`scripts/build_island_evolutionary_river.py` should generate:

- `data/results/island_evolutionary_river_v1.svg`
- `data/results/island_evolutionary_river_v1.json`

The JSON sidecar should record all source paths, transformations, model-vs-empirical distinctions, and claim boundaries.

## Claim boundary

This is a visualization of a constrained evolutionary **state space**, not a reconstructed historical chronology. River width is model-derived from the frozen v4 partner-opportunity gradient; local branching is the v6 mechanism class; internal reweighting is the v5 mechanism class. The figure does not estimate when a particular island took a branch, which habitat caused a branch, or the probability of any historical evolutionary trajectory.
