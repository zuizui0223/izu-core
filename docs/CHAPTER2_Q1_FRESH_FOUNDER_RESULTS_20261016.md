# Q1 — 8 independent founder genomes × 8 visitor histories: registered 1000-update readout (2026-10-16)

**Primary registered verdict: `fresh_founder_4setting_inconclusive`.** Three reproductive settings pass the frozen two-way crossed bootstrap and founder-sign gate. The **direct assurance-cost** setting remains **inconclusive**, not rejected and not confirmed. The original 2026-10-06 four-setting result remains numerically valid **for its own single shared founder background**; the new 4/4 cross-founder generality claim is **not** established.

## Source, trace admission and controls

- Prospectively frozen [full design](../data/design/chapter2_q1_fresh_founder_generality_20261016.json) and [interpretation protocol](CHAPTER2_Q1_FRESH_FOUNDER_GENERALITY_PROTOCOL_20261016.md).
- The new cohort was executed in [GitHub Actions run #38853989138](https://github.com/zuizui0223/izu-core/actions/runs/38853989138), immutable **source run SHA `0e5424f8ce47401a1a5049613a39021392d4a2bb`**. All **32/32** producer shards and the separate independent complete-cohort summary job succeeded.
- [Complete registered readout ZIP, artifact #12026417015](https://github.com/zuizui0223/izu-core/actions/runs/38853989138/artifacts/12026417015) (90-day retention; the full 32-shard raw NPZ/source manifest archives are other artifacts of the same run). Exact source and case hashes are in each source shard; the readout includes the full **4 × 8 × 8** original four-cell treatment interaction matrix at seven-plus decimal precision.
- **1,088/1,088** requested trajectories and source receipts admitted; **32/32 zero-mutation fixed/evolving pairs** have identical complete traces and diploid checkpoints; every one of the **1,024** new positive-mutation trajectories remains occupied at update1000.
- Separate local readback of the unmodified registered ZIP independently recomputed every row's `D_mean` by two identities, all 8 founder-specific sign counts, and every two-way crossed 9,999-draw bootstrap interval from the retained 8×8 arrays at absolute tolerance `1e-12`. This is **independent arithmetic/source readback**, not a second execution of 1,088 population histories or independent biological-model validation.
- The first run's *scientific-gate workflow* initially failed only two **repository-operational** guards: automatic pull-request workflow not on the allowlist; compact new design JSON increased the tracked data tree by 5,346 bytes relative to its previous fixed cap. These are **not biological simulation test failures**. The workflow was subsequently changed to dispatch-only and the budget received an explicitly documented compact-design revision; this did **not modify the original experiment source SHA, design bytes or already archived outputs**. Final merged PR checks are separately recorded.

## Main comparison

The preregistered `D = (I_evolving,far-I_evolving,near) - (I_fixed,far-I_fixed,near)` is computed **within the same new founder f and visitor seed h**, then averaged over the 8×8 crossed matrix. Bootstraps independently resample the 8 founder labels and 8 exogenous visitor-history labels, *not 64 independent islands*. All effects are on the original Model3 floral-investment `I` scale.

| Original reproductive setting | Historical source D (common founder) | New 8×8 D | Two-way crossed 95% interval | Founders with positive mean / 8 | Registered setting verdict |
| --- | ---: | ---: | ---: | ---: | --- |
| delayed_control | +0.160539 | **+0.096122** | **[+0.022020,+0.168607]** | 8/8 | PASS |
| prior_selfing | +0.220016 | **+0.192465** | **[+0.110756,+0.275589]** | 8/8 | PASS |
| pollen_discount | +0.191501 | **+0.163012** | **[+0.047329,+0.273690]** | 7/8 | PASS |
| assurance_cost | +0.100749 | **+0.044271** | **[−0.044065,+0.130837]** | 6/8 | **INCONCLUSIVE** |

The main registered rule requires **all four** settings to pass. Consequently the campaign is **inconclusive overall**. In the costly-A setting the interval includes negative values even though its point estimate is positive; it is incorrect to call the true effect zero, negative or equivalent.

### Arm-decomposed response: a nontrivial limitation

| Setting | New evolving−fixed I: near | New evolving−fixed I: far | Implication |
| --- | ---: | ---: | --- |
| delayed_control | −0.128775 | **−0.032653** | Near extra decline still dominates, but far relative *preservation* seen historically was **not** repeated |
| prior_selfing | −0.172759 | +0.019706 | Near extra decline, slight far relative preservation |
| pollen_discount | −0.147274 | +0.015737 | Near extra decline, slight far relative preservation |
| assurance_cost | −0.069061 | **−0.024790** | Both environments show additional I decline under A evolution; small positive cross-environment difference remains uncertain |

**Interpretation:** The near-side additional decline (`E−F < 0`) was retained in all four new mating settings, but the original 4/4 positive far-side `E−F` sign became **negative in two of four new settings**. This defeats the proposed generality of *relative low-visitor investment preservation*, even if the overall difference-in-differences stays positive. A negative far `E−F` is **not** evidence for absolute investment increase/decrease from founders by itself: arm effects are relative to fixed-A controls. The alternative initial genomes **and new visitor histories** differ jointly from the old campaign, so the sign change cannot uniquely be blamed on founder genetics.

### Founder means (each averaged over 8 visitor histories)

| Founder seed | Delayed D | Prior D | Pollen-discount D | Assurance-cost D |
| --- | ---: | ---: | ---: | ---: |
| 560201 | +0.15194 | +0.16656 | +0.15398 | +0.03595 |
| 560202 | +0.13497 | +0.18968 | **−0.04343** | +0.03958 |
| 560203 | +0.08003 | +0.08299 | +0.09002 | +0.03096 |
| 560204 | +0.06163 | +0.14412 | +0.24933 | +0.08006 |
| 560205 | +0.07826 | +0.34208 | +0.09516 | +0.09717 |
| 560206 | +0.05191 | +0.22615 | +0.33636 | **−0.01164** |
| 560207 | +0.14832 | +0.21405 | +0.29002 | **−0.03251** |
| 560208 | +0.06191 | +0.17408 | +0.13266 | +0.11459 |

Raw founder×visitor matrices, visitor-specific means, original scalar means, occupancy and all 9999-draw confidence limits are preserved in the [registered readout artifact](https://github.com/zuizui0223/izu-core/actions/runs/38853989138/artifacts/12026417015).

## Scientific changes to the one-paper argument

1. **Keep the original registered Q1 4/4 statement** explicitly conditional on its original 48-plant founder genome; it was not a code bug or one erroneous subtraction.
2. **Do not claim Q1 4/4 replicates across independent founders**. The new predeclared four-way decision is inconclusive because the direct-A-cost crossing interval includes zero.
3. **Downgrade the posthoc explanatory generalization** that evolving A always preserves relative I under extreme pollen limitation. Two signs reversed in the new cohort, so this is contingent, not a demonstrated universal near/far mechanism.
4. **Still not identified:** whether this lack of far-side preservation arises from founder-genotype differences, the separately new visitor-history distribution, the single nested population draw or higher-order state dynamics. Founder×visitor crossover narrows one weakness but is not a full causal mediator intervention.
5. This **same Model3 source operator** does not independently validate wild-island adaptive fitness, long-term equilibrium, nonpollen-limited mainland comparison, evolving pollinators or naturally evolved A-first-mediated persistence.

## Data-retention and inference limits

The fully reproducible case artifacts and SHA receipts reside in the Actions run, **not a public DOI archive**. They have platform retention settings, and [external archive blocker #436](https://github.com/zuizui0223/izu-core/issues/436) remains outstanding. New founder experiment results should not be silently promoted into the existing Letter abstract or merged into old S1 counts. This report is a separate registered qualification for editorial evaluation; it does not change the historical data/readout or the old manuscript's numeric endpoints.
