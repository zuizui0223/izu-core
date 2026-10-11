# Chapter 2 unified data-deposit readiness — 2026-10-11

**Status: readiness record prepared; external transfer, independent external recovery, licensing and persistent identification remain pending.** This record associates existing source packages with the **one** active [unified Ecology Letters manuscript](CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md). It creates no new raw archive, changes no original receipt, and supplies no author identity, license, account or DOI.

The companion [machine-readable readiness manifest](../data/submission/chapter2_unified_data_deposit_readiness_20261011.json) contains 32 repository source references with freshly computed SHA-256 and byte sizes, exact inventory pointers, existing package identities, missing inputs and ordered verification gates. Preparation began from integration commit `3fec785f2774c9ba43fd1bf4108e370aa46e3180`, incorporating main `3efb019deef215fe0f8f0179170238331d5932cd`. These are preparation-source identities, not the original biological execution commits or an external deposit version.

## 1. Three source groups, with distinct counting units

| Source group | Existing inventory | Existing preservation evidence | Readiness limit |
| --- | --- | --- | --- |
| Original evolutionary confirmation and assurance-generality campaigns | **50 original Actions ZIPs** across **two campaigns**: 17 + 33 | Per-artifact IDs, API-reported SHA-256, sizes and expiry dates in the [original evolution manifest](../data/design/chapter2_public_archive_manifest_20261006.json) | This preparation verified the metadata and referenced local files, not an available copy of the raw ZIPs or a completed outer-bundle receipt. |
| Four independent demographic cohorts tracked by [#436](https://github.com/zuizui0223/izu-core/issues/436) | **521 original Actions ZIPs**: 130 + 130 + 131 + 130, preserved inside **four existing tar files** | Prior raw preservation in the [ledger](CHAPTER2_INDEPENDENT_RAW_ARCHIVES_20261009.md), plus exact small-manifest recovery completing **521 distinct metadata IDs** | The original 390-entry snapshot remains unchanged. Recovered manifests supply the missing 131 records; all 130 overlapping fixed-B48 entries match. The raw cohort archives were not downloaded again. |
| Complete abrupt-versus-gradual tempo cohort | **One local ZIP**, **268,940,123 bytes**, containing **2,099 members** | Original admission, saved-copy retrieval and later local CRC/hash/endpoint recheck in the [tempo receipt](../data/results/chapter2_sequence_abrupt_gradual_functional_loss_receipt_20261011.json) and [fresh verification](../data/results/chapter2_sequence_tempo_fresh_verification_20261011.json) | Private saved artifact; no cohort Actions run or draft-release tag, and no external deposit or DOI. |

The four tar files are containers for the existing 521 demographic ZIPs. They are not four additional biological datasets. The tempo ZIP is not an Actions artifact and must not be included in the “521 Actions ZIPs” count. The demographic studies each retain their own 64-history inference unit; tempo retains 16 profiles and four nested demographic repeats. Neither archive-member counts nor trajectory counts create extra independent biological samples.

## 2. Evolution: preserve the existing 50 original ZIPs

The [2026-10-06 source manifest](../data/design/chapter2_public_archive_manifest_20261006.json) contains all 50 distinct artifact IDs, names, original digest records and sizes. Its two `campaigns.*.artifacts` arrays are referenced directly by the readiness JSON rather than duplicated.

| Campaign | Original workflow | Declared cases | Original ZIPs | Sum of recorded ZIP sizes |
| --- | --- | ---: | ---: | ---: |
| Independent confirmation | [37390991122](https://github.com/zuizui0223/izu-core/actions/runs/37390991122) | 4,096 | 17: 16 shards + one result | 140,194,174 bytes |
| Four-setting assurance generality | [37458098483](https://github.com/zuizui0223/izu-core/actions/runs/37458098483) | 8,448 | 33: 32 shards + one result | 377,934,908 bytes |

The recorded ZIP sizes sum to **518,129,082 bytes**. This is a sum of source API metadata, not a newly measured archive size. The source manifest records main `982e55e80e4ca1e880edf089c3a06ce6bebce61f`; the original workflow identities and frozen designs remain authoritative for their respective results.

The existing [archive preparation document](CHAPTER2_PUBLIC_ARCHIVE_PREP_20261006.md) and [builder](../scripts/build_chapter2_public_archive.py) document `outputs/chapter2_public_archive/chapter2_public_archive_20261006.zip`. A documented output path does not prove that a preserved copy or checksum receipt is currently available. Locate and authenticate any existing bundle/receipt before choosing a transfer route; otherwise recover the original ZIP bytes by their existing identifiers. No new bundle or raw copy was made for this readiness record.

Some shard-expiry records start at **2026-11-04T23:54:31Z** for confirmation and **2026-11-05T11:43:09Z** for assurance generality. The result-artifact records extend to January 3–4. These are historical manifest dates, not fresh accessibility checks. They should not be replaced with the January 7 dates associated with the later demographic cohorts.

The original manifest includes `docs/CHAPTER2_MANUSCRIPT_ECOLOGY_LETTERS_20261006.md`. Preserve that historical association inside its original archive. Associate the current unified paper through this separate readiness record and the active reviewer package; do not rewrite an original archive to make its historical manuscript appear current.

## 3. Issue #436: reuse the four verified draft-release packages

The following identities come from the [existing preservation ledger](CHAPTER2_INDEPENDENT_RAW_ARCHIVES_20261009.md) and the previously retrieved [open issue requirements](https://github.com/zuizui0223/izu-core/issues/436). Their prior verification is recorded evidence; this preparation did not repeat the downloads.

| Cohort | Existing draft-release tag | Original ZIPs | Existing tar size | Recorded preservation workflow |
| --- | --- | ---: | ---: | --- |
| Matched-founder orthogonal capacity | `chapter2-orthogonal-raw-20261009-v1` | 130 | 227,543,040 bytes | [37906844144](https://github.com/zuizui0223/izu-core/actions/runs/37906844144) |
| Independent K × B | `chapter2-kb-raw-20261009-v1` | 130 | 226,304,000 bytes | [37906844144](https://github.com/zuizui0223/izu-core/actions/runs/37906844144) |
| Independent fixed-B48 K confirmation | `chapter2-fixedB48-raw-20261009-v1` | 131 | 224,860,160 bytes | [37906236862](https://github.com/zuizui0223/izu-core/actions/runs/37906236862) |
| Independent early-versus-late seed viability | `chapter2-timed-self-raw-20261009-v1` | 130 | 225,617,920 bytes | [37953047322](https://github.com/zuizui0223/izu-core/actions/runs/37953047322) |

Exact existing tar names and SHA-256 values:

| Existing file | SHA-256 |
| --- | --- |
| `chapter2-orthogonal-130-original-shard-artifacts.tar` | `03e1292511219ea4ee64499d35ac0e5a5f824f1ee0fd420ecd7ca97f4f9ebf65` |
| `chapter2-kb-130-original-shard-artifacts.tar` | `7d367a9e4a9f4f60f25dbee2ccabc84ef0969f5d9b0096c7df07380314dcfff9` |
| `chapter2-fixedB48-all-original-131-artifacts.tar` | `3e522fc9d8da904ed70cc2213bc3b08816761c4e44a4badc72e0c87ba04bd42c` |
| `chapter2-timed-130-original-shard-artifacts.tar` | `b5ab3a99eeaf36da399290508a64fa022cacc734aa1d794cab3b8443707309aa` |

The four outer tar sizes sum to **904,325,120 bytes**. Keep their original ZIP members, included manifests and separately saved verification receipts unchanged.

### Per-ZIP inventory completed from existing records

The [committed 390-entry snapshot](../data/design/chapter2_raw_actions_artifact_inventory_20261009.json) covers the first **three cohorts across four workflow runs**:

- Orthogonal t400 sources: run `37887039116`, 65 entries.
- Orthogonal futures/readout: run `37887290489`, 65 entries.
- K × B: run `37893126472`, 130 entries.
- Fixed B48: run `37896872795`, 130 entries.

This snapshot explicitly describes **metadata only**, not raw-byte preservation. Its 390 recorded ZIP sizes sum to **677,782,795 bytes**. It omits one later source-preserving corrected fixed-B48 readout ZIP from run `37900150213`, and all 130 timed-cohort ZIPs from run `37944527799`.

The **131 records missing from the original snapshot** have now been recovered from existing preservation manifests. A fresh, read-only [GitHub release collection query](https://api.github.com/repos/zuizui0223/izu-core/releases?per_page=100) exposed all four draft releases and confirmed that their tar metadata sizes and SHA-256 values still match the ledger. It also independently identified the two companion manifests:

| Existing JSON manifest | Draft release ID | Asset ID | Recorded bytes | SHA-256 from asset metadata |
| --- | ---: | ---: | ---: | --- |
| `fixedB48-original-artifacts-manifest.json` | 407720483 | 624397843 | 74,952 | `b9702f07e9374bdb038dfdaffb36d88a8c4f44945ebb102b7910eab92a7b944b` |
| `timed-raw-130-manifest.json` | 408060663 | 625388987 | 62,890 | `ade98a9e3916f8d92b4cdc6b3a724fae811fb0696fdbc4bccf6290f0e51586a6` |

Their separate receipts also exist as JSON assets: `fixedB48-archive-receipt.json` (asset `624397845`, 354 bytes) and `timed-archive-receipt.json` (asset `625388990`, 360 bytes). The readiness JSON records all four cohorts' manifest/receipt asset IDs, sizes and digests. The fixed-B48 and timed manifest bytes recovered below independently match these Release asset metadata identities.

Both observed private-draft manifest download URLs returned HTTP 404 through the generic connector, while release-collection metadata remained readable. The existing dedicated Actions artifact-download tool supplied an alternative read-only route: the two preservation runs already retained small, independent receipt ZIPs. Both packages passed SHA-256, byte-size and complete ZIP CRC checks:

| Existing receipt package | Actions artifact ID | ZIP bytes | SHA-256 |
| --- | ---: | ---: | --- |
| Fixed-B48 preservation run `37906236862` | 11604921559 | 11,406 | `4e84546cd7bd75ef4e67d926fa5273d97f340453bc141442817a2a0dc56fc8b0` |
| Timed preservation run `37953047322` | 11626049740 | 10,555 | `87ba619b2d1528b8b46e170de0034de9f37c4b4127504dbf62af0ebd756007ba` |

Each receipt package contains three small JSON members: its original manifest, the historical preservation receipt, and draft-release status. The exact manifest byte streams are retained as deterministic gzip with modification time zero: [fixed-B48 original manifest](../data/submission/chapter2_archive_manifest_recovery_20261011/fixedB48-original-artifacts-manifest.json.gz) and [timed original manifest](../data/submission/chapter2_archive_manifest_recovery_20261011/timed-raw-130-manifest.json.gz). The separate [recovery receipt](../data/submission/chapter2_archive_manifest_recovery_20261011/recovery_receipt.json) records both ZIP identities, original and compressed manifest identities, CRC results and the reconciliation.

All **130 overlapping fixed-B48 entries** matched the unchanged snapshot across **nine mapped fields, 1,170 comparisons and zero mismatches**. The extra corrected readout is artifact `11601189449` from run `37900150213`, 1,289 bytes, SHA-256 `43c1eedef79e1ea06f61302c5148cf23b7bfe319d5bf7d5f3b21668bb54c6035`. Adding it and the 130 distinct timed entries completes **521 distinct original artifact IDs**, with **zero remaining per-ZIP metadata gap**. Their recorded original ZIP sizes sum to **903,095,464 bytes**. This is a metadata total, not a new raw-byte measurement.

Only **21,961 bytes of existing preservation-receipt ZIPs** were downloaded. No scientific raw ZIP or tar was downloaded, no workflow was added or triggered, and no external scientific deposit was made. The recovered historical receipts retain their original pre-upload readiness statuses; they were not rewritten to claim later verification. The manifest's fixed-B48 source-run SHAs are now preserved exactly, including the original run and corrected readout identities.

The current source readouts remain separately linked and hashed. Orthogonal capacity, B at K8, and timed viability retain their **inconclusive** registered primaries; the fixed-B48 K primary retains its model-specific supported verdict. Deposit preparation does not pool their intervals or change those decisions.

## 4. Tempo: reuse the existing single ZIP

The [admission receipt](../data/results/chapter2_sequence_abrupt_gradual_functional_loss_receipt_20261011.json) identifies:

```text
File:    izu_core_functional_loss_tempo_full_20261011.zip
Bytes:   268940123
SHA-256: 034e735d244228c1f4974897a76d16acef10767a81d5dd82f5f5204f48cf0738
Members: 2099, including inventory.json
```

The inventory SHA-256 is `2f5e09d18126d0a16fca93a13364f6c711c6c64a0b1b27c4e4f113acb176bd70`. It covers 1,024 raw case JSON files, 1,024 case receipts, 16 shard manifests and the other preserved provenance/readout files. The original execution commit is `dba65f11a4ee7295ae32b623ea1103cc8a25c1b5`, with its [unchanged frozen design](../data/design/chapter2_sequence_abrupt_gradual_functional_loss_20261011.json) and [original execution receipt](../data/results/chapter2_sequence_tempo_execution_receipt_20261011.json).

The saved-copy retrieval receipt records a separate-path SHA-256/size match at `2026-10-11T05:53:49.549570+00:00`. The [later verification record](../data/results/chapter2_sequence_tempo_fresh_verification_20261011.json) records complete CRC/hash reads of both existing copies and the endpoint audit. It explicitly records **no fresh external download**. This readiness task checked the local receipt links and compressed readout/audit bytes; it did not repeat the raw ZIP reads or biological calculations.

Retrieve the existing saved artifact through its established identifier/context when transfer work is authorized. The committed receipt attests that exact-identifier retrieval occurred, but does not include the identifier value itself. Do not invent a GitHub artifact ID, workflow run or release tag for this local cohort.

After eventual external recovery, the existing [independent checker](../scripts/audit_chapter2_sequence_tempo_results_20261011.py), used with the original frozen source, can check 1,024 cases, 410,624 census states and 128 event/order/occupancy comparisons. Its independent calculator excludes **all 156 secondary fields per setting**, including aggregate trait means/variances and conditional lag. The result remains descriptive and model-specific, with saturated occupancy and no identified persistence benefit or practical-equivalence claim. [REPRODUCE.md](../REPRODUCE.md#complete-functional-loss-tempo-result-2026-10-11) supplies the existing audit command.

## 5. Transfer and verification gates

These gates are recorded individually in the companion JSON. The first two are complete for this preparation.

1. **Local reference integrity — complete.** Parse the existing inventories; check their entry counts, unique artifact IDs and digest formats; freshly hash the referenced repository files; verify evolution design hashes and tempo receipt/gzip links. This does not authenticate raw bytes that were not read.
2. **Complete original per-ZIP metadata — complete.** Exact manifests recovered through the two existing small Actions receipt packages fill the former 131-record demographic gap. All 130 overlapping fixed-B48 records match, and current local metadata covers 521 distinct demographic artifact IDs. The separate evolution manifest retains its 50 IDs. This gate establishes metadata coverage; raw-package authentication and external recovery remain separate gates.
3. **Existing package availability and authentication — not rechecked here.** Locate the existing packages. Verify the four tar hashes and tempo ZIP hash, all original ZIP-member hashes, CRCs and completeness. Resolve whether an authenticated evolution bundle/copy already exists before making any new package decision.
4. **External repository metadata and usable access — pending.** Establish the actual independent repository/account, authenticated deposition capability, accurate creators, data/code licenses, disclosure/access decisions and intended version. Unknown values remain null.
5. **Actual transfer and independent external recovery — not performed.** Transfer the existing original packages through the established route. Independently recover the complete external version and compare container hashes and all original per-ZIP checksums, recording a separate recovery receipt.
6. **Source and scientific admission after recovery — pending.** Use each study's original source identity and read-only source/pedigree/future/admission checks against recovered data. Apply the retained tempo endpoint checker within its declared scope. Do not regenerate founders or rerun stochastic cohorts to repair a byte-preservation task.
7. **Persistent identifier and paper linkage — pending.** Record an actually issued and verified DOI/PID, immutable version URL, license, access route and checksums. Update the one active manuscript and `REPRODUCE.md`; assess every requirement of #436 before closing it. Keep the original Actions artifacts and draft Releases until external recovery and validation are complete.

## 6. Missing metadata and current capability limits

Local preparation does not require inventing publication metadata. External deposition still needs an established repository/account and its usable permissions, accurate dataset creators, data/code licenses and disclosure/access decisions. A DOI, record identifier, immutable version URL or public-access claim must come from the actual completed deposit and recovery evidence.

The [older Oikos template](../data/design/island_ecology_submission_metadata_template.json) has no final author list and contains historical route-specific defaults, including Dryad. It does not establish the current EL authors, creator metadata, selected repository/account, license or submission declarations. Keep these fields unset until supplied or otherwise explicitly established. Final title-page and journal-submission declarations are separate from this internal data-preservation inventory.

The inspection could read GitHub metadata and download the two existing small Actions receipt artifacts through the connector. That is not evidence of usable access to an independently administered scientific repository. No dedicated Zenodo, Dryad or Figshare tool was exposed in the tool catalog inspected for this preparation, and no alternative authenticated external-deposition route was verified. This is a capability observation, not a claim that an external account does not exist.

This readiness record contains repository identifiers and is **not** a blinded reviewer artifact. Keep any anonymous manuscript/SI derivative separate from the unchanged original scientific and archive records. The reviewer ZIP, compact SI, committed summary JSONs, private saved artifact and same-provider draft Releases do not by themselves satisfy the external raw-data deposit requirements.

No scientific raw archive was created, copied, downloaded or uploaded for this readiness and metadata-recovery work. Only the two existing small preservation-receipt packages were retrieved. No external service was mutated, no biological simulation was run, no publication or journal submission was made, and #436 remains open under the observed requirements.

## 7. Evolutionary raw archive recovery follow-up

**2026-10-11: the evolutionary package-availability gate has now advanced from metadata coverage to verified raw-byte recovery and private preservation.** Sections 1–6 and the original readiness JSON describe the earlier preparation; their original receipts and source files remain unchanged. The follow-up is recorded separately in the [recovery receipt](../data/submission/chapter2_evolution_archive_recovery_20261011.json) and [independent original-case audit](../data/submission/chapter2_evolution_original_case_audit_20261011.json).

The historical [archive workflow run 37484527507](https://github.com/zuizui0223/izu-core/actions/runs/37484527507) failed before packaging, at an HTTP 302 redirect followed by HTTP 401. Its artifact collection was empty. The inline downloader put GitHub Authorization in redirectable headers; the behavioral regression test reproduces that propagation with urllib's actual redirect handler. Authorization now uses `add_unredirected_header`, retaining authentication on the initial API request without carrying it to signed artifact storage. Original digest checks remain in place.

All 50 ZIPs selected by the unchanged October 6 manifest were retrieved by their exact artifact IDs. Every original byte size, SHA-256 and ZIP CRC passed. The additional reviewer-package artifact from the generality run was excluded from this frozen scientific selection.

| Campaign | Original ZIPs | Original case pairs | Original ZIP bytes |
| --- | ---: | ---: | ---: |
| Independent confirmation | 17: 16 shards + one result | 4,096 | 140,194,174 |
| Actual PR #411 assurance generality | 33: 32 shards + one result | 8,448 | 377,934,908 |
| Total | 50 | 12,544 | 518,129,082 |

The independent read-only audit verified every case's NPZ hash, task, original basename, shard assignment and completion marker. It checked all 25,236 original ZIP members, read 62,720 NPZ arrays and made 1,232 archived source-file comparisons with the original execution commits. No missing, extra or mismatched artifact or case was found. The confirmation cohort contains 2,048 far-only sequence cases and 2,048 fixed-assurance near/far cases; generality contains 8,192 main cases and 256 structural controls. These case counts do not increase either campaign's 64 independent visitor histories.

The raw result JSONs and the same-named committed summaries are different representations. The confirmation full result and console match the hashes explicitly retained in its compact committed result; the documented projection matches across 143 scalar comparisons. All original generality result fields match its committed JSON across 126 scalar comparisons; the committed version adds workflow provenance and changes formatting. The original result ZIP bytes were preserved unchanged.

The existing builder produced `chapter2_public_archive_20261006.zip`: **518,372,739 bytes**, **59 members**, SHA-256 **`0596de11afea2f9f0b5a781f6d0ddd1fa7ea772f048ec0ccfc06e9ecbbf60695`**. This outer ZIP was newly assembled on October 11, rather than recovered as a previously existing outer archive. All 50 original ZIP members and the eight supporting material files matched on readback. The ninth non-raw member is the builder's verification receipt. The separately saved copy was retrieved into a different path and inode at `2026-10-11T10:56:39.756216+00:00`; its full SHA-256 and byte size matched.

Supporting materials and the unchanged builder were recovered from the actual historical packaging checkout, **`94c051850a43b89047e78e653edae25b043624ab`**. This preserves the October 6 manuscript, which has since changed on main. The workflow now pins that supporting-material checkout. The original manifest's source-main field remains `982e55e80e4ca1e880edf089c3a06ce6bebce61f`; the original biological execution commits remain distinct. The unified manuscript stays the only active paper, linked through the current readiness and review records. ZIP timestamps can change a future outer-container checksum; authenticate the specific transferred file with its receipt and retain all original inner ZIP hashes.

The [reusable independent checker](../scripts/audit_chapter2_recovered_evolution_archives_20261011.py) verifies recovered original files without executing a biological simulation; [REPRODUCE.md](../REPRODUCE.md#recovered-evolutionary-raw-archive-2026-10-11) supplies its invocation. Its scope is bytes, source snapshots, receipts, task coverage and stored-array structure. The archived genomes occur at **t0, t200, t400 and t1000**, with a 1,001-row trace; annual genomes, original numerical runtime equivalence, stochastic replay and a new scientific/bootstrap result are not established by this audit.

The [PR #479 cohort-identity boundary](CHAPTER2_SOURCE_REPLAY_COHORT_IDENTITY_20261011.md) remains explicit: these 50 ZIPs cover confirmation and actual PR #411 generality. They do not admit the original sustained-isolation discovery cohort with histories 76001–76064. No demographic tar or tempo ZIP was downloaded again in this follow-up. Private preservation does not supply the independently administered scientific repository, creators, licenses, version, public DOI or external recovery still required for the unified paper and #436.
