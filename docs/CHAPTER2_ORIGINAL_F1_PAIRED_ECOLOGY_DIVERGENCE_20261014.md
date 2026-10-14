# Original Model3 F1 matched-context divergence (2026-10-14)

**Status: retrospective descriptive, source-pinned.** No new biological histories or model-operator changes. This is a follow-up to the original 2,304-history F1 access admission in PR #491 / #508, **not** the later independent 1,536-history approved genotype-access pilot. It does not alter the paper's original Q1–Q4 intervention, threshold 0.05, sustained 20-census criterion, tie window ±5 or original six-category outcomes.

## Precise question

Given the **same founder block and original paired stochastic replicate** across each of the nine registered ecological contexts, are the first-offspring F1 access **summary metrics** identical while the subsequent population-level response classes differ?

This contrast is narrower and more falsifiable than claiming that some histories have to wait longer for the *first* appearance of any A variation. In the source-verified original cohort, all 2,304 already have expressed A variance and unmutated individual-level +0.05 genotype support by F1. First access timing therefore has no cross-history variation; persistence and order do.

## Source and independent recount

- Input is the committed source-derived case CSV: `data/results/first_meiosis_access_20261014/data/results/chapter2_original_first_meiosis_access_2304_case_20261014.csv`, **Git blob `ea2c4009fc77cc59813dda0142e8da73c33a26fd`**. It was previously derived by independently rereading nine original-genotype source ZIPs and checking every event/mean; this new analysis **does not reread those raw ZIPs**.
- Frozen original Model3 biological source commit: `328548612e93469fcc8663f24548530a57399b9a`.
- Original preregistered ecological-order protocol: `docs/CHAPTER2_ECOLOGICAL_ORDER_BOUNDARY_PROTOCOL_20261013.md`. Ecological context 0 is the empty/zero-supply setting; contexts 1–8 are fixed supply/visitor-composition treatments. The same seed is reused across all nine contexts for each founder×replicate, so **the 2,304 rows are not 2,304 independent histories**.
- Reader: `scripts/audit_chapter2_f1_paired_ecology_20261014.py`, Python standard library only. Run `python scripts/audit_chapter2_f1_paired_ecology_20261014.py` for full machine-readable JSON.
- Source/domain/tamper regression: `tests/test_chapter2_f1_paired_ecology_20261014.py`. The reader aborts on changed source bytes, missing/duplicate 2×9×128 cells, invalid original event classes or absent F1 individual support.

## Results (256 matched founder×replicate clusters)

| Source-locked paired comparison | Result |
|---|---:|
| All seven original F1 summary fields exactly equal across nine contexts | **256 / 256** clusters |
| At least two distinct eventual six-class labels across nine contexts | **255 / 256** |
| A 0.05/20 sustained-event status differs across contexts | **191 / 256** |
| I 0.05/20 sustained-event status differs across contexts | **252 / 256** |
| Both A-first and I-first occur somewhere among the nine contexts | **128 / 256** |
| Number of distinct six-class outcomes per cluster (1/2/3/4/5/6) | **1 / 12 / 52 / 125 / 63 / 3** |

The **seven matched metrics** are first-offspring census `N_first_offspring`, t0 expressed A variance, F1 expressed A variance, any F1 individual reaching A +0.05, number of mutation-flagged A offspring, F1 unmutated-individual threshold support, and F1 mean A change. This is exact **CSV-field equality**, not a claim that every offspring genotype or parentage record is identical across contexts.

As a specific paired illustration, context 0 versus context 7 differs in final six-class label in **240/256**, in A sustained-event incidence in **152/256** and in I sustained-event incidence in **217/256** clusters. A sustained-event incidence is **256/256** in context 0 versus **104/256** in context 7. These are pre-existing Model3 contexts, **not island estimates** or a newly chosen ecological cutoff.

Among the **256 unique paired founder×replicate clusters**, initial F1 mean A change is negative in **131**, positive in **117**, and exactly zero in **8**. Thus the appearance of F1 A variance and individual threshold support is neither synonymous with a positive initial population-mean change nor sufficient to determine persistent population response.

## Interpretation and hard limits

**Supported:** first-generation A access *as captured by these seven summaries* can be held exactly the same across each registered nine-context matched series even while sustained A/I event incidence and their ordering differ substantially. The source experiment's ecological settings and later stochastic-genetic dynamics contain information not represented by F1 A availability alone. This is consistent with the established separation between **genetic access, realized response and sustained arrival**.

**Not supported:** a unique ecological reversal root, a quantitatively partitioned selection-versus-drift-versus-mutation mechanism, equality of all F1 genomes, 255 independent demonstrations of field causality, a validated prospective reaction clock, or an order-mediated demographic rescue effect. These counts use the **already exposed** original cohort, do not provide new independent biological replication or significance evidence, and cannot be pooled with the new 1,536-case A-access×I-homolog factorial.

This result is an additional diagnostic for the Q1→Q2 evidence boundary. It does **not** displace the primary investment-compression experiment or the existing negative/null findings, and it does **not** require changing the 4,990-word reviewer main text. A paper update should be considered only after exact-head CI and independent review of this companion analysis.
