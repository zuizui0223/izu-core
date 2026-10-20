# A–I mutation-birth ancestry: exact native Q1 technical tracer

**2026-10-20 | Status: newly implemented bounded technical experiment and reproducibility audit, NOT preregistered scientific confirmation.** Do **not** conflate this with original completed 1,088-case [Q1 PR #569](https://github.com/zuizui0223/izu-core/pull/569), or promote it into ongoing registered [PR #609](https://github.com/zuizui0223/izu-core/pull/609). Work is isolated in draft research [PR #610](https://github.com/zuizui0223/izu-core/pull/610).

## Key genetic identifiability gap

Original PR569 all **8 independently redrawn founder genotypes started A=.5 on every homolog**; founder `Cov(A,I)=0` by construction. The population evolved 1,000 updates with A-mutation allowed `rate=.01` and `sd=.05`. Four full-genotype snapshots per original trajectory (`t0,t200,t400,t1000`) and time series of trait means, variances and richness cannot reveal *which de-novo A mutation arose on which I genotype*. Existing `PlantState.mutation_flags` is a **cumulative boolean per transmitted allele**, not a unique mutation event identifier or the I ancestry when that event arose. Existing `PlantState.allele_origin` records a founder gene-copy identifier but is propagated through mutated copies; it alone does not distinguish different post-founder mutation births.

**Narrow technical target:** enrich a SOURCE-REPRODUCED Q1 trajectory with unique **A mutation-birth events** and their I genetic background without altering native `reproduce`, `advance`, `inherit`, `PlantState`, seed-arrival history or old registered trajectories.

## Implemented source parity

[`scripts/audit_chapter2_ai_mutation_origin_20261020.py`](../scripts/audit_chapter2_ai_mutation_origin_20261020.py) calls original `advance` once per reproductive year. Immediately beforehand, it deep-copies only the **original segregation and mutation RNG states**. The source-native advance returns complete `parentage` child/mother/father IDs and the true full genome.

The tracer independently draws precisely the native **maternal and paternal I/M/A homolog selections** and mutation mask+Gaussian steps from the cloned generators. It reconstructs, and demands exact equality for, the next census's **all three loci's diploid allele values, founder-origin IDs, cumulative mutation flags, resident child IDs and birth years**. It also demands that the shadow RNG states match their source-native counterparts after the step. No toleranced mismatch or synthetic "matching" by phenotype is admitted.

One new A mutation event gets a unique `caseID/year/childID/A_copy` token. Its payload includes:
- new-mutant inherited A copy and resulting A allele, signed mutation effect, year/child ID and maternal/paternal IDs;
- both true inherited child I copies **at birth**, child I mean, mother's I mean and father's I mean (all from inherited **source genomes**, not a later genotype mean);
- founder-origin label of the mutated A copy and, if it is a secondary hit, the earlier unique mutant token replaced by the new mutation.

The same maternal/paternal homolog draws are used to **transmit the separate A-mutation ID tokens** down the original pedigree, so each later census reports token copy counts and attrition. Tokens do not force all three loci onto a physical chromosome. Model3 has **three independently segregating loci**, with an independent maternal and paternal homolog choice at each locus. This is bookkeeping of the transmitted A *copy* event, not physical A–I linkage or phasing.

## Bounded execution mode and conditions

- Exactly **two frozen PR569 original Q1 founder IDs** (560201, 560202), **two original visitor-history IDs** (560301, 560302), each near/far, and **two unchanged mating settings** (delayed_control, assurance_cost): **16 labelled technical source pathways**. These inputs were **already exposed** in the completed PR569 study, so a successful trace is not independent source confirmation.
- Exactly **12** out of the original 1,000 reproductive updates per pathway; original A expression is allowed to evolve with original `mutation_rate=.01` and `mutation_sd=.05`.
- Original configuration requires **zero adult carryover** and **no migrant seedlings**. The sidecar rejects any future configuration outside those conditions rather than producing a silently incomplete parentage.
- At the end of every technical case, separately invoke the **unchanged original Q1 simulator** over the same 12 updates and test **entire 13-census trait trace** plus **complete terminal diploid genome** against the recorder. All original source seed families and visitor inputs remain the exact native inputs.
- The reader's default command fails closed; execution requires `--technical-bounded`. Any produced local JSON is an *engineering event log*, not registered biological evidence or a confidence interval. It refuses to overwrite another technical event log.
- Technical tests: [`tests/test_chapter2_ai_mutation_origin_20261020.py`](../tests/test_chapter2_ai_mutation_origin_20261020.py). Existing [Chapter 2 scientific gate](../.github/workflows/chapter2-scientific-gate.yml) executes focused assertions but no 1,000-generation population study.

## Expected adversarial interpretations

Even if newly arising A mutation copies survive for several generations and are statistically associated with inherited I allele backgrounds, **it does not show that I hitchhikes**. Event labels and their I background at birth reveal a potential path, not an effect. Distinguish:

1. **Occurrence**: how often A mutation events arise (positive and negative allelic effects, no survival selection imposed at the birth-event classification).
2. **Selection**: whether the mutation's descendants increase when A's own allele has a fitness advantage, conditional on environment and resource.
3. **I co-transmission**: whether an I founder allele's frequency changes **because** of the ancestral A mutation carrier association rather than direct I payoff, parent selection, drift or repeated selfing.
4. **Historical founder-sign explanation**: whether this dynamic accounts for the original 8-founder Q1 visitor×A-policy interaction, including the **inconclusive assurance-cost** mating setting and sign-reversed founder contrasts.

A convincing next experiment must manipulate A mutation origin background in the same initial I/M allele marginals, log and preserve original all-start extinctions, include **no-A-mutation and I-payoff-neutralized** controls, and then randomize I diplotypes **across parents** while maintaining copy/diplotype marginals. Even those interventions may alter mating and fertility; they require direct verification of what demographic/parent-weighting quantities stay matched. This source-only tracker is a prerequisite, not that decisive causal experiment.

**As of document creation**, no new PR569 historical long-run hitchhiking causal result is claimed; independently run or source-verify any new technical output before attaching it as an observation.
