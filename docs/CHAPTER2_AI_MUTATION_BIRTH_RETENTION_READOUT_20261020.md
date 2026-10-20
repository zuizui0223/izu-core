# De novo assurance A origins, their inherited I backgrounds and 12-update mutation-tag retention

**2026-10-20 | SOURCE-VERIFIED, POST-OUTCOME TECHNICAL REPRODUCTION, NOT LONG-RUN HITCHHIKING CONFIRMATION.** The [bounded PR569 parity/replay and exploratory post-birth grouping](https://github.com/zuizui0223/izu-core/actions/runs/39354442834) completed the `scientific-gate` job **success** at source commit `0ac4a4419f7aa51724524b1a8febee1f98e70f40`, job `118406051521`. The exact genome/segregation/mutation/native-run replay gate and the follow-up bounded data grouping were independently *tested against their software contracts*, **not against an independent biological model or field system**.

## Provenance and biological identity

- Original founder genotypes and pollinator-history seeds drawn from the **previously completed** PR #569 study: two frozen founder seeds (560201–560202) × two previously used visitor-history seeds (560301–560302) × near/far replenishment × delayed_control/direct_assurance_cost mating = **16 technical paths**. The 1,000-update frozen experiment remains untouched. These 16 paths share source founders, visitor RNGs and sometimes early mutation RNG; they are **not 16 independent ecological histories**, and paired repetitions of early mutation births are not independent mutant origins.
- Exactly **12 original reproductive updates per path**, unchanged native `reproduce()`, `advance()`, `inherit()`, source A mutation rate .01 and mutation SD .05. **All full diploid terminal genotypes, all source traces and entire shadow mutation/segregation stream state passed source parity.**
- Prior to births all A alleles of the original PR569 founders are exactly 0.5; initial `Cov(A,I)=0`. New mutations appear **after settlement in the synthetic Q1 histories**, not in the original t0 founder pool. The tracer annotates each new A mutation with parent IDs, mutation value, two inherited I copies, an independent uniquely named A mutation birth ID and subsequent exact A-homolog token transmission.
- The token's last-census disappearance is NOT necessarily genealogical extinction: a later A mutation can replace a token label on a transmitted homolog. Retained token copy count is not an expected fitness, selected founder frequency or survival probability.
- Readout grouping code: [`scripts/audit_chapter2_ai_mutation_birth_retention_20261020.py`](../scripts/audit_chapter2_ai_mutation_birth_retention_20261020.py), [tests](../tests/test_chapter2_ai_mutation_birth_retention_20261020.py); original recorder: [`scripts/audit_chapter2_ai_mutation_origin_20261020.py`](../scripts/audit_chapter2_ai_mutation_origin_20261020.py).

## Full technical event inventory

**216 annotated new A-mutation birth events (not independent sample units)** in the 16 technical paths. At census 12, **75 mutation event IDs** remain represented, totaling **204 current A homolog copies** carrying one of those original mutation IDs (or direct unreplaced descendant copies).

| A mutation effect at its original birth | Birth events | Birth-token IDs still present at census12 | Census12 tagged A copies |
| --- | ---: | ---: | ---: |
| Positive | 112 | 52 | 128 |
| Negative | 104 | 23 | 76 |
| Zero value change | 0 | 0 | 0 |
| **All** | **216** | **75** | **204** |

| Mutant child's I-background relative to its own original source founder I mean | Birth events | Birth-token IDs at census12 | Census12 tagged A copies |
| --- | ---: | ---: | ---: |
| I higher at birth | 123 | 47 | 119 |
| I lower at birth | 93 | 28 | 85 |
| Equal within numerical deadband | 0 | 0 | 0 |

| A sign × inherited child I background | Birth events | Original token IDs still present | Tagged A copies |
| --- | ---: | ---: | ---: |
| A positive, I high | 67 | 34 | 75 |
| A positive, I low | 45 | 18 | 53 |
| A negative, I high | 56 | 13 | 44 |
| A negative, I low | 48 | 10 | 32 |

The **background** is the newborn's current *mean inherited I trait*, compared with the founder pool's I mean, **not phased gametic linkage to the mutated A homolog**. This Model3 has independently segregating M, I and A loci. The observed difference in original token survival cannot by itself establish an A-driven hitchhiking mechanism.

## Competing alternative that makes the raw percentages unsafe

Different mutation births have **different durations of follow-up**. The original technical ledger explicitly records the time of first A mutation and separates:

| Original mutation birth time | Births | Original event IDs retained at census12 | Tagged A copies at census12 | Mean possible follow-up years |
| --- | ---: | ---: | ---: | ---: |
| Years 1–6 | 96 | 13 | 54 | 8.08 |
| Years 7–12 | 120 | 62 | 150 | 2.93 |

Therefore the apparently higher terminal retention fraction among **late births** is **not** evidence of stronger positive selection. Positive A mutations born with high-I offspring also had shorter average follow-up (**4.42** updates) than positive A mutations born with low-I offspring (**5.87** updates). No age-adjusted genetic background effect, hazard, inference interval, or source-independent Q1 generalization is identified here.

| Visitor replenishment treatment | Births | Original token IDs retained at census12 | Tagged A copies |
| --- | ---: | ---: | ---: |
| Near | 108 | 34 | 76 |
| Far | 108 | 41 | 128 |

These two arms reuse parts of the same mutant birth histories and founder/visitor seeds. The difference in final A token counts does **not** establish island-specific selection or co-transmission of I alleles.

## What has been accomplished and what is missing

**Newly executable and verified:** Original Model3 reproduction/source genotype, original Q1 founder initial A=0.5, independent segregation and mutation RNG shadow, unique birth-token labels and parent IDs, true newborn I alleles, token-to-census copied counts. Every one of the technical paths is directly checked against the unmodified original Q1 runner. This removes a **measurement limitation** present in sparse original archived genotypes.

**Not established:** A positive A mutation's intrinsic selective advantage at its origin, independent A–I inheritance coupling as opposed to altered mate/seed selection, the chance a given mutation fixes over 1,000 updates, the cause of the historical Q1 founder sign reversal, or an ecological/plant trait evolution result in natural islands. An observational correlation of positive-A mutant-tag survival with high-I newborn background is especially vulnerable to **mutation-birth-time, initial genotype, founder ID, visitor history, direct-I allocation payoff, and repeated RNG lineage** confounding.

**Next discriminating experiment:** freeze a truly new source×visitor design before outcomes, with equal source A/I/M genotype marginals, a randomized preassigned **A mutation-origin background** (instead of post-hoc sorting events), exact birth/parentage recorder, a direct-I-fitness-neutralized arm and an I-diplotype-shuffle arm with source genotype/parent count control. Contrast complete all-start **I allele-frequency trajectories**, original I allele-origin survival, and A mutation-token trajectories. Check matched viable offspring/census and direct native Model3 parity before interpreting genetic background as a causal mediator. Control for selfing/outcross fraction before claiming the effect is caused by selfing rather than generic background selection.
