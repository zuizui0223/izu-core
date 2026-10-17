# Chapter 2 — retrospective Q2 precision audit and future preregistration power gate (2026-10-17)

**Status:** technical planning improvement, **not** a new registered Q2 success, extra biological replicate, author-activated experiment, or validated prospective power calculation. The Q2 384 original paths, source operator, frozen design, co-primary family and `both_inconclusive` remain unchanged.

## Actual retrospective Q2 evidence

The entire [author-approved 384-path Q2 run](https://github.com/zuizui0223/izu-core/actions/runs/38918737325) was retrieved as **32 Actions wrapper ZIPs**. The new precision diagnostic reopens every nested source ZIP and every original signed individual NPZ and outcome receipt, reconstructs exactly **8 independently drawn founder labels × 8 visitor-history labels** and the two **far-side paired** contrasts. It refuses a mismatched file SHA, missing case or a mismatch with the [original signed readout](audits/CHAPTER2_Q2_I_SUPPORT_384_ORIGINAL_READOUT_20261016.json). No biology is executed.

**Original registered estimates, unchanged:** order-score difference `+0.109375 [-0.125000,+0.343750]`; I-event-incidence difference `+0.187500 [-0.062500,+0.421875]`, Bonferroni 97.5% intervals with 9,999 crossed founder/visitor resamples. **Neither registered interval excludes zero.**

| Quantity across the 8×8 far matched cases | A-first minus I-first score delta | I-event delta |
| --- | ---: | ---: |
| Founder-specific mean range | −0.125 to +0.500 | 0.000 to +0.500 |
| Visitor-specific mean range | −0.125 to +0.375 | 0.000 to +0.500 |
| Uncorrected sample variance of 8 founder conditional means | 0.03766741 | 0.03125000 |
| Uncorrected sample variance of 8 visitor conditional means | 0.02873884 | 0.03125000 |
| Balanced two-way residual mean square | 0.29623724 | 0.33163265 |
| Nonnegative ANOVA moment component for founders | 0.00063776 | 0 (clipped) |
| Nonnegative ANOVA moment component for visitor histories | 0 (clipped) | 0 (clipped) |

**Interpretation:** with **one stochastic realization per founder×visitor×policy cell**, founder×visitor interaction and the model's finite-history random noise are **not independently identified**. Eight founder-specific estimates do vary, but the assertion that founder variance *dominates* the adjusted CI is **not established** from this design alone. Nor can one conclude that lack of statistical power *caused* the inconclusive result; a genuinely smaller/heterogeneous effect is also compatible.

## A deliberately conservative, explicitly assumption-only sensitivity screen

For a hypothetical independent *future* experiment, an intentionally conservative variance proxy takes the **raw variance of founder means**, raw variance of visitor means, and the two-way residual MS **without subtracting overlap**. This **double counts some stochastic interaction contribution**; it is useful as an adverse planning screen, **not** unbiased component estimation.

For independent future founder count `nF` and visitor count `nV`, the proxy variance is

\[
V_\mathrm{plan}=v_F/n_F+v_V/n_V+v_R/(n_F n_V).
\]

With **two** co-primary positive-direction endpoints and two-sided Bonferroni familywise α=0.05, the approximate normal critical value is `z(0.9875)=2.2414`. Requiring each test to have ≥0.90 positive-direction discovery probability conservatively guarantees ≥0.80 probability of **both** passing by the union bound, without assuming endpoint independence. Thus an illustrative minimum-detectable-effect proxy is `(2.2414+1.2816)×sqrt(V_plan)`. This is not a direct power estimate of the finished 384-case study or a recommendation to add retrospective samples.

| Hypothetical independent future nF×nV | Order-score MDE proxy | I-event-rate MDE proxy |
| --- | ---: | ---: |
| 8×8 | 0.401 | 0.402 |
| 16×16 | 0.257 | 0.254 |
| 24×24 | 0.202 | 0.199 |
| 32×32 | 0.171 | 0.168 |
| 48×48 | 0.137 | 0.134 |

These figures are **sensitivity scenarios conditional on this proxy**, not new preregistered effect targets, true frequentist power guarantees, or an assertion that these n suffice for a new biological study. The source 8×8 is small; independently estimate uncertainty in the variance components and use simulation-based operating characteristics for nonnormal / six-class / nonlinear statistics before freezing a new trial.

## New mandatory step *before freezing any new confirmatory Chapter 2 study*

A **new study**, not a retroactive repair of the 384-path trial, must have a versioned, source-SHA-bound **power contract** `chapter2_future_crossed_power_contract_v1` and pass the automated validator **before** acceptance as a new confirmatory preregistration. The required input must record:

1. **Independent pilot provenance**: prior frozen source, source SHA-256, independent random-stream namespace, disjoint future founder/visitor namespaces and whether the source precedes the new registration. These assertions require review; the tool cannot prove biological independence from boolean declarations alone.
2. **Explicit estimands and SESOI**: the smallest biologically meaningful absolute effect for *every* co-primary contrast, its scientific rationale, direction, familywise α and multiplicity. Do **not** calibrate a supposedly prospective SESOI solely to the result of the future trial.
3. **Crossed sampling and variance sensitivity**: separate founder, visitor and residual/interaction-plus-path components, a baseline and an **adverse** uncertainty scenario, expected bootstrap/CI or independently justified analysis and a minimum **joint power** target (default ≥0.80). Do not treat 64 cross-product cells as 64 independent islands.
4. **Complete budget and hold rule**: independent founder and visitor counts, all environments/policies, exact number of original 200- (or predeclared other) update runs and their financial/compute budget. If the conservative screening criterion fails, or if a stronger nonnormal simulation design is needed, record **NO-GO/HOLD** and revise *before seeing any new outcomes*.
5. **Original cohort firewall**: preserve the existing Q2 readout as `both_inconclusive`; no outcome-based seed expansion, revised thresholds, extra hypotheses, or 'power rescue' of the old trial.

The new validator's **GO** means *ready for independent method review*, **never** automatic biological execution authorization. A true power certificate may require Monte Carlo simulation under the actual complex outcome distribution; this normal screen alone is insufficient to guarantee operating characteristics.

## Biological caveats to accompany the main hypothesis

- The inherited-allele containment theorem holds **per locus with mutation and immigrant alleles both absent**. In the completed 384-trial, **I mutation was disabled but A and M mutations remained enabled** at the predeclared mutation settings. Thus A-only outcomes (far dense 44/64, far sparse 56/64) are partly shaped by this **designed evolutionary asymmetry** and the I access gate, not pure evidence that A is intrinsically faster. Exact allocation of the category frequencies to mutation availability versus selection cannot be identified from this experiment.
- In the historical **A-half-width** response-order study, **A mutation remained active**. The mutation-zero accessibility theorem **must not** be silently used to explain all its A-first events. The width intervention changed inherited support, standing variance and eventual genotype dynamics together; an isolated segregational-variance effect has not been identified.
- The 315/1,238 first-loss transitions were **selected after an I allele was actually lost**. They are not a loss hazard or an estimated contribution of stochastic inheritance to the *separate* density-vs-finite 3/32 and 2/32 discrepancy.
- The non-necessity finding is a **counterexample under fixed nonzero A=0.5** and remains self-fertilization-capable; the original A-first 51/64 and the fixed-A cohorts use distinct original histories. The new independent 8-founder archive's fixed-A far−near means are negative in **4/4 settings and 8/8 founder-specific means per setting**, but per-history negative counts are 64, 61, 62, 64 (not 64/64 in every setting).
- Q4's independently registered +10.84-percentage-point interaction is **supported in its specified demographic stress setting**, not 'weak or random'; **natural A-first rescue** remains unidentified.

**Source references:** [final manuscript hypothesis](CHAPTER2_MAIN_HYPOTHESIS_DECISION_20261017.md) · [original Q2 registered results](CHAPTER2_Q2_I_SUPPORT_384_REGISTERED_RESULT_20261016.md) · [original two-proposition proof](CHAPTER2_TWO_PROPOSITIONS_PROOF_AND_RESULT_20261016.md) · [previous assumption-only power boundary](../data/results/chapter2_clock_pilot_power_boundary_20261014.json). The last item also explicitly cautions that an unrelated cluster-level variance cannot be substituted for the variance of a different estimand.
