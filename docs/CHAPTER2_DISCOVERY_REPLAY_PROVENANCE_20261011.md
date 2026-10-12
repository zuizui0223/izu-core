# Chapter 2: replay comparison and historical provenance

**2026-10-11 — comparison-boundary repair and bounded source-byte recovery.**

The discovery replay tools now distinguish agreement with supplied case files
from authentication of an original archive, executed source, runtime, or
annual genomes. Historical source inspection independently reconstructed
**21 of the 23 pinned replenishment source/configuration byte strings**.
The original discovery ZIP and the remaining historical inputs are still
unavailable. No original discovery case or full annual replay is admitted by
this change. The [machine-readable audit](../data/results/chapter2_discovery_replay_provenance_audit_20261011.json)
records the frozen inputs, Git objects, matching hashes, unresolved sources,
and focused regression evidence.

## 1. Correct the verification claim

The [single-case reader](../scripts/audit_chapter2_sequence_source_genome_replay_20261011.py)
previously set `verified_against_exact_original_archive` to true after a
caller-provided NPZ matched its caller-provided receipt, replay prefix, and
provided checkpoint dictionary. Those checks established internal agreement
only. A fabricated NPZ and its own hash receipt could pass; an empty trace
and empty checkpoint dictionary could also receive the historical-identity
claim. The [paired companion](../scripts/audit_chapter2_sequence_paired_original_replay_20261011.py)
propagated that claim across cases.

Both tools now describe outputs as **current-checkout replay candidates**.
Their v2 schemas retain legacy hash and identity keys, while every historical
identity flag remains false. An archive-root argument supplies files for
comparison; it does not activate an authentication path.

| Report field | Meaning after this repair |
|---|---|
| `supplied_case_record_verified` | The supplied task, receipt hash, full stored trace shape, requested prefix, and reached checkpoints agree. |
| `replay_matches_supplied_prefix` | The requested prefix equals the corresponding supplied trace values. |
| `compared_censuses`, `compared_updates`, `compared_checkpoint_years` | The exact extent that was compared. |
| `full_supplied_record_reproduced` | All 1,001 censuses and all four saved checkpoints were compared successfully. This is still a supplied-file comparison. |
| `supplied_npz_sha256` | SHA-256 of the exact NPZ bytes read for comparison. The legacy `original_npz_sha256` contains the same hash. |
| `verified_against_exact_original_archive` | Always false in this replay reader. |
| `historical_source_identity_verified`, `runtime_identity_verified` | Always false; importing the current checkout does not establish executed historical identity. |
| `original_annual_genomes_verified`, `original_discovery_full_replay_completed` | Always false; neither saved-summary agreement nor a one-case comparison closes these gates. |

The reader requires 2–1,001 censuses with ten columns and exactly the reached
checkpoint years from t0, t200, t400, and t1000. It rejects omitted checkpoints
and checkpoints beyond the compared prefix. Without supplied files, comparison
counts are zero and agreement flags are false. The NPZ is read once: both
the receipt hash and loaded arrays refer to the same captured byte sequence.
A path replacement between hashing and array loading can no longer bind one
file's hash to another file's arrays.

The paired report requires all **16** case comparisons to agree before an
aggregate supplied-record flag becomes true. It reports how many cases were
compared and separately distinguishes complete prefixes from complete stored
records. Its legacy per-case and aggregate archive-identity flags remain
false, including when a legacy child result contains a true identity flag.
Both command-line summaries include these comparison details.

The existing [archive intake](CHAPTER2_DISCOVERY_ARCHIVE_INTAKE_20261011.md)
performs a separate, stronger operation: comparison with the fixed external
archive receipt, manifest, and complete positive-mutation endpoint set. A
successful intake still requires subsequent executed-source/runtime and
replay evidence. This repair does not join these stages or add a bypass.

## 2. Recoverable source bytes: 21 of 23

The [frozen replenishment design](../data/design/model3_replenishment_evolution_20261005.json)
contains 23 source/configuration SHA-256 pins. The audit examined **53 distinct
exact-path Git blob versions** in the complete reachable repository history.
For each candidate it read raw blob bytes, required that they contained no
carriage returns, and tried the single deterministic transformation
`LF → CRLF`. A match requires equality with the pre-existing pinned SHA-256;
similar code, a plausible commit date, or equivalent behavior is insufficient.

All 21 matching blobs coexist at commit
[`2ea05fea7ad51e1ab53a3e7b7d35371170a3925e`](https://github.com/zuizui0223/izu-core/commit/2ea05fea7ad51e1ab53a3e7b7d35371170a3925e).
The base checkout at `1fb98dffd5cb6362722a3f94ac58fe627da1af07` matches only
20 pins after that transformation. Historical `selection.py`, blob
`c603f1cf907336a5ed44a7399f60631ad399d2d7`, supplies the additional exact
match. No model source was replaced in the current checkout.

| Remaining source | Required SHA-256 |
|---|---|
| `scripts/model3_island/birth_diffusion.py` | `534e0b75d441f058327b3904e290ceb189c91f83fb003fb3703da4fa9fe180c2` |
| `scripts/model3_island/tensor_density.py` | `dfe759136daaa8dad0cc4cff917af62823108167fc567817c6cadf137266a4a4` |

Each unresolved path has one distinct blob in the inspected exact-path
history. Neither its raw bytes nor its uniformly converted bytes match the
pin. This does not identify the content or biological effect of the missing
difference. Reconstructing 21 pinned byte strings also does not establish
that a particular checkout or numerical runtime executed the original cases.

The full mapping is in the machine-readable audit. To independently repeat
the common-commit comparison from a complete repository clone:

```python
import hashlib
import json
from pathlib import Path
import subprocess

commit = "2ea05fea7ad51e1ab53a3e7b7d35371170a3925e"
design = json.loads(Path(
    "data/design/model3_replenishment_evolution_20261005.json"
).read_text())
matched = []
for path, expected in design["source_sha256"].items():
    raw = subprocess.check_output(["git", "show", f"{commit}:{path}"])
    assert b"\r" not in raw
    candidate = raw.replace(b"\n", b"\r\n")
    if hashlib.sha256(candidate).hexdigest() == expected:
        matched.append(path)
assert len(matched) == 21
```

This transformation is only for reconstructing candidate source byte strings
against known pins. The production archive intake continues to compare raw
archived source bytes without line-ending normalization.

## 3. Earlier campaign sources and recorded runtime

The [full-mutation result record](../data/results/model3_full_mutation_20261004.json)
has a separate **25-file** source contract. The same Git inspection recovers
**20/25** pinned byte strings. In addition to the two modules above, the
unresolved files are `scripts/run_model3_full_mutation.py` and the two original
full-mutation planning/execution documents. Their exact pins and examined
blobs are preserved in the new audit.

That result records Python **3.10.11**, Windows **10.0.22621**, NumPy **2.2.6**,
and SciPy **1.15.3**, with the runner commands setting both
`OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1`. Its own note says these were
recorded **during the campaign**, rather than locked before launch. These
observations narrow the missing-runtime evidence; they do not authenticate
an available execution environment or prove exact trajectory reproduction.

The most targeted missing source inputs are the original campaigns'
`sources.json` and `sources.zip`, with member bytes checked against the
appropriate frozen source contract. The recorded older raw-archive lead is
`model3_full_mutation_20261004_raw.zip`: **224,236,731 bytes**, SHA-256
`4647eb772303f0b53387227f052bae6ce0aff84d1b056ab3cdf6f71348917c48`.
Its present availability and actual contents have not been verified here.

## 4. Later recovered archives have a different identity

[PR #481](https://github.com/zuizui0223/izu-core/pull/481) preserves 50 original
Actions ZIPs for the later confirmation and assurance-generality campaigns.
The [case audit](../data/submission/chapter2_evolution_original_case_audit_20261011.json)
covers **12,544 cases** in those cohorts. It explicitly leaves original
discovery admission, original-runtime identity, and annual diploid genomes
unverified. Those cases cannot replace the discovery histories 76001–76064.

For each later campaign, all 23 relevant recorded source hashes equal the
raw Git blobs at that campaign's recorded execution head. Uniform LF-to-CRLF
conversion matches the same 21 discovery pins and leaves the same two modules
unresolved. Neither source map supplies the full-mutation runner pin. These
comparisons used the committed audit's source maps and Git objects; no later
archive was represented as the missing discovery archive.

The bounded fresh search of the two named original archives, newly modified
saved files, and GitHub runs/artifacts/releases since **2026-10-11 11:22:59 UTC**
resolved no new discovery-original candidate. This is a statement about the
inspected sources and interval, not universal absence.

The primary missing input remains
`model3_replenishment_evolution_20261005.zip`: **763,914,318 bytes**, SHA-256
`37bd0bd312734715392add19f424696121fbe88517dfa784d8e702173ec71b6c`, as fixed by
the [external receipt](../data/results/model3_replenishment_archive_20261005.json).
The existing intake covers its 2,048 positive-mutation discovery endpoints;
the full discovery design has 4,096 trajectories and includes mutation zero.

## 5. Regression evidence and scientific boundary

The original 20 source/paired tests passed before this repair. New targeted
tests first reproduced 19 source-comparison failures, six paired-report
failures, and the separate hash/array file-replacement failure. After the
repair, the focused run passed **87 tests**: 37 source-reader, eight paired,
and 42 archive-intake tests. An independent reviewer reran that set and
found no blocking defect in the five-file code/test/workflow diff.

```bash
python -m pytest -q \
  tests/test_chapter2_sequence_source_genome_replay_20261011.py \
  tests/test_chapter2_sequence_paired_original_replay_20261011.py \
  tests/test_chapter2_discovery_archive_intake_20261011.py
```

Both replay test files are now included in the active
[scientific gate](../.github/workflows/chapter2-scientific-gate.yml).
Regression archives and metadata fixtures are synthetic. Existing short
current-code compatibility replays are engineering checks, not newly admitted
historical trajectories or a new scientific campaign. No numerical model,
RNG stream, founder, exposure routing, gradient calculation, or frozen event
threshold changed.

The earlier [identity note](CHAPTER2_SOURCE_REPLAY_COHORT_IDENTITY_20261011.md),
archive-intake records, and completed
[1,024-case tempo accounting](CHAPTER2_TEMPO_REALIZATION_ACCOUNTING_20261011.md)
remain dated, byte-preserved evidence. This new report records the later
reader correction and source reconstruction without rewriting their old
code hashes, test counts, or retrieval observations. The tempo accounting is
already complete; the outstanding work is authenticated discovery-source
replay and the annual evidence it would produce. All-adult gradient expansion,
additional histories, and new biological runs are outside this repair.
