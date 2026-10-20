# Additional stricter Model3 control: neutralize both M and I reproductive payoffs

**2026-10-20 | technical sensitivity extension specified before inspecting its new results.** It extends the source-locked [initial six-arm technical readout](CHAPTER2_AI_HITCHHIKING_FACTORIAL_TECHNICAL_READOUT_20261020.md), not its source commit, and remains within research [Draft PR #610](https://github.com/zuizui0223/izu-core/pull/610). No biological experiment has been prospectively registered and it does NOT enter publication Results in [PR #609](https://github.com/zuizui0223/izu-core/pull/609).

## Reason for the extra control

The first six-arm source-compatible short Q1 factorial showed that (a) suppressing I's expressed reproductive payoff did not eliminate all I changes when de-novo A mutation was allowed, and (b) artificially redistributing whole I diplotypes altered that response. But this annual I-diplotype reassignment changes **I–M** as well as **I–A** associations; with native M expressed, M carries its own mating/visitor fitness. Those changes cannot be uniquely attributed to A.

**Now hold BOTH expressed M and I at 0.5 in the reproductive ledger**, while leaving M/I's true inherited diploid alleles, mutation rates and Mendelian transmission entirely unchanged. Under this modified synthetic ledger, any between-parent **genotype-dependent fitness differences** are attributable to expressed A, not expressed M or I (ecological visitor conditions and shared density still affect the overall rate). A mutation OFF leaves the initial A copies equal to 0.5, so there is no direct phenotypic difference among parents in this neutral-payoff artificial model. Stochastic offspring sampling, genetic drift and reflected new M/I mutations remain.

## Four NEW technical arms, appended without changing the existing six

| Arm | A mutation | Expressed M/I contributions | I genotype reallocated every generation |
| --- | --- | --- | --- |
| `Aon_IMneutral` | yes | M=0.5, I=0.5 | no |
| `Aoff_IMneutral` | no | M=0.5, I=0.5 | no |
| `Aon_IMneutral_scramble` | yes | M=0.5, I=0.5 | yes |
| `Aoff_IMneutral_scramble` | no | M=0.5, I=0.5 | yes |

All four arms use unchanged **native** `reproduce()`, `advance()`, independent M/I/A Mendelian homolog choices, and A/M/I mutation **random draws**, with A's mutation MASK changed only in Aoff. In source generation, founder A starts monomorphic at 0.5 for every allele. Whole I-diplotype scramble preserves all original locus genotype marginals and every M and A allele/provenance, while destroying within-individual I association with A and M; **M–I association has no direct M payoff in these four arms**, reducing but not magically identifying the A-only mediation question.

The exact A and M inherited genotype histories, census occupancy, selfed and outcrossed recruited offspring counts for each M+I-neutral arm MUST be identical to those of its source-paired M+I-neutral annual-I-reshuffle arm; otherwise this artificial mechanism does not isolate changes in inherited I association and the test must fail.

## Fixed observation window and interpretation

The original **16 old-source contexts** remain: two PR569 founder seed identities × two original exogenous visitor-history seeds × near/far replenishment × delayed/assurance-cost mating setting. Each is exposed under **10 policies**, **160 bounded technical trajectories**, 24 updates per path (not the original 1000), all old-source RNG master labels unchanged, and no new natural-island experiments. The original six policies and their 96 paths must be **numerically identical** to the previously passed job under original source head `f2c3c1f9e635fb7a84407cdc36ba683b14a793ed`.

Report all-start survival and true inherited I changes from original founder. The narrow new primary synthetic comparison is:

`A-mutational association sensitivity under both M/I neutral = [I(Aon_IMneutral)−I(Aoff_IMneutral)] − [I(Aon_IMneutral_scramble)−I(Aoff_IMneutral_scramble)]`.

This is a **difference of model policy endpoint means**, *not* a causal mediator coefficient: artificially scrambling genotypes changes family pedigree, not natural meiotic recombination; allowing A mutation can perturb parent-choice/genotype histories; outcomes may vary with low stochastic source sample. The associated tests must verify source Q1 old pair bitwise parity and exactly identical M/A and offspring paths under new I-shuffled and nonshuffled M/I-neutral arms.

**Falsifiers of the simple short-horizon hypothesis** include zero or unstable A-mutational effects with both M/I payoff neutral, inability to preserve A/M and offspring-number paths across I reallocation, or I effects that remain as large when A mutation is disallowed. Every such outcome is admissible; do not retune the old source seeds or technical grid to manufacture a coherent sign.

**Next science beyond this technical step:** independently prepared new source founder genotypes/visitor histories, verified mutation-origin parent labels, proper demographic unit-level uncertainty and genetic reassignment that distinguishes A–I from M–I without unphysical recombination. An actual 1000-update original-Q1 mutation-origin hitchhiking claim is NOT tested here.
