# Galápagos DataONE recovery route

## Purpose

The Dryad metadata API identifies the Galápagos package and its file, but public download routes can return HTTP 403 in GitHub Actions. `scripts/acquire_galapagos_dataone.py` adds a lawful alternate transport/index route through the DataONE Coordinating Nodes.

This is not a title-based substitute-data search. Admission starts from the exact Dryad dataset DOI:

```text
10.5061/dryad.0c3cn5f
```

## DOI-lock procedure

1. Query the DataONE CN Solr endpoint for exact DOI variants in `id`, `seriesId`, and package-link fields.
2. Retain only seed documents whose returned metadata explicitly contains the same canonical DOI.
3. Expand only object identifiers linked from those DOI-matching seeds through resource-map, document, series, and version relationships.
4. Exclude objects classified as metadata or resource maps.
5. Attempt download only for linked data-like objects.
6. Reject empty, HTML, error-XML, invalid ZIP, and structurally invalid XLSX payloads.
7. Save source identifiers, source checksums, local SHA-256 values, download attempts, and extraction inventories.

The output uses the existing Galápagos acquisition directory layout, allowing the same schema and network-analysis gates to run regardless of whether bytes came directly from Dryad or through a DOI-locked DataONE object.

## Allowed states

- `acquired_via_dataone`: at least one valid linked data object was downloaded;
- `dataone_objects_found_but_download_failed`;
- `dataone_doi_record_found_metadata_only`;
- `dataone_search_returned_unlocked_records`;
- `dataone_doi_not_indexed_or_unreachable`.

All non-acquired states remain transport/index diagnoses. They are never converted into a zero interaction, zero effect, missing species, or support for/against the biological hypothesis.

## Claim boundary

A successfully recovered ZIP still must pass the existing Galápagos source-schema gates. A DataONE object is not accepted merely because its title resembles the target paper, and no raw network is reconstructed from the article tables when the object is absent.
