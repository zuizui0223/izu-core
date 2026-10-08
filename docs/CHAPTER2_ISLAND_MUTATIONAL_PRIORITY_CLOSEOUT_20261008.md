# Mutational access order, ecological payoff and island persistence — 2026-10-08 closeout

**Scientific status:** The temporal-priority extension is **not established**. A directionally appealing four-history exploratory result **failed independent 16-history confirmation**. A follow-up experiment which equalized the duration of mutational supply returned a zero pooled descriptive contrast. This is a meaningful falsification boundary, not a reason to retune seeds, costs or thresholds.

## Why the question was worth testing

The existing prospectively frozen four-setting assay merged as PR #411 found: under sustained shortage of visiting pollinator types, floral investment still declines when assurance-capacity evolution is blocked, while allowing assurance to evolve compresses the between-environment investment difference. Most of that compression arose from additional loss of floral investment in the **higher-pollination** environment. This result is distinct from, and stronger than, the order hypothesis.

A new PR #413 extension then found under a fixed, deliberately stressful post-switch environment that allowing assurance evolution can alter **historically conditioned population persistence**. Its pooled new-32-history gate passed, but the demographic stress range was chosen following exposed exploratory pilot screens; survival is conditional on an artificial eight-individual bottleneck, jointly reduced ovule budget and density-dependent pollen delivery. The 64-history first-generation payoff joint gate also **failed 1 of 5**; do not relabel it.

The next question was whether **which of the two evolutionary responses could occur first** would itself determine that persistence advantage. New experiments manipulated time of mutational access for inherited floral investment (`I`) and reproductive assurance capacity (`A`), on identical founder genomes initially fixed at `I=A=0.5`. Matching-locus variation was preserved. The normal population dynamics and Mendelian inheritance were never replaced with prescribed trait trajectories.

## Experiment 1 — independent16 *failed* its frozen confirmation rule

The first pilot crossed four reproductive settings × four access schedules (A first, I first, both early, both delayed) × four independent new visitor histories × two nested demographic repeats × near/far historical visitor regimes × eight postshock stress environments. Its 256 ancestral groups produced 2,048 postshock trajectories. The initial 150-update mutation gate held in all groups.

- Delayed selfing: A-first minus I-first interaction on the far-history persistence advantage **+0.0938**.
- Prior selfing: **+0.1563**.
- Pollen discount: **−0.0938**.
- Direct assurance cost: **−0.0313**.
- Equal four-setting mean: **+0.0313**.

This was exploratory, and early-access traits had mutation supply for 400 updates versus 250 for late-access traits. The positive prior vs negative pollen-discount contrast generated **one new, independently frozen test** using 16 entirely new visitor histories, one demographic repeat, 512 historical groups and 4,096 postshock trajectories. See `data/design/chapter2_island_mutational_priority_independent16_20261008.json`.

**Frozen independent16 result: FAIL.** The expected difference between the prior-selfing priority interaction and the pollen-discount priority interaction was **−0.08594**, 95% history bootstrap **[−0.27344, +0.09375]** (the preregistered rule required a positive mean and lower bound > 0).

| Reproductive setting | Exploratory 4-history priority effect | Independent16 priority effect | Independent16 95% bootstrap |
|---|---:|---:|---:|
| Delayed control | +0.0938 | −0.0234 | [−0.1094, +0.0547] |
| Prior selfing | +0.1563 | −0.0469 | [−0.1953, +0.1094] |
| Pollen discount | −0.0938 | +0.0391 | [−0.1250, +0.1953] |
| Direct assurance cost | −0.0313 | 0.0000 | [−0.0781, +0.1016] |

These intervals are over the **16 independent visitor histories**, not over 4,096 cases. No setting-specific interval excludes zero. This experiment rejects the proposal to promote a reproducible prior-versus-discount advantage from the initial four-history sample. It does not prove all priority effects are exactly zero.

## Experiment 2 — balanced mutational opportunity

The previous mutation-access design combined arrival order and a **150-generation difference in available mutational-supply duration**. This follow-up declared equal total supply time *before new outcomes* in `data/design/chapter2_island_mutational_priority_balanced_20261008.json`.

Each schedule used three phases of 150, 150 and 100 generations:

- A first: A only, then I only, then both.
- I first: I only, then A only, then both.
- Both early: both, then neither, then both.
- Both late: neither, then both, then both.

The matching/access locus remained mutable throughout. **Both focal traits had exactly 250 updates of mutational supply** under every schedule. Inherited alleles from a previous phase could still be selected and segregated later; no phenotype or genome was reset between phases. This controls the *duration of mutational input*, but not the age of alleles under selection.

Four wholly new visitor histories × two nested repeats × four settings × near/far prehistories × four schedules yielded another 256 ancestral groups and 2,048 postshock trajectories. All initial locked-locus checks passed.

| Reproductive setting | Balanced A-first − I-first effect on far-history persistence advantage |
|---|---:|
| Delayed control | +0.0156 |
| Prior selfing | +0.0313 |
| Pollen discount | +0.0469 |
| Direct assurance cost | −0.0938 |
| **Four-setting average** | **0.0000** |

The four individual histories remain variable; this is a **descriptive pilot**, not an independent second confirmation of zero effect.

## Island ecological meaning and boundaries

**Supported model-level causal spine:** visitor-replenishment history changes pollen receipt/export and costs, which changes local evolutionary fitness components. Heritable evolutionary responses then alter the same payoff balance; allowing assurance evolution may mask geographical investment divergence and, under the previously tested synthetic bottleneck, modify subsequent persistence.

**Not established:** universal assurance-first evolution, a direct causal role of phenotypic sequence in persistence, a general adaptive basin created by mutation priority, or a measured benefit of selfing evolution in actual island plant populations. The independent16 failure is especially important: a sign pattern from four histories cannot be used as proof of a broader mating-mechanism interaction.

**Future mechanism-led empirical distinction:** island phenotypic similarity can arise from arrival/establishment filters, convergence after establishment, or counteracting within-lineage evolution. To distinguish them, measure founder/ancestral lineage states, pollinator visit effectiveness (not visitor richness alone), viable selfed progeny, viable outcrossed maternal progeny, pollen-export fitness, allocation costs and demographic recruitment. Species-level trait means or pollen-deficit fractions alone do not close the causal chain. No current model coordinate is fitted to kilometres, island area, particular taxa or calendar years.

**Workflow decision:** retain PR #413 as Draft until technical replay and claim-boundary audit are complete. Do not merge these bounded results into the established PR #411 main manuscript as generalized evolutionary sequence or island rescue. Continue the validated payoff/selection and breeding-system feedback argument, treating sequence as a secondary, setting- and history-dependent diagnostic.

## Traceable evidence

- Frozen protocols: `data/design/chapter2_island_mutational_priority_pilot_20261008.json`, `data/design/chapter2_island_mutational_priority_independent16_20261008.json`, `data/design/chapter2_island_mutational_priority_balanced_20261008.json`.
- Machine-readable results: corresponding `data/results/chapter2_island_mutational_priority_*.json` files; original independent16 explicitly marked FAILED.
- Offline original-source data archives (not deposited publicly): `izu_core_mutational_priority_pilot_20261008.zip` SHA-256 `b95e6a798d45d0034c947ac59df7b5a32029d08174f8078d28bc797948957e94`; `izu_core_mutational_priority_independent16_20261008.zip` SHA-256 `28b03fc0ea5a20e8f5bd9b2b9e54ae8e3873f3fca9c8af5bae40d40099d57a28`; balanced archive SHA-256 `758830ecdcd168a49d733037f4d985d98a2dda4b1bf38625e257774d98988a7e`.
- The archived prior biological source ZIP SHA-256 was `71a1b1d9c4d683b874c989fa7768a14e72c5353063d8213cbe42f42cd37473d4`. Local run source, full cases, checksum manifests and readouts are included in the three archives; the independent repository replay workflow has not yet been declared successful.
