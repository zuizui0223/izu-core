# Chapter 2 two-stage clock: source-bound pilot input registry

**2026-10-13. Immutable original-input registry, not pilot execution or scientific confirmation.**

## What is now reproducible

The independent source registry starts from the three **original, non-regenerated** ecological-order provider archives (contexts 0, 3, 4). Each original ZIP, each original founder's r0 NPZ payload, the five typed founding arrays (IDs, two homologs at all three loci, allele origin, mutation flags, birth year) and the original full Model 3 config are authenticated against the archived immutable hashes. Founders are checked across all three visitor contexts rather than quietly using context-zero genotypes for unrelated environments.

The registry covers exactly **2 founder blocks × 64 new salted stochastic stream clusters × 3 ecological contexts × 2 assurance half-widths × 2 I-hidden homolog settings = 1,536 cases**; if approved for execution, each case has exactly 200 Model 3 updates, **307,200 total**. Each founder×seed stream is shared by its twelve nested ecological/genetic arms; seeds are distinct between founders and random draws are not statistically independent across twelve arms. No biological populations have been advanced.

The 8 counterfactual founding genotype hashes agree with the separately registered pre-execution feasibility readout already on PR #496. Every individual initial expressed M/I/A phenotype remains unchanged under the hidden-homolog assignment. The fixed Model 3 source blobs, mutation mask `(False,False,True)`, visit regimes, sampling horizon and original endpoint rule `(0.05, 20 consecutive censuses, tie<=5)` are not changed.

Machine-readable deliverables:

- `data/design/chapter2_clock_factorial_pilot_registered_inputs_20261013.json`: all 1,536 case IDs, 128 master seeds, six original configuration and first-census field signatures, eight modified genotype signatures, and SHA-256 of the exact expanded input tuple inventory.
- `scripts/register_chapter2_clock_factorial_pilot_20261013.py`: the sole proposed byte-verified input registry. Its `--design` CLI must match the original **Git blob `75d49de2781a240c14bdc3f9106212b0dbbda6aa`**, not just a schema/version label. The three provider archives and their per-case original receipts must match. Uses exclusive output file creation; never overwrites a prior registry.
- `scripts/verify_chapter2_clock_pilot_input_manifest_20261013.py`: an independent implementation: reconstructs original first census arrays from source ZIPs, recalculates every genotype SHA and all case IDs, checks canonical task inventory hash and 128 cluster seeds. Does *not* import the registry generator or the biological operator.
- `data/design/chapter2_clock_pilot_manifest_independent_receipt_20261013.json`: independent readback status **`ALL1536_REGISTERED_INPUTS_AND_ORIGINAL_FOUNDER_BYTES_INDEPENDENTLY_MATCH`**, with **108 source/checksum checks**, exact full case-inventory SHA-256 `d0bc8f750650c9fa94e8e1b4eefeac9357ecd9e484db21cb69737760e683c956` and new biological history count zero.
- `tests/test_chapter2_clock_pilot_input_manifest_20261013.py`: source/protocol pin, all-case inventory, original genotype hashes and seed pairing, phenotype preservation and deliberate tampering rejection. The tests do not run the 1,536-case biological study.

The generator compactly stores the 1,536 complete deterministic *keys* plus 128 master seeds, and uses six source-config and eight genotype hash lookup tables rather than repeating identical full config documents 1,536 times. Its expanded per-case tuple has its own SHA-256 in the independent readout. No ambiguity in source config, genotype, random history or source step mask is permitted.

## What is **not** yet claimed or authorized

1. The previously failed Python 3.11/3.12 technical ledger check on PR #496 was diagnosed as a cross-NumPy source-checksum error. Its repair awaits all-three-version CI success (see PR #496, [CI 38356542933](https://github.com/zuizui0223/izu-core/actions/runs/38356542933)). The independent input registration here **does not** satisfy the 48×3 native inheritance/demographic gate.
2. A full **200-update** prospective producer with genome, parentage, population, pollen/maternal/paternal/self history, deterministic event/category and immutable output/zip/reuse guards has **not** been implemented and independently reviewed in this PR. Do not replace the source Model 3 with a reduced shortcut.
3. An independent reader reproducing *all* 1,536 raw genome histories without relying only on the producer's event labels has not yet been admitted. A finished output is not science-ready until every source case and all six outcome categories are validated.
4. The pilot is for **variance/feasibility exploration**, not confirmatory evolution timing evidence. The two-stage access→selection clock, stronger ecological-interaction null, calibration method and confirmatory trial size must each be independently frozen *before entirely new independent confirmation histories*. The exploratory pilot cannot support Q4 natural-order-caused persistence.
5. Do not dispatch any biological pilot under the current design-only PR or revise its original parameter/threshold/horizon after observing new outcomes. Do not promote an incomplete CI or turn an unverified input package into a completed run.

## Reproduction commands (source ZIPs must be the frozen originals)

```bash
python scripts/register_chapter2_clock_factorial_pilot_20261013.py \
  --design data/design/chapter2_clock_factorial_pilot_protocol_20261013.json \
  --original-shard-0 original-shard-0.zip \
  --original-shard-3 original-shard-3.zip \
  --original-shard-4 original-shard-4.zip \
  --out newly-generated-pilot-inputs.json
python scripts/verify_chapter2_clock_pilot_input_manifest_20261013.py \
  --manifest newly-generated-pilot-inputs.json \
  --original-shard-0 original-shard-0.zip \
  --original-shard-3 original-shard-3.zip \
  --original-shard-4 original-shard-4.zip \
  --out fresh-independent-receipt.json
```

The committed full inventory is not replaced with a later look-alike. A new recomputation must be compared with the published exact input/task signature before the first biological trial.
