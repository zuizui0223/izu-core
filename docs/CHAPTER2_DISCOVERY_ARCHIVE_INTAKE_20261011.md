# Chapter 2: intake for the original discovery archive

**2026-10-11 — executable archive verification; no new biological result.**

The original discovery archive remains unrecovered in this task. The new
[intake command](../scripts/audit_chapter2_discovery_archive_intake_20261011.py)
checks an available candidate against the historical external receipt and the
complete positive-mutation endpoint cohort. It does not execute a model or
replay a trajectory. The [recorded intake status](../data/results/chapter2_discovery_archive_intake_status_20261011.json)
contains the actual result of this task's attempt; synthetic test archives do
not establish historical archive availability.

## 1. Exact input and bounded coverage

The required candidate is `model3_replenishment_evolution_20261005.zip`:

| Property | Frozen expectation |
|---|---|
| External archive bytes | 763,914,318 |
| External SHA256 | `37bd0bd312734715392add19f424696121fbe88517dfa784d8e702173ec71b6c` |
| Packaged trajectories | 13,312 |
| Manifest file records | 26,671 |
| Total ZIP entries | 26,673: the recorded files plus `ARCHIVE_MANIFEST.json` and `RESTORE.txt` |
| Discovery endpoints required by this intake | 2,048: two settings × 64 histories × eight demographic repeats × two arms |
| Discovery histories | 76001–76064 |
| Demographic repeats | 7101–7108 |
| Mutation probability covered | .01 |
| Annual trace | 1,001 censuses × 10 columns; 1,000 updates |
| Diploid genome checkpoints | t = 0, 200, 400, 1000 |
| Embedded source/configuration files pinned by the design | 23 |

These expectations come from the [external archive receipt](../data/results/model3_replenishment_archive_20261005.json),
[frozen replenishment design](../data/design/model3_replenishment_evolution_20261005.json),
and [original archive builder](../scripts/archive_model3_replenishment_evolution.py).
The receipt's `members` field is the number of manifest file records. The
builder adds two metadata entries after those files; treating 26,671 as the
total ZIP entry count would reject the intended archive.

The 13,312-case package includes 11,264 intermediate-distance trajectories.
The discovery readout uses only the 2,048 reused endpoints at distance 0 and 3.
All declared manifest files are hash-checked, but the semantic case validation
described below covers these 2,048 endpoints. It does not revalidate or analyze
the intermediate-distance experiment.

The near endpoint is the evolving population in
`outputs/model3_full_mutation_20261004/core_<setting>_u0.01_h<history>_r<repeat>_near`.
The far endpoint is in
`outputs/model3_persistent_isolation_20261005/persistent_core_<setting>_u0.01_h<history>_r<repeat>_far`.
Each complete basename has both `.npz` and `.json` files. The full-mutation
experiment's far arm is not this persistent-isolation far arm.

Settings are `assurance_cost` (delayed selfing, direct cost .5) and
`prior_selfing` (prior selfing, direct cost 0). The independent confirmation
histories beginning 26100601 and the actual PR #411 histories beginning
26110601 are different populations. Their archives cannot satisfy this
intake. See the [cohort identity note](CHAPTER2_SOURCE_REPLAY_COHORT_IDENTITY_20261011.md)
for their separate questions and founder definitions.

## 2. Verification before acceptance

The command first authenticates its committed receipt and design, then the
candidate ZIP's full byte count and SHA256. A self-consistent manifest inside
an unrecognized ZIP cannot establish historical identity.

For the authenticated candidate, it checks that the ZIP and manifest have
the complete, unambiguous path set and that each declared file has its
recorded byte count and SHA256. Duplicate and noncanonical member paths are
rejected. It then checks the embedded design and the design's 23 original
source/configuration hashes using raw bytes; line endings are not normalized.
The embedded design must have the same parsed values as the trusted design;
its original raw bytes are authenticated by the manifest and outer ZIP hash.

Every required discovery case must have its original task identity, matching
NPZ/receipt hash, full trace and all four genome checkpoints. The case
validation retains the original empty-population representation: census zero
with undefined trait summaries, rather than an invented mean genotype.
For occupied checkpoints it recomputes the original mean, variance and unique
allele counts from the saved arrays. Means and variances use an absolute
readback tolerance of `1e-12`; unique counts must agree exactly. This numerical
consistency check does not change a biological event threshold or relax the
outer ZIP's exact byte identity.
No partially checked collection receives the complete intake status.

The command reads the archive without extracting files or importing archived
source code. It has no option to skip the external identity check, replace
the expected hash, change the cohort, or run a biological simulation.

## 3. Run and interpret the result

From the repository root, once the original ZIP is available:

```bash
python -m scripts.audit_chapter2_discovery_archive_intake_20261011 \
  --archive /absolute/path/model3_replenishment_evolution_20261005.zip \
  --out outputs/chapter2_discovery_archive_intake_20261011/intake.json
```

| Status | Exit code | Meaning |
|---|---:|---|
| `ARCHIVE_UNAVAILABLE` | 2 | The specified archive could not be read; no historical cases were accepted. |
| `ARCHIVE_INTAKE_REJECTED` | 2 | The archive identity, structure or required content failed a check; the error identifies the failed condition. |
| `ARCHIVE_BYTES_AND_DISCOVERY_ENDPOINTS_VERIFIED` | 0 | The exact package and all 2,048 required endpoint records passed the intake checks. |

The JSON report records the result and limits. A missing input produces a
blocked report instead of a success-shaped placeholder. The output may not
alias the input archive or either fixed input contract (design and external
receipt), including through symbolic or hard links. That error is reported
on standard output without overwriting those inputs.

The [regression tests](../tests/test_chapter2_discovery_archive_intake_20261011.py)
exercise accepted synthetic structures and rejected identities, records and
arrays. These are engineering fixtures. Production acceptance remains tied
to the historical external archive identity.

## 4. What remains after a successful intake

The success status is an archive-admission result. Both
`original_discovery_full_replay_completed` and `runtime_identity_verified`
remain false. The replenishment builder includes the 23 pinned sources but
does not add the original campaigns' `sources.json`/`sources.zip`, the
full-mutation runner, or a lock identifying the historical numerical runtime.
Current checkout files must not be described as byte-identical to those
historical sources without a separate comparison.

The next scientific step still requires an authenticated source/runtime
contract and reproduction of every original full trace and checkpoint before
using newly reconstructed annual genotypes or parentage. The existing
[single-case replay auditor](../scripts/audit_chapter2_sequence_source_genome_replay_20261011.py)
is not converted into a batch runner by this intake.

The full discovery design has 4,096 trajectories, including mutation zero.
This positive-mutation archive intake covers only 2,048; it does not close
the zero-mutation half. The completed [1,024-case tempo accounting](CHAPTER2_TEMPO_REALIZATION_ACCOUNTING_20261011.md)
and the confirmed PR #411 result retain their existing evidence and scope.
There are no new histories, settings, thresholds, bootstrap draws, hypothesis
tests or biological trajectories in this change.
