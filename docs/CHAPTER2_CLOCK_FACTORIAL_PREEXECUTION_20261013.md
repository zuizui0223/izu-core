# Q1→Q2 two-axis clock: phenotype-matched genetic-access factorial (v2 pre-execution design)

**2026-10-13 — NEW biological histories = 0; not registered confirmation or manuscript evidence.** The old 2,304-source outcome and A-width boundary cohort have already been exposed. This is a separate, prospective **pilot proposal** to test whether genetic access and inherited response jointly explain six original evolutionary threshold outcomes. It preserves the canonical Model 3 biology and all pre-existing failed/null results.

## 1. Question and evidence boundary

In the retrospective 2,304 histories, initial A has the same expressed value0.5 and zero t0 expected genetic response across all 18 founder×visitor conditions. Potential segregation variance0.001953125 is constant; it cannot explain different onset clocks within that cohort. A source t0 I Price-response feature improved parsimonious retrospective models, but a flexible ecological/genetic-interaction model yielded lower double-heldout six-class Log loss (1.41659 vs1.42169). Independently, 299 assurance-first histories showed earlier *on-path* expected I-decline selection onset (216 sustained), so onset sign alone does not dictate threshold-event order.

**Pilot question:** holding every starting adult's expressed floral traits and initial pollination environment identical within each founder×visitor regime, does *hidden* inherited A-versus-I allele availability alter six-category realized response frequencies? The pilot is a first step toward a truly prospectively validated access-delay + genetic-response probabilistic clock, NOT confirmation of such a clock.

## 2. Scientifically important pre-execution correction

The original unreviewed v1 design proposed population-centred I allele scaling, `I' = mu_I + c*(I-mu_I)` with `c=0.5 or1`. Although it held the **population** I mean constant, it moved individual adults' flower-investment phenotypes and hence their potential t0 ecological returns. It could not cleanly discriminate genetic access from changed ecological matching. **No new biological case was produced using v1.** Its historical Git commits remain source provenance; v2 below supersedes it before a biological pilot is authorized.

The corrected contrast **preserves every individual's initial expressed M, I and A phenotype exactly**. Let original adult `i` carry investment alleles `(I_i1,I_i2)`, `m_i=(I_i1+I_i2)/2` and `d_i=(I_i2-I_i1)/2`. Replace only its investment alleles by

`I_i1' = m_i - h*d_i;   I_i2' = m_i + h*d_i`, with `h ∈ {0,1}`.

At `h=0`, each individual's original expression is maintained but its hidden I heterozygosity is removed. At `h=1`, the original two alleles are restored. **Between-adult expressed I variance is unchanged** under this manipulation; we vary inherited homolog *segregation potential*, not claim a factor-four reduction in expressed additive variance. Any genetic covariance and next-generation change must be reported rather than attributed solely to one scalar variance.

Cross independently with A locus width `w∈{0.046875,0.078125}` by assigning every adult the heterozygote `(.5−w,.5+w)`. Its starting **expressed A is always0.5**. The F1 no-mutation segregational potential `w²/2` is **0.0010986328125 vs0.0030517578125**. At the pre-existing +0.05 threshold, width0.046875 cannot cross without a new A mutation; width0.078125 permits but does not guarantee crossing without mutation.

### Actual raw-founder feasibility: 8 of 8 combinations pass

Immutable original GitHub Actions shard0 SHA256 **`5b850eaad6104f572f56df2a37da00fbc8473503a827703c82f6870a87e9a881`** was re-read. The eight genotype arrays were checked for bounded alleles, no clipping, unchanged *per-individual* M/I/A expressions and original founder-wide means, genetic support for I decline0.05, and source genotype hash identities. No `reproduce`, `inherit`, `advance`, mutation or new environmental trajectory was executed.

| Founder | Original/expression I variance (all four arms) | Hidden I homolog half-difference variance at h=0 | at h=1 |
|---|---:|---:|---:|
| main | 0.00921630859375 | 0 | 0.00341796875 |
| confirmation | 0.002685546875 | 0 | 0.0068359375 |

Each combination preserves the hash of the **whole expressed 48×3 trait matrix**. All eight keep a path to founder-relative I decline0.05 even without I mutation, although the event need not occur. This provides a source-backed t0 genotype manipulation, **not yet a source-operator proof that the reproduction-ledger bytes are identical**; that proof and original mutation-masks/ancestry verification are gates for the future producer.

## 3. Proposed exploratory pilot — NOT DISPATCHED

- Two original 48-adult founder blocks (`main` seed27200701; `confirmation` seed27210701), three original visitor contexts: zero/empty, supply0.125/matched, supply0.125/separated. Original visitor optima and activity scaling unchanged.
- Two A widths × two hidden I heterozygosity treatments = four source-genotype configurations per founder; `A` is the sole mutating locus (original rate0.01/SD0.05), `M/I` do not mutate. No seed arrival, adult survival, other biological rule changes.
- Exactly **64 new demographic streams per founder**, salted `chapter2-clock-factorial-pilot-v1-20261013` and paired over the **12 genotype×visitor treatments**. Thus **128 independent founder×history clusters, 1,536 trajectories**, each200 updates. Not 1,536 independent ecological histories, and not 128 independent natural populations.
- Original outcomes unchanged: assurance-first, investment-first, near-simultaneous, assurance-only, investment-only, neither. Event thresholds: A increase0.05/I decrease0.05 relative to each transformed founder, sustained20 censuses, tie window5. Sensitivities0.025 and0.10 described separately; no replacing primary definitions after observing failures.
- Retain ALL starts, all source genetic copies, maternal/paternal/self viability records, parentage, mutation flags, population size, extinction and event-censoring states. Extinction makes trait means undefined, not zero. A-only or I-only is **never** relabelled first in a two-event ordering.
- Pilot permitted claims: feasibility, genotype-access response, all six class fractions, descriptive treatment interactions and *score-contrast variance estimation for later independent power*. **Pilot cannot confirm the clock and cannot be pooled into later confirmation.**

A source-pinned producer, complete input registration, independent original parentage/genotype replay and short technical fixtures must undergo separate code review BEFORE any of the 1,536 biological trajectories run.

## 4. Power calculated before drafting/freeze, independent of new outcomes

One confirmatory question to plan after an exploratory pilot is: does a formally specified two-stage inherited A-access+I-response predictor beat an **equal-or-more-flexible ecology × hidden-genetic-access interaction baseline** in *six-class held-out log loss* by at least a scientifically meaningful0.02? The current code does **not yet specify the full source-compatible two-stage transition predictor**; do not run confirm until its code, feature definitions, training/calibration rules, evaluation folds, null, error family and model source are separately frozen and tested.

The independent audit power worksheet uses normal paired-history mean log-score differences, 95% two-sided lower interval >0, assumed effect0.02, assumed standard deviation `s` of each **founder×stochastic stream aggregate over12 nested treatments**, and no model-refitting noise. These are **hypothetical planning scenarios**, not empirically measured pilot power:

| Hypothetical per-history score SD | Power if n=512 independent clusters | Proposed independent confirm size |
|---:|---:|---:|
| 0.10 | 99.5% | minimum512 (256 each founder; 6,144 paths) |
| 0.15 | **85.5%** | 512 (6,144 paths) |
| 0.20 | 61.9% | 896 (10,752 paths) |
| 0.25 | 44.0% | **NO-GO** within cap1024 |

For any later proposed confirmation, predefine (before its outcomes) `n=ceil_to_multiple128(max(512, [(z0.975+z0.80)*max(s_pilot,0.15)/0.02]^2))`, upper cap1024 clusters; stop with NO-GO if it exceeds cap. Only `s_pilot`, not pilot estimated mean effect, enters this size rule. The pilot histories must remain absent from confirm inference. The conservative SD floor does not cure possible new-model-fitting uncertainty, so its inference method must receive independent review as a separate gate.

## 5. Remaining gates and rollback/no-go conditions

1. **Original source/runtime identity:** use the original 048-adult diploid Model 3 source/recipe package, not a current-main variant silently substituted. Verify the exact original source SHA and all founder-specific allele/ancestry arrays, then implement the h/w transformations in a new producer-wrapper only. Reject changes to M/I/A *expressed* t0 traits, source configurations, indexed parentage or mutation masks.
2. **Initial reproduction equality:** replay the original mating operator on all four adjusted t0 states **without advance/recruitment** to verify identical initial maternal/paternal/self viability and pollen transfer per founder×visitor context. This tests the hypothesised phenotype-only t0 operator and is a prerequisite, not assumed evidence.
3. **Prospective pilot registration:** persist exact salt, 1,536 input IDs, configs/sha, raw genotype/source output format, the complete six-class event definitions and the independent verification process. Preserve original source ZIP and failed technical attempts. No retrospective tuning or selective re-run of completed cases.
4. **Clock-vs-flexible-null readiness:** calculate the A-access waiting distribution/availability from genetics, exact A and I returns and mutation law, not from future observed genotypes. Freeze the *statistical* two-stage prediction and stronger ecological interaction null only after pilot exploration and before independent confirmation. A raw source β-gradient sign by itself is not a full first-passage time.
5. **Post-pilot stop rule:** if original source access, operator equality, parentage, status/stream pairing, six-class denominator or calibration fails, `HOLD` and do not promote. If pilot SD implies confirmation n>1024, `NO_GO`; do not select favorable ecological cells or increase hypothesized effect.

**Current decision:** `DESIGN_V2_READY_FOR_INDEPENDENT_SOURCE_AND_STATISTICAL_REVIEW; NO BIOLOGICAL EXECUTION AUTHORIZED`. This is a tightened experiment to distinguish hidden genetic access from immediate phenotype ecology, not an affirmative Q2 or Q4 conclusion.

### Reproduction surfaces

- [`Pilot design JSON`](../data/design/chapter2_clock_factorial_pilot_protocol_20261013.json)
- [`Source-genotype audit`](../scripts/audit_chapter2_clock_factorial_feasibility_20261013.py) and [`8-state result`](../data/results/chapter2_clock_factorial_feasibility_20261013.json)
- [`Power-envelope method`](../scripts/audit_chapter2_clock_power_envelope_20261013.py) and [`90 assumed scenarios`](../data/results/chapter2_clock_power_envelope_20261013.json)
