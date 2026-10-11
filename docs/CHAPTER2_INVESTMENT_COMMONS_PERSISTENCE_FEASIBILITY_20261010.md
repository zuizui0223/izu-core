# Chapter 2: can pollen-mediated floral public goods affect finite population survival? Source-feasibility verdict (2026-10-10)

**Decision: NO CONFIRMATORY CLAIM YET. Engineering feasibility complete; the source K8 conflict is a transient N=6–9 window and is not matched to an unsaturated H80 survival regime in the declared pilot. No after-outcome budget search is authorized.**

## Scientific question

Within finite Model3, a **unilateral increase in one plant's floral investment** generates a positive net increase in *other conspecific maternal plants' viable seeds* in all 128 visitor-present original source environments, including all **14/14** states where focal investment β is negative but population-wide viable seed Gamma is positive. One representative K8/B48, delayed-selfing source showed **net OTHER mothers +0.3658 seeds per unit focal investment**, while the focal mother's own viable maternal seeds fall by −0.1286. This establishes a model-internal **pollen-mediated reproductive externality** rather than an assumed visitor-attraction/recruitment effect.

The new intended **next claim** is distinctly more ambitious: does the actual genetic evolution of investment toward lower levels reduce **unconditional 80-generation occupancy** versus an intervention on investment mean expression? Such a claim requires sustained β-negative/group-Gamma-positive reproduction, standing genetic variation at the investment locus, demonstrably changed trait mean and nonsaturated occupancy. This investigation tests whether a fair experiment can be set up *before* consuming new confirmatory visitor-history RNG seeds.

## Complete engineering pilot: 384 source-matched 80-update paths

The pilot `data/design/chapter2_investment_commons_pilot_power_20261010.json` was committed before **its** 16 synthetic visitor-history IDs 9701201–9701216 were simulated. It did NOT promise source-level ecological confirmation.

Biological source: unchanged `scripts/chapter2_kb_reproduction.py` plus unchanged `scripts/model3_island/population.py`. At t0, eight joint diploid founders have **matching exactly .2, assurance exactly .35**, and standing allele variation **only at the investment locus**, with source investment mean **.352632** and range of allele homologs [.303630,.412490]. No mutations, immigration or adult survival; B=48 constant. Source genotype support guarantees all subsequent additive investment-mean expressions within [.194770,.521350] without clipping.

Two t0-matched policies:

- **Native**: complete Mendelian source inheritance; the investment genotype determines the reproductive investment phenotype.
- **Founder-mean-centered**: source genotype inheritance remains unmodified, but for each reproductive ledger the parental investment expression is recentered by a **common shift** to the t0 mean. Within-generation investment-genotype variation is retained; genome drift/selection does NOT stop.

**All paired policies have bitwise identical initial reproductive ledgers and first-generation offspring genotypes.** Thus the intervention is specifically on demographic feedback from the *population investment-mean expression*, not a falsely labeled genotype/selection freeze or an initial homogeneity treatment. The two static or stochastic visitor regimes start with the same original hand-authored four types (optima .15/.35/.55/.75, bandwidth .18), and source resource budgets 4.5/6/8, K8/K48 are explored completely.

Reproducible execution `scripts/audit_chapter2_investment_commons_pilot_power.py` and source-only `tests/test_chapter2_investment_commons_pilot_power.py`: focused tests, 384 paths and original JSON artifact upload **PASS** at [Actions #38022335262](https://github.com/zuizui0223/izu-core/actions/runs/38022335262) (after correcting two **test-only** mistaken hardcoded Clopper-Pearson widths; no outcome conditions or confidence formula changed). [Raw full artifact #11658478685](https://github.com/zuizui0223/izu-core/actions/runs/38022335262/artifacts/11658478685), original JSON SHA256 `3f528fcbe7585b6c4a5e713780d7260201630e7f8d4c752c6b5f65d1e1f5a459`; ZIP SHA256 `b18eb18497f8cd0ad43afc1c29449ccbe0a5cc5398f79d00bc59589bb427b7e6`; compact original summary `data/results/chapter2_investment_commons_pilot_power_receipt_20261010.json`.

### Pilot H80 outcome-saturation diagnosis

Each cell consists of 16 paired synthetic visitor histories. These **are feasibility observations, not ecological or statistical significance estimates**.

| Visitor path | K | Ovule budget | Native occupied80 | Centered occupied80 |
|---|---:|---:|---:|---:|
| static 4 visitors | 8 | 4.5 | 0/16 | 0/16 |
| static 4 visitors | 8 | 6 | 0/16 | 0/16 |
| static 4 visitors | 8 | 8 | 15/16 | 15/16 |
| dynamic from same 4 visitors | 8 | 4.5 | 0/16 | 0/16 |
| dynamic from same 4 visitors | 8 | 6 | 0/16 | 1/16 |
| dynamic from same 4 visitors | 8 | 8 | 14/16 | 13/16 |
| static 4 visitors | 48 | 4.5 | 1/16 | 2/16 |
| static 4 visitors | 48 | 6 | 14/16 | 14/16 |
| static 4 visitors | 48 | 8 | 16/16 | 16/16 |
| dynamic from same 4 visitors | 48 | 4.5 | 2/16 | 2/16 |
| **dynamic from same 4 visitors** | **48** | **6** | **12/16** | **13/16** |
| dynamic from same 4 visitors | 48 | 8 | 16/16 | 16/16 |

Only **1/12** environment/K/budget combinations has both source policies' H80 occupancy between .15 and .85 under the pilot16 criterion: dynamic visitors, **K48/budget6**, and the native/centered difference is −1/16 (**not** evidence of a group conflict). This does NOT validate use of that cell for an original **individual-beta-negative** hypothesis: once that K48 population grows, source β may become positive.

The native-arm endpoint *investment allelic means among survivors only* are also near the founder value: for K8/budget8/static original founder .352632 to survivor mean .3583; stochastic K8/budget8 to mean .3545; stochastic K48/budget6 to mean .3597. Those are NOT unconditional genetic evolutionary effects and do NOT establish sustained genetic selection toward smaller floral displays.

## Why K creates a moving selection boundary, not merely stochastic extinction

A separate **source-only, post-outcome** census diagnostic scanned EVERY integer N=1..K at fixed pollen denominator B48, resident monomorphic [.2,.35,.35], same four visitor types, delayed selfing, each budget 4.5/6/8. No visitor RNG histories or new genetically evolving populations were added. All native Model3 ledger and exactly source `capped_poisson_mean` recruitment moments were used: `scripts/audit_chapter2_investment_density_selection.py`, `tests/test_chapter2_investment_density_selection.py`. Execution at [Actions #38022592931](https://github.com/zuizui0223/izu-core/actions/runs/38022592931) dedicated scientific test and raw upload **PASS**; full [artifact #11657999363](https://github.com/zuizui0223/izu-core/actions/runs/38022592931/artifacts/11657999363), raw JSON SHA256 `68142cc102798eb910af4728db06587ff7515d7ce8238d681b88300f8ea44ddc`, ZIP SHA256 `17e59b7e757d4cd7ca77e303c88b2524d3c1c88b3fc03bc52de56b540f5ffdd7`, compact receipt `data/results/chapter2_investment_density_selection_receipt_20261010.json`.

At source budget6 (signs identical for all three budgets, with only seed counts scaled):

| Census N | Focal finite β (log reproductive gene contribution) | Collective Γ_seed (log total viable seeds) | Interpretation |
|---|---:|---:|---|
| 1 | −.350 | −.350 | Investment reduction benefits both; no other mother present |
| 5 | −.172 | −.030 | Both reduce investment |
| **6** | **−.134** | **+.037** | **Selection and seed production opposed** |
| **8** | **−.0632** | **+.1582** | **Selection and seed production opposed** |
| **9** | **−.0306** | **+.2132** | **Selection and seed production opposed** |
| 10 | +.0004 | +.2649 | Local individual selection ~0: do not classify as a reliable positive |
| 11 | +.0299 | +.3134 | Both increase investment |
| 48 | +.5840 | +1.0625 | Both increase investment |

**At fixed B48, the conflict is a very specific source-census window N=6–9, NOT a permanent property of floral investment.** For N≤5, β and Γ_seed both favor *decreasing* investment; for N≥11, they both favor *increasing* investment. At N10 β≈0 and requires an unresolved/near-zero label. Other mothers' pollen-mediated reproductive externalities remain positive for N≥2, but positive spillovers ALONE are insufficient for individual/group selection disagreement at all N.

The exact census cap compounds the problem. At the **SAME N0=8 genotype state and budget6**, mean *uncapped* viable seed intensity is **8.9944** offspring per year; its capped expected recruitment is **7.2680 when K8**, but **8.9944 when K48**. Even with source expected viable seeds **greater than 8**, a K8 adult census at its cap has expected NEXT census **less than 8** after stochastic capped-Poisson recruitment. At budget8, uncapped seed intensity 11.9926 produces **7.8332** expected recruits under K8. This explains how finite carrying capacity can create sustained demographic drift/decline despite initially sufficient gross fecundity; the mechanism is not only a naive 'small K loses alleles' account.

**Caveat:** these β(N), Γ(N), externality(N) values assume the SAME *monomorphic original* phenotypes and fixed visitors. Real multi-genotype trajectories can change visitor compatibility, investment/assurance allele distributions, and thus the local selection boundary. The census diagnostic is an engineering model-operator check, NOT a measured selection gradient at every year of the 384 evolutionary trajectories.

## Detection-power screen: exact paired-event intervals BEFORE more confirmatory runs

The original pilot protocol declared a separate, **hypothetical scenario** Monte Carlo power calculation for 95% conservative paired exclusive-discordance Clopper-Pearson intervals, requiring their lower bound to exceed an absolute **+5pp meaningful-effect threshold**. It uses **no future confirmatory visitor histories**, and does not pretend the pilot16 is a reliable estimate of discordance rates.

| Hypothetical true positive survival contrast | Total fraction of discordant paired source histories | n128 power | n256 power | n512 power | n1024 power |
|---|---:|---:|---:|---:|---:|
| +15pp | 30% | 0.16 | 0.47 | **0.89** | 1.00 |
| +15pp | 50% | 0.09 | 0.32 | 0.65 | **0.96** |
| +20pp | 30% | 0.57 | **0.95** | 1.00 | 1.00 |
| +20pp | 50% | 0.32 | 0.74 | **0.98** | 1.00 |

The powers were estimated from 1,999 simulated paired Bernoulli-discordance multinomial draws per feasible scenario and n; simulation uncertainty and model misspecification remain. These are **not power estimates for the actual investment-evolution effect**, which is unknown. They demonstrate why choosing the confidence method, target effect, expected discordance and sample size together matters more than declaring n192 and tightening a significance threshold afterward. The earlier Hoeffding experiment's failed strict threshold similarly does not prove a zero effect.

## Adjudication and next engineering criterion

**Decision: STOP before launching a confirmatory 'floral commons tragedy causes extinction' trial under current source K8/B48/4 visitors.** The biology-source one-step externality exists, but the model's individual-minus-group conflict occupies a **transient low-census region** while the demonstrated H80 persistence window is either at a source-cap floor/ceiling K8 or at K48 after the individual selection gradient has already changed sign. In the actual pilot, survivor-conditional investment mean does not show robust decline. Running 1,024 independent histories in an outcome-selected budget corner would be a high-compute *low-interpretability* experiment.

A future publication-scale test must first supply a **biologically motivated mechanism that makes reproductive externality, sustained negative individual selection, and finite-persistence sensitivity overlap**, or precommit to a fully separated occupancy and genetic-gradient joint state test with at least one controlled competing model. It should preserve the actual reduced-investment genetic change, monomorphic-vs-segregating source differences, real pollen transfer/parentage and an explicit fixed-horizon occupancy primary.

**No evolutionary suicide, natural island floral shrinkage or persistent commons tragedy has been demonstrated** by these 384 pilot or 168 census static-source states. The supported narrower claim is **pollen-mediated conspecific reproductive externality with a census-dependent, transient local individual-group disagreement and a mathematically identifiable capped-recruitment bottleneck**. This is a mechanistic contribution to a future paper, not a finalized broad biological discovery.
