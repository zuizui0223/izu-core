# Visitor tempo: expected and realized inheritance in all 1,024 archived cases

**2026-10-11 — retrospective accounting of the completed, separately frozen Model 3 visitor-tempo cohort.** The original experiment and its descriptive inference remain as admitted in [PR #476](https://github.com/zuizui0223/izu-core/pull/476). This analysis uses the same archived outcomes and adds no biological histories, new bootstrap, hypothesis test, or causal intervention.

**The new result is an exact account of how source reproductive expectations became realized genetic changes.** All eight abrupt-minus-gradual investment contrasts are negative over 400 updates, and all eight corresponding expected-response contrasts are negative. However, every delayed-selfing arm has a positive mean investment change from its founders. Abrupt replacement therefore often means *less investment increase than gradual replacement*. Later parental sampling can also oppose the expected-response contrast, even after the prescribed visitor environments become identical. These statements concern the recorded cohort; the component sums are not independent causal effects or mediation fractions.

The population endpoint is nearly capacity-limited. Of 410,624 censuses, 410,601 are at 48 individuals; the remaining 23 occur in 13 cases, with a minimum of 34. No population becomes extinct. This establishes the actual demographic margin in the recorded paths, while leaving an evolutionary effect on persistence unidentified.

The [complete numerical tables](CHAPTER2_TEMPO_REALIZATION_ACCOUNTING_TABLES_20261011.md), [case/profile/arm summary](../data/results/chapter2_tempo_realization_accounting_20261011.json.gz), [independent audit](../data/results/chapter2_tempo_realization_independent_audit_20261011.json.gz), and [source and artifact receipt](../data/results/chapter2_tempo_realization_receipt_20261011.json) retain the supporting quantities. The separately saved `izu_core_tempo_realization_full_20261011.json.gz` additionally contains every annual census and recruitment diagnostic.

## What was analyzed

The original design has 16 synthetic visitor profiles, four nested demographic repeats, delayed/prior selfing, assurance cost 0/.5, mutation rate 0/.01, and abrupt/gradual functional-optimum replacement: 1,024 cases with 400 reproductive updates and 401 genomic censuses each. The four visitor types persist. This is a functional-optimum chronology contrast, not visitor disappearance. Both schedules have identical prescribed visitor environments during updates 100–399; their evolved states can still differ.

The original first100 cumulative-pollen match used only the fixed clonal reference with N=48 and X=I=A=.5. It does not impose equal delivered pollen on the evolving, heterozygous populations. This accounting retains each population's actual source state and reproductive ledger.

The calculation includes every case, both traits, and the two design-defined phases. It averages four repeats within each profile, then the 16 profile means. Abrupt-minus-gradual contrasts pair the same profiles and repeats. Cases, years, parents, and offspring are not additional independent environmental units. There is no restriction to A-only cases, crossed cases, or surviving subsets.

| Window | Reproductive updates summed | Observed mean change |
|---|---|---|
| Early | 0–99, 100 updates | Census 100 minus census 0 |
| Late | 100–399, 300 updates | Census 400 minus census 100 |
| Full | 0–399, 400 updates | Census 400 minus census 0 |

Values are signed changes on the original 0–1 diploid trait scale. The phase quantities are sums, so the 100-update and 300-update windows are not averaged with equal weight. The exact source design and original results are linked in the [original result report](CHAPTER2_SEQUENCE_ABRUPT_GRADUAL_FUNCTIONAL_LOSS_RESULTS_20261011.md).

## 1. The expected-to-realized accounting

For either investment I or assurance A, let `g_i` be adult i's diploid mean. The unchanged native reproductive ledger gives maternal outcross return F, paternal outcross return P, and viable self return S. Full parental genetic return is

\[
W_i=\tfrac12F_i+\tfrac12P_i+S_i,
\qquad
m_t=\frac{\sum_i W_i g_i}{\sum_i W_i}.
\]

Here `m_t` is the expected offspring mean before mutation, conditional on the archived source population and a positive retained offspring count. An independent donor-by-mother pair calculation verifies the same mean. The source population mean is `gbar_t`. The retained parental-pair mean `q_t` averages `(g_mother + g_father)/2` over the actual recruited children, using saved parent IDs. The observed child mean is `gbar_(t+1)`.

\[
\bar g_{t+1}-\bar g_t
=\underbrace{(m_t-\bar g_t)}_{\text{expected response}}
+\underbrace{(q_t-m_t)}_{\text{parental sampling}}
+\underbrace{(\bar g_{t+1}-q_t)}_{\text{segregation and mutation remainder}}.
\]

The first term uses the source genotypes and their complete reproductive weights. It is distinct from the local marginal gradient obtained by perturbing an individual's phenotype. Its sum follows the *realized, state-dependent source path*; it is not the expected terminal response across all possible alternative histories.

The second term records which parents contributed to the retained generation relative to that source expectation. The last term is Mendelian segregation when mutation is zero, and combined segregation plus mutation when mutation is active. Saved parent IDs and final offspring alleles cannot recover the separate mutation and homolog-draw contributions in mutation-enabled cases. No percentage of a causal effect is assigned to these terms.

The identity uses the native zero-adult-survival and zero-immigration design. If a child population were empty, its mean and realized components would be unavailable, rather than zero. All 409,600 source-to-child transitions are available for both traits in this cohort. The [native calculator](../scripts/audit_chapter2_tempo_realization_accounting_20261011.py) and [independent archive calculator](../scripts/audit_chapter2_tempo_realization_independent_20261011.py) document the implementation.

## 2. Full-period schedule contrasts

Each row is a descriptive abrupt-minus-gradual contrast over all 400 updates, based on 16 paired profiles and 64 paired cases. The three component columns sum to the observed contrast, apart from displayed rounding. Both traits and all eight settings are shown.

### Investment I

| Selfing timing | Cost | Mutation | Observed | Expected response | Parental sampling | Segregation/mutation remainder |
|---|---:|---:|---:|---:|---:|---:|
| delayed | 0 | 0 | −0.107699 | −0.099786 | −0.011093 | +0.003180 |
| delayed | 0 | .01 | −0.092622 | −0.117286 | +0.024549 | +0.000114 |
| delayed | .5 | 0 | −0.095261 | −0.096111 | +0.003616 | −0.002767 |
| delayed | .5 | .01 | −0.133097 | −0.085347 | −0.056547 | +0.008797 |
| prior | 0 | 0 | −0.036583 | −0.052996 | +0.010550 | +0.005864 |
| prior | 0 | .01 | −0.009405 | −0.004434 | +0.003065 | −0.008036 |
| prior | .5 | 0 | −0.050231 | −0.060970 | +0.013155 | −0.002416 |
| prior | .5 | .01 | −0.103123 | −0.096884 | −0.022965 | +0.016726 |

The negative schedule contrast agrees in sign with the summed expected-response contrast in all settings. The finite realized terms sometimes narrow that difference and sometimes enlarge it. Their directions are not uniform across settings.

### Assurance A

| Selfing timing | Cost | Mutation | Observed | Expected response | Parental sampling | Segregation/mutation remainder |
|---|---:|---:|---:|---:|---:|---:|
| delayed | 0 | 0 | +0.034635 | +0.032136 | +0.016984 | −0.014485 |
| delayed | 0 | .01 | +0.070923 | +0.058032 | +0.009083 | +0.003809 |
| delayed | .5 | 0 | +0.074801 | +0.056630 | +0.007520 | +0.010650 |
| delayed | .5 | .01 | +0.110609 | +0.114221 | +0.001186 | −0.004797 |
| prior | 0 | 0 | +0.030690 | +0.029719 | +0.008292 | −0.007321 |
| prior | 0 | .01 | +0.006977 | −0.000972 | +0.007890 | +0.000059 |
| prior | .5 | 0 | +0.024234 | +0.042799 | −0.043522 | +0.024957 |
| prior | .5 | .01 | +0.096557 | +0.078390 | +0.017593 | +0.000574 |

Assurance is higher under abrupt replacement at the terminal census in every setting. Its expected-response contrast is positive in seven settings. The prior/cost0/mutation.01 setting has a small negative expected-response contrast and a positive realized contrast because the retained-parent term opposes it. The costly prior/no-mutation setting also has substantial cancellation between signed components. A single pooled “fraction explained” would hide this structure.

### Absolute founder-relative investment change

The actual founder mean I is 0.5023530254221786. Every delayed arm has positive observed and expected I change over both the early and full windows. The following table lists all delayed settings; the complete tables retain prior arms as well.

| Cost | Mutation | Early I change, abrupt | Early I change, gradual | Full I change, abrupt | Full I change, gradual |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | +0.038241 | +0.154901 | +0.027830 | +0.135529 |
| 0 | .01 | +0.063695 | +0.159693 | +0.086770 | +0.179393 |
| .5 | 0 | +0.067041 | +0.168767 | +0.061693 | +0.156954 |
| .5 | .01 | +0.079012 | +0.194475 | +0.120634 | +0.253731 |

Consequently, lower I under abrupt replacement does not by itself establish a decrease from founders. This distinction also prevents interpreting the delayed A-only majority as a general failure to transmit a source-expected, long-run I decline: the mean summed source expectation itself is positive in these arms.

## 3. What happens after the visitor schedules converge?

During updates 100–399 the prescribed visitor environments are identical across schedules, while each arm retains its own evolved state. The late I contrast is positive in six settings, narrowing the earlier negative difference, and negative in two settings. Seven of the eight late expected-response contrasts are positive.

| Selfing timing | Cost | Mutation | Late observed I contrast | Late expected response | Late parental sampling | Late remainder |
|---|---:|---:|---:|---:|---:|---:|
| delayed | 0 | 0 | +0.008961 | +0.002507 | +0.005945 | +0.000509 |
| delayed | 0 | .01 | +0.003376 | +0.000454 | +0.003887 | −0.000965 |
| delayed | .5 | 0 | +0.006465 | +0.004448 | −0.000790 | +0.002807 |
| delayed | .5 | .01 | −0.017634 | +0.010890 | −0.038290 | +0.009767 |
| prior | 0 | 0 | +0.004144 | +0.014721 | −0.009685 | −0.000892 |
| prior | 0 | .01 | +0.012174 | +0.016426 | −0.001290 | −0.002963 |
| prior | .5 | 0 | +0.015640 | +0.010265 | +0.002421 | +0.002953 |
| prior | .5 | .01 | −0.024244 | −0.015733 | −0.011712 | +0.003201 |

The delayed/cost.5/mutation.01 row demonstrates the distinction particularly clearly:

\[
-0.017633764
=+0.010889545-0.038290161+0.009766852.
\]

Along these recorded paths, the expected term points toward narrowing the investment gap, but the retained-parent term points in the opposite direction and the observed gap widens. The prior/cost.5/mutation.01 row widens with a negative expected term as well. These are different accounts of the same sign of late contrast. Neither establishes a reproducible stochastic bias or an independently manipulated mechanism.

### Event categories and terminal states answer different questions

Original 20-census sustained-threshold categories are copied unchanged, and supplementary terminal descriptors are listed for all 16 arms in the complete tables. For example, delayed/cost.5/mutation.01 gradual has 47 A-only cases by400; 46 finish I above their founder mean. The corresponding abrupt arm has 37 A-only cases, all 37 above founders. Among that abrupt arm's 17 recorded I-event cases, four no longer meet the I-decrease threshold at400, and two finish above founders.

Thus A-only means a qualifying assurance increase but no qualifying sustained investment decrease within the declared horizon; it does not mean that I was unchanged. Conversely, an earlier confirmed I event does not guarantee a permanently below-threshold terminal state. These supplementary descriptors neither redefine the registered categories nor condition the main accounting on an event. The [independent audit](../data/results/chapter2_tempo_realization_independent_audit_20261011.json.gz) retains every original case category and its corresponding terminal descriptors.

## 4. Recruitment accounts for the nearly saturated demographic endpoint

With native adult survival and seed immigration both zero, the original recruitment law is

\[
\lambda_{R,t}=\text{outcross}_t+\text{viable self}_t,
\qquad R_t\sim\operatorname{Poisson}(\lambda_{R,t}),
\qquad N_{t+1}=\min(R_t,48).
\]

Capacity is an upper limit, not a guaranteed population floor. Every retained child's parentage was checked against the next census. Inventory totals are:

| Quantity | All original cases |
|---|---:|
| Genomic censuses, including founders | 410,624 |
| Censuses at N=48 | 410,601 |
| Censuses below 48 | 23 |
| Cases ever below 48 | 13 |
| Minimum observed N | 34 |
| Extinct censuses | 0 |
| Reproductive updates | 409,600 |
| Updates with uncapped seed intensity lambda_R below48 | 7 |
| Minimum uncapped seed intensity lambda_R | 41.31719220969113 |
| Retained selfed recruits | 12,644,952 |
| Retained outcross recruits | 7,015,750 |
| Total retained recruits | 19,660,702 |
| Missing recruit slots relative to 48 each update | 98 |

The minimum census occurs at t=36 in `p48271007_r49271001_delayed_cost50_mu100_abrupt`; the minimum source expectation occurs at update t=32 of the same case. They are different observations. All 23 below-capacity censuses occur after reproduction, so 409,577 of 409,600 post-update censuses are at capacity. The full tables identify the affected arms.

The directly evaluated conditional capacity shortfall is

\[
E[48-N_{t+1}\mid\text{saved state}]
=\sum_{r=0}^{47}(48-r)\Pr\{\operatorname{Poisson}(\lambda_{R,t})=r\}.
\]

Its mean across saved states is 0.00016598257209346875 individuals, and the corresponding mean conditional next census is 47.99983401742791. Shortfall is computed directly to avoid cancellation when a displayed expected census rounds to 48. These are averages of conditional one-step model quantities along the observed paths, not new independent population outcomes.

The largest model-implied one-step extinction probability on a saved state is `exp(-41.31719220969113) = 1.138076394794322e-18`. It does not bound the risk at unvisited future states or estimate a 400-update survival effect. Conditional risks are not multiplied into a long-run survival probability.

The uncapped realized candidate count was not saved for capped updates. For a next census below48 it equals the retained count; at next census48 only the lower bound `R >= 48` is known. Exact discarded candidate counts or the parental composition of unretained candidates cannot be reported. Pooled selfed fraction is 0.6431587234270678; the mean case-specific fraction is 0.6431586660190615. These denominators are kept separate in the numerical output.

### A structural reproductive margin already exists in the founders

For a fixed archived state, the unchanged ovule and viability rules imply the zero-pollen seed intensity

\[
S_{0,t}=\tfrac12\sum_i A_i\,8\exp[-0.5I_i^2-cA_i^2].
\]

Native total intensity is at least `S0`: it is `S0 + sum(F_i)` under prior selfing and `S0 + sum((1 - .5*A_i)*F_i)` under delayed selfing. The native ledger and this algebra were checked at every source state.

| Assurance cost | Source states | Minimum S0 | States with S0 below48 | Founder S0 |
|---:|---:|---:|---:|---:|
| 0 | 204,800 | 49.459570556031736 | 0 | 81.93736447996565 |
| .5 | 204,800 | 31.65557999027227 | 3,604 | 71.5337791056919 |

The actual heterozygous founders already have positive assurance and a substantial one-step reproductive margin. This helps explain why a change in pollen or recruitment composition need not produce an occupancy contrast here. It does not establish that assurance evolution rescued the populations, that the zero-pollen margin always exceeds capacity in costly settings, or that a zero-pollen population would persist for400 updates. Under delayed selfing, removing pollen frees additional unfertilized ovules; retaining the observed selfed quantity while merely subtracting observed outcross production would not implement the native zero-pollen response.

## 5. Verification and evidence rank

The native calculator replayed deterministic reproduction from all archived genotypes. It generated no offspring or new demographic histories. The 30 original receipted source files, frozen design, runtime/founder identities, all 16 manifests, and all 1,024 case/receipt hashes were checked. The case/receipt mapping also equals the mapping already admitted by the original endpoint audit: `61d843407819cfe8d11862b50609e03f639703a3eafee2f9afd7cd4c88e5d40b`.

| Validation | Observed discrepancy |
|---|---:|
| Native versus saved expected I/A responses | 0 |
| Native versus saved delivered/outcross/viable-self quantities | 0 |
| Genotype versus saved trace means | 0 |
| Per-update genetic component closure | 0 |
| Case-window sums versus actual endpoints | 0 |
| Independent case/window/component comparisons, 24,576 values | 0 |
| Maximum donor/mother pair expectation versus W expectation | 3.99e-14 |
| Maximum sum(W) versus total seed intensity | 1.42e-13 |
| Maximum case-window component closure | 1.11e-16 |

The independent archive checker was written and run without reading or importing the native-accounting implementation. It reconstructed means and parental contributions from raw alleles/IDs and used saved expected-response fields as declared inputs. It does not independently validate those expectations by itself; the native replay provides that separate check. The [comparison receipt](../data/results/chapter2_tempo_realization_comparison_20261011.json) additionally checks all profile, arm, paired-profile and paired-setting summaries.

The [full artifact receipt](../data/results/chapter2_tempo_realization_receipt_20261011.json) records numerical provenance, preserved original artifacts, tests and independent review. Reproduction commands are in [REPRODUCE.md](../REPRODUCE.md). The saved annual result preserves the native JSON bytes under deterministic gzip; the compact Git summary explicitly omits only the two annual arrays from each case and identifies the full result by SHA256.

This completes the original-state expected-to-realized accounting gate **for the tempo cohort**. It does not replay all old #411 selection-gradient histories or identify an intervention on natural inherited order. Q3 now has verified stage-specific realized accounting; Q3-to-Q4 causal mediation remains unestablished. The confirmed #411 evolution result, the narrow #442 demographic moderator, and the prior failed/equivalent/inconclusive verdicts keep their existing ranks. The active manuscript and submission headline are unchanged. The dated [current evidence addendum](../data/results/chapter2_four_question_current_evidence_addendum_20261011.json) supersedes the October10 snapshot only for current availability and scope.
