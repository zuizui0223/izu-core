# Chapter 2 — Independent fixed-B48 K experiment: late-extinction and recruitment diagnostic (2026-10-09)

**Evidentiary status: POST-OUTCOME EXPLORATORY / NOT AN ADDITIONAL CONFIRMATORY TEST.** The full 64-history capacity primary, frozen in merged [PR #442](https://github.com/zuizui0223/izu-core/pull/442), stays **SUPPORTED**, `+0.0077457139`, paired-history 95% `[+0.0024971581,+0.0130154788]`. Earlier separately frozen capacity and B hypotheses remain `inconclusive`.

## Original-data chain and scope

- All biological t400 sources and future trajectories come **only** from successful original [Run #37896872795](https://github.com/zuizui0223/izu-core/actions/runs/37896872795) at frozen input SHA `2737736f1dca36c8b43e9ac6a9fbd862ca21165b`.
- Frozen raw-admitted confirmatory readout, unchanged: successful [Run #37900150213](https://github.com/zuizui0223/izu-core/actions/runs/37900150213), source SHA `592cdad7fa0442a26fd5e79a2fd94812d4515c5d`.
- Post-outcome read-only pathway review: [Run #37918887205](https://github.com/zuizui0223/izu-core/actions/runs/37918887205), **completed successfully**. Its code re-invoked the original complete source-chain admission for all **64 visitor-history clusters, 2,048 t400 states and 114,688 raw futures**, and rechecked original registered mean/interval exactly **before** extracting descriptive demographic channels.
- Original exploratory machine artifact: [`chapter2-fixedB48-independent-posthoc-demographic-pathways-20261009`](https://github.com/zuizui0223/izu-core/actions/runs/37918887205/artifacts/11610537993). Original raw JSON is archived byte-identically at [`results/chapter2/k_fixedB48_posthoc_pathways_20261009.json`](../results/chapter2/k_fixedB48_posthoc_pathways_20261009.json), SHA-256 `8fea4bd8c1858c445ba0eb57dfc038bac6819ed767932c596b79e4cd3ed6e542`.

## Correctly interpret the outcomes

Define the assigned-expression-order contrast `D(K,g) = E[occupancy or channel | A-first,K,g] − E[... | I-first,K,g]` where `g` is baseline or 50%-selfed-viability gate. Define the gate sensitivity `tau(K)=D(K,baseline)−D(K,self_half)`.

Every row below reports the exploratory, history-paired **`tau(K8,B48)−tau(K48,B48)`** on the corresponding response. It is a *difference of assigned-order viability sensitivities*, not the mean outcome or the unconditional K effect. The bootstrap is a separate **9,999-draw paired 64-visitor-history** analysis, seed `2026100973`, chosen after the main result was exposed.

| Demographic response/channel | Descriptive sensitivity contrast K8−K48 | 95% paired-history bootstrap |
| --- | ---: | --- |
| Initial viable selfed seed output | 0 (exact) | [0,0] |
| Extinct by update 20 | +0.000988 | [−0.003417,+0.005314] |
| Extinct by update 40 | −0.004365 | [−0.009145,+0.000438] |
| Extinct by update 60 | **−0.007934** | **[−0.012978,−0.003133]** |
| Terminal occupied after update 80 | +0.007746 | [+0.002594,+0.013211] (exploratory seed; **not** the registered CI) |
| Restricted persistence duration, capped at 80 updates | +0.2543 updates | [−0.0071,+0.5277] |
| 80-update cumulative selfed recruits | −15.5409 individuals | [−26.0362,−5.2158] |
| 80-update cumulative outcross recruits | +3.8883 individuals | [−0.5338,+8.5086] |
| Cumulative total recruits | −11.6526 individuals | [−22.5338,−0.7700] |
| End population size (not binary occupancy) | −0.0561 individuals | [−0.2470,+0.1323] |

**First independent observation:** the initial reproductive payoff has exact **K parity when B and complete F8 founder genomes are held fixed**; early-extinction channel differences at 20 and 40 updates are not resolved by their descriptive intervals. By update 60 the posthoc extinction sensitivity contrast excludes zero, with the expected opposite sign from terminal occupancy. This is suggestive of delayed accumulation of the response, **not** a prospectively confirmed onset-time threshold. Differences between "interval excludes zero" and "does not exclude zero" cannot by themselves establish a statistically significant difference between the two timepoints.

**Second observation:** the cumulative **selfed recruitment** K-moderation contrast is negative (rather than positive), even though the terminal occupancy contrast is positive. Consequently the naive mechanism "the smaller K increases the assigned-order occupancy gain simply by producing more cumulative selfed recruits" **is not supported by the descriptive readout**. These recruitment totals accumulate for trajectories of **different survival durations**, density-regulated turnover, genotype inheritance, and competition. They are **not randomized mediators**, and their sign does not exclude complex time-local mediation.

**Third observation:** the survival-duration and terminal population size channel intervals include zero, despite the confirmatory binary occupancy contrast. These are different estimands with different distributions; neither removes the original positive bounded outcome nor proves a smooth change in longevity or biomass.

## Interpretation boundary and next discriminator

A defensible extension is that, **within this explicit synthetic evolutionary plant–pollinator model and fixed B48**, demographic capacity modifies how assigned expression-order effects on eventual local occupancy depend on postzygotic seed viability. The current posthoc evidence suggests that the divergence need not be visible in the first 20 updates or in net cumulative self-recruitment.

This does **not** establish time-local causal mediation, universally favorable selfing-first evolution, natural genetic mutation order, island area, field-calibrated extinction probability or individual lifetime fitness. The original main Ecology Letters manuscript on **non-necessity of assurance evolution for floral-investment loss and the compression of near/far divergence** remains a distinct, stronger four-setting paper, not replaced by this conditional finite-population survival result.

**Next scientific test, if pursued:** prospectively manipulate **early versus late seed viability retention at matched K and B**, keeping the identical 80-update horizon, randomization and cluster unit, to ask which *stage of reproduction* determines occupancy. Existing raw `first_extinction` is an observed trajectory summary and cannot alone substitute for that causal intervention. First record the new hypothesis, fresh independent IDs and one primary estimand *before* new outcomes; do not re-label this exploratory audit as causal confirmation.

**Preservation:** Original source/future ZIPs have been independently mirrored and verified as 391 original artifact ZIPs in three unpublished GitHub draft Releases (merged [PR #445](https://github.com/zuizui0223/izu-core/pull/445)). Public external data deposition and DOI remain open under [Issue #436](https://github.com/zuizui0223/izu-core/issues/436).
