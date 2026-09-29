# Effective-dependency field preflight

Run a preflight before treating any CSV folder as the first empirical Issue #91 pilot bundle.

The preflight distinguishes five states: `required_files_missing`, `schema_invalid`, `template_only_no_field_rows`, `partial_required_channels`, and `candidate_real_field_bundle_present`.

The key rule is simple: committed header-only templates are **not empirical data**. A candidate real bundle requires all six required channels (plants, effort, visits, SVD, treatments, fruits) to be present, readable, schema-compatible with their committed templates, and non-empty.

A candidate state still opens no scientific gate. Freeze the exact raw bytes next, then run the existing linkage and admission audits. A partial bundle may be frozen as a versioned collection checkpoint, but it must not be treated as a structurally complete panel.

Preflight does not establish linked IDs, usable observation effort, valid SVD controls, analyzable reproductive outcomes, independent plant replication, measurement reliability, historical causation, or cross-lineage evidence.
