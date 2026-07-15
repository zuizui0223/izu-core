# Campanula guide-source audit — 2026-07-15

## Verdict

The guide values currently transcribed in `izu-core` are **exact copies of the
locked source table**, but they are **not final reviewed estimates**.

The correct evidence status is:

```text
exact transcription of an initial automated segmentation summary
+ provisional direction evidence
- not a reviewed plant-level effect estimate
```

## Locked source

- repository: `zuizui0223/shimahotarubukuro`
- commit: `6343d152a743c240348c736baf5c65768c9b7020`
- table: `results/per_island_summary.csv`
- blob SHA: `822fb14d8bb7cc481800d58be503eb9308687304`
- operational trait: detected strict-purple pigment pixels divided by segmented
  corolla pixels, multiplied by 100

The source script uses flattened 300-DPI corolla scans. Purple pigment is
localized with a CIELAB `a* - b*` index. Island values are arithmetic means of
per-corolla `guide_cov_pct` values. The `guide_present` threshold is 0.5%.

## Exact transcription check

The locked source table and
`data/predictive_meta/campanula_guide_scan_summary.csv` agree on all five island
rows:

| island | n corolla | locked mean guide coverage |
|---|---:|---:|
| Oshima | 88 | 28.39% |
| Toshima | 63 | 5.27% |
| Niijima | 35 | 12.15% |
| Shikinejima | 5 | 2.00% |
| Kozushima | 18 | 4.31% |

Thus the transcription and the arithmetic equal-island contrast are correct for
that locked table.

## Why the values are not final

The source repository is now 92 commits beyond the locked commit. Later work
added:

- sheet-by-sheet raw-scan QC;
- reviewed corolla masks and split/exclusion corrections;
- improved ruler/orientation handling;
- a two-stage purple-spot detector;
- an orange-rejecting micro-stipple branch;
- a separate oxidised-inclusive guide measure;
- reviewed per-sheet numeric outputs.

The old `results/per_island_summary.csv` still has the same blob SHA as at the
locked commit and has not been regenerated from those reviewed outputs.

A concrete mismatch is Shikinejima: the locked table reports five corollas,
whereas the reviewed sheet output retains six. The reviewed strict-purple values
range from 0.042% to 11.621%, and one corolla rises to 23.544% only in the
separate oxidised-inclusive trait. This shows both that the sampling rows changed
and that strict-purple coverage cannot be silently treated as total historical
guide pigment on degraded material.

## Biological interpretation boundary

`guide_cov_pct` is an operational **purple-pigment coverage** measure. Calling it
"nectar guide" is a morphological interpretation based on the location/pattern
of the purple markings. It does not by itself demonstrate:

- that visitors use the markings as a guide;
- that the markings affect pollen transfer or reproductive success;
- that Bombus loss caused their change;
- that strict-purple loss equals total pigment loss after preservation;
- or that corollas are independent evolutionary replicates.

The old summary is also corolla-weighted. The documented sampling unit is plant,
with one to two corollas per plant, but plant IDs and exclusions were not fully
resolved in the locked island summary.

## Required replacement analysis

Before the guide channel is restored as a final focal calibration:

1. combine only reviewed per-sheet outputs;
2. resolve exclusions, merged/folded corollas, and plant IDs;
3. average multiple corollas within plant before island aggregation;
4. report strict-purple and oxidised-inclusive coverage as separate traits;
5. report island n at both plant and corolla levels;
6. quantify preservation sensitivity and leave-one-island-out direction;
7. version a new channel contract rather than silently overwriting v1.1.
