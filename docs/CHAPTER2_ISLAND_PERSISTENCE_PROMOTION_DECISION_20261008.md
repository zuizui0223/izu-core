# Island demographic persistence: evidence-rank and promotion decision (2026-10-08)

## Decision

**PROMOTE to an independently confirmed, narrowly scoped simulation result.** The previously frozen 32-new-visitor-history experiment `data/design/chapter2_island_demographic_independent32_20261008.json` passed its declared pooled gate. Subsequent **different** causal questions that failed—temporal mutation-access order, an across-setting immediate-payoff sign conjunction, and a mating-setting difference in allele transplantation—do **not** invalidate this prior positive estimand.

**DO NOT automatically promote to a general island-biogeographic law, observed evolutionary rescue, an allele-level mediation coefficient, or the current Ecology Letters abstract.** The scientific result is accepted within the declared synthetic demographic intervention; the externality/transport and publication-packaging questions remain separately open.

## What was actually established

The experimental intervention was **whether reproductive-assurance capacity could evolve** during 400 updates of high versus low functional pollinator replenishment. Both arms shared the same founder genetics and matched random history. Then each realized plant population was sampled down to eight individuals, with a postshock carrying capacity of eight and a fixed factorial of synthetic ovule budgets `[2,3,4,5]` crossed with near/far future visitor regimes for 80 reproductive updates. Both near/far historical plant states encountered the same visitor histories at the postshock phase; seed immigration was disabled.

For each of **32 new independent visitor histories**, and within each of the **four predeclared reproductive settings**, the frozen estimand was:

`D = [(survival_farHistory - survival_nearHistory)_A-evolving] - [(survival_farHistory - survival_nearHistory)_A-fixed]`

where each survival probability is the equal-weight mean of eight *terminal occupancy indicators* over the **entire fixed four-budget × two-future-pollination grid**. The four settings were then equally pooled **within each independent visitor history**. All 4,096 postshock trajectories were included; no favourable budget, reproductive setting or surviving population was selected after seeing these new outcomes.

### Independently confirmed narrow result

- **Pooled `D = +0.1083984375` = +10.84 percentage points.**
- **95% percentile visitor-history bootstrap interval `[+0.0654296875,+0.1513671875]`.**
- New histories `30100801–30100832`; one demographic repeat per visitor history; 9,999 history-level bootstrap resamples.
- Predeclared global criterion: positive mean **and** lower bootstrap endpoint > 0. **PASS**.
- Setting-specific interactions and 95% history-bootstrap intervals:
  - delayed control `+0.15234 [+0.05859,+0.24609]`
  - prior selfing `+0.05078 [-0.01953,+0.12109]` (**not individually distinguished from zero**)
  - pollen discount `+0.09766 [+0.01953,+0.17188]`
  - direct assurance cost `+0.13281 [+0.07422,+0.19141]`

The appropriate scientific claim is:

> **In an independently confirmed simulation conditional on a predeclared, pilot-informed demographic-stress grid, allowing reproductive assurance to evolve increased the relative terminal-persistence advantage of populations with a history of low pollinator replenishment.**

This is a **total model intervention effect of enabling A evolution**. The intervention changes the realized later I/A/matching genetic state and thus may operate via many downstream feedbacks. It is *not* an isolated mediation effect of A allele means, and not an effect of the ordering of A versus I evolution.

## Why promotion beyond this scope is not yet authorized

1. **Pilot-informed stress range.** Budgets 2–5 were chosen *after inspecting earlier eight-history pilot outcomes*, which saturated at lower/higher budgets. They **were frozen before the 32 new histories**. This supports a conditional independent confirmation, not universal robustness to demographic risk; pilot-informed design is *not* the same thing as reusing the confirmatory outcomes.
2. **Joint demographic shock.** Capacity changed to eight **together with** ovule budget and density-dependent pollen transfer; the population-stress components are not isolated. This is a meaningful intervention within the declared model but is not a measured natural-island extinction mechanism.
3. **Statistical independence.** There are 32 independent visitor histories, **one demographic realization per history**, and 4,096 nested stress trajectories. The bootstrap correctly uses history as the unit; however, the result does not isolate ecological-history variance from within-history demographic randomness.
4. **Mechanism and order differ.** The already attempted independent 16-history *mutation-access priority* sign test **FAILED** and the balanced exploratory pooled result was zero. That failure rules out the tested general priority interpretation, **not** the 32-history A-evolution treatment's conditional persistence effect.
5. **Unresolved external transport.** The synthetic near/far control is functional visitor replenishment, not measured kilometres, island area, pollinator visitation, species-specific floral costs, or a natural plant population's extinction probability. It requires independent field measurement to establish a natural-island claim.
6. **Technical replay.** The offline execution has source and eight exact raw-shard SHA-256 records plus runnable code and a manual GitHub Actions replay. Until the latter demonstrably completes, note that the independent *scientific* result exists but a second environment's byte-exact replay has not been verified.

## Relation to the Ecology Letters manuscript

Merged PR #411 separately established **four-setting non-necessity of assurance evolution for floral-investment decline**, and **four-setting divergence compression when assurance can evolve**. The 32-history persistence test is a **confirmed, conditional extension** that could be presented in a clearly scoped Results subsection or supplemental figure **if** the target manuscript were deliberately revised and independently audited; it is not evidence of universal evolutionary rescue or inevitable A-first evolution.

The current manuscript has not been revised automatically. Any proposal to make persistence a co-primary claim must define a revised paper question, graphical route, audience/journal fit and disclosed pilot-informed stress selection. Later null or failed tests targeting *other estimands* must be shown, not used to falsely discredit or to shore up the 32-history result.

## Outcome accounting

| Experiment | Scientific status | Different question |
|---|---|---|
| PR #411 four-setting investment necessity/attenuation | **Independently confirmed 4/4** | Does assurance-capacity evolution change floral-investment divergence? |
| PR #413 32-history pooled persistence under synthetic stress | **Independent conditional confirmation: PASS** | Does enabling A evolution alter the *relative survival contrast* after past low pollination? |
| PR #413 64-history five-part immediate payoff conjunction | **FAIL (4/5)** | Is the full preregistered set of mating-rule-specific viable/outcross output signs established? |
| PR #413 16-history mutation-access order contrast | **FAIL** | Does A-first priority outperform I-first differently in prior selfing vs pollen discount? |
| PR #413 16-history allele-donor between-setting contrast | **FAIL** | Does full A donor transfer cause a stronger occupancy effect under pollen discount vs prior selfing? |
| PR #413 four-history mean/distribution, RNG and A dispersion ablations | **Exploratory; no confirmation gate** | What explains the conditional state and persistence differences? |

**Action completed:** evidence rank is corrected without editing frozen experimental design or result, without merging Draft PR #413, and without retroactively expanding the submitted claim ceiling.
