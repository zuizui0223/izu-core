# Izu public-data acquisition

## Purpose

This acquisition creates the first concrete occurrence-based input for the Izu
regime-transition programme. It belongs in `izu-core`; the global `island`
repository is used only as a pinned upstream data source.

## Pinned source

The source lock is `config/izu_public_data_source_lock.json`.

- repository: `zuizui0223/island`
- commit: `77417f18e713f6eff9567f21ba338f07665fe2bb`
- occurrence product: `island_species_occurrences.csv.gz`
- observation-effort product: `island_observation_effort.csv`

The immutable commit and upstream blob SHAs are retained in every generated
provenance file.

## Current exact-island scope

The first acquisition covers the six frozen polygons already available upstream:

- Izu Oshima
- Niijima
- Kozushima
- Miyakejima
- Mikurajima
- Hachijojima

Toshima, Shikinejima, and Aogashima are not silently approximated by bounding
boxes. They remain a separate supplemental exact-polygon acquisition task.

## Generated products

Running

```bash
python scripts/acquire_izu_public_data.py \
  --source-lock config/izu_public_data_source_lock.json \
  --output-dir artifacts/izu_public_data
```

writes:

- `izu_island_species.csv.gz`: exact-island occurrence-derived species rows;
- `izu_island_effort.csv`: island-level record, species, dataset, basis, date, and coordinate-quality diagnostics;
- `izu_species_incidence.csv`: number and identity of islands per raw species label;
- `izu_pairwise_jaccard.csv`: descriptive pairwise overlap among the six candidate floras;
- `izu_public_data_summary.json`: counts, missing scope, and interpretation limits; and
- `SOURCE_PROVENANCE.json`: pinned upstream provenance.

The GitHub Actions workflow `Acquire Izu public data` performs the real download,
runs the focused extraction test, and publishes these files as the
`izu-public-data-audit` artifact.

## Interpretation boundary

These products are suitable for data-availability auditing and later
observation-process modelling. They are not yet a native-flora matrix.

In particular:

- an occurrence is not proof of native establishment;
- non-detection is not biological absence;
- a species label does not reveal pollinator dependence;
- occupancy is not a floral phenotype; and
- the outputs cannot by themselves identify a cline, threshold, or causal loss of
  pollination service.

## Next acquisition stages

1. Add exact polygons and occurrence extraction for Toshima, Shikinejima, and
   Aogashima.
2. Normalize taxonomy and retain synonym decisions.
3. Join island flora/checklist and specimen evidence to classify native,
   introduced, cultivated, transient, and unresolved records.
4. Build effort-aware Apidae/Bombus availability products for the same island
   universe.
5. Join only source-direct reproductive and floral-trait evidence, keeping
   continuous, binary, ordinal, interaction, and occupancy domains separate.
