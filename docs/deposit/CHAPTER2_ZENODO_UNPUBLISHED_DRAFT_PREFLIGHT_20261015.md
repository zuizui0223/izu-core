# Chapter 2 — Zenodo unpublished-draft preflight (2026-10-15)

**State: repository-local metadata proposal only. No Zenodo account session, draft record, reserved DOI, raw upload, embargo change or publication.** Target repository for planning: [Zenodo](https://zenodo.org/). Machine preflight: [proposed record and source-lock inventory](chapter2_zenodo_unpublished_preflight_20261015.json). This handoff is **not** a Deposit Receipt, Data Availability assertion or a manuscript scientific result.

## Immediate, independently checkable outcome

The initial **six-package source core** follows already committed historical archive receipts. These six archives are containers for existing source data; never treat archive members as independent ecological samples.

| Original source group | Prepared package | Prior bytes | Science/provenance status |
| --- | --- | ---: | --- |
| Demographic orthogonal (independent 64 histories) | `chapter2-orthogonal-130-original-shard-artifacts.tar` | 227,543,040 | Previously preserved GitHub draft Release; original primary inconclusive |
| Demographic K × B (independent 64 histories) | `chapter2-kb-130-original-shard-artifacts.tar` | 226,304,000 | Previously preserved GitHub draft Release; original primary inconclusive |
| Demographic K at B48 (independent 64 histories) | `chapter2-fixedB48-all-original-131-artifacts.tar` | 224,860,160 | Previously preserved GitHub draft Release; model-specific conditional K moderator supported |
| Demographic early/late viability (independent 64 histories) | `chapter2-timed-130-original-shard-artifacts.tar` | 225,617,920 | Previously preserved GitHub draft Release; original primary inconclusive |
| Evolution (two distinct, separately frozen campaigns) | `chapter2_public_archive_20261006.zip` | 518,372,739 | Historical full-byte original ZIP audit; 50 unchanged Actions ZIPs including 4,096 and 8,448 cases |
| Synthetic visitor-tempo supplement | `izu_core_functional_loss_tempo_full_20261011.zip` | 268,940,123 | Existing source/archive receipt for 1,024 modeled cases; descriptive, model-specific |

**Total: 6 containers / 1,691,637,982 bytes (~1.69 GB).** Source identities, exact SHA-256 strings and historic receipt pointers are in the JSON. This preflight did **not** download, rehash or transfer these six giant containers. Existing private copies and same-provider GitHub backups are provenance—not a Zenodo draft.

Two additional previously recorded source archives have been identified as **separate candidates**, not automatically approved files: original discovery `model3_replenishment_evolution_20261005.zip` (763,914,318 bytes) and matched finite-ABM `completed_atom_abm_20261011.zip` (389,730,774 bytes). If all eight were admitted, their cumulative recorded size would be 2,845,283,074 bytes (~2.85 GB). **This is still not a complete paper-wide SI/source inventory**: Q3 conditional restoration, original ABM auxiliary archives and other source-qualified companions require a source-specific audit, not new simulation. No assumption that their raw content is contained in the six core packages is made.

## Zenodo service and confidentiality rules

Zenodo documents **100 files and 50,000,000,000 bytes** as default per-record upload limits ([manage files](https://help.zenodo.org/docs/deposit/manage-files/)). A record can be prepared and saved as an unpublished draft; Zenodo's UI requires basic metadata including **creators** ([draft creation](https://help.zenodo.org/docs/deposit/create-new-upload/), [creators](https://help.zenodo.org/docs/deposit/describe-records/creators/)). Published record **metadata are public even if file access is restricted** ([record lifecycle](https://help.zenodo.org/docs/deposit/about-records/)). Zenodo can **reserve** a DOI in a draft, but this workflow deliberately does not reserve or register one until specifically approved ([DOI guidance](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/)). A saved draft and a registered/public DOI are different states.

The workspace currently has no confirmed authenticated Zenodo connection available to the assistant. The author/depositor must connect an account before a real private Zenodo draft can be saved; **the presence of a browser profile with a Zenodo-related label alone is not proof of login**. Do not paste API tokens, passwords, private Drive URLs or author personal identifiers into the public repo.

## Registration decisions deliberately left unset

The [proposal JSON](chapter2_zenodo_unpublished_preflight_20261015.json) contains a model-grounded, copy-ready **candidate title, description and keywords**, but deliberately leaves **ordered creators, affiliations/ORCIDs, dataset license, code license, final version, access/embargo choice and release date** as `null`. No publication metadata are silently borrowed from older Journal of Ecology/Oikos/Dryad templates. The final attribution, rights and disclosure audit remain the author/depositor's decision.

The earlier fixed-B48 private external-provider safety stop remains in force: **520/521 original demographic ZIPs** were previously authenticated via private external readback; the omitted `chapter2-k48-future-shard-18.zip` was successfully re-fetched and checked from GitHub Actions under [PR #524](https://github.com/zuizui0223/izu-core/pull/524), **but the blocked private transfer was not retried or bypassed**. Do not describe private backup as 521/521, even though all originals remain preserved in same-provider draft Releases. Also keep the 50 evolutionary originals and the independent tempo ZIP distinct from the 521 demographic originals.

## Reproducible, read-only local gate

```bash
python -m scripts.verify_chapter2_zenodo_unpublished_preflight_20261015
pytest -q tests/test_chapter2_zenodo_unpublished_preflight_20261015.py
```

The verifier compares the six candidate file names/sizes/SHA-256 strings against existing committed receipts, checks distinct original-case counts, retains source limits and refuses to promote unapproved status or invented creators/licenses/DOIs. **It does not authenticate raw source ZIP bytes or access Zenodo**. Do not add this optional archival preparation test to the manuscript's fast scientific-gate test list merely for documentation; the repository-wide CI will collect the test.

## Next gates, in order

1. **Author-side account and metadata approval.** Resolve whether the Zenodo account/profile is signed in; approve exact creator order and identities, licenses, dataset version, rights and planned access. Until then this remains a local proposal, not a remotely saved draft.
2. **Complete source scope.** Resolve the additional archived originals and supplementary data actually consumed by the active unified manuscript, without merging inference units or deleting historical source files. Recheck the active paper/SI paths at the exact source commit.
3. **Read-only source acquisition and verification.** Obtain each selected unchanged container via authorized existing GitHub/private paths; authenticate container and all nested original ZIP/pedigree/case hashes and store a new exact-size receipt. Stop and do not work around any provider access/safety restriction.
4. **Unpublished Zenodo draft only, after account/author approval.** Enter the approved basic metadata and, if separately permitted, stage verified files. Choose **Save draft**, not Publish. Do not choose “Get a DOI now!” and do not share the draft by link without approval. Audit draft record ID/owner, source-file digest readback and visibility.
5. **Publication authorization separately.** Only after complete deposit checks, authors/licensing/access agreement, cross-host independent readback and an explicit publish instruction may a DOI be registered and manuscript Data Availability plus [Issue #436](https://github.com/zuizui0223/izu-core/issues/436) be updated.

**No change** to Model 3 biological kernels, original experiment designs, statistical verdicts, raw source ZIP bytes, user storage permissions or journal submission is performed by this preflight.
