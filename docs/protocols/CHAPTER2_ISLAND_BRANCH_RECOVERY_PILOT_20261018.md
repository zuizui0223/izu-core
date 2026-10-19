# Chapter 2 — the three-question pollinator-return recoverability study

**Pre-outcome exploratory micro-pilot — 2026-10-18. Single-Article program: PR #590.**
This is a *proposed pilot implementation*, not an executed experiment, registered confirmation, supported ratchet/lifeboat claim, or second manuscript. The 2026-10-13/17 historical data, Q1 results, Q2 384-case `both_inconclusive`, paper figures, archived sources and receipts remain frozen.

## One overarching island-evolution question

Is a floral island syndrome a reversible adaptation to pollinator scarcity, or can evolutionary recovery become unavailable **while plants still survive**?

Three questions ONLY:

1. **Necessity (existing Q1):** Under effective pollinator limitation, does lower floral investment I require evolution of reproductive assurance A? **No, within the tested finite Model3**, including separately tested independent founders; importantly A **fixed at expressed 0.5** still allows selfing. It is NOT a no-selfing intervention.
2. **Recoverability (new main Q2):** If functional pollinator services are restored at time t, what is the conditional probability that an **occupied and already-declined** plant population regains founder-relative high-I expression within horizon H? Estimate whether a sustainable no-return-window exists; distinguish biological recovery from simple post-return survival or states that never declined.
3. **Assurance (new causal Q3):** Does assigning A to **evolve vs remain expressed at 0.5 throughout history** change the recovery curve? Within saved evolving-A states, additionally **freeze expressed A at its attained checkpoint mean** in the future to explore how continuing A evolution differs from carrying the already-evolved A level.

### Outcome and selection requirements

`I_star` is each founder's measured t=0 population mean of I (not a fitted optimum). A history is an eligible recovery *state* only if alive at checkpoint t and mean `I_t <= I_star − 0.05`. Count recovery only when the population remains extant and the mean I is >= `I_star` for >=5 consecutive future occupied censuses within H=25. A checkpoint is never relabeled as recovered solely because I was already high when visitors returned.

Keep separate outcomes:

- **State-specific recovery probability**: repeated future streams conditional on being alive and having declined at t; undefined when no such states.
- **Policy effect**: unconditional joint survival-and-high-I attainment over **all originally randomized founder×visitor blocks**, with deaths before t retained as failures; this is not synonymous with regain-after-decline and must never silently condition on survivors.
- **Selection diagnostic**: local marginal relative focal maternal+paternal output for a +0.02 increase in I, with donor/recipient redistribution; compare visitors restored vs absent. This is **not** a formally validated long-term rare-mutant invasion fitness gradient.
- **Genetic support theorem**: if no mutation at I and no seed immigration, the maximum resident I allele cannot increase. For a living state with max I allele < `I_star`, high-I recovery is structurally impossible under the specified rules. Conversely, retained support does **not** guarantee recovery.

Two independent sufficient explanations can coexist: (i) higher I lacks an immediate positive relative reproductive return even with visitors restored, (ii) high-I alleles needed for the target have vanished. **Do not force every failed finite-H history into only these two causes.** States with both criteria permissive can fail because of finite sampling, drift, short horizon, frequency dependence or unforeseen model states. Report these as finite-time nonrealization / unresolved, never as a third proof of irreversibility. Population extinction is distinct.

### Candidate no-return clock, not a demonstrated tipping point

`T_E=35` is the *artificially imposed* time that all visitors are removed, without repopulation, on the historical declining regime. Earlier sparse visitors must not be called permanent extirpation.

A future confirmatory `t^*` requires **predeclared probability threshold**, independently resolved founder×visitor uncertainty, repeatable failure at later t and adequately long H, with positive return selection separately verified. A time-point effect in this sparse pilot is only a **screened time-specific recovery frequency**, not `t^*`. No extrapolation past the last checkpoint or from geological island age to time since loss.

## Micro-pilot intervention and resource cap

- Import the **unchanged** finite Model3 `reproduce` and `advance` operators from `scripts/model3_island`. No new sexual-system loci, inbreeding-load genetics, or density/finite equality assumptions.
- Read `data/design/model3_island_v2.json` for Config; explicit override: `K=48`, adult survival 0, delayed selfing, assurance cost 0.5, A-fixed=0.5 versus A-evolving, selfed-depression 0.5, per-allele mutation 0 and plant seed immigration 0.
- Two artificial founders (48 diploid plants each; I from {0.375,0.5,0.625}) crossed with two independent exogenous visitor histories. Keep initial genetic states identical for both historical policy assignments. Historical functional visitors: six until t=5, one during 5..34, **none starting T_E=35**; duration 45 updates.
- Retain complete in-memory `PlantState` at checkpoint t=10,30,45, with ID, genotype, origin, mutation marks and birth census. Checkpoint t=10 and 30 are before artificial T_E; t=45 is after.
- For every occupied or extinct checkpoint in each of **2×2×2 = 8** matched historical paths, branch into 25 additional reproductive updates with constant, externally imposed **six functional visitor types** vs continued absence, each with 2 independent future streams. This imposes actual *visitor availability*, not just a rate of hypothetical arrivals.
- Future policies: (a) historical fixed 0.5 remains fixed; (b) historical evolving A continues evolving; (c) from historical evolving A states, set expressed A to their current population mean without modifying standing A genotypes (freezing at reached A). This third future intervention is **conditional on the evolved historical state**, NOT an independently randomized historical treatment.
- Maximum intended biological paths: **8 history + 144 future trajectories** (2×2 founder–visitor blocks × 3 t × 2 visitor futures × 2 RNG repeats × 3 future-A policy combinations); 360 history updates + 3,600 continuation updates. If a checkpoint is extinct, any attained-A value is undefined; represent that arm as structurally ineligible, not as a numeric A=0.5 substitute. All initially randomized history paths still count in unconditional comparisons.
- Save the complete casewise readout with source code, protocol and design SHA256, refuse file overwrite. This is the **maximum exploratory cap**, not a power calculation. Four independent founder×visitor blocks cannot provide precise population-wide effect or a formal `t^*`.
- Do not treat 144 nested follow-on paths as 144 independent islands. Repeated future RNGs estimate conditional futures from four original block pairs; expand only under a separate protocol and #585 design-power gate.

## Existing evidence boundaries

- The frozen Q1 model counterexample shows I may decline with expressed assurance 0.5 held constant. It does NOT demonstrate floral change in dioecious plants or absence of any selfing.
- The 2,304 original Q3 paths show upper-I support exclusion in **1,455/2,304**, with 758 before and 697 at I fixation. The **703/2,304** old finding refers to lack of LOW-I alleles for *further decline*, not recovery. Neither is a pollinator-return result, pre-extirpation clock, or causal comparison of evolving vs fixed historical A.
- The existing one-time **investment-allele variation restoration** in 64 fixed histories concerned another, lower-I target, not restoring pollinators and high-I expression; it cannot substitute for this study.
- Large-scale island dioecy and colonization filtering are **not** part of the present Article causal test. Save as later research; do not add a new broad Q2.

## Exit gate

Check new source/test integrity and CI. Separately derive exact checkpoint allelic upper bounds, conditional state outcomes and unconditional policy denominators. If the real restored-visitor local marginal return is nonpositive at most states, a genetic no-return conclusion is not warranted there. A confirmatory `t^*`, ecological fitness assay, crossed power, multiple settings and independent observation-based comparisons are required **before** interpreting the proposed new main figures as established. This protocol is a *prospective exploratory* screen only.
