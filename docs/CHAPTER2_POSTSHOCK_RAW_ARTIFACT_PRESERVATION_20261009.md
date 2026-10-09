# Chapter 2 postshock raw archive: original GitHub artifact inventory (2026-10-09)

**Status: 390 artifact metadata records frozen; original archive ZIP bytes have NOT been permanently deposited.** This is an urgent preservation receipt and action contract, not a new experiment or a scientific effect estimate.

Machine-readable inventory: [`data/design/chapter2_raw_actions_artifact_inventory_20261009.json`](../data/design/chapter2_raw_actions_artifact_inventory_20261009.json). The inventory was created by listing **both pages** of the GitHub Actions artifact API for each original production run, not by reading only the first 100 results. Each record retains exact GitHub artifact ID, name, reported ZIP size, GitHub-supplied SHA-256 digest, creation time and expiration time. All were unexpired when inspected.

| Original campaign | Run | Raw/state shards | Artifacts including admissions/readouts |
| --- | --- | ---: | ---: |
| Independent fixed-eight t400 source states | [37887039116](https://github.com/zuizui0223/izu-core/actions/runs/37887039116) | 64 diploid | 65 |
| Their independent future branches | [37887290489](https://github.com/zuizui0223/izu-core/actions/runs/37887290489) | 64 future | 65 |
| New orthogonal K×B cohort | [37893126472](https://github.com/zuizui0223/izu-core/actions/runs/37893126472) | 64 diploid + 64 future | 130 |
| New fixed-B48 K-confirmation cohort | [37896872795](https://github.com/zuizui0223/izu-core/actions/runs/37896872795) | 64 diploid + 64 future | 130 |
| **Total** | 4 source runs | **128 diploid + 192 future shard sets** | **390 artifacts** |

The GitHub-reported total compressed ZIP payload is **approximately 646 MiB**. For the sampled artifacts, expiration is **2027-01-07 UTC** (the inventory contains each record's exact expiry). GitHub Actions retention is not a permanent data repository. This manifest alone cannot reconstruct a raw genotype, a birth pedigree, or a future occupancy outcome.

## Required irreversible-free preservation operation

1. Enumerate **every page** of the original `/actions/runs/{run_id}/artifacts?per_page=100` API. Confirm exactly 65/65/130/130 artifact records and no duplicate names or IDs. Use the frozen inventory as the independent expected set.
2. Download **all 390 original ZIP bytes**, individually by the verified artifact ID; never infer that `actions/download-artifact@v4`'s first 100 discovered artifacts equals the complete raw archive. Reject any missing, expired, HTTP-failed or empty response.
3. Check each downloaded ZIP SHA-256 against its GitHub-reported `github_archive_sha256`. Validate ZIP structure and preserve exactly the original bytes (not only extracted JSON, not regenerated histories).
4. Store the original verified ZIPs and inventory in a durable versioned research repository with retention beyond the 90-day GitHub Actions TTL. Preserve immutable source run SHAs and provenance, and mint a stable DOI/record URL if the deposit provider allows it. Do not make a DOI claim before a successful deposit.
5. **Download again from the independent deposit**, verify its 390 SHA-256 hashes, then extract archives and rerun all 64-history raw source/future admission gates and the existing immutable verdict checks. Keep failed old null/negative results, exploratory/confirmatory labels, and earlier `inconclusive` primaries.
6. Only after those gates succeed, record the deposit's exact DOI/URL and verification receipt in the manuscript Data Accessibility / `REPRODUCE.md`.

**Currently completed:** source-run success and earlier whole-cohort scientific admission, immutable readout JSONs committed under PRs #435, #440 and #442, plus complete artifact metadata enumeration for four original runs. **Not completed:** 390 original ZIPs transferred to a durable off-GitHub repository, independent re-download verification, or DOI assignment.

Track the actual deposit under [Issue #436](https://github.com/zuizui0223/izu-core/issues/436). No selective re-simulation or outcome-directed hypothesis adjustment is permitted as a substitute for preserving original raw states.
