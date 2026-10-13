# Q1 → Q2 clock pilot: source-bound native-birth technical gate

**2026-10-13. Technical implementation and original-input receipt, not the pilot or an independent evolutionary result.**

This step checks whether the already declared 2×2 hidden genetic-access manipulation can be passed through the **original Model 3 types, full female/paternal/self reproductive ledger, native parent-pair lottery, Mendelian segregation, A-only mutation and density-recruitment operator** without changing original biological source code. It neither estimates nor tests a two-trait evolutionary response clock. The 1,536 predeclared 200-update pilot remains **not dispatched**.

## Historical source and typed-original-input gate

At historical biological commit `328548612e93469fcc8663f24548530a57399b9a`, the following **unchanged Git blobs** were independently compared with the proposed PR branch:

| Original operator | Git blob SHA-1 |
| --- | --- |
| `types.py` | `0bc427b3261e7baf1651648ee879b368f9bf935b` |
| `reproduction.py` | `95314698a3296b6f13b8c053c36f2df0b7b744ca` |
| `population.py` | `20e90f249f63e9f37e8801d19d9b75cade2fe193` |
| `randomness.py` | `46f1ee55899e729cdd09d9dbb9332694ef1e2071` |
| `history.py` | `0c58aee6f73ae133d96d8da4dd6678886ff3061c` |

The byte-preserved original provider ZIPs for context 0 (no visitors), 3 (matched) and 4 (separated) were checked against their immutable SHA256s. The fixture [`data/design/chapter2_clock_original_t0_typed_fixture_20261013.json`](../data/design/chapter2_clock_original_t0_typed_fixture_20261013.json), Git blob `4b529cce12bc44e06d43a22b10c325a52bbd967b`, stores **only archived time-zero arrays** (`ids`, `alleles`, `allele_origin`, `mutation_flags`, `birth_years`) and the complete original typed configurations/first annual return totals for two founder blocks. Its source is exactly six original t0 NPZ cases, not a newly regenerated founder population.

A separate container-side readback compared **30 original array byte streams across six source cases**, all original NPZ SHA256s, stored configuration objects and the eight original source-return totals per case. All matched. This is a raw-source admission, **not** a native-birth test result.

## Technical fixture and assertions

Implemented in [`scripts/audit_chapter2_clock_native_birth_technical_20261013.py`](../scripts/audit_chapter2_clock_native_birth_technical_20261013.py) and the corresponding focused test.

- **48 technical fixture paths**: two original founders × three original visitor conditions × two A-allele half-widths (`.046875`, `.078125`) × two I-hidden homolog states (`h=0`, `h=1`) × **two distinctly salted technical streams**.
- **Exactly three Model3 updates per path**, 144 technical state advances. Technical salt is `chapter2-clock-factorial-technical-3step-v1-20261013`, **not** the 1,536-case pilot salt. The same `(founder,technical_repeat)` master stream is reused across its 12 nested arms/visitor contexts and instantiated fresh for each comparison.
- Check all five exact source module Git SHA-1s before any native `reproduce` or `advance` call. The original `Config.from_dict`, `PlantState`, `VisitorState`, native `population.advance` and `population.inherit` are **imported unchanged**. Use only a source-authenticated, immutable original t0 genotype/config fixture.
- At time zero, compare native maternal/paternal/outcross/self and pollen reproductive totals with the preserved original first-year returns; apply original <1e-12 numerical tolerance for source cross-runtime totals, and require bytewise same-environment ledger equality across the four hidden-genotype treatments.
- At each of three steps, verify source/next census, unique original parent IDs, resident-only recruits, zero adult survival/seed immigrants, exact `parentage` child-parent links, conservation of outcross plus viable selfed contributions, and next-state hashes for **alleles, allele origins, mutation flags, IDs and birth years**.
- Clone the segregation/mutation RNGs immediately before the native `advance` call. With the actual newly recorded parents, independently call native birth-only `inherit` under the **unchanged** biological source and compare every resulting child field exactly. Shadowed no-mutation birth isolates transmitted M/I alleles and identifies A-only **new** mutation changes without treating inherited mutation flags as current-birth events.
- Recreate each technical path from fresh streams and compare every row/hash identically. Read in all 48 original technical starts, including any extinct state; no outcome category is estimated from a three-step fixture.
- The checksum/provenance gates fail closed if historical model bytes, fixture bytes, parentage, mutation locus, source t0 reproductive law or technical seed identity differ.

## Results admission policy

The code, fixture and test were committed on PR #496. The three-version GitHub CI `pytest` jobs execute these technical paths as source-bound regression tests and **must return success before this scope is labelled executed and passed**. Full CI status and its exact executing source SHA should be captured separately after completion. Do not claim published 48-path source-derived results merely because a local test body or the historical original t0 source was accepted.

If CI fails: first isolate the failing source, code, or test invariant; do not substitute a numerically convenient source, relax original hashes or turn technical cases into biological pilot repeats. Repair on the same design, preserve the old failure, rerun focused tests, and recheck independent historical signatures. The registered 1,536-trajectory pilot is a **distinct authorized/execution gate**; neither technical success nor this memo authorizes its dispatch. Pilot predictor/null score contract is also not yet independently frozen.
