# Figure 3 B–C: original one-locus native trace archive source admission

**Date:** 2026-10-15. **Scope:** archived original dataset and descriptive figure-source verification only. No new Model3 biology, simulations, inference unit, or external deposit.

## Original immutable source and archived claims

The existing `scripts/run_model3_mutation_memory.py` implemented a one-locus (investment I only) history diagnostic. Model state `X=A=0.5` was fixed, 200 initial updates with visitors present or absent were followed by 800 identical-environment updates. Two capacities (K48, K192), mutation probabilities (0, 0.01) and **eight original demographic seeds 6101–6108** generated 64 native finite-population NPZ output cases. The present/absent environmental treatments are **two fixed visitor-history sequences**, not 128 independently generated visitor environments.

Its preserved original source ZIP is `data/results/model3_mutation_memory_20261004.zip`; the recorded original raw archive SHA-256 in **both** committed readouts is `1bb184ed451f4dec1eadd20562cdc9adb3e3b6f615b94646d024154633b7ad79`:

- `data/results/model3_mutation_memory_20261004.json` records the means at t200/t400/t1000, separate finite and density records, original source-code hash and archive digest;
- `data/results/model3_mutation_variability_20261005.json` records all **64 original native case NPZ SHA-256 strings**, eight-repeat values for all 16 displayed panel B/C estimates, and descriptive bootstrap intervals (seed 5102026, 5,000 resamples);
- the embedded `point_kernel_and_abm/manifest.json` records original native case NPZ hashes and source identity.

**The existing `raw_archive_verified` label describes an earlier source audit.** This PR independently reopens the binary ZIP in CI and reproduces the complete Figure 3 B–C plotted values from its original NPZ traces. Treat this as a *targeted admission of an authentic native-trace archive* only when the exact-head raw-byte CI test passes, not merely because its expected digest is written in metadata.

## Recheck contract

The new read-only `scripts/verify_chapter2_figure3_onelocus_original_raw_20261015.py`:

1. Reads unchanged original ZIP bytes and compares their SHA-256 to both independently committed JSON readouts and the fixed original hash.
2. Performs **full ZIP CRC**, duplicate/path-safety checks and verifies embedded source manifest hashes for all 64 raw `point_kernel_and_abm/abm_n{48,192}_u{0.0,0.01}_s{6101..6108}_{present,absent}.npz` files.
3. Reopens each NPZ in `allow_pickle=False`, rejects missing/nonfinite traces and censuses, requires a complete **1,001 × 4 annual trait/census trace**, and recomputes all eight native individual replicate values for `I` allele count at t1000 and investment change from t900 to t1000.
4. Recalculates **all 16 panel B/C means and descriptive 95% repeat-bootstrap intervals** with the original 5,000 resamples and checks identity against the frozen 2026-10-04 and 2026-10-05 source data within `1e−13`.
5. Reports `original_1001_census_trace_values_verified=true`, but explicitly `genetic_pedigree_complete_for_all_censuses=false`. Having the annual trait trace and snapshots at 0, 200, 400, 1000 is **not** having annual parentage or full diploid genetic states at each census.

The source archive is **distinct** from both the Figure 3A prospective zero-mutation **128-history** bridge (17 original endpoint ZIPs; original full annual genomes runner-local) and the separately published Q3 original-birth-mutation **3/32, 2/32** experiment in SI S7. They cannot be added together as independent pollination histories.

## Admission status and next gate

- **No archive bytes altered** and no source output overwritten. CI test invokes the validator directly from the Git-tracked archive; any unreadable/missing/mismatched ZIP fails.
- Passing CI means the one-locus original NPZ source traces and Figure3 B/C **numerical derivations** are available in the GitHub tree at the audited SHA, not that an external DOI repository has accepted them.
- The active Letter's 143-word abstract, 4,995-word anonymous body, Q1/Q2/Q3/Q4 scope, and Figure3 pixels remain unchanged.
- **Issue #436 remains open**: source coverage for all SI S1–S33, actual Zenodo permissions/authorship/access/license/version, all original raw cohorts, external upload and independent cross-host re-download require separate authorization and verification; no public DOI exists.

Re-run without numerical experiments:

```bash
python -m scripts.verify_chapter2_figure3_onelocus_original_raw_20261015 \
  --out /a/new/output/figure3_one_locus_original_source_audit.json
pytest -q tests/test_chapter2_figure3_onelocus_original_raw_20261015.py
```
