# Secondary colonisation: genealogical-descent audit (2026-10-20)

**Scope:** technical readback of the existing 240 archived exploratory futures in PR #611, not 240 new independent ecological replicates and not a biological-model replication.

The original experiment's endpoint is **retention of alleles at the three Model3 selected loci** (M/I/A). The name "source lineage" in the first exploratory result must not be confused with either (i) a source-descended family tree or (ii) genome-wide or neutral ancestry. In a recipient containing resident conspecifics, recombination and interbreeding can preserve descent even after every tracked source allele has disappeared. Recipient occupancy can also persist without any migrant descendants.

This addendum defines separate, auditable outcomes at every census:

| Endpoint | Operational definition | Does NOT prove |
|---|---|---|
| Total recipient occupancy | Any plants remain | Migration succeeded |
| Migrant genealogical descendants | Native parentage graph still connects at least one current individual to an original migrant founder | Neutral or selected migrant allele remains |
| Migrant ancestry proportion | Expected pedigree fraction, with each newborn receiving half its genealogical fraction from each parent | Actual realised genome-wide ancestry |
| Selected source allele persistence | At least one original migrant allele at M/I/A remains | Independent migrant population or genome-wide genetic diversity |

The replay function reconstructs original dispersal, settlement, native reproduction, and finite sampling with the **same frozen seeds**. At every census it first compares its original ancestry summary to the archived census, refusing to publish if even one recorded biological endpoint differs. It then reads the already-returned native parentage table to propagate genealogical weights. No new allele, cost, selection operator, or RNG call is added to the original population dynamics. Any selected source allele must have a nonzero migrant pedigree. A pedigree can persist without surviving alleles at the model's three selected loci; that is **not** evolutionary or demographic recovery proof.

Full archive input: download EXPLORATORY.json from [Actions run 39366132489](https://github.com/zuizui0223/izu-core/actions/runs/39366132489). The archive includes a source fingerprint; readback requires exact agreement with the unmodified producer, protocol and native operator bytes. It also requires all **240 futures**; it cannot silently admit a favorable subset. Source donor extinctions and zero-settlement paths remain in denominators.

Command from repository root:

    python -m scripts.secondary_colonization_pedigree_audit_20261020 \
      --read-only-replay \
      --original PATH_TO_ARCHIVED_EXPLORATORY_JSON \
      --out NEW_PATH_TO_PEDIGREE_READBACK_JSON

This script is an **engineering and descriptive separation of endpoints**. Do not call the outcome a neutral-marker experiment, a true geographic mainland reinvasion, self-sustaining migrant establishment, or a significant advantage of evolved assurance. The pilot has only four founder × visitor blocks and nested stochastic futures. Independently randomized genetic-background swaps and matched propagule interventions are still necessary for isolating a causal A mechanism, while an independently sampled destination population study is required before biological generalisation. The existing selected-locus results remain unchanged.


## Review correction and archive-admission repair (2026-10-20)

The original pilot protocol is retained byte-for-byte for provenance. **Erratum to protocol lines117–119:** loss of all tracked M/I/A source alleles means selected-locus marker loss, not migrant genealogical extinction. Descendants can persist without retaining those selected markers. This correction also governs interpretation of the original `source_lineage_present_at_horizon` field.

The replay now requires the original archive byte SHA-256 through the independent archive checker before CLI execution. Both the direct dictionary entry point and CLI reject anything other than the frozen two-founder/two-visitor identities and all240 distinct allocated keys, before biological replay begins. Fingerprint comparison canonicalizes only path separators, rejects duplicate canonical keys and retains exact source-byte hashes. The original producer and frozen protocol bytes are unchanged, preserving compatibility with the Ubuntu archive on Windows. Full replay status is recorded separately below; passing technical tests is not evidence of a completed full replay.


## Completed full-source replay (2026-10-20)

The repaired auditor completed **240/240 original futures**, with exact native census-readout parity at all21 censuses per path (4,800 original updates replayed; **zero new independent scientific samples**) on Windows. The original archive SHA-256 was admitted before any replay. [Verified summary and provenance](audits/CHAPTER2_SECONDARY_COLONIZATION_PEDIGREE_VERIFIED_20261020.json) records all30 groups and the full replay-output digest; this supersedes earlier statements that the full replay was unexecuted.

In the resident mainland-like recipient at distance1.5, t25 fixed/evolving histories retained selected loci in **2/8 versus4/8**, but genealogical descendants in **4/8 versus6/8**. In each arm two futures retained descendants after losing every selected source marker. All recipient communities remained occupied8/8. These nested descriptive counts demonstrate the endpoint distinction, not a significant A-policy advantage, independent establishment, genome-wide ancestry or adaptation. The original frozen source results and protocol bytes remain unchanged.
