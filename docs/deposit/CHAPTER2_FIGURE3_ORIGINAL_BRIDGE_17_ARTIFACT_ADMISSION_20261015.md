# Figure 3 panel A: original 17-artifact SHA-256 readback and endpoint reaggregation

**2026-10-15 / source original workflow [36311030639](https://github.com/zuizui0223/izu-core/actions/runs/36311030639). State: 17/17 original compact Actions archive bytes freshly read and authenticated; all eight source-derived plotted effect means independently reproduced. NO complete annual-genome raw source archive or external DOI is claimed.**

## Completed technical audit

The original [prospective source study](../MODEL3_CH2_BRIDGE_PROSPECTIVE_RESULTS_20260927.md) saved 16 `model3-ch2-bridge-shard-N` GitHub Actions ZIPs and one `model3-ch2-bridge-prospective-summary` ZIP. The [machine-pinned 17-file digest and history inventory](chapter2_figure3_original_bridge_17artifact_intake_20261015.json) identifies each asset using its exact original GitHub Actions artifact ID, original SHA-256, byte size and eight source visitor-history seeds.

- **17/17** original downloaded ZIPs matched their original GitHub Actions SHA-256 digests and passed ZIP CRC readback (16 shards + one summary).
- Every shard declares **1,536 executed and audited cases**, total **24,576 endpoint cases**, with 128 **distinct visitor histories** (`74001..74128`), eight histories per shard and eight nested demographic repeats for each of three initial I conditions.
- Each shard embeds snapshots of **20 original scientific source-code files**, and all 20 files are byte-identical across the 16 shards (the *nested ZIP containers themselves* are not byte-identical; they may encode differing container metadata/compression). All completed shards have distinct, authenticated endpoint-array audit roots.
- **Eight plotted means** were recomputed independently from the original `shard-N.json` endpoint matrices, by differencing each original matched far and near arm *within* history, initial state and demographic replicate before averaging 128 history-level means. The machine verifier checks these values against the already committed `model3_ch2_bridge_summary_20260927/summary.json` at absolute precision better than `1e−13`.

| Main Figure 3A intervention | Finite diploid ABM | Deterministic genotype-density |
|---|---:|---:|
| Native near/far visitor histories | −0.1446356879 | −0.4509830626 |
| Annual visitor-count matching | +0.0333226522 | +0.0337573408 |
| Eight visitor histories pooled | −0.2259496053 | −0.5560421533 |
| Plant capacity 192 (otherwise native) | −0.2716497209 | −0.4509830626 |

This audit reproduces the figure's finite-vs-density **descriptive source means**, not the independent causal contribution of drift, variance partitions or a stochastic expectation identity. Visitor count matching also alters visitor identity persistence; pooling alters composition and nonlinear aggregation; capacity alters density regulation.

## Crucial raw-data distinction

Every original shard states:

> `compact endpoint export after full input/receipt/array hash verification; raw trajectories intentionally remain runner-local`

The source workflow completed **24,576 runs** and asserted its input, source, receipt and array hashes at execution time, but the 17 preserved outer artifacts contain *compact terminal arrays, run manifests, status, recorded hash roots and source snapshots*, **not the full 200-census native genotype trajectories** for all paths.

Therefore the defensible claim is **“complete original terminal-export evidence independently recovered”**, *not* “full original genetic raw trajectories deposited/replayed”. This difference matters for reviewer data sufficiency and may require an explicit declared availability limitation, authorized recovery from another original backup, or independently labelled new source reconstruction. Do not silently rerun or replace the old original files.

The existing main Figure 3A compact endpoint data and the separate one-locus panels B–C **do not share** one inferential cohort. The separate original-mutation 3/32 and 2/32 study is still distinct; its original `completed_atom_abm_20261011.zip` is **not a direct plot input**. See [Figure 3 panel-source map](CHAPTER2_MAIN_FIGURE3_SOURCE_TO_DOI_AUDIT_20261015.md) (PR #559).

## Reproduction and admission

The immutable machine manifest stores the original 17 artifacts, with 16 × eight visitor history identifiers and eight committed effect means. The [verification script](../../scripts/verify_chapter2_figure3_original_bridge_intake_20261015.py) accepts **unchanged outer GitHub Actions ZIPs**, never their unverified unpacked estimates:

```bash
python -m scripts.verify_chapter2_figure3_original_bridge_intake_20261015 \
  --source-dir /directory/containing/17/original-zips \
  --out /new/path/figure3_bridge_verified.json
```

For the locally prepared 945,025-byte source-intake bundle (all 17 original ZIPs and the independently generated no-raw-claim readout), use `--bundle /path/to/ch2_fig3_panelA_original_endpoint_artifacts_verified_20261015.zip` instead of `--source-dir`. The bundle is an **unpublished local provenance convenience**, not a Zenodo/DOI or complete genotype trajectory archive.

The verifier refuses missing/changed source ZIP SHA-256, CRC failure, altered source snapshots, missing or repeated visitor histories, non-3×8×8 endpoint dimensions, incomplete case receipts, mixed original-code paths, or drift from the committed eight plotted means. Tests validate the immutable pinned numerical contract without fetching 17 original GitHub artifacts on every CI run.

**Next blocking action under [Issue #436](https://github.com/zuizui0223/izu-core/issues/436):** source-match and independently byte-verify the archived **one-locus original mutation-memory ZIP** (64 full trace-case hashes recorded) and the separate **original-mutation atom source ZIP**, then assess full S1–S33 source coverage, lawful licenses, author attribution/access, external Zenodo deposition and re-download. Do not overstate original bridge full genotype availability.
