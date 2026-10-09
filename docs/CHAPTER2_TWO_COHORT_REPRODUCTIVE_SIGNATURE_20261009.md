# Chapter 2 — Two-exposed-cohort reproductive signature audit (2026-10-09)

**Status: POST-OUTCOME DESCRIPTIVE REPRODUCIBILITY, NOT PREREGISTERED CONFIRMATION OR CAUSAL MEDIATION.**

## Original sources and exact unit

- Original assigned-expression full-cohort experiment: [GitHub Actions #37856410822](https://github.com/zuizui0223/izu-core/actions/runs/37856410822), 64 independent visitor histories `37110801–37110864`, **3,072 t400 source groups**, **86,016 future branches** (includes three assigned order arms).
- Independent fixed-window follow-up: [GitHub Actions #37862121201](https://github.com/zuizui0223/izu-core/actions/runs/37862121201), 64 disjoint histories `38110901–38110964`, **2,048 t400 source groups**, **57,344 future branches** (two assigned arms).
- Paired raw replay: [GitHub Actions #37866140534](https://github.com/zuizui0223/izu-core/actions/runs/37866140534), **success**. It downloaded original and follow-up raw future artifacts, required all 64 shard manifests for each cohort, audited SHA-256 and frozen protocol/source hashes for every **5,120 raw source-case future records**, checked every 28-cell fork grid, and required all **143,360 futures** to be present before comparisons.
- Machine-readable receipt: [`results/chapter2/two_cohort_reproductive_signature_posthoc_20261009.json`](../results/chapter2/two_cohort_reproductive_signature_posthoc_20261009.json).
- Read-only script: [`scripts/chapter2_order_two_cohort_signature.py`](../scripts/chapter2_order_two_cohort_signature.py). The original cohort's synchronous timing arm is authenticated but **excluded** from A-first vs I-first, because that arm changes the overlap duration of simultaneously expressed traits.
- Both cohorts retain the same biological model, four mating settings, historical near/far settings, seven ovule budgets and two future visitor regimes. Each cohort is bootstrapped **only at its own 64 independent visitor-history units** (9,999 draws, reproducible fixed seed). Cohort-mean differences resample the **two sets separately**; the 143,360 branches are not 143,360 independent replicates.

## Main observed response: same sign, but not necessarily identical magnitude

The table shows A-first minus I-first contrasts, equally averaged across historical near/far environments, four reproductive settings, the original log-budget weighting, future visitors, and nested demographic repeats. The primary synthetic stress is eight founders / population capacity 8.

| Observed channel | Original 64-history cohort [95% bootstrap] | Independent follow-up 64-history cohort [95% bootstrap] |
| --- | --- | --- |
| 80-update terminal occupancy probability | **+0.00862** [+0.00323, +0.01397] | **+0.01209** [+0.00668, +0.01760] |
| t0 viable selfed maternal output, population sum | **+0.40026** [+0.29464, +0.50300] | **+0.39634** [+0.30227, +0.49131] |
| t0 female outcross output, population sum | **−0.32930** [−0.44666, −0.21308] | **−0.23696** [−0.33090, −0.14764] |
| t0 expected pollen export, population sum | **−1.44203** [−1.95001, −0.94697] | **−0.79853** [−1.14990, −0.46285] |
| Cumulative selfed recruits, 80 updates | **+9.82367** [+6.73298, +12.82704] | **+10.69013** [+7.71439, +13.72383] |
| Cumulative outcross recruits, 80 updates | **−4.89883** [−6.45233, −3.40287] | **−3.63008** [−4.89646, −2.43656] |
| Cumulative total recruits, 80 updates | **+4.92484** [+1.89878, +7.78283] | **+7.06004** [+4.16070, +9.85051] |

**All seven signs recur in both disjoint sets of 64 visitor histories.** The same positive selfed-output/recruitment, negative outcross/pollen-export, and small positive local occupancy signature is also present in the no-founder-bottleneck/capacity-48 comparison. This is evidence of *descriptive reproducibility under the same frozen model*.

The magnitude of the negative pollen-export contrast varies: the new minus original cohort difference is **+0.64350**, history-bootstrap95 **[+0.03574, +1.24933]** (8-founder capacity-8) and **+3.95036** [+0.33822, +7.57216] in capacity-48. The other six 8-founder differences have bootstrap intervals containing zero. Therefore **sign stability does not imply equality of effect size**.

## Ecological and causal identification

- A-first here **randomly assigns transient expression order** (A: reproductive assurance, I: floral attraction investment) under a fixed schedule; it does not randomly assign which genetic locus naturally evolves first.
- The postshock reproductive ledger already records expected viable selfed output, expected female outcross output, and expected pollen export at future entry. The increase in selfed output and the reductions in outcross and export are therefore visible **at t0**, not constructed by conditioning on later surviving populations.
- `Ledger.exported` is the model's **expected pollen export**, not realized sire offspring or total male lifetime fitness. The mating-system tradeoff cannot be restated as proven overall inclusive-fitness gain.
- The 80-update selfed and outcross recruit totals are realized counts, but their cumulative sizes depend on extinction timing and population dynamics. They are **not independently randomized mediators** of the occupancy effect.
- The common absolute occupancy advantage is small (~0.9–1.2 percentage points per cohort). It cannot supersede the **preregistered practical-equivalence result for the original far–near DID** or the **failed prospectively fixed budget-3/4 window test**.
- The two cohorts are independent environmental replicates but were **both already examined before selecting this particular cross-cohort signature**. The two-cohort sign agreement is thus descriptive reproducibility, **not a fresh preregistered test**. No new natural-island field evidence is implied.

## Next mechanistic discriminator

To separate a genuine reproductive-assurance contribution from demographic amplification, a **new pre-outcome controlled simulation** would need to hold founding genotype, population size and future random numbers fixed while changing a specified reproductive payoff pathway. For instance, a controlled reproductive-ledger component swap could test selfed-recruitment versus outcross-recruitment channels. Such a swap modifies a biologically connected payoff vector; one must first specify which conservation constraints and counterfactual genotype/pedigree relationships remain valid, verify numerical invariants, and declare a precise causal estimand. Merely correlating reproductive channel totals with later extinction does **not** identify mediation.

This result locks a model-specific reproductive tradeoff and explicitly stops short of claiming an evolutionary rescue law. No new biological cohort was generated by the audit.
