# Chapter 3 programme: reproductive assurance and the evolutionary recoverability of floral investment

**2026-10-17. STATUS: CONCEPT/IDENTIFICATION DESIGN ONLY — NOT PREREGISTERED, NOT EXECUTED, NO NEW BIOLOGICAL HISTORIES, NO SUBMISSION.**
Parent source: main after Chapter 2 [PR #587](https://github.com/zuizui0223/izu-core/pull/587), merge commit 439099ca6e3b8137f7884132f143d56d5e72e8be. This is a proposal for a **separate** study; the Ecology Letters Letter's Q1–Q4 original source results, manuscript and registered decisions are not changed. This document must **not** be mistaken for authorization to run confirmatory simulations.

## Thesis architecture and main question

- **Ch1, world island plants:** geographic isolation is associated with recurrent reproductive-assurance function and geographically contingent floral traits, not a single universal syndrome. Existing field data do not identify a global pollinator-mediated mechanism or a historical time of pollinator loss.
- **Ch2, the Ecology Letters Letter:** disabling assurance-capacity evolution at expressed A=0.5 does not prevent investment reduction within the registered Model 3 conditions. Temporal A-first precedence and causal necessity are distinct.
- **Ch3, proposed independent recoverability study:** **Can the ability of a finite plant population to re-evolve high floral investment disappear before local pollinator disappearance, and does allowing reproductive assurance to evolve accelerate or delay this loss?** Test whether the contrast operates through high-investment genetic support, a change in selection after restoration, or finite demographic survival.

Do not redefine a failed restoration over H updates as literal permanent irreversibility. Do not confuse the initiation of declining investment, a fixed genetic locus, genetic inability to reach a *specified high-I target*, low-probability functional recovery, or population extinction.

Working causal tension: delayed autonomous selfing supplies private maternal reproductive insurance; a change in focal floral investment can affect other conspecific mothers through pollen transfer (a documented **context-dependent source-ledger externality**, **not** a confirmed persistent public-goods-to-extinction mechanism). Each proposed causal path can help, harm, or have no effect.

## Original source evidence: exact scope and the directional error to avoid

| Existing registered/model-internal result | What is supported | What Ch3 must NOT inherit as a new result |
| --- | --- | --- |
| Original Q1, four mating settings and fresh founders | A capacity evolution is not necessary for the tested low-replenishment I decline; original compression 4/4, fresh-founder attenuation 3/4 | Not absence of realized selfing: fixed expressed A=0.5 still allows selfing |
| Q2 original one cost-bearing delayed setting | A-first in 51/64 independent visitor histories at founder-relative threshold .05 sustained 20 updates | Not universal A-first, natural mutation chronology, or necessity for future trapping |
| Q2 assigned-order demographic experiments | Small/practically equivalent imposed **expression schedules** in original contrasts, other primaries inconclusive | Not a manipulation of naturally evolved allele-order |
| Q3 access source cohort | 703/2,304 histories lose standing support for a **further DECREASE** in I before I fixation, with no I mutation and no seed immigration | Not evidence that the **HIGH-I** alleles needed for recovery have been lost in 703 histories |
| Q3 fixed-state restoration | Replacing all pairs [v,v] by [v−1/16,v+1/16] changes support, variation and heterozygosity together, with some paired terminal I responses; no visitor restoration | Not a pure support-only intervention or general proof of genetic/temporal irreversibility |
| Q4 pilot-informed independent32 stress | Integrated registered A-evolvability × past-visitor occupancy interaction **+0.1083984375** [0.0654296875, 0.1513671875]; +0.15234375 belongs to delayed-control setting alone | Not general +15.2 pp survival rescue; A evolvability CONTINUES in the future, K/fecundity/pollen were jointly shocked, and no order mediation is identified |
| Previous common-environment test | After 200 distinct historical updates, trait differences remain after 800 common-environment updates under some positive-mutation settings | This is finite-horizon historical memory, not proof that recovery is impossible forever |
| Ch1 data | Island traits and pollination architecture proxies, plus distinct pollen-supplementation observations | Flower syndromes do not identify current effective pollinator identities, geological island ages do not identify time since pollinator disappearance |

Original source pointers:
- [Primary manuscript decision](audits/CHAPTER2_MAIN_HYPOTHESIS_DECISION_20261017.json)
- [Original sequence result](../data/results/chapter2_1005_confirmatory_replication_20261006.json)
- [Q3 raw-source access diagnosis](../data/results/directional_access_20261013/READOUT.json)
- [Q3 restoration conditional futures](CHAPTER2_RESTORATION_CONDITIONAL_FUTURES_RESULTS_20261014.md)
- [Q4 independent32 readout](../data/results/chapter2_island_demographic_independent32_20261008.json)
- [Historical-memory and novelty audit](MODEL3_MUTATION_HISTORY_NOVELTY_20261004.md)
- [Floral investment externality feasibility NO-GO](CHAPTER2_INVESTMENT_COMMONS_PERSISTENCE_FEASIBILITY_20261010.md)
- Ch1 active selector: https://github.com/zuizui0223/island/blob/main/config/chapter1_submission_current.json

## Three distinct failure mechanisms and two distinct time coordinates

**Ecological lock**: under the restored visitor community, the relevant high-investment change is not selectively beneficial at the saved plant state. Assay maternal, paternal, and selfed returns; do not infer sign from visitor count or use a fixed A state with a latent A genotype as if it were expressed.

**Structural genetic lock**: in a no-I-mutation/no-I-immigration finite diploid model, let S_I(t) be the set of investment allele values in surviving plants. Mendelian transmission gives S_I(t+1) subset of S_I(t) along an occupied lineage. Since expressed I is the mean of two alleles, a *predeclared* target I_star is impossible for descendants whenever max S_I(t) < I_star (even though positive expressed variance can remain). This is a **sufficient impossibility condition**; max S_I(t) >= I_star does NOT guarantee realizable threshold crossing, timely selection, viable pairing, or persistence. In Ch3 this is the **HIGH-I** allele direction, the opposite of the earlier 703 low-I losses. Mutation, introgression/seed immigration, or an intentional genetic-restoration policy remove this structural no-reopening argument.

**Finite-time nonrealization**: selection for high I and high-I allele support can both be present, yet an occupied finite population may not recover within a fixed H-update horizon. Failure by H is not infinite-time impossibility or necessarily an attractor.

**Pollinator loss clock** T_E: the extirpation/exposure schedule must be externally imposed and declared, e.g. staged visitor-function decline followed by permanent absence/zero arrival after T_E. The endogenous Model 3 visitor process can have temporary years with zero visitors and subsequent recolonization: first year at zero is NOT the permanent disappearance time. Report pollinator ID count, functional effective pollen, and composition separately.

**Recoverability clock** T_R: start from **identical SAVED genotype/census/visitor-history state at each scheduled checkpoint** t, assign a common restored visitor regime, and calculate success probability after future stochastic evolution. A first transient low estimate should not be relabelled an irreversible threshold; predeclare confidence/uncertainty and a sustained-crossing convention, report the complete time curve, and allow nonmonotonicity.

## Candidate predeclared outcomes (NOT frozen or powered yet)

At checkpoint t, with founder/visitor history h, baseline founder information B, assurance policy a, and restored visitor regime E0, define

    R_a(t;H,L,I_star) =
        P( alive AND I reaches >= I_star for L consecutive censuses
           by t+H | saved full state at t, do(E_future=E0), policy a ).

Here the probability is over independently named FUTURE biological random streams. Predefine target I_star, recovery horizon H, consecutive length L, and the minimum ecological effect worth detecting BEFORE new confirmatory outcomes. Confirm that the founder allelic support makes the target reachable in at least the intended baseline cases. Source high-replenishment is still pollen-limited and **not automatically a floral-investment-favouring restoration**: also assay whether high-I selection is actually positive after E0 at each state.

Report at least four different quantities, never substituting one for another:

1. **Unconditional occupied-and-recovered probability** R_a, with extinction a recovery failure (no zero-filled extinct trait).
2. **Probability of occupancy to H** S_a and **recovery conditional on occupancy** C_a. Conditional contrasts may be selected by survival and are NOT an unconditional treatment effect.
3. **High-I support-loss incidence** with **competing extinction** before/after the loss. No double-counting extinct branches as a genetic loss.
4. **Time-to-threshold summary** or curve-based area/integrated loss and a strict T_E comparison only under predeclared no-return-point convention. No claim of a single irreversible tipping time if the curve recovers or mutation reopens genetic access.

Main randomization: cross **independent founder genotypes × independent exogenous visitor histories** with treatments matched on named histories; new demographic/future draws are NESTED within that cross and are not independent new islands. Standardized interventions must keep matched random-state semantics and original phenotype-at-time-zero parity.

A-only, I-only, both-events, tie and neither categories must retain an all-start denominator. They are distinct from restoration success or occupancy and are optional mediators/secondary observations, not substitutes for the recovery estimand.

## Proposed causal arms — freeze only after independent pilot and feasibility gate

At the **start of historical evolution** compare at least:

- E: assurance capacity A can evolve (native allele transmission/mutation, declared mating context).
- F: expressed A held at 0.5; **selfing still occurs**. This isolates capacity evolvability compared with E under the declared baseline.
- Z, OPTIONAL distinct intervention: actual autonomous selfing expression set to zero. NOT a synonym for F; it changes reproduction and potentially population extinction.

Each historical branch is replayed after the SAME externally forced restoration dates, but the resulting saved genomes/census sizes can differ legitimately. To examine mechanisms at a specific saved state, add paired **post-checkpoint** interventions independently from historical treatments:

- P: pollinators restored only, inherited genotypes unchanged;
- PG: same pollinator return plus explicitly defined high-I access restoration;
- G: high-I access restored without pollinator return (control for ecological selection);
- Aafter: change future assurance-expression/evolution policy only, without claiming a natural order intervention;
- TECHNICAL no-edit replay: exactly equal genotypes/RNG outcomes when no intervention is performed.

Restoring a high-I allele generally changes frequencies, genotype combinations, available support and/or initial mean; these are not independently manipulated by a naive [v−h,v+h] reset. Use separately defined interventions and matched controls when feasible; stop rather than asserting "allele support alone causes recovery" if the parameters cannot be matched.

When survival differs between E and F, the strong biological test is whether one policy raises S but decreases C or structural high-I availability: a possible **lifeboat for survival and ratchet against recovery**. The opposite, both favorable, both adverse, context reversal and no-effect are competing permitted outcomes.

## Exploration gate and confirmation gate

**Stage 0 — source and precedent review (read-only):** verify original state snapshots by full genotype checksum, visitor histories, mutation policy, authorizations and applicability; check prior selfing/irreversibility models including Acoca-Pidolle (2025) and Lepers et al. (2014). Existing Q3 restoration is mostly about LOW-I re-decline and was not the planned HIGH-I recoverability test.

**Stage 1 — outcome-known PILOT only:** from a prespecified subset of already-authenticated original states, compute source-only high-I support, visitor zero-run / effective-service histories, and the restored-state **selection sign** first. Before launching any restored future branches, distinguish technical recoverability from a positive-return environment; establish acceptable founder target coverage and compute cost estimates. If selected old states then get future replay, findings remain exploratory; no promotion to confirmation.

**Stage 2 — registered confirmation:** freeze new independent founder × visitor labels, A policies, T_E schedule, I_star, H,L, restoration definition, minimum effects, multiple-testing family, seed namespaces, archive/checkpoint checksums, stop/failure rules and full computational budget. Apply the cross-axis precision/joint-power gate merged in [PR #585](https://github.com/zuizui0223/izu-core/pull/585) and require source-independent pilot data. **NO launch** if time and high-I access are not identifiable or events are too rare at the stated budget.

**Stage 3 — mechanism and robustness:** no-I mutation first for a mathematical support-loss bound; separately test positive I mutation for *finite-horizon* recovery only, four mating conditions, founder variants, inbreeding depression, K and pollen-background decoupling, and genuinely distinct simplified model. Numerical changes to old runs do not count as independent biological replication.

**Stage 4 — external test only AFTER model winner and data eligibility frozen:** the Chapter 1 world island universe contains plant trait/assurance descriptors and separate current experimental pollen-limitation data, but not a universal matched island geological age, time since actual pollinator loss, direct pollinator identity or historical founding time. Geological island age != colonization age != pollinator disappearance time. Pollination-architecture "large bee"/"butterfly" descriptors are **NOT** actual pollinator identities. Before looking at outcomes, audit matched island-age/actual service/flower traits/taxonomic/geographic support and define an externally observable divergent prediction. Qualitative direction alone does NOT repair missing mechanistic observables; if no sufficient data, mark external test NOT IDENTIFIABLE, not a supported NEE result.

**Stage 5 — publication review:** only after the new work has independent evidence. Refer to the Chapter 2 Letter as antecedent without repeating its original data as independent NEE main results. The EGWE manuscript studies the sufficiency of state representations under fragmentation; this proposed study's endpoint is intervention-defined plant-side post-restoration recoverability. Their shared genetics/future language is not enough to claim separate novelty without distinct estimands and datasets.

## What would disconfirm or block the ambitious thesis

- T_R does not precede imposed visitor extirpation after uncertainty and full restoration calibration.
- E and F do not differ in high-I access or restored trajectories within the prespecified SESOI, even if the source chronologies differ.
- Differences are selection-lock only under restored pollen (high-I not favored), not loss of adaptive high-I alleles.
- Genetic support is present yet trajectories mostly fail by H: finite-time nonrealization, not irreversible allelic lock.
- Positive mutation/immigration reopen support or long-enough future branches recover.
- The only favorable result is among survivor-selected states, while the unconditional effect is weak or reverses.
- The simpler model or at least one biologically motivated reproduction regime fails to preserve the direction.
- No complete, eligible empirical comparison exists; do not replace this with a geological-age correlation selected after seeing outcomes.

The desired headline **is not a required result**. Any of these outcomes can be a useful bounded mechanistic result; NEE journal suitability depends on the demonstrated novelty, generality and independent empirical support, not on relabelling a negative as success.

**No new run, data deposit, PR merge or submission authorization is given by this document.**
