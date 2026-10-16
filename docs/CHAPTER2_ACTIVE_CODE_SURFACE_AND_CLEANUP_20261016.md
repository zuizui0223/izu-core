# izu-core — Model 3 active code surface, cleanup and retention policy (2026-10-16)

**Action taken:** shrink the practical *entry point and dependency surface*, not erase original research. `main` at cleanup base `09c477c7bbe1094451b6ae79662147e4fda85c0f`. This PR resolves a concrete packaging defect, exposes three safe read-only commands, removes unused imports from recent audit utilities and makes the supported-vs-historical code route explicit. It does **not** delete frozen scientific producer files.

## 1. Which code to use now

| Purpose | Supported path | Mutation / deletion policy |
| --- | --- | --- |
| Biological model, original numerical/finite inference | `scripts/model3_island/{types,reproduction,population,history,randomness,density,tensor_density}.py` | **Immutable for archived-source identity**. Fork/version a new biological operator for sensitivity tests. Never refactor in place for purely stylistic reasons |
| Original 4-setting Q1 | `scripts/run_chapter2_assurance_generality.py` + source design `data/design/chapter2_assurance_generality_20261006.json` | Original 8,448 case evidence and source SHA pinned; no historical rewrite |
| New 8×8 founder/visitor Q1 | `scripts/run_chapter2_q1_fresh_founders_20261016.py` and `scripts/summarize_chapter2_q1_fresh_founders_20261016.py` | Producer pinned to original Actions #38853989138. Reader is independently patchable but must reproduce the original signed 1,088-case readout and 3/4 result |
| Q4 independent32 stress persistence | `scripts/run_chapter2_island_demographic_independent32.py` and `scripts/summarize_chapter2_island_demographic_independent32.py` | Producer pinned; reader supports strengthened input validation. Changing post mutation rates requires a separately approved producer |
| Original packet, supported paper route | `scripts/build_chapter2_unified_el_submission_bundle.py`, `scripts/generate_chapter2_unified_model3_figures.py` and `docs/CHAPTER2_UNIFIED_EVOLUTION_PERSISTENCE_MANUSCRIPT_20261010.md` | Respect 5,000 main words / 150 abstract, S1–S33 source freeze, original figure and raw cohort hashes |
| Operational source integrity | `scripts/audit_chapter2_repository_wide_static_20261016.py`, `scripts/audit_chapter2_q4_post_mutation_contract_20261016.py` and the Q1 readout | Read-only, safe when pointing at verified original inputs. Does not run new biology or approve scientific claims |

**Core source:** there are 21 files in `scripts/model3_island/`. **Broader code:** 593+ standalone `scripts/*.py` research and support modules; 474+ Python tests and 40 workflows. Earlier full-tree grammar check on 1,079 nonlegacy Python sources/134,790 lines passed with 0 syntax errors; it is **not** a proof of all scientific calculations.

## 2. Fixed package-install defect

Earlier `pyproject.toml` declared `dependencies=[]` even though `scripts.model3_island.run` imported NumPy, SciPy, psutil and threadpoolctl. Running `pip install -e .` in a clean environment therefore did **not** install the numerical prerequisites. The cleanup places these four libraries in **actual runtime dependencies**, removes their duplicate listings from the development extras, and keeps Matplotlib as an optional plotting dependency while preserving all scientific reviewer/build dependencies under `.[dev]`.

Read-only command entry points are added without registering old biological-producer runners as click-and-run scripts:

```bash
python -m pip install -e '.[dev]'
izu-core-source-audit --out outputs/active-python-static-audit.json
izu-core-q4-contract
izu-core-q1-readout --input-root /path/to/32-original-shards --out /path/to/new-readout.json
```

The last command **does not** simulate new biological histories and refuses incomplete 1,088 cases or a mismatched original source manifest. For package-only numerical use, `python -m pip install -e .` now declares its imported engine prerequisites. For figures, `pip install -e '.[plotting]'` is also supported. Existing reproducibility commands with `.[dev]` stay compatible.

## 3. Classification for cleanup: preservation first

- **Retain unchanged:** original producer implementations, dates/scientific result manifests, historical frozen workflows and ZIP hashes, `legacy/model2`, original S1–S33, independent failing and inconclusive numerical experiments. More than one algorithm may be retained specifically to document why a numerical approximation did not work. Removing them would weaken reproducibility.
- **May safely refactor after targeted tests:** read-only current result summarizers, source/ZIP admission, review package builders, current tests, current package metadata and documentation. In this PR, remove only actually unused imports and fix packaging. No change to finite/density ecological update equations.
- **Candidates for later verified removal, not automatically deleted now:** duplicate *non-source-pinned* diagnostic scripts, abandoned one-off CLI wrappers, redundant review document indexes, and old manual workflows **only after** manifest / import / workflow references and external raw provenance are checked. Absence of a Python import is not proof that a frozen CLI was never used; GitHub Actions may call a module via shell.
- **Unacceptable cleanup:** deleting entire `legacy` directories or PR-specific scientific code without a source mirror; changing its path while old hashes point to it; consolidating unrelated Q1–Q4 histories; weakening a frozen scientific gate to force CI pass; changing historical result JSONs or manuscript evidence by cosmetic refactors.

## 4. Q4 original-compatible strict replay readback (separate read-only audit)

[Original clean replay run #38272136110](https://github.com/zuizui0223/izu-core/actions/runs/38272136110) contains eight original biological-projection-matched Q4 shard artifacts (512 historical groups, 4,096 future trajectories) and its own readout. These were recovered and independently validated using the new numerical constraints and the **eight previously stored SHA-256 biological projection digests** from [the original/replay receipt](../data/results/chapter2_island_demographic_independent32_replay_receipt_20261013.json).

- **PASS:** 8/8 replay shards exactly match their biological-projection digests; 512/512 groups, 4,096/4,096 postshock stress futures. All terminal N / minimum N / occupied flags / first-extinction times / finite three-trait endpoints / nonnegative female viable per-capita fields passed. **No inadmissible case** was encountered.
- Recomputed integrated interaction `+0.1083984375` and the original history bootstrap interval **[+0.0654296875, +0.1513671875]** matched the stored original raw readout exactly. Among 4,096 futures, 1,231 occupied and 2,865 became extinct (descriptive, not independent replicates).
- **Boundary:** These are clean *replay* shards linked to the original biological state. The separate historical `izu_core_island_demographic_stress_20261008.zip` (**335,015 bytes, SHA-256 `cd9f998e38ec51e747c4495dbe94b1fe1168d48d31ef54a438250bfa0ace5a21`**) was **not directly materialized** in the reviewed session. This is **not** a byte-for-byte re-audit of the original ZIP. No claim that raw source deposition at an external DOI is complete.

## 5. Review gates and nonclaims

The code-surface cleanup must pass exactly matching head commit **Python 3.10/3.11/3.12 full CI** and Chapter 2 scientific gate. The source audit, original Q1 exact genotype readback, Q4 regression tests and packet rebuild are all preserved. This is not an independent ecological model, a solved genetic-mediation identification, or a new empirical island study.

### Active conclusions unchanged

- Original Q1 shared-founder 4/4 positive compression; new registered independent founder/visitor Q1 **3/4 with direct A-cost inconclusive**.
- In the new founder/visitor experiment, far-side investment relative to fixed A declines under delayed selfing and costly assurance; do not overclaim universal far-side protection.
- Q3 density-vs-ABM has different self-pollen/density handling; their discrepancy is not pure drift.
- Q4 historical mode continues evolving A throughout its future; capacity K also changes pollen background in the canonical operator.
- DOE/public data deposition remains blocked under [issue #436](https://github.com/zuizui0223/izu-core/issues/436). Cleanup should preserve all source traces for that deposit.
