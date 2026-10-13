# Initial-state evolutionary response clock: identifiability gate

**2026-10-13 — retrospective descriptive audit, not a new prospective result.**
This is an additive companion to the single four-question manuscript, **not** a new manuscript headline or an alteration of any registered criterion. Input is the previously admitted complete 2,304-history *compact* ecological-order summary, not 2,304 newly replayed genomes. The primary ecological reversal test remains unsupported, as originally recorded.

## Research question and the first obstacle

Can **a clock computed exclusively from founding plant genotypes and the declared visitor context** predict which of the six historically fixed sustained response outcomes will occur by update 200?

The unchanged source design (`scripts/run_ecological_order_boundary_20261013.py`) has exactly **two founder blocks, nine visitor contexts, and 128 paired replicate streams per founder/context**. Within a `(founder, context)` cell, the starting diploid plant state and visitor context are the same for all 128 replicates; `replicate` enters the salt for future stochastic updates, not the initial biological features. Those same replicate IDs/streams are reused across the nine visitor contexts. A deterministic predictor restricted to time-0 genotype + context must therefore give a single class (or one probability vector) to the 128 histories in a cell. There are at most **18 distinguishable time-0 profiles**. A model that uses realized first-generation seeds, time-1 genotypes, event labels, future RNG streams, or recovered mutation outcomes would be a different, information-leaking predictor.

The post-outcome **oracle** below is the maximum *realized-sample* accuracy of a deterministic six-class lookup allowed to distinguish all 18 founder/context groups. It cheats by seeing each cell's results, so it is **not** a trained model, prospective score, or population-level upper bound. It nevertheless diagnoses an irreducible source of *observed within-cell classification variation* for any initial-state-only clock in this particular realized sample.

## Executed, descriptive upper-bound arithmetic

| Information exposed to an oracle | t0 groups | Correct six-class / 2,304 | Accuracy | Strict-order correct / 770 | Strict-order accuracy |
|---|---:|---:|---:|---:|---:|
| None; global majority | 1 | 895 | **38.85%** | 435 | 56.49% |
| Founder genotype block only | 2 | 895 | **38.85%** | 435 | 56.49% |
| Visitor context only | 9 | 1,102 | **47.83%** | 448 | 58.18% |
| Both founder and visitor context | 18 | **1,117** | **48.48%** | **463** | **60.13%** |

The joint partition's six-class empirical categorical entropy (best *post-outcome* lookup log loss, nats per trajectory) is **1.101973**; without grouping it is **1.527082**. It permits context-dependent probabilistic forecasts, but does not mean any proposed biological clock has achieved this score or that the difference is significant. The founder-only majority accuracy staying equal to the global majority does **not** demonstrate zero genetic effects; it is a coarse observed-sample majority statistic.

All six outcomes are retained: `assurance_first=335`, `investment_first=435`, `near_simultaneous=358`, `assurance_only=895`, `investment_only=10`, `neither=271`. Exactly `1,128/2,304` achieve both events including near-ties, while only **770/2,304** achieve a strict A/I order. The strict-order binary oracle is **postselected on achieved two-event histories** and therefore cannot be used to infer accuracy for all starts, fit an unbiased survival model, or claim an acceptable success rule based on confidence-interval lower bounds. The old 0.05 change/20 sustained censuses/5-update tie rules are unchanged.

## Interpretation for a biological `response clock`

1. The simple rate expression `tau_k ~ required_change/(G_k * beta_k)` is a *candidate approximation*, not an admitted predictor. The source t0 assurance phenotype is identical across adults, so the existing 320-history source-audit's exact t0 expected A response is zero even though segregating diploid alleles can create first-generation variation. A no-access/no-variance signal cannot be blindly interpreted as infinite physical evolutionary time.
2. The correct genetic accounting uses full maternal, paternal and selfed returns and the standing diploid genotype distribution: `W_i = F_i/2 + P_i/2 + S_i` and `E[delta gbar | next occupied] = Cov(g_i,W_i)/mean(W_i)` in the source's matched no-survival/no-immigration/no-mutation accounting scope. An *individual rare-mutant* selection beta is not interchangeable with this source-state covariance. If using `G*beta` as a forecast, specify which finite-plant genetic covariance and cross-trait terms are being approximated.
3. A useful next predictor has two nonidentical pieces: (i) **access delay** for a selectable allele/genotype distribution to arise (segregation or mutation), and (ii) **response-time distribution** after access. Each six-class event probability must incorporate first-passage thresholds, ties, nonarrival, fixation/absorbing states, survival/extinction and finite parental sampling. Initial state and visitor regime may predict probabilities, **not the stochastic identity of the successful replicate**.
4. For model comparison, the ecological-only, founder-genetic-only, and joint t0 forecasts must all use the same held-out **independent history seed IDs**. Since seeds are *paired across contexts*, every context of a given seed is in the same train/test fold. Nested repeated runs/contexts are not independent histories. Founder-block generality cannot be established with only two founding genotypes.
5. Use predeclared proper scoring rules (multiclass log loss / Brier) and calibration, not merely the hit rate on the censored strict-order subset. Compare biological clock to explicit ecological-only, genotype-only and calibrated joint/constant-frequency baselines. The latter are not causally separable from predictions using current data.

## Executed validation and limits

- `scripts/audit_chapter2_initial_clock_identifiability_20261013.py` validates the frozen 18-cell source-labelled inventory (2 blocks × 9 contexts × 128 histories), original six-class partitions, original order-score `D`, preserved source identifier, and **Git blob of the input summary**. It computes all descriptive majority/entropy/Brier oracles reproducibly without replaying biology or altering original readouts.
- `tests/test_chapter2_initial_clock_identifiability_20261013.py` checks category and denominator partition, monotonicity of nested oracles, source drift, impossible category counts, swapped contexts, duplicate cells, and postselected strict-only accounting. The exact-input integration check is run when the original PR491 branch file is present. The offline sandbox executed **14 tests**, with the exact-input integration check unavailable in the sandbox; it must pass on GitHub before claiming a source checkout replay.
- The **first aggregate-only phase** does not calculate actual t0 response. The separate source-authenticated **raw t0 follow-up** below does. Neither phase estimates two-trait first-passage times or out-of-sample clock accuracy. There are **no new genotypes, stochastic trajectories, p-values, bootstrap intervals or significance conclusions**. Observed-sample oracle comparisons are descriptive only and cannot substitute for preregistration.

## Completed original-genome t0 follow-up (run 38337931445)

The newly isolated, read-only GitHub job [38337931445](https://github.com/zuizui0223/izu-core/actions/runs/38337931445) **succeeded**. The job downloaded the already public **251,663,558-byte** original `ecological_order_actual_github_38312090996.zip`, checked outer SHA256 `819741aa4a9f5bc1aaf2dadddbd56b79d158fc9295d07fc3bffe362693fc056a`, all nine nested provider ZIP hashes and all 2,304 raw case hashes against the frozen event/category registry. It verified that each founder×visitor context has an identical full initial genotype across its 128 stochastic repeats. No new biological generation, mutation experiment, threshold adjustment, or trajectory replay was executed.

A separate [18-row compact result](../data/results/chapter2_initial_clock_t0_raw_20261013.json) now reports original saved **t0 genetic-return Price response** and starting genetic-variance proxies. The features depend only on initial genotypes, original t0 female/paternal/selfed return components and visitor context. Later results were read solely for identity/category admission.

| Source-derived t0 diagnostic | Confirmed result |
|---|---:|
| Source-genotype initial profiles across 2,304 paths | **18** |
| Founding expressed assurance phenotypic variance | **0** in all 18 |
| Founding expected assurance genetic-selection response | **0** in all 18 |
| Hypothetical unmutated F1 A expressed Mendelian segregation variance | **0.001953125** in all 18 |
| Main founder investment allelic additive-variance proxy | **0.00631714** |
| Confirmation founder investment allelic additive-variance proxy | **0.00476074** |
| t0 inherited-investment response favours investment decline | **12/18 conditions** |
| t0 inherited-investment response favours investment increase | **6/18 conditions** |

Exploratory descriptive association with later registered 200-update **investment-decline event** (any of A-first/I-first/tie/I-only): **1,060/1,536 = 69.01%** of starts in the 12 initially decline-favoured cells; **78/768 = 10.16%** of starts in the six opposite-direction cells. These cell groups are neither randomized nor independent ecological systems; the same replicate seeds are paired across contexts, and differences confound founder genetics, activity and functional composition. They are **not** a six-class clock, adjusted selection effect, causal genetic-access attribution or prospective accuracy estimate.

**Mechanistic constraint revealed:** the initial expected A response is identically zero even though assurance is heterozygous and Mendelian segregation makes selectable variation possible. A one-stage `0.05 / t0 R_A` clock is formally undefined/infinite for all 18 initial states and cannot predict observed A-first histories. Building the proposed two-stage *access → response* clock therefore requires predicting first-generation segregation/mutation and subsequent selection without reading observed post-t0 states. The observed t0 investment direction alone is promising for **I-event incidence** but is not a model of relative A-versus-I crossing times.

The next gate remains an outcome-blind 18-condition, t0-only two-stage clock with all six categories, held-out paired-history evaluation and predeclared proper scores. The raw follow-up is source verification and feature extraction, **not confirmation of that clock**.

## Single next scientific gate

Compute **18 source-matched initial state feature vectors** from the authenticated original raw package, explicitly recording the t0 full Price response (`F/P/S`), standing additive-variance proxy and segregation-derived A access potential, with no outcomes read while forming feature vectors. Then test a predeclared probabilistic six-class *clock* on independently held-out seed clusters and estimate power/sensitivity before launching genuinely new histories. First demonstrate performance against ecological-only and genotype-only baselines; do not reduce the 6-class target to a strict A/I subset to recover a 60% result.

Preserve the frozen 2,304-cohort original ecological reversal verdict and the separately supported four-setting assurance-compression result. Do not promote this exploratory identifiability gate to a new empirical mechanism, universal ecological threshold, or naturally order-mediated persistence effect.

**Source identity:** [`data/results/ecological_order_boundary_20261013.json`](../data/results/ecological_order_boundary_20261013.json) original Git blob `5608ad2cdcbef167fe9062ab5f26318abf2e1bd9`; original execution `328548612e93469fcc8663f24548530a57399b9a`, provenance recorded by the source reader. Existing package: [four-question-resolution-20261013 GitHub Release](https://github.com/zuizui0223/izu-core/releases/tag/four-question-resolution-20261013); study PR: [#491](https://github.com/zuizui0223/izu-core/pull/491).