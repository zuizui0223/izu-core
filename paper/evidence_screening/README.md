# Expanded evidence screening for the Izu flora

## Purpose

The existing 156-species table is an entomophilous, gradient-spanning analysis cohort. It is not the upper limit of the literature search. The broader GBIF island-facet probe reported 319 mainland + >=2-island plant species, 289 species on >=3 islands, and 113 on >=5 islands. This directory provides the audit trail for rebuilding that broader universe and screening it without mistaking distribution records for trait data.

## Cohorts are nested, not interchangeable

| Cohort | Inclusion | Role | Never used as |
|---|---|---|---|
| U0 distribution universe | all accepted mainland + >=2-island vascular plant candidates | searchable parent universe and missingness audit | a trait-response dataset |
| U1 trait-search universe | U0 species with flowers, an island taxon, or a plausible mainland comparator | literature, flora, image and record search | evidence that a trait changed |
| U2 comparable records | a source has an explicit mainland--island, island--island, island taxon--mainland taxon, or time-series comparison | structured evidence extraction | a pooled effect unless the metric is compatible |
| U3 quantitative effects | source contains a recoverable mean/rate plus n and variance, or enough raw data to reconstruct them | primary random-effects meta-analysis | a substitute for missing mechanisms |
| U4 ordinal evidence | source text or blinded photo review supports a direction but no compatible effect size | ordinal/evidence-map sensitivity analysis | a numeric effect size |
| U5 shape subset | at least four ordered positions after missingness, with true island identity retained | cline/step/none and breakpoint testing | proof that a common historical cause is established |
| U6 mechanism subset | trait evidence plus independently supported pollination functional group | moderator and falsification analysis | a causal proof from group labels alone |

A record can be in several cohorts, but U4 evidence is never converted into U3 by assigning an invented variance or effect size. Occurrence/photos are not evidence of pollinator effectiveness, and absence of public records is not biological absence.

## Initial 40-species docket

`high_information_docket.csv` is the first search batch. It protects the key contrast before literature availability biases the synthesis: 30% specialist candidates, 40% generalist negative controls, 20% large-flower counter-direction candidates, and 10% non-bee/ambiguous comparison systems.

`screening_registry.schema.csv` specifies the one-row-per-source evidence record. Every retained source receives an exact query, retrieval date, source identifier, page/table/figure, trait definition, comparison design, and inclusion or exclusion reason.

## Expand from 156 to the full U0 universe

Do not append species by hand. Recreate the island-facet parent table first, retaining at least:

```text
species_key, accepted_name, family, taxonomic_status,
mainland_present, Oshima_present, Toshima_present, Niijima_present,
Kozushima_present, Miyake_present, Hachijo_present,
n_islands, total_occ, retrieval_date, source_url_or_query, source_version
```

The present 156-species file is a pilot input, not the completed search universe. Once the full table is reconstructed, make a second docket using the same protected functional-group allocation and retain the original 40-species pilot unchanged.

## Source and measurement axes

Every retained source gets both axes; do not collapse them into one confidence label.

| Source provenance | Definition |
|---|---|
| P1 | peer-reviewed paper, thesis, or original table/figure with citable page |
| P2 | museum/university bulletin, flora, official survey report, or archive with stable provenance |
| P3 | specimen/media database or geotagged public image with retained metadata |
| P4 | field-group page, individual site, or SNS record; retained only with date/location/taxon review |

| Measurement strength | Definition |
|---|---|
| M3 | compatible effect size can be reconstructed |
| M2 | direction or ordinal contrast is explicit and source-backed |
| M1 | image/text is suggestive but scale, identity, phenology, or comparison is incomplete |
| M0 | occurrence/distribution only |

Only P1/P2 x M3 enter U3 by default. P1/P2 x M2 and reviewed P3 x M2 enter U4. P4 can support lead generation or a clearly flagged D-rank sensitivity layer, never the primary numeric result.

## Required source review

For each candidate, screen Japanese and English literature, taxonomic names and synonyms, institutional repositories, regional floras, GBIF media, iNaturalist, YAMAP and eligible geotagged public images. Save the exact query, date, source identifier, page/table/figure, and exclusion reason. LLMs may retrieve and structure leads, but a human verifies each retained trait datum against the primary page or image.

## Stop rules

A source is excluded from primary effects when it lacks a valid comparison, mixes cultivation with wild populations, has an unresolved taxon/island assignment, duplicates another record, reports a non-floral display without a comparable trait definition, or cannot identify the sampling unit. Keep excluded hits in the registry with their exclusion reason; they are part of the systematic-search evidence.
