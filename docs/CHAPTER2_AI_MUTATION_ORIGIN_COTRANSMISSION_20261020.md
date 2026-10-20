# A mutation-birth I background and short-lived copy co-carriage — source-admitted readout

**2026-10-20 | TECHNICAL, retrospective, no new biological source, no causal hitchhiking confirmation, no independent founder inference.** This is the follow-up to [the corrected A–I founder-origin falsification](CHAPTER2_AI_HITCHHIKING_SOURCE_AND_FALSIFIER_20261020.md). All conclusions and denominators refer to the **same 16 already-exposed short technical replays of the original 2026-10-16 Q1 source**, not 216 independent simulated plant populations, and NOT the original 1000-update experimental outcomes.

## Execution, source identity and engineering gate

- Original source-compatible 16-case Q1 **mutation-birth sidecar** and per-event retention reader already passed [scientific gate 39354816983](https://github.com/zuizui0223/izu-core/actions/runs/39354816983) at historical technical HEAD `cdd643e28e717aec7e4c357dc6324384f58ce071`. The original source biology and frozen PR569 1000-update Q1 output were not edited.
- Corrected, fully logged latest [scientific gate **39362026117**](https://github.com/zuizui0223/izu-core/actions/runs/39362026117) (job `118432233454`; tested head `cab7316a68e40d4aa3c4eeb2b1d2215e0023dea2`) completed **success**. Individual mutation birth and allele-state parity [tests](../tests/test_chapter2_ai_mutation_origin_20261020.py), [carrier-I census readout](../tests/test_chapter2_ai_copy_alignment_20261020.py) and [fixed-age follow-up comparison](../tests/test_chapter2_ai_retention_age_20261020.py) passed, alongside the independent original code audit gate.
- The original [source-compatible recorder](../scripts/audit_chapter2_ai_mutation_origin_20261020.py) shadows Model3's SEGREGATION and MUTATION random streams, checks that alleles, inherited origin IDs, mutation flags, offspring IDs and the terminal trace are identical to [the original PR569 Q1 technical replay](../scripts/run_chapter2_q1_fresh_founders_20261016.py). No edit was made to `model3_island/population.py` or `model3_island/reproduction.py`.
- Each A mutation carries its **specific new mutation-event ID**, the two inherited pre-newborn-mutation I copies, the **actual** newborn I copies after possible same-birth I mutation, mother/father identities, and the most recent A-mutation-token ancestry chain. The follow-up confirms **zero** simultaneous A and I mutation births in these 216 technical A mutation events; the distinction must nevertheless be enforced for future designs. I and A are separately segregating loci, not physically phased chromosome linkage.
- Technical cases are **2 founder genome seeds × 2 visitor history seeds × 2 near/far environments × 2 mating regimes × 12 updates**, generated from only two genuinely distinct original source founder genotypes and two visitor histories. Each setting/arm duplicates substantial seed history; all the original PR569 8×8×4×2×2 1000-update trajectories retain their previous evidence status.

## Original 12-update A mutation birth evidence

| Technical measure | Count |
| --- | ---: |
| De novo A mutation birth events across the 16 path cases | **216** |
| A allele value increased by that mutation | **112** |
| A allele value decreased by that mutation | **104** |
| Original A mutation token IDs still present at common update12 | **75/216** |
| Latest-original-tagged A allele copies at update12, summed across all 16 paths | **204** |
| Mutation birth on I higher than **own founder's** mean | **123** |
| Mutation birth on I lower than own founder's mean | **93** |

**Naive terminal-presence comparison:** higher-I original A mutation tokens present **47/123**, lower-I **28/93**. A-positive-only tokens are **34/67** versus **18/45**. These are *not comparable exposure durations*: A-increasing events with high-I backgrounds were born with mean remaining follow-up **4.418 updates**, whereas A-increasing events with low-I backgrounds had **5.867 updates**. Late-born mutants have fewer opportunities to disappear before the fixed common endpoint; this directly biases the naive 12-update denominator. Event tokens can be replaced by later A mutations on the same homolog; current-tag loss is not proof that all genealogical descendants disappeared.

## Mutation-token retention at EQUAL post-birth age: more discriminating

The [age-matched source-only reader](../scripts/audit_chapter2_ai_retention_age_20261020.py) uses only native per-census original event-token counts. For each age `h`, eligibility requires original mutation birth at least `h` updates before the last technical update12. Retention is the same **specific, latest A mutation token ID** present after exactly `h` updates; no mutation ages are imputed for later-born events. No significance test or pseudoreplicated standard errors are calculated.

| A mutation direction | Post-birth follow-up | High-I-at-birth event IDs retained / eligible | Low-I-at-birth event IDs retained / eligible |
| --- | ---: | ---: | ---: |
| A increases | birth (`h=0`) | 67/67 | 45/45 |
| A increases | **1 update** | **42/58** | **27/38** |
| A increases | **3 updates** | **27/53** | **14/35** |
| A increases | **6 updates** | **3/26** | **5/22** |
| A decreases | birth | 56/56 | 48/48 |
| A decreases | **1 update** | **22/56** | **26/48** |
| A decreases | **3 updates** | **13/50** | **16/46** |
| A decreases | **6 updates** | **2/26** | **4/22** |

**Observed interpretation:** For positive A mutations, the apparent high-I-origin token advantage seen in naive terminal presence is **not stable after standardizing available post-birth follow-up**: high/low retention is 72.4%/71.1% at age1, 50.9%/40.0% at age3, and **11.5%/22.7% at age6**. At all fixed ages and signs, age eligibility remains a subset of the exact 216 all-birth source event ledger, with **216 eligible at age0, 200 at age1, 184 at age3 and 96 at age6**. This age-matched record does **not** fix differences in *calendar birth year/ecological history*, effects on background viability, mutation sign/magnitude, case dependencies or native I selection. The changing sign means no robust continuous **high-I A-mutant origin advantage** is established by this cohort.

## Same-census I backgrounds of A mutation-tagged versus untagged A copies

At each census the original source genotype assigns each A mutant tag's carrier individual's current **diploid I mean** to that tag's A homolog copies. This is **copy-weighted same-individual association**, NOT physical phased A–I linkage, recombination fraction, an independently evolved trait covariance or a direct causal effect. A copy is untagged if no new A mutation has been recorded on its exact homolog lineage; a later A mutation replaces the previous tag.

Below is the **unweighted average among four artificial cases in each setting/arm** of `mean I among A-tagged A homolog copies − mean I among untagged A copies`.

| Q1 source setting | Visitor regime | Census 3 | Census 6 | Census 9 | Census 12 |
| --- | --- | ---: | ---: | ---: | ---: |
| delayed_control | near | +0.030682 | −0.007614 | +0.004228 | **−0.002575** |
| delayed_control | far | +0.080001 | −0.002801 | +0.037416 | **+0.052160** |
| assurance_cost | near | +0.030323 | −0.003539 | +0.020919 | **+0.015629** |
| assurance_cost | far | +0.077082 | −0.019542 | +0.031713 | **+0.039664** |

This temporal pattern changes sign even **within the same artificial mating regime**; it is **not monotonically linked** to a higher-I fate. The four values per arm are not four independent founder×visitor populations, and each census is serially correlated.

## Scientific answer and next experiment

**Confirmed technical feasibility:** New A mutation origins and their I background can be traced through the native diploid source process, preserving all original genotype and mutation RNG semantics. Matching the time at risk reveals that the initial high-I vs low-I terminal retention comparison could be misleading.

**NOT confirmed:** A new mutant on high I has higher true fitness, selective spread causes higher I, A–I hitchhiking explains PR #569 fresh-founder sign reversals, genetic linkage between A and I, or a universal stochastic/deterministic hierarchy. Direct I fitness and mutational changes in I/M continue, and reproduction is conditioned on inherited individual genotype, family size and pollen interactions. No mutation-origin causal knockout or independent full-history study has been performed.

**Next discriminating, prospective biological contrast:** In an independently fixed source × visitor design, cross A mutation permitted versus prohibited with I direct reproductive-payoff expression active versus neutralized, recording full A-mutation I-background pedigrees. Add a locus-diplotype-swap or meiosis-preserving conditional parentage control **without conflating recombination with altered mate choice or offspring counts**. Require whole-source and whole-visitor heldouts, a biological minimum-interest threshold and complete all-start case accounting before a causal claim. Existing [PR #609](https://github.com/zuizui0223/izu-core/pull/609) remains the single supported Q1–Q4 paper. Draft [PR #610](https://github.com/zuizui0223/izu-core/pull/610) remains a technical research branch.
