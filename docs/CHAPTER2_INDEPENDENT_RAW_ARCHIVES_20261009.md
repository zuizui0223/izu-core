# Chapter 2 — complete raw-artifact preservation ledger (2026-10-09)

**Scope:** preserve all original simulated individual genomes, complete pedigree/source receipts, and future trajectories from the three earlier independent 64-history experiments **and the fourth prospective timed-viability cohort**. This is a data-accessibility and reproducibility record, **not** another analysis or a change to frozen evidence.

## Evidence hierarchy remains unchanged

| Original scientific experiment | Original complete raw source workflow(s) | Raw size / data grain | Registered primary decision | Exact public result JSON |
| --- | --- | --- | --- | --- |
| Fixed-eight founder, varying capacity with seed viability intervention | Source [37887039116](https://github.com/zuizui0223/izu-core/actions/runs/37887039116), futures [37887290489](https://github.com/zuizui0223/izu-core/actions/runs/37887290489) | 64 visitor histories, 2,048 t400 sources, 172,032 future trajectories | **`inconclusive`** for the capacity moderator | [orthogonal_capacity_full_readout_20261009.json](../results/chapter2/orthogonal_capacity_full_readout_20261009.json) |
| New independently generated 2×2 demographic K × pollen-background B | Full workflow [37893126472](https://github.com/zuizui0223/izu-core/actions/runs/37893126472) | 64 histories, 2,048 t400 sources, 229,376 futures | **`inconclusive`** for the preregistered B effect at fixed K8; other comparisons are descriptive | [kb_independent_full_readout_20261009.json](../results/chapter2/kb_independent_full_readout_20261009.json) |
| Separate independent confirmation of demographic K effect at fixed B48 | Original full workflow [37896872795](https://github.com/zuizui0223/izu-core/actions/runs/37896872795), source-preserving corrected readout [37900150213](https://github.com/zuizui0223/izu-core/actions/runs/37900150213) | 64 histories, 2,048 t400 sources, 114,688 futures | **`supported_controlled_demographic_K_moderation_at_fixed_B48`**, model-conditional | [k_fixedB48_independent_primary_20261009.json](../results/chapter2/k_fixedB48_independent_primary_20261009.json) |

Future trajectory cells and nested demographic repeats are **not independent sampling units**: all registered bootstrap estimates are based on 64 visitor histories per separately constructed experiment. These samples must not be pooled as if there were 192 unrelated studies or hundreds of thousands of independent futures.

## Non-public GitHub draft releases as an additional preservation copy

GitHub Actions originally set `retention-days: 90` for source and future ZIPs. The completed readout JSONs in this repository are **not substitutes** for the raw diploid t400 alleles, pedigrees, complete reproductive trajectories and checksummed source/future receipts.

Raw original artifact ZIP bytes are preserved in unpublished **draft** GitHub Releases, retaining each original artifact name and GitHub artifact-ID and SHA-256. A versioned tar contains each original ZIP **unchanged** alongside a machine-readable manifest. Preserving a release in draft state does not make its assets public or mint a DOI.

| Study | Draft-release tag | Original ZIP inventory | Preservation verification |
| --- | --- | --- | --- |
| Fixed-B48 K confirmation | `chapter2-fixedB48-raw-20261009-v1` | 131 ZIPs = 64 t400 source shards + 64 future shards + 3 metadata/readout artifacts | **Verified** in [Run 37906236862](https://github.com/zuizui0223/izu-core/actions/runs/37906236862): SHA-256 verified original zip downloads, tar uploaded and independently re-downloaded/verified |
| Earlier matched-founder orthogonal cohort | `chapter2-orthogonal-raw-20261009-v1` | 130 ZIPs = 64 t400 + 64 future + 2 receipts | **Verified** in [Run 37906844144](https://github.com/zuizui0223/izu-core/actions/runs/37906844144): original GitHub SHA-256 matched; upload and independent draft-release download verified |
| Earlier K×B 2×2 cohort | `chapter2-kb-raw-20261009-v1` | 130 ZIPs = 64 t400 + 64 future + 2 receipts | **Verified** in [Run 37906844144](https://github.com/zuizui0223/izu-core/actions/runs/37906844144): original SHA-256 matched, upload/re-download hash verified |

All three preservation Runs have **completed/success**, and the corresponding draft Releases are still **unpublished**. GitHub release assets were independently re-downloaded and SHA-256 verified, including their complete original ZIP inventories:

| Experiment | Release tar (original unchanged ZIPs + machine manifest) | Release asset SHA-256 |
| --- | --- | --- |
| Orthogonal | `chapter2-orthogonal-130-original-shard-artifacts.tar` (227,543,040 bytes) | `03e1292511219ea4ee64499d35ac0e5a5f824f1ee0fd420ecd7ca97f4f9ebf65` |
| K×B | `chapter2-kb-130-original-shard-artifacts.tar` (226,304,000 bytes) | `7d367a9e4a9f4f60f25dbee2ccabc84ef0969f5d9b0096c7df07380314dcfff9` |
| Fixed B48 | `chapter2-fixedB48-all-original-131-artifacts.tar` (224,860,160 bytes) | `3e522fc9d8da904ed70cc2213bc3b08816761c4e44a4badc72e0c87ba04bd42c` |

The releases also contain separately downloadable original-artifact SHA-256 manifest JSON and independent verification receipt JSON. Their asset IDs and the original GitHub run SHAs are retained; none of the underlying model data has been regenerated or filtered.

The fixed-B48 draft Release currently holds `chapter2-fixedB48-all-original-131-artifacts.tar` (224,860,160 bytes), SHA-256 `3e522fc9d8da904ed70cc2213bc3b08816761c4e44a4badc72e0c87ba04bd42c`. The draft-release manifest and verification receipt are uploaded as independent assets. No public release/public external data deposition has been performed.

## How to obtain and verify the complete source archive

A collaborator with GitHub repository draft-release access can fetch a given draft by tag using GitHub CLI:

```bash
gh auth login
gh release download chapter2-fixedB48-raw-20261009-v1 \
  --repo zuizui0223/izu-core \
  --pattern 'chapter2-fixedB48-all-original-131-artifacts.tar' \
  --dir raw-archive
sha256sum raw-archive/chapter2-fixedB48-all-original-131-artifacts.tar
# Expected SHA-256:
# 3e522fc9d8da904ed70cc2213bc3b08816761c4e44a4badc72e0c87ba04bd42c
tar -tf raw-archive/chapter2-fixedB48-all-original-131-artifacts.tar
```

The tar contains the machine manifest plus original artifact ZIPs; reconstruct and rerun the original SHA-256/source-pedigree validation using the frozen model at the recorded original workflow SHAs, **not** the mutable `main` branch. Mere ZIP/tar checksums do not prove biological model validity.

## Fourth independent cohort — prospective early-versus-late seed-viability timing

The **fourth** cohort must be kept separate from the preceding three. It is a new 64-visitor-history set (42110901–42110964), with **2,048 t400 complete diploid sources and 229,376 80-update future trajectories**. Its preregistered *late-versus-early capacity moderation* primary returned **`inconclusive`**, −0.0029649032, history-bootstrap95 [−0.0072632191,+0.0013173206]. The earlier supported fixed-B48 `K` result is unaffected.

- Original one-time source + full-audit run: [37944527799](https://github.com/zuizui0223/izu-core/actions/runs/37944527799), original code SHA `e679e0ee190fa02e0a9d60876cd1a3e9987a4c79`, **131/131 jobs success**.
- Exact original scientific readout: `chapter2-timed-self-viability-64-history-full-readout`, artifact ID `11623707416`; JSON SHA-256 **`42d90c17cef4be1643b987428d3a6367ba09dee6594055ae2d2b693ccb190a01`**. The same machine JSON is preserved in [PR #448](https://github.com/zuizui0223/izu-core/pull/448), separately from this raw backup.
- Original raw original **130 ZIP assets** = 64 t400 source shards + 64 future shards + 2 source-admission/final-readout assets. Original GitHub SHA-256 and size/expiry recorded per source artifact.
- Preservation run [37953047322](https://github.com/zuizui0223/izu-core/actions/runs/37953047322): **completed/success**. Downloaded every original artifact across both API pages, checked each original ZIP against GitHub artifact digest, uploaded a versioned tar+manifest+receipt into a GitHub **unpublished draft Release**, then independently re-downloaded the tar and verified SHA-256 and all 130 original ZIP entries.
- Draft release tag **`chapter2-timed-self-raw-20261009-v1`** (not published, not externally citable), three assets: `chapter2-timed-130-original-shard-artifacts.tar`, `timed-raw-130-manifest.json`, `timed-archive-receipt.json`.
- Original ZIP tar **225,617,920 bytes**, SHA-256 **`b5ab3a99eeaf36da399290508a64fa022cacc734aa1d794cab3b8443707309aa`**. Independent draft-Release re-download hash verification **success**. Manifest SHA-256 `ade98a9e3916f8d92b4cdc6b3a724fae811fb0696fdbc4bccf6290f0e51586a6`.
- One-time execution workflow and launch marker were **removed** after successful preservation. The durable GitHub draft copy is independent of the 90-day Actions artifact expiry but remains within the same provider.

**Totals now preserved as unpublished GitHub draft Releases:** **four independent cohorts, four release tags, 521 original Actions artifact ZIPs** (130 + 130 + 131 + 130; the 131 fixed-B48 set includes its independently corrected readout) with all original byte hashes verified. This does **not** make 4×64 visitor histories one universally representative population or elevate the timed-gate failed primary to support.

## What's still required before journal deposition

[Issue #436](https://github.com/zuizui0223/izu-core/issues/436) remains **open**. External long-lived/versioned scientific repository deposition, checksums after independent external download, DOI minting, and explicit data-availability/licensing review are separate tasks; GitHub draft-release backups do not satisfy those publication requirements. Do not delete original Actions artifacts in the meantime.

**Scientific claim limit:** These are model-generated pollination/flower-trait evolution and finite-population dynamics, not a measured causal effect of island geography, a natural mutation-order rescue law, or lifetime fitness in a wild plant.
