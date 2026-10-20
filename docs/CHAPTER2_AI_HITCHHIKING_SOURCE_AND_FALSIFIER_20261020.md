# A–I founder background versus mutation-born hitchhiking: scientific identifiability gate

**2026-10-20 | Source-grounded new mechanistic question; NOT a confirmed explanation of PR #569, a new ecological theory, or a preregistered new biological campaign.** This belongs to prospective research Draft [PR #610](https://github.com/zuizui0223/izu-core/pull/610), **not** the registered and manuscript-integrated original Q1–Q4 science on [PR #609](https://github.com/zuizui0223/izu-core/pull/609).

## Critical correction that changes the hypothesis

The 8-founder × 8-visitor experiment [PR #569](https://github.com/zuizui0223/izu-core/pull/569), merged, is the experiment in which the four mating regimes showed founder-specific sign changes in the Q1 evolutionary assurance × visitor environment interaction. Its frozen [input design](../data/design/chapter2_q1_fresh_founder_generality_20261016.json), and original [native producer](../scripts/run_chapter2_q1_fresh_founders_20261016.py) state, unequivocally:

- Every one of **eight newly sampled source-founder diploid populations** is initialized with **ALL A alleles exactly 0.5**, by `alleles[:, 2, :] = f["A_initial_alleles"]` and `A_initial_alleles=[0.5,0.5]`; n=48 per source.
- I and M start with nondegenerate source variation, but **population-level within-individual Cov(A,I) = 0 identically at t0 for every one of these eight founders**.
- Original main simulations allow A mutation rate 0.01 and mutation SD 0.05 over 1000 updates, so A variation can arise **AFTER** the founder census; A is fixed only in the fixed-expression policy, not a literal non-selfing counterfactual.
- Original source files save per-update mean/variance/richness traits, plus full diploid genotype **snapshots only at t=0, 200, 400, and 1000**. They do **not** save every birth's mutation origin, first A-mutation event, original maternal/paternal pedigree or first new A allele's exact I parent background; this information cannot be recovered uniquely from the aggregates/sparse snapshots.

**Therefore the sentence “The initial founder A–I association explains PR #569's founder-specific I sign” is FALSE for that exact archived cohort.** A more discriminating conjecture remains: *When A begins monomorphic, do independent A mutations that arise later on different inherited I backgrounds induce indirect frequency changes in I as A-rich descendants increase?* Even this requires tracking full mutation pedigrees through stochastic replication and controlling direct I fitness; the current Q1 archival source does not identify it.

## Model3 biology and established theory

Native genetic transmission in [`population.py`](../scripts/model3_island/population.py) makes a **separate random maternal and paternal homolog choice at each of three loci M/I/A**. There is no physical same-chromosome linkage parameter in the current model. Selfing is a **reproductive parent-pair event** in [`reproduction.py`](../scripts/model3_island/reproduction.py); it need not force all three loci into one inseparable physical block. Individual-level *diploid trait covariance*, linkage/identity disequilibrium and physical genomic linkage must not be interchanged. Classical partial-selfing hitchhiking, including **unlinked** loci, is already theoretical literature, notably Hedrick (1980, *Genetics* 94:791–808; DOI [10.1093/genetics/94.3.791](https://doi.org/10.1093/genetics/94.3.791)); this is **not** a new basic genetic principle.

With original Model3 no-visitor delayed selfing and I expression artificially held at a single reference in **the reproduction ledger only**, the native viable-selfing parent weights simplify to

`W_i = B(1−δ) exp(−c_I I_ref²) × A_i exp(−c_A A_i²)`.

The **true inherited I alleles are left unchanged**. Conditional on a nonzero offspring draw, expected Mendelian I change is the standard Price accounting identity

`E[ Ibar_next ] − Ibar = Cov_N( I_i, W_i ) / mean_N( W_i )`.

If source A and I genotype marginals are identical across two founding scenarios but the within-individual pairing is reversed, the I response changes sign **even though I is phenotypically neutral in this ledger**. This is ordinary *indirect transmission through selected parental backgrounds*, not physical linkage and not proof of long-term environmental predictability.

To verify the ORIGINAL reproductive operator, the [source-only auditor](../scripts/audit_chapter2_ai_background_20261020.py) constructs **12 synthetic homozygous parents** with identical marginal 0.25/0.75 A and 0.35/0.65 I at every pairing, one constant M and no visitors:

- **Positive A–I pairing:** high A co-occurs with high I.
- **Negative pairing:** high A co-occurs with low I.
- **Balanced pairing:** individual A and I dosage covariance is zero.
- **Complete neutral-shuffle null:** average the conditional next-I response over all `C(12,6)=924` possible placements of the exact six high-I diplotypes among fixed A backgrounds, with identical marginal A, I genotype counts and unchanged native reproduction. This 924 is a **combinatorial control**, not 924 simulated islands or independent populations.
- Test both declared resource budgets B4.5 and B8; under the simple no-visitor one-step factorization resource budget is a common multiplicative weight and cancels from the **conditional direction**, not from survival probability or long-run drift.

**This is a deliberately constructed algebraic sanity check, not evidence that real Q1 mutation-origin hitchhiking occurred.** Any source-only positive result must remain technical-only.

## Source-locked numerical readout — TECHNICAL ONLY

The corrected source-only auditor and focused tests passed [GitHub Actions scientific gate **39352321694**](https://github.com/zuizui0223/izu-core/actions/runs/39352321694), `scientific-gate` job `118399112896`, original head `9e3617963f865b2bc634b373f4138a7307660471`, **success**. The initial run of the new test failed a literal float-equality assertion comparing positive and negative diploid covariances (0.03750000000000001 versus 0.037500000000000006), not a biological mismatch. The test was changed to an absolute `1e-14` arithmetic tolerance; the native reproduction, source genotypes, result definitions and historic original Q1 material were not modified.

- **Eight exact original PR569 founder inputs:** all initial A alleles=0.5; `Cov_N(A,I)=0` for every founder; I and M were polymorphic. This is a **direct input constraint**, not a statistical nonsignificant test.
- **All 12-plant artificially constructed founders have identical per-locus A and I allele and diploid genotype marginals**, independent loci and no visitors. I expression for the source reproduction ledger alone is fixed at 0.5; its *true* alleles are still those of each edited parent, with normal Mendelian conditional inheritance in the exact expectation.
- Under both B4.5 and B8, **positive A–I individual-dosage association** `Cov_N(A,I)=+0.0375` yields expected immediate `ΔI=+0.0600827872`; reversing the exact same I diplotypes gives `Cov_N(A,I)=−0.0375` and `ΔI=−0.0600827872`. Balanced A/I combinations have `Cov_N=0` and `ΔI≈0` to floating roundoff.
- **All 924 distinct placements** of six high-I homozygote diplotypes among twelve fixed A-genotype parents have an exact permutation-average immediate I response `≈0` (numerical residual ~`1e−16`).
- Equal expected I shifts between B4.5 and B8 arise because no-visitor resource budget is a common positive reproductive-rate multiplier, which cancels in conditional inheritance probabilities; this **does not** imply equal viability, demography, fixation probability or long-term phenotype.

This sanity check demonstrates that an A-associated **indirect I transmission mechanism is present mathematically in the original reproductive source operator**, even with direct I payoff disabled; but the constructed sign is a **known selection covariance identity**, so it is not novel, unexpected, or evidence that any archived PR569 evolving-A mutation rode an I allele to fixation. No new stochastic biological trajectory or historical-parent mutation-origin record was produced by this audit.

## Nearest existing original Model3 genomic assays

- The retrospective [original-far t200/t400 checkpoint Price audit](CHAPTER2_FAR_ASSURANCE_ORIGINAL_GENOME_PRICE_AUDIT_20261015.md) read **4096 source genome snapshots**, of which 2048 are candidate one-step Price cells. At far t400, 50/64 visitor histories have zero visitors. The zero-visitor **A-alignment term was tiny and sign-inconsistent** across four mating conditions (one negative, three positive). Thus the available late-state original evidence does **not** identify A–I association as the explanation of the far-positive A-evolving−fixed I endpoint. In particular at far t400, the mean *one-step Price E−F* contrast is negative in all four conditions despite a positive terminal E−F I comparison: different estimands and time scales.
- The independent [K32 diplotype reallocation](MODEL3_K32_LOCUS_REASSIGNMENT_20261009.md) kept original per-locus marginals while shuffling whole A diplotypes across parents and altered **M's** expected next-generation selection direction. For B8, native +0.005533 → A-shuffle +0.002689; this tests M rather than I, in another source model/history, and includes source-dependent mating interactions. It motivates—but does not establish—the proposed A–I long-term mechanism.
- [PR #569 fresh founder result](CHAPTER2_Q1_FRESH_FOUNDER_RESULTS_20261016.md) is **3/4 independently supported** for the original attenuation decision, with assurance-cost inconclusive and some founder-specific sign changes. The original positive A–I founder association explanation has been ruled out at `t0`; emergence of correlation after mutation remains open.

## Future mutually discriminating biological experiments (NOT EXECUTED OR AUTHORIZED)

1. **Mutation-origin audit:** Preserve the exact 8 founder source genotypes and new separately defined visitor streams. Record **every new A mutation event** with original I/M diplotypes of carrier, maternal and paternal parentage, A mutation age/frequency and tracking of ancestral I alleles through the actual offspring pedigree (not just `mutation_flags=True`, which is not a unique mutation ID). Retain all extinct populations and both successful and unsuccessful A mutations in the denominator. This needs a new lineage-labeling recorder, not merely retrospective t0/200/400/1000 snapshots.
2. **Mechanistically controlled indirect I selection:** Replay the exact parent genotypes with **I payoff-expression held constant** but native I alleles transmitted, preserving real A genotype-dependent selfing and all original M structure. Compare the expected source conditional I allele direction to a full **diploid I-diplotype permutation across parents**, retaining both I allele and diplotype marginals and recording changed I–A and I–M associations. The experiment must preserve the original selfed/outcrossed viable-recruit counts when asking about pure inheritance; otherwise a genome exchange can also affect mating and demographic fitness.
3. **Multi-generation necessity and sufficiency:** Run a preregistered source × visitor × A-mutation-origin-background crossed experiment. First vary **founder I diplotype placement** holding marginal founder I/M and all A=.5, and separately force/blind mutation-carrier I ancestry. Compare native mating, I-payoff-neutralized mating, a formally defined per-generation I-diplotype randomization, and a no-A-mutation control; include false or zero I-direction outcomes without suppressing them. The intervention may change co-transmission, selfing fraction and realized population size: distinguish these explicitly.
4. **Selfing specificity:** Separately manipulate selfing/outcross *conditional on matched viable offspring number and parental marginals*, or estimate a standard effective recombination/null predictor, before claiming the mechanism is selfing-specific rather than generic founder covariance, family-level selection, inbreeding, or simple drift. Ancestral I response variance and its predictability on held-out founders/histories must improve beyond genotype marginal and direct-I-selection baselines.

**Novelty gate:** A sign reversal in I with artificial A/I pairing and neutral I expression merely reproduces known covariance/hitchhiking mathematics and does **not** justify a high-impact theory paper. Only **source-backed predictive explanation** of previously unresolved founder sign variation (with out-of-source validation, negative controls and mechanism discrimination) can raise the status of this hypothesis. The original four-question paper remains separate on PR #609.
