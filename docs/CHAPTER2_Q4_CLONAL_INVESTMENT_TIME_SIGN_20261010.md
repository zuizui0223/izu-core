# Q4: time- and census-dependent reversal of floral-investment value, without evolution

**2026-10-10. Exploratory exact fixed-genotype Model 3 analysis; NOT a genetic evolution experiment, randomized field study, independent replication, pre-registered test, or evidence of an evolved extinction mechanism.**

## Main ecological question

Does an increase in total plant floral investment that raises short-term reproduction necessarily increase long-term population persistence? The four-question Chapter 2 study asks **threshold → order → realization → consequence**. Here, in a deliberately restricted **Q4** population, inherited variation and visitor changes are absent. Thus we can test this one specific alternative: **could a time-scale reversal arise solely from demography, density and reproductive allocation?**

The answer **within the original clonal, static-visitor Model 3 kernel** is yes.

## Exact original model and scope

Reuse the original `scripts/chapter2_kb_reproduction.py::reproduce_kb` and the already merged #461 census Markov formulation:

- Identical diploid plant genotypes, matching = 0.20, assurance = 0.35, no mutation, no immigrant seeds, adult survival = 0. No genetic variation and no genetic response are generated.
- Four fixed synthetic pollinator functional types with optima [0.15, 0.35, 0.55, 0.75], breadth 0.18, effectiveness 1, and the original encounter/reproductive resource rules.
- Demographic K=8 or 48; pollen background B=48 held fixed; resource/ovule budgets 4.5, 6, 8; founder census N0=8.
- Community-wide *fixed trait counterfactuals* investment **0.34, 0.35 and 0.36** for the entire population at every generation. This is not a rare mutation, focal plant perturbation, evolutionary trait trajectory or genetically mediated treatment. These values are diagnostic, selected on previously exposed synthetic source model context; this is a descriptive source analysis, NOT a fresh independent confirmatory trial.
- For each fixed investment state `I`, compute via the **original** reproductive ledger `μ_I(n)` (expected viable maternal seeds at each n), then the exact `(K+1)×(K+1)` Markov transitions `N[t+1]=min(Poisson(μ_I(N[t])),K)`. Propagate all mass for t=1,5,10,20,40,80. No Monte Carlo histories are sampled.

## Direct, reproducible results

`ΔP80` below is **P80(I=0.36) minus P80(I=0.34)**; these are absolute probabilities, not percent change, fitness gradients or independent ecological estimates.

| K | Budget | P80 at I=0.35 | ΔP1 (0.36−0.34) | ΔP20 | ΔP80 |
|---:|---:|---:|---:|---:|---:|
| 8 | 4.5 | 0.000000003940 | +0.00002510 | −0.00047918 | −0.000000000599 |
| 8 | 6 | **0.03024265** | **+0.000003532** | **−0.00115787** | **−0.000465907** |
| 8 | 8 | 0.90274790 | +0.000000235 | +0.00005213 | +0.000124149 |
| 48 | 4.5 | 0.01527523 | +0.00002510 | +0.00350778 | +0.004281195 |
| 48 | 6 | **0.82871923** | **+0.000003532** | **+0.00321730** | **+0.004220454** |
| 48 | 8 | 0.99818455 | +0.000000235 | +0.00001450 | +0.000014477 |

At initial **N=8**, B48, budget6, baseline `μ_I=.35=8.994424151` expected viable seeds. Across I=.34 to .36, `μ` increases from **8.98005046 to 9.00850876**. Therefore the one-generation reproductive/occupancy response to increasing investment is **positive** in both K arms. But by 80 generations:

- **K8/budget6:** P80(I=.36)-P80(I=.34)=**−0.000465907** (**−0.0466 percentage points**). The finite time-horizon group investment benefit **reverses**.
- **K48/budget6:** same trait shift yields **+0.004220454** (**+0.4220 percentage points**), because census trajectories move into higher density states.

**When does the sign actually reverse?** Propagating the exact 0.34-versus-0.36 counterfactual through *every* horizon, not only selected reporting years, reveals that K8/budget6 begins with a positive occupied-probability difference for updates 1–7 but **first becomes negative at update 8**. Its largest negative difference occurs at update **31** (−0.00140346 probability, or −0.1403 percentage points). Under K48/budget6, no negative occupied-probability contrast occurs in the declared updates 1–80. This timing belongs only to the original fixed-clone, fixed-visitor model; it is not an inferred natural critical period or an evolutionary trait-order effect.

Even the negative K8 shift is **small in absolute probability**; it is neither evidence of evolutionary suicide nor a large adaptive collapse. The low-resource K8/budget4.5 sign is negative at 80 when almost all populations are extinct, and K8/budget8 has a positive sign. This is an outcome-heterogeneous conditional model result, not a universal rule.

## Mechanism: whose reproductive benefit, at which density?

With original B48, four visitors and investment I=.35, source viable seed intensity `μ(n)` changes direction with investment:

- For **N=1…5**, additional community-wide floral investment **reduces** expected viable seed output: attraction supplies too little extra compatible cross-pollen to offset resource allocation cost.
- For **N=6…8** (and in this fixed context larger N), increasing investment **raises** expected seed output.
- At the initial N8 and budget6, the central finite source seed gradient across I=.34/.36 is **+1.42292 viable seeds per unit investment**; at N1 it is **−0.34565**. These are **derivatives of total group seed expectation under a uniform group shift**, not individual rare-mutant `β` gradients.

Thus a population that begins at N8 can initially benefit from a higher floral investment, but after stochastic recruitment lowers census below N6, its *future* reproduction becomes more costly under that trait value. At K8 this low-density cost influences extinction risk strongly. Larger K often moves survivors beyond this low-density range.

To check the explanation quantitatively, the audit decomposes the first-order t80 survival sensitivity using the finite Markov propagator:

```text
dP80/dI = sum(t=0..79) p_t · T'_I · (T^(79-t) occupied_indicator)
```

The contribution of each current census n is separately recorded; `T'_I` is approximated by a central difference at investment .35 ± 1e−5 using the *unchanged source reproductive ledger*. This derivative decomposition is exact **given that numerical derivative**, not an exact symbolic derivative, historical genetic mediation or causal percentage.

| K, budget6 | Contribution from N=1…5 | Contribution from N≥6 | Total dP80/dI |
|---|---:|---:|---:|
| 8 | **−0.072458** | +0.049166 | **−0.023292** |
| 48 | −0.074591 | **+0.285553** | **+0.210962** |

The negative small-N and positive higher-N contributions compete in both capacities. Their relative weight changes with the trajectory's demographic occupancy distribution, explaining how the 80-step sign can reverse even with unchanged genotypes and visitors. The decomposition reproduces the independently propagated centered finite-difference sensitivity to within 5×10⁻⁹.

**Important non-equivalence:** This is a *group-wide uniform fixed-investment response*. Previously observed #452 individual `β<0 / Γ_seed>0` conflict at N6–9 comes from a **one-individual genetic payoff** versus a group reproductive response. The present `μ(n)` derivative cannot substitute for or validate that individual selection gradient. Nor is the observed Q4 sign reversal evidence that evolution actually drives the community-wide investment shift.

## Implications for the four questions

- **Q1 閾値:** ecological census can change the *sign of a collective reproductive response*. It does not uniquely determine a focal individual's full genetic selection gradient.
- **Q2 順序:** the accumulation of low-N exposure over generations matters, but these exact calculations do not manipulate the temporal order of inherited trait evolution.
- **Q3 実現:** clonal fixed genotypes eliminate genetic variance and genetic change. No realized evolutionary sequence is observed; this is a negative control.
- **Q4 帰結:** short-term seed benefits, one-generation occupied status and long-term surviving probability can have **different signs**. The full demographic transition, not a one-year proxy, is required.

To establish an **evolved investment → group harm** story, a new study must show actual allelic investment change and isolate its increment beyond this density-only counterfactual, with matched source genomes and visitor histories, independently fixed operating parameters, comprehensive maternal/paternal/selfing payoffs and unconditional survival. The current original #452 16-history design is post-outcome and **NO-GO** for promotion to a confirmatory harmful-persistence test.

## Files, evidence provenance and validation

- This PR adds `scripts/audit_chapter2_q4_clonal_investment_time_sign.py` and `tests/test_chapter2_q4_clonal_investment_time_sign.py`; no canonical biological code is altered.
- It imports source `reproduce_kb` and merged [#461 exact clonal demographic baseline](https://github.com/zuizui0223/izu-core/pull/461).
- The prior original [#452 source pilot](https://github.com/zuizui0223/izu-core/pull/452) is exploratory and unmerged; no raw new pilot outcome is introduced.
- Frozen prospective results [#411](https://github.com/zuizui0223/izu-core/pull/411) and [#442](https://github.com/zuizui0223/izu-core/pull/442) remain at their old evidentiary rank.
- No new randomized visitor history, genetic trajectory, natural island observation, independent archipelago or prospective biological confirmation is claimed.
