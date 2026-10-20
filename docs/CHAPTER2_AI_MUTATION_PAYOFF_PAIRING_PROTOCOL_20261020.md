# A–I mutation-born hitchhiking — bounded six-policy technical factorial

**2026-10-20 | TECHNICAL PROTOCOL WRITTEN BEFORE ITS FIRST SIX-ARM CI OUTCOME. NOT an independent confirmatory ecology experiment, causal genetic mediation, novel hitchhiking theorem or original 1000-update Q1 repetition.**

## Active scientific question

The original [PR #569](https://github.com/zuizui0223/izu-core/pull/569) fresh-founder result contains **eight source genomes whose every A allele equals 0.5**. Thus founding `Cov_N(A,I)=0`; an **already present** high-A / high-I founding association CANNOT explain its founder-dependent long-term I response. A mutation rate of 0.01 during 1000 original updates nonetheless allows **new A mutations to arise on different I genotype backgrounds**, a possible indirect-transmission mechanism.

The [12-update native-birth mutation tracker](CHAPTER2_AI_MUTATION_ORIGIN_COTRANSMISSION_20261020.md) proved exact alignment of new A event IDs, parent identities and inherited/newborn I, but its **216 original mutations are nested within 16 short artificial repeated technical cases**. At matched time since birth, a high-I-background retention advantage was not consistently supported. No physical A–I linkage exists in the three-locus code: maternal and paternal homologs segregate *independently per locus*. Therefore test the **mechanistic possibility** separately from the historical origin of the signed PR569 signal.

## Bounded design / exact interventions

[Technical producer](../scripts/chapter2_ai_mutation_payoff_pairing_20261020.py) calls the **unchanged** original `model3_island.reproduction.reproduce`, `population.advance` and [original Q1 reproduction configuration](../scripts/run_chapter2_assurance_generality.py).

Original source axes are 2 genome seeds `560201,560202` × 2 visitor history seeds `560301,560302` × near/far visitors × two historical mating regimes `delayed_control,assurance_cost` = **16 source×ecology×mating cells**. These are **not 16 independent islands**, as founders and visitor histories are reused across cells. Within each cell start from exactly the same original **48-individual genotype**, with all A alleles=.5; follow **24 reproductive updates**, not the original 1000. Six intervention arms generate **96 short trajectories = 2,304 arm-updates** with all source assignments retained, including extinction.

| Technical arm | New A mutation allowed? | I-genotype payoff to reproduction | I diplotypes across standing parents |
| --- | --- | --- | --- |
| `Aon_Inative` | Yes, original .01 Gaussian mutation | **Native** I phenotypic expression | Untouched |
| `Aoff_Inative` | **No**, while I/M mutation remains active | Native | Untouched |
| `Aon_Ineutral` | Yes | Every parent's **expressed** I set to .5 **only in the reproductive ledger** | Untouched |
| `Aoff_Ineutral` | No, I/M mutations maintained | Expressed I=.5 | Untouched |
| `Aon_Ineutral_shuffle` | Yes | Expressed I=.5 | **Synthetic full diploid I-genotype reassignment every pre-reproduction census** |
| `Aoff_Ineutral_shuffle` | No | Expressed I=.5 | Same artificial I reassignment |

### Semantics / false identifications avoided

1. **Aoff ≠ no-selfing.** No novel A mutation is allowed, but original A=.5 can still mediate autonomous reproductive assurance. M and I Mendelian transmission and mutations remain native.
2. **Ineutral ≠ deleting the I locus.** I alleles continue to segregate and mutate. Setting **expressed** I=.5 in the native reproductive ledger neutralizes its current *genotype-dependent maternal/paternal allocation effects*. The baseline shared energetic investment cost remains common to all individuals.
3. **I_shuffle ≠ ordinary recombination.** Every current parent's entire two-allele I diplotype, I origin IDs, and I mutation flags are permuted across living plants **before reproduction**. All complete I-diplotype marginal counts and A/M loci remain unchanged, but I–A, I–M, family association and parent identities assigned to an I genotype can change. This is a declared **artificial genetic experiment**, not a clean isolated recombination-rate or selfing-rate manipulation.
4. All arms use the original Q1 master segregation, mutation, parental-recruitment and visitor streams, with a separate sidecar stream for synthetic I rearrangement. Same master ≠ synchronized events if paths diverge.
5. Every **native Aon+Inative** case is compared to the original Q1 runner on its exact source IDs and 24 updates; full original Q1 1000-update result stays untouched.

## Outcomes, falsifiers, and technical contract

All-start endpoints: occupied vs extinct at step24 for every cell/arm, and surviving population's mean A/I (undefined after extinction, never zero-imputed). Report total A mutation birth events, allele-tag copy counts, selfed/outcrossed newborns, evolving `Cov_N(A,I)`, native founder-relative `ΔI`, and the near–far difference in *A mutation enabled minus disabled* I only when **all four original paired terminal cells are occupied**. Never substitute a survivor-only average for an all-start policy effect.

- **Basic difference:** Does allowing A mutation affect I evolution when I's *direct* reproductive payoff is preserved?
- **Indirect-transmission candidate:** With I expression neutral, does A mutation still alter inherited I in a reproducible direction?
- **Association-disruption sensitivity:** With I expression neutral, does artificial I diplotype rearrangement remove, reverse or attenuate that mutation-dependent I difference?
- **Hard technical negative control:** In the **I-neutral** arms, reshuffling I must NOT change census size, mean/variance of A, total selfed/outcrossed recruits, A mutation births or A tagged-copy trajectories **within the same A-mutation policy**, because all reproductive weights depend only on M and A. If this fails, stop and diagnose instead of claiming hitchhiking.
- **Null result accepted:** If I response is unchanged by A mutation or I reshuffling, no mutation-origin hitchhiking mechanism is supported by the technical result. An apparent positive effect in only one selected founder or setting is not ecological generality.

The frozen six-policy hypotheses deliberately have **no biological SESOI, independent held-out source/visitor axes, predeclared ecological power, physical linkage model, real-field genotype test or causal mediation identification**. Successful CI verifies native-kernel parity and artificial intervention semantics, not a new high-impact ecological result.

**Source protection:** Do not change numerical rules, choose new favourable visitors or merge this exploration into [PR #609](https://github.com/zuizui0223/izu-core/pull/609)'s registered Q1–Q4 paper. [PR #610](https://github.com/zuizui0223/izu-core/pull/610) remains Draft.
