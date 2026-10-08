# One-process Chapter 2: ecological payoff → selection → evolution → feedback → persistence

**2026-10-08 status: DESIGN FROZEN + IMPLEMENTED, NEW COHORT NOT EXECUTED.** No new 64-history biological trajectories have been executed or adjudicated under this protocol. This is a **clean branch off main**, separated from the 80+ file exploratory Draft PR #413. The merged #411 four-setting result and PR #413 independent32 *conditional* survival confirmation are the **motivation**, not new-cohort outcomes.

## One biological question

> **When pollinator replenishment deteriorates, how do the maternal/outcross, paternal/export, autonomous-selfing and allocation payoffs change which inherited floral states are selected, and how does the resulting evolution reshape both geographic floral divergence and later demographic persistence?**

This question does not assume a serial selfing-first mechanism. Flower investment can decrease without evolving assurance, while assurance evolution can modify which environment loses investment and may influence the inherited genotype mixture available during future demographic stress.

### One continuous process, two interventions

```text
Shared genetically identical 48-plant founders + fixed mating-system rule
                          |
          Near vs far VISITOR REPLENISHMENT
          × A-capacity fixed vs A-capacity evolving
                          |
    400 successive reproductive updates in the SAME ABM
           |                 |                  |
      pollen delivery   parental genome     recruitment / inherited
      and costs         contributions       three-trait state
           |                 |                  |
    corrected fixed-     maternal F/2 +     matching, investment,
    resident rare-       paternal P/2 +     assurance mean/variance
    mutant diagnostic    selfed S            at t0/100/200/300/400
                          |
               Actual finite t400 population
                          |
                FORK WITHOUT REFITTING
            - retain ALL plants, capacity48
            - take 8 plants, capacity48
            - take 8 plants, capacity8
                          |
          each × ovule budgets 0.5/1/2/3/4/5/8
                × common future near/far visitors
                          |
           next 80 reproductive updates, same ABM
                          |
         expected payoff + genetic state + extinction
```

There is **no separate response-rule layer** and no manual evolutionary trajectory prescription. For each source cohort, the shock runs fork the realised **finite inherited genotype state**. Fixed and evolving A capacity are matched interventions **only in the first 400 updates**. At the t400 fork, **both historical arms switch to the same A-evolving future rules**. A fixed capacity in the prehistory never means zero realised selfing.

## What is genuinely new compared with the two prior positive findings?

**Merged #411, prospectively confirmed:** four reproductive settings, 64 visitor histories ×8 nested repeats, 1,000-update divergence: fixed assurance did not prevent low-replenishment investment decline; evolving assurance compressed environmental differentiation in 4/4 settings, mostly due to additional high-replenishment investment loss. Corrected local rare-mutant gradients identify the maternal and paternal outcross return available to be lost in high replenishment.

**Draft #413, separately confirmed conditional effect:** a *new* 32-history test of 80-update occupancy after 400-update evolution passed its pooled interaction criterion (+0.10840 [95% history bootstrap +0.06543,+0.15137]); but the small-population stress budgets were selected following **exposed eight-history discovery runs**, and only one demographic repeat per history was used. This is a valid independent-new-history conditional model result, **not** automatically a general natural-island extinction rate.

**The new protocol remeasures the complete chain within the SAME new histories.** It does not splice independently sampled selection gradients, evolution and persistence means into one apparent mediation analysis. It also tests broader shock coverage, decomposing effects of reduced maternal reproductive resources, a bottleneck and maintained small carrying capacity instead of treating their combination as a generic single stress treatment.

## Predeclared experimental units and why a single experiment is meaningful

The **64 independent visitor histories are the ecological units**. Each history is paired across four settings, near/far, fixed/evolving assurance and **two nested demographic repeats**. The 400-update prehistory runs create **2,048 actual genetically evolving plants/populations** (not 2,048 independent visitor environments).

The terminal populations are then forked to the 3×7×2 postshock grid (**42 branches per prehistory, 86,016 poststress trajectories**). The three regimes are:

| Regime | Actual plants transferred | Capacity | What it tests |
|---|---|---|---|
| Fecundity only | all surviving t400 plants | 48 | Reduced maternal budget without an imposed founder sample |
| Founder bottleneck | up to 8 sampled surviving plants | 48 | Bottleneck with potential demographic expansion |
| Bottleneck + small capacity | up to 8 sampled surviving plants | 8 | Continued small population, where earlier pilot found a conditional persistence effect |

All three regimes use **every declared** budget 0.5, 1, 2, 3, 4, 5, 8 and both newly seeded visitor environments. The two bottleneck arms must begin from the same *selected eight* founder genotypes. Their future demographic random-stream **seeds are also paired**, so the declared treatment difference is subsequent carrying capacity (although changing population sizes can make later random-number consumption diverge). The separate fecundity-only arm has no bottleneck and retains its own stochastic stream. This is common-random-number variance control, not additional independent ecological replication. Future visitor processes and demographic RNG streams are matched across the historical and assurance-evolution counterfactuals, but this pairing is **variance reduction**, not extra independent histories.

When a prehistory is extinct, every planned future arm has occupancy 0 and missing trait endpoints, **not** silently excluded from the survival comparison. When a prehistory has fewer than eight plants, transfer only available plants and explicitly report the bottleneck shortfall.

**Common-future mode rule (identification correction before any new outcomes):** at t400 **both** previously A-fixed and previously A-evolving histories enter the same future `assurance_mode=evolving` and `mutation_traits=(True,True,True)` at rate 0.01. Historical A-fixed plants start the future at their inherited A=0.5, but may subsequently evolve; historical A-evolving plants begin from their t400 evolved genotype distribution. Neither state is reset. This contrasts *past evolutionary opportunity* under identical subsequent opportunity, rather than a combined 480-update fixed-versus-evolving policy.

## Selection and evolution are not the same measurement

- At the same model state, **reproductive payoffs** are attributed to viable maternal outcross, paternal pollen export, viable autonomous selfed seed contribution, inbreeding depression and resource costs. Genomic fitness accounting is `W=F/2+P/2+S`, not maternal seed set alone.
- A **corrected fixed-resident rare-mutant investment gradient** at source/observed resident means is a *local counterfactual selection diagnostic*, never the actual polymorphic finite population's full selection gradient. Preserve maternal, paternal, selfing-displacement and ovule-cost terms and their exact additive identity.
- The **ABM** evolves distributions from reproduction, Mendelian inheritance, new mutation, nonrandom recruitment and chance extirpation. This gives actual trait means/variances and finite mortality histories.
- A **deterministic genotype density / PDE** would be a companion requiring numerical admission. Previous positive-mutation high-resolution long-run comparisons were not admitted; do **not** claim PDE matches the 400+80 ABM or treat an unvalidated heat approximation as ground truth.

That ordering prevents the previous mistake of interpreting a pointwise payoff as identical to long-term population fitness.

## Two hierarchical scientific gates: one joint theory, no post-hoc rescue

**Gate 1 — Evolutionary divergence, all four settings:** At t400, in A-fixed populations the far-minus-near investment contrast must be negative with history-bootstrap95 upper below zero. Evolving-minus-fixed interaction must be positive with lower above zero in **each** setting. This is a stringent independent cohort re-challenge at **400, not 1,000 updates**. Its failure does not overturn #411's previously proven 1,000-update result, but it prevents declaring this unified new experiment successful across the full process.

**Gate 2 — Subsequent persistence, all settings pooled:** For every visitor history and setting, average the two nested demographic repeats and both common future visitor environments. Over **all seven** ovule-budget points, compute trapezoidal area weighted by **log ovule budget**, normalised over 0.5–8. In the `bottleneck_small_capacity` regime calculate `[(S_farPre−S_nearPre)_A-evolving−(S_farPre−S_nearPre)_A-fixed]`. Pool all four settings equally **within history**, then bootstrap the 64 history-level values 9,999 times. Pass only if pooled mean and bootstrap95 lower endpoint are positive. All four setting-specific estimates are mandatory even if some intervals include zero.

This postshock contrast tests an **inherited-history legacy**, not the original #413 cumulative fixed/evolving policy over the whole period. Stage 2 is reported even when Stage 1 fails, but the single **payoff → evolution → survival chain** is said to pass only when **both** rules pass. Compulsory secondary results: the other two demographic regimes, all budgets, both post visitor arms, extinction timing and initial viable maternal output, even if opposing the primary effect.

### Why the broad budget grid matters

The older pilot found trivial universal extinction at budgets ≤1 and almost universal survival at 8 under one small-capacity shock. A test restricted to 2–5 could overstate generality. The present **entire log-spaced coverage** keeps floors and ceilings and uses a predeclared quadrature of the full risk window, not the best middle cells. **The range is still pilot-informed and uncalibrated to any natural frequency of environmental stress**; broad coverage does not transform it into random sampling from nature.

The three regimes assess the extent to which a positive prior 32-history result survives without the artificially low future capacity. If it exists only under the eight-plant maintained-capacity case, that outcome itself is informative and cannot be hidden.

## Technical feasibility and reason to delay the biological run

The protocol declares **2,048 prehistories + 86,016 paired 80-update descendants**, substantially larger than the prior 4,096-case persistence experiment. Source code, mutation masks, history-level seeds and exact task identities must be pinned before executing the production campaign. The design compiler can enumerate the complete grid and compute its weight vector **without using a single outcome**.

At this stage **do not run production simulation** while runtime/memory and source-artifact provenance have not been admitted. An engineering-only smoke run on existing source model **must not inspect the new 64 history outcomes**. If infeasible, record a new future cohort/protocol as a separate design; do not quietly reduce the 86,016-case plan after inspecting any partial outcomes.

## Explanatory ceiling

A joint positive result would show that **ecological payoff changes can be realized as evolutionary changes which alter future demographic persistence in a specific finite plant–visitor model**, and that the effect depends on the way demographic stress acts. It would not show that a named island's pollinators declined, that selfing evolved before investment, that genetic variance alone mediates rescue, or that the selected 0.5–8 risk range is a naturally observed shock distribution.

The corresponding island-empirical test still needs effective visitation/pollen deposition, autonomous selfing, viable outcross maternal and paternal fitness, allocation cost and inherited changes through time. Present Chapter 1 and 3 cross-sectional results are not a complete joint selection-fitness transition dataset.

## Files / state

- Frozen design: `data/design/chapter2_unified_payoff_evolution_persistence_20261008.json`
- Manifest/cost-only compiler: `scripts/plan_chapter2_unified_payoff_evolution_persistence.py`
- Automated non-peeking design tests: `tests/test_chapter2_unified_payoff_evolution_persistence.py`
- **Scientific outcomes: NONE yet.** This branch is design-only and is deliberately separate from the large Draft PR #413; existing failed exploratory routes are neither rewritten nor deleted.


## Execution implementation and pre-production engineering checks (2026-10-08)

The frozen protocol is now **implemented**, rather than merely outlined, in separate state-preserving stages:

1. `scripts/run_chapter2_unified_payoff_prehistories.py`: evolves each historical group using the frozen, unmodified Model 3 reproductive/inheritance functions. Saves the complete t400 diploid genotype/ancestry/mutation-flag/individual-ID state as `.npz`, plus an explicit JSON receipt containing the exact source-file hashes and census/payoff/rare-mutant-gradient diagnostics.
2. `scripts/run_chapter2_unified_payoff_postshock.py`: loads **only the hash-admitted full t400 genotype**, uses common future visitor realizations and matched demographic RNG streams, forks it into all 42 stress arms, and preserves a **per-file SHA-256 receipt**. Every branch uses the *identical A-evolving future policy* regardless of historical A-fixed/A-evolving assignment.
3. `scripts/summarize_chapter2_unified_payoff_evolution_persistence.py`: demands all **2,048** prehistory states and all **86,016** postshock cases, rechecks both genotype and postshock file hashes, and then applies the predeclared two-stage history-bootstrap gates. Neither historical repeats nor the 42 nested postshock conditions are treated as independent ecological histories.
4. `tests/test_chapter2_unified_payoff_runner_smoke.py`: engineering-only two-reproductive-update smokes use **OLD visitor seeds 26110601** (not the 64 new cohort seeds), check additive corrected rare-mutant gradient accounting, exact genotype round-trip, identical shared future streams, and the 60-of-64 admissibility rule.
5. `.github/workflows/chapter2-unified-payoff-evolution-persistence.yml`: manual-only 64-shard workflow with admission before calculation, hash-verified prehistory/postshock artifacts, and an all-case final readout. It has **not been triggered** and a new biological result must not be reported before a completed verified workflow.

### Engineering-only wall-time sample (not a scientific outcome)

A locally available copy of the pre-confirmation frozen biological source was tested using **OLD** visitor seed `26110601`. For one historical simulated plant population (400 reproductive updates), elapsed wall time was **0.2257 s**; for the same legacy evolved state forked to the 42 future stress conditions (each 80 updates), **0.9189 s**. This gives a purely illustrative **0.65 hours serial runtime** by scaling the measured case to 2,048 prehistories, excluding packaging/GitHub setup and history/setting variability. The measured old-seed population had 48 surviving plants. This is **not a source-locked production speed guarantee** and uses no new cohort history or scientific outcome. Larger/other configurations and CI runners may differ materially.

### GitHub manual launch constraint

The production workflow is intentionally `workflow_dispatch` only. **GitHub requires a manually dispatched workflow file to exist on the default branch.** Therefore a brand-new workflow file that exists only on this Draft PR branch is not directly dispatchable in the GitHub Actions UI. The technical path is: (1) pass existing PR scientific-gate/CI tests, (2) review and merge the **design + implementation only**, (3) manually launch the frozen workflow from `main`. A failed or queued PR CI must not be hidden by a premature merge. A manual Actions launch also has repository compute-cost implications, and only a completed 86,016-case artifact gives a new scientific answer. This PR is not an already running experiment.

### Reproducibility and launch guard

Do **not** start or interpret partial production without the source-hash/CI admission, because the previous Draft PR #413 contained many source-specific post-outcome explorations. The new protocol's population histories cannot be interchanged with those prior archives: this one additionally fixes postshock **future A evolution equal across historical modes**, and broadens the demographic risk domain and two independent nested demographic repeats.

The original base-source commit is pinned to `94c051850a43b89047e78e653edae25b043624ab`, the prospectively confirmed four-setting source artifact digest is pinned to `34bedf03e6cde0b3d7f5140b7f352227b5dd1550c097e66e42022aa9830d3d8c`, and new-run receipts hash every model/execution source used. If the numerical model or outcome definition changes after production begins, stop and create a separate version rather than modifying the frozen cohort.

**Result status remains: NO new 400+80 generation biological findings.** The existing #411 and #413 conclusions keep their original, different scientific scopes.
