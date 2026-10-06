# Chapter 2 confirmatory raw-data preservation manifest — 2026-10-06

## Why this exists

The 2026-10-05 process claim is now independently confirmed, but the 4,096-case
history-level confirmation data are currently stored as GitHub Actions artifacts.
Actions retention is temporary. This manifest fixes the exact artifact identities,
hashes and expiry dates needed for permanent deposition.

**Scientific result:** confirmed.
**Workflow run:** `37390991122`
**Workflow head:** `380de3240992db691e1434f8577256ced80d5ae8`
**Independent unit:** 64 new visitor histories; eight demographic repeats are nested.
**Declared confirmatory trajectories:** 4,096.

## Raw shard artifacts

The 16 raw shard ZIPs total **140185877 bytes** before any permanent-repository
repackaging. Their current GitHub retention ends around **2026-11-04**.

| shard | artifact id | bytes | GitHub artifact SHA-256 | expires |
|---:|---:|---:|---|---|
| 0 | 11381221933 | 8790387 | sha256:176e143f96173798c304545e32900898330f0fa4573be3a4ae8dc6ea01bdefe6 | 2026-11-04T23:54:58Z |
| 1 | 11380299610 | 8734300 | sha256:3a968e2f8a8feb9d8584b9081eb55c1ae87a9f80be5a0a1595cee99164384d79 | 2026-11-04T23:54:31Z |
| 2 | 11380853633 | 8789078 | sha256:f533e629940f3397f668d89466cc29c5904497dd5e0fd600ddeae248547a6299 | 2026-11-04T23:56:02Z |
| 3 | 11380309897 | 8751040 | sha256:17b1fa5c4b6ad4a7f3f62a69a207d6611072fa3e065ad777946d1fa62fbb44e9 | 2026-11-04T23:56:06Z |
| 4 | 11380619458 | 8805543 | sha256:1474f8459533ef00a0a9d99a9c9dc1f7707c1f2e38c88576ed5f781940cbc59f | 2026-11-04T23:56:00Z |
| 5 | 11380699306 | 8726701 | sha256:700ab871f9315f175b18aad17caeffd20ab8b27d674dfecd0512bbc0e553c712 | 2026-11-04T23:54:31Z |
| 6 | 11380838613 | 8790768 | sha256:a2b80b05350f5029d98d3204d3b913ece51321240d7457f771b885f2e0dec602 | 2026-11-04T23:56:26Z |
| 7 | 11380504445 | 8738241 | sha256:76940ae1c7a02f0ca671ae7e3b472bb7bdc2e326b8f648e4dffdb672c1d57c39 | 2026-11-04T23:55:06Z |
| 8 | 11381482009 | 8788063 | sha256:da2e8a5a5c3067228a0d9dd58c907447a5a0f7688fd93a642a55db83cb6b8b43 | 2026-11-04T23:56:06Z |
| 9 | 11381540018 | 8722374 | sha256:777773aaec4495befb8c79977d34538436a6ddbf562657d9078ce11dc507b7d7 | 2026-11-04T23:56:04Z |
| 10 | 11381382104 | 8781953 | sha256:f5ee0aad99a400cc010d62248fdf2b32160b18ffb9ac4f3af7d5eadb23451812 | 2026-11-04T23:56:05Z |
| 11 | 11381102203 | 8727865 | sha256:39ec74fcab0236bc992578f30882ee5c279c00e9ba1955d8796404ad2843ee36 | 2026-11-04T23:56:03Z |
| 12 | 11381506870 | 8783990 | sha256:68fb69cbd5a4800582cf38aba5a42a1417e9d0ad9c7d4a3e51fa7e666474a22e | 2026-11-04T23:55:14Z |
| 13 | 11380384653 | 8731153 | sha256:5bceb43b753df9e1513265d73614e9a18ab5dce49b4280ec136c1486b481200a | 2026-11-04T23:55:08Z |
| 14 | 11380714344 | 8789338 | sha256:2c73fcb2135c2bd74ff1ed266021ac24830ebb79191a362285e71972a304314f | 2026-11-04T23:55:14Z |
| 15 | 11380908751 | 8735083 | sha256:a75461952a41cc54a2f522fb7afc9ba83f17fd2fe7d1950e795037b30379d2b7 | 2026-11-04T23:56:19Z |

## Confirmatory readout artifact

- artifact id: `11381590034`
- name: `chapter2-1005-confirmatory-result`
- bytes: `8297`
- SHA-256: `sha256:7c5c252cf559067f218bbd9f37b74b00c5d9c52fe30f25bb0196c9bfb9cb4872`
- expires: `2027-01-03T23:52:59Z`
- committed compact result:
  `data/results/chapter2_1005_confirmatory_replication_20261006.json`

The compact committed result is not a substitute for the raw shard archive,
because history-level re-analysis requires the case NPZ/receipt files.

## Permanent deposit contents

Deposit one immutable record containing:

1. all 16 raw shard ZIPs above;
2. `data/design/chapter2_1005_confirmatory_replication_20261006.json`;
3. `data/results/chapter2_1005_confirmatory_replication_20261006.json`;
4. `scripts/run_chapter2_1005_confirmatory_replication.py`;
5. `scripts/summarize_chapter2_1005_confirmatory_replication.py`;
6. the source commit SHA and this manifest;
7. a top-level checksum file for every deposited object.

Recommended record title:

> **Independent confirmation data for sequence versus causal necessity in the izu-core Model 3 plant–pollinator experiment**

The deposit description should state explicitly that the fixed-assurance
experiment blocks **evolution of reproductive assurance capacity**, not the
existence of assurance or realized selfing.

## Local recovery recipe

With GitHub CLI authentication that can read the repository, each artifact can
be recovered before expiry using its numeric id. For example:

```bash
mkdir -p chapter2_1005_confirmatory_raw
gh api repos/zuizui0223/izu-core/actions/artifacts/11381221933/zip \
  > chapter2_1005_confirmatory_raw/shard-00.zip
sha256sum chapter2_1005_confirmatory_raw/shard-00.zip
```

Repeat for all ids in the table and verify against the listed GitHub artifact
digests before uploading to the permanent repository. Preserve the ZIPs
unchanged so the recorded GitHub artifact digests remain directly checkable.

## Publication rule

The manuscript/Data Availability statement must cite the permanent record once
it exists. GitHub Actions artifact URLs alone are not a durable data citation.
The committed compact summary may remain the fast audit surface; the permanent
record is the history-level reproducibility source.
