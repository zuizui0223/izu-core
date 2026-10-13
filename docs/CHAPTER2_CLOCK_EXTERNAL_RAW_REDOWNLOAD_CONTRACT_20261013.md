# Q1→Q2 Model 3 pilot: external-archive six-shard re-download contract

**2026-10-13. Executable reviewer code / negative controls only. Zero 200-update pilot histories generated; no external pilot raw data or DOI exists yet.** Stacked on PR #500, not a new biological study. CI success of the earlier 48×3 native technical fixture does not constitute 1,536×200 pilot source admission.

## Source and identifier controls

The previously registered **2 founders × 3 ecological contexts × 2 A half-widths × 2 hidden-I homolog states × 64 paired history seeds = 1,536 biological paths** imply **six distinct 256-case source ZIPs**, one per founder×ecology. Each path must have 201 annual full original typed genomes and 200 original Model 3 reproduction/recruitment updates. The original pilot registry Git blob is `f18eae09e3f569ae7edefe970ea17d93c64b1bd5` and original biological code is source-pinned at commit `328548612e93469fcc8663f24548530a57399b9a` with its individual typed/reproduction/population/randomness/history Git blobs checked by the independent reader.

The added `review_chapter2_clock_external_archives_20261013.py` is *only* a read-only reviewer. It imports the existing original-model native raw reviewer and complete six-shard admission aggregator, **never the producer**. It requires an independently obtained manifest listing all six sha256 digests, six GitHub release download URLs and six separate-mirror receipt references. Those strings alone cannot prove actual release custody, backup existence or DOI registration: a reviewer must obtain and authenticate the actual original release/backup sources outside this program. The committed manifest `chapter2_clock_external_archive_receipt_TEMPLATE_20261013.json` has deliberately missing digests and `PENDING_RAW_ARCHIVES_NEVER_RUN`; this placeholder **must always fail admission**.

## Raw ZIP → six independent native replays → one all-start admission

For each of six archived source ZIPs, in its frozen order:

1. Recompute the **ZIP byte SHA256** and require equality to the externally reviewed manifest. Reject duplicate or omitted original NPZ members, extra files, nested paths, symlinks, oversized/unexpected payloads and invalid `_COMPLETION.json` identity/horizon/source registry. Never extract untrusted filenames without checking their original 256-case allowlist.
2. Materialize the exact allowlisted members into a new temporary directory. Invoke **independent original Model3** `verify()` directly on every saved NPZ, with expected case IDs, full diploid genotypes, maternal/paternal/self return arrays, exact yearly parentage and seeded original reproduction/birth, mutation masks, extinction, and six-class censoring. The producer cannot be imported or used to replace an archive readback.
3. Publish each independent readout using **exclusive file creation**, recording source ZIP SHA256 and full readout SHA256 keyed by **founder×visitor context** (not only basename). On any corrupt source, this run **fails closed**; an incomplete output directory cannot be considered passed.
4. Only after six full source replays, invoke the existing six-shard aggregator, which independently requires all **1,536** registered cases, **128 paired founder×history groups with 12 original arms each**, exactly **307,200** independently checked Model 3 updates and the original six mutually exclusive response categories (including all unobserved/censored histories).

The complete output has source manifest hash and archive/readout digests and explicitly records `new_biological_histories_generated_by_reviewer=0`. It remains *pilot exploratory source admission*, **not** confirmation of an independently predictive A-access/I-response clock, a natural ecological threshold, or Q4 order-caused population persistence.

## What remains on HOLD

- Real 200-update producer is still blocked by its **unset independently frozen scientific approval SHA**, so there are no six real ZIPs for this reviewer. Do not substitute synthetic mock ZIPs, short technical fixtures, the old 2,304-history cohort, or unverified branch files.
- Before any biological pilot, an independent reviewer must approve the original fixed producer, separate archival destination, complete safety/backups, verified mirror source, data export/DOI strategy and the exploratory statistical handling. Then a reviewed approval receipt must be committed distinctly; this document does not authorize it.
- Once actual archives exist, the independently obtained external manifest and two copies must be inspected for actual custody/bytes. A false manifest saying `RELEASE_ARCHIVED_AND_MIRROR_RECORDED` is not evidence; its SHA relation only checks equality to what it asserts. DOI registration remains a distinct unresolved gate.
- Confirmatory Q1→Q2 modeling needs a frozen access-delay clock and an equal-or-more-flexible ecological-genetic alternative, plus new separate histories after pilot exploration. The all-six raw source verifier does not create scientific independence or infer a causal mechanism.

### Technical negative controls

The new isolated tests create **only mock ZIP byte files and fake registry keys**; they never call `population.advance()` or run Model3. They verify the required six manifest entries, incomplete/pending receipt rejection, missing/extra/symlink members, and impossibility of overwriting an already reviewed destination. The positive mock check means merely that a canonical 257-member ZIP *shape* is recognized, not that it contains biological data. Native 48×3 writer/reader tests remain on the parent PR; the new code does not change them.
