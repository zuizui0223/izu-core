# A-mutational supply × floral-I direct payoff × synthetic I-genotype reallocation

**2026-10-20 — prospective description of the TECHNICAL engineering fixture only; NOT a newly registered biological experiment or evidence of A–I hitchhiking in the original PR #569.** Keep the source-registered single-article [PR #609](https://github.com/zuizui0223/izu-core/pull/609) separate from experimental Draft [PR #610](https://github.com/zuizui0223/izu-core/pull/610).

## Precise mechanistic question

The original [PR #569](https://github.com/zuizui0223/izu-core/pull/569) source starts all eight founding A loci genetically uniform at 0.5. Therefore the original founder **A–I covariance is zero** even though there are polymorphic I and M loci. Fresh A mutation is allowed later. Does the original source biology **permit a post-founder A-mutation-associated shift in inherited I**, when I expression has no direct allocation/visitor payoff? And what happens when artificially destroying whole-I-diplotype associations with A **and also M**?

This is **not a physical chromosomal linkage model**. The Model3 `inherit()` function independently selects maternal and paternal homologs at the three loci. Selfing is a parentage/mating event, not a guarantee that independently segregating loci remain in one inherited block. The prior [source-only 12-update A mutation tracer](CHAPTER2_AI_MUTATION_ORIGIN_COTRANSMISSION_20261020.md) identified 216 A mutations in 16 nested technical source histories, with no robust high-I-origin token benefit after fixed-age comparison. This is motivation, not statistical power or an independent source.

## Original biological functions kept unchanged

[`scripts/chapter2_ai_hitchhiking_factorial_technical_20261020.py`](../scripts/chapter2_ai_hitchhiking_factorial_technical_20261020.py) directly calls native original `founder()` / `exposure()`, `reproduce()`, `advance()` and original Q1 `Config`, retaining mother/father sampling, viable selfed offspring, visitor transfer, numerical mutation generator and original independent-locus Mendelian inheritance. Do not modify any files in `scripts/model3_island/`, the frozen Q1 design or old case archives. All arms inherit I and M with exactly the same original mutation law (rate .01, SD .05).

### Six declared source-level intervention policies

| Policy | A new mutation permitted | I genotype pays native investment+visitor costs/returns | Independent annual artificial I-diplotype scramble |
| --- | --- | --- | --- |
| `Aon_Inative` | yes | yes | no |
| `Aoff_Inative` | no | yes | no |
| `Aon_Ineutral` | yes | **no; I expression set to .5 only in reproduction ledger** | no |
| `Aoff_Ineutral` | no | no | no |
| `Aon_Ineutral_scramble` | yes | no | **yes** |
| `Aoff_Ineutral_scramble` | no | no | **yes** |

**Critical strict controls:** A mutation OFF is **not zero mutation everywhere**. A starts monomorphic .5 in all arms; `mutation_traits=(True,True,False)` suppresses only de novo A mutation, while M and I retain source genetic inheritance/mutation. `assurance_mode="evolving"` stays native for all arms. The two `Inative` arms are tested **bitwise against the original registered Q1 simulator**, respectively evolving-A and fixed-A-expression source traces/genomes over the same 24 updates, to verify that altering only the A mutation mask on a monomorphic A source is identical to its original historical fixed expression setting. This source check has no power to validate the other synthetic policies biologically.

I direct-payoff neutralization replaces **expressed I** with 0.5 in the maternal allocation and pollinator-affinity ledger only, while all original inherited I alleles are transmitted unchanged. It is a very artificial **functional** knockout of the modeled investment trait, not an empirical flower size/color gene knockout; M still evolves and can influence mating. I itself is not necessarily neutral in full multilocus association even under that expression suppression.

Scrambling annually reassigns each individual's ENTIRE **diploid I pair**, its `allele_origin` values and mutation flags together, leaving the current I locus diplotype marginal, A/M alleles and their provenance, census and original visitors exactly unchanged. This is **an external genetic exchange**, not meiosis, recombination, ordinary mating, or a source-mutational input; it destroys I association with **M as well as A**. The intervention is restricted to `Ineutral` arms so the I reassignment cannot change the source-native maternal/visitor reproductive weights directly. The **A and M full paths, demographic recruitment, selfed and outcross offspring numbers must match exactly** between otherwise paired neutral-I scrambled and unscrumbled source arms; tests fail on a single mismatch. Any terminal I contrast still cannot be attributed exclusively to A-specific hitchhiking.

## Exact technical scope and pre-readout controls

- **16 original-source contexts**, two original founder seeds 560201/560202 × two visitor history seeds 560301/560302 × near/far replenishment × two original Q1 mating regimes delayed_control/assurance_cost, all source-exposed in PR #569, so they are **not 16 independent newly sampled natural islands or populations**.
- Each original source context is forked to six synthetic policy arms, **96 paths total**, each **24 reproductive updates**, not the original 1000-update registered main Q1 campaign.
- Original A t0 is **0.5 for every diploid gene copy**. Per-step offspring and genotype arrays follow the same original Model3; A-on and A-off source-negative controls are directly replay-verified against original Q1.
- The technical [tests](../tests/test_chapter2_ai_hitchhiking_factorial_technical_20261020.py) verify exact matched original source, original Q1 trace/genome parity for both base arms, I-payoff-only masking, precise I diploid-genotype marginal conservation, true I genetic inheritance, A/M exact history identity and identical demographic/self/outcross totals under I-neutralized I shuffle, source registry validation, and no ungrounded ecological inference.
- Terminal outcomes: all-start binary occupancy, conditional mean and start-to-final I and A, source allele-copy mutation flags (NOT unique mutation IDs), original genotype source pairing. Extinct terminal I is undefined; do not impute I=0. Any source-wise A/I outcome is *technical descriptive*, not an inferred effect of a new independent biological treatment.
- **No CI/p-value for founder-population effects is admissible from 16 shared old-source contexts.** Other setting/time/parameter regimes are neither sampled nor an evidence base for universal deterministic evolution. There is no physical recombination control or real plant-breeding/genomic measurement.

## What would be a useful *technical* output

If A mutation is required to change I under I-payoff-neutral reproduction, whereas A-mutation-free and/or annually I-shuffled arms behave differently, one candidate mechanism is indirect I transmission via A/M-selected families. Even under this pattern, it is NOT proof of a hitchhiking *cause* (I-shuffle disrupts M–I associations; A mutation can change demography and family composition) or of the original PR #569 1000-update sign reversals.

If the same I pattern occurs when A mutation is disabled or is untouched by I scrambling, that weakens the simple A-origin hitchhiking explanation **in the 24-update technical regime only**, not in original long-term positive-mutation trajectories.

Strong future admission gate: a genuinely new source-founder × external visitor history experiment with registered birth-phase I/A association and I/M control, explicit physical/or effective recombination contrast, known cohort sampling units, I direct-selection neutralization, and source-registered no-A-mutation controls. Such a biological campaign is **NOT** initiated or authorized by this fixture's successful tests.

**No editing of paper PR #609's registered G/S endpoints, Q1 3/4 founder generality verdict, Q2 inconclusive decision or canonical figures.**
