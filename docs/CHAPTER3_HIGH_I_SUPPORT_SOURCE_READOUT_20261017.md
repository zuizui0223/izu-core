# Chapter 3: HIGH-I genetic-support loss — original Q3 histories

2026-10-17. **READ-ONLY RETROSPECTIVE ORIGINAL-SOURCE RESULT, NOT A CONFIRMATORY POLLINATOR RESTORATION OR A NEW ECOLOGICAL RUN.**

## Provenance and interpretation

Original source: [the complete Q3 directional-access census archive](../data/results/directional_access_20261013/README.md), 2,304 original diploid histories, 201 annual censuses, two founder blocks, nine synthetic ecological contexts and 128 replay streams per block/context. These are not independent natural island systems. Original [Q3 machine readout](../data/results/directional_access_20261013/READOUT.json) and SHA-256 pinned all original compressed census arrays and case rows.

The new [calculation script](../scripts/audit_ch3_high_i_support_20261017.py) first exactly reproduced the original LOW-I source result (1,238 first exclusions of further I decline; 703 before fixation, 535 at fixation), including the complete first-loss time list. All rows were then re-used in the *opposite* HIGH-I direction. No new visitor processes, genotypes, simulations, resampling tests, or hypothesis registrations were executed.

**Source job**: [Actions run 39021528932](https://github.com/zuizui0223/izu-core/actions/runs/39021528932), exact script head ef3b054dbdd36ae93f9209627aee7630320b5a60, report artifact ID 12096482930, ZIP SHA-256 a46929525653ee4147ad7ffd1293bd039924e09946dfd6837c2607efc80aabf9. [Complete resulting JSON](audits/ch3_high_i_source_readout_20261017.json). The PR test verifies that this saved numerical JSON equals the result of a fresh source-only NPZ/CSV recomputation. Source archive retention is separate; the output artifact expires in January 2027.

The source's actual founder means are **I0=0.5078125 (main) and I0=0.515625 (confirmation)**. Investment alleles can only take the inherited founder support **0.375, 0.5, 0.625** (no I mutation or immigration). Thus a future occupied descendant's expressed I can be at least a chosen HIGH-I target only if at least one extant allele remains as large as that target. When maximum extant I allele falls below the target, the target is structurally impossible under this same model. Retaining a sufficient allele does NOT guarantee a future response, and the absence of mutation is necessary to the permanent-source-set statement.

The three exploratory HIGH-I criteria—(i) return to the source path's actual founder mean I0, (ii) reach I0+0.05, and (iii) retention of the founder's highest 0.625 allele—gave **exactly the same first-loss times**, because both mean-based thresholds lie strictly between 0.5 and 0.625. **These are not three independent results**.

## Primary read-only counts

| Same original 2,304 paths | HIGH-I exclusion |
|---|---:|
| By census 200 | **1,455/2,304 (63.15%)** |
| First excluded before complete I-locus fixation | **758** |
| First excluded at I fixation | **697** |
| Median first exclusion among only excluded histories | **census 28** |
| Cumulative by census 25 | 655 |
| Cumulative by census 50 | 1,141 |
| Cumulative by census 100 | 1,383 |
| Cumulative by census 150 | 1,439 |
| Main founder block (1,152 paths) | 714 |
| Confirmation founder block (1,152 paths) | 741 |

**Directional joint inventory in the same 2,304 histories**, using original further-LOW-I target I0−0.05 and exploratory HIGH-I target I0+0.05:

| Relationship by census 200 | Histories |
|---|---:|
| Both HIGH and LOW targets genetically excluded | **404** |
| HIGH only | **1,051** |
| LOW only | **834** |
| Neither excluded | **15** |
| Total | **2,304** |

Of the 404 dual-loss histories, HIGH support was lost first in **192**, LOW support first in **208**, and both were excluded at the same census in **4**. The labels refer to *structural genotype support*, not an observed pollinator-return experiment, change in directional selection, or distinct stochastic island replicates.

### Ecological contexts, untested descriptive grouping

The original protocol contained synthetic visitor-supply contexts 0, 0.03125, 0.125, 0.5 and 1.0; nonzero supplies had two source-defined functional visitor compositions. The full 18 separate founder×context rows are preserved in the numeric readout. Summing existing context counts (without confidence intervals):

| Historical synthetic visitor supply | HIGH-I loss by 200 |
|---|---:|
| 0 | 254 / 256 |
| 0.03125 | 502 / 512 |
| 0.125 | 459 / 512 |
| 0.5 | 174 / 512 |
| 1.0 | 66 / 512 |

This strong descriptive pattern is not a pre-registered causal visit-rate effect, a fitted ecological threshold, or an estimate of real time since loss. Visitor composition, source genotype and finite transmission can all matter. Zero annual visitors and permanent extirpation are different events.

## Scientific GO / NO-GO

**GO: genetic-source feasibility**. The saved Model 3 already contains an explicit, source-verified HIGH-I allelic-access boundary in many original histories, often **before** complete locus fixation. This is the opposite genetic direction from the old 703 further-decrease exclusions. The machine result is reproducible from the committed original-census descriptors without generating new biological histories.

**NOT PROVEN, and needed for NEE**:

1. **T_R < T_E is not observed.** There is no experimentally imposed permanent pollinator extirpation clock in this cohort. Temporary no-visitor years and low visitor arrivals are not a defined T_E.
2. **No restoration probability.** Zero saved-path high-visitor reintroduction futures were run here. A high-I allele support exclusion is not itself an experimentally observed failure to recover after pollinator restoration.
3. **No assay that HIGH-I is favoured.** At each saved state, restored pollination might not make higher floral investment advantageous; the source ecological gradient must first be tested at the restored reference environment.
4. **No ratchet/lifeboat effect.** This cohort does not randomize historical evolvable A against fixed A. Its original assurance-first history categories are post-outcome and cannot identify A as the cause of the high-I loss.
5. **Not general irreversible evolution.** Birth mutation, new source alleles, plant immigration, other founder supports, or a different recovery threshold may reopen paths. The current target equivalence exposes how much the 3-allele model limits quantitative discrimination.
6. **No population-level inference.** The 2,304 paths include repeated source contexts and reused streams. These are descriptive counts; no new bootstrap, independent founder population or natural-island calibration is claimed.

## Next research action

Before any expensive new model run, use original native reproduction (fixed-state source assays only) at **saved states immediately before and after a HIGH-I loss**. Replace the visitor environment by a declared restored functional community and check whether the focal high-I selection gradient is positive. This separates selection-lock candidates from genetic support-lock candidates without inferring recoverability from a trait-syndrome proxy.

Only after the direction and state coverage are verified should a new restoration-futures pilot compare (i) pollinator restoration only, (ii) restored visitor plus explicitly specified sufficient HIGH-I alleles, and (iii) no-restoration control. The later A-ratchet versus A-lifeboat causal contrast requires separately randomized **historical** evolving versus fixed-A policies and independent founder×visitor histories under the [prospective precision gate #585](https://github.com/zuizui0223/izu-core/pull/585). Do not rebrand this signed retrospective source account as that experiment.

Chapter 2 Letter [merged PR #587](https://github.com/zuizui0223/izu-core/pull/587), its immutable nulls and Q1–Q4 original conclusions remain unchanged. Closed, unmerged program-design [PR #589](https://github.com/zuizui0223/izu-core/pull/589) is not reopened or merged by this report.
