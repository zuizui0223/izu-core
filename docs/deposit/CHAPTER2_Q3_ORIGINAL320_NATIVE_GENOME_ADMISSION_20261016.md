# Q3 original-mutation source: full 320 diploid annual-genome readback (2026-10-16)

**Historical pre-execution state: one-shot source-only recheck prepared. The completed source admission and its actual readback are recorded below.** No full original-source success, new biological simulation, new statistical result or DOI is claimed until an actual run verifies the complete source bytes. This is a **retrospective** source audit for the already reported separate Model3 original-mutation comparison, not a preregistered new hypothesis test.

## Source locked before readback

The original source bundle is the GitHub [`atom-cell-inputs-20261011` release](https://github.com/zuizui0223/izu-core/releases/tag/atom-cell-inputs-20261011). The release's current original-asset records indicate:

| Immutable source | Original bytes | Release asset | Original SHA-256 |
|---|---:|---:|---|
| `completed_atom_abm_20261011.zip` | 389,730,774 | 630963509 | `7ae00916ed2cbb38323c3fb9ffc5824de3e8272df1f5a35785842c316191f918` |
| `remote_atom_inputs_20261011.zip` | 148,159,152 | 630069066 | `f0fd126f638e1c6bd130e640ce4491b3bb47aac3da1838359a902776c9a4e037` |

The completed cohort originally ran as [GitHub Actions 38120835221](https://github.com/zuizui0223/izu-core/actions/runs/38120835221), archived executor `e331e0fe2c0048f94197f41f34575dbcd77c0377`. Its [preservation manifest](../../data/results/atom_cell_completed_20261011/COMPLETED_ATOM_ABM_PRESERVATION_20261011.json) records **774 ZIP members including 773 ordinary members**, with **320 original ABM NPZ + receipt pairs** and **30 numerical density NPZ + receipt pairs**; complete original source-side audit arrays are among the other members.

## Why this is needed despite earlier verification

[Existing original-mutation verdict](../atom_comparison_20261011/ATOM_ABM_NUMERICAL_VERDICT_20261011.md) independently checked 990 event/category classifications and 40 recorded source checkpoints from the original *stored phenotype/trait means* for 320 ABM paths and ten finest-grid density references. **It did not recompute all those annual trait means from the saved original diploid alleles.** The new check fills precisely that source-to-output gap:

1. Download **only unchanged original archive bytes** from the already existing release, authenticate the outer original digest and byte size, and read all **774 ZIP members** using CRC and original 773 filename/size/SHA manifest. Verify separate source input archive digest; never overwrite anything.
2. For all **320 original finite diploid cases**, load the complete original 201-census `alleles/offsets/population` traces and independently reconstruct the **64,320 genotype-derived trait-mean censuses** (201 × 320). Require exact match to the saved trait summaries at tolerance `1e−12`. Do not substitute summary means for missing or corrupted alleles.
3. Verify the **30 native deterministic genotype-density archives** separately against the source-approved density digests; match ten original contexts with finest admitted 257-node density trajectories, keeping 65- and 129-node source archives intact without rerunning their numerical solver.
4. Reclassify all **990** event-history categories across `0.025, 0.05, 0.10` thresholds, 20 consecutive censuses and a 5-update tie rule, with the previous founder-relative definitions unmodified; also recompute **40** paired 0/25/100/200 checkpoint summaries.
5. Require the original, nonselected **two matched 0.125-low-supply contexts** to produce density `assurance_first` while only **3/32** and **2/32** finite histories reach assurance-first at threshold `0.05`. All 32 must remain occupied at t200 in each context. Preserve every other null, opposite-sign and mixed response category.

The old source simultaneously encodes finite parent sampling, diploid segregation, density regulation and two founder-genetic backgrounds. A discrepancy between finite ABM and conditional genotype density **does not isolate drift**, prove a mathematical finite-size expectation identity or establish an island's evolutionary past. At `0.025`, density order for these two low-supply contexts can instead be near-simultaneous; the event-definition sensitivity is real and must not be concealed.

## Source admission outcome (2026-10-16, completed)

**Original source readback SUCCEEDED.** The one-shot read-only [Actions run 38823339694](https://github.com/zuizui0223/izu-core/actions/runs/38823339694) completed successfully on source commit `e1550a89b0976a1453e052ca21de011c69e2ab2c`, and the preserved [original-readback artifact 12013992974](https://github.com/zuizui0223/izu-core/actions/runs/38823339694/artifacts/12013992974) was independently downloaded, CRC-tested and checked against its internal execution receipt.

- Both original Release ZIPs matched byte length and SHA-256: original completed cohort `389,730,774` bytes / `7ae00916ed2cbb38323c3fb9ffc5824de3e8272df1f5a35785842c316191f918`, original source inputs `148,159,152` bytes / `f0fd126f638e1c6bd130e640ce4491b3bb47aac3da1838359a902776c9a4e037`.
- Original ZIP **774/774 members**, all **773 separately recorded original paths/lengths/SHA values** reauthenticated; no added/missing source member, CRC failure or source input substitution.
- **320 complete original diploid ABM trajectories × 201 occupied censuses = 64,320 allele-derived annual trait-mean checks**, with **maximum saved-mean discrepancy 0.0**.
- **30 native density source NPZ archives**, ten unique contexts and the original 65/129/257 numerical grids, each source digest checked. No new finite/population run or numerical grid integration.
- The original **990 event category assignments** across three founder-relative sustained-crossing thresholds and **40 ABM/density checkpoints** were reproduced *from independently recomputed genome-derived means*. No outcome-selected cases removed.
- At threshold **0.05**, native low-supply 0.125/matched density is **assurance-first** in both original founder contexts, while finite realized assurance-first is **3/32 and 2/32**; all 32 finite paths in both contexts are occupied at t200. This is an original-source authentication of an *already reported model contrast*, not a new outcome confirmation cohort.

**Threshold sensitivity must be retained:** at threshold 0.025, founder1 density is `near_simultaneous` and founder2 density is `assurance_first`; finite A-first frequencies there are 6/32 and 3/32. At threshold 0.10, founder1 density remains `assurance_first` but founder2 density is `assurance_only`; finite A-first frequencies are 1/32 and 0/32. Thus neither a universal assurance-first model prediction nor event-order equality across threshold definitions is established.

The independently inspected original artifact ZIP outer SHA-256 is `ed9fa1232493fce63d04449d923ddb393bddd49581477fb7ce945538b9afa452`; its inner JSON report SHA-256 `0e457b18a29a4058ec79609ea97be203925da78525bd80670da3635b1c428c9b`, original reader source SHA-256 `4424efd5e2e97ca0c6f7a8aa1ba4dd186228ed27cd5d62ff5edc46988d109383`. The full result retains **all ten contexts**, six outcome categories and separate inference units.

**Still NO external DOI:** archived release data are on GitHub, not Zenodo; rights, creator approval, source-wide S1–S33 coverage and independent cross-host readback remain unresolved in [Issue #436](https://github.com/zuizui0223/izu-core/issues/436). Source genomic identity is now verified without natural island causation or attribution of a unique drift component.

## Reproduction and original-data scope

The machine-lock [activation protocol](protocols/chapter2_q3_original320_genome_readback_activation_20261016.json) is `PREPARED_NOT_ACTIVATED` until manually advanced, authorizing exactly one read-only GitHub Actions run via an exact branch and protocol path. It excludes broad automatic workflows, scheduled monitoring, sample selection, rerunning source biology or publishing data.

The standalone verifier [`scripts/audit_chapter2_q3_original320_annual_genomes_20261016.py`](../../scripts/audit_chapter2_q3_original320_annual_genomes_20261016.py) and fast [unit tests](../../tests/test_chapter2_q3_original320_annual_genomes_20261016.py) preserve original science. Once source-authenticated original archives are available, use:

```bash
python -m scripts.audit_chapter2_q3_original320_annual_genomes_20261016 \
  --archive /read-only-input/completed_atom_abm_20261011.zip \
  --out /new/output/Q3_ORIGINAL_GENOME_READBACK.json
```

**External DOI gate remains open (Issue #436):** even a successful fresh GitHub release ZIP download and full archived 320-genome readback is **not** a separately administered external DOI deposit. It does not verify unrelated Q1/Q2/Q4/S1–S33 raw archives, source disclosure rights, creator identity/order, dataset license, embargo/public access or cross-host re-download. No Zenodo draft, upload, DOI or public permission change is authorized by this source audit.
