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

## First completed acquisition

Workflow run `29403095838` completed successfully against the pinned source. The
full products are available in the `izu-public-data-audit` artifact, while the
small audit tables are committed under `data/public/izu_occurrence_audit/`.

Current counts are:

| island | occurrence records | raw species labels | datasets |
|---|---:|---:|---:|
| Hachijojima | 3,991 | 469 | 45 |
| Izu Oshima | 2,392 | 439 | 36 |
| Mikurajima | 1,186 | 260 | 10 |
| Miyakejima | 1,177 | 282 | 18 |
| Kozushima | 691 | 206 | 9 |
| Niijima | 441 | 173 | 10 |

Across the six islands, the effort table contains **9,878 occurrence records**.
The species aggregation retains **9,795 records** assigned to **1,829
island-species rows** and **863 distinct raw species labels**. The 83-record gap is
reported explicitly rather than hidden; it represents records not assigned to a
retained non-empty species row or otherwise excluded by the upstream species
aggregation.

Among the 863 labels, 54 occur on all six islands and 457 occur on only one of the
six. These figures describe the occurrence snapshot, not endemism or true island
restriction. Pairwise candidate-flora Jaccard similarity ranges from about 0.230
(Hachijojima-Niijima) to 0.349 (Kozushima-Niijima).

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

The observation process is highly uneven. For example, the snapshot is dominated
by preserved specimens on Hachijojima and Mikurajima, while Oshima has a larger
human-observation component. Coordinate uncertainty is also heterogeneous. These
terms must enter any occupancy or boundary-crossing analysis.

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
