# R2: identical current floral phenotypes and allele frequencies need not yield identical allele transmission

**2026-10-26 | Technical feasibility / design-only. HOLD / NO DISPATCH.** This note follows the mathematical independent-source source review in Issue [#638](https://github.com/zuizui0223/izu-core/issues/638) and the two design-only PRs #639–#640. It is not an independent evolution experiment, registration, natural-island evidence, intervention on historic founder genotypes, or an approved future study.

## The next identifiability gap

The Model 3 t30 floral-investment allele-access proposal can change an individual diploid I pair `(0.50,0.50) → (0.25,0.75)`, preserving **that individual's expressed investment** I=0.50. If all 48 adults retain exactly the same expressed M/I/A, original model visitor settings and life-history parameters, the **immediate native reproduction ledger** (ovules, pollen transfer, outcross fertilization, viable selfing, paternal and maternal contributions) remains numerically identical.

But even with the **same total copy counts** of all I alleles, and the same per-plant expressions, the association of a new lower-I allele with *specific parents* could be different. A low-I allele carried by an adult with high expected parental gene contributions has a different transmission expectation from the same low-I allele carried by a low-return adult.

Thus **copy count, mean I, individual I expression, and even current pollen q are not sufficient to identify the immediate allele-frequency expectation unless allele-to-parent placement is specified**.

## A static counterexample under unchanged native Model 3 reproduction

Use a **synthetic labelled 48-plant mathematical template, not a new founder cohort**:
- Exactly 24 plants have I homologs `(.50,.50)`; 24 have `(.75,.75)`. Their M and A values vary across adults, but these values remain unchanged in every comparison.
- Choose **eight of the original 24 I=.50 adults** and recode *only* their I homologs as `(.25,.75)`; each such adult still expresses I=.50.
- Construct two genotype allocations: place the eight new heterozygotes on the **highest** eight or **lowest** eight originally expected parental gene return positions, ranked **once** using the unchanged source native Model 3 reproductive ledger with strong previous pollen limitation and maintained activity=0.40.
- Both allocations have exactly the **same I allele value counts (I=.25/.50/.75 = 8/32/56 out of 96)**, the same diploid heterozygote count (8), and the same expressed I vector (24×.50,24×.75), mean **.625** and across-plant variance **.015625**. Expressed M and A and individual identifiers likewise do not change.
- Evaluate the native `reproduce` **without population.advance, inheritance, stochastic seed allocation or history generation** under strong/weak original pollen effectiveness and 0.40/0.04 visitor activity. Check exact equality of all nine original ledger components under the two allocations.

Let `w_i = 0.5 × outcross_i^father + 0.5 × outcross_i^mother + self_viable_i` be native expected parental allele return. In either allocation, the initial I=.25 frequency is **8/96**. Each recoded adult has one of two I homologs at .25, so its expected fraction among viable resident newborn alleles is

[
p^{\mathrm{newborn}}_{.25}
= \frac{\tfrac12\sum_{i \in\mathrm{carriers}} w_i}
       {\sum_{j=1}^{48} w_j}.
]

The higher-return and lower-return carrier assignments therefore differ by

[
\Delta p^{\mathrm{newborn}}_{.25}
=\frac{\tfrac12(\sum_{i\in\mathrm{high}} w_i -\sum_{i\in\mathrm{low}} w_i)}
       {\sum_j w_j}.
]

If native parentage weights are nonuniform, this difference is strictly positive under the **reference setting by deliberate ranking**, even though all current phenotype/allele-frequency summaries and reproductive ledger arrays are exactly identical. The observed contrast is a **constructed identifiability counterexample**, not an unbiased treatment estimate or newly found ecological adaptation.

The native code independently recomputes each per-allele Mendelian expected frequency and verifies it against this parental-return algebra. The four executed static readbacks, independently checked by the source-genetic-parentage formula, are documented below with actual Actions provenance.

## Verified static Model 3 native ledger readback (2026-10-26)

The original native `reproduce()`-only author-review verification passed in [GitHub Actions run 40255080484](https://github.com/zuizui0223/izu-core/actions/runs/40255080484), artifact **12621963266**. The 8,573-byte `R2_STATIC_CARRIER_PLACEMENT_HOLD.json` has SHA256 `4fe0474778ef6bbcf6a0b47c3f208fea11778df2021621cb2132c4924cae8b35`. The compact machine [source receipt](audits/CHAPTER2_R2_STATIC_CARRIER_PLACEMENT_20261026.json) preserves the exact values and explicitly denies prospective approval.

| Native original baseline | Activity | Expected I=.25 fraction in offspring, high-return carriers | Low-return carriers | Difference |
|---|---:|---:|---:|---:|
| Strong prior pollen limitation | .40 | .098285 | .047855 | **+.050430** |
| Strong prior pollen limitation | .04 | .111436 | .053816 | **+.057619** |
| Weak prior pollen limitation | .40 | .073724 | .044087 | **+.029637** |
| Weak prior pollen limitation | .04 | .082019 | .041015 | **+.041004** |

In every row, **both artificial allocations began with 8/96 low-I copies**, identical individual M/I/A expression, exactly the same ovule and pollen-transfer matrices and maternal/paternal/self expected parentage. The table contrasts *two deliberately chosen parental-carrier assignments*, not a treatment randomized over independent founders. The parental ranking was chosen from the first row and retained for all other rows.

The result verifies a **constructive failure of identification by allele copy counts alone**. It does not quantify a causal island effect, estimate allele fixation odds, demonstrate a naturally arising genealogy or establish that the best/worst parental placements differ by these amounts in a newly sampled population. **New biological population updates and offspring draws: zero.**

## Meaning for independent study design

Two distinct and currently inseparable manipulations must be distinguished:
1. **Latent genetic access:** the number and values of I alleles, within-individual heterozygosity, segregation potential, and genetic variance;
2. **Carrier background / allocation:** which M/A genotypes and expected maternal/paternal/selfing parents carry those alleles.

Matching only **initial I mean, I copy counts and overall I variance is not enough** to hold (2) fixed. For a new independent prospective study, decide whether to randomize/deliberately block carrier placement across founder×visitor histories, or explicitly estimate a genotype-background interaction. The source identity, randomization and exact ancestry labels are still undefined.

This counterexample uses **synthetic individuals with fabricated allele origin labels**, not actual wild or authentic founder histories. It says nothing about natural linkage, recombination, field pollinator preferences or ecological population effects. No causal separation of genetic drift, no universal allele-frequency threshold, and no new independent 50-update study has been identified. The preexisting R1–R5 results, registered G/S and fresh founder R2 **overall INCONCLUSIVE** remain intact.

## Reproduce and no-dispatch proof

- Static design script: `scripts/review_chapter2_r2_carrier_placement_20261026.py`
- Focused parentage/negative-control tests: `tests/test_chapter2_r2_carrier_placement_20261026.py`
- Source Model 3: `scripts/model3_island/reproduction.py`; the frozen 2026-10-19 pilot source is admitted by immutable source SHA, but no original source biological data is reclassified.
- Existing protocol authorization: `docs/protocols/CHAPTER2_R2_HISTORY_POLLEN_STATE_NEXT_STUDY_PROPOSAL_20261023.json` remains **all run_gate false** and unapproved.

```bash
python -m scripts.review_chapter2_r2_carrier_placement_20261026
python -m pytest -q tests/test_chapter2_r2_carrier_placement_20261026.py
```

**Execution scope:** source `reproduce()` static expected parental matrices only; **0** biological population updates, **0** new offspring draws, **0** seed reservations and **0** experiment dispatches. New sampling, primary effects, SESOI, genome ancestry and author permission must be defined before any future biological experiment.
