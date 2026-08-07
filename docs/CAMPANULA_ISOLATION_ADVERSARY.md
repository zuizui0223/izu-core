# Campanula mainland-isolation adversary

## Question

Can the current three source-locked *Campanula* response channels be reproduced by a simple continuous mainland-isolation gradient, rather than by the staged response profile?

This is the next geographic adversary after the existing climate-PC1 audit. It is deliberately narrower than a full environment/history model.

## Data boundary

The analysis uses:

- `data/inoue_literature_island_traits.csv` for the adopted island-side flower length, multilocus outcrossing interval midpoint and bagged capsule-set proportion;
- `data/design/izu_regime_scaffold.csv` for the frozen mainland geographic anchor and island coordinate seeds.

The Honshu trait row is **not** assigned the mainland-anchor coordinate. Its flower-length measurement context is not the same as the geographic anchor. All response fits are therefore island-only, beginning with Oshima.

Great-circle mainland distance is a geographic-isolation surrogate. It is not colonisation-path length, gene flow, island age, habitat similarity or demographic history.

## Why isolation is a serious adversary

The geography/history alternative is not included as a straw man. An independent population-genetic study of *Weigela coraeensis* across Honshu and the Izu Islands (Yamada & Maki 2012; DOI `10.1111/j.1365-2699.2011.02634.x`) analysed 349 mainland and 504 island individuals. Its abstract reports that island genetic diversity decreased with distance from Honshu and discusses repeated founder effects during north-to-south inter-island colonisation plus stepping-stone dispersal. This does not establish the same process in *Campanula*, but it shows that mainland isolation and demographic history can covary strongly with the same island sequence and therefore deserve an explicit competing model.

## Candidate shapes

Each channel is compared with the same low-parameter candidates:

- `null`;
- `island_order_cline`;
- `mainland_distance_cline`;
- `oshima_to_toshima_step`.

Composite diagnostics additionally compare:

- one island-order cline for all channels;
- one mainland-distance cline for all channels;
- an order-based two-stage hybrid: flower size and outcrossing follow island order while autonomous capacity takes the Oshima-to-Toshima step;
- a distance-based two-stage hybrid with mainland distance substituted for island order in the two continuous channels.

## Why this distinguishes axes

The frozen coordinate scaffold does not make mainland distance equivalent to north-to-south order. In particular, Toshima is slightly closer to the mainland anchor than Oshima, while it is the immediate post-Oshima second-boundary island. The second boundary can therefore be tested against a continuous isolation surrogate rather than being guaranteed by construction.

## Interpretation

A distance model that fits well would strengthen geographic isolation/demographic history as an alternative explanation. A poor distance model does **not** reject all geographic or historical mechanisms: stepping-stone connectivity, island area, volcanism, source-population identity, habitat and genetic founder history remain viable adversaries.

Likewise, superior fit of the predeclared step for autonomous capacity does not identify historical *Bombus* loss as the cause. It establishes only that the observed island-side response is difficult to approximate with this particular continuous mainland-distance axis.

Run:

```bash
python paper/run_campanula_isolation_adversary.py
```

Outputs are written to `artifacts/campanula_isolation_adversary/` and uploaded by the `Campanula isolation adversary` workflow.
