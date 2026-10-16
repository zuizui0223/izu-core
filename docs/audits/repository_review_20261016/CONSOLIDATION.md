# Approved consolidation: source-record comparison

The two original F1 audit entrypoints now use
`scripts/source_record_validation.py::equal_source_record`.
The shared function compares the complete dictionary/list structure, metadata,
boolean types and finite numeric values. It never writes source records.

- Focal-return audit keeps its absolute tolerance of 1e-10.
- Signed-quadrant audit keeps its absolute tolerance of 1e-12.
- Scientific arithmetic, CLI arguments and contract-specific failure messages
  are unchanged by this extraction.
- Existing CLI corruption tests remain; additional shared-boundary tests cover
  nonfinite values, boolean/number substitutions, ordering and caller tolerance.
- Frozen historical copies, model kernels and scientific result records remain
  in place. No wholesale deduplication of historical experiments was attempted.

`VALIDATION.json` and `change_manifest.json` describe the earlier review
checkpoint. `DELIVERY_VALIDATION.json` records the later consolidation test run.
This delivery is a dedicated branch push; it does not merge main or create a PR.
