# Q3–Q4: mating-system and time-horizon sensitivity (2026-10-11)

**Status:** Post-discovery exact synthetic Model 3 analysis. Not four independent populations, not a fresh prospective confirmation, and not a natural-island inference.

The original native reproductive operator is evaluated with K8, pollen background B48, four fixed artificial visitor functions, and eight initially identical heterozygous founders (investment alleles 0.20/0.50). The comparison is native genotype-dependent floral investment versus expression forced to 0.35, while diploid inheritance continues normally. The first-generation offspring distributions are identical.

| Mating rule | P80 native | P80 fixed | Difference | Generation of largest negative difference |
|---|---:|---:|---:|---:|
| Delayed selfing | .02627183 | .03024265 | −.00397082 | 22 |
| Prior selfing | .01696147 | .01818519 | −.00122373 | 19 |
| Pollen discount | .01460142 | .01482419 | −.00022277 | 17 |
| Assurance cost | .00290459 | .00343642 | −.00053182 | 16 |

All four budget6 contrasts first turn negative at generation2.

The cumulative occupied-years expectation over generations1–80 is calculated as the sum of each year's occupied probability. Differences (native minus fixed) across delayed/prior/discount/cost rules are:

- Resource 4.5: −.1081 / −.0915 / −.0845 / −.0779 years.
- Resource 6: −.8859 / −.6652 / −.5552 / −.5368 years.
- Resource 8: −.3692 / −.4737 / −.5203 / −.7401 years.

At resource4.5 the terminal P80 differences are almost zero and slightly positive because the two arms approach the same low-survival floor, despite negative cumulative differences. Consequently, the final census alone understates the temporary model response in this synthetic fixture.

**Inference ceiling:** This does not identify naturally selected allele-order effects or prove extinction caused by evolved reproductive assurance. The synthetic K/resource values were previously explored. All 12 cells belong to a single Model 3 family, with no new visitor-history draws. The four-setting source comparison is distinct from the prospectively frozen four-setting PR #411 and from the independent capacity result PR #442.

Implementation: `scripts/audit_chapter2_q3q4_four_mating_timing_20261011.py`. Regression checks: `tests/test_chapter2_q3q4_four_mating_timing_20261011.py`.
