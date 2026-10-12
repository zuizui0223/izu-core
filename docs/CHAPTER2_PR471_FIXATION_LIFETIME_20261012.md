# PR471: genetic fixation, persistence at a horizon, and persistence duration

2026-10-12. **Retrospective diagnostic of existing saved matrices; not a new confirmatory experiment.** The original biology, random histories, 80-update primary endpoint and active manuscript are unchanged.

## Question and principal result

Does the greater probability of low-investment fixation translate into longer persistence, or merely higher occupancy at update80? Under the original shifted visitor arm, low-allele first-fixation probability rises in **all24 settings**, while occupancy at80 rises in14 and restricted mean persistence duration rises in8. In6 settings the endpoint improves but restricted mean duration decreases. Statewise total-pollen equalization leaves every one of these sign classifications unchanged.

These counts are model-setting counts, not independent populations or islands. Effects are exact probabilities of this restricted finite model, not sample survival percentages or statistical significance findings.

## Estimands

Let tau be the first census with N=0, starting with N0=8. All starts are retained.

- Original endpoint: P(N80>0).
- Added retrospective duration: E[min(tau,80)] = sum[t=0..79] P(Nt>0), measured in model update intervals. This is neither uncensored lifetime nor the sum of occupied censuses1..80 (both are exported separately).
- First low/high fixation: first census containing only the respective allele before extinction; count entry once, not every subsequent fixed census.
- Six endpoint partitions: low-fixed/high-fixed/segregating and alive; extinct after low fixation/after high fixation/before fixation. Because there is no mutation or immigration, genetically fixed states can leave their class only by extinction.

The expression comparison is genotype-dependent I versus clamping I=0.35 while still transmitting alleles. It is not evolution versus no evolution. Conditions remain K8/B48, matching0.20, assurance0.35, two investment alleles0.20/0.50, four visitor types, no mutation/adult survival/immigration. Budget6/8 is the model ovule-production budget, not observed nutrient supply. Lambda shifts visitor optima, not the percentage of visitors lost.

## Endpoint versus duration: all24 shifted-visitor settings

Endpoint differences are **percentage points**; duration differences are **model update intervals**. Both are genotype expression minus clamped expression. Full48-pair results including the equalized arm are in the [compact readout](../data/results/pr471_fixation_lifetime_readout_20261012.csv).

| Lambda | Mating setting | Budget6 endpoint pp | Budget6 duration | Budget8 endpoint pp | Budget8 duration |
|---:|---|---:|---:|---:|---:|
| 0.25 | delayed_control | +0.023170 | -0.495419 | -1.243920 | -0.527058 |
| 0.25 | prior_selfing | +0.162231 | -0.291238 | -1.455222 | -0.633145 |
| 0.25 | pollen_discount | +0.202202 | -0.212727 | -1.535159 | -0.676928 |
| 0.25 | assurance_cost | +0.016240 | -0.305363 | -1.904343 | -0.909062 |
| 0.50 | delayed_control | +0.326901 | +0.327467 | -1.510251 | -0.905167 |
| 0.50 | prior_selfing | +0.327363 | +0.349639 | -1.463949 | -0.906301 |
| 0.50 | pollen_discount | +0.327254 | +0.357407 | -1.449708 | -0.908214 |
| 0.50 | assurance_cost | +0.035283 | +0.103026 | +0.357208 | -0.616447 |
| 1.00 | delayed_control | +0.325651 | +0.426651 | -1.256890 | -0.903385 |
| 1.00 | prior_selfing | +0.325651 | +0.426652 | -1.256886 | -0.903385 |
| 1.00 | pollen_discount | +0.325651 | +0.426652 | -1.256885 | -0.903385 |
| 1.00 | assurance_cost | +0.033297 | +0.150302 | +1.228381 | -0.401237 |

At budget6, all12 endpoints are positive, but duration is positive only in8 and negative in4 (range -0.495419 to +0.426652 intervals). At budget8, duration is negative in all12 (range -0.909062 to -0.401237), including the two positive endpoints. These added estimands do not replace or overturn the earlier endpoint verdict.

## Reaching low fixation is not sufficient for persistence

At budget6 with shifted visitors, **50.863–54.579%** of starts reach low fixation by80 under genotype-dependent expression. Of those that reach it, only **0.087–2.172%** remain occupied at80. This conditional percentage mixes different entry times and census sizes; it is not a causal effect of becoming fixed. Crucially, the all-start measure counts starts that fixed and subsequently died.

For lambda0.25/assurance_cost, budget6: low-fixation probability is50.8627% under genotype expression versus45.8719% under fixed expression. Yet restricted duration is15.7751 versus16.0805 updates; the original endpoint is0.13555% versus0.11931%. A small positive endpoint does not erase earlier persistence losses.

For the same context at budget8: low-fixed/alive endpoint mass rises from34.000585% to41.515237%, while high-fixed/alive mass falls from34.000585% to24.582601%. Including the very small segregating remainder yields the original -1.904343pp total. This is a mutually exclusive probability partition, not independent causal pathway effects or mediator fractions.

## Standardizing post-fixation comparisons

Both expression policies were evaluated from each identical fixed genotype/census N=1..8, for each common remaining duration1..80. High-fixed expression has lower survival than I=0.35 throughout this finite grid. Low-fixed expression generally has higher survival, but not universally: lambda0.25, delayed_control or assurance_cost, either budget, N8 and one remaining update give small negative differences (in both visitor arms). All other low-fixed grid entries are positive above the1e-12 arithmetic screen. The repeated state/horizon entries are not biological replication. This check cannot identify mediation by natural evolution or prove a general low-investment fitness advantage.

## Verification and reproduction

The code first counted entries and deaths in full forward propagation, then separately used renewal recursions on segregating and fixed blocks. Duration was checked by backward rewards and the extinction-time distribution. Additional readback made first fixation absorbing in a separate reduced chain and used an augmented matrix-power reward calculation.

- 96 saved165-state matrices;48 expression pairs;7,776 first-passage time rows and61,440 common-entry post-fixation comparisons.
- 288 previously native-executed endpoints agree within 4.885e-15.
- 384 independent hit-flag checks: maximum error 7.772e-16.
- 96 augmented-block lifetime checks: maximum error 7.105e-14.
- 96 sums of the earlier published time series: maximum error 1.421e-14.
- 13 closed-form/invalid-input unit tests pass after missing-implementation failures were demonstrated. These are local focused tests, not a completed full-repository CI claim.

New first-passage/lifetime results propagate previously reconstructed saved matrices. PR487 establishes native agreement at the original endpoints, not a native rerun of these new time-resolved quantities. No sampling confidence intervals, new registered success rule, universal resource effect, evolutionary-rescue claim, historical-discovery authentication, or external DOI deposit is introduced.

Required input conversation archives (unchanged):
- `izu_core_pr471_verification_20261012.zip`; SHA256 `1f58a0f0988d1215a53ea50aa30ece049a37da4a0cd459a72a44f2f05065a783`.
- `izu_core_pr471_native_outputs_20261012.zip`; SHA256 `b7f3814d682095e91783db0e4cebef2f0eb235835ff71de68e3ad28bb3c3ca84`.
- Matrix member SHA256 `9d13fe6d116e2c0ef7e08658fa9d9488cb7320e8e7cab2ecc9946e0780a852c3`.

```bash
OPENBLAS_NUM_THREADS=1 python scripts/audit_pr471_fixation_lifetime_20261012.py \
  --archive /path/to/izu_core_pr471_verification_20261012.zip \
  --native-archive /path/to/izu_core_pr471_native_outputs_20261012.zip \
  --out /path/to/fixation_lifetime_results
python -m pytest -q tests/test_pr471_fixation_lifetime_20261012.py
```

The reader rejects altered input ZIPs or incomplete matrix domains. The run emits complete96-arm/48-pair summaries and all time/state tables. The compact committed readout selects four contrasts/flags from the paired CSV without changing values. Full new tables, code and checks are also retained in the conversation archive; do not describe that attachment as a permanent public scientific deposit. Native-source provenance remains in [PR487 companion](CHAPTER2_PR471_NATIVE_VERIFICATION_20261012.md).
