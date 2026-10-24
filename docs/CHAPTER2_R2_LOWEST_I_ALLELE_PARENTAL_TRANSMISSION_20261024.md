# R2 original source: expected lowest-I allele transmission versus eventual loss

**2026-10-24 — exploratory Model 3 source-internal parental-genetic diagnostic.** This is not a newly registered or independently replicated experiment, a causal selection/drift partition, a valid I-allele-frequency threshold, or a general law of evolution on real islands. It builds on the original genome source audits #633–#635 without changing frozen Model 3 source or registered R1–R5 evidence.

## Why a phenotype-mean selection expectation is not enough

The authenticated 2026-10-19 R2 pollen-factorial source has **22** original populations (only **11 distinct founder IDs**) in which A and M were already monomorphic and I still segregated at the census30 visitor-activity intervention, under strong historical pollen limitation. In all 22 source states, the external visitor decline led to a more negative **expected mean offspring I** in the *first generation* than maintained visitors. Yet 2 of the 22 ended after the original 50 updates at **higher I allele values**, despite lower-I alleles being present at the shock. The lowest allele had only **6/96 or 4/96** copies in these two exceptions.

A decrease in mean offspring I does not by itself prove every individual lower-I numerical allele has a positive expected transmission difference if a source population has three or more I alleles. **Twenty of these original 22 sources had exactly two I numerical allele values, but two had three.** The target-specific copy-expectation should be inspected explicitly in the original source model rather than assigned from a regression on phenotype means.

## Source-exact conditional transmission calculation

For numerical I allele value a, plant i has two diploid I homologs, and `h_i(a)` is its fraction (0, 1/2 or 1) of homologs with that value. Model 3's original deterministic ledger uses `O[f,m]` for viable outcross progeny with father f and mother m, and `S[i]` for viable selfed progeny.

The native source expected newborn frequency for that numerical allele (conditional on positive viable resident progeny) is:

    p_child(a) =
      { sum_(f,m) O[f,m] * [h_f(a)+h_m(a)]/2
        + sum_i S[i]*h_i(a) }
      / { sum_(f,m) O[f,m] + sum_i S[i] }.

For each original census30 genotype, the script runs the original `reproduce` operator at maintained activity **0.4** and visitor-decline activity **0.04** on *exactly the same full 48-plant diploid source population*. The native allele-frequency formula is checked against an **independent parent-weight summation** and against the earlier source-verified expected offspring I mean. It validates that all allele frequencies sum to one.

This is a **conditional parental transmission expectation** and not a direct estimate of the next realized census or of eventual fixation probability. The original source outcomes, verified separately by exact full-genome SHA fingerprints for both futures, are then attached descriptively.

## Two original high-I fixation exceptions

The two original source states had only **two numerical I alleles** each, separated by 0.25. For these special biallelic cases the exact identity

    Δ_expected(mean I) = (I_low - I_high) * Δ_expected(p_low)

holds when comparing the two activity treatments at fixed current state. The original source's negative *I mean* expectation contrasts therefore imply **positive expected low-I allele frequency contrasts**:

| Original source | Census30 lowest I allele | Initial fraction | Extra expected low-I frequency under decline versus control | Eventually fixed I |
| --- | ---: | ---: | ---: | ---: |
| A0=.3, founder **810102**, nested replicate **4** | 0.50 | **6/96** | **+0.0045774812** | **0.75** |
| A0=.5, founder **810110**, nested replicate **3** | 0.25 | **4/96** | **+0.0030824778** | **0.50** |

This is a *within-model numerical identity* using already source-verified expected I mean and actual allele support, not a new independent positive outcome. It establishes that the extra pollen decline **increases the expected share of the low-I allele among newborns relative to maintained visitors**, while that same rare lower-I allele is ultimately absent from **both** original surviving source futures. Whether its *absolute* expected frequency rises above census30 is checked separately by the new native parental-ledger calculation; a positive between-treatment expected difference alone does not establish that.

In all 20 biallelic original source states, a negative mean-I treatment difference implies a positive minimum-I allele expected-frequency treatment difference by the same algebra. **The other two triallelic states require explicit allele-level source accounting**: one cannot apply the biallelic identity to them.

## Scope boundaries

These 22 original state/treatment pairs are nested within **11 founder seeds** and were selected after examination of original exploratory outcomes, not through new independent sampling. No original source breeding parameter, native inheritance rule, mutational kernel or pollen histories are changed.

- We do not infer a general success rate, probability of allele fixation, sample-independent frequency cutoff, or natural island adaptive evolution.
- Numerical allele identity does not establish equal identity by descent, nor does a direct negative mean trait expectation uniquely identify the success of every allele in a multiallelic population.
- One-generation parental expected frequencies cannot be equated with realized survival and segregation, and the two-allele contrast does not uniquely separate selection, drift, correlated genetic backgrounds or finite stochastic sampling.
- The existing R2 independent four-setting founder replication retains **overall INCONCLUSIVE**, as well as the registered R1–R5 and R4 G/S bounds.

## Verification

- Native genotype/parentage reader: `scripts/audit_chapter2_r2_low_I_allele_transmission_20261024.py`.
- Native source/ancestor audit: `scripts/audit_chapter2_r2_shock_genome_expected_I_20261023.py` and `scripts/audit_chapter2_r2_original_I_accessibility_20261024.py`.
- Negative controls/chemical source invariants: `tests/test_chapter2_r2_low_I_allele_transmission_20261024.py`.
- Original independent source ZIP: [Actions run 39233450099](https://github.com/zuizui0223/izu-core/actions/runs/39233450099), artifact **12178257738**, checksum `10bb8bdd52b53b32429e350c2f392ed2aeaa791683ede1d563ae6627c5ecb35e`.

    python -m scripts.audit_chapter2_r2_low_I_allele_transmission_20261024
    python -m pytest -q tests/test_chapter2_r2_low_I_allele_transmission_20261024.py

The final source gate output will record whether the **triallelic 2 original sources** have positive or negative lowest-I expected transmission under the extra visitor decline, and whether the exceptions also have positive absolute expected low-I shifts. These questions will **not** be decided merely by the negative mean-I contrast.
