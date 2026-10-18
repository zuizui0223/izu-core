# One-paper Chapter 2: visitor-return recoverability exploration (2026-10-18)

**Status: implementation with five isolated technical tests; NO archived-state biological probe has been executed or interpreted in this change. NOT the registered definitive Q2/Q3 result.** Preserve all original biological operators, original outcomes, and the developing single-paper PR #590.

## Precisely three questions

1. Is evolvability of reproductive assurance `A` **necessary** for flower-investment `I` to fall in pollinator-limited environments? **Already answered no within Model 3:** fixed expressed A=0.5 (selfing remains possible) still permits I decline. Original and fresh-founder sets are independent, and new-carrier Q2 co-primaries remained inconclusive.
2. After an occupied source population has decreased `I`, at which source census can externally replenished visitors no longer induce **realized recovery** within a fixed horizon?
3. Does the **historical ability to evolve A** shorten or extend the recovery window, given a fixed founder distribution and the same visitor histories? **The currently available 64 previously archived A-evolving histories cannot identify this contrast.**

## Archived input and correct unit

Read-only original 64-path cohort (`causal_main` 32; `causal_confirmation` 32), matched visitor composition and low `supply=0.125`, recorded all 201 original census genotypes. Do not confuse it with the independent 2,304 HIGH-I source audit or Q1 64×8 study. Invoke the repository's existing `q3_futures_contract_20261014.admit`; it verifies the original `INVESTMENT_VARIATION_RESTORATION_64_20261013.zip` SHA256 `90b9d063c564edf97f12d3a3917819486f72d4ecb8281a20ebdaf39ad7de14c6`, original source-input ZIP SHA256 `f0fd126f638e1c6bd130e640ce4491b3bb47aac3da1838359a902776c9a4e037`, case/receipt/source identities and native historical code. The authoritative original source-input digest is in `scripts/q3_futures_contract_20261014.py` and is not overridden by this document.

The illustrative default picks the first **two** case keys in each of the two fixed archived founder blocks, at original censuses **0, 25, 50, 100, 150, 200**. These are *repeated census states*, not six independent founders or independent islands. Stochastic fresh futures (8 streams per state by default) are *nested under* each original archived state. No claim about population-level sampling error is made from the number of fresh futures.

## One ecological operation, no model extension

The old state at source time `t` is held exactly: full `PlantState` alleles, origins, mutation flags, IDs and birth years. Rebuild only the future, **externally imposed visitor environment** from the same initial matching visitor identities. The paired low-replenishment arm retains the archived original visitor-arrival settings, starting from the same archived initial visitor cohort and using the same named exogenous and demographic stream seeds. For the recovery arm set future `visitor_arrival.distance=0` and `visitor_arrival.supply=max(0.3, original supply)` with unchanged loss hazard, establishment, trait matching, pollen kernel, ovule cost, K, selfing, survival and genetic inheritance. `History.make_history` draws the future *independently of the plant state*. The historical low visitor environment is not reconstructed as a permanent extinction event; the t-grid cannot identify `T_E`. The intervention changes expected arrivals, not necessarily realized beneficial pollen service in every short stochastic future. A per-state **paired** contrast compares target attainment and cumulative expected outcrossing after restoration versus original replenishment. A grid-threshold interval is disabled where observed mean outcross difference does not demonstrate positive service delivery, without treating that as a confirmed negative treatment effect.

Continuations call the **archived native** `reproduction.reproduce` and `population.advance`; investment-locus mutation and seed immigration remain OFF, hence its maximum allele value cannot rise. `A` still evolves under the archived original rule. No sex locus, moving inbreeding depression, population-genetic rescue, or new floral optimum is added.

## Recovery is not survival, and absence of alleles is not absence of selection

For history `h`, checkpoint `t`, fresh future `r`, target `I*=I_h(0)` (realized original founder mean), and horizon `H=40` updates, define:

`Y_htr = 1{population occupied at t+H AND mean I >= I* in >=10 consecutive POST-return censuses}`.

Also report whether the **source** investment has fallen at least `0.05` from `I*` by `t`. If it has not, this is target maintenance/attainment and **not** a re-evolutionary recovery: no recovery probability `p(t)` is assigned on that checkpoint. The fixed-state stochastic success fraction is for **occupied** original states only. For each future visitor/demographic seed run two future arms (restored replenishment vs original replenishment), never replacing or overwriting the archived historical state. Extinct original states are flagged, not given an I value zero; full-population unconditional survival/recovery policy effects remain for the future confirmatory experiment.

For every occupied checkpoint classify separately:

* **Genetic necessary-support closure**: `max(I alleles at t) < I*` under zero I mutation + zero seed immigration. This is mathematically sufficient to rule out target attainment in the descendant-only model; the reverse does **not** guarantee success.
* **Local ecological selection proxy**: sign from the source's monomorphic-resident invasion-gradient function evaluated at mean source traits **across the actual restored future visitor states**; record its time series distribution (positive, negative, mixed, undefined) per paired replicate, not merely the starting old community; **NOT** exact selection of a variant in the polymorphic finite population and **NOT** a proof that all future restored visitor realizations keep the same sign. For fixed expressed-A policies, use actual fixed expression, not latent A alleles.
* **Realized response**: maintain/recover I target after 10 consecutive censuses before the future deadline, occupancy at the endpoint, plus all original vs fresh seeds and source-history identity.
* **Residual**: finite-time nonrealization when requisite allele support exists, and other ecological/genetic model differences, remain explicitly unresolved. Selection and genetic closures may overlap.

## Candidate grid threshold (not a proven irreversible t*)

For fixed source state and a grid of `t`, calculate independent-future Bernoulli point estimates and **within-history Bonferroni-adjusted 95% Wilson intervals** across available grid checkpoints. Default cutoff is `0.2`, explicitly *illustrative and non-ecologically calibrated*. Only call `candidate_grid_t_star` the **first eligible checkpoint** whose upper confidence bound, and **all later measured upper bounds**, are below `0.2`. If none qualifies, return `null`. This neither tests between-grid times nor proves a permanent no-return boundary; multiple independent archival source cases are not a jointly powered effect estimate.

The archived no-I-mutation source also permits a separate **exact first HIGH-I upper-support loss** time across all 201 stored original censuses. It is *genetic source-only*, not a restored-pollinator estimate, and must not be pooled as an independent replicate of the old 2,304-history source result.

## Execution and gate

The adapter is created as an **exploratory analysis harness** only; no CI task auto-runs numerical biology. Six isolated deterministic technical tests check theorem scope, sustained-event duration, conservative threshold handling, overlapping reasons and stream identity. Before conducting any fresh biological paths, complete the independent founder×visitor power/source and SESOI review in #585, affirm the scoped resource/study-ID budget and verify original archive/source hashes. A small engineering fixture may be tested without claiming an ecological outcome; actual archival-state biological output remains **PENDING**.

When the explicit pre-execution gates are satisfied and the two authenticated original ZIPs are available, the following is the limited diagnostic invocation (no new model source edits):

```sh
python -m scripts.chapter2_recovery_probe_20261018 \
  --archive ORIGINAL_INVESTMENT_VARIATION_RESTORATION_64_20261013.zip \
  --source-input ORIGINAL_remote_atom_inputs_20261011.zip \
  --out work/recovery_probe_20261018 \
  --samples-per-block 2 --repeats 8 --horizon 40 \
  --sustained 10 --checkpoint-times 0 25 50 100 150 200 \
  --cutoff .2
```

Expected scheduled *maximum* `4 source cases × 6 checkpoints × 8 paired repeats × 2 arms × 40 annual advances = 15,360 native updates`, fewer if source states are extinct. This is a **planning arithmetic bound, not completed updates**. Missing archives / source-hash mismatches / coverage failure yield no scientific verdict. Never treat a missing source as a zero effect.


## Post-design, pre-biological-execution precision feasibility (2026-10-18)

The planned **8 conditional future streams per occupied source state cannot, even
in the mathematical best case of eight failed recoveries, produce a multiple-
checkpoint-adjusted 95% Wilson upper endpoint below the illustrative cutoff
0.20**. With six registered time points, z = 2.6382572735 and the best upper
endpoint is 6.96040144 / (8 + 6.96040144) = **0.4652549912**. A strict
upper endpoint below 0.20 with *zero* successes requires a **minimum of 28
nested futures per state**. This is a necessary arithmetic screen for such
an interval, NOT a joint statistical power analysis or an approved change to
the 8-future pre-outcome cap.

Therefore, under the current design `candidate_grid_t_star` is *necessarily
null* regardless of the biological outcome. Do not interpret its null as
biological reversibility or a missing evolutionary lock. The planned 8
futures can still supply descriptive conditional direction and mechanistic
diagnostics, subject to archived source admission and service efficacy.
A future confirmation must separately define SESOI, independently crossed
founder/visitor variation, full-population estimands, power and resource
budget under #585; simply increasing conditional RNG repeats cannot solve
the lack of independently sampled founder histories.

The standalone source-only calculation is validated in
`tests/test_chapter2_recovery_probe_20261018.py`; the exploratory adapter
now records the exact `threshold_precision_preflight` field in any later
result. **No archived-source biological futures were run or inferred by this
preflight update.**

## What next figures can and cannot say

- **Fig. 2 / Q1:** original fixed-versus-evolvable A result remains frozen.
- **Fig. 3 / Q2:** candidate plots of fixed-state return fractions against original source t, the exact genetic upper bound, the matched no-return arm, and separately source occupancy; no claimed `T_E` or definitive `t*`.
- **Fig. 4 / mechanisms:** source-only upper-I allele absence vs local-gradient proxy vs finite-horizon failure. The last two are not an identified causal decomposition.
- **Fig. 5 / Q3:** currently blocked. A causal A-policy effect requires **paired A-evolvable vs fixed assigned before the historical divergence** in independent founder × visitor histories, followed by the same restoration at common times. Future expression fixed at evolved A and genetic rescue are distinguishable secondary experiments, not substitutes.

The article stays one NEE candidate. Its field generalization cannot use geological island age as a proxy for time since functional pollinator disappearance.